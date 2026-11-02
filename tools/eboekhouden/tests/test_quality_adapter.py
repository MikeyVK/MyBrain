"""Offline bootstrap-candidate verification; no administration or vault access."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("candidate_adapter", Path(__file__).resolve().parent.parent / "quality" / "adapter.py")
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)
PINS = {"pytest": "9.1.1", "pytest-cov": "7.1.0", "pytest-xdist": "3.8.0",
        "coverage": "7.16.2", "pytest-asyncio": "1.4.0"}


class Admission(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name).resolve()
        self.root = self.workspace / "tools" / "eboekhouden"
        self.root.mkdir(parents=True)
        (self.root / "tests").mkdir()
        (self.root / ".venv" / ("Scripts" if os.name == "nt" else "bin")).mkdir(parents=True)
        self.python = self.root / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        self.python.write_bytes(b"synthetic-interpreter-not-executed")
        (self.root / ".venv" / "pyvenv.cfg").write_text("include-system-site-packages = false\n")
        self.cfg = dict(workspace=str(self.workspace), interpreter=str(self.python),
                        python_version="3.15.0", pins=PINS)
        self.calls = []

    def content(self, path=None, text="answer = 42\n"):
        return dict(operation="syntax", target_path=str(path or self.root / "new.py"),
                    content=text, args=[], execution_context={"scratch_directory": str(self.workspace)})

    def fake(self, argv, **kwargs):
        self.calls.append((argv, kwargs))
        job = json.loads(kwargs["input"])
        return types.SimpleNamespace(returncode=0, stdout=json.dumps({"status": "passed",
            "identity": {"python": "3.15.0", "prefix": str(self.root / ".venv"), "pins": PINS},
            "parsed": 1}))

    def test_inside_content_fixed_isolated_interpreter(self):
        result, code = adapter.run(self.content(), self.cfg, self.fake)
        self.assertEqual((result["decision"]["status"], code), ("passed", 0))
        argv, kwargs = self.calls[0]
        self.assertEqual(argv[:3], [str(self.python), "-I", "-B"])
        self.assertFalse(kwargs["shell"])
        self.assertEqual(kwargs["cwd"], str(self.root))

    def test_outside_and_same_prefix_refused_before_native(self):
        for target in [self.workspace / "app.py", self.workspace / "tools" / "eboekhouden-other" / "x.py"]:
            with self.subTest(target=target):
                result, code = adapter.run(self.content(target), self.cfg, self.fake)
                self.assertEqual(code, 3)
                self.assertEqual(result["decision"]["message"], "OUTSIDE_APPROVED_ROOT")
        self.assertEqual(self.calls, [])

    def test_traversal_and_reparse_refused(self):
        value = self.content(self.root / ".." / "eboekhouden" / "new.py")
        self.assertEqual(adapter.run(value, self.cfg, self.fake)[1], 3)
        target = self.root / "existing.py"
        target.write_text("x=1")
        real = Path.lstat
        def observed(path, *a, **k):
            info = real(path, *a, **k)
            if path == target:
                return types.SimpleNamespace(st_mode=info.st_mode, st_file_attributes=0x400)
            return info
        with patch.object(Path, "lstat", observed):
            self.assertEqual(adapter.run(self.content(target), self.cfg, self.fake)[1], 3)
        self.assertEqual(self.calls, [])

    def test_real_directory_link_refused(self):
        outside = self.workspace / "outside"
        outside.mkdir()
        link = self.root / "linked"
        if os.name == "nt":
            done = subprocess.run(["cmd", "/d", "/c", "mklink", "/J", str(link), str(outside)],
                                  capture_output=True, text=True, shell=False)
            self.assertEqual(done.returncode, 0, done.stderr)
        else:
            link.symlink_to(outside, target_is_directory=True)
        self.addCleanup(lambda: link.rmdir() if os.name == "nt" else link.unlink())
        result, code = adapter.run(self.content(link / "new.py"), self.cfg, self.fake)
        self.assertEqual(code, 3)
        self.assertEqual(result["decision"]["message"], "LINK_OR_REPARSE_PATH_REFUSED")
        self.assertEqual(self.calls, [])

    def test_no_inherited_secret_environment_or_path(self):
        with patch.dict(os.environ, {"SYNTHETIC_SECRET": "not-a-real-secret", "PYTHONPATH": "outside"}):
            adapter.run(self.content(), self.cfg, self.fake)
        env = self.calls[0][1]["env"]
        self.assertNotIn("SYNTHETIC_SECRET", env)
        self.assertNotIn("PYTHONPATH", env)
        self.assertNotIn("PATH", env)
        self.assertEqual(env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"], "1")

    def test_wrong_interpreter_and_global_site_packages_refused(self):
        cfg = {**self.cfg, "interpreter": sys.executable}
        self.assertEqual(adapter.run(self.content(), cfg, self.fake)[1], 3)
        (self.root / ".venv" / "pyvenv.cfg").write_text("include-system-site-packages = true\n")
        self.assertEqual(adapter.run(self.content(), self.cfg, self.fake)[1], 3)
        self.assertEqual(self.calls, [])

    def test_test_selection_outside_tests_and_native_args_refused(self):
        source = self.root / "module.py";source.write_text("x=1")
        value = dict(operation="tests", targets=[str(source)], args=[],
                     execution_context={"scratch_directory": str(self.workspace)})
        self.assertEqual(adapter.run(value, self.cfg, self.fake)[1], 3)
        value = self.content();value["args"] = ["--collect-only"]
        self.assertEqual(adapter.run(value, self.cfg, self.fake)[1], 3)
        self.assertEqual(self.calls, [])

    def test_selection_empty_or_link_or_nonpython_refused(self):
        value = dict(operation="syntax", targets=[], args=[],
                     execution_context={"scratch_directory": str(self.workspace)})
        self.assertEqual(adapter.run(value, self.cfg, self.fake)[1], 3)

    def test_private_or_environment_source_never_admitted(self):
        for directory in ('.venv','.local-work'):
            p=self.root/directory/'hidden.py';p.parent.mkdir(exist_ok=True);p.write_text('x=1')
            self.assertEqual(adapter.run(self.content(p),self.cfg,self.fake)[1],3)
            value=dict(operation='syntax',targets=[str(p)],args=[],execution_context={'scratch_directory':str(self.workspace)})
            self.assertEqual(adapter.run(value,self.cfg,self.fake)[1],3)
        self.assertEqual(self.calls,[])
        p = self.root / "readme.txt";p.write_text("x")
        value["targets"] = [str(p)]
        self.assertEqual(adapter.run(value, self.cfg, self.fake)[1], 3)

    def test_native_exit_or_identity_mismatch_not_passed(self):
        def wrong(*a, **k):
            result = self.fake(*a, **k);result.returncode = 1;return result
        self.assertEqual(adapter.run(self.content(), self.cfg, wrong)[1], 3)
        def wrong_identity(*a, **k):
            result=self.fake(*a, **k);v=json.loads(result.stdout);v['identity']['prefix']='outside';result.stdout=json.dumps(v);return result
        self.assertEqual(adapter.run(self.content(), self.cfg, wrong_identity)[1], 3)

    def test_inside_selection_coverage_exact_files_and_directory_expansion(self):
        folder=self.root/'selected';folder.mkdir();a=folder/'one.py';b=folder/'two.py'
        a.write_text('x=1');b.write_text('y=2')
        value=dict(operation='syntax',targets=[str(a)],args=[],execution_context={'scratch_directory':str(self.workspace)})
        result,code=adapter.run(value,self.cfg,self.fake)
        self.assertEqual(code,0)
        self.assertEqual(result['coverage'],{'targets':['tools/eboekhouden/selected/one.py'],'expanded':False})
        self.assertEqual(result['required_targets'],[])
        value['targets']=[str(folder)]
        result,code=adapter.run(value,self.cfg,self.fake)
        self.assertEqual(code,0)
        self.assertEqual(set(result['coverage']['targets']),{'tools/eboekhouden/selected/one.py','tools/eboekhouden/selected/two.py'})
        self.assertTrue(result['coverage']['expanded'])

    def test_outside_selection_and_failed_native_have_no_fictitious_coverage(self):
        outside=self.workspace/'outside.py';outside.write_text('x=1')
        value=dict(operation='syntax',targets=[str(outside)],args=[],execution_context={'scratch_directory':str(self.workspace)})
        result,code=adapter.run(value,self.cfg,self.fake)
        self.assertEqual(code,3);self.assertIsNone(result['coverage']);self.assertEqual(result['required_targets'],[])
        self.assertEqual(self.calls,[])
        inside=self.root/'inside.py';inside.write_text('x=(');value['targets']=[str(inside)]
        def failed(*a,**k):
            r=self.fake(*a,**k);v=json.loads(r.stdout);v.update(status='failed',message='SYNTAX_FAILED');r.stdout=json.dumps(v);r.returncode=1;return r
        result,code=adapter.run(value,self.cfg,failed)
        self.assertEqual(code,1);self.assertIsNone(result['coverage']);self.assertEqual(result['required_targets'],[])
