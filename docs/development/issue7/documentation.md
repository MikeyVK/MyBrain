<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Portable workspace documentation and delivery

**Status:** DOCUMENTATION — independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-28

## Purpose

Complete issue 7 Planning Documentation D_1 and D_2 by reconciling the validated instructions and recording the frozen delivery handoff, without changing packaged bytes.

## Scope In

Current operator/target navigation, startup/recovery commands, artifact/source identities, source-consumer documentation parity, concise local-agent prompt and truthful coverage/limits.

## Scope Out

Rebuilding or editing R6, new deployment/native/recovery runs, product/database implementation, private data/accounts, source/donor changes, global host configuration and remote publication.

## Prerequisites

- Original independent MIGRATION-I7-VALIDATION-QA-1 GO for validation→documentation was directly read for exact 71bd55db3e8d4c0148338fb040c5c626aa786612 and unchanged R6 outer digest below.
- Native transition, supported own restart, required three-second wait and actual context readback confirmed issue 7 Documentation. The audit contains only the authorized validation→documentation addition; no force/drift repair.
- get_project_plan(issue_number=7) read back Validation complete, Documentation active, and its D_1/D_2. The Validation report is the claims boundary.

## Summary

The maintained operator/target instructions already match validated R6 behavior and remain unchanged. This phase adds only this delivery document plus its native phase audit. Documentation review is requested; no Ready transition or publication is authorized.

## Reviewed surfaces and deliverables

| Surface | Disposition and reason |
| --- | --- |
| [Repository navigation](../../../README.md) | Existing portable-deployment entry links to the maintained README; byte-identical to the packaged source. |
| [Deployment README](../../../setup/deployment/README.md) | Build/verify, manifest, scope, source/ancestry, privacy and bounded Git availability remain aligned with Validation; no edit. |
| [START-HERE](../../../setup/deployment/START-HERE.md) | Supported target, literal commands, prerequisites, coverage, host activation and recovery remain accurate; no edit. |
| [Short agent handover](../../../setup/deployment/agent-handover.md) | Existing ZIP task includes prerequisite exit semantics and missing product/database coverage; no edit. |
| [Portable PGMCP map](../../../setup/pgmcp/README.md), [quality sources](../../../setup/quality/README.md), [agent entrypoint](../../../AGENTS.md) and portable skills | No authority/policy/role/template change; no consumer synchronization required. Existing validated generated-consumer evidence remains applicable. |
| [Validation report](validation.md), [implementation evidence](implementation-evidence.md), [Planning](planning.md) | Context and evidence only; left unchanged. This document supplies Documentation D_1 reconciliation and D_2 delivery. |

No production behavior, authoritative protocol/template source or deployed consumer is changed. No additional external handover file is needed because the ZIP already contains agent-handover.md.

## Frozen delivery identity

| Item | Value |
| --- | --- |
| ZIP | `build/deployment/mybrain-windows-x64-20261028-r6.zip` |
| Size | 80,158,029 bytes |
| Outer SHA-256 | 96529ff8f3ed018d3d6d4b903eca3cbcf465525a8a9cd67f8ba989ac13f65e01 |
| Detached outer digest | Same ZIP path plus `.sha256` |
| Manifest | `build/deployment/mybrain-windows-x64-20261028-r6/manifest.json` |
| Manifest SHA-256 | a947202f79d5eff65cd5c7af554c0a0c4e1228ff0b90a5d44df7b72a782198f5 |
| Detached manifest digest | Staged/package `manifest.sha256` |
| External scoped report | Same ZIP path plus `.verification.json` |
| Included target files | Package-root `START-HERE.md` and `agent-handover.md` |
| Build-input revision | ecdb66717c7887427f7a5ca4819ff2dd3b7fae95 |
| Source capture UTC | 2026-10-28T14:08:46.866656Z |

Actual machine delivery paths belong in the chat handoff, not public repository documentation. This new phase document postdates the cutoff and is outside R6. Checksums detect change; use the outer digest from the trusted handoff before executing contents.

## Validated coverage and continuation

Bootstrap restores standalone development Git/workspace and source snapshots, CPython 3.15 x64, PGMCP 4.0.0, native quality tooling and role/named-binding configuration. It recreates environments instead of copying a venv. Target login/trust/host activation is separate.

Original main is 84d5e0cbbe488fd45160de64d5faab9a97ba7687; active-storage 655e9563ba5536d24d9db3c98ef5819ae40feff4 retains issue 6 research/design/storage-model/operations/preservation/acceptance documents. Its PostgreSQL 18 contracts are future implementation inputs; no app/src/API/UI/migrations are present there. The only selected local original is setup/local/find-postgresql-download.py, a vendor-URL finder, not a downloader/installer/provisioner. No PostgreSQL server, MyBrain schema/empty product storage or running application/API/UI is built or tested.

The local agent can restore development setup and continue separately authorized product development from these retained inputs. Original refs/SHAs differ from the new local import commit; snapshots and historical workflow/QA do not confer current issue authority. Keep standalone main without origin, or use a separately authorized authoritative checkout and reviewed source-only deltas; no automatic unrelated-history merge, origin overwrite or force-push. Existing private operational data, credentials/account caches, private IDs/manifests and original private research PDFs are excluded.

