"""Offline synthetic tests; never create a vendor connection."""
import json
import unittest
import probe_rest as p


class Response:
    def __init__(self, status=200, data=None, raw=None):
        self.status = status
        self.raw = json.dumps(data).encode() if raw is None else raw

    def getheader(self, key, default=""):
        return "application/json"

    def read(self, maximum):
        return self.raw[:maximum]


class Connection:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def request(self, *args, **kwargs):
        self.calls.append((args, kwargs))

    def getresponse(self):
        return self.response

    def close(self):
        pass


class Reader:
    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []

    def request(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        value = self.replies.pop(0)
        if isinstance(value, Exception):
            raise value
        return value


class Checks(unittest.TestCase):
    def test_financial_writes_and_foreign_routes_rejected(self):
        for method, path in [("POST", "/v1/mutation"), ("PUT", "/v1/mutation/17"),
                             ("DELETE", "/v1/mutation/17"), ("GET", "/v1/mutation"),
                             ("GET", "https://other.invalid/v1/mutation/17"),
                             ("GET", "/v1/administration"), ("POST", "/api/v4/auth/login")]:
            transport = p.Transport(lambda *a, **kw: self.fail("Network constructed"))
            with self.assertRaisesRegex(p.Stop, "REQUEST_NOT_ALLOWED"):
                transport.request(method, path)

    def test_tls_origin_and_redirect_refusal(self):
        conn = Connection(Response(302, {"token": "FAKE_SECRET"}))
        observed = []
        def factory(host, **kwargs):
            observed.append((host, kwargs))
            return conn
        with self.assertRaisesRegex(p.Stop, "MUTATION_HTTP_302"):
            p.Transport(factory).request("GET", "/v1/mutation/17", token="FAKE_SESSION")
        self.assertEqual(observed[0][0], "api.e-boekhouden.nl")
        self.assertEqual(observed[0][1]["timeout"], 15)
        self.assertTrue(observed[0][1]["context"].check_hostname)
        self.assertEqual(observed[0][1]["context"].verify_mode, p.ssl.CERT_REQUIRED)
        self.assertEqual(len(conn.calls), 1)

    def test_header_fallback_only_on_401(self):
        reader = Reader([p.Stop("MUTATION_HTTP_401"), {"id": 17}])
        detail, bearer = p.read_record(reader, "FAKE_SESSION", 17)
        self.assertTrue(bearer)
        self.assertEqual(reader.calls[1][1]["bearer"], True)
        self.assertEqual(detail["id"], 17)
        for code in ("MUTATION_HTTP_403", "MUTATION_HTTP_404", "NETWORK_OR_TLS_FAILURE"):
            reader = Reader([p.Stop(code)])
            with self.assertRaises(p.Stop):
                p.read_record(reader, "FAKE_SESSION", 17)
            self.assertEqual(len(reader.calls), 1)

    def test_selected_identity_and_secret_projection(self):
        detail = {"id": 17, "description": "FAKE_SESSION FAKE_ACCESS", "rows": [], "vat": [],
                  "token": "FAKE_SESSION", "unrelatedProfile": "not-for-report"}
        projected = json.dumps(p.project(detail, 17, ("FAKE_SESSION", "FAKE_ACCESS")))
        for value in ("FAKE_SESSION", "FAKE_ACCESS", "not-for-report"):
            self.assertNotIn(value, projected)
        with self.assertRaisesRegex(p.Stop, "MUTATION_NUMBER_MISMATCH"):
            p.project(detail, 99, ())

    def test_limits_and_redacted_errors(self):
        transport = p.Transport(lambda *a, **kw: Connection(Response(data={})))
        for _ in range(p.MAX_CALLS):
            transport.request("GET", "/v1/mutation/17")
        with self.assertRaisesRegex(p.Stop, "CALL_LIMIT"):
            transport.request("GET", "/v1/mutation/17")
        huge = p.Transport(lambda *a, **kw: Connection(Response(raw=b"x" * (p.MAX_BYTES + 1))))
        with self.assertRaisesRegex(p.Stop, "RESPONSE_TOO_LARGE"):
            huge.request("GET", "/v1/mutation/17")
        transport = p.Transport(lambda *a, **kw: Connection(Response(401, {"password": "FAKE_ACCESS"})))
        with self.assertRaises(p.Stop) as caught:
            transport.request("GET", "/v1/mutation/17")
        self.assertNotIn("FAKE_ACCESS", str(caught.exception))

    def test_own_session_cleanup_is_only_allowed_delete(self):
        conn = Connection(Response(204))
        transport = p.Transport(lambda *a, **kw: conn)
        self.assertIsNone(transport.request("DELETE", "/v1/session", token="FAKE_SESSION"))
        with self.assertRaisesRegex(p.Stop, "REQUEST_NOT_ALLOWED"):
            transport.request("DELETE", "/v1/mutation/17", token="FAKE_SESSION")

    def test_certificate_failure_is_safe_and_never_relaxed(self):
        conn = Connection(Response())
        def failure(*args, **kwargs):
            raise p.ssl.SSLCertVerificationError("FAKE_SECRET_DIAGNOSTIC")
        conn.request = failure
        with self.assertRaisesRegex(p.Stop, "TLS_CERTIFICATE_VERIFY_FAILED") as caught:
            p.Transport(lambda *a, **kw: conn).request("GET", "/v1/mutation/17")
        self.assertNotIn("FAKE_SECRET", str(caught.exception))

    def test_400_diagnoses_stage_and_only_known_machine_fields(self):
        payload = {"Code": "API_SESSION_004", "Type": "validation", "PropertyName": "accessToken",
                   "Message": "FAKE_SECRET", "Title": "FAKE_SECRET", "traceId": "FAKE_SECRET"}
        transport = p.Transport(lambda *a, **kw: Connection(Response(400, payload)))
        with self.assertRaises(p.Stop) as caught:
            transport.request("POST", "/v1/session", body={"accessToken": "FAKE_SECRET", "source": "MBProbe"})
        self.assertEqual(str(caught.exception), "SESSION_HTTP_400|code=API_SESSION_004|type=validation|property=accessToken")
        malicious = {"code": "FAKE_SECRET", "type": "FAKE_SECRET", "propertyName": "FAKE_SECRET"}
        transport = p.Transport(lambda *a, **kw: Connection(Response(400, malicious)))
        with self.assertRaises(p.Stop) as caught:
            transport.request("GET", "/v1/mutation/17", token="FAKE_SECRET")
        self.assertEqual(str(caught.exception), "MUTATION_HTTP_400")

    def test_token_edges_only_and_control_input_rejected(self):
        self.assertEqual(p.normalize_access_token("  FAKE_TOKEN\r\n"), "FAKE_TOKEN")
        for token in ("", "FAKE TOKEN", "FAKE\x16TOKEN", "FAKE\nTOKEN"):
            with self.assertRaisesRegex(p.Stop, "TOKEN_INPUT_INVALID"):
                p.normalize_access_token(token)


if __name__ == "__main__":
    unittest.main()
