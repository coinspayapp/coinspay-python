import http.client
import json
import random
import re
import socket
import ssl
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Any, Callable, Dict, Mapping, Optional, Protocol

from ._errors import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    CoinsPayError,
    ConflictError,
    InvalidResponseError,
    RateLimitError,
)

IDEMPOTENCY_KEY = re.compile(r"[\x21-\x7e]{8,128}")


class HTTPResponse:
    """An HTTP answer as received."""

    def __init__(self, status: int, headers: Mapping[str, str], body: bytes) -> None:
        self.status = status
        self.headers = {name.lower(): value for name, value in headers.items()}
        self.body = body


class TransportError(Exception):
    """A transport got no answer; the client turns it into ``APIConnectionError`` or ``APITimeoutError``."""

    def __init__(self, message: str, *, sent: bool, timeout: bool = False, retryable: bool = True) -> None:
        super().__init__(message)
        self.sent = sent
        self.timeout = timeout
        self.retryable = retryable


class Transport(Protocol):
    """Sends one HTTP request. It must not follow redirects."""

    def send(self, method: str, url: str, headers: Dict[str, str], body: Optional[bytes], timeout: float) -> HTTPResponse:
        ...


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """A redirect would carry the API key to another address."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        return None


class UrllibTransport:
    """
    HTTP over the standard library. The timeout applies to each socket operation (connect,
    send, every read), not to the request as a whole. Proxies come from the usual environment
    variables (HTTPS_PROXY), or pass ``proxies``.
    """

    def __init__(self, *, ssl_context: Optional[ssl.SSLContext] = None, proxies: Optional[Dict[str, str]] = None) -> None:
        handlers = [urllib.request.HTTPSHandler(context=ssl_context or ssl.create_default_context()), _NoRedirect()]
        if proxies is not None:
            handlers.append(urllib.request.ProxyHandler(proxies))
        self._opener = urllib.request.build_opener(*handlers)

    def send(self, method: str, url: str, headers: Dict[str, str], body: Optional[bytes], timeout: float) -> HTTPResponse:
        request = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with self._opener.open(request, timeout=timeout) as response:
                return HTTPResponse(response.status, dict(response.headers.items()), response.read())
        except urllib.error.HTTPError as error:
            try:
                text = error.read()
            except socket.timeout as timeout:
                raise _transport_error(timeout, connecting=False) from timeout
            except (OSError, http.client.HTTPException):
                text = b""
            finally:
                error.close()
            return HTTPResponse(error.code, dict(error.headers.items()) if error.headers else {}, text)
        except urllib.error.URLError as error:
            # urllib wraps only what failed while connecting and sending the request.
            raise _transport_error(error.reason, connecting=True) from error
        except (OSError, http.client.HTTPException) as error:
            raise _transport_error(error, connecting=False) from error


def _transport_error(reason: Any, *, connecting: bool) -> TransportError:
    message = f"Could not reach the CoinsPay API: {reason}"
    if isinstance(reason, socket.timeout):
        return TransportError(message, sent=True, timeout=True)
    if isinstance(reason, ssl.SSLCertVerificationError):
        return TransportError(message, sent=False, retryable=False)
    if connecting and isinstance(reason, ssl.SSLError):
        return TransportError(message, sent=False, retryable=False)
    if connecting and isinstance(reason, (ConnectionRefusedError, socket.gaierror)):
        return TransportError(message, sent=False)
    return TransportError(message, sent=True)


class ResponseInfo:
    """What the API answered to a request, besides the body."""

    def __init__(self, status: int, headers: Dict[str, str], replayed: bool) -> None:
        self.status = status
        self.headers = headers
        self.replayed = replayed
        """
        True when a create request repeated an earlier one with the same idempotency key:
        the API returned the existing object (status 200) in its current state instead of
        creating a new one (201).
        """

    def __repr__(self) -> str:
        return f"ResponseInfo(status={self.status}, replayed={self.replayed})"


def new_idempotency_key() -> str:
    """A random idempotency key, for when there is no natural one such as an order or payout number."""
    return str(uuid.uuid4())


def check_idempotency_key(key: Any) -> str:
    if not isinstance(key, str) or not IDEMPOTENCY_KEY.fullmatch(key):
        raise ValueError("idempotency_key must be 8 to 128 printable ASCII characters without spaces")
    return key


class Requestor:
    """Sends API requests: headers, retries, errors."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        transport: Transport,
        *,
        timeout: float,
        max_retries: int,
        max_retry_delay: float,
        headers: Mapping[str, str],
        sleep: Callable[[float], None],
        user_agent: str,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url
        self._transport = transport
        self._timeout = timeout
        self._max_retries = max_retries
        self._max_retry_delay = max_retry_delay
        self._headers = dict(headers)
        self._sleep = sleep
        self._user_agent = user_agent
        # Per thread: a client shared by the threads of a web server must not mix the answers.
        self._local = threading.local()

    def __repr__(self) -> str:
        return f"Requestor(base_url={self._base_url!r})"

    @property
    def last_response(self) -> Optional[ResponseInfo]:
        """The answer to the last successful request of this thread; None after a failed one."""
        return getattr(self._local, "info", None)

    def send(
        self,
        method: str,
        path: str,
        *,
        query: Optional[Dict[str, Any]] = None,
        body: Any = None,
        retry: str,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        url = self._base_url + path
        if query:
            pairs = [(key, _query_value(value)) for key, value in query.items() if value is not None]
            if pairs:
                url += "?" + urllib.parse.urlencode(pairs, quote_via=urllib.parse.quote)
        # The same bytes on every attempt: the idempotency key is bound to the body.
        payload = _encode(body) if method == "POST" else None
        request_headers = self._build_headers(payload is not None, idempotency_key, headers or {})
        limit = self._max_retries if max_retries is None else max_retries
        attempt_timeout = self._timeout if timeout is None else timeout
        self._local.info = None

        attempt = 0
        while True:
            retryable_transport = True
            try:
                response = self._transport.send(method, url, request_headers, payload, attempt_timeout)
                data = _parse(response.status, response.body)
                if 200 <= response.status < 300:
                    self._local.info = ResponseInfo(response.status, response.headers, idempotency_key is not None and response.status == 200)
                    return data
                failure: CoinsPayError = _error(response.status, data, response.headers)
            except TransportError as error:
                failure = APITimeoutError(str(error)) if error.timeout else APIConnectionError(str(error), error.sent)
                failure.__cause__ = error
                retryable_transport = error.retryable
            except InvalidResponseError as error:
                failure = error

            # A retried cancel that finds the invoice cancelled: the first attempt went through.
            if (
                retry == "cancel"
                and attempt > 0
                and isinstance(failure, ConflictError)
                and failure.code == "INVOICE_NOT_OPEN"
                and (failure.details or {}).get("status") == "cancelled"
            ):
                return self.send("GET", re.sub(r"/cancel$", "", path), retry="safe", timeout=timeout, max_retries=max_retries, headers=headers)

            delay = self._retry_delay(failure, retry, attempt, retryable_transport) if attempt < limit else None
            if delay is None:
                raise failure
            self._sleep(delay)
            attempt += 1

    def _retry_delay(self, failure: CoinsPayError, retry: str, attempt: int, retryable_transport: bool) -> Optional[float]:
        status = failure.status if isinstance(failure, (APIError, InvalidResponseError)) else None
        hinted: Optional[int] = None
        if status == 429:
            # Rate limits act before the request is handled: any request may repeat.
            retryable = True
            hinted = failure.retry_after if isinstance(failure, RateLimitError) else None
        elif status == 503:
            retryable = True
        elif status in (502, 504):
            retryable = retry != "unsafe"
        elif isinstance(failure, APIConnectionError):
            retryable = retryable_transport and (not failure.sent or retry != "unsafe")
        else:
            retryable = False
        if not retryable:
            return None
        delay = float(hinted) if hinted is not None else 0.5 * 2**attempt * (0.75 + random.random() * 0.5)
        return None if delay > self._max_retry_delay else delay

    def _build_headers(self, has_body: bool, idempotency_key: Optional[str], extra: Mapping[str, str]) -> Dict[str, str]:
        headers = {name.lower(): value for name, value in {**self._headers, **extra}.items()}
        headers["accept"] = "application/json"
        headers["user-agent"] = self._user_agent
        headers["authorization"] = f"Bearer {self._api_key}"
        if has_body:
            headers["content-type"] = "application/json"
        if idempotency_key is not None:
            headers["idempotency-key"] = idempotency_key
        for name, value in headers.items():
            if "\r" in name + value or "\n" in name + value:
                raise ValueError(f"Header {name} contains a line break")
        return headers


def _query_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _encode(body: Any) -> bytes:
    if body is None or body == {}:
        return b"{}"
    return json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def _parse(status: int, body: bytes) -> Any:
    if 300 <= status < 400:
        raise InvalidResponseError(f"The CoinsPay API answered with a redirect ({status}); redirects are not followed", status)
    if body == b"":
        if 200 <= status < 300:
            raise InvalidResponseError(f"Empty answer with status {status}", status)
        return None
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        raise InvalidResponseError(f"The answer with status {status} is not JSON", status) from None


def _error(status: int, data: Any, headers: Dict[str, str]) -> CoinsPayError:
    error = data.get("error") if isinstance(data, dict) else None
    if not isinstance(error, dict) or not isinstance(error.get("code"), str):
        return InvalidResponseError(f"HTTP {status} without an API error body", status)
    message = str(error["message"]) if isinstance(error.get("message"), str) else str(error["code"])
    details = error.get("details") if isinstance(error.get("details"), dict) else None
    return APIError.create(status, error["code"], message, details, headers)


def default_sleep(seconds: float) -> None:
    time.sleep(seconds)


def normalize_base_url(value: Any, allow_insecure_http: bool) -> str:
    """The API address from the dashboard origin or the full address ending in ``/api/v1``."""
    if not isinstance(value, str) or value.strip() == "":
        raise ValueError("base_url is required")
    parts = urllib.parse.urlsplit(value.strip())
    if not parts.scheme or not parts.hostname:
        # Without the value: an API key passed here by mistake must not reach the logs.
        raise ValueError("base_url is not a URL; the arguments are (api_key, base_url)")
    if parts.query or parts.fragment or parts.username or parts.password:
        raise ValueError("base_url must not contain a query, a fragment or credentials")
    scheme = parts.scheme.lower()
    host = parts.hostname.lower()
    local = host in ("localhost", "127.0.0.1", "::1")
    if scheme != "https" and not (scheme == "http" and (local or allow_insecure_http)):
        raise ValueError("base_url must use https (http is allowed for localhost or with allow_insecure_http)")
    path = parts.path
    path = "/api/v1" if path.strip("/") == "" else path.rstrip("/")
    if not path.endswith("/api/v1"):
        raise ValueError("base_url must be the dashboard origin or end with /api/v1")
    netloc = f"[{host}]" if ":" in host else host
    if parts.port is not None:
        netloc += f":{parts.port}"
    return f"{scheme}://{netloc}{path}"