## Start, prerequisites and recovery

Use Windows 10 or newer x64 and x64 Windows PowerShell 5.1 or newer, at least 1 GB free and a writable new destination no longer than 100 characters. Spaces are supported. Extract the verified package elsewhere; the example below is a generic destination, not a source-host path.

From the package directory:

```powershell
powershell.exe -NoProfile -File .\Preflight.ps1 -Destination 'C:\Work\MyBrain'
powershell.exe -NoProfile -File .\Bootstrap.ps1 -Destination 'C:\Work\MyBrain'
powershell.exe -NoProfile -File .\Verify.ps1 -Destination 'C:\Work\MyBrain'
```

Require Preflight exit 0 before setup. Its exit 2 means a missing/unproved prerequisite; it is read-only and performs no artifact download or destination creation. Bootstrap/Verify exit 2 is expected only with local_tooling_verified_host_activation_pending. Integrity/conflict/failure outcomes require inspection and preservation.

Python/harness/wheels/native tools are bundled. Only inadequate/missing Git needs the declared primary-download MinGit 2.56.0.4 fallback, verified against its pinned SHA-256. Correct host Git, owned local Git or verified cache avoids unneeded network. This remains hybrid, not proven fully offline.

Installed source is destination/workspace; separate originals are under source-snapshots. Read installed AGENTS.md and the effective PGMCP bootstrap/general/collaboration/selected-role protocols. Obtain target Codex installation/login, project trust and actual named-connection activation through supported host actions; verify each intended target-local binding rather than using a source fixed-root connection.

After interruption, run `Recover.ps1 -Destination <same path> -Action Resume`. Rerun Bootstrap only for the same matching package/destination. Changed/foreign work is preserved and refused. DiscardStaging removes only verified unchanged owned staging; unknown/changed bytes remain preserved. Stop on checksum/privacy/path/binding conflicts, missing prerequisites or unresolved host action; never weaken host policy or import accounts.

## Short standalone target-agent prompt

> Verify mybrain-windows-x64-20261028-r6.zip against SHA-256 96529ff8f3ed018d3d6d4b903eca3cbcf465525a8a9cd67f8ba989ac13f65e01. Read START-HERE.md and agent-handover.md. Use one new Windows x64 destination for Preflight.ps1, then Bootstrap.ps1 and Verify.ps1. Require Preflight exit 0; setup exit 2 is expected only with local_tooling_verified_host_activation_pending. Restore development tooling only: PostgreSQL/schema/storage/app are not supplied. Read installed AGENTS/PGMCP protocols, preserve conflicts/provenance, complete authorized host login/trust/named-binding actions and report actual results. No private data/accounts, invented issue/QA authority or origin overwrite. Continue product work only under fresh authority.

## Documentation evidence and remaining limits

Read-only comparison of current source against actual R6 ZIP entries found all four reviewed README/target documents byte-identical, including package-root START-HERE and agent-handover. All 26 packaged portable PGMCP/quality/skill-source files also matched current source bytes. Invocation/scope: workspace Python -B with zipfile.ZipFile, direct byte comparison and hashlib.sha256 for those four source/ZIP document pairs and all 26 manifest entries under payload/workspace/setup/pgmcp, setup/quality and .agents/skills. Outer and manifest hashes still equal the frozen values above. No included-byte edit or rebuild was necessary.

scaffold_artifact(artifact_type='generic_doc', file_name='documentation.md', target_path='docs/development/issue7', validation='enforce') created this document and executed its native Markdown gate: Lychee 0.24.2, exit 0, 16/16 successful local links, zero errors, configured --offline --cache=false --include-fragments. Final guarded edits repeat only that file-scoped gate. Existing source-document/manifest/parser checks, Validation's single repository_review branch request and neutral no_active_tests outcome remain fresh; none is repeated. No YAML/schema/code family changes occur. See Validation for exact native versions/invocations and Implementation evidence for source checks and behavioral results.

R6 fresh archive/Preflight evidence and original R5 full bootstrap/recovery/native evidence retain separate revisions/digests. The exact unchanged-core comparison justified proportional reuse; no full R6 recovery claim or old verdict inheritance is made. This Documentation artifact requests its own independent phase review.

Actual Codex host activation, second-PC/VM and fully offline proof remain open. PostgreSQL and product implementation/setup remain future work. These are explicit delivery limits for Co/Ready triage, not hidden capabilities. No new substantive documentation gap was found; Ready scheduling, publication or issue closure remains outside this assignment.

## Related Documents

- [Validation claims boundary](<validation.md>)
- [Implementation evidence](<implementation-evidence.md>)
- [Planning D\_1/D\_2](<planning.md>)
- [Maintainer instructions](<../../../setup/deployment/README.md>)
- [Target instructions](<../../../setup/deployment/START-HERE.md>)
- [Packaged task source](<../../../setup/deployment/agent-handover.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-28 | @imp documenter | Reconcile unchanged packaged instructions and portable source parity; record frozen delivery, precise scope, startup/recovery and short target-agent prompt. |
