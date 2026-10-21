<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# MyBrain quality tooling setup

**Status:** MAINTAINED — owner-approved policy  
**Version:** 1.1  
**Last Updated:** 2026-10-21

## Purpose

Reproduce the owner-approved documentation and configuration checks through the workspace-local PGMCP connection.

## Summary

The [repository quality policy](../../README.md#quality-policy) defines required evidence, timing and deferrals. This directory contains reviewed deployment sources; ignored .pgmcp/config overrides are their local deployed copies.

## Inputs and effective configuration

| Source | Responsibility |
| --- | --- |
| [checks.yaml](checks.yaml) | Four acknowledged native checks, repository_review default profile and branch target policies. |
| [tests.yaml](tests.yaml) | Inactive application tests; no passing-test claim. |
| [fixes.yaml](fixes.yaml) | Unresolved automatic fix bindings; no source fixes authorized. |
| [dependencies.yaml](dependencies.yaml) | Current native pins, official Lychee release and Windows archive hash. |
| [Harness lock](../../requirements-pgmcp.lock.txt) | Existing PGMCP dependency baseline; application tooling is separate. |

PGMCP 4.0.0 composes .pgmcp/config/defaults/<name>.yaml with optional .pgmcp/config/<name>.yaml. Keep packaged defaults unchanged. The three portable override files are authoritative reviewed deployment sources; merge intentional changes here first and redeploy them. Do not edit github.yaml, credentials or machine-specific launcher settings into these sources. dependencies.yaml is an installation manifest, not a PGMCP override.

## Provision native prerequisites

Start with the pinned harness and its supported workspace environment, following [workspace setup](../../README.md#workspace-setup). From the repository root, install the quality prerequisites into the same environment selected by adapter execution:

```powershell
& '.\.venv\Scripts\python.exe' -c "import pathlib,subprocess,sys,yaml; d=yaml.safe_load(pathlib.Path('setup/quality/dependencies.yaml').read_text(encoding='utf-8')); subprocess.run([sys.executable,'-m','pip','install',*d['python_requirements']],check=True)"
```

The harness lock fixes shared transitive dependencies; the quality manifest adds pinned check-jsonschema, orjson, ruamel.yaml and regress while retaining the required jsonschema version. Do not substitute newer adapter-native versions without reviewing the installed adapter declarations.

Install the native Lychee 0.24.2 executable from its [official release](https://github.com/lycheeverse/lychee/releases/tag/lychee-v0.24.2). On Windows x86-64, use the exact archive URL and SHA-256 in dependencies.yaml. Verify the archive before extraction; install its single lychee.exe into .venv/Scripts. Downloaded archives and extraction contents belong under ignored setup/downloads/. The upstream .sha256 file can use Windows certutil text rather than the common hash-first format; compare the actual 64-hex-digit hash or the release asset digest.

Other supported hosts must select the matching official archive and verify its published checksum for the same pinned version; do not reuse the Windows hash. The portable YAML policy has no host paths.

The server's absolute Python command does not choose adapter executables. Configure the actual connection PATH with the workspace environment's Scripts (Windows) or bin directory first, preserving required existing entries. Python adapter entrypoints must resolve that interpreter and Lychee must resolve the intended native executable. Keep actual host paths and deployment records local. Verify actual tool identities through native PGMCP execution; health and version discovery alone are insufficient.

## Deploy reviewed overrides

Review the three source files and any existing local customizations before deployment. For a fresh deployment with absent destination overrides, the following explicit setup operation seeds the reviewed files and breaks the scaffold acknowledgement bootstrap circle:

```powershell
foreach ($qualityName in @('checks.yaml', 'tests.yaml', 'fixes.yaml')) {
    $qualityDestination = Join-Path '.pgmcp/config' $qualityName
    if (Test-Path -LiteralPath $qualityDestination) {
        throw "Existing override requires review and merge: $qualityDestination"
    }
    Copy-Item -LiteralPath (Join-Path 'setup/quality' $qualityName) -Destination $qualityDestination
}
```

For existing overrides, merge reviewed differences with safe_edit_file instead of overwriting customizations. Initial unresolved configuration can require validation=report on an existing file; that write is not a validation pass. Normal scaffold/edit enforcement resumes after binding configuration and prerequisite provisioning.

Call restart_server after deployment, wait for its stated restart interval, then call get_work_context first. Inspect pgmcp://rules/coding_standards: default_profile must be repository_review and python_tests must be inactive. Compare each local override with its portable source, then execute representative checks. A successful reload proves consumer admission, not native check success. Startup/configuration failure blocks progression and requires diagnosis; do not weaken bindings to obtain admission.

## Select checks through PGMCP

Use family-specific explicit file targets during implementation. Examples from the repository root:

```json
{"scope":"targets","targets":["README.md","AGENTS.md"],"checks":["markdown_links"]}
{"scope":"targets","targets":["setup/quality/checks.yaml","setup/quality/tests.yaml","setup/quality/fixes.yaml","setup/quality/dependencies.yaml"],"checks":["yaml_configuration"]}
```

For a changed .schema.json file, select json_schema_shape and json_schema_metaschema on that exact file. YAML checks require a mapping root; they do not validate application-specific keys or PGMCP semantics. The actual consumer must also accept configuration after reload.

repository_review is intended for branch selection. Only scope=branch applies per-check configured_targets filtering. Explicit targets, workspace and configured scopes do not inherit that filtering; do not send mixed file families to the whole profile or assume directory discovery for file-required checks.

In Validation, run run_checks(scope="branch") once after final implementation changes and run_tests(scope="configured") as required by the chore workflow. Inactive tests may return no_active_tests; that is no executed test evidence. A branch family with no matching files is not_applicable, also not a passing check.

Caller args replace the complete default argument list for that binding. Ordinary checks should omit args and retain configured offline Markdown and schema policies. Any intentional override must record its full effective arguments and rationale. Required unavailable/unexecuted checks block acceptance. External URLs are outside the offline check's evidence.

## Disposable verification and evidence

[Implementation evidence](../../docs/development/issue2/implementation-evidence.md) records exact selections, synthetic fixture content and observed persistence. Fixtures use ignored tmp/issue2-quality/ and must not be staged.

Verify valid Markdown scaffolding, missing local paths and fragments under enforce, invalid content under report, rejected guarded edits preserving original content, and repair under enforce. Verify positive/negative YAML and schema checks and preserve actual native versions and outcomes. Keep checks, tests and fixes separate. No automated fix is exercised under the current deferred fix policy.

A successful tool envelope, acknowledged binding, empty selection or healthy server is never proof of a required native pass. report may persist failed content. Native unavailability differs from a completed negative check; record both honestly.

## Deferred capabilities and revisit triggers

| Capability | Current decision | Revisit trigger |
| --- | --- | --- |
| Python syntax, Ruff format/lint, Mypy and Pyright | Choices remain unresolved; excluded from repository_review. | Application language, production/test roots, runtime, rules, severities and exclusions are approved. |
| TypeScript syntax | Choice unresolved; no application stack selected. | TypeScript source/runtime becomes an approved repository concern. |
| python_tests | Inactive and unresolved; explicit selection still refuses configuration. | Real test suite, discovery, native arguments and evidence policy are approved. |
| python_format / python_lint fixes | Unresolved; no automatic fixes executed or permitted. | Explicit disposable-target verification and owner-approved fix policy. |
| commit_message / Commitlint | Unresolved; PGMCP commit conventions remain in force. Commit-template scaffolding remains blocked until configured. | Native commit rules/config and pinned prerequisites are approved. |
| External URL checks | Outside the approved offline gate. | An explicit network-dependent evidence and failure policy is approved. |

Do not label an unused binding configuration_choice=not_applicable to suppress a blocker: that value means no additional native policy is needed. Phase instructions may ask for checks/tests whose capabilities remain deferred; record the actual neutral/refused outcomes and explicit policy decision, never a fabricated pass.

## Related Documents

- [Approved Research](<../../docs/development/issue2/research.md>)
- [Initial setup validation](<../../docs/development/issue2/validation.md>)
- [Repository agreements](<../../README.md#working-agreements>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-21 | @imp implementer | Document pinned native setup, workspace override deployment, selection limits and revisit triggers for issue 2. |
| 1.1 | 2026-10-21 | @imp documenter | Reconcile maintained status and link the initial setup validation record. |
