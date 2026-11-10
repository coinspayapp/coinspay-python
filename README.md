# CoinsPay for Python

Official library for the [CoinsPay](https://coinspay.app) crypto payments API: invoices
with a payment page, receiving addresses, payments, payouts to your wallets and webhooks.
Python 3.8 or newer, typed, no dependencies.
The API reference is at [coinspay.app/docs](https://coinspay.app/docs).

```bash
pip install coinspay
```

## Quick start

Create an API key in the dashboard: shop → "API keys". A key with "Invoices only" access is
enough for a website; addresses, payments, balances and payouts need full access. Keep the
key on your server.

```python
import os
import coinspay

client = coinspay.Client(os.environ["COINSPAY_KEY"], "https://coinspay.app")

invoice = client.invoices.create(
    currency="USD",
    amount="49.90",
    reference="order-1042",
    return_url="https://shop.example/orders/1042",
    idempotency_key="order-1042",
)
# redirect the buyer to invoice.pay_url
```

Amounts are decimal strings or `Decimal`, never floats. Parameters go by name, so a typo
raises `TypeError` instead of being silently ignored by the API. Pass a field this version
does not know yet in `extra_body` or `extra_query`. `None` sends `null`; a parameter you do
not pass is not sent.

## Webhooks

```python
from coinspay import SignatureVerificationError, construct_event, models

# Flask
@app.post("/coinspay/webhook")
def webhook():
    try:
        event = construct_event(request.get_data(), request.headers.get("x-cpay-signature"), os.environ["COINSPAY_WEBHOOK_SECRET"])
    except SignatureVerificationError:
        return "", 401
    if isinstance(event, models.InvoiceEvent) and not event.test and event.type == "invoice.paid":
        mark_order_paid(event.data.invoice.reference, event.data.invoice.id)
    return "", 200
```

In Django use `request.body`, in FastAPI `await request.body()`: the body exactly as
received, before `json.loads`.

- One event may arrive twice: drop duplicates by `event.id`.
- Rely on the state in the body, not on the arrival order.
- While you replace the secret, pass both: `[new_secret, old_secret]`.
- An event of a type this version does not know is an `UnknownEvent`.
- `signature_header(body, secret)` signs a body for tests of your handler.

## Objects

Answers are frozen dataclasses with fields named as in the API (`invoice.pay_url`,
`invoice.items[0].price`); `to_dict()` gives the object exactly as the API sent it,
including fields this version does not know yet. Dates are ISO 8601 strings.

## Lists

```python
page = client.invoices.list(status="paid", limit=100)  # page.data, page.next_cursor
for invoice in client.invoices.iterate(status="paid"):
    ...  # every paid invoice, page after page
```

## Errors

```python
try:
    client.balances.list()
except coinspay.PermissionDeniedError as error:
    if error.code == "KEY_ACCESS_DENIED":
        ...  # an "Invoices only" key
except coinspay.RateLimitError as error:
    print(error.retry_after)
except coinspay.APIConnectionError as error:
    if not error.sent:
        ...  # never reached the API: safe to try again
except coinspay.APIError as error:
    print(error.status, error.code, error.details)
```

`APIError` subclasses by status: `InvalidRequestError` 400, `AuthenticationError` 401,
`PermissionDeniedError` 403, `NotFoundError` 404, `ConflictError` 409,
`UnprocessableError` 422, `RateLimitError` 429, `ServiceUnavailableError` 503. Without an
answer: `APIConnectionError` and `APITimeoutError`; a non-JSON answer:
`InvalidResponseError`. All extend `CoinsPayError`. Codes are constants of
`coinspay.ErrorCode`; `coinspay.ERROR_CODES` lists them by status.

## Retries and idempotency

Failures that are safe to retry are retried twice with a short pause: network errors and
timeouts, 429, 502, 503 and 504 for reads, quotes, cancellations and creates with an
idempotency key. `addresses.create` has no idempotency key and is retried only when the
request surely did not reach the API.

`invoices.create` without `idempotency_key` gets a random key for its own retries; pass
your order number to make your own retries safe too. `payouts.create` requires a key.
A repeat with a used key returns the existing object in its current state, and
`client.last_response.replayed` is `True`. `last_response` belongs to the calling thread,
so one client can serve the threads of a web server; it is `None` after a failed request.

## Client behaviour

- The API address must use `https`. Plain `http` is accepted for `localhost` and `127.0.0.1`, or with `allow_insecure_http=True` for a test stand.
- Each attempt times out after 30 seconds, and connecting after 10.
- Redirects are not followed, so the key is never sent to another host.
- IDs in the path are checked as UUIDs before the request is sent.
- The key never shows up in exceptions or `repr`.
- The transport can be replaced, for example to go through a proxy (see Options). The timeout applies to each socket operation.

## Options

```python
client = coinspay.Client(
    key, "https://coinspay.app",
    timeout=30.0,          # seconds for each socket operation of an attempt
    max_retries=2,
    max_retry_delay=5.0,   # a longer Retry-After fails at once
    transport=coinspay.UrllibTransport(proxies={"https": "http://proxy:3128"}),
)
client.invoices.get(invoice_id, timeout=5, max_retries=0)
client.request("GET", "/something/new")  # a method this version does not know yet
```

Proxies from `HTTPS_PROXY` work by default.

## Development

```bash
PYTHONPATH=src:tests python -m unittest discover -s tests
pip install mypy && MYPYPATH=src mypy --strict src tests/typing_check.py
```

The library supports Python 3.8 and newer, and mypy checks it against 3.8. Tests that need a real HTTP server are skipped unless `COINSPAY_MOCK_URL` points to one. `node scripts/mock-server.mjs` from [coinspay-node](https://github.com/coinspayapp/coinspay-node) starts it and prints its address.

Files that start with "Generated from the CoinsPay OpenAPI document" and the data in `tests/data` come from our generator and are shared by the libraries for Node.js, PHP, Python and Go. Please do not edit them by hand: if a model or a test vector looks wrong, open an issue.

## License

MIT
