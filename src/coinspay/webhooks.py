"""
Webhooks: checks the signature of an event and turns it into an object::

    event = coinspay.webhooks.construct_event(request.body, request.headers.get("x-cpay-signature"), secret)
    if event.type == "invoice.paid":
        ...
"""

import hashlib
import hmac
import json
import math
import re
import time
from typing import Optional, Sequence, Union, cast

from ._errors import CoinsPayError, SignatureVerificationError
from ._model import Model
from .models import EVENT_CLASSES, WebhookEvent

SIGNATURE_HEADER = "x-cpay-signature"
"""Header with the signature: ``t=<unix>,v1=<hex>``."""
EVENT_HEADER = "x-cpay-event"
"""Header with the event type."""
DELIVERY_HEADER = "x-cpay-delivery"
"""Header with the event id; a repeated delivery carries the same id."""
DEFAULT_TOLERANCE = 300
"""Allowed clock difference in seconds, in both directions."""

Payload = Union[bytes, bytearray, memoryview, str]
_HEX = re.compile(r"[0-9a-f]{64}")


def _bytes(payload: Payload) -> bytes:
    if isinstance(payload, str):
        return payload.encode("utf-8")
    if isinstance(payload, (bytes, bytearray, memoryview)):
        return bytes(payload)
    raise TypeError("The webhook payload must be the raw body: bytes or str")


def verify_signature(
    payload: Payload,
    header: Union[str, Sequence[str], None],
    secret: Union[str, Sequence[str]],
    *,
    tolerance: int = DEFAULT_TOLERANCE,
    now: Optional[float] = None,
) -> None:
    """
    Checks the ``x-cpay-signature`` header and raises ``SignatureVerificationError`` if it does
    not hold.

    ``payload`` is the request body exactly as received (``request.body`` / ``request.data``),
    before ``json.loads``: the signature covers the bytes. ``secret`` may be a list: the old
    secret stops working at once when you replace it in the dashboard, so pass both while you
    roll the new one out.
    """
    if isinstance(tolerance, bool) or not isinstance(tolerance, (int, float)) or not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be a non-negative number of seconds")
    if header is not None and not isinstance(header, str):
        header = ",".join(header)
    if not header:
        raise SignatureVerificationError("missing")
    body = _bytes(payload)

    timestamp: Optional[str] = None
    signatures = []
    for piece in header.split(","):
        eq = piece.find("=")
        if eq <= 0:
            raise SignatureVerificationError("malformed")
        key, value = piece[:eq].strip(), piece[eq + 1 :].strip()
        if key == "t":
            timestamp = value
        elif key == "v1":
            signatures.append(value)
    if timestamp is None or not re.fullmatch(r"[0-9]+", timestamp) or not signatures or not all(_HEX.fullmatch(item) for item in signatures):
        raise SignatureVerificationError("malformed")

    # A timestamp of thousands of digits would not even convert to int; it is stale anyway.
    if len(timestamp) > 15:
        raise SignatureVerificationError("stale")
    t = int(timestamp)
    current = time.time() if now is None else now
    if abs(current - t) > tolerance:
        raise SignatureVerificationError("stale")

    secrets = [secret] if isinstance(secret, str) else list(secret)
    if not secrets or any(not isinstance(item, str) or item == "" for item in secrets):
        raise ValueError("The webhook secret is empty")
    signed = f"{t}.".encode("ascii") + body
    for item in secrets:
        expected = hmac.new(item.encode("utf-8"), signed, hashlib.sha256).hexdigest()
        if any(hmac.compare_digest(expected, signature) for signature in signatures):
            return
    raise SignatureVerificationError("mismatch")


class UnknownEvent(Model):
    """A webhook event of a type this version of the library does not know; read ``raw`` yourself."""

    @property
    def type(self) -> str:
        return str(self.raw.get("type"))

    @property
    def id(self) -> str:
        return str(self.raw.get("id"))


def construct_event(
    payload: Payload,
    header: Union[str, Sequence[str], None],
    secret: Union[str, Sequence[str]],
    *,
    tolerance: int = DEFAULT_TOLERANCE,
    now: Optional[float] = None,
) -> Union[WebhookEvent, UnknownEvent]:
    """
    Verifies the signature and returns the event: ``PaymentEvent``, ``PayoutEvent``,
    ``InvoiceEvent``, ``TestEvent``, or ``UnknownEvent`` for a type this version of the
    library does not know. Branch on ``event.type``.
    """
    verify_signature(payload, header, secret, tolerance=tolerance, now=now)
    try:
        data = json.loads(_bytes(payload).decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        raise CoinsPayError("The webhook body is not JSON") from None
    if not isinstance(data, dict) or not isinstance(data.get("type"), str):
        raise CoinsPayError("The webhook body is not a CoinsPay event")
    cls = EVENT_CLASSES.get(data["type"])
    if cls is None:
        return UnknownEvent(raw=data)
    return cast(WebhookEvent, cls.from_dict(data))


def signature_header(payload: Payload, secret: str, timestamp: Optional[int] = None) -> str:
    """A valid ``x-cpay-signature`` value, for testing your webhook handler."""
    t = int(time.time()) if timestamp is None else int(timestamp)
    mac = hmac.new(secret.encode("utf-8"), f"{t}.".encode("ascii") + _bytes(payload), hashlib.sha256).hexdigest()
    return f"t={t},v1={mac}"
