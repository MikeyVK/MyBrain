<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Toolkit-only quality bootstrap

**Status:** Research tooling  
**Version:** 0.1  
**Last Updated:** 2026-10-31

## Purpose

Reproduce the isolated native verification boundary without changing the MyBrain application policy.

## Summary

Maintained adapter and YAML fragments live here. The installed adapter/configuration under ignored server data are local deployment artifacts. A healthy server or a passing empty selection is not acceptance.

## Source to deployment

[adapter.py](adapter.py) and [manifest.yaml](manifest.yaml) deploy to `.pgmcp/workspace_adapters/eboekhouden_quality/`. [bootstrap.py](bootstrap.py) generates the local absolute-path `config.json` from this checkout and its fixed `.venv`; that config never belongs in Git. At this snapshot the maintained adapter bytes equal the independently reviewed installed r2 adapter. The maintained manifest is a native-scaffolded YAML mapping; record source and deployment hashes when reconciling serialized artifacts. Absolute local configuration remains ignored.

## Fresh checkout

From the repository root, create `tools/eboekhouden/.venv` with CPython 3.15.0 and no inherited system packages. Install only [the pinned lock](../requirements.lock.txt). Run `tools/eboekhouden/.venv/Scripts/python.exe tools/eboekhouden/quality/bootstrap.py` to inspect the local setup proposal. The POSIX interpreter is `.venv/bin/python`. `--install` copies only the scoped adapter/manifest and generates its local config, preserving changed prior deployed bytes under ignored `.local-work/quality-history`. It does not activate trust or merge policy.

## Reviewed activation

Merge only [checks.override.yaml](checks.override.yaml), [tests.override.yaml](tests.override.yaml) and [adapters.override.yaml](adapters.override.yaml) into the matching local server configuration. Do not replace unrelated checks/trusted IDs. Keep the packaged `python_syntax` choice null and the original application `python_tests` inactive. The existing Python content profile deliberately routes through the path-confined toolkit adapter: unrelated paths remain refused, not newly admitted. Keep the server runtime and PATH unchanged. Use the supported restart/reload and get_work_context for every participating named role connection.

## Actual verification

Use explicit native toolkit targets for syntax and synthetic tests. Confirm selected-file coverage, valid-content admission, invalid-content nonpersistence, outside-path read-only refusal and the isolated interpreter/pin identities. Do not attempt an outside source scaffold. The default/configured empty test selection returns unavailable and is not a toolkit pass. [test_quality_adapter.py](../tests/test_quality_adapter.py) retains twelve portable policy regressions; four historical nested-environment native probes remain private setup evidence rather than invented permanent application tests.

## Format admission

Python uses native scoped AST enforcement, YAML uses native mapping-root checks and Markdown uses native offline local-link validation. The dependency lock, pytest.ini and two ignore rules have no registered content validator: the named setup exception uses report and records not_executed honestly, followed by direct content and ignore/status inspection. No Python, Markdown or YAML check is disabled. The adapter rejects caller-supplied pytest arguments and environment/private source selection; test children refuse socket calls and credential API symbols. This protects trusted offline tests, not hostile arbitrary code.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-31 | Imp | Preserve reviewed scoped adapter and explicit local deployment route. |
