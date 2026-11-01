"""Fixed private runtime boundary; importing this module performs no I/O."""
from __future__ import annotations
import json
from pathlib import Path
import http.client

# Retained once so test-injected connection factories never become host access.
_NATIVE_HTTPS = http.client.HTTPSConnection

SOURCE_ROOT = Path(__file__).absolute().parent
WORKROOT = SOURCE_ROOT / ".local-work"

def runtime_area(name: str) -> Path:
    if name not in {"core", "rest", "app", "prebooking", "uploads", "edits", "ledger", "links", "metadata", "hours"}:
        raise ValueError("UNKNOWN_RUNTIME_AREA")
    return WORKROOT / name

def private_path(path: Path) -> Path:
    """Reject traversal and every existing symlink/reparse ancestor before I/O."""
    path = Path(path)
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("UNSAFE_PRIVATE_PATH")
    for item in (path, *path.parents):
        if item.exists() or item.is_symlink():
            if item.is_symlink() or getattr(item.lstat(), "st_file_attributes", 0) & 0x400:
                raise ValueError("PRIVATE_REPARSE_PATH_REFUSED")
    resolved = path.resolve()
    if not resolved.is_relative_to(WORKROOT.resolve()):
        raise ValueError("PRIVATE_PATH_OUTSIDE_FIXED_WORKROOT")
    return resolved

def ensure_private_directory(path: Path) -> Path:
    path = private_path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def require_live_config() -> dict:
    """A fresh checkout cannot touch host credentials on a historical mandate."""
    path = private_path(WORKROOT / "host-config.json")
    if not path.is_file():
        raise ValueError("LOCAL_HOST_CONFIGURATION_REQUIRED")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("allowLiveOperations") is not True:
        raise ValueError("LIVE_OPERATIONS_NOT_ENABLED")
    return value

def live_connection(factory, *args, **kwargs):
    """Guard the actual host transport; injected fake factories remain offline."""
    if factory is _NATIVE_HTTPS:
        require_live_config()
    return factory(*args, **kwargs)
