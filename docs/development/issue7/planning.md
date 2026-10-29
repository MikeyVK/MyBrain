<!-- pgmcp:v1 id=planning pv=1.0.0 pf=OSfLTQ1qMuWvM9fi sf=WI5iXHBKVOU91bYE -->

# Portable Windows workspace deployment planning

**Status:** PLANNING — independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-28

## Purpose

Slice the approved Research and Design v1.1 into bounded implementation cycles and later phase evidence; no production implementation occurs in Planning.

## Scope In

Workspace/tooling/setup transfer only: source retention, executable package commands, verified dependencies, isolated target consumers, real ZIP and synthetic/local verification.

## Scope Out

Private operational data or export, credentials/account caches, provider identifiers/private resumption manifests/PDFs, donor mutation, application redesign, global destructive configuration and push/PR/merge.

## Prerequisites

- [Research Approved Strategy](research.md#approved-strategy) and [Design v1.1](design.md) remain binding.
- Original independent Design GO was consulted for exact 497190f90748327f498cec05a7d1a9de214fc388. Co assigned one Planning writer on issue 7 and authorized only this phase.
- After design-to-planning entry, the assigned connection was restarted through its supported route; post-wait get_work_context read back issue 7, the correct branch and Planning before authoring.
- No existing application suite is approved; deployment public-command/build/smoke verification is explicitly within the technical mandate.

## Summary

Three dependency-ordered cycles implement the chosen design: C_1 establishes contracts and durable negatives, C_2 admits real artifacts/source and target consumers, C_3 builds and exercises the actual ZIP. Two deliverables per cycle plus two each for Validation and Documentation make ten stored deliverables. No generic installer framework or new application stack is planned.

### Acceptance-to-evidence map

The rows follow the [issue 7 acceptance criteria](https://github.com/MikeyVK/MyBrain/issues/7), rather than redefining them.

| Acceptance boundary | Planned deliverables and decisive evidence |
| --- | --- |
| 1. Primary/donor progress, fixed cutoffs and omissions | D_2.2 and D_3.1: source ref/SHA inventory refreshed at build, stable source-only local capture, exact retained bytes/overlay reconstruction and explicit public-safe exclusions; donor untouched. |
| 2. Standalone usable source and safe history boundary | D_1.1, D_2.2, D_3.2: new Git metadata, no raw history/worktree pointers; integrated/deployment/donor trees separately recoverable, exact source hash comparison and usable Git commands. |
| 3. Original versus new identity and later development | D_2.2, D_3.1; Documentation D_1: original refs/SHAs/cutoffs and new import SHA distinguished, old workflow/QA historical only, no origin/force-push/automatic reconciliation; safe reviewed delta route documented. |
| 4. Configurable safe bootstrap and reruns | D_1.1-D_1.2, D_3.2: preflight/write separation; path with spaces, interrupted resume, locks, edited/foreign destination and sentinel preservation tested through actual public commands. |
| 5. Portable roles/quality/schema/tool dependencies | D_2.1-D_2.2: artifact licenses/hashes/ABI/closure, actual local venv install/native execution and source-consumer parity; fresh package assets, no copied venv. |
| 6. Target-local named registration and activation | D_2.2, D_3.2: parsed project registration, actual root/PATH/role/native positive-negative isolation; every participating host connection admitted separately, missing trust/login/activation explicit. Bootstrap invents no issue. |
| 7. Workspace/tooling/setup only | D_1.2, D_2.2, D_3.2: allowlist plus content/metadata review and negative private-category fixtures; independent actual archive inspection; no runtime/export task. |
| 8. Integrity, environment, recovery and short handover | D_2.1, D_3.1; Documentation D_1-D_2: inventory/licenses/source provenance, noncircular manifest/outer SHA-256, supported OS/tool facts, tested recovery, short command and stop conditions. |
| 9. Real archive extraction, quality and independent QA | D_3.2; Validation D_1-D_2: actual ZIP fresh extraction/checksums/bootstrap/rerun/negative cases, precise limitations, required repository gates and independent exact-revision/outer-digest review; final artifact paths and target-agent message. |

### Verification and review policy

New behavior in each cycle requires meaningful RED → GREEN through public entrypoints. Follow with only justified planned refactoring and rerun affected cases. Do not count missing tools, syntax/import failures, version assertions, test-file existence or marker text as behavioral proof. Actual artifact download/license/capture/build evidence and mechanical documentation work need no artificial RED. Tests use injected local artifacts/synthetic identities, ordinary annotations, narrow readers and no private-method assertions; preserve the Architecture Principles and typing rules without enabling unrelated deferred gates.

Use the planned driver `setup/deployment/tests/Invoke-DeploymentTests.ps1 -Suite Contracts|Provisioning|Archive` (one concrete suite value per invocation) for focused technical build/smoke evidence. It calls the Design public commands. Reuse fresh passing suites until an affected change invalidates them. Native PowerShell parsing and helper syntax compilation supplement behavior, never replace it. Keep exact commands, fixture purpose, versions, results and limitations in a screened implementation evidence index; machine paths/host identities and bulky reports stay ignored/local.

For changed Markdown run `run_checks(scope="targets", targets=[<changed .md files>], checks=["markdown_links"])`. For changed YAML select `yaml_configuration` and demonstrate actual consumer admission; for changed JSON Schema select both `json_schema_shape` and `json_schema_metaschema`. Retain configured arguments and separate file families. These are [existing native bindings](../../../setup/quality/README.md); application lint/type/tests/fixes remain deferred. Reserve `run_checks(scope="branch")` and `run_tests(scope="configured")` for Validation once after final implementation. A returned `no_active_tests` is no executed application-test evidence; it does not invalidate separately observed deployment smoke results or become a claimed pass.

C_1 and C_2 are unmarked intermediate exits: proceed only after their objective evidence within Co's mutation assignment, using the next cycle context. **C_3 is QA-required**, as is every phase exit. Freeze the final implementation revision/archive, quiesce, and request independent QA. Co schedules progression after the original matching verdict. No reviewer is created or approval inferred by this plan. Final archive QA binds the actual outer digest; later included-byte changes require new archive hashes, extraction and affected review.

### Planning evidence and persistence

`save_planning_deliverables(issue_number=7, ...)` stored three named ordered cycles and ten complete deliverables. `get_project_plan(issue_number=7)` readback was compared to submitted cycle/deliverable names, descriptions and exit criteria, including phase blocks and ordering. The server-derived C_1-C_3/D_1.1-D_3.2 references below and phase-local D_1/D_2 are authoritative; they are not a parallel progress register. Semantic completion requires the stated actual behavior/evidence, not shallow file-existence predicates. This plan performs no deployment tests or build. `run_checks(scope="targets", targets=["docs/development/issue7/planning.md"], checks=["markdown_links"])` executed Lychee 0.24.2 with configured `--offline --cache=false --include-fragments`: passed, seven successful local links, zero errors and one external URL excluded. The final enforced guarded edit also executes this native document gate. No YAML or JSON Schema source is changed in Planning.

## Dependencies

- C_1 requires independent Planning GO and Co-scheduled implementation entry; first entry starts C_1.
- C_2 requires C_1; C_3 requires both earlier cycles. Only one mutating Imp per verified worktree; no root-bound operation is routed to the donor or extracted target.
- Validation follows independent final implementation GO. Documentation follows independent Validation GO; any included instruction change refreshes affected archive evidence.
- No real issue continuation or remote reconciliation on restored sources until Co verifies target admission, original owner authority and fresh issue initialization.

## Risks

### Redistribution, ABI or exact runtime/Git artifact closure may be incomplete.

Resolve exact artifacts/licenses in C_2; use only the approved item-specific hash-verified primary-download fallback and disclose hybrid status. Stop affected provisioning if neither route works.

**Consequence:** Unexpected network/build dependency or unsupported target.

### Live donor changes or later package edits invalidate cutoffs and archive evidence.

Read immutable SHAs, verify stable local bytes, refresh final capture; bind the ZIP to its actual build input and digest. No donor writer takeover.

**Consequence:** Lost selected progress or stale evidence.

### Target login/trust/host activation and second-PC evidence cannot be guaranteed locally.

Prove generated-launch versus actual host evidence separately, report pending actions and unavailable environments precisely; do not weaken required selected-capability acceptance.

**Consequence:** A locally verified ZIP may still need declared target-host action.

### Previously observed unexplained phase regression could recur.

Check phase/history after supported own-connection activation and before commit; on mismatch stop and route exact call chronology to Co. Preserve committed audit, never invent a replacement transition.

**Consequence:** Wrong-phase mutations or corrupted lifecycle evidence.

## Work Units

### C\_1 — Package contracts and public-command verification

**Goal:** Establish safe observable package contracts before real inputs.

**Cycle Number:** 1

**Owner:** Imp

#### Scope In

Planned seams: setup/deployment entrypoints Preflight.ps1, Bootstrap.ps1, Verify.ps1, Recover.ps1, Build-Package.ps1 and Test-Package.ps1; manifest schemas, helper and setup/deployment/tests/Invoke-DeploymentTests.ps1. Names follow Design; helper decomposition stays cohesive.

#### Scope Out

Actual third-party dependency procurement, real source capture, host registration activation and final archive acceptance belong to later cycles.

#### Deliverables

##### D\_1.1

Implement setup/deployment PowerShell entrypoints and cohesive Python helper for Design v1.1 package/manifest schemas, exact selected-source reconstruction, non-mutating preflight, strict containment, destination ownership/conflicts, journal/resume/recovery and structured exit codes. Preserve configured architecture and privacy boundaries; no installed-package patch, private input, global change or remote action.

**Owner:** Imp

##### D\_1.2

Provide setup/deployment/tests/Invoke-DeploymentTests.ps1 contract cases that call public commands and compare observable outputs and untouched sentinels. Cover valid manifests/source overlays and corrupt/missing/extra payload, traversal/ADS/duplicate/link/reparse/size cases, unknown schema, selected-source bytes versus generated outputs, existing conflicts, interruption/lock/resume/recovery. Record intended RED then GREEN; syntax/import/missing-host errors are not behavior proof.

**Owner:** Imp

#### Exit Criteria

C_1 depends on approved Planning and no earlier cycle. Contract suite passes through public commands; invalid inputs are rejected before destination admission and selected safe source bytes reconstruct exactly. PowerShell parsing/helper syntax and changed Markdown/YAML/schema gates pass where applicable; expected-negative invocations are recorded separately. Commit meaningful RED/GREEN and only changed planned refactoring. No additional independent intermediate-cycle QA is required; transition only on objective evidence under Co assignment, never on an unexecuted application-test claim.

#### Dependencies

- Approved Planning

#### Obligations

- Design v1.1 manifest, source-byte retention, public command and containment/recovery contracts are binding.
- Use RED → GREEN for new durable public behavior. Supply only the minimal executable boundary needed to expose the intended behavior gap; missing runtime/syntax/import errors do not establish RED. Refactor only changed planned cohesion/duplication.

#### Verification

##### Public contracts and preservation

**Method:** Run the planned Invoke-DeploymentTests.ps1 -Suite Contracts driver on synthetic fixtures; it invokes the documented public commands and compares return codes, reconstructed bytes and unchanged sentinel files. Preserve intended RED then GREEN output.

**Expected Result:** All positive contracts succeed, all intended negatives reject before admission, no private helper access or live data; syntax failures are separately diagnosed.

##### Narrow static/document gates

**Method:** Parse changed PowerShell files with the native parser; compile helper syntax without retained bytecode. Run PGMCP changed-family targets as specified in the shared verification policy below.

**Expected Result:** Executable syntax and applicable native Markdown/schema/YAML checks pass; no claim of deferred lint/type/application-test execution.

#### Stop Conditions

- A malformed/unsafe fixture writes outside its verified target or corrupts a sentinel.
- Selected source cannot be reconstructed exactly, an unreviewed interface change is needed, or phase/worktree identity drifts.

### C\_2 — Verified dependencies, source capture and local consumers

**Goal:** Admit the real distributable toolchain and reconstruct correct isolated local consumers.

**Cycle Number:** 2

**Owner:** Imp

#### Scope In

Extend the same provisioning, source capture and consumer seams; add portable dependency/hash lock and license/provenance inputs under setup/deployment. Use existing setup/quality, setup/pgmcp and .agents sources; installed assets come from the exact admitted wheel. Downloads/environments/trial outputs stay ignored.

#### Scope Out

No private runtime inspection/export, active donor edits/checkout, source package patches, policy weakening, global installation, target account copying or remote modification.

#### Deliverables

##### D\_2.1

Resolve and verify actual CPython 3.15.0 x64, PGMCP 4.0.0 wheel, complete binary/hash-pinned harness-plus-quality closure, Lychee 0.24.2 and usable Git baseline/portable fallback. Record exact primary URLs, versions/ABI, hashes, licenses/notices and redistribution decisions. Exercise destination-local runtime/venv and native executables. Enumerate only approved item-specific pinned verified-download gaps and mark hybrid/network requirements; no silent index/source-build/latest fallback.

**Owner:** Imp

##### D\_2.2

Implement fixed-SHA capture of integrated/deployment and active-storage source plus individually screened stable local differences without donor mutation. Preserve every selected safe original byte/hash and reconstruction operation separately from generated output; explicit public-safe exclusions for non-selected/unsafe candidates. Generate new standalone target Git identity without origin or inherited issue/QA state, fresh PGMCP assets, reconciled protocols/quality overrides and target-local Codex roles/unique named binding. Verify parsed parity, final-path launchers, pip consistency and positive/negative native isolation using synthetic fixtures; local generated-launch proof is distinct from host activation.

**Owner:** Imp

#### Exit Criteria

C_2 depends on C_1. Dependency/license manifest admits every required artifact or precisely declares the approved pinned hybrid gap; actual installation/import/native execution succeeds from the admitted artifacts at a path with spaces. Provisioning suite covers new behavior RED/GREEN plus actual toolchain evidence. Source input bytes/cutoffs and generated consumer parity are proven, no private/donor/global/remote mutations occur, and stage conflicts/reruns preserve customizations. Changed-family gates and real consumer admission execute. No additional independent intermediate-cycle QA is required. Host trust/login/connection activation still needs its separate evidence and cannot be inferred from local launch success.

#### Dependencies

- C_1

#### Obligations

- C_1 is complete; hashes/licenses/ABI and actual installation must admit each artifact before use. Resolve exact Git/runtime distribution details without silently changing the approved runtime or dependency strategy.
- Test new provisioning/source/consumer behavior RED → GREEN with synthetic local artifacts; actual dependency/license inspections and installation trials need factual evidence, not artificial RED.
- Preserve all selected safe original source bytes alongside target-generated consumers, with explicit public-safe candidate dispositions; capture without taking over the donor writer.

#### Verification

##### Real dependency closure

**Method:** Run Invoke-DeploymentTests.ps1 -Suite Provisioning and Bootstrap.ps1/Verify.ps1 on disposable paths with spaces. Install from the admitted wheelhouse/hash lock with index access disabled in bundled mode; exercise pip consistency, venv launchers, imports and actual Lychee/schema tools. Negative cases remove/corrupt artifacts and deny declared downloads.

**Expected Result:** No undeclared fetch/source build or global modification; exact versions/ABI/licenses are recorded. Hybrid items are specifically enumerated and failures honest.

##### Source and consumer correctness

**Method:** Reconstruct selected source trees/overlays and compare exact bytes/hashes; stable before/after donor capture checks. Parse target TOML and compare role fields/protocol/override content. Inspect launcher roots and run native positive/negative synthetic checks through the generated target launch route.

**Expected Result:** New standalone Git identity, no copied origin/old active issue/QA, target-local paths/native PATH and isolation. Launcher success alone is not actual Codex host activation.

#### Stop Conditions

- An item cannot be bundled or covered by the approved exact primary-download fallback; no unpinned substitute.
- A source candidate is unstable/private, a license disallows inclusion, a destination is foreign/customized or required native consumer admission fails. Stop that affected operation; preserve and disclose safe exclusions.

### C\_3 — Real ZIP, fresh extraction and recovery evidence

**Goal:** Produce and exercise the actual handover bytes with truthful evidence.

**Cycle Number:** 3

**Owner:** Imp

#### Scope In

Final builder/archive/handover outputs and the same public verification driver, actual extracted bootstrap environment and screened docs/development/issue7/implementation-evidence.md index. Candidate artifacts/reports remain ignored/local; tracked evidence is public-safe.

#### Scope Out

Clean-second-PC/VM or offline claims without proof; target account/trust automation outside host permissions; personal data; force-push/origin replacement or implicit issue continuation.

#### Deliverables

##### D\_3.1

Refresh source refs/stable local capture and freeze explicit final build-input revision/cutoffs after package sources are committed. Build the actual screened ZIP with exact inventory, dependency/license/provenance facts, detached manifest hash and externally delivered outer SHA-256. Include concise START-HERE/start command, supported environment, original/new Git identity distinction, safe later remote reconciliation, exclusions and recovery/stop instructions. Final own-archive extraction/QA evidence remains beside the ZIP and names its digest, avoiding self-reference.

**Owner:** Imp

##### D\_3.2

Extract the actual final ZIP into a fresh disposable path containing spaces after member checks, verify exact hashes/membership, run preflight/bootstrap/verify, rerun and controlled interruption/resume/conflict/recovery cases, and prove standalone source restoration/exact selected overlays and unchanged unrelated sentinels. Run full deployment verification including negative archive/dependency paths; demonstrate actual named target host binding/role/native isolation when available and distinguish pending host action from completion. Record precise OS/network/login/second-PC/VM limitations, actual ZIP/checksum/manifest/handover paths and exact target-agent message; independent final archive QA is required against this digest.

**Owner:** Imp

#### Exit Criteria

C_3 depends on C_1 and C_2. Final actual ZIP and external digest/evidence exist; extracted bytes, local tooling, safe reruns/recovery and privacy/source obligations are demonstrated, with unavailable target-host/second-PC proof explicit rather than fabricated. Archive orchestration behavior uses durable RED/GREEN where new; repeated evidence-only trials need no artificial RED. All relevant focused suites and invalidated file-family checks pass; no inactive application-test pass is claimed. QA-required: independent original exact-revision GO for this final implementation cycle/phase exit plus inspection of the actual final archive digest before progression. Stop quiescent; any changed included byte requires refreshed hashes, extraction evidence and affected QA.

#### Dependencies

- C_2

#### Obligations

- C_1 and C_2 complete; refresh fixed source facts and freeze a real committed build-input revision before final capture. Later included-byte changes invalidate the outer digest and affected extraction/archive QA.
- Test newly introduced archive orchestration behavior RED → GREEN; capture/build/repeated verification-only work needs no manufactured RED. Reuse unchanged fresh contract evidence.
- QA-required final cycle and implementation-phase exit. Independent QA must inspect the actual outer digest; no extra intermediate-cycle review is imposed for C_1/C_2.

#### Verification

##### Actual archive journey

**Method:** Build-Package.ps1 -Destination <ignored-output> -Sources <local-spec>; then Test-Package.ps1 -Archive <actual.zip> -Destination <fresh-space-path> and Invoke-DeploymentTests.ps1 -Suite Archive. Exercise Preflight.ps1, Bootstrap.ps1, Verify.ps1 and Recover.ps1 against the extracted package, second run, controlled interruption and conflicting/edited outputs.

**Expected Result:** Exact archive membership/hash/source reconstruction; usable standalone Git/toolchain; no unrelated sentinel changes; verified resume and conflict preservation. Final self-archive evidence is external and digest-bound.

##### Host and handover facts

**Method:** Under the host's supported route, activate each intended generated named connection, independently inspect root/branch/no invented issue and demonstrate synthetic positive/negative native isolation. Co must admit any additional host connection; never operate the extracted workspace through the parent's fixed-root pgmcp.

**Expected Result:** Actual host proof recorded where available; unavailable login/trust/capability remains pending with exact action and limits. Absence of second-PC/VM evidence remains explicit and does not become a clean-machine claim.

#### Stop Conditions

- Any manifest/privacy/containment/recovery failure or outer-digest mismatch; any attempt to treat generated output as retained original source.
- Missing independent final-cycle/archive verdict, unverified required host capability or changed reviewed archive prevents the associated acceptance/transition. Report unavailable external evidence instead of fabricating success.

## Phase Deliverables

### Validation

#### D\_1

Create docs/development/issue7/validation.md mapping all issue acceptance criteria and C_1-C_3 outcomes to exact commands, native identities, observed results and durable screened evidence. Run run_checks(scope='branch') once after final implementation changes and run_tests(scope='configured') once; retain no_active_tests as no executed application-test evidence. Complete only materially missing deployment checks, record actual host proof or explicit pending action and absent second-PC/VM/offline evidence.

**Owner:** Imp

#### D\_2

Provide the final ZIP path/digest, exact manifest/source cutoff facts, exclusions, reproduction commands, failures/limits and external extraction evidence for independent archive QA. Preserve original revision-bound review and outer-digest identity; any later archive-byte change needs new extraction/affected review. No register or post-review recording commit is required.

**Owner:** Imp

### Documentation

#### D\_1

Finalize setup/deployment/README.md, package START-HERE text and repository entry links with tested start/preflight/bootstrap/verify/recovery commands, requirements, safe source/remote continuation and exact retained-source boundary. Keep local paths/IDs/secrets/private evidence out of tracked docs; verify local links and any changed configuration families. If an included instruction changes, rebuild and reverify the archive rather than retaining stale evidence.

**Owner:** Imp

#### D\_2

Return the real final archive path, outer SHA-256, manifest/handover/evidence paths and precise short target-agent message. State what was actually tested, bundled versus hybrid online items, target login/trust/activation needs, absent second-PC/VM proof and unfinished capabilities. Completion/publication authority is not inferred; no push/PR/merge or private-data transfer.

**Owner:** Imp

## Related Documents

- [Approved Research](<research.md>)
- [Approved Design v1.1](<design.md>)
- [Repository quality policy](<../../../README.md#quality-policy>)
- [Portable source/deployment map](<../../../setup/pgmcp/README.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-28 | @imp planner | Define three dependency-ordered deployment cycles, acceptance/evidence mapping and complete Validation/Documentation deliverables. |
