"""Official Python library for the CoinsPay crypto payments API."""

from . import models, webhooks
from ._client import Client
from ._errors import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    AuthenticationError,
    CoinsPayError,
    ConflictError,
    InvalidRequestError,
    InvalidResponseError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ServiceUnavailableError,
    SignatureVerificationError,
    UnprocessableError,
)
from ._http import HTTPResponse, ResponseInfo, Transport, TransportError, UrllibTransport, new_idempotency_key
from ._model import NOT_GIVEN, Model, NotGiven
from ._operations import ERROR_CODES, ErrorCode
from ._resource import Page
from ._version import __version__
from .webhooks import UnknownEvent, construct_event, signature_header, verify_signature

__all__ = [
    "APIConnectionError",
    "APIError",
    "APITimeoutError",
    "AuthenticationError",
    "Client",
    "CoinsPayError",
    "ConflictError",
    "ERROR_CODES",
    "ErrorCode",
    "HTTPResponse",
    "InvalidRequestError",
    "InvalidResponseError",
    "Model",
    "NOT_GIVEN",
    "NotFoundError",
    "NotGiven",
    "Page",
    "PermissionDeniedError",
    "RateLimitError",
    "ResponseInfo",
    "ServiceUnavailableError",
    "SignatureVerificationError",
    "Transport",
    "TransportError",
    "UnknownEvent",
    "UnprocessableError",
    "UrllibTransport",
    "__version__",
    "construct_event",
    "models",
    "new_idempotency_key",
    "signature_header",
    "verify_signature",
    "webhooks",
]
