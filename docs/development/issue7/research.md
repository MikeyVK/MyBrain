<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Portable Windows workspace deployment research

**Status:** RESEARCH — Co strategies recorded; independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-28

## Purpose

Establish the evidence, transfer boundary and strategy choices for issue 7 before design.

## Scope In

Windows x64 workspace/tooling/setup ZIP; relevant public-safe source progress; pinned PGMCP/native prerequisites; configurable, repeatable and resumable target recreation; integrity evidence and a short target-agent handover.

## Scope Out

Existing database/mail/archive contents, private operational manifests or identifiers, credentials/account caches, original private research PDFs, active storage-worktree mutation, global/destructive host configuration, application redesign, push/PR/merge without later authority.

## Prerequisites

- Co initialized the real issue 7 feature branch from main and assigned one mutating Imp to this checkout.
- The original owner requested a downloadable deployment ZIP and explicitly selected workspace, tooling and setup only.
- The existing storage-worktree writer remains independent; source inventory is read-only and revision-bound.

## Problem Statement

A Git checkout supplies reviewed source but does not by itself reconstruct the local interpreter, pinned harness distribution, server assets, native checks or correctly bound agent consumers. Copying the current checkout directory or Git object database would also mix source with host-local state and potentially inappropriate history. The required result is a real extracted-and-verified ZIP, not only deployment advice.

## Goals

- Preserve the relevant screened source revisions and disclose the exact capture cutoff and omissions.
- Recreate the supported tooling on a configurable Windows x64 destination, including paths with spaces, while preserving existing work.
- Make ZIP integrity, source provenance, dependency availability, rerun/recovery behavior and remaining manual host steps verifiable.
- Keep all existing private runtime and account data out of the package.

## Background

The repository already versions quality sources, ten shared agent protocols and portable role/phase configuration. Installed consumers live outside those maintained sources and must be recreated/compared. Issue 7 starts from the current integrated documentation baseline; separately active issue 6 has later committed research/architecture progress. This research inspected source metadata and package resources; it neither started nor inspected a live database or mail store.

## Findings

### Observed inventory and source cutoff

Initial inventory was recorded at 2026-10-28T10:05:25Z; source snapshots were rechecked at **2026-10-28T10:14:43Z**. These are explicit research cutoffs, not the final future ZIP cutoff.

| Surface | Observed fact | Consequence |
| --- | --- | --- |
| Integrated source | main at 84d5e0cbbe488fd45160de64d5faab9a97ba7687; 41 tracked files and clean before Co's issue-7 initialization. | Preserve this baseline without copying its original .git directory. Issue-7 implementation must later be captured at its actual build revision. |
| Active storage source | Recheck: feature/6-mybrain-storage-foundation at 3fb5b348e34bde8fb727ab660cf5bb508898d62d; 51 tracked files, no tracked/untracked changes, identical HEAD before/after observation; integrated baseline is its merge base. Initial intake was 71a1a6c699deb5c2bb549b6aab809f2910ccadf0 with 50 files. | The donor added its design artifact and phase fact independently. Preserve the later public-safe research/design/architecture source; do not substitute the intake revision or call this implemented storage functionality. Capture immutably without checkout/reset/merge or stopping its writer. |
| Harness/runtime | PGMCP 4.0.0 requires Python >=3.15; workspace Python is CPython 3.15.0 x64. Its local interpreter subtree includes venv support and LICENSE.txt. | Python version/architecture are real compatibility constraints. A copied venv is not a portable installation; runtime redistributability/completeness still needs package verification. |
| Original harness artifact | phase_gate_mcp-4.0.0-py3-none-any.whl exists; 763216 bytes; SHA-256 dc9d86ce846fc507cf9bfe04ddbe9e75a101b3e6daa970941df7d0b0a16402b1 matches installed distribution provenance; ZIP CRC clean; license files and bootstrap present, 144 template-suite entries. | Bundle the known distribution rather than assuming a public package index reproduces this build. Initialize fresh server assets from it. |
| Portable/deployed parity | All ten agent sources equal effective copies; checks/tests/fixes/contracts overrides also match. Installed wheel lists 226 asset files. | Existing reviewed sources and packaged defaults are reusable; do not distribute the live server-data tree wholesale. |
| Local source candidates | Besides clean Git working states, read-only inspection found six primary and four donor setup-code candidates outside tracked source; their contents were not admitted or copied. | Review relevance/privacy and preserve only screened source-only progress or regenerate target-local setup; absence from Git is not automatic permission to include it. |
| Dependency closure | Current harness lock has 44 requirement lines: 43 exact version pins and one direct HTTPS requirement; no --hash entries. Quality additions are separately pinned. Complete third-party wheelhouse is not present in the inspected download areas. | Derive a portable, hash-pinned combined dependency closure; verify every Windows/Python ABI artifact. A source-host lock plus one wheel is not proof of an offline-capable payload. |
| Native quality | check-jsonschema 0.38.2, jsonschema 4.26.0, orjson 3.13.0, ruamel.yaml 0.18.16 and regress 2026.9.1 installed. Lychee 0.24.2 Windows archive matches SHA-256 32975d1493ee1a975d6bb41e4fb56fe419cb442ded628bb772ba2e614acfacad. | Preserve the reviewed pins/policy. Several installed native wheels use cp315/win_amd64 tags; runtime ABI compatibility matters. |
| Binding | Existing primary connection's interpreter, CWD, workspace root and server root match the assigned checkout; no GitHub token is embedded in that connection's env table. | Render new target-local bindings and PATH instead of copying source-host registration. This observation is not a blanket credential audit. |
| History/runtime boundary | Corrected selected-history filename screening found zero non-public-research path signals: two initial matches were allowed public-directory tree entries. No private blob content was opened. Live server logs/temp, environments, downloads and host configuration exist. | Filename screening does not certify all blob/metadata/ref history. Co selected snapshots without ancestry; no actual private-history finding is asserted. Live runtime remains excluded. |

