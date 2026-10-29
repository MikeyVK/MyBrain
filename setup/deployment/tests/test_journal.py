"""Public journal behavior: conflicts, live/stale locks and preserved partial stages."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from journal import Journal
from contracts import DeploymentError, digest

class JournalTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.base = Path(self.scratch.name)
        self.package = self.base / "package"
        self.package.mkdir()
        (self.package/"manifest.json").write_bytes(b"synthetic")
        self.target = self.base / "target with spaces"
        self.journal = Journal(self.target, self.package, {"package_id":"synthetic"})

    def test_rerun_and_changed_outputs(self):
        with self.journal.exclusive():
            self.journal.put("workspace/source.py", b"original")
        with self.journal.exclusive():
            self.journal.put("workspace/source.py", b"original")
        (self.target/"workspace/source.py").write_bytes(b"edited")
        with self.assertRaises(DeploymentError):
            with self.journal.exclusive():
                self.fail("edited content admitted")
        self.assertEqual((self.target/"workspace/source.py").read_bytes(), b"edited")

    def test_concurrent_and_stale_lock(self):
        with self.journal.exclusive():
            with self.assertRaises(DeploymentError):
                self.journal.recover_lock()
        self.journal.lock.write_text(json.dumps({"pid":2147483647,"owner":self.journal.owner}))
        self.journal.recover_lock()
        self.assertFalse(self.journal.lock.exists())

    def test_interrupted_stage_quarantine_preserves_bytes(self):
        with self.journal.exclusive():
            self.journal.stage("environment", "running")
            self.journal.put(".venv/partial", b"keep me")
        with self.journal.exclusive():
            self.journal.quarantine_incomplete("environment", self.target/".venv")
            self.assertFalse((self.target/".venv").exists())
            copies = list((self.target/".deployment/quarantine").rglob("partial"))
            self.assertEqual(copies[0].read_bytes(), b"keep me")
            self.journal.stage("environment", "complete")
        self.journal.validate()


    def test_windows_reader_sharing_delay_preserves_atomic_update(self):
        import ctypes
        import threading
        import time
        from journal import atomic_json
        path=self.base/"record.json"
        atomic_json(path,{"value":"before"})
        kernel=ctypes.WinDLL("kernel32",use_last_error=True)
        kernel.CreateFileW.restype=ctypes.c_void_p
        kernel.CreateFileW.argtypes=[ctypes.c_wchar_p,ctypes.c_ulong,ctypes.c_ulong,ctypes.c_void_p,ctypes.c_ulong,ctypes.c_ulong,ctypes.c_void_p]
        kernel.CloseHandle.argtypes=[ctypes.c_void_p]
        handle=kernel.CreateFileW(str(path),0x80000000,3,None,3,0,None)
        self.assertNotEqual(handle,ctypes.c_void_p(-1).value)
        def release():
            time.sleep(.15)
            kernel.CloseHandle(handle)
        worker=threading.Thread(target=release)
        worker.start()
        try:
            atomic_json(path,{"value":"after"})
        finally:
            worker.join()
        self.assertEqual(json.loads(path.read_bytes()),{"value":"after"})

    def test_pending_atomic_bytes_are_preserved_on_explicit_recovery(self):
        self.journal.claim()
        pending=self.journal.path.with_suffix(".json.new")
        pending.write_bytes(b"preserve interrupted metadata")
        self.journal.recover_lock()
        with self.journal.exclusive():
            self.journal.put("workspace/recovered.txt",b"recovered")
        copies=list((self.target/".deployment/quarantine").glob("metadata-*"))
        self.assertEqual(len(copies),1)
        self.assertEqual(copies[0].read_bytes(),b"preserve interrupted metadata")
        self.assertEqual((self.target/"workspace/recovered.txt").read_bytes(),b"recovered")

if __name__ == "__main__":
    unittest.main()
