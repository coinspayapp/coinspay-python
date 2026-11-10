import threading
import unittest

import coinspay
from coinspay import SignatureVerificationError, signature_header, verify_signature

from support import INVOICE_ID, client


class Review(unittest.TestCase):
    def test_payout_with_a_none_key_is_refused_not_given_a_random_one(self) -> None:
        made, transport, _ = client([])
        with self.assertRaisesRegex(ValueError, "needs idempotency_key"):
            made.payouts.create(address_id=INVOICE_ID, asset="USDT", recipients=[{"address": "T1", "percent": "100"}], idempotency_key=None)  # type: ignore[arg-type]
        self.assertEqual(transport.requests, [])

    def test_a_nan_or_negative_tolerance_is_refused(self) -> None:
        header = signature_header("{}", "s", 0)
        for tolerance in (float("nan"), -1, float("inf")):
            with self.subTest(tolerance), self.assertRaises(ValueError):
                verify_signature("{}", header, "s", tolerance=tolerance, now=1_000_000_000)  # type: ignore[arg-type]

    def test_a_huge_timestamp_is_stale(self) -> None:
        with self.assertRaises(SignatureVerificationError) as caught:
            verify_signature("{}", "t=" + "9" * 5000 + ",v1=" + "0" * 64, "s")
        self.assertEqual(caught.exception.reason, "stale")

    def test_last_response_belongs_to_the_thread_and_is_cleared_by_a_failure(self) -> None:
        made, _, _ = client(
            [
                {"status": 201, "body": {"invoice": {"id": INVOICE_ID}}},
                {"status": 404, "body": {"error": {"code": "NOT_FOUND", "message": "Not found"}}},
            ],
            max_retries=0,
        )
        made.invoices.create(currency="USD", amount="1")
        assert made.last_response is not None
        self.assertEqual(made.last_response.status, 201)
        seen = []
        thread = threading.Thread(target=lambda: seen.append(made.last_response))
        thread.start()
        thread.join()
        self.assertEqual(seen, [None])
        with self.assertRaises(coinspay.NotFoundError):
            made.invoices.get(INVOICE_ID)
        self.assertIsNone(made.last_response)

    def test_a_key_passed_as_the_base_url_is_not_repeated_in_the_error(self) -> None:
        with self.assertRaises(ValueError) as caught:
            coinspay.Client("https://pay.example.com", "cpk_live_secret_value")
        self.assertNotIn("cpk_live_secret_value", str(caught.exception))

    def test_error_codes_are_constants(self) -> None:
        self.assertEqual(coinspay.ErrorCode.KEY_ACCESS_DENIED, "KEY_ACCESS_DENIED")


if __name__ == "__main__":
    unittest.main()
