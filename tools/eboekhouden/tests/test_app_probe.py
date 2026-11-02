"""Offline synthetic tests for the bounded App metadata filter."""
import json
import unittest
from unittest.mock import patch
import app_probe as p

DAY = "2000-01-01"

def admin(identifier=1):
    return {"valid": True, "currentAdministratie": {"id": identifier, "naam": "Synthetic"}}

def row(identifier=902, number=17, day=DAY):
    return {"id": identifier, "mutatieNummer": number, "datum": day + "T00:00:00",
            "mutatieRegels": [], "omschrijving": "FAKE_PASSWORD FAKE_JWT FAKE_USER"}

def page(items, current=1, more=False):
    return {"currentPage": current, "pageSize": 20, "hasMoreRows": more, "items": items}

AUTH = {"loginOk": True, "twoFactorCodeRequired": False, "token": "FAKE_JWT"}

class FakeTransport:
    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []
    def request(self, method, path, body=None, token=None):
        self.calls.append((method, path, body))
        value = self.replies.pop(0)
        if isinstance(value, Exception):
            raise value
        return value

def read(transport, confirm=lambda value: True):
    return p.read_selected(transport, p.Login("FAKE_USER", "FAKE_PASSWORD"), 17, DAY, confirm)

class Checks(unittest.TestCase):
    def test_filter_query_allowlist_is_exact_and_financial_writes_rejected(self):
        body = p.filter_body(DAY, 1)
        self.assertTrue(p.request_allowed("POST", "/api/v4/mutaties/filter", body))
        self.assertEqual(body["pageSize"], 20)
        self.assertEqual(body["period"]["startDate"], DAY + "T00:00:00")
        self.assertEqual(body["period"]["endDate"], DAY + "T23:59:59")
        for method, path, payload in [
            ("POST", "/api/v4/mutaties", {}),
            ("PUT", "/api/v4/mutaties", {}),
            ("DELETE", "/api/v4/mutaties/902", None),
            ("POST", "/api/v4/auth/renew", {}),
            ("GET", "/api/v4/mutaties/search?mutatienummer=17", None),
            ("GET", "/mutaties/search?mutatienummer=17", None),
            ("POST", "/api/v4/mutaties/filter", {**body, "pageSize": 21}),
            ("POST", "/api/v4/mutaties/filter", {**body, "page": 3}),
            ("POST", "/api/v4/mutaties/filter", {**body, "unknown": True}),
        ]:
            transport = p.Transport(lambda *a, **kw: self.fail("Network constructed"))
            with self.assertRaisesRegex(p.app.Stop, "REQUEST_NOT_ALLOWED"):
                transport.request(method, path, payload)

    def test_invalid_or_broad_date_scope_rejected(self):
        for day in ("", "not-a-date", "2000-01", "2000-02-31"):
            with self.assertRaises(p.app.Stop):
                p.filter_body(day, 1)
        body = p.filter_body(DAY, 1)
        body["period"]["endDate"] = "2001-01-01T23:59:59"
        self.assertFalse(p.request_allowed("POST", "/api/v4/mutaties/filter", body))

    def test_login_2fa_or_failure_stops_before_profile(self):
        for response in ({"twoFactorCodeRequired": True}, {"loginOk": False, "twoFactorCodeRequired": False}, {}):
            transport = FakeTransport([response])
            with self.assertRaises(p.app.Stop):
                read(transport)
            self.assertEqual(len(transport.calls), 1)

    def test_admin_refusal_precedes_metadata_query(self):
        transport = FakeTransport([AUTH, admin()])
        with self.assertRaisesRegex(p.app.Stop, "ADMINISTRATION_NOT_CONFIRMED"):
            read(transport, lambda value: False)
        self.assertEqual(len(transport.calls), 2)

    def test_exact_day_number_internal_id_and_secret_projection(self):
        transport = FakeTransport([AUTH, admin(), page([row()]), admin(), row(), admin()])
        selected = read(transport)
        self.assertEqual(transport.calls[2], ("POST", "/api/v4/mutaties/filter", p.filter_body(DAY, 1)))
        self.assertIn(("GET", "/api/v4/mutaties/902", None), transport.calls)
        for secret in ("FAKE_USER", "FAKE_PASSWORD", "FAKE_JWT"):
            self.assertNotIn(secret, json.dumps(selected))

    def test_two_pages_are_bounded_and_third_page_is_never_requested(self):
        transport = FakeTransport([AUTH, admin(), page([row(901, 16)], more=True),
                                   page([row()], current=2), admin(), row(), admin()])
        self.assertEqual(read(transport)["id"], 902)
        filters = [call for call in transport.calls if call[1] == "/api/v4/mutaties/filter"]
        self.assertEqual([call[2]["page"] for call in filters], [1, 2])
        transport = FakeTransport([AUTH, admin(), page([row()], more=True), page([], current=2, more=True)])
        with self.assertRaisesRegex(p.app.Stop, "FILTER_SCOPE_EXCEEDS_TWO_PAGES"):
            read(transport)
        self.assertEqual(len(transport.calls), 4)

    def test_filter_scope_duplicates_and_absence_stop_without_detail(self):
        for result in (page([]), page([row(), row(903)]),
                       page([row(day="2001-01-01")]), page([row()] * 21)):
            transport = FakeTransport([AUTH, admin(), result])
            with self.assertRaises(p.app.Stop):
                read(transport)
            self.assertEqual(len(transport.calls), 3)

    def test_admin_and_detail_identity_changes_stop(self):
        transport = FakeTransport([AUTH, admin(), page([row()]), admin(2)])
        with self.assertRaisesRegex(p.app.Stop, "ADMINISTRATION_CHANGED"):
            read(transport)
        transport = FakeTransport([AUTH, admin(), page([row()]), admin(), row(999)])
        with self.assertRaisesRegex(p.app.Stop, "DETAIL_IDENTITY_MISMATCH"):
            read(transport)

    def test_error_validation_keys_and_values_redacted_and_bounded(self):
        class Response:
            def read(self, maximum):
                return json.dumps({"errors": {"FAKE_PASSWORD": ["FAKE_JWT\n", "FAKE_USER", "safe", "not-included"]},
                                   "message": "FAKE_PASSWORD", "profile": "DO_NOT_PRINT"}).encode()
        result = p.error_fields(Response(), ["FAKE_PASSWORD", "FAKE_JWT", "FAKE_USER"])
        for secret in ("FAKE_PASSWORD", "FAKE_JWT", "FAKE_USER", "not-included", "DO_NOT_PRINT"):
            self.assertNotIn(secret, json.dumps(result))
        self.assertEqual(len(result["errors"]["[REDACTED]"]), 3)
        self.assertEqual(p.request_label("POST", "/api/v4/mutaties/filter"), "APP_FILTER_METADATA")

    def test_filter_wire_payload_tls_and_call_limit(self):
        class Response:
            status = 200
            def getheader(self, key, default=""):
                return "application/json"
            def read(self, maximum):
                return b"{}"
        class Connection:
            def request(self, method, path, **kwargs):
                self.method, self.path, self.payload = method, path, json.loads(kwargs["body"])
            def getresponse(self):
                return Response()
            def close(self):
                pass
        observed = []
        connection = Connection()
        def factory(host, timeout, context):
            observed.append((host, timeout, context))
            return connection
        transport = p.Transport(factory)
        for _ in range(8):
            transport.request("POST", "/api/v4/mutaties/filter", p.filter_body(DAY, 1), token="FAKE_JWT")
        self.assertEqual(connection.payload, p.filter_body(DAY, 1))
        self.assertEqual(observed[0][0:2], ("appapi.e-boekhouden.nl", 15))
        self.assertTrue(observed[0][2].check_hostname)
        with self.assertRaisesRegex(p.app.Stop, "CALL_LIMIT"):
            transport.request("POST", "/api/v4/mutaties/filter", p.filter_body(DAY, 1))

    def test_certifi_host_verification_and_gui_credential(self):
        observed = []
        with patch.object(p.http.client, "HTTPSConnection", side_effect=lambda *a, **kw: observed.append((a, kw))):
            p.tls_connection("appapi.e-boekhouden.nl", 15, p.ssl.create_default_context())
        self.assertTrue(observed[0][1]["context"].check_hostname)
        self.assertEqual(observed[0][1]["context"].verify_mode, p.ssl.CERT_REQUIRED)
        with self.assertRaises(p.app.Stop):
            p.tls_connection("other.invalid", 15, p.ssl.create_default_context())
        login = p.decode_login("synthetic-user", "", 3, "Synthetic Pässword".encode("utf-16-le"))
        self.assertEqual(login.password, "Synthetic Pässword")
        self.assertNotIn("Pässword", repr(login))

    def test_credential_load_only_exact_app_key(self):
        class MissingAPI:
            def CredReadW(self, target, kind, flags, pointer):
                self.target = target
                return False
        api = MissingAPI()
        with patch.object(p, "owner_sid", return_value="owner"), patch.object(p.ctypes, "get_last_error", return_value=1168):
            with self.assertRaisesRegex(p.app.Stop, "APP_CREDENTIAL_MISSING"):
                p.load_login(api)
        self.assertEqual(api.target, "MyBrain/eBoekhouden-App-v4")

if __name__ == "__main__":
    unittest.main()
