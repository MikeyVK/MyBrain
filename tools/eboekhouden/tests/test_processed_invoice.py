"""Synthetic processed-invoice exact lookup and archive-download checks."""
import unittest
from urllib.parse import parse_qs, urlsplit
import processed_invoice_probe as p


class FakeTransport:
    def __init__(self, replies):
        self.replies, self.calls = list(replies), []
    def request(self, method, path, body=None, token=None, bearer=False):
        self.calls.append((method, path))
        value = self.replies.pop(0)
        if isinstance(value, Exception):
            raise value
        return value

ADMIN = {"valid": True, "currentAdministratie": {"id": 1, "naam": "Synthetic"}}
AUTH = {"loginOk": True, "twoFactorCodeRequired": False, "token": "FAKE_JWT"}


class Checks(unittest.TestCase):
    def test_exact_invoice_query_is_encoded_and_bounded(self):
        query = parse_qs(urlsplit(p.invoice_query("SYNTHETIC-INV/1")).query)
        self.assertEqual(query, {"invoiceNumber": ["SYNTHETIC-INV/1"], "type": ["1"], "limit": ["5"], "offset": ["0"]})

    def test_no_financial_archive_link_or_crossfile_writes(self):
        for mode in ("rest", "app"):
            transport = p.Transport(mode, invoice="SYNTHETIC", file_id=9,
                                    factory=lambda *a, **kw: self.fail("Network constructed"))
            for method, path in [("POST", "/v1/mutation"), ("PUT", "/api/v4/mutaties"),
                                 ("POST", "/api/v4/bestanden/koppel"), ("POST", "/api/v4/bestanden/upload"),
                                 ("DELETE", "/api/v4/bestanden/bestand/9"),
                                 ("GET", "/api/v4/bestanden/download/10"), ("GET", "https://other.invalid/x")]:
                with self.assertRaisesRegex(p.app.app.Stop, "EXEMPLAR_REQUEST_NOT_ALLOWED"):
                    transport.request(method, path)

    def test_unique_purchase_invoice_and_only_needed_reference_lookups(self):
        detail = {"id": 17, "type": 1, "invoiceNumber": "SYNTHETIC", "relationId": 3,
                  "ledgerId": 4, "rows": [{"ledgerId": 5, "amount": 1}], "vat": []}
        transport = FakeTransport([{"token": "FAKE_SESSION"}, {"items": [{"id": 17, "type": 1, "invoiceNumber": "SYNTHETIC"}]},
                                   detail, {"id": 3, "name": "Synthetic supplier", "profile": "NOT_SELECTED"},
                                   {"id": 4, "code": "SYNTHETIC"}, {"id": 5, "description": "Synthetic ledger"}, None])
        result = p.read_rest_invoice(transport, "FAKE_ACCESS", "SYNTHETIC")
        self.assertEqual(result["mutation"]["id"], 17)
        self.assertFalse(result["archiveLinkVerified"])
        self.assertNotIn("profile", result["relation"])
        self.assertEqual(transport.calls[-1], ("DELETE", "/v1/session"))

    def test_missing_duplicate_or_wrong_type_stops_without_detail(self):
        for items in ([], [{"id": 17}, {"id": 18}], [{"id": 17, "type": 2, "invoiceNumber": "SYNTHETIC"}]):
            transport = FakeTransport([{"token": "FAKE_SESSION"}, {"items": items}, None])
            with self.assertRaises(p.app.app.Stop):
                p.read_rest_invoice(transport, "FAKE_ACCESS", "SYNTHETIC")
            self.assertEqual(len(transport.calls), 3)

    def test_binary_magic_mime_and_executable_rejection(self):
        self.assertEqual(p.validate_file(b"%PDF-1.7 SYNTHETIC", "application/octet-stream")["extension"], ".pdf")
        for raw, mime in [(b"MZEXECUTABLE", "application/pdf"), (b"%PDF-1.7", "image/png"), (b"<html>error", "text/html")]:
            with self.assertRaisesRegex(p.app.app.Stop, "EXEMPLAR_FILE_TYPE_MISMATCH"):
                p.validate_file(raw, mime)

    def test_app_admin_file_identity_and_content_controls(self):
        transport = FakeTransport([AUTH, ADMIN, {"id": 9, "naam": "synthetic.pdf"},
                                   p.validate_file(b"%PDF-1.7 SYNTHETIC", "application/pdf"), ADMIN])
        file, metadata = p.read_app_file(transport, p.app.Login("FAKE_USER", "FAKE_PASSWORD"), 1, 9)
        self.assertEqual(metadata["id"], 9)
        self.assertEqual(file["mime"], "application/pdf")
        self.assertEqual(len(transport.calls), 5)
        transport = FakeTransport([AUTH, ADMIN])
        with self.assertRaisesRegex(p.app.app.Stop, "ADMINISTRATION_MISMATCH"):
            p.read_app_file(transport, p.app.Login("FAKE_USER", "FAKE_PASSWORD"), 2, 9)
        self.assertEqual(len(transport.calls), 2)

    def test_binary_limit_and_redirect_no_follow(self):
        class Response:
            status = 200
            def getheader(self, key, default=""):
                return "application/pdf"
            def read(self, maximum):
                return b"x" * maximum
        class Connection:
            def request(self, *a, **kw):
                pass
            def getresponse(self):
                return Response()
            def close(self):
                pass
        transport = p.Transport("app", file_id=9, factory=lambda *a, **kw: Connection())
        with self.assertRaisesRegex(p.app.app.Stop, "EXEMPLAR_RESPONSE_TOO_LARGE"):
            transport.request("GET", "/api/v4/bestanden/download/9", token="FAKE_JWT")
        Response.status = 302
        with self.assertRaises(p.app.RequestFailure) as caught:
            p.Transport("app", file_id=9, factory=lambda *a, **kw: Connection()).request("GET", "/api/v4/bestanden/download/9")
        self.assertEqual(str(caught.exception), "HTTP_302")


if __name__ == "__main__":
    unittest.main()
