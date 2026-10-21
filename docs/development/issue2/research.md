<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue 2 quality tooling research

**Status:** RESEARCH — strategy approved by owner; independent review pending  
**Version:** 0.2  
**Last Updated:** 2026-10-21

## Scope In

Workspace quality policy, portable reviewed overrides and setup documentation, native adapter prerequisites and disposable public-safe verification fixtures.

## Scope Out

Application implementation or stack selection, PGMCP server changes, QA authority changes, remote protection or visibility changes.

## Problem Statement

At initial inspection, the repository had no approved native quality policy. All eleven check bindings, one test binding and two fix bindings inherited unresolved configuration_choice values, blocking Markdown scaffolding before native validation. The owner subsequently approved the strategy below; initial bootstrap and native evidence are recorded separately.

## Goals

- Separate current documentation/configuration needs from future application tooling.
- Identify supported configuration and dependency boundaries without changing packaged defaults.
- Present concrete policy decisions and factual verification obligations.

## Findings

### Observed baseline before owner-approved setup

ConfigLoader composes .pgmcp/config/defaults/<name>.yaml with optional .pgmcp/config/<name>.yaml. The config directory currently contains only github.yaml as a root override. There are no checks.yaml, tests.yaml or fixes.yaml root overrides.

| Surface | Inherited bindings | Current state |
| --- | --- | --- |
| Checks | python_syntax, typescript_syntax, commit_message, python_format, python_lint, python_types, python_pyright, markdown_links, yaml_configuration, json_schema_shape, json_schema_metaschema | All configuration_choice values null |
| Tests | python_tests via pytest | Active true; choice null; no repository application tests |
| Fixes | python_format and python_lint via Ruff | Both choices null |
| Default check profile | python_review | Unsuitable as the default proof of a documentation/configuration change |

Markdown defaults select offline Lychee local-link and fragment validation with --offline --cache=false --include-fragments. YAML validation requires a mapping root; this does not validate PGMCP-specific semantic configuration. JSON Schema validation has separate envelope and metaschema checks. No application source/test tree or QA verdict artifact was found.

### Native declarations

| Adapter | Package-declared prerequisite |
| --- | --- |
| Lychee | Native executable lychee 0.24.2 |
| check-jsonschema | check-jsonschema 0.38.2, orjson 3.13.0, ruamel.yaml 0.18.16, jsonschema 4.26.0 in the execution interpreter |
| Commitlint | @commitlint/cli 21.2.2, conventional-changelog-conventionalcommits 10.4.0; Node >=22.12.0 |
| Ruff / Mypy / Pyright | Ruff 0.17.1 / Mypy 2.4.0 / Pyright 1.1.414 |
| Pytest | pytest 9.1.1, pytest-cov 7.1.0, pytest-xdist 3.8.0, coverage 7.16.2, pytest-asyncio 1.4.0 |
| TypeScript syntax | typescript 6.0.3 |

Static package-directory inspection found jsonschema 4.26.0 in the workspace environment but did not find check-jsonschema, orjson or ruamel.yaml distribution directories. This is an inventory finding, not a native availability test. Host-shell executable discovery found several tools outside the workspace environment; this does not establish the MCP child's PATH, matching native versions or actual adapter usability.

### Owner-approved policy

Require offline Markdown local-link/fragment checks for changed maintained Markdown and enforce them during ordinary scaffolding and guarded editing. Require YAML mapping validation and both JSON Schema checks when their file families are changed; separately verify PGMCP consumer acceptance after configuration reload. Use explicit file targets during implementation and one branch-wide documentation/configuration profile in Validation. Preserve raw passed/failed/unavailable/not_executed outcomes; report mode never counts as a pass.

Defer application Python/TypeScript analysis, pytest and automated Ruff fixes until application language, source/test roots and quality rules are chosen. Defer native Commitlint until its native rules/configuration are explicitly chosen; retain existing PGMCP commit conventions. A deferred binding must not be falsely acknowledged with configuration_choice=not_applicable, which means no additional native policy is needed rather than that the capability is unused.

Use version-controlled portable setup sources outside ignored server data, deploy reviewed overrides under .pgmcp/config, preserve packaged defaults, and pin approved native prerequisites to the adapter declarations. No automatic source fixes are proposed. Document retained configured-scope test calls truthfully even if no active test binding is selected.

