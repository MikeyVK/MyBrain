<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Portable Windows workspace deployment validation

**Status:** VALIDATION — independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-28

## Purpose

Satisfy Planning Validation D_1 and D_2 for issue 7 with revision-bound producer evidence and truthful limits. This report does not grant independent Validation GO.

## Scope In

Frozen development workspace/tooling/setup ZIP, source provenance and preservation, actual extracted-package evidence, required native repository verification and external final artifact review index.

## Scope Out

Private-data migration/export; PostgreSQL server, MyBrain schema/product storage or application/API/UI implementation; target accounts/global settings; donor mutation; push/PR/merge/closure.

## Prerequisites

- Original independent MIGRATION-I7-IMPLEMENTATION-QA-3 GO for final C_3 and implementation→validation was directly read in Qa_a for exact 96d75884032a3983fd784a3ba7bbd6fc9a7ddf7d and R6 digest 96529ff8f3ed018d3d6d4b903eca3cbcf465525a8a9cd67f8ba989ac13f65e01.
- Co assigned one mutating Imp on feature/7-portable-workspace-deployment through exact pgmcp in the primary worktree. The native transition entered validation; own supported restart, required three-second wait and actual context readback confirmed validation with preserved audit before authoring.
- get_project_plan(issue_number=7) read back C_1-C_3 completed, Validation active, its D_1/D_2 and later Documentation pending. Research, Design, Planning and final implementation handover were consulted; no plan/register mutation was needed.

## Issue Number

#7

## Validation Status

PASS

## Scope

Producer verification covers the frozen development-workspace/tooling scope. PASS below means applicable native repository gates and the documented available evidence, not application, target-host or universal clean-PC acceptance.

| Issue acceptance criterion | Planned deliverables | Observable evidence / boundary |
| --- | --- | --- |
| 1. Source progress, inventory and cutoffs | C_2 D_2.2; C_3 D_3.1 | R6 manifest fixes deployment ecdb66717c7887427f7a5ca4819ff2dd3b7fae95, main 84d5e0cbbe488fd45160de64d5faab9a97ba7687 and storage 655e9563ba5536d24d9db3c98ef5819ae40feff4 at 2026-10-28T14:08:46.866656Z. Donor remained read-only; explicit candidate exclusions and retained local bytes survive. |
| 2. Standalone usable source without unsafe history | C_1 D_1.1; C_2 D_2.2; C_3 D_3.2 | R5 actual Git init/add/commit/status and no remote; R6 exact source reconstruction/extraction, no original .git/history/worktree pointers. Separate snapshots remain recoverable. |
| 3. Provenance versus new identity; remote continuation | C_2 D_2.2; C_3 D_3.1 | Original refs/SHAs and target-created import SHA distinguished; workflow/QA historical only. Shipped instructions require separately authorized authoritative checkout and reviewed deltas, with no automatic merge/force-push/origin overwrite. |
| 4. Safe configurable Windows bootstrap/reruns | C_1 D_1.1-D_1.2; C_3 D_3.2 | R5 path-with-spaces complete journey: normal rerun/Resume, changed/foreign conflict refusal, own-process interruption, four exact files quarantined, verified/changed staging cases and sentinel. R6 adds read-only prerequisite outcomes and preserves runtime admission. |
| 5. Portable pinned tooling/consumers/licenses | C_2 D_2.1-D_2.2 | Verified CPython 3.15 x64, harness 4.0.0, 49-wheel hash lock, Lychee 0.24.2 and retained license/source notices; new venv, no copied environment. Actual R5 install/pip/native facts reused only for identical core. |
| 6. Named target registration, native operation/isolation | C_2 D_2.2; C_3 D_3.2 | Parsed role/binding parity and actual generated STDIO route: four native positives, three intended negatives, sibling refusal and no active issue. Actual Codex login/trust/per-role host connection activation remains pending. |
| 7. Workspace/tooling/setup only | C_1 D_1.2; C_2 D_2.2; C_3 D_3.2 | Allowlist/content/metadata screening, private-category negatives and independent archive inspection. No private database/mail/archive data, IDs/manifests, credentials/account caches, original private PDFs or private export. Only screened public research editions may be present. |
| 8. Manifest/digests/recovery/short handover | C_2 D_2.1; C_3 D_3.1 | R6 manifest/detached digest/outer digest and START-HERE/agent-handover; supported Windows x64/PS5.1, exact hybrid fallback and preservation/stop instructions. No publisher-authenticity claim from checksums alone. |
| 9. Actual archive and realistic safe execution | C_3 D_3.2 | R6 fresh 385-member extraction/hash verification and six actual-package Preflight cases; R5 full bootstrap/Verify/recovery/native journey reused with its own identity after exact core comparison. No full R6 recovery or second-PC/VM/offline claim. |
| 10. Native gates, meaningful verification, independent QA | C_1-C_3; Validation D_1-D_2 | Fresh branch repository_review passed; configured tests returned no_active_tests. Earlier meaningful deployment RED/GREEN and independent QA-3 exact HEAD/R6 digest GO admit this phase; Validation still requires its own independent review. |