### Transfer and compatibility options

| Boundary | Option | Cost/risk and consumer impact | Research recommendation / status |
| --- | --- | --- | --- |
| Source history | Screened file snapshots at named original SHAs, imported into a fresh standalone Git repository. | Loses original ancestry; preserve original branch/SHA/cutoff facts in the manifest. Avoids shipping old objects, reflogs, linked-worktree pointers and private recovery refs. | Selected by Co under the owner deployment mandate; preserve separately recoverable integrated/deployment and active-storage source snapshots without silent merging. |
| Source history | Audit and transfer selected full Git histories/bundle. | Preserves ancestry but requires complete blob/ref/metadata review, including history not visible in the current checkout. --all would widen exposure. | Not selected for this transfer. No full blob/ref/metadata history audit has been performed. |
| Dependency availability | Bundle a reviewed runtime plus a complete hash-pinned wheelhouse and native archive. | Larger ZIP and redistribution/license accounting; can reduce network needs after genuine closure/extraction verification. | Co-selected normal path, subject to actual artifact/license verification and installation from the packaged closure. |
| Dependency availability | Hybrid payload with pinned, verified downloads for missing runtime/dependencies. | Smaller package, but network/proxy/release availability becomes a real setup prerequisite. Must never claim fully offline installation. | Co-approved fallback only for specifically unavailable/non-redistributable items: enumerate pinned, checksum-verified primary-source downloads and disclose hybrid/online status. |
| Target compatibility/recovery | Create/rebuild only within a chosen destination and preserve existing files/customizations on rerun. | Requires explicit conflict and interrupted-run behavior. A matching prior stage can be reused only after verification; foreign/mismatched files cannot be silently overwritten. | Preserves the owner's non-destructive recreation boundary; detailed contracts belong in Design. |
| Host activation/authentication | Generate target-local registration, then verify activation through the actual host connection; obtain target-host login/credentials separately. | Host trust, policy, UI/version behavior and login can require owner action. A config file or process restart alone does not prove activation. | Required boundary; no account-cache/token transfer. See official and packaged bootstrap references. |

### Blast radius and verification expectations

Likely affected source surfaces are maintained deployment tooling under setup, dependency manifests/locks, target-local generated PGMCP/Codex consumers, package inventory/integrity data, deployment documentation and short agent handover. Existing package defaults, role authority, native quality policy and active storage implementation are preserved. No installed package source patch is justified by the evidence.

Meaningful later verification must cover archive construction and independent extraction, manifest/file hashes, source revision reconciliation and exclusions, Python/native compatibility, fresh target provisioning, native PGMCP operations, target path spaces, rerun/interruption/conflict recovery, and activation through the actual target-bound connection. Negative cases should include corrupt/missing payload, unsafe archive paths/link escapes, unavailable pinned dependencies and attempted modification of unrelated existing work. Test helpers/fixtures must be synthetic; no live database or mail content is needed.

