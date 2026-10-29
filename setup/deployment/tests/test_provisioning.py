"""Focused source restoration and target rendering behavior; synthetic source only."""
from pathlib import Path
import sys
import tempfile
import unittest
import json
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from journal import Journal
from sources import SourceRestorer

class ProvisioningTests(unittest.TestCase):
    def test_exact_source_restore_and_preserved_customization(self):
        with tempfile.TemporaryDirectory() as t:
            base=Path(t);package=base/"package";package.mkdir()
            (package/"manifest.json").write_text("{}")
            p=package/"payload/workspace/example.py";p.parent.mkdir(parents=True);p.write_bytes(b"original")
            manifest={"package_id":"synthetic","sources":[{"id":"deployment","role":"deployment","tree_path":"payload/workspace","files":[{"path":"example.py"}]}]}
            target=base/"target with spaces";journal=Journal(target,package,manifest)
            with journal.exclusive():
                SourceRestorer().restore(package,journal,manifest)
            self.assertEqual((target/"workspace/example.py").read_bytes(),b"original")
            (target/"workspace/example.py").write_bytes(b"customized")
            with self.assertRaises(Exception):
                with journal.exclusive():
                    SourceRestorer().restore(package,journal,manifest)
            self.assertEqual((target/"workspace/example.py").read_bytes(),b"customized")


    def test_snapshot_and_local_overlay_are_separately_exact(self):
        import subprocess
        from builder import SourceCapture
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)/"repo";root.mkdir();stage=Path(t)/"stage";stage.mkdir()
            git=lambda *args: subprocess.check_output(["git","-c","core.hooksPath="+str(Path(t)/"no-hooks"),"-c","commit.gpgsign=false","-c","user.name=Synthetic","-c","user.email=synthetic@invalid.example",*args],cwd=root)
            git("init","--initial-branch=main")
            (root/"README.md").write_bytes(b"# Original\n")
            (root/".env").write_bytes(b"SYNTHETIC_PRIVATE_VALUE=not-real\n")
            git("add","--all");git("commit","-m","Synthetic baseline")
            sha=git("rev-parse","HEAD").decode().strip()
            (root/"README.md").write_bytes(b"# Changed safe source\n")
            spec={"sources":[{"id":"deployment","root":str(root),"ref":sha,"role":"deployment"}]}
            sources,excluded=SourceCapture().capture(spec,stage)
            self.assertEqual((stage/"payload/workspace/README.md").read_bytes(),b"# Original\n")
            self.assertEqual((stage/"payload/snapshots/working-deployment/README.md").read_bytes(),b"# Changed safe source\n")
            self.assertFalse(list(stage.rglob(".git")))
            self.assertFalse(list(stage.rglob(".env")))
            self.assertTrue(excluded)
            overlay=next(x for x in sources if x["id"]=="working-deployment")
            self.assertEqual(overlay["operations"],[{"operation":"replace","path":"README.md"}])

    def test_rendered_binding_and_roles_are_target_local(self):
        import tomllib
        from sources import ConsumerRenderer
        root=Path("X:/synthetic-target/workspace")
        roles={k:{"name":"pgmcp-"+k,"description":"Synthetic","developer_instructions":"Read local protocol"} for k in ("co","imp","qa")}
        files=dict(ConsumerRenderer().render(root,"pgmcp-synthetic",roles,"TARGET-PATH"))
        config=tomllib.loads(files[".codex/config.toml"].decode())
        entry=config["mcp_servers"]["pgmcp-synthetic"]
        self.assertEqual(entry["env"]["PGMCP_WORKSPACE_ROOT"],str(root))
        self.assertNotIn("GITHUB_TOKEN",entry["env"])
        self.assertEqual(entry["env_vars"],["GITHUB_TOKEN"])
        self.assertEqual(len(config["agents"]),3)
        for role in roles.values():
            self.assertEqual(tomllib.loads(files[".codex/agents/"+role["name"]+".toml"].decode()),role)


    def test_inherited_git_pip_and_temp_routing_is_not_reused(self):
        import os
        from unittest.mock import patch
        from provision import base_environment
        workspace=Path("X:/synthetic-target/workspace")
        poison={"GIT_DIR":"unrelated","GIT_WORK_TREE":"unrelated","GIT_CONFIG_COUNT":"1",
                "GIT_CONFIG_KEY_0":"core.hooksPath","GIT_CONFIG_VALUE_0":"unrelated",
                "PIP_TARGET":"unrelated","PIP_PREFIX":"unrelated","PIP_ROOT":"unrelated",
                "PIP_USER":"1","PIP_CONFIG_FILE":"unrelated","PYTHONPATH":"unrelated",
                "TEMP":"unrelated","TMP":"unrelated"}
        with patch.dict(os.environ,poison):
            value=base_environment(workspace,"X:/synthetic-target/tooling/git/cmd/git.exe")
            self.assertEqual(os.environ["GIT_DIR"],"unrelated")
            self.assertEqual(os.environ["PIP_TARGET"],"unrelated")
        for key in ("GIT_DIR","GIT_WORK_TREE","GIT_CONFIG_COUNT","GIT_CONFIG_KEY_0","GIT_CONFIG_VALUE_0","PIP_TARGET","PIP_PREFIX","PIP_ROOT","PIP_USER","PYTHONPATH"):
            self.assertNotIn(key,value)
        self.assertEqual(value["TEMP"],str(workspace.parent/".deployment/temp"))
        self.assertEqual(value["TMP"],value["TEMP"])
        self.assertNotEqual(value["PIP_CONFIG_FILE"],"unrelated")

    def test_privacy_scanner_rejects_real_headers_without_matching_itself(self):
        from builder import screen
        from contracts import DeploymentError
        screen("setup/deployment/builder.py",(Path(__file__).parents[1]/"builder.py").read_bytes())
        with self.assertRaises(DeploymentError):
            screen("src/synthetic.py",("-----BEGIN "+"PRIVATE KEY-----").encode())

if __name__=="__main__":
    unittest.main()
