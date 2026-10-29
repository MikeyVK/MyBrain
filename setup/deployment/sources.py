"""Exact selected source restoration and pure target consumer rendering."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
from contracts import DeploymentError, relative_name
from journal import Journal

class SourceRestorer:
    """Restore each admitted source tree without old active issue state."""
    def restore(self, package: Path, journal: Journal, manifest: dict) -> None:
        for source in manifest["sources"]:
            prefix = "workspace" if source["role"] == "deployment" else "source-snapshots/" + relative_name(source["id"])
            for item in source["files"]:
                name = relative_name(item["path"])
                if source["role"] == "deployment" and name.startswith((".git/", ".pgmcp/", ".codex/", ".venv/")):
                    raise DeploymentError("active_local_state_in_source")
                data = (package/source["tree_path"]/name).read_bytes()
                if "sha256" in item and hashlib.sha256(data).hexdigest() != item["sha256"]:
                    raise DeploymentError("source_reconstruction")
                journal.put(prefix + "/" + name, data)
        journal.put("source-snapshots/provenance.json",(json.dumps({"sources":manifest["sources"],"exclusions":manifest.get("exclusions",[])},indent=2)+"\n").encode())
        journal.stage("source", "complete")

HOST_LAUNCH_GUARD = "import os,pathlib,runpy\nfor k in list(os.environ):\n    if k.upper().startswith((\"GIT_\",\"PIP_\",\"PYTHON\",\"_PYTHON\")):\n        del os.environ[k]\nw=pathlib.Path(os.environ[\"PGMCP_WORKSPACE_ROOT\"])\nt=w.parent/\".deployment/temp\"\nc=w.parent/\".deployment/cache\"\nfor p in (t,c):\n    if not p.is_dir() or any(q.is_symlink() or q.is_junction() for q in (p,*p.parents)):\n        raise RuntimeError(\"target_environment_conflict\")\nos.environ.update({\"TEMP\":str(t),\"TMP\":str(t),\"PIP_CONFIG_FILE\":os.devnull,\"PIP_CACHE_DIR\":str(c),\"GIT_CONFIG_NOSYSTEM\":\"1\",\"GIT_CONFIG_GLOBAL\":os.devnull,\"GIT_CONFIG_SYSTEM\":os.devnull,\"PYTHONPATH\":\"\",\"PYTHONHOME\":\"\",\"PYTHONNOUSERSITE\":\"1\",\"PYTHONSAFEPATH\":\"1\",\"PYTHONDONTWRITEBYTECODE\":\"1\"})\nrunpy.run_module(\"mcp_server.core.proxy\",run_name=\"__main__\")\n"

class ConsumerRenderer:
    """Render immutable target-local TOML outputs from reviewed role values."""
    def render(self, workspace: Path, binding: str, roles: dict, path: str) -> tuple:
        if not re.fullmatch("[a-z][a-z0-9-]{2,63}", binding):
            raise DeploymentError("invalid_binding_name", 4)
        literal = lambda value: json.dumps(str(value), ensure_ascii=False)
        environment = {
            "PGMCP_WORKSPACE_ROOT":str(workspace),
            "PGMCP_SERVER_PROJECT_DIR":str(workspace/".pgmcp"),
            "PGMCP_CONFIG_ROOT":str(workspace/".pgmcp/config"),
            "PGMCP_TEMPLATE_ROOT":str(workspace/".pgmcp/template_suite"),
            "PGMCP_SERVER_NAME":binding,
            "PGMCP_RESPONSE_MODE":"structured",
            "PATH":path
        }
        lines = [f"[mcp_servers.{binding}]",
                 f"command = {literal(workspace/'.venv/Scripts/python.exe')}",
                 'args = ["-I", "-B", "-c", '+literal(HOST_LAUNCH_GUARD)+']',
                 f"cwd = {literal(workspace)}",
                 "startup_timeout_sec = 120", "tool_timeout_sec = 3600",
                 'env_vars = ["GITHUB_TOKEN"]', "enabled = true", "",
                 f"[mcp_servers.{binding}.env]"]
        lines += [f"{key} = {literal(value)}" for key,value in environment.items()]
        outputs = []
        for role in roles.values():
            name=role["name"]
            if not re.fullmatch("pgmcp-(co|imp|qa)", name):
                raise DeploymentError("role_identity")
            content="".join(f"{key} = {literal(role[key])}\n" for key in ("name","description","developer_instructions"))
            outputs.append((".codex/agents/"+name+".toml",content.encode()))
            lines += ["", f"[agents.{name}]", f'config_file = "agents/{name}.toml"',
                      f'description = {literal(role["description"])}']
        outputs.append((".codex/config.toml",("\n".join(lines)+"\n").encode()))
        return tuple(outputs)
