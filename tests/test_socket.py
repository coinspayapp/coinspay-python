import json
import os
import time
import unittest
import urllib.request

from coinspay import APIConnectionError, APITimeoutError, Client, InvalidResponseError

from support import INVOICE_ID

MOCK = os.environ.get("COINSPAY_MOCK_URL", "")


@unittest.skipUnless(MOCK, "COINSPAY_MOCK_URL is not set")
class Socket(unittest.TestCase):
    def client(self, mode: str, **options: object) -> Client:
        return Client("cpk_test_wire", f"{MOCK}/{mode}/api/v1", max_retries=0, allow_insecure_http=True, **options)  # type: ignore[arg-type]

    def test_sends_what_the_api_expects(self) -> None:
        invoice = self.client("echo").invoices.create(currency="USD", amount="1.50", title="Заказ ✓", idempotency_key="order-77")
        raw = invoice.raw
        self.assertEqual(raw["method"], "POST")
        self.assertEqual(raw["path"], "/api/v1/invoices")
        self.assertEqual(raw["headers"]["authorization"], "Bearer cpk_test_wire")
        self.assertEqual(raw["headers"]["content-type"], "application/json")
        self.assertEqual(raw["headers"]["idempotency-key"], "order-77")
        self.assertEqual(int(raw["headers"]["content-length"]), len(raw["body"].encode("utf-8")))
        self.assertEqual(json.loads(raw["body"]), {"currency": "USD", "amount": "1.50", "title": "Заказ ✓"})

    def test_gives_up_after_the_timeout(self) -> None:
        started = time.monotonic()
        with self.assertRaises(APITimeoutError):
            self.client("slow", timeout=0.3).invoices.get(INVOICE_ID)
        self.assertLess(time.monotonic() - started, 2)

    def test_tells_a_refused_connection_from_a_sent_request(self) -> None:
        with self.assertRaises(APIConnectionError) as caught:
            Client("cpk_x", "http://127.0.0.1:1", max_retries=0).invoices.get(INVOICE_ID)
        self.assertFalse(caught.exception.sent)

    def test_does_not_follow_a_redirect(self) -> None:
        with self.assertRaises(InvalidResponseError) as caught:
            self.client("redirect").invoices.get(INVOICE_ID)
        self.assertEqual(caught.exception.status, 302)
        with urllib.request.urlopen(f"{MOCK}/hits") as response:
            self.assertEqual(json.loads(response.read())["target"], 0)

    def test_html_page_is_an_invalid_answer(self) -> None:
        with self.assertRaises(InvalidResponseError) as caught:
            self.client("html502").invoices.get(INVOICE_ID)
        self.assertEqual(caught.exception.status, 502)


if __name__ == "__main__":
    unittest.main()
