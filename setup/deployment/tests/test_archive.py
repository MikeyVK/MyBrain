"""Archive delivery uses actual output bytes, independent extraction and conflict refusal."""
from pathlib import Path
import hashlib
import json
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from builder import ArchiveWriter
from contracts import ArchiveReader, DeploymentError

class ArchiveTests(unittest.TestCase):
    def test_actual_archive_extraction_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);package=root/"package";package.mkdir()
            data=b"selected source\n";(package/"source.txt").write_bytes(data)
            manifest={"schema_version":1,"package_id":"synthetic","files":[{"path":"source.txt","size_bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}]}
            body=json.dumps(manifest).encode();(package/"manifest.json").write_bytes(body)
            (package/"manifest.sha256").write_bytes(hashlib.sha256(body).hexdigest().encode())
            archive=root/"deliverable.zip";ArchiveWriter().write(package,archive)
            self.assertTrue(archive.is_file(),"public archive writer produced no deliverable")
            ArchiveReader().extract(archive,root/"fresh space path")
            self.assertEqual((root/"fresh space path/source.txt").read_bytes(),data)
            before=archive.read_bytes()
            with self.assertRaises(DeploymentError):
                ArchiveWriter().write(package,archive)
            self.assertEqual(archive.read_bytes(),before)

if __name__=="__main__":
    unittest.main()

