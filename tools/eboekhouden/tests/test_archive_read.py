"""Synthetic archive metadata scope and privacy checks; no real credentials."""
import json
import unittest
import archive_read as p


AUTH = {"loginOk": True, "twoFactorCodeRequired": False, "token": "FAKE_JWT"}
ADMIN = {"valid": True, "currentAdministratie": {"id": 1, "naam": "Synthetic"}}

def listing(identifier=0):
    return {"id": identifier, "naam": "Synthetic", "directories": [{"id": 10, "naam": "FAKE_PASSWORD"}],
            "files": [{"id": 20, "naam": "FAKE_JWT.pdf", "datum": "2000-01-01", "directoryId": identifier,
                       "scanStatus": 0, "data": "CONTENT_MUST_NOT_BE_SAVED"}]}

class FakeTransport:
    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []
    def request(self, method, path, body=None, token=None):
        self.calls.append((method, path))
        return self.replies.pop(0)

class Checks(unittest.TestCase):
    def test_allowlist_excludes_all_writes_downloads_financial_queries_and_unknown_routes(self):
        for method, path in [("POST", "/api/v4/bestanden/koppel"), ("POST", "/api/v4/bestanden/upload"),
                             ("POST", "/api/v4/mutaties/filter"), ("DELETE", "/api/v4/bestanden/bestand/20"),
                             ("GET", "/api/v4/bestanden/download/20"), ("GET", "/api/v4/bestanden/bestand/20"),
                             ("GET", "/api/v4/mutaties/17"), ("GET", "https://other.invalid/x")]:
            with self.assertRaisesRegex(p.core.app.Stop, "ARCHIVE_REQUEST_NOT_ALLOWED"):
                p.Transport(lambda *args, **kwargs: self.fail("Connection constructed")).request(method, path)

    def test_wrong_admin_stops_before_archive_read(self):
        transport = FakeTransport([AUTH, ADMIN])
        with self.assertRaisesRegex(p.core.app.Stop, "ADMINISTRATION_MISMATCH"):
            p.read_metadata(transport, p.core.Login("FAKE_USER", "FAKE_PASSWORD"), 2)
        self.assertEqual(len(transport.calls), 2)

    def test_root_only_projection_redacts_secrets_and_excludes_content(self):
        transport = FakeTransport([AUTH, ADMIN, listing(), ADMIN])
        result = p.read_metadata(transport, p.core.Login("FAKE_USER", "FAKE_PASSWORD"), 1)
        text = json.dumps(result)
        for secret in ("FAKE_PASSWORD", "FAKE_JWT", "CONTENT_MUST_NOT_BE_SAVED"):
            self.assertNotIn(secret, text)
        self.assertEqual(transport.calls, [("POST", "/api/v4/auth/login"), ("GET", "/api/v4/auth/userinfo"),
                                           ("GET", "/api/v4/bestanden"), ("GET", "/api/v4/auth/userinfo")])

    def test_one_chosen_directory_must_exist_in_root(self):
        transport = FakeTransport([AUTH, ADMIN, listing(), listing(10), ADMIN])
        result = p.read_metadata(transport, p.core.Login("FAKE_USER", "FAKE_PASSWORD"), 1, 10)
        self.assertEqual(result["selectedDirectory"]["id"], 10)
        transport = FakeTransport([AUTH, ADMIN, listing()])
        with self.assertRaisesRegex(p.core.app.Stop, "DIRECTORY_NOT_IN_ROOT_LISTING"):
            p.read_metadata(transport, p.core.Login("FAKE_USER", "FAKE_PASSWORD"), 1, 999)
        self.assertEqual(len(transport.calls), 3)

    def test_unknown_shape_has_types_not_values_and_hard_entry_cap(self):
        with self.assertRaises(p.ShapeFailure) as caught:
            p.project_listing({"FAKE_PASSWORD": {"secret": "VALUE_NOT_FOR_OUTPUT"}}, ("FAKE_PASSWORD",))
        text = json.dumps(caught.exception.shape)
        self.assertNotIn("FAKE_PASSWORD", text)
        self.assertNotIn("VALUE_NOT_FOR_OUTPUT", text)
        large = listing()
        large["files"] = large["files"] * 201
        with self.assertRaises(p.ShapeFailure):
            p.project_listing(large, ())

    def test_context_change_prevents_result_return(self):
        changed = {"valid": True, "currentAdministratie": {"id": 2, "naam": "Synthetic"}}
        transport = FakeTransport([AUTH, ADMIN, listing(), changed])
        with self.assertRaisesRegex(p.core.app.Stop, "ADMINISTRATION_CHANGED"):
            p.read_metadata(transport, p.core.Login("FAKE_USER", "FAKE_PASSWORD"), 1)


if __name__ == "__main__":
    unittest.main()
