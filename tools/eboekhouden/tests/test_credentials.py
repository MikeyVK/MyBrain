"""Synthetic offline checks; never touch real Windows credentials."""
import unittest
from unittest.mock import patch
import contextlib
import io
import json
from pathlib import Path
import tempfile
import probe_rest as p
import credential_store as c
import setup_credential as setup


class MemoryBackend:
    def __init__(self, entry=None):
        self.entry = entry
        self.operations = []

    def read(self, target, include_secret=False):
        self.operations.append(("read", target))
        return self.entry

    def write(self, target, secret):
        self.operations.append(("write", target))
        self.entry = c.Entry(target, c.MARKER, c.COMMENT, c.LOCAL_MACHINE, secret)


class Checks(unittest.TestCase):
    def test_manual_gui_and_existing_helper_encodings_are_explicit(self):
        self.assertEqual(c.decode_blob("SYNTHETIC_TOKEN".encode("utf-16-le"), c.GUI_USERNAME, ""), "SYNTHETIC_TOKEN")
        self.assertEqual(c.decode_blob(b"SYNTHETIC_TOKEN", c.MARKER, c.COMMENT), "SYNTHETIC_TOKEN")
        for persist in (2, 3):
            backend = MemoryBackend(c.Entry(c.TARGET, c.GUI_USERNAME, "", persist, "SYNTHETIC_TOKEN"))
            self.assertEqual(c.CredentialStore(backend, lambda: "owner").load(), "SYNTHETIC_TOKEN")
        for raw, username, comment in [(b"UTF8_NOT_UTF16", c.GUI_USERNAME, ""),
                                        (b"A\x00B\x00", c.MARKER, c.COMMENT),
                                        (b"SECRET", "unknown", ""),
                                        (b"SECRET", c.GUI_USERNAME, "unexpected")]:
            with self.assertRaises(c.CredentialFailure) as caught:
                c.decode_blob(raw, username, comment)
            self.assertNotIn("SECRET", str(caught.exception))

    def test_gui_marker_does_not_accept_session_or_unknown_persistence(self):
        for persist in (0, 1, 4):
            with self.assertRaisesRegex(c.CredentialFailure, "NOT_MYBRAIN_OWNED"):
                c.CredentialStore(MemoryBackend(c.Entry(c.TARGET, c.GUI_USERNAME, "", persist, "SYNTHETIC")), lambda: "owner").load()

    def test_missing_credential_has_no_fallback(self):
        backend = MemoryBackend()
        store = c.CredentialStore(backend, lambda: "S-1-5-21-1")
        with self.assertRaisesRegex(c.CredentialFailure, "CREDENTIAL_MISSING_RUN_SETUP"):
            store.load()
        self.assertEqual(backend.operations, [("read", c.TARGET)])

    def test_sandbox_identity_refused_before_read(self):
        backend = MemoryBackend()
        def blocked():
            return c.owner_sid(lambda: '"HOST\\CodexSandboxOffline","S-1-5-21-1"')
        with self.assertRaisesRegex(c.CredentialFailure, "WINDOWS_OWNER_REQUIRED"):
            c.CredentialStore(backend, blocked).load()
        self.assertEqual(backend.operations, [])

    def test_exact_key_and_no_unconfirmed_overwrite(self):
        entry = c.Entry(c.TARGET, c.MARKER, c.COMMENT, c.LOCAL_MACHINE, "SYNTHETIC_TOKEN")
        backend = MemoryBackend(entry)
        store = c.CredentialStore(backend, lambda: "owner")
        self.assertEqual(store.load(), "SYNTHETIC_TOKEN")
        with self.assertRaisesRegex(c.CredentialFailure, "REPLACEMENT_NOT_CONFIRMED"):
            store.save("NEW_SYNTHETIC")
        self.assertNotIn("SYNTHETIC_TOKEN", repr(entry))
        self.assertTrue(all(target == c.TARGET for op, target in backend.operations))

    def test_unrelated_exact_key_entry_never_overwritten(self):
        backend = MemoryBackend(c.Entry(c.TARGET, "other", "other", c.LOCAL_MACHINE, "other"))
        store = c.CredentialStore(backend, lambda: "owner")
        with self.assertRaisesRegex(c.CredentialFailure, "NOT_MYBRAIN_OWNED"):
            store.save("NEW_SYNTHETIC", replace=True)
        self.assertFalse(any(op == "write" for op, target in backend.operations))

    def test_setup_requires_admin_confirmation_and_matching_hidden_entry(self):
        backend = MemoryBackend()
        store = c.CredentialStore(backend, lambda: "owner")
        with self.assertRaisesRegex(c.CredentialFailure, "ADMINISTRATION_NOT_CONFIRMED"):
            setup.setup(store, lambda prompt: "NO", lambda prompt: self.fail("Secret requested"))
        secrets = iter(["ONE_SYNTHETIC", "OTHER_SYNTHETIC"])
        with self.assertRaisesRegex(c.CredentialFailure, "TOKEN_CONFIRMATION_MISMATCH"):
            setup.setup(store, lambda prompt: "JA", lambda prompt: next(secrets))
        self.assertFalse(any(op == "write" for op, target in backend.operations))

    def test_replace_prompt_can_cancel_before_secret_input(self):
        backend = MemoryBackend(c.Entry(c.TARGET, c.MARKER, c.COMMENT, c.LOCAL_MACHINE, "OLD_SYNTHETIC"))
        store = c.CredentialStore(backend, lambda: "owner")
        answers = iter(["JA", "NO"])
        with self.assertRaisesRegex(c.CredentialFailure, "REPLACEMENT_NOT_CONFIRMED"):
            setup.setup(store, lambda prompt: next(answers), lambda prompt: self.fail("Secret requested"))
        self.assertEqual(backend.entry.value, "OLD_SYNTHETIC")

    def test_setup_writes_only_owned_key_local_machine_marker(self):
        backend = MemoryBackend()
        store = c.CredentialStore(backend, lambda: "owner")
        setup.setup(store, lambda prompt: "JA", lambda prompt: "SYNTHETIC_TOKEN")
        self.assertEqual(backend.entry.persist, 2)
        self.assertEqual(backend.entry.username, c.MARKER)
        self.assertEqual(backend.entry.target, c.TARGET)

    def test_noninteractive_read_reuses_credential_and_preserves_prior_output(self):
        backend = MemoryBackend(c.Entry(c.TARGET, c.MARKER, c.COMMENT, c.LOCAL_MACHINE, "SYNTHETIC_ACCESS"))
        class FakeTransport:
            def request(self, method, path, body=None, token=None, bearer=False):
                if method == "POST":
                    self.asserted_access = body["accessToken"]
                    return {"token": "SYNTHETIC_SESSION", "expiresIn": 60}
                if method == "DELETE":
                    return None
                return {"id": 17, "description": "SYNTHETIC_ACCESS", "rows": [], "vat": []}
        store_type = c.CredentialStore
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            previous = root / "selected-mutation.json"
            previous.write_text("SYNTHETIC_PRIOR_RESULT")
            with patch.object(p, "runtime_area", return_value=root), \
                 patch.object(p.sys, "argv", ["probe_rest.py", "--number", "17"]), \
                 patch.object(c, "owner_sid", return_value="S-1-5-21-1"), \
                 patch.object(c, "WindowsBackend", return_value=backend), \
                 patch.object(c, "CredentialStore", side_effect=lambda b: store_type(b, lambda: "synthetic-owner")), \
                 patch.object(p, "set_private_acl"), \
                 patch.object(p, "Transport", FakeTransport), \
                 patch.object(p, "hidden", side_effect=AssertionError("No secret prompt allowed")):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    p.main()
            self.assertEqual(previous.read_text(), "SYNTHETIC_PRIOR_RESULT")
            files = list(root.glob("selected-mutation-*.json"))
            self.assertEqual(len(files), 1)
            saved = files[0].read_text()
            self.assertEqual(json.loads(saved)["mutation"]["id"], 17)
            self.assertNotIn("SYNTHETIC_ACCESS", saved + output.getvalue())
            self.assertNotIn("SYNTHETIC_SESSION", saved + output.getvalue())


if __name__ == "__main__":
    unittest.main()
