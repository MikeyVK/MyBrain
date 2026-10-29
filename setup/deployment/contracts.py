"""Read-only integrity and containment contracts; standard library only."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tarfile
import zipfile

class DeploymentError(Exception):
    """A structured policy refusal."""
    def __init__(self, code: str, exit_code: int = 3):
        super().__init__(code)
        self.code = code
        self.exit_code = exit_code

def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()

def strict_json(data: str | bytes) -> dict:
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise DeploymentError("duplicate_json_key")
            result[key] = value
        return result
    try:
        value = json.loads(data, object_pairs_hook=pairs)
    except (ValueError, TypeError) as exc:
        raise DeploymentError("invalid_json") from exc
    if not isinstance(value, dict):
        raise DeploymentError("mapping_required")
    return value

def relative_name(name: str) -> str:
    if not isinstance(name, str) or not name or "\\" in name or name.startswith("/"):
        raise DeploymentError("unsafe_path")
    for part in name.split("/"):
        if part in ("", ".", "..") or part[-1:] in (" ", ".") or re.search(r'[<>:"|?*\x00-\x1f]', part):
            raise DeploymentError("unsafe_path")
        if re.fullmatch(r"(?i)(con|prn|aux|nul|com[0-9]|lpt[0-9])(?:\..*)?", part):
            raise DeploymentError("reserved_path")
    if str(PurePosixPath(name)) != name:
        raise DeploymentError("noncanonical_path")
    return name

def no_links(path: Path) -> None:
    for item in (path, *path.parents):
        if item.is_symlink() or item.is_junction():
            raise DeploymentError("reparse_path")

def tree_files(root: Path) -> dict[str, Path]:
    no_links(root)
    result = {}
    folded = set()
    for base, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            no_links(Path(base) / name)
        for name in files:
            p = Path(base) / name
            rel = relative_name(p.relative_to(root).as_posix())
            if rel.casefold() in folded:
                raise DeploymentError("duplicate_path")
            folded.add(rel.casefold())
            result[rel] = p
    return result

def manifest_records(manifest: dict) -> dict:
    admitted = {"$comment", "schema_version", "package_id", "created_utc", "builder_revision",
                "target", "network_mode", "files", "sources", "dependencies", "exclusions", "limits"}
    if set(manifest) - admitted or manifest.get("schema_version") != 1:
        raise DeploymentError("manifest_schema")
    if not isinstance(manifest.get("package_id"), str) or not manifest["package_id"]:
        raise DeploymentError("package_identity")
    entries = manifest.get("files")
    if not isinstance(entries, list) or not entries:
        raise DeploymentError("empty_inventory")
    records = {}
    folded = set()
    for item in entries:
        if not isinstance(item, dict) or not {"path","size_bytes","sha256"} <= set(item) or set(item) - {"path","size_bytes","sha256","category","source_id"}:
            raise DeploymentError("file_schema")
        name = relative_name(item["path"])
        if name in ("manifest.json", "manifest.sha256") or name.casefold() in folded:
            raise DeploymentError("duplicate_path")
        if type(item.get("size_bytes")) is not int or item["size_bytes"] < 0:
            raise DeploymentError("file_size")
        if not re.fullmatch("[a-f0-9]{64}", str(item.get("sha256", ""))):
            raise DeploymentError("file_digest")
        folded.add(name.casefold())
        records[name] = item
    if sum(e["size_bytes"] for e in records.values()) > 2_000_000_000 or len(records) > 20000:
        raise DeploymentError("package_bounds")
    for source in manifest.get("sources", []):
        if not isinstance(source,dict) or not {"id","tree_path","files"} <= set(source) or set(source)-{"id","role","ref","commit_sha","capture_utc","tree_path","original_ancestry_included","files","base_source_id","base_commit_sha","operation","operations"}:
            raise DeploymentError("source_schema")
        relative_name(source["id"]);relative_name(source["tree_path"])
        if not isinstance(source.get("files"),list):
            raise DeploymentError("source_schema")
        for item in source["files"]:
            if set(item)!={"path","sha256"} or not re.fullmatch("[a-f0-9]{64}",str(item["sha256"])):
                raise DeploymentError("source_file_schema")
            relative_name(item["path"])
        for operation in source.get("operations",[]):
            if set(operation)!={"operation","path"} or operation["operation"] not in ("add","replace","delete"):
                raise DeploymentError("overlay_schema")
            relative_name(operation["path"])
    for dep in manifest.get("dependencies",[]):
        if not isinstance(dep,dict) or set(dep)-{"name","version","filename","size_bytes","sha256","platform","provenance_url","origin","license","license_paths","redistribution","delivery","reason","source_filename","source_sha256","source_url"}:
            raise DeploymentError("dependency_schema")
        if dep.get("delivery") not in ("bundled","download") or not re.fullmatch("[a-f0-9]{64}",str(dep.get("sha256",""))):
            raise DeploymentError("dependency_schema")
        relative_name(dep["filename"])
        if dep["delivery"]=="bundled":
            if dep["filename"] not in records or records[dep["filename"]]["sha256"]!=dep["sha256"]:
                raise DeploymentError("dependency_inventory")
            if not dep.get("license_paths"):
                raise DeploymentError("dependency_license")
        for path in dep.get("license_paths",[]):
            if relative_name(path) not in records:
                raise DeploymentError("missing_license")
        if dep.get("source_filename"):
            if dep["source_filename"] not in records or records[dep["source_filename"]]["sha256"]!=dep["source_sha256"]:
                raise DeploymentError("dependency_source_digest")
    return records


def inspect_source_tar(path: Path) -> tuple[int,int]:
    names=set();total=0;count=0
    with tarfile.open(path,"r:gz") as archive:
        for member in archive:
            name=relative_name(member.name.rstrip("/"))
            if name.casefold() in names or not (member.isfile() or member.isdir()):
                raise DeploymentError("source_archive_path_or_link")
            names.add(name.casefold());count+=1;total+=member.size
            if count>20000 or total>2_000_000_000 or member.size>600_000_000:
                raise DeploymentError("source_archive_bounds")
    return count,total

class PackageVerifier:
    """Validate a complete declared byte inventory without mutation."""
    def __init__(self, archive_reader=None):
        self.archive_reader=archive_reader or ArchiveReader()

    def verify(self, root: Path) -> dict:
        no_links(root)
        if not (root/"manifest.json").is_file() or not (root/"manifest.sha256").is_file():
            raise DeploymentError("missing_manifest")
        body = (root / "manifest.json").read_bytes()
        if hashlib.sha256(body).hexdigest() != (root / "manifest.sha256").read_text("ascii").strip():
            raise DeploymentError("manifest_digest")
        manifest = strict_json(body)
        records = manifest_records(manifest)
        files = tree_files(root)
        if set(files) != set(records) | {"manifest.json", "manifest.sha256"}:
            raise DeploymentError("inventory_mismatch")
        for name, entry in records.items():
            p = files[name]
            if p.stat().st_size != entry["size_bytes"] or digest(p) != entry["sha256"]:
                raise DeploymentError("payload_digest")
        # Independently declared original-source maps prevent substituting generated outputs.
        for source in manifest.get("sources", []):
            for item in source["files"]:
                rel = relative_name(source["tree_path"] + "/" + item["path"])
                if rel not in records or records[rel]["sha256"] != item["sha256"]:
                    raise DeploymentError("source_reconstruction")
        for dep in manifest.get("dependencies",[]):
            if dep["delivery"]=="bundled" and dep["filename"].lower().endswith((".zip",".whl")):
                self.archive_reader.inspect(root/dep["filename"],False)
            if dep.get("source_filename","").endswith(".tar.gz"):
                inspect_source_tar(root/dep["source_filename"])
        return manifest

class ArchiveReader:
    """Inspect all members before creating extraction outputs."""
    def __init__(self, verifier_factory=None):
        self.verifier_factory=verifier_factory or (lambda reader: PackageVerifier(reader))

    def inspect(self, archive: Path, packaged: bool = True) -> list:
        with zipfile.ZipFile(archive) as z:
            entries = z.infolist()
            names = set()
            files = {}
            total = 0
            for info in entries:
                name = relative_name(info.filename.rstrip("/"))
                folded = name.casefold()
                if folded in names:
                    raise DeploymentError("duplicate_archive_path")
                names.add(folded)
                mode = info.external_attr >> 16
                if stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR):
                    raise DeploymentError("archive_link")
                if info.flag_bits & 1:
                    raise DeploymentError("encrypted_archive")
                total += info.file_size
                if total > 2_000_000_000 or len(entries) > 20000 or info.file_size > 600_000_000:
                    raise DeploymentError("archive_bounds")
                if not info.is_dir():
                    files[name] = info
            if packaged:
                if not {"manifest.json","manifest.sha256"} <= set(files):
                    raise DeploymentError("missing_manifest")
                body = z.read("manifest.json")
                if hashlib.sha256(body).hexdigest() != z.read("manifest.sha256").decode("ascii").strip():
                    raise DeploymentError("manifest_digest")
                records = manifest_records(strict_json(body))
                if set(files) != set(records) | {"manifest.json", "manifest.sha256"}:
                    raise DeploymentError("inventory_mismatch")
                for name, entry in records.items():
                    with z.open(files[name]) as stream:
                        h = hashlib.file_digest(stream, "sha256").hexdigest()
                    if h != entry["sha256"] or files[name].file_size != entry["size_bytes"]:
                        raise DeploymentError("payload_digest")
            return entries

    def extract(self, archive: Path, target: Path, packaged: bool = True) -> None:
        entries = self.inspect(archive, packaged)
        no_links(target)
        if target.exists() and any(target.iterdir()):
            raise DeploymentError("existing_extract_target", 4)
        target.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive) as z:
            for info in entries:
                out = target / relative_name(info.filename.rstrip("/"))
                no_links(out)
                if info.is_dir():
                    out.mkdir(parents=True, exist_ok=True)
                else:
                    out.parent.mkdir(parents=True, exist_ok=True)
                    with z.open(info) as src, out.open("xb") as dst:
                        import shutil
                        shutil.copyfileobj(src, dst)
        if packaged:
            self.verifier_factory(self).verify(target)

class TargetOwnership:
    """Validate one package-owned destination and preserve foreign content."""
    def inspect(self, target: Path, package: Path, manifest: dict) -> dict:
        target = target.absolute()
        no_links(target)
        if target == Path(target.anchor) or target == package or target in package.parents or package in target.parents:
            raise DeploymentError("unsafe_destination", 4)
        owner = target / ".deployment/owner.json"
        if target.exists() and any(target.iterdir()):
            if not owner.is_file():
                raise DeploymentError("foreign_destination", 4)
            value = strict_json(owner.read_bytes())
            if value != {"package_id": manifest["package_id"], "manifest_sha256": digest(package/"manifest.json"), "target": str(target)}:
                raise DeploymentError("destination_identity", 4)
            return value
        return {"package_id": manifest["package_id"], "manifest_sha256": digest(package/"manifest.json"), "target": str(target)}
