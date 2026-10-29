"""Local runtime recreation using admitted artifacts and the package's own init primitive."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib
import urllib.request
import zipfile
from contracts import ArchiveReader, DeploymentError, PackageVerifier, digest, no_links, tree_files
from journal import Journal, atomic_json
from sources import ConsumerRenderer, SourceRestorer

def run(arguments: list[str], *, cwd: Path, env: dict | None = None) -> str:
    completed = subprocess.run(arguments, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
    if completed.returncode:
        raise RuntimeError(json.dumps({"command":Path(arguments[0]).name,"exit":completed.returncode,
                                      "stdout":completed.stdout,"stderr":completed.stderr}))
    return completed.stdout.strip()

def base_environment(workspace: Path, git: str) -> dict:
    environment = dict(os.environ)
    for key in list(environment):
        if key.upper().startswith(("PGMCP_","GIT_","PIP_","PYTHON","_PYTHON")) or key=="VIRTUAL_ENV":
            del environment[key]
    environment.update({
        "PGMCP_WORKSPACE_ROOT":str(workspace), "PGMCP_SERVER_PROJECT_DIR":str(workspace/".pgmcp"),
        "PGMCP_CONFIG_ROOT":str(workspace/".pgmcp/config"),
        "PGMCP_TEMPLATE_ROOT":str(workspace/".pgmcp/template_suite"), "PGMCP_RESPONSE_MODE":"structured",
        "PYTHONDONTWRITEBYTECODE":"1", "PYTHONNOUSERSITE":"1", "PYTHONSAFEPATH":"1",
        "PIP_DISABLE_PIP_VERSION_CHECK":"1", "PIP_NO_INPUT":"1", "PIP_CONFIG_FILE":os.devnull,
        "PIP_CACHE_DIR":str(workspace.parent/".deployment/cache"),
        "TEMP":str(workspace.parent/".deployment/temp"), "TMP":str(workspace.parent/".deployment/temp"),
        "GIT_CONFIG_NOSYSTEM":"1", "GIT_CONFIG_GLOBAL":os.devnull,"GIT_CONFIG_SYSTEM":os.devnull,
        "PATH":str(workspace/".venv/Scripts")+os.pathsep+str(Path(git).parent)+os.pathsep+environment.get("PATH","")
    })
    return environment

class GitProvider:
    """Use an adequate existing Git or one pinned primary-download fallback."""
    def __init__(self, reader=None):
        self.reader=reader or ArchiveReader()

    def obtain(self, package: Path, target: Path, manifest: dict, journal: Journal) -> str:
        installed=shutil.which("git")
        if installed:
            version=run([installed,"--version"],cwd=target)
            match=re.search(r"(\d+)\.(\d+)\.(\d+)",version)
            if match and tuple(map(int,match.groups())) >= (2,51,0):
                return installed
        selected=next((d for d in manifest["dependencies"] if d["name"]=="MinGit"),None)
        if selected is None or selected["delivery"]!="download":
            raise DeploymentError("git_required",2)
        git=target/"tooling/git/cmd/git.exe"
        if git.is_file():
            return str(git)
        download=target/".deployment/downloads/mingit.zip"
        no_links(download)
        download.parent.mkdir(exist_ok=True)
        if not download.exists():
            urllib.request.urlretrieve(selected["provenance_url"], download)
        if digest(download)!=selected["sha256"]:
            raise DeploymentError("git_download_digest")
        stage=target/".deployment/git-stage"
        if stage.exists():
            journal.quarantine_incomplete("git",stage)
        journal.stage("git","running")
        self.reader.extract(download,stage,False)
        destination=target/"tooling/git"
        no_links(destination)
        destination.parent.mkdir(exist_ok=True)
        self.promote(target,download,selected["sha256"])
        journal.record_tree(destination)
        journal.stage("git","complete")
        if not git.is_file():
            raise DeploymentError("git_layout")
        return str(git)

    def promote(self, target: Path, archive: Path, expected_sha: str) -> None:
        """Promote only the exact managed Git stage; preserve conflicts and bounded failures."""
        import time
        stage=target/".deployment/git-stage"
        destination=target/"tooling/git"
        owner=target/".deployment/owner.json"
        no_links(owner)
        owner_hash=digest(owner)  # Caller holds the validated journal's exclusive ownership.
        if digest(archive)!=expected_sha:
            raise DeploymentError("git_download_digest")
        entries=self.reader.inspect(archive,False)
        with zipfile.ZipFile(archive) as z:
            expected={i.filename:hashlib.sha256(z.read(i)).hexdigest() for i in entries if not i.is_dir()}
        directories=set()
        for entry in entries:
            path=Path(entry.filename.rstrip("/"))
            directories.update(p.as_posix() for p in path.parents if p!=Path("."))
            if entry.is_dir():
                directories.add(path.as_posix())
        for attempt in range(20):
            no_links(owner);no_links(stage);no_links(destination)
            if digest(owner)!=owner_hash:
                raise DeploymentError("destination_identity",4)
            if destination.exists():
                raise DeploymentError("git_destination_conflict",4)
            observed=tree_files(stage)
            observed_directories={p.relative_to(stage).as_posix() for p in stage.rglob("*") if p.is_dir()}
            if (not stage.is_dir() or set(observed)!=set(expected) or observed_directories!=directories
                    or any(digest(path)!=expected[name] for name,path in observed.items())):
                raise DeploymentError("git_stage_inventory_conflict",4)
            try:
                stage.rename(destination)
                return
            except OSError as exc:
                if os.name!="nt" or getattr(exc,"winerror",None) not in (5,32,33):
                    raise
                if attempt==19:
                    raise OSError(exc.errno,"git_stage_promotion_blocked after 20 attempts; winerror="+str(exc.winerror)) from exc
                time.sleep(.05)  # At most 19 waits: 0.95 seconds, with complete re-admission per attempt.


class Provisioner:
    """Compose verified source, environment and consumer stages."""
    def __init__(self, restorer=None, git_provider=None, renderer=None, verifier=None, journal_factory=Journal):
        self.restorer=restorer or SourceRestorer()
        self.git_provider=git_provider or GitProvider()
        self.renderer=renderer or ConsumerRenderer()
        self.verifier=verifier or PackageVerifier()
        self.journal_factory=journal_factory
    def bootstrap(self, package: Path, target: Path, binding: str = "", recover: bool = False) -> dict:
        manifest=self.verifier.verify(package)
        journal=self.journal_factory(target,package,manifest)
        if recover:
            journal.recover_lock()
        with journal.exclusive():
            self.restorer.restore(package,journal,manifest)
            workspace=target/"workspace"
            git=self.git_provider.obtain(package,target,manifest,journal)
            for name in ("temp","cache"):
                path=target/".deployment"/name
                no_links(path)
                path.mkdir(exist_ok=True)
            env=base_environment(workspace,git)
            python=workspace/".venv/Scripts/python.exe"
            if journal.read()["stages"].get("environment")!="complete":
                journal.quarantine_incomplete("environment",workspace/".venv")
                if (workspace/".venv").exists():
                    raise DeploymentError("foreign_environment",4)
                journal.stage("environment","running")
                run([sys.executable,"-I","-B","-m","venv",str(workspace/".venv")],cwd=workspace,env=env)
                run([str(python),"-I","-B","-m","pip","install","--no-index","--find-links",str(package/"artifacts/wheels"),
                     "--require-hashes","--only-binary=:all:","--no-compile","-r",str(package/"tools/requirements.lock.txt")],cwd=workspace,env=env)
                journal.record_tree(workspace/".venv")
                journal.stage("environment","complete")
            if journal.read()["stages"].get("git_import")!="complete":
                journal.quarantine_incomplete("git_import",workspace/".git")
                if (workspace/".git").exists():
                    raise DeploymentError("foreign_git_metadata",4)
                admitted={item["path"] for source in manifest["sources"] if source["role"]=="deployment" for item in source["files"]}
                observed={name for name in tree_files(workspace) if not name.startswith(".venv/")}
                if observed!=admitted:
                    raise DeploymentError("unknown_source_before_import",4)
                journal.stage("git_import","running")
                empty=target/".deployment/no-hooks";empty.mkdir(exist_ok=True)
                command=[git,"-c","core.hooksPath="+str(empty),"-c","commit.gpgsign=false",
                         "-c","user.name=MyBrain Deployment","-c","user.email=deployment@invalid.example"]
                run(command+["init","--initial-branch=main"],cwd=workspace,env=env)
                run(command+["add","--all"],cwd=workspace,env=env)
                run(command+["commit","--no-gpg-sign","-m","Import screened deployment snapshot"],cwd=workspace,env=env)
                journal.stage("git_import","complete")
            server=workspace/".pgmcp"
            if journal.read()["stages"].get("server")!="complete":
                journal.quarantine_incomplete("server",server)
                if server.exists():
                    raise DeploymentError("foreign_server_root",4)
                journal.stage("server","running")
                run([str(python),"-I","-B","-m","mcp_server.cli","--init"],cwd=workspace,env=env)
                if not server.exists():
                    raise DeploymentError("server_init_failed")
                for p in server.rglob("*"):
                    if p.is_file() and not any(x in p.relative_to(server).parts for x in ("logs","temp")):
                        journal.put(p.relative_to(target).as_posix(),p.read_bytes())
                journal.stage("server","complete")
            roles=json.loads(run([str(python),"-I","-B","-c",
                "import yaml,json,pathlib; print(json.dumps(yaml.safe_load(pathlib.Path('setup/pgmcp/codex-roles.yaml').read_text(encoding='utf8'))['roles']))"],cwd=workspace,env=env))
            selected_binding=binding or "pgmcp-mybrain-"+hashlib.sha256(str(target).casefold().encode()).hexdigest()[:12]
            # Review exact source copies. Existing differing files are refused by Journal.put.
            for source in (workspace/"setup/pgmcp/agents").rglob("*.md"):
                rel=".pgmcp/agents/"+source.relative_to(workspace/"setup/pgmcp/agents").as_posix()
                self.deploy_reviewed(journal,"workspace/"+rel,source.read_bytes())
            for name in ("checks","tests","fixes"):
                self.deploy_reviewed(journal,"workspace/.pgmcp/config/"+name+".yaml",(workspace/f"setup/quality/{name}.yaml").read_bytes())
            self.deploy_reviewed(journal,"workspace/.pgmcp/config/contracts.yaml",(workspace/"setup/pgmcp/contracts.yaml").read_bytes())
            self.deploy_reviewed(journal,"workspace/.pgmcp/config/github.yaml",b'owner: "MikeyVK"\nrepo: "MyBrain"\n')
            for rel,data in self.renderer.render(workspace,selected_binding,roles,env["PATH"]):
                journal.put("workspace/"+rel,data)
            archive=next(d for d in manifest["dependencies"] if d["name"]=="Lychee")
            with zipfile.ZipFile(package/archive["filename"]) as z:
                ArchiveReader().inspect(package/archive["filename"],False)
                names=[n for n in z.namelist() if n.lower().endswith("lychee.exe")]
                if len(names)!=1:
                    raise DeploymentError("lychee_layout")
                journal.put("workspace/.venv/Scripts/lychee.exe",z.read(names[0]))
            if (server/"state.json").exists() or (server/"deliverables.json").exists():
                raise DeploymentError("unexpected_active_issue")
            journal.stage("consumers","complete")
            result=self.verify(package,target)
            journal.stage("local_verification","complete")
            from datetime import datetime, timezone
            report=target/".deployment/reports"/(datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")+".json")
            no_links(report)
            report.parent.mkdir(exist_ok=True)
            atomic_json(report,result)
            return result

    def deploy_reviewed(self,journal: Journal,rel: str,data: bytes) -> None:
        path=journal.target/rel
        # Package-created defaults are reconciled only before the reviewed consumer stage.
        if path.exists() and path.read_bytes()!=data:
            state=journal.read()
            old=state["outputs"].get(rel)
            if state["stages"].get("consumers")=="complete" or old is None or digest(path)!=old:
                raise DeploymentError("consumer_conflict:"+rel,4)
            no_links(path)
            temporary=path.with_suffix(path.suffix+".reviewed-new")
            if temporary.exists():
                raise DeploymentError("consumer_temporary_conflict",4)
            temporary.write_bytes(data)
            temporary.replace(path)
        journal.put(rel,data)

    def verify(self, package: Path, target: Path) -> dict:
        manifest=self.verifier.verify(package)
        journal=self.journal_factory(target,package,manifest)
        journal.validate()
        workspace=target/"workspace"
        python=workspace/".venv/Scripts/python.exe"
        configuration=tomllib.loads((workspace/".codex/config.toml").read_text("utf8"))
        if len(configuration["mcp_servers"])!=1:
            raise DeploymentError("binding_count")
        binding,entry=next(iter(configuration["mcp_servers"].items()))
        if Path(entry["cwd"])!=workspace or Path(entry["env"]["PGMCP_WORKSPACE_ROOT"])!=workspace or Path(entry["env"]["PGMCP_SERVER_PROJECT_DIR"])!=workspace/".pgmcp":
            raise DeploymentError("binding_root")
        env=base_environment(workspace,shutil.which("git",path=entry["env"]["PATH"]) or "git")
        env.update(entry["env"])
        env["PYTHONDONTWRITEBYTECODE"]="1"
        native=run([str(python),"-I","-B","-m","pip","check"],cwd=workspace,env=env)
        versions=json.loads(run([str(python),"-I","-B","-c",
            "import sys,struct,json,importlib.metadata as m; print(json.dumps({'python':sys.version.split()[0],'bits':struct.calcsize('P')*8,'harness':m.version('phase-gate-mcp')}))"],cwd=workspace,env=env))
        if versions!={"python":"3.15.0","bits":64,"harness":"4.0.0"}:
            raise DeploymentError("toolchain_identity")
        if (workspace/".pgmcp/state.json").exists() or (workspace/".pgmcp/deliverables.json").exists():
            raise DeploymentError("unexpected_active_issue")
        git=shutil.which("git",path=env["PATH"])
        if not git or run([git,"remote"],cwd=workspace,env=env):
            raise DeploymentError("unexpected_remote")
        sha=run([git,"rev-parse","HEAD"],cwd=workspace,env=env)
        git_status=run([git,"status","--porcelain"],cwd=workspace,env=env)
        if git_status:
            raise DeploymentError("restored_source_dirty",4)
        probe=json.loads(run([str(python),"-I","-B",str(package/"tools/probe.py"),str(workspace)],cwd=workspace,env=env))
        return {"status":"pending","code":"local_tooling_verified_host_activation_pending",
                "versions":versions,"pip_check":native,"binding":binding,"native_probe":probe,
                "snapshot_commit":sha,"original_sources":[{"id":s["id"],"original_sha":s.get("commit_sha")} for s in manifest["sources"]],
                "manifest_sha256":digest(package/"manifest.json"),"network_mode":manifest["network_mode"],
                "host_activation":"not_verified","second_pc_vm":"not_tested"}
