"""Probe the generated registration directly; this is not Codex host activation."""
from __future__ import annotations
import asyncio
import json
import os
from pathlib import Path
import sys
import tomllib
if __name__ == "__main__":
    sys.path.insert(0,str(Path(__file__).parent))
from contracts import DeploymentError, digest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def verify(workspace: Path) -> dict:
    configuration=tomllib.loads((workspace/".codex/config.toml").read_text("utf8"))
    binding,entry=next(iter(configuration["mcp_servers"].items()))
    environment=dict(os.environ)
    for key in list(environment):
        if key.startswith("PGMCP_") or key=="GITHUB_TOKEN":
            del environment[key]
    environment.update(entry["env"])
    environment["PYTHONDONTWRITEBYTECODE"]="1"
    hostile=workspace.parent/".deployment/hostile-context"
    hostile.mkdir(exist_ok=True)
    # Only inert context bytes; no startup module or code-execution marker probe.
    fixture=hostile/"context.txt"
    inert=b"inert inherited context fixture\n"
    if fixture.exists() and fixture.read_bytes()!=inert:
        raise DeploymentError("hostile_fixture_conflict",4)
    if not fixture.exists():
        fixture.write_bytes(inert)
    environment.update({"PYTHONPATH":str(hostile),"GIT_DIR":str(hostile/"not-a-repository"),
                        "GIT_WORK_TREE":str(hostile),"GIT_INDEX_FILE":str(hostile/"wrong-index"),
                        "PIP_TARGET":str(hostile/"wrong-install"),"PIP_PREFIX":str(hostile/"wrong-prefix"),
                        "PIP_ROOT":str(hostile/"wrong-root"),"PIP_USER":"1"})
    directory=workspace/".pgmcp/temp/deployment-probe"
    directory.mkdir(parents=True,exist_ok=True)
    fixtures={"positive.md":b"# Synthetic\n\n[local](positive.md#synthetic)\n",
              "negative.md":b"# Synthetic\n\n[missing](not-present.md)\n",
              "positive.yaml":b"synthetic: true\n","negative.yaml":b"- sequence\n",
              "positive.schema.json":b'{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object"}\n',
              "negative.schema.json":b'{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"invalid"}\n'}
    for name,data in fixtures.items():
        p=directory/name
        if p.exists() and p.read_bytes()!=data:
            raise DeploymentError("probe_fixture_conflict",4)
        if not p.exists():
            p.write_bytes(data)
    sibling=workspace.parent/".deployment/sibling-only.md"
    if not sibling.exists():
        sibling.write_bytes(b"# Outside the selected workspace\n")
    parameters=StdioServerParameters(command=entry["command"],args=entry["args"],cwd=entry["cwd"],env=environment)
    results={}
    async with stdio_client(parameters) as (reader,writer):
        async with ClientSession(reader,writer,read_timeout_seconds=120) as session:
            await session.initialize()
            available={x.name for x in (await session.list_tools()).tools}
            for name in ("health_check","git_status","get_work_context","run_checks"):
                if name not in available:
                    raise DeploymentError("missing_native_capability:"+name)
            async def call(name,arguments):
                response=await session.call_tool(name,arguments)
                structured=response.structured_content
                if structured is None:
                    raise DeploymentError("missing_structured_response")
                operation=structured.get("data",{}).get("operation")
                if not isinstance(operation,dict):
                    raise RuntimeError(json.dumps(structured))
                return operation
            health=await call("health_check",{})
            if health.get("status")!="healthy" or health.get("version")!="4.0.0":
                raise RuntimeError(json.dumps(health))
            context=await call("get_work_context",{})
            if context.get("issue_number") is not None:
                raise DeploymentError("invented_active_issue")
            status=await call("git_status",{})
            if status.get("branch")!="main":
                raise DeploymentError("target_git_branch")
            for filename,check,expected in (
                ("positive.md","markdown_links","passed"),("negative.md","markdown_links","failed"),
                ("positive.yaml","yaml_configuration","passed"),("negative.yaml","yaml_configuration","failed"),
                ("positive.schema.json","json_schema_shape","passed"),("positive.schema.json","json_schema_metaschema","passed"),
                ("negative.schema.json","json_schema_metaschema","failed")):
                operation=await call("run_checks",{"scope":"targets","targets":[".pgmcp/temp/deployment-probe/"+filename],"checks":[check]})
                values=operation.get("results",[])
                if not values or values[0].get("status")!=expected:
                    raise RuntimeError(json.dumps(operation))
                invocation=values[0].get("invocation") or {}
                capture=values[0].get("capture") or invocation.get("capture")
                # A requested native negative must execute, not merely refuse configuration.
                if not capture or capture.get("exit_code")!=(0 if expected=="passed" else 1):
                    raise RuntimeError(json.dumps(operation))
                results[filename+":"+check]={"status":expected,"native_exit":capture["exit_code"]}
            sibling_result=await call("run_checks",{"scope":"targets","targets":["sibling-only.md"],"checks":["markdown_links"]})
            if sibling_result.get("run_status")=="passed":
                raise DeploymentError("sibling_root_not_isolated")
    if (hostile/"wrong-index").exists() or (hostile/"wrong-install").exists():
        raise DeploymentError("inherited_host_context_not_isolated")
    if (workspace/".pgmcp/state.json").exists():
        raise DeploymentError("probe_created_issue_state")
    return {"binding":binding,"route":"generated STDIO registration; host activation not tested",
            "health_pid":health["pid"],"root":str(workspace),"branch":status["branch"],
            "native_results":results,"sibling_only":"absent_or_refused","active_issue":None,"poisoned_inherited_context":"guard_exercised_with_inert_fixture"}

if __name__=="__main__":
    print(json.dumps(asyncio.run(asyncio.wait_for(verify(Path(sys.argv[1])),180))))