### Bootstrap boundary

scaffold_artifact refuses unresolved required quality setup under enforce and report. safe_edit_file report can edit existing files but cannot create a missing root override. Consequently, creating the first root checks.yaml override through ordinary scaffold/edit routes is blocked. The owner explicitly approved the narrow exception for initial creation of workspace overrides on 2026-10-21. The initial checks.yaml override was created under this exception; packaged defaults were left unchanged. It must not authorize editing packaged defaults, acknowledge unrelated bindings or claim validation.

The change ceases to be mechanical if it requires server changes, choosing an application stack, weakening required validation, or changing workflow/QA authority. Stop and return the decision in those cases.

## Approved Strategy

On 2026-10-21 the owner explicitly approved the proposed policy, native prerequisite provisioning and one-time initial workspace-override creation exception, then instructed implementation to continue. The authorization was: "Akkoord met het voorgestelde beleid, het provisioneren van de native tools en de eenmalige uitzondering voor het aanmaken van de eerste workspace-overrides. Ga verder."

Documentation boundary: require offline local-link and fragment checks, preserving normal scaffold/edit enforcement. Configuration boundary: require applicable YAML mapping and JSON Schema envelope/metaschema checks and actual PGMCP consumer loading; do not change packaged defaults or server implementation. Selection boundary: explicit focused files during implementation, branch-wide repository profile during Validation. Application boundary: defer Python/TypeScript checks and tests until application stack, roots and policy are selected. Fix/commit boundary: defer automated fixes and native Commitlint; retain PGMCP commit conventions. Distribution boundary: version portable setup sources, keep machine deployment and credentials local. Bootstrap exception: create only the initial workspace overrides needed to break unresolved setup; normal tools govern subsequent artifacts. No compatibility bridge or supported server-contract break is authorized.

## Expected Results

After explicit owner decisions and implementation: record PGMCP native passing and deliberately failing checks; valid/invalid local path and fragment scaffold/edit persistence under enforce/report; unavailable and unexecuted outcomes where applicable; exact selections and configured arguments. Keep checks, tests and fixes separate. Tests/fixes may remain explicitly deferred without a passing claim.

## Evidence

### Initial native YAML inability was reported truthfully.

After loading the first acknowledged binding but before installing dependencies, the selected check returned unavailable/dependency_unavailable.

**Invocation:** run_checks(scope="targets", targets=[".pgmcp/config/checks.yaml"], checks=["yaml_configuration"])

**Observed Result:** incomplete; yaml_configuration unavailable/dependency_unavailable

### The selected YAML binding executes after approved provisioning.

The same explicit-target YAML check returned passed with configured arguments after installing the package-declared prerequisites.

**Invocation:** run_checks(scope="targets", targets=[".pgmcp/config/checks.yaml"], checks=["yaml_configuration"])

**Observed Result:** passed

### Offline Markdown execution uses the declared native Lychee pin.

PGMCP reported markdown_links passed, Lychee 0.24.2, native exit 0 and effective configured offline arguments. External URLs were excluded as intended.

- [README](<../../../README.md>)
- [Agent entrypoint](<../../../AGENTS.md>)

**Invocation:** run_checks(scope="targets", targets=["README.md","AGENTS.md"], checks=["markdown_links"])

**Observed Result:** passed

## Consumers

### Imp

Configure and verify selected workspace bindings.

**Impact:** Needs approved strategy before implementation.

### QA

Independently assess evidence.

**Impact:** Receives exact scope and outcomes, without producer approval claims.

## Risks

### Shell-discovered programs may not match the server execution interpreter or PATH.

Verify actual selected adapters through PGMCP after approved provisioning; never use health or discovery as validation evidence.

## Related Documents

- [Issue 2](<https://github.com/MikeyVK/MyBrain/issues/2>)
- [Repository agreements](<../../../README.md#working-agreements>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-21 | @imp researcher | Inventory current bindings, setup boundaries and proposed policy; no policy approved or activated. |
| 0.2 | 2026-10-21 | @imp researcher | Record explicit owner approval, bootstrap exception and initial native evidence. |
