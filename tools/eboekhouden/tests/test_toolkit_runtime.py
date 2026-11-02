"""Synthetic portability boundaries; no host credentials or network."""
import ctypes
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch
import toolkit_runtime as runtime
import credential_store
import probe
from private_output import PrivateOutput

class RuntimeBoundaries(unittest.TestCase):
    def test_source_root_system_and_traversal_are_refused_without_mkdir(self):
        with patch.object(Path, "mkdir") as mkdir:
            for path in (runtime.SOURCE_ROOT, Path(runtime.SOURCE_ROOT.anchor),
                         runtime.WORKROOT / ".." / "escaped"):
                with self.subTest(path=str(path)), self.assertRaises(ValueError):
                    runtime.ensure_private_directory(path)
            mkdir.assert_not_called()

    def test_reparse_ancestor_is_refused_before_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve() / ".local-work"
            root.mkdir()
            original = Path.lstat
            def attributes(path, *args, **kwargs):
                actual = original(path, *args, **kwargs)
                if path == root:
                    return types.SimpleNamespace(st_mode=actual.st_mode, st_file_attributes=0x400)
                return actual
            with patch.object(runtime, "WORKROOT", root), patch.object(Path, "lstat", attributes):
                with self.assertRaisesRegex(ValueError, "REPARSE"):
                    runtime.private_path(root / "new.json")

    def test_fixed_output_preserves_redaction_and_rejects_outside_journal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve() / ".local-work"
            with patch.object(runtime, "WORKROOT", root):
                private = runtime.ensure_private_directory(root / "synthetic")
                output = PrivateOutput(private, ["SYNTHETIC_SECRET"])
                saved = output.save("receipt", {"value": "SYNTHETIC_SECRET", "token": "excluded"})
                self.assertNotIn("SYNTHETIC_SECRET", saved.read_text())
                self.assertNotIn("excluded", saved.read_text())
                with self.assertRaisesRegex(ValueError, "OUTSIDE_FIXED_WORKROOT"):
                    output.append(Path(tmp).resolve() / "unsafe.jsonl", {"state": "PENDING"})

    def test_unsafe_acl_target_refused_before_windows_security_call(self):
        with patch.object(ctypes, "WinDLL") as dll:
            with self.assertRaisesRegex(ValueError, "OUTSIDE_FIXED_WORKROOT"):
                probe.set_private_acl(runtime.SOURCE_ROOT, ("S-1-5-21-1",))
            dll.assert_not_called()

    def test_absent_or_disabled_host_config_stops_before_credential_api(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve() / ".local-work"
            root.mkdir()
            with patch.object(runtime, "WORKROOT", root), patch.object(ctypes, "WinDLL") as dll:
                with self.assertRaisesRegex(ValueError, "CONFIGURATION_REQUIRED"):
                    credential_store.WindowsBackend()
                (root / "host-config.json").write_text('{"allowLiveOperations": false}', encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "NOT_ENABLED"):
                    credential_store.WindowsBackend()
                dll.assert_not_called()

class OfflinePreservation(unittest.TestCase):
    def test_native_https_stops_before_connection_constructor_when_disabled(self):
        import http.client
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve() / ".local-work"
            root.mkdir()
            (root / "host-config.json").write_text('{"allowLiveOperations": false}', encoding="utf-8")
            with patch.object(runtime, "WORKROOT", root), patch.object(http.client.HTTPSConnection, "__init__") as connect:
                with self.assertRaisesRegex(ValueError, "NOT_ENABLED"):
                    runtime.live_connection(http.client.HTTPSConnection, "api.e-boekhouden.nl")
                connect.assert_not_called()

    def test_injected_connection_factory_needs_no_host_configuration(self):
        sentinel = object()
        calls = []
        def fake(*args, **kwargs):
            calls.append((args, kwargs))
            return sentinel
        self.assertIs(runtime.live_connection(fake, "synthetic.invalid", timeout=1), sentinel)
        self.assertEqual(calls, [(("synthetic.invalid",), {"timeout": 1})])

    def test_complete_preserved_module_imports_have_no_host_or_runtime_effects(self):
        import json
        import subprocess
        import sys
        modules = [
            "probe", "private_output", "app_session", "credential_store", "probe_rest", "setup_credential",
            "app_probe", "archive_read", "processed_invoice_probe", "preflight", "catalogue_match",
            "full_relation_names", "relation_supplement", "create_relations", "book_one_invoice",
            "reconcile_one_invoice", "rest_create_command", "upload_invoice", "prepare_edit", "change_ledger",
            "probe_link_contract", "link_invoice", "booking_source_guard", "repair_contract", "repair_io",
            "metadata_repair", "hours_cli", "hours_domain", "hours_io"]
        source = str(Path(__file__).resolve().parent.parent)
        script = r'''
import ctypes, http.client, importlib, json, pathlib, subprocess, sys
from unittest.mock import patch
sys.path.insert(0, sys.argv[1])
def forbidden(*args, **kwargs):
    raise AssertionError("IMPORT_HOST_OR_RUNTIME_EFFECT")
with patch.object(ctypes, "WinDLL", forbidden), patch.object(http.client, "HTTPSConnection", forbidden), \
     patch.object(subprocess, "run", forbidden), patch.object(pathlib.Path, "mkdir", forbidden), \
     patch.object(pathlib.Path, "read_text", forbidden), patch.object(pathlib.Path, "read_bytes", forbidden), \
     patch.object(pathlib.Path, "open", forbidden):
    for name in json.loads(sys.argv[2]):
        importlib.import_module(name)
print(json.dumps({"imported": len(json.loads(sys.argv[2]))}))
'''
        result = subprocess.run([sys.executable, "-I", "-B", "-c", script, source, json.dumps(modules)],
                                capture_output=True, text=True, timeout=30, shell=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"imported": len(modules)})
