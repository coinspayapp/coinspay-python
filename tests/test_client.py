import dataclasses
import json
import unittest
import urllib.parse
from decimal import Decimal
from typing import Any, Dict

import coinspay
from coinspay import Client, construct_event, models, signature_header

from support import INVOICE_ID, client, vectors


def ok(body: Dict[str, Any], status: int = 200) -> Dict[str, Any]:
    return {"status": status, "body": body}


class Options(unittest.TestCase):
    def test_base_url_is_the_origin_or_ends_in_api_v1(self) -> None:
        def make(url: str, **options: Any) -> str:
            return Client("cpk_x", url, **options).base_url

        self.assertEqual(make("https://pay.example.com"), "https://pay.example.com/api/v1")
        self.assertEqual(make("https://Pay.Example.com/"), "https://pay.example.com/api/v1")
        self.assertEqual(make("https://pay.example.com/api/v1/"), "https://pay.example.com/api/v1")
        self.assertEqual(make("https://example.com/coinspay/api/v1"), "https://example.com/coinspay/api/v1")
        self.assertEqual(make(" https://pay.example.com:8443 "), "https://pay.example.com:8443/api/v1")
        self.assertEqual(make("http://localhost:3400"), "http://localhost:3400/api/v1")
        self.assertEqual(make("http://[::1]:3400"), "http://[::1]:3400/api/v1")
        self.assertEqual(make("http://host.docker.internal:3400", allow_insecure_http=True), "http://host.docker.internal:3400/api/v1")
        for url in ["", "pay.example.com", "https://pay.example.com/api", "https://pay.example.com/api/v2", "https://pay.example.com/?x=1", "https://u:p@pay.example.com", "ftp://pay.example.com", "http://host.docker.internal:3400"]:
            with self.subTest(url), self.assertRaises(ValueError):
                make(url)

    def test_key_is_required_and_never_shown(self) -> None:
        made = Client("cpk_test_super_secret", "https://x.example")
        self.assertTrue(made.test_mode)
        self.assertFalse(Client("cpk_live", "https://x.example").test_mode)
        self.assertNotIn("super_secret", repr(made) + repr(vars(made)) + repr(made.invoices))
        with self.assertRaises(ValueError):
            Client("cpk_a\nb", "https://x.example")
        with self.assertRaises(ValueError):
            Client("cpk_x", "https://x.example", timeout=0)


