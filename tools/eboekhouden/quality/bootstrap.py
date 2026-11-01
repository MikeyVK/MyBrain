"""Install the reviewed scoped quality sources locally; never merge policy implicitly."""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import sys

PINS = {"pytest": "9.1.1", "pytest-cov": "7.1.0", "pytest-xdist": "3.8.0",
        "coverage": "7.16.2", "pytest-asyncio": "1.4.0"}

def checked(path):
    path = Path(path).absolute()
    for part in (path, *path.parents):
        if part.exists() or part.is_symlink():
            if part.is_symlink() or getattr(part.lstat(), "st_file_attributes", 0) & 0x400:
                raise ValueError("BOOTSTRAP_REPARSE_REFUSED")
    return path.resolve()

def install(apply=False):
    source = checked(Path(__file__).parent)
    toolkit = source.parent
    if toolkit.name != "eboekhouden" or toolkit.parent.name != "tools":
        raise ValueError("EXPECTED_TOOLKIT_SOURCE_LOCATION")
    workspace = toolkit.parent.parent
    python = checked(toolkit / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python"))
    if checked(sys.executable) != python or platform.python_version() != "3.15.0":
        raise ValueError("RUN_WITH_PINNED_ISOLATED_TOOLKIT_PYTHON")
    if "include-system-site-packages = false" not in (toolkit / ".venv" / "pyvenv.cfg").read_text().lower():
        raise ValueError("ISOLATED_VENV_REQUIRED")
    actual = {name: importlib.metadata.version(name) for name in PINS}
    if actual != PINS:
        raise ValueError("NATIVE_TEST_PINS_MISMATCH")
    destination = checked(workspace / ".pgmcp" / "workspace_adapters" / "eboekhouden_quality")
    config = {"workspace": str(workspace), "interpreter": str(python),
              "python_version": "3.15.0", "pins": PINS}
    if not apply:
        return {"state": "QUALITY_SETUP_DRYRUN", "destination": str(destination),
                "configuration": config, "policyMerged": False}
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("adapter.py", "manifest.yaml"):
        target = checked(destination / name)
        body = (source / name).read_bytes()
        if target.exists() and target.read_bytes() != body:
            old = target.read_bytes()
            history = checked(toolkit / ".local-work" / "quality-history")
            history.mkdir(parents=True, exist_ok=True)
            backup = history / (hashlib.sha256(old).hexdigest() + "-" + name)
            if not backup.exists():
                backup.write_bytes(old)
        target.write_bytes(body)
    target = checked(destination / "config.json")
    if target.exists():
        old = target.read_bytes()
        history = checked(toolkit / ".local-work" / "quality-history")
        history.mkdir(parents=True, exist_ok=True)
        backup = history / (hashlib.sha256(old).hexdigest() + "-config.json")
        if not backup.exists():
            backup.write_bytes(old)
    target.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return {"state": "LOCAL_QUALITY_ADAPTER_INSTALLED", "destination": str(destination),
            "policyMerged": False,
            "next": "Review scoped YAML merges, reload each named consumer, then run actual native probes."}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()
    print(json.dumps(install(args.install), indent=2))
