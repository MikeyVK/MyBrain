"""Public process-level package admission regressions; synthetic bytes only."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
import stat

CLI = Path(__file__).resolve().parents[1] / "deploy.py"

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        (self.root / "data.txt").write_bytes(b"synthetic\n")
        self.manifest = {"schema_version": 1, "package_id": "synthetic", "files": [
            {"path": "data.txt", "size_bytes": 10, "sha256": hashlib.sha256(b"synthetic\n").hexdigest()}
        ]}
        self.seal()

    def seal(self):
        body = json.dumps(self.manifest).encode()
        (self.root / "manifest.json").write_bytes(body)
        (self.root / "manifest.sha256").write_text(hashlib.sha256(body).hexdigest()+"\n", encoding="ascii")

    def command(self):
        return subprocess.run([sys.executable, "-B", str(CLI), "check", "--package", str(self.root)],
                              capture_output=True, text=True)

    def test_valid(self):
        self.assertEqual(self.command().returncode, 0)

    def test_changed_byte_rejected(self):
        (self.root / "data.txt").write_text("corrupted\n", encoding="utf-8")
        self.assertEqual(self.command().returncode, 3)

    def test_unlisted_file_rejected(self):
        (self.root / "unlisted.txt").write_text("not admitted", encoding="utf-8")
        self.assertEqual(self.command().returncode, 3)

    def test_missing_file_rejected(self):
        (self.root / "data.txt").unlink()
        self.assertEqual(self.command().returncode, 3)

    def test_manifest_digest_rejected(self):
        (self.root / "manifest.sha256").write_text("0"*64, encoding="ascii")
        self.assertEqual(self.command().returncode, 3)

    def test_unknown_schema_rejected(self):
        self.manifest["schema_version"] = 2
        self.seal()
        self.assertEqual(self.command().returncode, 3)

    def test_unsafe_names_rejected(self):
        for name in ["../outside", "/absolute", "C:/drive", "a:b", "CON", "x.", "x ", "a\\b", "a//b"]:
            with self.subTest(name=name):
                self.manifest["files"][0]["path"] = name
                self.seal()
                self.assertEqual(self.command().returncode, 3)

    def test_duplicate_case_rejected(self):
        self.manifest["files"].append(dict(self.manifest["files"][0], path="DATA.TXT"))
        self.seal()
        self.assertEqual(self.command().returncode, 3)


    def test_unknown_field_rejected(self):
        self.manifest["unexpected"] = True
        self.seal()
        self.assertEqual(self.command().returncode, 3)

    def test_missing_manifest_rejected(self):
        (self.root / "manifest.json").unlink()
        self.assertEqual(self.command().returncode, 3)

    def test_preflight_never_creates_destination(self):
        target = self.root.parent / (self.root.name + "-absent")
        result = subprocess.run([sys.executable, "-B", str(CLI), "preflight",
            "--package", str(self.root), "--destination", str(target)], capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertFalse(target.exists())

    def test_foreign_destination_preserved(self):
        with tempfile.TemporaryDirectory() as t:
            target = Path(t)
            sentinel = target / "sentinel"
            sentinel.write_bytes(b"original")
            result = subprocess.run([sys.executable, "-B", str(CLI), "preflight",
                "--package", str(self.root), "--destination", str(target)], capture_output=True)
            self.assertEqual(result.returncode, 4)
            self.assertEqual(sentinel.read_bytes(), b"original")

    def test_archive_admission(self):
        for bad in (None, "../escape", "DATA.TXT", "symlink"):
            with self.subTest(bad=bad), tempfile.TemporaryDirectory() as t:
                archive = Path(t) / "test.zip"
                target = Path(t) / "new"
                with zipfile.ZipFile(archive, "w") as z:
                    for p in self.root.iterdir():
                        z.write(p, p.name)
                    if bad:
                        info = zipfile.ZipInfo(bad)
                        if bad == "symlink":
                            info.create_system = 3
                            info.external_attr = (stat.S_IFLNK | 0o777) << 16
                        z.writestr(info, b"synthetic")
                result = subprocess.run([sys.executable, "-B", str(CLI), "extract",
                    "--archive", str(archive), "--destination", str(target)], capture_output=True)
                self.assertEqual(result.returncode, 0 if bad is None else 3, result.stdout)
                self.assertEqual(target.exists(), bad is None)
                if bad is None:
                    self.assertEqual((target/"data.txt").read_bytes(), b"synthetic\n")

    def test_source_original_hash_is_independent_of_generated_output(self):
        self.manifest["sources"] = [{"id":"source", "tree_path":"source", "files":[{"path":"original.py","sha256":"0"*64}]}]
        self.seal()
        self.assertEqual(self.command().returncode, 3)

if __name__ == "__main__":
    unittest.main()
