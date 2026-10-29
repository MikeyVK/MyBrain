"""Screen fixed source snapshots and assemble a manifest-bound distribution directory."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import zipfile
from contracts import ArchiveReader, DeploymentError, PackageVerifier, digest, no_links, relative_name, tree_files

def git_read(root: Path, *arguments: str) -> bytes:
    environment={k:v for k,v in os.environ.items() if not k.upper().startswith("GIT_")}
    environment.update({"GIT_CONFIG_NOSYSTEM":"1","GIT_CONFIG_GLOBAL":os.devnull,"GIT_CONFIG_SYSTEM":os.devnull})
    return subprocess.check_output(["git","--no-optional-locks","-c","core.fsmonitor=false","-c","safe.directory="+str(root.resolve()),"-C",str(root),*arguments],env=environment)

def screen(name: str, data: bytes) -> None:
    if name.endswith(".pdf"):
        if not name.startswith("docs/research/public/"):
            raise DeploymentError("nonpublic_pdf")
        return
    text=data.decode("utf-8-sig")
    if re.search(r"(?i)(?:[a-z]:[\\/](?:users|temp|program files)[\\/]|github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN (?:(?:RSA|EC|OPENSSH|DSA) )?PRIVATE KEY-----)",text):
        raise DeploymentError("source_privacy_signal:"+name)

def allowed(name: str) -> bool:
    roots=("docs/development/","docs/architecture/","docs/research/public/",
           "setup/pgmcp/","setup/quality/","setup/deployment/",".agents/","src/","tests/")
    return name in ("README.md","AGENTS.md",".gitignore",".gitattributes",".python-version","requirements-pgmcp.lock.txt") or name.startswith(roots)

class SourceCapture:
    """Read immutable Git objects and admitted stable auxiliary sources only."""
    def capture(self, spec: dict, stage: Path) -> tuple[list,list]:
        sources=[];exclusions=[]
        now=datetime.now(timezone.utc).isoformat()
        for value in spec["sources"]:
            root=Path(value["root"])
            sha=git_read(root,"rev-parse",value["ref"]+"^{commit}").decode().strip()
            names=git_read(root,"ls-tree","-r","--name-only",sha).decode().splitlines()
            tree="payload/workspace" if value["role"]=="deployment" else "payload/snapshots/"+relative_name(value["id"])
            selected=[];historical=[]
            for name in names:
                relative_name(name)
                if name in (".pgmcp/state.json",".pgmcp/deliverables.json"):
                    data=git_read(root,"show",sha+":"+name);screen(name,data)
                    out="payload/provenance/"+value["id"]+"/"+Path(name).name
                    path=stage/out;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
                    historical.append({"path":Path(name).name,"sha256":hashlib.sha256(data).hexdigest()})
                    continue
                if not allowed(name):
                    exclusions.append({"source_id":value["id"],"category":"unadmitted tracked source family","reason":"Outside the reviewed workspace/tooling snapshot allowlist"})
                    continue
                data=git_read(root,"show",sha+":"+name);screen(name,data)
                path=stage/tree/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
                selected.append({"path":name,"sha256":hashlib.sha256(data).hexdigest()})
            sources.append({"id":value["id"],"role":value["role"],"ref":value.get("original_ref",value["ref"]),"commit_sha":sha,
                            "capture_utc":now,"tree_path":tree,"original_ancestry_included":False,"files":selected})
            if historical:
                sources.append({"id":"history-"+value["id"],"role":"historical","ref":value.get("original_ref",value["ref"]),"commit_sha":sha,
                                "capture_utc":now,"tree_path":"payload/provenance/"+value["id"],
                                "original_ancestry_included":False,"files":historical})
        # Capture stable, allowlisted working differences as separately reconstructable overlays.
        for value in spec["sources"]:
            root=Path(value["root"])
            base=next(s for s in sources if s["id"]==value["id"])
            head_before=git_read(root,"rev-parse","HEAD").decode().strip()
            if head_before!=base["commit_sha"]:
                exclusions.append({"source_id":value["id"],"category":"post-freeze source progress",
                                   "reason":"Current HEAD differs from the explicitly frozen source ref; no live checkout takeover or later ancestry included"})
                continue
            changed=git_read(root,"diff","--name-only","--no-renames",base["commit_sha"],"-z").decode().split("\0")
            untracked=git_read(root,"ls-files","--others","--exclude-standard","-z").decode().split("\0")
            names=sorted(set(n for n in changed+untracked if n and allowed(n)))
            selected=[];operations=[];captured={}
            tree="payload/snapshots/working-"+value["id"]
            for name in names:
                p=root/relative_name(name);no_links(p)
                if p.is_file():
                    data=p.read_bytes();screen(name,data);captured[name]=data
                    out=stage/tree/name;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
                    selected.append({"path":name,"sha256":hashlib.sha256(data).hexdigest()})
                    operations.append({"operation":"replace" if any(x["path"]==name for x in base["files"]) else "add","path":name})
                elif not p.exists():
                    operations.append({"operation":"delete","path":name})
                else:
                    raise DeploymentError("working_source_not_regular")
            if git_read(root,"rev-parse","HEAD").decode().strip()!=head_before or any((root/n).read_bytes()!=data for n,data in captured.items()):
                raise DeploymentError("unstable_working_capture")
            if operations:
                sources.append({"id":"working-"+value["id"],"role":"local-source","ref":"screened-working-differences",
                                "commit_sha":None,"base_source_id":value["id"],"base_commit_sha":base["commit_sha"],
                                "capture_utc":now,"tree_path":tree,"original_ancestry_included":False,
                                "operations":operations,"files":selected})
        for local in spec.get("local_sources",[]):
            path=Path(local["root"])/relative_name(local["path"])
            no_links(path)
            before=path.read_bytes();sha=hashlib.sha256(before).hexdigest()
            screen(local["path"],before)
            if path.read_bytes()!=before:
                raise DeploymentError("unstable_local_capture")
            tree="payload/snapshots/"+relative_name(local["id"])
            out=stage/tree/local["path"];out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(before)
            sources.append({"id":local["id"],"role":"local-source","ref":"screened-local-source","commit_sha":None,
                            "capture_utc":now,"tree_path":tree,"original_ancestry_included":False,
                            "base_source_id":local["base_source_id"],"operation":"add",
                            "files":[{"path":local["path"],"sha256":sha}]})
        exclusions.extend(spec.get("excluded_candidates",[]))
        return sources,exclusions

class PackageBuilder:
    """Assemble declared source/artifact bytes without copying live directories."""
    def __init__(self, capture=None, verifier=None):
        self.capture=capture or SourceCapture()
        self.verifier=verifier or PackageVerifier()

    def build(self, output: Path, spec: dict) -> Path:
        no_links(output)
        if output.exists():
            raise DeploymentError("existing_build_destination",4)
        output.mkdir(parents=True)
        source_root=Path(spec["primary_root"])
        artifacts=Path(spec["artifact_root"])
        sources,exclusions=self.capture.capture(spec,output)
        dependencies=json.loads((artifacts/"dependencies.json").read_text("utf8"))
        needed=set()
        for dep in dependencies:
            if dep["delivery"]=="bundled":
                p=artifacts/dep["filename"]
                if digest(p)!=dep["sha256"]:
                    raise DeploymentError("dependency_digest")
                needed.add(dep["filename"])
            needed.update(dep["license_paths"])
            if dep.get("source_filename"):
                if digest(artifacts/dep["source_filename"])!=dep["source_sha256"]:
                    raise DeploymentError("dependency_source_digest")
                needed.add(dep["source_filename"])
        for rel in sorted(needed):
            relative_name(rel)
            out=output/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(artifacts/rel,out)
        tools=source_root/"setup/deployment"
        for p in tools.glob("*.py"):
            shutil.copyfile(p,output/"tools"/p.name) if (output/"tools").exists() else self.first_tool(p,output)
        for p in tools.glob("*.ps1"):
            shutil.copyfile(p,output/p.name)
        shutil.copyfile(artifacts/"requirements.lock.txt",output/"tools/requirements.lock.txt")
        shutil.copyfile(tools/"manifest.schema.json",output/"tools/manifest.schema.json")
        # Preserve original locks as source; bootstrap exclusively consumes the portable hash lock.
        for name in ("START-HERE.md","agent-handover.md"):
            start=tools/name
            if start.exists():
                shutil.copyfile(start,output/name)
        builder_sha=git_read(source_root,"rev-parse","HEAD").decode().strip()
        manifest={"schema_version":1,"package_id":"mybrain-"+builder_sha[:12],
                  "created_utc":datetime.now(timezone.utc).isoformat(),"builder_revision":builder_sha,
                  "target":{"os":"Windows 10 or newer","architecture":"x64","powershell_min":"5.1"},
                  "network_mode":"hybrid","sources":sources,"dependencies":dependencies,
                  "exclusions":exclusions+[{"category":x,"reason":"Outside owner workspace/tooling/setup transfer scope"} for x in
                      ("original Git ancestry/reflogs/linked worktree metadata","existing private runtime/database/mail/archive data",
                       "provider IDs and personal selection/resumption manifests","credentials/OAuth/account caches/private PDFs",
                       "live .pgmcp logs/cache/checkpoints and source-host .codex settings")],
                  "limits":{"files":20000,"uncompressed_bytes":2000000000},"files":[]}
        for rel,p in sorted(tree_files(output).items()):
            manifest["files"].append({"path":rel,"size_bytes":p.stat().st_size,"sha256":digest(p),
                                      "category":rel.split("/",1)[0],"source_id":"inventory"})
        body=(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n").encode()
        (output/"manifest.json").write_bytes(body)
        (output/"manifest.sha256").write_text(hashlib.sha256(body).hexdigest()+"\n",encoding="ascii",newline="\n")
        self.verifier.verify(output)
        return output

    def first_tool(self,p: Path,output: Path) -> None:
        (output/"tools").mkdir()
        shutil.copyfile(p,output/"tools"/p.name)


class ArchiveWriter:
    """Create new deliverable bytes and their independent outer digest."""
    def __init__(self, verifier=None, reader=None):
        self.verifier=verifier or PackageVerifier()
        self.reader=reader or ArchiveReader()

    def write(self, package: Path, archive: Path) -> None:
        self.verifier.verify(package)
        no_links(archive)
        if archive.exists() or archive.with_suffix(archive.suffix+".sha256").exists():
            raise DeploymentError("existing_archive",4)
        with zipfile.ZipFile(archive,"x",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for name,p in sorted(tree_files(package).items()):
                compression=zipfile.ZIP_STORED if p.suffix.lower() in (".zip",".whl",".gz",".pdf") else zipfile.ZIP_DEFLATED
                z.write(p,name,compress_type=compression)
        self.reader.inspect(archive)
        archive.with_suffix(archive.suffix+".sha256").write_text(digest(archive)+"  "+archive.name+"\n",encoding="ascii",newline="\n")

def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--sources",type=Path,required=True)
    args=parser.parse_args()
    stage=PackageBuilder().build(args.output,json.loads(args.sources.read_text("utf8")))
    archive=stage.with_suffix(".zip")
    ArchiveWriter().write(stage,archive)
    print(json.dumps({"status":"archive_verified","archive":str(archive),"sha256":digest(archive),"size_bytes":archive.stat().st_size}))

if __name__=="__main__":
    main()
