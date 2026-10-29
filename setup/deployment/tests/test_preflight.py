"""Read-only public native Preflight behavior with deterministic inert transport outcomes."""
import hashlib
import io
import zipfile
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
URL="https://github.com/git-for-windows/git/releases/download/v2.56.0.windows.4/MinGit-2.56.0.4-64-bit.zip"

class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.scratch=tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.base=Path(self.scratch.name)
        self.package=self.base/"package";self.package.mkdir()
        self.target=self.base/"target with spaces"
        for name in ("Start-Deployment.ps1","Preflight.ps1"):
            shutil.copyfile(ROOT/name,self.package/name)
        self.manifest={"schema_version":1,"package_id":"inert-preflight","network_mode":"hybrid","files":[],
            "dependencies":[{"name":"MinGit","delivery":"download","version":"2.56.0.4","sha256":"0"*64,"provenance_url":URL}]}
        self.seal()
        self.shell=str(Path(os.environ["SystemRoot"])/"System32/WindowsPowerShell/v1.0/powershell.exe")
        self.git=shutil.which("git")
        self.assertIsNotNone(self.git,"Verified source test host requires Git")

    def seal(self):
        self.manifest["files"]=[{"path":p.name,"size_bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in self.package.iterdir() if p.name not in ("manifest.json","manifest.sha256")]
        body=json.dumps(self.manifest).encode()
        (self.package/"manifest.json").write_bytes(body)
        (self.package/"manifest.sha256").write_text(hashlib.sha256(body).hexdigest())

    def inventory(self,root):
        return {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob("*") if p.is_file()} if root.exists() else None

    def invoke(self,mode,path):
        before=self.inventory(self.package);target_before=self.inventory(self.target);caller=dict(os.environ)
        env={k:v for k,v in os.environ.items() if k.casefold()!="psmodulepath"};env["PATH"]=path
        result=subprocess.run([self.shell,"-NoProfile","-File",str(ROOT/"tests/Invoke-PreflightFixture.ps1"),
            "-Package",str(self.package),"-Destination",str(self.target),"-Mode",mode],
            capture_output=True,text=True,env=env,timeout=25)
        self.assertEqual(self.inventory(self.package),before)
        self.assertEqual(self.inventory(self.target),target_before)
        self.assertEqual(dict(os.environ),caller)
        return result,json.loads(result.stdout)

    def test_suitable_git_requires_no_download_or_network(self):
        result,value=self.invoke("unavailable",str(Path(self.git).parent))
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertFalse(value["git"]["network_required"])
        self.assertFalse(value["git"]["download_required"])
        self.assertEqual(value["git"]["source"],"host")
        self.assertNotIn("primary_probe:",result.stderr)
        self.assertFalse(self.target.exists())

    def test_needed_fallback_primary_reachability_is_observed(self):
        result,value=self.invoke("reachable","")
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertTrue(value["git"]["network_required"])
        self.assertTrue(value["git"]["download_required"])
        self.assertEqual(value["git"]["availability"],"primary_reachable")
        self.assertIn("primary_probe:"+URL,result.stderr)
        self.assertFalse(self.target.exists())

    def test_unavailable_or_unproven_fallback_is_pending(self):
        for mode in ("unavailable","unproven"):
            with self.subTest(mode=mode):
                result,value=self.invoke(mode,"")
                self.assertEqual(result.returncode,2,result.stdout+result.stderr)
                self.assertEqual(value["code"],"git_download_unverified")
                self.assertTrue(value["git"]["network_required"])
                self.assertFalse(self.target.exists())

    def test_changed_cached_artifact_is_refused_and_preserved(self):
        cache=self.target/".deployment/downloads/mingit.zip"
        cache.parent.mkdir(parents=True);cache.write_bytes(b"inert changed cache")
        owner={"package_id":self.manifest["package_id"],"manifest_sha256":hashlib.sha256((self.package/"manifest.json").read_bytes()).hexdigest(),"target":str(self.target)}
        (self.target/".deployment/owner.json").write_text(json.dumps(owner))
        result,value=self.invoke("reachable","")
        self.assertEqual(result.returncode,4,result.stdout+result.stderr)
        self.assertEqual(value["code"],"git_cached_artifact_conflict")
        self.assertNotIn("primary_probe:",result.stderr)

    def test_verified_target_cache_needs_no_network(self):
        buffer=io.BytesIO()
        with zipfile.ZipFile(buffer,"w") as archive:archive.writestr("cmd/git.exe",b"inert nonexecutable fixture bytes")
        data=buffer.getvalue()
        self.manifest["dependencies"][0]["sha256"]=hashlib.sha256(data).hexdigest()
        self.seal()
        cache=self.target/".deployment/downloads/mingit.zip"
        cache.parent.mkdir(parents=True);cache.write_bytes(data)
        owner={"package_id":self.manifest["package_id"],"manifest_sha256":hashlib.sha256((self.package/"manifest.json").read_bytes()).hexdigest(),"target":str(self.target)}
        (self.target/".deployment/owner.json").write_text(json.dumps(owner))
        result,value=self.invoke("unavailable","")
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertEqual(value["git"]["source"],"verified_target_cache")
        self.assertFalse(value["git"]["network_required"])
        self.assertFalse(value["git"]["download_required"])
        self.assertNotIn("primary_probe:",result.stderr)

if __name__=="__main__":unittest.main()
