<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# MyBrain target-agent handover

**Status:** DEPLOYMENT HANDOVER — target host activation required
**Version:** 1.1
**Last Updated:** 2026-10-28

## Purpose

Restore only the screened workspace, tooling and setup on Windows x64.

## Summary

Compare the ZIP SHA-256 received through the trusted handover before executing any content. Use Windows 10 or newer, x64 PowerShell 5.1 or newer, a writable short destination (at most 100 characters) and at least 1 GB free. Existing private data and account caches are absent. Scripts do not change global host settings. Respect target-host execution/trust policy.

## Delivered coverage and remaining product work

Bootstrap restores a standalone development Git workspace and fixed public-safe source snapshots, recreates CPython 3.15 x64 and PGMCP 4.0.0, and provisions native quality tools, roles and target-local named bindings. Host login/trust/activation remains separate.

The primary/deployment source is development workspace/harness material. The active-storage snapshot at 655e9563ba5536d24d9db3c98ef5819ae40feff4 contains issue 6 research/design and storage-model, operations, preservation and acceptance documents. Its PostgreSQL 18 contracts are future implementation input; this snapshot contains no app/src, API/UI or database migrations. Continue the storage design from its retained `docs/development/issue6/` documents in source-snapshots under a newly authorized issue.

The selected local source `setup/local/find-postgresql-download.py` only finds vendor URLs. It does not download, install or provision PostgreSQL. Bootstrap does not install/prove a PostgreSQL server, MyBrain schema or empty product storage, or a running application/API/UI. Those need future product implementation and separately scoped setup/verification. No private database or other operational data is transferred.

## Start

Extract the trusted ZIP to a package directory. From that directory run:

```powershell
powershell.exe -NoProfile -File .\Preflight.ps1 -Destination 'C:\Work\MyBrain'
powershell.exe -NoProfile -File .\Bootstrap.ps1 -Destination 'C:\Work\MyBrain'
powershell.exe -NoProfile -File .\Verify.ps1 -Destination 'C:\Work\MyBrain'
```

Use the same configurable destination throughout; spaces are supported. The repository is its workspace subdirectory. The package directory and installation must be separate. Local setup/verification returns exit 2 with code local_tooling_verified_host_activation_pending when local checks complete but Codex host activation remains unverified. This is not a complete host-activation claim. Other refusal/failure codes require inspection; do not treat every exit 2 as success.

Preflight is read-only: it reports usable Git or a verified target cache, otherwise performs a bounded HEAD availability check against the exact declared primary Git URL. It downloads no artifact and creates no destination. Missing/unproven availability returns exit 2 with a prerequisite code such as git_download_unverified; stop and resolve that prerequisite before Bootstrap. A completed Preflight confirms its prerequisite scope, not application or host activation.

## Network and host actions

Python, the harness, quality tools and the hash-locked wheel closure are bundled. If usable Git 2.51 or newer is absent, setup downloads only the exact declared MinGit 2.56.0.4 archive from its official primary URL and verifies its SHA-256. Therefore this package is hybrid, with network needed for that fallback. Target Codex installation/sign-in, project trust, allowed script execution and actual connection loading remain host actions. Never transfer credentials or weaken host policy. Open the installed workspace in Codex, inspect its project-local registration and activate each intended role connection using the host's supported route; no universal restart button is assumed.

## Local instructions and source

Read the installed workspace's AGENTS.md, README.md and .pgmcp/docs/setup/agentic-bootstrap.md; choose one role and read the complete effective general/collaboration/role protocol. Source snapshots/provenance are in the destination's source-snapshots directory and the package manifest. Original refs/SHAs differ from the new standalone Git import identity. Source history, origin remotes, old active issue state and old QA validity are not installed. Co must verify target admission and explicit local Git identity/signing settings before initializing a real issue. Never force-push or overwrite origin to reconcile ancestry; use a separately authorized authoritative checkout and reviewed deltas.

## Recovery and stop conditions

Rerun Bootstrap only for the same unmodified package/destination. After interruption, use Recover.ps1 -Destination <same-path> -Action Resume. Incomplete environment/server bytes are preserved in .deployment/quarantine. DiscardStaging removes only verified-owned unchanged staging; changed/unknown bytes are preserved and refused. Conflicts require a new destination or explicit review. Stop on checksum/privacy/path/binding failures, changed existing work, missing prerequisites or required host action. Setup reports remain under .deployment. No second-PC/VM or offline end-to-end claim is made.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.1 | 2026-10-28 | @imp implementer | Clarify delivered development/tooling coverage, remaining PostgreSQL/product work and read-only Git/network prerequisite outcomes. |
| 1.0 | 2026-10-28 | @imp implementer | Provide short configurable target setup commands, declared network/host requirements and preservation/authority stop conditions. |
