import re
from typing import Any, Dict, Mapping, Optional


class CoinsPayError(Exception):
    """Base class of every error raised by this library."""


class APIError(CoinsPayError):
    """
    The API answered with an error: HTTP status 4xx or 5xx and a body
    ``{"error": {"code", "message", "details"}}``. Branch on ``code``: ``message`` is an
    English explanation and may change.
    """

    def __init__(
        self,
        status: int,
        code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message
        self.details = details
        self.headers: Dict[str, str] = dict(headers or {})

    def __repr__(self) -> str:
        return f"{type(self).__name__}(status={self.status}, code={self.code!r}, message={self.message!r})"

    @staticmethod
    def create(
        status: int,
        code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> "APIError":
        """The subclass that matches the HTTP status."""
        cls = _BY_STATUS.get(status, APIError)
        return cls(status, code, message, details, headers)


class InvalidRequestError(APIError):
    """400: the request is invalid; for ``VALIDATION_ERROR`` ``details`` maps field paths to reasons."""


class AuthenticationError(APIError):
    """401: the API key is missing, wrong or revoked."""


class PermissionDeniedError(APIError):
    """
    403: the key may not do this: ``KEY_ACCESS_DENIED`` (an invoices-only key),
    ``TEST_MODE_UNSUPPORTED`` (a test key), ``IP_NOT_ALLOWED`` (see ``details["ip"]``),
    ``SHOP_DISABLED``.
    """


class NotFoundError(APIError):
    """404: no such object in this shop."""


class ConflictError(APIError):
    """409: ``IDEMPOTENCY_CONFLICT``, or ``INVOICE_NOT_OPEN`` (see ``details["status"]``)."""


class UnprocessableError(APIError):
    """422: the payout cannot be made: ``INSUFFICIENT_BALANCE``, ``FUNDS_NOT_MATURE``, ``BELOW_MINIMUM`` and others."""


class RateLimitError(APIError):
    """429: too many requests."""

    @property
    def retry_after(self) -> Optional[int]:
        """Seconds to wait before retrying, if the API said so."""
        header = self.headers.get("retry-after", "")
        if re.fullmatch(r"\s*\d+\s*", header):
            return int(header)
        value = (self.details or {}).get("retry_after")
        if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
            return value
        return None


class ServiceUnavailableError(APIError):
    """503: the service is temporarily unavailable; retry later."""


_BY_STATUS = {
    400: InvalidRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    422: UnprocessableError,
    429: RateLimitError,
    503: ServiceUnavailableError,
}


class APIConnectionError(CoinsPayError):
    """
    The request did not get an answer. With ``sent`` false it never reached the API
    (connection refused, DNS failure), so any request is safe to retry. With ``sent`` true it
    may have been processed.
    """

    def __init__(self, message: str, sent: bool) -> None:
        super().__init__(message)
        self.sent = sent


class APITimeoutError(APIConnectionError):
    """No answer within the timeout; the request may have been processed."""

    def __init__(self, message: str) -> None:
        super().__init__(message, sent=True)


class InvalidResponseError(CoinsPayError):
    """The answer was not the JSON the API sends, for example an HTML error page of a proxy or a redirect."""

    def __init__(self, message: str, status: int) -> None:
        super().__init__(message)
        self.status = status


class SignatureVerificationError(CoinsPayError):
    """The webhook signature is missing, malformed, too old or does not match."""

    MESSAGES = {
        "missing": "No x-cpay-signature header",
        "malformed": "The x-cpay-signature header is malformed",
        "stale": "The webhook signature is too old or from the future",
        "mismatch": "The webhook signature does not match the body and secret",
    }

    def __init__(self, reason: str) -> None:
        super().__init__(self.MESSAGES[reason])
        self.reason = reason
        """``missing``, ``malformed``, ``stale`` or ``mismatch``."""