Successful local extraction/provisioning is not clean-second-PC or VM evidence. Report that limitation, account actions and network needs precisely. This research ran no installation, extraction, bootstrap idempotence or clean-machine test.

### Packaging evidence and rollback boundary

The final artifact needs an inclusion/exclusion manifest with relative payload paths, versions/licenses/provenance, source snapshot and cutoff facts, byte counts and SHA-256 values, plus an independently reported outer ZIP checksum. Its checksum set must avoid a self-referential manifest hash. Extraction must reject paths escaping the target and unreviewed links; only a fully verified intended payload may be admitted. Recovery must preserve pre-existing work and avoid touching unrelated services, database data, host account settings or other worktrees.

Original SHA facts preserve source provenance when snapshots are imported into new Git history; they must not be misrepresented as the new repository's commit IDs. Preserve selected original source/local differences exactly and recoverably, with base/delta/cutoff facts; losing ancestry is explicit. Original public-safe workflow or QA facts are historical provenance and do not become current approval for a newly imported snapshot identity. Keep the target bootstrap free of fabricated active issue authority. Any later source capture must check for new committed or uncommitted progress and rescreen it without taking over the active writer. Existing private runtime, source-selection/resumption manifests, credentials, host settings and logs are explicit exclusions rather than backup candidates. Co explicitly forbids automatic force-push, origin-branch replacement, history rewrite or silent reconciliation of the new ancestry. Later development must either retain the standalone import without publication or use a separately authenticated authoritative remote/base and a new branch with reviewed deltas/conflict checks under owner-authorized reconciliation.

## Questions

- Which exact third-party/runtime artifacts pass redistribution review and complete a verified Windows x64 Python 3.15 closure? Apply the approved narrow online fallback only to any enumerated gap.
- Which local setup-code candidates are relevant safe source progress, and which must be excluded or regenerated as target-local configuration?
- What actual extraction/provisioning/rerun/activation evidence can be demonstrated locally, and what must remain an explicit second-PC/host-login/network limitation?

## References

