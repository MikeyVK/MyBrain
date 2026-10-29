"""Windows-only inert managed Git-stage promotion behavior."""
import ctypes
import hashlib
import os
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest
import zipfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from provision import GitProvider
from contracts import DeploymentError

@unittest.skipUnless(os.name=="nt","Windows sharing semantics required")
class GitPromotionTests(unittest.TestCase):
    def setUp(self):
        self.scratch=tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.target=Path(self.scratch.name)/"target with spaces"
        self.stage=self.target/".deployment/git-stage"
        (self.stage/"cmd").mkdir(parents=True)
        (self.stage.parent/"owner.json").write_bytes(b'{"package_id":"synthetic"}')
        self.data=b"inert managed file"
        (self.stage/"cmd/git.txt").write_bytes(self.data)
        (self.target/"tooling").mkdir()
        self.destination=self.target/"tooling/git"
        self.archive=Path(self.scratch.name)/"git.zip"
        with zipfile.ZipFile(self.archive,"w") as z:
            z.writestr("cmd/git.txt",self.data)
        self.sha=hashlib.sha256(self.archive.read_bytes()).hexdigest()
        self.provider=GitProvider()
        self.kernel=ctypes.WinDLL("kernel32",use_last_error=True)
        self.kernel.CreateFileW.restype=ctypes.c_void_p
        self.kernel.CreateFileW.argtypes=[ctypes.c_wchar_p,ctypes.c_ulong,ctypes.c_ulong,ctypes.c_void_p,ctypes.c_ulong,ctypes.c_ulong,ctypes.c_void_p]
        self.kernel.CloseHandle.argtypes=[ctypes.c_void_p]

    def hold(self):
        handle=self.kernel.CreateFileW(str(self.stage/"cmd/git.txt"),0x80000000,3,None,3,0,None)
        self.assertNotEqual(handle,ctypes.c_void_p(-1).value)
        return handle

    def promote(self):
        self.provider.promote(self.target,self.archive,self.sha)

    def test_released_reader_allows_exact_promotion(self):
        handle=self.hold()
        worker=threading.Thread(target=lambda:(time.sleep(.2),self.kernel.CloseHandle(handle)))
        worker.start()
        try:self.promote()
        finally:worker.join()
        self.assertFalse(self.stage.exists())
        self.assertEqual((self.destination/"cmd/git.txt").read_bytes(),self.data)

    def test_persistent_reader_refuses_with_finite_budget(self):
        handle=self.hold()
        start=time.monotonic()
        try:
            with self.assertRaises(OSError):self.promote()
        finally:self.kernel.CloseHandle(handle)
        elapsed=time.monotonic()-start
        self.assertGreaterEqual(elapsed,.8)
        self.assertLess(elapsed,3)
        self.assertEqual((self.stage/"cmd/git.txt").read_bytes(),self.data)
        self.assertFalse(self.destination.exists())

    def test_foreign_destination_preserved(self):
        self.destination.mkdir()
        sentinel=self.destination/"foreign.txt";sentinel.write_bytes(b"foreign")
        with self.assertRaises(DeploymentError) as caught:self.promote()
        self.assertEqual(caught.exception.code,"git_destination_conflict")
        self.assertEqual(sentinel.read_bytes(),b"foreign")
        self.assertEqual((self.stage/"cmd/git.txt").read_bytes(),self.data)

    def test_changed_stage_bytes_preserved(self):
        changed=self.stage/"cmd/git.txt";changed.write_bytes(b"inert change")
        with self.assertRaises(DeploymentError) as caught:self.promote()
        self.assertEqual(caught.exception.code,"git_stage_inventory_conflict")
        self.assertEqual(changed.read_bytes(),b"inert change")
        self.assertFalse(self.destination.exists())

    def test_unknown_stage_bytes_preserved(self):
        extra=self.stage/"extra.txt";extra.write_bytes(b"inert extra")
        with self.assertRaises(DeploymentError) as caught:self.promote()
        self.assertEqual(caught.exception.code,"git_stage_inventory_conflict")
        self.assertEqual(extra.read_bytes(),b"inert extra")
        self.assertFalse(self.destination.exists())

    def test_change_during_sharing_wait_is_not_adopted(self):
        handle=self.hold()
        def change_and_release():
            time.sleep(.15)
            (self.stage/"cmd/git.txt").write_bytes(b"inert concurrent change")
            self.kernel.CloseHandle(handle)
        worker=threading.Thread(target=change_and_release);worker.start()
        try:
            with self.assertRaises(DeploymentError) as caught:self.promote()
        finally:worker.join()
        self.assertEqual(caught.exception.code,"git_stage_inventory_conflict")
        self.assertEqual((self.stage/"cmd/git.txt").read_bytes(),b"inert concurrent change")
        self.assertFalse(self.destination.exists())

if __name__=="__main__":unittest.main()
