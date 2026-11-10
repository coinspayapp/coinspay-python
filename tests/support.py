import json
import pathlib
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple

import coinspay
from coinspay import HTTPResponse, TransportError

VECTORS = pathlib.Path(__file__).resolve().parent / "data" / "vectors"
INVOICE_ID = "7c9e6679-7425-40de-944b-e07fc1f90ae7"

ERROR_CLASS = {
    "Api": "APIError",
    "InvalidRequest": "InvalidRequestError",
    "Authentication": "AuthenticationError",
    "PermissionDenied": "PermissionDeniedError",
    "NotFound": "NotFoundError",
    "Conflict": "ConflictError",
    "Unprocessable": "UnprocessableError",
    "RateLimit": "RateLimitError",
    "ServiceUnavailable": "ServiceUnavailableError",
    "ApiConnection": "APIConnectionError",
    "ApiTimeout": "APITimeoutError",
    "InvalidResponse": "InvalidResponseError",
}


def vectors(name: str) -> Dict[str, Any]:
    return json.loads((VECTORS / f"{name}.json").read_text(encoding="utf-8"))


class FakeTransport:

    def __init__(self, steps: List[Dict[str, Any]]) -> None:
        self.steps = list(steps)
        self.requests: List[Dict[str, Any]] = []

    def send(self, method: str, url: str, headers: Dict[str, str], body: Optional[bytes], timeout: float) -> HTTPResponse:
        parts = urllib.parse.urlsplit(url)
        self.requests.append(
            {"method": method, "path": parts.path.replace("/api/v1", "", 1), "query": parts.query, "headers": dict(headers), "body": body}
        )
        if not self.steps:
            raise AssertionError(f"Out of steps: request {len(self.requests)}")
        step = self.steps.pop(0)
        network = step.get("network")
        if network == "refused":
            raise TransportError("Connection refused", sent=False)
        if network == "reset":
            raise TransportError("Connection reset", sent=True)
        if network == "timeout":
            raise TransportError("timed out", sent=True, timeout=True)
        text = step["text"] if "text" in step else json.dumps(step["body"])
        return HTTPResponse(step["status"], step.get("headers", {}), text.encode("utf-8"))


def client(steps: List[Dict[str, Any]], **options: Any) -> Tuple[coinspay.Client, FakeTransport, List[float]]:
    transport = FakeTransport(steps)
    sleeps: List[float] = []
    made = coinspay.Client(
        "cpk_test_secret_key_value",
        "https://pay.example.com",
        transport=transport,
        _sleep=sleeps.append,
        **options,
    )
    return made, transport, sleeps


def call_by_retry(made: coinspay.Client, retry: str) -> Any:
    if retry == "safe":
        return made.invoices.get(INVOICE_ID)
    if retry == "idempotent":
        return made.invoices.create(currency="USD", amount="49.90", idempotency_key="order-1042")
    if retry == "unsafe":
        return made.addresses.create(chain="tron")
    if retry == "cancel":
        return made.invoices.cancel(INVOICE_ID)
    raise ValueError(retry)
