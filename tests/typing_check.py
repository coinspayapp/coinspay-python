from decimal import Decimal
from typing import List, Optional

import coinspay
from coinspay import models


def checkout(client: coinspay.Client, order_id: str, total: Decimal) -> str:
    invoice = client.invoices.create(
        currency="USD",
        amount=total,
        reference=order_id,
        return_url=f"https://shop.example/orders/{order_id}",
        items=[{"name": "Consulting", "quantity": "1", "price": "49.90"}],
        idempotency_key=f"order-{order_id}",
    )
    status: models.InvoiceStatus = invoice.status
    paid: Optional[str] = invoice.paid_at
    print(status, paid, invoice.items[0].amount)
    return invoice.pay_url


def paid_orders(client: coinspay.Client) -> List[Optional[str]]:
    return [invoice.reference for invoice in client.invoices.iterate(status="paid", limit=100)]


def payout(client: coinspay.Client, address_id: str, payout_id: str) -> models.Payout:
    quote = client.payouts.quote(address_id=address_id, asset="USDT", recipients=[{"address": "T1", "percent": "100"}])
    print(quote.amount)
    return client.payouts.create(
        address_id=address_id,
        asset="USDT",
        amount="MAX",
        recipients=[{"address": "T1", "percent": "60"}, {"address": "T2", "percent": "40"}],
        idempotency_key=f"payout-{payout_id}",
    )


def webhook(body: bytes, header: Optional[str], secret: str) -> None:
    event = coinspay.construct_event(body, header, secret)
    if isinstance(event, models.InvoiceEvent) and event.type == "invoice.paid":
        print(event.data.invoice.reference)
    elif isinstance(event, models.PaymentEvent):
        print(event.data.deposit.tx_hash)


def errors(client: coinspay.Client) -> None:
    try:
        client.balances.list()
    except coinspay.PermissionDeniedError as error:
        print(error.code, error.details)
    except coinspay.RateLimitError as error:
        print(error.retry_after)
    except coinspay.APIConnectionError as error:
        print(error.sent)