- [Official Codex MCP configuration and activation](<https://learn.chatgpt.com/docs/extend/mcp>)
- [Official trusted project configuration](<https://learn.chatgpt.com/docs/config-file/config-basic>)
- [Official target-host authentication and credential boundaries](<https://learn.chatgpt.com/docs/auth>)

## Approved Strategy

| Boundary | Approved policy and provenance | Rationale / remaining evidence |
| --- | --- | --- |
| Transfer/privacy | Direct owner request and scope answer: real downloadable workspace/tooling/setup ZIP; exclude all existing private operational data. Repository privacy rules remain binding. No private export, encrypted backup or account-cache transfer. | Preserve setup/source value without migrating private runtime. Scope is settled. |
| Source/history | Co selected screened versioned source snapshots restored into a new standalone Git repository. Preserve original branch/SHA/cutoff and screened uncommitted source provenance. Keep integrated/deployment and active storage-source snapshots recoverable separately. No ancestry, raw .git, reflogs, backup refs, unreviewed bundle refs or silent merge; do not interrupt the donor writer. | Bounded current-source portability is needed; a complete history-content/ref/metadata audit is not performed. The two initial filename matches were public-directory false positives; corrected signal count is zero, so no actual private-history leak is claimed. Original SHA facts differ from newly imported commit identities. |
| Dependencies/runtime | Co selected bundled verified CPython/runtime, the known harness wheel, a complete hash-pinned wheelhouse and Lychee archive, subject to license/redistribution verification. Exercise actual installation from packaged artifacts. | Recreate compatible tooling without copying a venv, global host installs or patched package sources. Runtime/ABI and artifact closure require direct proof. |
| Narrow online fallback | Co permits specifically enumerated pinned, checksum-verified primary-source downloads only when an item cannot lawfully or actually be bundled. Mark the package hybrid/online and expose network prerequisites. | Continue within the approved mandate rather than inventing a new scope approval gate. No full-offline claim without evidence. |
| Target/recovery | Owner-mandated issue outcome and Co assignment: Windows x64, configurable non-destructive local recreation, preserving existing work and the independent storage worktree. | Concrete conflict/resume contracts belong in Design; unrelated services/data/host settings remain untouched. |
| Host/authority/evidence | Generate target-local consumers, preserve role/native-quality contracts and keep bootstrap distinct from issue initialization. Target-host credentials, login, project trust and actual MCP activation remain host actions outside the payload. Build/extract/verify the actual ZIP and disclose missing second-PC/VM evidence. No push/PR/merge authority is added. | Config files or health alone are not functional proof. Required original scope decisions are settled; independent phase review still precedes Design. |

These are owner privacy/outcome boundaries plus Co-approved technical choices under the original deployment mandate, not fabricated verbatim owner statements. Remaining unknowns are execution evidence within that envelope, not reopened scope decisions.

Co also clarified the technical setup/build authority: executable host-format bootstrap/build outputs may use the explicitly authorized technical route when no admitted scaffold family represents that format. Do not disguise PowerShell as Markdown/Python or create a new approval gate. Existing applicable Markdown/YAML/schema checks remain required; unrelated deferred application bindings are unchanged. Deployment-script verification must be scoped to actual syntax, synthetic package behavior, containment, dependency installation and repeatable recovery rather than fabricated application-test readiness.

## Expected Results

| Observable result | Acceptance evidence |
| --- | --- |
| A real ZIP can be handed to a local target agent. | Actual artifact path, outer checksum, relative manifest and concise handover exist; extracted bytes match the manifest. |
| Relevant source progress survives without private-history/runtime leakage. | Explicit included original SHAs and final cutoff; screened content; standalone usable target Git repository; disclosed snapshot/ancestry limitations and omissions. |
| A supported target path, including spaces, recreates tooling. | Compatible Python/runtime and pinned dependencies provisioned; fresh PGMCP assets and reviewed consumer parity; actual target-bound native operations succeed. |
| Reruns/recovery preserve work. | Verified idempotence, controlled interruption/resume and conflicting-existing-target cases; no unrelated services/worktrees/data altered. |
| Boundaries remain truthful. | Exclusion checks, independent archive inspection, recorded network/manual-login/activation needs and explicit absence of second-PC/VM evidence where not performed. |

These are behavioral success criteria, not completed results or an implementation sequence.

## Evidence

### Integrated and active-worktree source facts were read without taking over a writer.

At initial intake, primary main was 84d5e0c (41 tracked files, clean); active feature/6 was 71a1a6c (50 tracked files, no pending changes). Read-only source recheck at 2026-10-28T10:14:43Z found donor 3fb5b348e34bde8fb727ab660cf5bb508898d62d (51 tracked files, clean, unchanged HEAD across inspection), including its independently added design source. Integrated main remains their merge base. Co initialized feature/7 from that same integrated revision; expected state/deliverables initialization is not unexplained drift.

- [Repository Git and privacy agreements](<../../../README.md>)

**Invocation:** git --no-optional-locks worktree list --porcelain; per-worktree read-only status --porcelain=v1 --untracked-files=all; ls-files; merge-base; no root-bound PGMCP operation was used on the other worktree.

**Observed Result:** Two immutable source identities and clean-source observations; no claim that a later final build cutoff is already frozen.

**Observed At:** 2026-10-28T10:05:25Z

### A redistributable candidate for the pinned harness exists locally and includes setup assets.

Wheel 4.0.0 is 763216 bytes, CRC clean, with SHA-256 dc9d86ce846fc507cf9bfe04ddbe9e75a101b3e6daa970941df7d0b0a16402b1 matching installed provenance. Python requirement >=3.15; wheel bootstrap/templates and two license entries observed. License terms still govern redistribution.

- [Harness dependency baseline](<../../../requirements-pgmcp.lock.txt>)
- [Portable deployment map](<../../../setup/pgmcp/README.md>)

**Invocation:** Workspace Python -B: importlib.metadata distribution/read_text metadata; zipfile read/testzip; one explicit SHA-256 identity check of the harness wheel; runtime venv/license presence inspection.

**Observed Result:** Original harness candidate available; a complete third-party dependency closure and target installation remain unproved.

**Observed At:** 2026-10-28T10:05:25Z

### Portable maintained sources match current deployed consumers.

All ten generic agent sources and four quality/contracts override pairs compare equal. Reviewed quality manifest pins and Lychee archive hash are available.

- [PGMCP source/deployment map](<../../../setup/pgmcp/README.md>)
- [Quality deployment sources](<../../../setup/quality/README.md>)
- [Native dependency manifest](<../../../setup/quality/dependencies.yaml>)

**Invocation:** Read-only byte comparison of setup/pgmcp/agents against effective copies and setup quality/contracts overrides; inspect native package metadata; explicit Lychee archive SHA-256 comparison.

**Observed Result:** Reusable source-consumer baseline; no activation/native quality readiness inferred for a different PC.

**Observed At:** 2026-10-28T10:05:25Z

### A raw history transfer is not certified by current-source allowlisting.

Corrected filename-only enumeration of selected source histories found zero non-public-research path signals. Two initial matches were public directory-tree entries and were disconfirmed. No corresponding private blob contents, database or mail content were opened; a complete history-content/ref/metadata audit was not performed.

- [Publication and complete-history boundary](<../../../README.md>)

**Invocation:** git --no-optional-locks rev-list --objects for the selected source SHAs; classify path categories without publishing their names or opening private evidence.

**Observed Result:** Co selected screened snapshot transfer without ancestry; filename-only screening is not claimed as comprehensive history certification, and no actual private-history leak is alleged.

**Observed At:** 2026-10-28T10:05:25Z

## Consumers

### Target local agent

Run the approved package bootstrap and inspect local instructions.

**Impact:** Needs a short start instruction, deterministic supported target behavior, original source provenance and concrete stop conditions.

### PGMCP/Codex role contexts

Use the assigned target-local named binding and current protocols.

**Impact:** Need regenerated paths/PATH, templates/schema assets, consumer parity and actual per-connection activation; source-host task IDs are excluded.

### Existing storage worktree

Continue its separately authorized source work.

**Impact:** Read-only revision capture only; packaging cannot reset, commit for, stop, silently merge or include its private runtime.

### Independent QA

Verify phase artifacts and final actual archive.

**Impact:** Requires exact review revisions, reproducible synthetic package tests, source/cutoff facts and truthful unavailable/manual/online outcomes.

## Risks

### Copying linked worktree metadata or full Git history exposes unrelated history or produces a broken target repository.

Select a screened snapshot transfer or prove an explicitly bounded history audit; recreate standalone repository identity and preserve original SHA facts separately.

**Consequence:** Privacy breach, missing relevant work or unusable checkout.

### Copied venv paths, an unhashed/incomplete dependency set or incompatible native ABI causes target installation failure.

Preserve supported Python/native pins, inspect redistribution terms and complete the declared distribution closure; recreate environments and test from the actual extracted ZIP.

**Consequence:** Setup depends on the source PC or unexpected network/build tools.

### A rerun or unsafe archive path overwrites unrelated work or escapes the configured target.

Define non-destructive conflict/recovery behavior and extraction containment; test synthetic malicious/corrupt payloads and existing-target cases.

**Consequence:** Data loss or unauthorized host mutation.

### Source changes while packaging make a supposedly current transfer inconsistent.

Capture fixed Git revisions, detect changed source-only working state before/after any later patch capture and disclose the actual final cutoff; never lock or take over the other writer.

**Consequence:** Relevant progress is lost or manifest claims are false.

### Host trust/login/reload is mistaken for an automatic package capability.

Generate only target-local portable consumers and verify actual connection activation; explicitly surface irreducible host/account actions and avoid copying credentials.

**Consequence:** Tools are unavailable or bound to the wrong workspace despite apparent setup success.

## Assumptions

- The target is Windows x64; other operating systems/architectures are outside this issue.
- The package may require documented target-host software trust, authentication and network access unless full offline closure is actually demonstrated.
- The private source location and content of existing runtime stores are irrelevant to building the allowed source/tooling package and are not enumerated here.
- No tests or install claims in this research imply a completed ZIP or independent approval.

## Related Documents

- [Repository and current quality policy](<../../../README.md>)
- [Portable PGMCP deployment sources](<../../../setup/pgmcp/README.md>)
- [Quality toolchain deployment](<../../../setup/quality/README.md>)
- [Issue 7 acceptance contract](<https://github.com/MikeyVK/MyBrain/issues/7>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-28 | @imp researcher | Record read-only deployment inventory, public-safe source cutoff, compatibility/privacy boundaries, strategy options and expected results for issue 7. |