class Requests(unittest.TestCase):
    def test_sends_key_version_and_json(self) -> None:
        made, transport, _ = client([ok({"invoice": {"id": INVOICE_ID, "status": "open", "unknown_new_field": 1}}, 201)])
        invoice = made.invoices.create(currency="USD", amount=Decimal("49.90"), title="Заказ ✓", return_url="https://shop.example/a/b")
        request = transport.requests[0]
        self.assertEqual(request["method"], "POST")
        self.assertEqual(request["path"], "/invoices")
        self.assertEqual(request["headers"]["authorization"], "Bearer cpk_test_secret_key_value")
        self.assertEqual(request["headers"]["content-type"], "application/json")
        self.assertRegex(request["headers"]["user-agent"], rf"^coinspay-python/{coinspay.__version__} python/\d")
        self.assertRegex(request["headers"]["idempotency-key"], r"^[0-9a-f-]{36}$")
        self.assertEqual(json.loads(request["body"]), {"currency": "USD", "amount": "49.90", "title": "Заказ ✓", "return_url": "https://shop.example/a/b"})
        self.assertIsInstance(invoice, models.Invoice)
        self.assertEqual(invoice.status, "open")
        self.assertEqual(invoice.raw["unknown_new_field"], 1)
        self.assertEqual(invoice.to_dict(), {"id": INVOICE_ID, "status": "open", "unknown_new_field": 1})
        assert made.last_response is not None
        self.assertEqual(made.last_response.status, 201)
        self.assertFalse(made.last_response.replayed)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            invoice.status = "paid"  # type: ignore[misc]

    def test_none_sends_null_and_omitted_is_not_sent(self) -> None:
        made, transport, _ = client([ok({"invoice": {"id": INVOICE_ID}}, 201)])
        made.invoices.create(currency="USD", amount="1", title=None)
        self.assertEqual(json.loads(transport.requests[0]["body"]), {"currency": "USD", "amount": "1", "title": None})

    def test_decimal_formats_without_exponent(self) -> None:
        made, transport, _ = client([ok({"invoice": {"id": INVOICE_ID}}, 201)])
        made.invoices.create(currency="USD", items=[{"name": "A", "quantity": Decimal("1E+2"), "price": Decimal("0.0000001")}])
        self.assertEqual(json.loads(transport.requests[0]["body"])["items"], [{"name": "A", "quantity": "100", "price": "0.0000001"}])

    def test_amounts_must_be_strings_or_decimals(self) -> None:
        made, transport, _ = client([])
        with self.assertRaisesRegex(TypeError, r"^amount must be a decimal string"):
            made.invoices.create(currency="USD", amount=49.9)  # type: ignore[arg-type]
        with self.assertRaisesRegex(TypeError, r"items\[0\]\.price"):
            made.invoices.create(currency="USD", items=[{"name": "A", "quantity": "1", "price": 1}])  # type: ignore[typeddict-item]
        with self.assertRaisesRegex(TypeError, r"payout\[0\]\.percent"):
            made.addresses.create(chain="tron", payout=[{"address": "T1", "percent": 100}])  # type: ignore[typeddict-item]
        self.assertEqual(transport.requests, [])

    def test_unknown_parameters_are_typos_unless_extra(self) -> None:
        made, transport, _ = client([ok({"invoice": {"id": INVOICE_ID}}, 201)])
        with self.assertRaises(TypeError):
            made.invoices.create(currency="USD", ammount="1")  # type: ignore[call-arg]
        with self.assertRaisesRegex(TypeError, r"Unknown parameter items\[0\]\.qty"):
            made.invoices.create(currency="USD", items=[{"name": "A", "qty": "1", "price": "1"}])  # type: ignore[typeddict-unknown-key]
        made.invoices.create(currency="USD", amount="1", extra_body={"brand_new": True})
        self.assertEqual(json.loads(transport.requests[0]["body"]), {"currency": "USD", "amount": "1", "brand_new": True})

    def test_payout_needs_an_idempotency_key(self) -> None:
        made, _, _ = client([])
        recipients = [{"address": "T1", "percent": "100"}]
        with self.assertRaises(TypeError):
            made.payouts.create(address_id=INVOICE_ID, asset="USDT", recipients=recipients)  # type: ignore[call-arg,list-item]
        for key in ["short", "has space inside"]:
            with self.subTest(key), self.assertRaises(ValueError):
                made.payouts.create(address_id=INVOICE_ID, asset="USDT", recipients=recipients, idempotency_key=key)  # type: ignore[list-item]
        self.assertRegex(Client.new_idempotency_key(), r"^[0-9a-f-]{36}$")

    def test_cancel_sends_an_empty_json_object(self) -> None:
        made, transport, _ = client([ok({"invoice": {"id": INVOICE_ID, "status": "cancelled"}})])
        made.invoices.cancel(INVOICE_ID.upper())
        self.assertEqual(transport.requests[0]["path"], f"/invoices/{INVOICE_ID}/cancel")
        self.assertEqual(transport.requests[0]["body"], b"{}")

    def test_ids_are_checked_before_sending(self) -> None:
        made, transport, _ = client([])
        for bad in ["..", "../payouts", "", "not-a-uuid", f"{INVOICE_ID}/cancel", None, 42]:
            with self.subTest(bad), self.assertRaises(ValueError):
                made.invoices.get(bad)  # type: ignore[arg-type]
        self.assertEqual(transport.requests, [])

    def test_query_and_pages(self) -> None:
        made, transport, _ = client(
            [
                ok({"invoices": [{"id": "a"}, {"id": "b"}], "next_cursor": "b0000000-0000-4000-8000-000000000000"}),
                ok({"invoices": [{"id": "c"}], "next_cursor": None}),
                ok({"invoices": [], "next_cursor": None}),
            ]
        )
        ids = [invoice.id for invoice in made.invoices.iterate(status="paid", limit=2)]
        self.assertEqual(ids, ["a", "b", "c"])
        self.assertEqual(transport.requests[0]["query"], "status=paid&limit=2")
        self.assertEqual(
            dict(urllib.parse.parse_qsl(transport.requests[1]["query"])),
            {"status": "paid", "limit": "2", "cursor": "b0000000-0000-4000-8000-000000000000"},
        )
        page = made.invoices.list(reference="order 1&2")
        self.assertEqual(transport.requests[2]["query"], "reference=order%201%262")
        self.assertEqual(len(page), 0)
        self.assertFalse(page.has_more)

    def test_balances_shop_and_raw_requests(self) -> None:
        made, transport, _ = client(
            [
                ok({"balances": [{"chain": "tron", "asset": "USDT", "decimals": 6, "confirmed": "1", "pending": "0", "seen": "0"}]}),
                ok({"shop": {"id": "s", "name": "Shop", "created_at": "2026-10-29T00:00:00.000Z"}, "key": {"test": True, "access": "invoices"}}),
                ok({"anything": True}),
            ]
        )
        balances = made.balances.list()
        self.assertEqual(balances[0].asset, "USDT")
        shop = made.shop.get()
        self.assertEqual(shop.key.access, "invoices")
        self.assertEqual(made.request("GET", "/something/new", query={"a": 1}), {"anything": True})
        self.assertEqual(transport.requests[2]["query"], "a=1")
        for path in ["../admin", "/a/../b", "invoices"]:
            with self.subTest(path), self.assertRaises(ValueError):
                made.request("GET", path)

    def test_error_codes_by_status(self) -> None:
        self.assertIn("KEY_ACCESS_DENIED", coinspay.ERROR_CODES["403"])


class Webhooks(unittest.TestCase):
    def test_event_types(self) -> None:
        vector = vectors("signatures")["signHeader"]
        self.assertEqual(signature_header(vector["body"], vector["secret"], vector["timestamp"]), vector["header"])
        event = construct_event(vector["body"].encode(), [vector["header"]], vector["secret"], now=vector["timestamp"])
        self.assertIsInstance(event, models.InvoiceEvent)
        assert isinstance(event, models.InvoiceEvent)
        self.assertEqual(event.type, "invoice.paid")
        self.assertEqual(event.data.invoice.status, "paid")

        future = '{"id":"e","type":"refund.created","created_at":"2026-10-29T00:00:00.000Z","shop_id":"s","test":false,"data":{"refund":{}}}'
        unknown = construct_event(future, signature_header(future, "s", 100), "s", now=100)
        self.assertIsInstance(unknown, coinspay.UnknownEvent)
        self.assertEqual(unknown.type, "refund.created")
        with self.assertRaises(ValueError):
            construct_event(vector["body"], vector["header"], "", now=vector["timestamp"])


if __name__ == "__main__":
    unittest.main()
