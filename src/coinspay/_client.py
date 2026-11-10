import platform
import re
from decimal import Decimal
from typing import Any, Callable, Dict, List, Mapping, Optional

from . import models
from ._http import (
    Requestor,
    ResponseInfo,
    Transport,
    UrllibTransport,
    check_idempotency_key,
    default_sleep,
    new_idempotency_key,
    normalize_base_url,
)
from ._model import NotGiven
from ._operations import OPERATIONS
from ._resource import Page
from ._resources import Addresses, Balances, Chains, Currencies, Deposits, Invoices, Payouts, ShopResource
from ._version import __version__

UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.IGNORECASE)
PATH = re.compile(r"/[\w\-./]*")


class Client:
    """
    Client of the CoinsPay API::

        coinspay = coinspay.Client(os.environ["COINSPAY_KEY"], "https://pay.example.com")
        invoice = coinspay.invoices.create(currency="USD", amount="49.90", reference="order-1042")
        redirect(invoice.pay_url)

    :param api_key: API key of the shop: ``cpk_…``, or ``cpk_test_…`` for test mode. Keep it on your server.
    :param base_url: The dashboard origin (``https://pay.example.com``) or the API address ending in ``/api/v1``.
    :param timeout: Seconds for each socket operation of an attempt; 30 by default.
    :param max_retries: Retries after failures that are safe to retry; 2 by default, 0 turns them off.
    :param max_retry_delay: The longest pause before a retry in seconds; a longer ``Retry-After`` fails at once.
    :param allow_insecure_http: Allows plain http to hosts other than localhost, for a test stand.
    :param transport: Your own HTTP transport; ``UrllibTransport`` by default.
    :param headers: Headers sent with every request.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str,
        *,
        timeout: float = 30.0,
        max_retries: int = 2,
        max_retry_delay: float = 5.0,
        allow_insecure_http: bool = False,
        transport: Optional[Transport] = None,
        headers: Optional[Mapping[str, str]] = None,
        _sleep: Optional[Callable[[float], None]] = None,
    ) -> None:
        if not isinstance(api_key, str) or api_key.strip() == "":
            raise ValueError("api_key is required")
        api_key = api_key.strip()
        if re.search(r"[\s\x00-\x1f\x7f]", api_key):
            raise ValueError("api_key contains spaces or control characters")
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or timeout <= 0:
            raise ValueError("timeout must be a positive number")
        if isinstance(max_retries, bool) or not isinstance(max_retries, int) or max_retries < 0:
            raise ValueError("max_retries must be a non-negative integer")
        if isinstance(max_retry_delay, bool) or not isinstance(max_retry_delay, (int, float)) or max_retry_delay < 0:
            raise ValueError("max_retry_delay must not be negative")

        self._base_url = normalize_base_url(base_url, allow_insecure_http)
        self._test_mode = api_key.startswith("cpk_test_")
        self._requestor = Requestor(
            api_key,
            self._base_url,
            transport or UrllibTransport(),
            timeout=float(timeout),
            max_retries=max_retries,
            max_retry_delay=float(max_retry_delay),
            headers=headers or {},
            sleep=_sleep or default_sleep,
            user_agent=f"coinspay-python/{__version__} python/{platform.python_version()}",
        )

        self.invoices = Invoices(self)
        self.addresses = Addresses(self)
        self.deposits = Deposits(self)
        self.balances = Balances(self)
        self.payouts = Payouts(self)
        self.shop = ShopResource(self)
        self.chains = Chains(self)
        self.currencies = Currencies(self)

    @property
    def base_url(self) -> str:
        """The API address requests go to, ending in ``/api/v1``."""
        return self._base_url

    @property
    def test_mode(self) -> bool:
        """True for a test key (``cpk_test_…``): invoices only, paid without money."""
        return self._test_mode

    @property
    def last_response(self) -> Optional[ResponseInfo]:
        """Status, headers and ``replayed`` of the last answer."""
        return self._requestor.last_response

    def __repr__(self) -> str:
        return f"coinspay.Client(base_url={self._base_url!r}, test_mode={self._test_mode})"

    @staticmethod
    def new_idempotency_key() -> str:
        """A random idempotency key, for when there is no natural one such as an order or payout number."""
        return new_idempotency_key()

    def request(
        self,
        method: str,
        path: str,
        *,
        query: Optional[Dict[str, Any]] = None,
        body: Any = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """
        Any API request, for methods this version of the library does not know yet.
        ``path`` is relative to ``/api/v1``, for example ``/invoices``. Returns the parsed JSON.
        """
        if method not in ("GET", "POST"):
            raise ValueError("method must be GET or POST")
        if not isinstance(path, str) or not PATH.fullmatch(path) or any(part in (".", "..") for part in path.split("/")):
            raise ValueError(f"Bad API path: {path!r}")
        key = check_idempotency_key(idempotency_key) if idempotency_key is not None else None
        return self._requestor.send(
            method,
            path,
            query=query,
            body=body,
            retry="safe" if method == "GET" else ("idempotent" if key else "unsafe"),
            idempotency_key=key,
            timeout=timeout,
            max_retries=max_retries,
            headers=headers,
        )

    def _call(
        self,
        operation: str,
        id: Optional[str],
        params: Dict[str, Any],
        extra: Optional[Dict[str, Any]],
        idempotency_key: Optional[str],
        *,
        timeout: Optional[float],
        max_retries: Optional[int],
        headers: Optional[Dict[str, str]],
    ) -> Any:
        spec = OPERATIONS[operation]
        path = spec["path"]
        if "{id}" in path:
            if not isinstance(id, str) or not UUID.fullmatch(id):
                raise ValueError(f"id must be a UUID, got {id!r}")
            path = path.replace("{id}", id.lower())

        values = {key: value for key, value in params.items() if not isinstance(value, NotGiven)}
        if spec["params"] is not None:
            _check_keys(values, spec["params"], "")
            for decimal_path in spec["decimals"]:
                values = _decimals(values, decimal_path.split("."), "")
        if extra:
            # Fields this version of the library does not know yet: sent as given.
            values.update(extra)

        if spec["retry"] == "idempotent":
            if idempotency_key is not None:
                idempotency_key = check_idempotency_key(idempotency_key)
            elif spec["idempotency"] == "required":
                # A random key here would let a repeated call send the money twice.
                raise ValueError(f"{operation} needs idempotency_key: take it from your own record, so that a repeat never sends twice")
            else:
                idempotency_key = new_idempotency_key()

        data = self._requestor.send(
            spec["method"],
            path,
            query=values if spec["method"] == "GET" else None,
            body=values if spec["method"] == "POST" else None,
            retry=spec["retry"],
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=headers,
        )

        cls = getattr(models, spec["returns"])
        if spec["page"]:
            items = data.get(spec["page"]) if isinstance(data, dict) else None
            return Page([cls.from_dict(item) for item in items or [] if isinstance(item, dict)], data.get("next_cursor"))
        if spec["unwrap"]:
            data = data.get(spec["unwrap"]) if isinstance(data, dict) else None
        if spec["many"]:
            return [cls.from_dict(item) for item in data or [] if isinstance(item, dict)]
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected answer of {operation}")
        return cls.from_dict(data)


def _check_keys(values: Any, allowed: Dict[str, Any], where: str) -> None:
    """Unknown keys are typos: the API would silently ignore them."""
    if not isinstance(values, dict):
        raise TypeError(f"{where.rstrip('.') or 'parameters'} must be a dict")
    for key, value in values.items():
        if key not in allowed:
            raise TypeError(f"Unknown parameter {where}{key}; pass new API fields in extra_body or extra_query")
        nested = allowed[key]
        if isinstance(nested, dict) and value is not None:
            if isinstance(value, list):
                for index, item in enumerate(value):
                    _check_keys(item, nested, f"{where}{key}[{index}].")
            else:
                _check_keys(value, nested, f"{where}{key}.")


def _decimals(value: Any, segments: List[str], where: str) -> Any:
    """Decimal → plain string; floats are refused: 0.1 + 0.2 is not what you meant."""
    if value is None:
        return None
    if not segments:
        if isinstance(value, Decimal):
            if not value.is_finite():
                raise ValueError(f"{where} must be a finite number")
            return format(value, "f")
        if isinstance(value, str):
            return value
        raise TypeError(f'{where} must be a decimal string such as "49.90" or a Decimal, not {type(value).__name__}')
    if not isinstance(value, dict):
        return value
    segment, rest = segments[0], segments[1:]
    many = segment.endswith("[]")
    name = segment[:-2] if many else segment
    if name not in value:
        return value
    prefix = f"{where}.{name}" if where else name
    copy = dict(value)
    if not many:
        copy[name] = _decimals(value[name], rest, prefix)
    elif isinstance(value[name], list):
        copy[name] = [_decimals(item, rest, f"{prefix}[{index}]") for index, item in enumerate(value[name])]
    return copy
