"""Offline synthetic checks only; importing the probe does not contact a service."""
import contextlib
import io
import json
import unittest
from unittest.mock import patch

import probe


class Response:
    def __init__(self, status=200, data=None, content_type="application/json", raw=None):
        self.status = status
        self.data = json.dumps(data).encode() if raw is None else raw
        self.content_type = content_type

    def getheader(self, key, default=""):
        return self.content_type if key == "Content-Type" else default

    def read(self, maximum):
        return self.data[:maximum]


class Connection:
    def __init__(self, response):
        self.response = response
        self.requests = []
        self.closed = False

    def request(self, *args, **kwargs):
        self.requests.append((args, kwargs))

    def getresponse(self):
        return self.response

    def close(self):
        self.closed = True


class ScriptedReader:
    def __init__(self, replies):
        self.replies = list(replies)
        self.paths = []

    def get(self, path):
        self.paths.append(path)
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return reply


def admin(identifier=1):
    return {"valid": True, "currentAdministratie": {"id": identifier, "naam": "Synthetic"}}


class ProbeChecks(unittest.TestCase):
    def test_allowlist_rejects_writes_foreign_urls_and_query_injection(self):
        forbidden = [("PUT", "/api/v4/mutaties"), ("POST", "/api/v4/mutaties"),
                     ("DELETE", "/api/v4/auth/login"), ("GET", "https://other.invalid/x"),
                     ("POST", "/api/v4/auth/renew"), ("GET", "/api/v4/afschriftregels"),
                     ("GET", "/mutaties/search?mutatienummer=9&all=true"),
                     ("GET", "//other.invalid/api/v4/auth/userinfo")]
        for method, path in forbidden:
            with self.subTest(method=method, path=path):
                transport = probe.Transport(lambda *a, **kw: self.fail("Network constructed"))
                with self.assertRaisesRegex(probe.Stop, "REQUEST_NOT_ALLOWED"):
                    transport.request(method, path)

    def test_tls_origin_headers_and_no_redirect_follow(self):
        conn = Connection(Response(302, {"secret": "SHOULD_NOT_BE_READ"}))
        observed = []
        def factory(host, **kwargs):
            observed.append((host, kwargs))
            return conn
        with self.assertRaisesRegex(probe.Stop, "HTTP_302"):
            probe.Transport(factory).request("GET", "/api/v4/auth/userinfo", token="FAKE_TOKEN")
        self.assertEqual(len(conn.requests), 1)
        self.assertEqual(observed[0][0], "appapi.e-boekhouden.nl")
        self.assertEqual(observed[0][1]["timeout"], 15)
        tls = observed[0][1]["context"]
        self.assertTrue(tls.check_hostname)
        self.assertEqual(tls.verify_mode, probe.ssl.CERT_REQUIRED)
        self.assertTrue(conn.closed)

    def test_bounded_calls_and_response(self):
        transport = probe.Transport(lambda *a, **kw: Connection(Response(data={})))
        for _ in range(probe.MAX_CALLS):
            transport.request("GET", "/api/v4/auth/userinfo")
        with self.assertRaisesRegex(probe.Stop, "CALL_LIMIT"):
            transport.request("GET", "/api/v4/auth/userinfo")
        huge = probe.Transport(lambda *a, **kw: Connection(Response(raw=b"x" * (probe.MAX_BYTES + 1))))
        with self.assertRaisesRegex(probe.Stop, "RESPONSE_TOO_LARGE"):
            huge.request("GET", "/api/v4/auth/userinfo")

    def test_errors_never_disclose_vendor_body_or_exception(self):
        for conn in [Connection(Response(401, {"password": "FAKE_PASSWORD"})),
                     Connection(Response(raw=b"FAKE_PASSWORD-not-json"))]:
            with self.assertRaises(probe.Stop) as caught:
                probe.Transport(lambda *a, **kw: conn).request("GET", "/api/v4/auth/userinfo")
            self.assertNotIn("FAKE_PASSWORD", str(caught.exception))
        conn = Connection(Response())
        conn.request = lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("FAKE_PASSWORD"))
        with self.assertRaisesRegex(probe.Stop, "NETWORK_OR_TLS_FAILURE"):
            probe.Transport(lambda *a, **kw: conn).request("GET", "/api/v4/auth/userinfo")

    def test_exact_lookup_not_visible_number_as_internal_id(self):
        row = {"id": 902, "mutatieNummer": 17, "datum": "2000-01-01"}
        reader = ScriptedReader([[row], admin(), row, admin()])
        result = probe.read_one(reader, 17, (1, "Synthetic"), lambda rows: 0)
        self.assertEqual(result["id"], 902)
        self.assertIn("/api/v4/mutaties/902", reader.paths)
        self.assertNotIn("/api/v4/mutaties/17", reader.paths)

    def test_unknown_context_or_changed_context_stops_before_detail(self):
        with self.assertRaisesRegex(probe.Stop, "ACTIVE_ADMINISTRATION_UNKNOWN"):
            probe.active_administration({"valid": True, "administraties": [{"id": 1}]})
        row = {"id": 902, "mutatieNummer": 17, "datum": "2000-01-01"}
        reader = ScriptedReader([[row], admin(2)])
        with self.assertRaisesRegex(probe.Stop, "ADMINISTRATION_CHANGED"):
            probe.read_one(reader, 17, (1, "Synthetic"), lambda rows: 0)
        self.assertEqual(len(reader.paths), 2)

    def test_ambiguity_and_detail_identity_validation(self):
        rows = [{"id": n, "mutatieNummer": 17, "datum": "2000-01-01"} for n in (1, 2)]
        reader = ScriptedReader([rows, admin(), rows[0]])
        with self.assertRaisesRegex(probe.Stop, "DETAIL_IDENTITY_MISMATCH"):
            probe.read_one(reader, 17, (1, "Synthetic"), lambda options: 1)
        self.assertEqual(reader.paths[-1], "/api/v4/mutaties/2")

    def test_unknown_search_shape_or_excess_scope_stops(self):
        for value in [{"unrecognized": []}, {"id": 17}, [None], [{}] * 21]:
            with self.assertRaises(probe.Stop):
                probe.candidates(value, 17)

    def test_only_404_uses_second_documented_prefix_candidate(self):
        row = {"id": 902, "mutatieNummer": 17, "datum": "2000-01-01"}
        reader = ScriptedReader([probe.Stop("HTTP_404"), {"mutaties": [row]}, admin(), row, admin()])
        probe.read_one(reader, 17, (1, "Synthetic"), lambda options: 0)
        self.assertEqual(reader.paths[:2], ["/mutaties/search?mutatienummer=17", "/api/v4/mutaties/search?mutatienummer=17"])
        reader = ScriptedReader([probe.Stop("HTTP_401")])
        with self.assertRaisesRegex(probe.Stop, "HTTP_401"):
            probe.read_one(reader, 17, (1, "Synthetic"), lambda options: 0)
        self.assertEqual(len(reader.paths), 1)

    def test_projection_omits_profile_and_redacts_session_credentials(self):
        detail = {"id": 1, "mutatieNummer": 17, "omschrijving": "FAKE_PASSWORD FAKE_TOKEN",
                  "token": "FAKE_TOKEN", "user": {"email": "not-for-report"},
                  "mutatieRegels": [{"omschrijving": "FAKE_USER", "password": "FAKE_PASSWORD"}]}
        projected = json.dumps(probe.project_record(detail, ("FAKE_USER", "FAKE_PASSWORD", "FAKE_TOKEN")))
        for secret in ("FAKE_USER", "FAKE_PASSWORD", "FAKE_TOKEN", "not-for-report"):
            self.assertNotIn(secret, projected)

    def test_noninteractive_run_stops_before_prompts_or_network(self):
        with patch.object(probe.sys.stdin, "isatty", return_value=False):
            with self.assertRaisesRegex(probe.Stop, "INTERACTIVE_WINDOWS_CONSOLE_REQUIRED"):
                probe.protect_directory(probe.Path(__file__).parent)


if __name__ == "__main__":
    unittest.main()
