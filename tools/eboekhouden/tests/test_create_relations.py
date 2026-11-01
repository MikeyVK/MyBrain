from private_output import PrivateOutput as _SyntheticOutput

def synthetic_output(root, secrets=()):
    return _SyntheticOutput(root, secrets, path_validator=Path)

import json
from pathlib import Path
import tempfile
import unittest
import create_relations as p


class Checks(unittest.TestCase):
    def test_pending_persisted_before_create_and_exact_readback(self):
        events = []
        payload = {"type": "B", "code": "SYNTH01", "name": "Synthetic", "termOfPayment": 0}
        class Output:
            def append(self, path, value): events.append(value)
            def note(self, text): pass
        class Client:
            def detail(self, kind, identifier): return {**payload, "id": identifier}
        class API:
            client = Client()
            def create(self, body):
                self_outer.assertEqual(events[-1]["state"], "PENDING")
                return 10
        self_outer = self
        result = p.apply(API(), [{"payload": payload}], {}, None, "hash", Output())
        self.assertEqual([e["state"] for e in events], ["PENDING", "VERIFIED"])
        self.assertEqual(result[0]["id"], 10)
        self.assertFalse(p.same_payload(payload, {**payload, "termOfPayment": 14}))

    def test_uncertain_outcome_blocks_any_automatic_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = synthetic_output(root)
            class API:
                def create(self, payload): raise TimeoutError()
            payload = {"code": "SYNTH01", "name": "Synthetic"}
            journal = root / "journal.jsonl"
            with self.assertRaisesRegex(p.base.app.app.Stop, "NO_BLIND_RETRY"):
                p.apply(API(), [{"payload": payload}], {}, journal, "hash", output)
            with self.assertRaisesRegex(p.base.app.app.Stop, "UNCERTAIN"):
                p.previous_events(journal, "hash")
            self.assertEqual(len(journal.read_text().splitlines()), 2)

    def test_existing_identity_stops_before_create(self):
        detail = {"id": 1, "type": "B", "code": "OLD01", "name": "Different trade name", "vatNumber": "NL123456789B01"}
        class Client:
            paths = set()
            def get(self, path):
                if 'limit=1000' in path: return {"items": [{"id": 1, "type": "B", "code": "OLD01"}], "count": 1}
                return {"items": [], "count": 0}
        manifest = {"relations": [{"payload": {"code": "SYNTH01", "name": "Synthetic", "vatNumber": "NL123456789B01"}, "searchNames": ["Synthetic"]}]}
        with self.assertRaisesRegex(p.base.app.app.Stop, "EXISTING_IDENTITY"):
            p.precheck(Client(), manifest, {"relations": [detail]}, {})

    def test_writer_never_serializes_secret_keys_or_reflected_values(self):
        with tempfile.TemporaryDirectory() as directory:
            output = synthetic_output(directory, ["synthetic-secret"])
            path = output.save("test", {"token": "hidden", "payload": {"password": "hidden"}, "note": "synthetic-secret"})
            raw = path.read_text()
            self.assertNotIn('hidden', raw)
            self.assertNotIn('synthetic-secret', raw)
            self.assertIn('[REDACTED]', raw)

    def test_create_transport_only_admitted_payload_once(self):
        payload = {"code": "SYNTH01", "name": "Synthetic"}
        class Response:
            status = 201
            def getheader(self, *args): return "application/json"
            def read(self, *args): return b'{"id": 3, "code": "SYNTH01"}'
        calls = []
        class Connection:
            def request(self, method, path, **kwargs): calls.append((method, path))
            def getresponse(self): return Response()
            def close(self): pass
        client = p.base.Client([], {"acceptedAmazonCentralCode": "unused"}, lambda *args, **kwargs: Connection())
        client.token = "synthetic-session"
        api = p.RelationAPI(client, [payload])
        self.assertEqual(api.create(payload), 3)
        with self.assertRaises(p.base.app.app.Stop): api.create(payload)
        with self.assertRaises(p.base.app.app.Stop): api.create({"code": "OTHER", "name": "Other"})
        self.assertEqual(calls, [("POST", "/v1/relation")])

    def test_pending_write_failure_prevents_network(self):
        class Output:
            def append(self, *args): raise OSError("Synthetic disk failure")
        class API:
            def create(self, payload): raise AssertionError("Must not send")
        with self.assertRaises(OSError):
            p.apply(API(), [{"payload": {"code": "SYNTH01"}}], {}, None, "hash", Output())


if __name__ == "__main__":
    unittest.main()
