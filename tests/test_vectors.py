import unittest

from coinspay import SignatureVerificationError, verify_signature

from support import ERROR_CLASS, INVOICE_ID, call_by_retry, client, vectors


class SignatureVectors(unittest.TestCase):
    def test_signatures(self) -> None:
        for case in vectors("signatures")["cases"]:
            with self.subTest(case["name"]):
                reason = "ok"
                try:
                    verify_signature(case["body"], case["header"], case["secrets"], tolerance=case["tolerance"], now=case["now"])
                except SignatureVerificationError as error:
                    reason = error.reason
                self.assertEqual(reason, case["expect"])


class RetryVectors(unittest.TestCase):
    def test_retries(self) -> None:
        for case in vectors("retries")["cases"]:
            with self.subTest(case["name"]):
                options = {"max_retries": case["maxRetries"]} if "maxRetries" in case else {}
                made, transport, sleeps = client(case["steps"], **options)
                error = None
                try:
                    call_by_retry(made, case["retry"])
                except Exception as caught:  # noqa: BLE001
                    error = caught
                expect = case["expect"]
                self.assertEqual(len(transport.requests), expect["attempts"], "attempts")

                if expect["result"] == "ok":
                    self.assertIsNone(error, repr(error))
                    if "replayed" in expect:
                        assert made.last_response is not None
                        self.assertEqual(made.last_response.replayed, expect["replayed"])
                else:
                    self.assertIsNotNone(error)
                    self.assertEqual(type(error).__name__, ERROR_CLASS[expect["error"]])
                    if "code" in expect:
                        self.assertEqual(error.code, expect["code"])  # type: ignore[union-attr]
                    if "retryAfter" in expect:
                        self.assertEqual(error.retry_after, expect["retryAfter"])  # type: ignore[union-attr]
                    if "sent" in expect:
                        self.assertEqual(error.sent, expect["sent"])  # type: ignore[union-attr]

                if "sleeps" in expect:
                    self.assertEqual(len(sleeps), len(expect["sleeps"]), "sleeps")
                    for got, want in zip(sleeps, expect["sleeps"]):
                        ms = got * 1000
                        if isinstance(want, list):
                            self.assertTrue(want[0] <= ms <= want[1], f"sleep {ms}")
                        else:
                            self.assertAlmostEqual(ms, want)

                attempts = transport.requests
                if "lastRequest" in expect:
                    last = attempts[-1]
                    attempts = attempts[:-1]
                    self.assertEqual(f"{last['method']} {last['path']}", expect["lastRequest"])
                self.assertEqual(len({(request["body"], request["headers"].get("idempotency-key")) for request in attempts}), 1)


class ErrorVectors(unittest.TestCase):
    def test_errors(self) -> None:
        for case in vectors("errors")["cases"]:
            expect = case["expect"]
            with self.subTest(f"{case['status']} {expect['error']}"):
                made, _, _ = client([case], max_retries=0)
                with self.assertRaises(Exception) as caught:
                    made.invoices.get(INVOICE_ID)
                error = caught.exception
                self.assertEqual(type(error).__name__, ERROR_CLASS[expect["error"]])
                self.assertEqual(error.status, case["status"])  # type: ignore[attr-defined]
                if "code" in expect:
                    self.assertEqual(error.code, expect["code"])  # type: ignore[attr-defined]
                if "message" in expect:
                    self.assertEqual(str(error), expect["message"])
                if "details" in expect:
                    self.assertEqual(error.details, expect["details"])  # type: ignore[attr-defined]
                if "retryAfter" in expect:
                    self.assertEqual(error.retry_after, expect["retryAfter"])  # type: ignore[attr-defined]


if __name__ == "__main__":
    unittest.main()
