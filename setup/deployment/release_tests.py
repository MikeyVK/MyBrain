"""Exercise the actual extracted package via Windows public commands and controlled interruption."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import zipfile
if __name__=="__main__":
    sys.path.insert(0,str(Path(__file__).parent))
from contracts import ArchiveReader, DeploymentError, PackageVerifier, digest, no_links
from journal import atomic_json

class ReleaseJourney:
    """Keep the actual archive, command outcomes and preservation evidence together."""
    def __init__(self,package: Path,target: Path,archive: Path):
        self.package=package;self.target=target;self.archive=archive;self.outcomes=[]
        self.shell=str(Path(os.environ["SystemRoot"])/"System32/WindowsPowerShell/v1.0/powershell.exe")

    def command(self,name: str,target: Path,expected: int,extra: list | None=None) -> dict:
        arguments=[self.shell,"-NoProfile","-File",str(self.package/name),"-Destination",str(target),*(extra or [])]
        result=subprocess.run(arguments,capture_output=True,text=True,encoding="utf8",errors="replace",timeout=600)
        try:
            value=json.loads(result.stdout)
        except ValueError:
            raise RuntimeError(json.dumps({"script":name,"exit":result.returncode,"stdout":result.stdout,"stderr":result.stderr}))
        if result.returncode!=expected:
            raise RuntimeError(json.dumps({"script":name,"expected":expected,"exit":result.returncode,"output":value}))
        if expected==2 and value.get("code")!="local_tooling_verified_host_activation_pending":
            raise RuntimeError(json.dumps(value))
        self.outcomes.append({"script":name,"exit":result.returncode,"code":value.get("code")})
        return value

    def stop_owned_tree(self, process: subprocess.Popen, step: str) -> None:
        """Keep strict taskkill success criteria and preserve native failure diagnostics."""
        arguments=[str(Path(os.environ["SystemRoot"])/"System32/taskkill.exe"),"/PID",str(process.pid),"/T","/F"]
        killed=subprocess.run(arguments,capture_output=True,text=True,encoding="utf8",errors="replace")
        if killed.returncode:
            raise RuntimeError(json.dumps({"step":step,"operation":"taskkill own launched tree",
                "pid":process.pid,"returncode":killed.returncode,"stdout":killed.stdout,"stderr":killed.stderr}))

    def execute(self) -> dict:
        manifest=PackageVerifier().verify(self.package)
        ArchiveReader().inspect(self.archive)
        sentinel=self.target.parent/"unrelated-sentinel.txt";sentinel.write_bytes(b"untouched synthetic\n")
        first=self.command("Verify.ps1",self.target,2)
        self.command("Bootstrap.ps1",self.target,2)
        self.command("Recover.ps1",self.target,2,["-Action","Resume"])
        # A user edit must be preserved. Restore only the exact synthetic edit made by this test.
        edited=self.target/"workspace/README.md";original=edited.read_bytes()
        edited.write_bytes(original+b"\nSynthetic customization for rejection test.\n")
        try:
            self.command("Bootstrap.ps1",self.target,4)
        finally:
            if edited.read_bytes()!=original+b"\nSynthetic customization for rejection test.\n":
                raise DeploymentError("customization_not_preserved")
            edited.write_bytes(original)
        foreign=self.target.parent/"foreign";foreign.mkdir()
        (foreign/"sentinel").write_bytes(b"foreign")
        self.command("Bootstrap.ps1",foreign,4)
        if (foreign/"sentinel").read_bytes()!=b"foreign":
            raise DeploymentError("foreign_destination_modified")
        # Terminate only the process tree started here, once its own environment stage is actually running.
        interrupted=self.target.parent/"interrupted installation"
        log=self.target.parent/"interruption.log"
        arguments=[self.shell,"-NoProfile","-File",str(self.package/"Bootstrap.ps1"),"-Destination",str(interrupted)]
        with log.open("w",encoding="utf8") as stream:
            process=subprocess.Popen(arguments,stdout=stream,stderr=stream,creationflags=subprocess.CREATE_NO_WINDOW)
            stop_reason=None
            deadline=time.monotonic()+240
            journal=interrupted/".deployment/journal.json"
            while time.monotonic()<deadline and process.poll() is None:
                if journal.exists():
                    try:state=json.loads(journal.read_bytes())
                    except (ValueError,OSError):state={}
                    if state.get("stages",{}).get("environment")=="running" and (interrupted/"workspace/.venv/Scripts/python.exe").is_file():
                        stop_reason="environment_running"
                        self.stop_owned_tree(process,"environment_running_interruption")
                        break
                time.sleep(.2)
            if stop_reason is None:
                if process.poll() is None:
                    self.stop_owned_tree(process,"interruption_deadline_cleanup")
                raise RuntimeError("Controlled interruption did not reach expected environment stage: "+log.read_text("utf8"))
            process.wait(timeout=30)
        # The killed stage's exact bytes remain recoverable even after successful reconstruction.
        partial_files={p.relative_to(interrupted/"workspace/.venv").as_posix():digest(p)
                       for p in (interrupted/"workspace/.venv").rglob("*") if p.is_file()}
        if not partial_files:
            raise DeploymentError("no_interrupted_environment_bytes")
        resumed=self.command("Recover.ps1",interrupted,2,["-Action","Resume"])
        # Discard only a verified subset of this package's staging; changed bytes stay intact.
        runtime=next(d for d in manifest["dependencies"] if d["name"]=="CPython")
        stage=self.target/".deployment/python-stage"
        with zipfile.ZipFile(self.package/runtime["filename"]) as z:
            stage.mkdir()
            staged_name=next(n for n in z.namelist() if n=="python.exe")
            (stage/staged_name).write_bytes(z.read(staged_name))
        self.command("Recover.ps1",self.target,0,["-Action","DiscardStaging"])
        if stage.exists():
            raise DeploymentError("verified_staging_not_discarded")
        stage.mkdir();(stage/"python.exe").write_bytes(b"synthetic changed stage")
        self.command("Recover.ps1",self.target,4,["-Action","DiscardStaging"])
        if (stage/"python.exe").read_bytes()!=b"synthetic changed stage":
            raise DeploymentError("changed_staging_not_preserved")
        (stage/"python.exe").unlink();stage.rmdir()
        quarantine=list((interrupted/".deployment/quarantine").glob("environment-*"))
        if len(quarantine)!=1 or any(not (quarantine[0]/name).is_file() or digest(quarantine[0]/name)!=sha for name,sha in partial_files.items()):
            raise DeploymentError("interrupted_bytes_not_preserved")
        if sentinel.read_bytes()!=b"untouched synthetic\n":
            raise DeploymentError("unrelated_sentinel_modified")
        self.command("Verify.ps1",self.target,2)
        result={"status":"local_archive_journey_verified","archive_sha256":digest(self.archive),
                "archive_size_bytes":self.archive.stat().st_size,"manifest_sha256":digest(self.package/"manifest.json"),
                "source_identities":[{k:s.get(k) for k in ("id","ref","commit_sha","capture_utc")} for s in manifest["sources"]],
                "public_commands":self.outcomes,"actual_interruption":stop_reason,
                "partial_environment_files_preserved":len(partial_files),"sentinel":"unchanged",
                "versions":first["versions"],"native_probe":first["native_probe"],
                "host_activation":"not_verified","second_pc_vm":"not_tested","network_mode":manifest["network_mode"],
                "remaining_host_actions":["Codex installation/sign-in if absent","trust project under target host policy","load named registration and verify each intended role connection"]}
        report=self.archive.with_suffix(self.archive.suffix+".verification.json")
        if report.exists():
            raise DeploymentError("existing_release_verification_report",4)
        atomic_json(report,result)
        return result

if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--archive",type=Path,required=True);parser.add_argument("--package",type=Path,required=True);parser.add_argument("--destination",type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(ReleaseJourney(args.package,args.destination,args.archive).execute()))