The maintained Design v1.1 contracts and Research Approved Strategy align with these rows: fixed screened snapshots without ancestry; exact safe original-byte retention alongside generated consumers; destination-local recreation; narrow pinned hybrid download; strict integrity/containment/conflict boundaries; separate host activation and remote authority. No redesign, product/database implementation or quality-policy change occurs in Validation.

## Obligations

### Validation D\_1 — Acceptance and repository validation evidence

**Evidence:**

- [Planning](<planning.md>)
- [Implementation evidence](<implementation-evidence.md>)
- [Repository quality policy](<../../../README.md#quality-policy>)

**Outcome:** All acceptance rows above have observable scoped evidence. Applicable required branch gates passed; configured tests are neutral/no execution. Remaining host/hardware/product limits are explicit.

### Validation D\_2 — Independent final artifact review index

**Evidence:**

- [Maintained target instructions](<../../../setup/deployment/START-HERE.md>)
- [Short target-agent task](<../../../setup/deployment/agent-handover.md>)

**Outcome:** Frozen ZIP/manifest/source/digest/report identities below support new exact-revision Validation review. Original implementation GO already binds the actual R6 digest; no additional verdict register or post-review recording commit is required.

## Evidence

### Required single native branch quality request

One requested configured suite returned success=true with error_code=no_active_tests, selected_tests=[] and results=[]. This is neutral/no execution, not an application-test pass. No binding was enabled, acknowledged, waived or relaxed. Deployment technical smoke results are separately observed evidence.

One branch request returned run_status=passed/profile=repository_review. Markdown: Lychee 0.24.2 exit 0, 73 successful links, 9 excluded external URLs, 0 errors; configured --offline --cache=false --include-fragments. JSON Schema shape and metaschema each executed exit 0 with check-jsonschema 0.38.2 (orjson 3.13.0, ruamel.yaml 0.18.16, jsonschema 4.26.0). Shape used --schemafile .pgmcp/config/check_schemas/json_schema_source.schema.json --force-filetype json --output-format JSON; metaschema used --check-metaschema --force-filetype json --output-format JSON. YAML was not_executed/not_applicable because no applicable changed YAML was selected; this is not a YAML pass.

The new Validation Markdown receives its own enforced native local-link/fragment gate after the branch request. No duplicate branch/configured-suite run is needed for this document-only addition.

**Sources:**

- [Native quality sources and policy](<../../../setup/quality/README.md>)

**Invocation:** run_checks(scope='branch', profile='repository_review')

**Observed Result:** passed; Markdown, JSON Schema shape and metaschema executed and passed; YAML not_applicable/not_executed

### Required single configured test request

Do not convert a successful envelope or no-active-tests response into a test pass. Relevant separately executed deployment tests remain described in Implementation evidence.

**Sources:**

- [Configured test policy](<../../../setup/quality/tests.yaml>)

**Invocation:** run_tests(scope='configured')

**Observed Result:** no_active_tests; zero selected/executed application tests

### Fresh R6 affected-boundary evidence retained without rerunning unchanged flows

Actual host Git and exact primary-URI HEAD were exercised. Deterministic unreachable/unproved fixtures separately returned exit 2. Correct target Git/cache avoided network. No package/target/caller mutation or Preflight download/creation. Parser/docs/manifest passed; no startup/payload/marker probe repeated. QA-3 independently repeated the affected package tests.

**Sources:**

- [Final scoped evidence index](<implementation-evidence.md>)
- [Public Preflight tests](<../../../setup/deployment/tests/test_preflight.py>)
- [Safe runtime inventory test](<../../../setup/deployment/tests/Test-RuntimeAdmission.ps1>)

**Invocation:** Invoke-DeploymentTests.ps1 -Suite Contracts; Test-RuntimeAdmission.ps1; ignored verify-r6.py — executed during Implementation and independently reviewed

**Observed Result:** 24 contract-suite tests; inert runtime inventory refusal; fresh actual archive/source checks and six Preflight cases passed

## Demonstration

No new live setup/native/recovery run is justified: implementation code/artifact is unchanged and original independent exact-revision/archive GO is fresh. Review the digest-bound R6 report and independently retained R5 journey report. For a separately authorized target, compare the outer digest, extract safely, read START-HERE.md, run Preflight.ps1 -Destination <new space path> and proceed to Bootstrap.ps1/Verify.ps1 only after Preflight exit 0. Resume uses Recover.ps1 -Destination <same path> -Action Resume; preserve conflicts. Preflight exit 2 means unresolved prerequisite; setup exit 2 is expected only with local_tooling_verified_host_activation_pending. These are reproducible instructions, not newly executed Validation demonstrations.

## Preservation

R6 is frozen outside this phase's new evidence:
- ZIP: `build/deployment/mybrain-windows-x64-20261028-r6.zip`, 80,158,029 bytes.
- Outer SHA-256: 96529ff8f3ed018d3d6d4b903eca3cbcf465525a8a9cd67f8ba989ac13f65e01; detached file is the same ZIP path plus `.sha256`.
- Manifest: `build/deployment/mybrain-windows-x64-20261028-r6/manifest.json`; SHA-256 a947202f79d5eff65cd5c7af554c0a0c4e1228ff0b90a5d44df7b72a782198f5.
- External R6 report: same ZIP path plus `.verification.json`; it records actual_archive_and_preflight_verified, not a newly run full journey.
- Short package handover: staged `agent-handover.md` and `START-HERE.md`; maintained source links below.
- Selected safe original `setup/local/find-postgresql-download.py`: SHA-256 537fcc9338408de2a7d25728d5660a671b7d2a09fa704513d0b6229fc8fe4dc2. It only finds vendor URLs; it is not a downloader/installer. Nine other setup candidates have screened explicit exclusion reasons.
- Independent QA-3 rechecked all 385 members and 171 original Git files. Producer direct comparison counted 167 ordinary deployment/integrated/development files; the four historical workflow originals explain the independent count. Historical records remain provenance, not active issue/QA authority.

R5 core evidence retains build input 39eb07fb385c9c5fc3090037891bfa3d0d918930, review HEAD 7c1e65eec46524d1a259bd9a210257599c026629 and ZIP SHA-256 dbbeacb4768e3e1b435779cd35ae7383732ab9a0e3122baa4ba15c066ab0a590. Its external `mybrain-windows-x64-20261028-r5.zip.verification.json` records the actual full journey. QA-3 confirmed 14 identical packaged core files, 12 unchanged pre-existing shared functions, identical non-Preflight dispatch and dependencies. R5's overall QA-2 NOGO on P2 is preserved; new QA-3 GO addresses the corrected R6 boundary and does not rewrite old identities. No old approval is inherited by a new target import commit.

This Validation document and phase audit postdate the ZIP cutoff. No packaged byte, included instruction, source selection, artifact or donor work is changed.

## Containment

Public boundaries reject unsafe/archive-link/reparse paths and changed/unlisted runtime bytes before interpreter start. Owned journal/recovery preserves conflicts and partial bytes; finite Windows Git promotion retries recheck exact staging/ownership/absent destination. The R5 full journey and R6 affected evidence establish these scoped facts. No private operational store was read/migrated and no target was operated through the primary fixed-root PGMCP connection.

## Failures

- No newly observed applicable repository gate failure. Earlier rejected R2/R3/R4 trials and R5 P2 remain preserved in the implementation history; corrections and final R6 GO do not relabel them as successful.

## Caveats

- Actual Codex installation/login, project trust and each intended named-host connection activation remain unverified; direct generated STDIO/native evidence does not establish host activation.
- No second-PC/VM or fully offline end-to-end proof. Tested local environment was Windows 10 build 19045 x64/Windows PowerShell 5.1.
- Hybrid fallback is only pinned MinGit 2.56.0.4, SHA-256 e3bf78351fe777fba47ddee5950082f8a98bb0f02604fdc7ba3ee2cb68ffa877 at its declared immutable Git-for-Windows primary URL. Network is unnecessary when usable Git or verified local prerequisite exists. Runtime/wheels/native licenses and applicable source archives are retained; local pure-Python PyYAML wheel provenance is disclosed in the manifest.
- Storage snapshot 655e9563 contains issue 6 design/contracts/operations/preservation/acceptance inputs only, with no app/src/API/UI/migrations. No PostgreSQL server, MyBrain schema/empty product storage or running application is provisioned or proved.

## Risks

### A target host can require login/trust/connection admission or lack network for the narrow fallback.

Use truthful Preflight outcomes; perform host actions under target authority and verify each exact named connection before relying on it.

**Consequence:** Local tooling evidence does not guarantee target-host readiness.

### Later archive/source/included-doc changes would invalidate the frozen identity.

Keep R6 frozen; any later included-byte change needs a new digest, affected extraction/review and explicit evidence scope.

**Consequence:** Stale or wrongly attributed artifact acceptance.

## Deferred Work

### Independent Validation review and Co-scheduled Documentation/Ready work.

Every phase exit requires original exact-revision GO; this producer report is not that verdict.

**References:**

- [Planning phase obligations](<planning.md>)

### Target-host activation/hardware confirmation and separately authorized future product/storage implementation.

Remain explicit for Co/Ready triage; the deployment scope includes tooling and design inputs, not database/application construction or private-data export.

**References:**

- [Coverage and host actions](<../../../setup/deployment/START-HERE.md>)

## Related Documents

- [Approved Research](<research.md>)
- [Design v1.1](<design.md>)
- [Planning](<planning.md>)
- [Implementation evidence](<implementation-evidence.md>)
- [Deployment README](<../../../setup/deployment/README.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-28 | @imp validator | Map issue acceptance to frozen R6/new checks and explicit R5 core reuse; record native branch/configured-test outcomes, artifacts and remaining host/product limits. |
