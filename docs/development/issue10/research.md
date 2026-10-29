<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Consolidation maintenance boundary

**Status:** REVIEW REQUESTED — consolidation boundary  
**Version:** 1.1  
**Last Updated:** 2026-10-29

## Purpose

Record the bounded source consolidation requested by the owner.

## Scope In

The 52 pinned files in the inventory, reconciliation of README additions, issue navigation and necessary documentation-link migration.

## Scope Out

Private inputs, credentials, operational data, source workflow state, new application logic, deployment, source issue closure or phase advancement, source branch rewriting and worktree removal.

## Problem Statement

Research, design and deployment work for issues 5–9 exists on separate branches while main lacks a coherent reference baseline.

## Goals

- Bring screened existing material together without changing application behavior.
- Keep source provenance, historical status and issue ownership explicit.

## Findings

### Frozen source-to-destination inventory

All rows refer to committed Git objects, not a moving checkout. Main baseline is `84d5e0cbbe488fd45160de64d5faab9a97ba7687`. The existing public PDF and issue 1/2 material remain unchanged. There are 52 imported source files; README additions are reconciled separately rather than replacing the integration entrypoint.

| Issue | Source commit | Source path | Destination |
| --- | --- | --- | --- |
| 6 | `8a80c184cacfc61cc665b4fe12adf757bac8e54f` | `docs/architecture/digital-brain-discussion-map.md` | `docs/architecture/digital-brain-discussion-map.md` |
| 5 | `c959d0e45cc4c8a92c67f34a70db38d3598045bb` | `docs/development/issue5/design.md` | `docs/development/issue5/design.md` |
| 5 | `c959d0e45cc4c8a92c67f34a70db38d3598045bb` | `docs/development/issue5/planning.md` | `docs/development/issue5/planning.md` |
| 5 | `c959d0e45cc4c8a92c67f34a70db38d3598045bb` | `docs/development/issue5/research.md` | `docs/development/issue5/research.md` |
| 6 | `8a80c184cacfc61cc665b4fe12adf757bac8e54f` | `docs/architecture/decisions/0001-digital-brain-foundational-principles.md` | `docs/architecture/decisions/0001-digital-brain-foundational-principles.md` |
| 6 | `8a80c184cacfc61cc665b4fe12adf757bac8e54f` | `docs/development/issue6/design.md` | `docs/development/issue6/design.md` |
| 6 | `8a80c184cacfc61cc665b4fe12adf757bac8e54f` | `docs/development/issue6/research.md` | `docs/development/issue6/research.md` |
| 6 | `8a80c184cacfc61cc665b4fe12adf757bac8e54f` | `docs/development/issue6/storage-acceptance.md` | `docs/development/issue6/storage-acceptance.md` |
| 6 | `8a80c184cacfc61cc665b4fe12adf757bac8e54f` | `docs/development/issue6/storage-model.md` | `docs/development/issue6/storage-model.md` |
| 6 | `8a80c184cacfc61cc665b4fe12adf757bac8e54f` | `docs/development/issue6/storage-operations.md` | `docs/development/issue6/storage-operations.md` |
| 6 | `8a80c184cacfc61cc665b4fe12adf757bac8e54f` | `docs/development/issue6/storage-preservation.md` | `docs/development/issue6/storage-preservation.md` |
| 6 | `8a80c184cacfc61cc665b4fe12adf757bac8e54f` | `docs/research/public/open-source-knowledge-core-candidates.md` | `docs/development/issue6/open-source-knowledge-core-candidates.md` |
| 6 | `8a80c184cacfc61cc665b4fe12adf757bac8e54f` | `docs/research/public/open-source-platform-candidates.md` | `docs/development/issue6/open-source-platform-candidates.md` |
| 9 | `8a80c184cacfc61cc665b4fe12adf757bac8e54f` | `docs/research/public/opencloud-admission-extension-feasibility.md` | `docs/development/issue9/opencloud-admission-extension-feasibility.md` |
| 6 | `8a80c184cacfc61cc665b4fe12adf757bac8e54f` | `docs/research/public/opencloud-wikibase-gap-analysis.md` | `docs/development/issue6/opencloud-wikibase-gap-analysis.md` |
| 6 | `8a80c184cacfc61cc665b4fe12adf757bac8e54f` | `docs/research/public/opencloud-wikibase-trial-design.md` | `docs/development/issue6/opencloud-wikibase-trial-design.md` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `docs/development/issue7/design.md` | `docs/development/issue7/design.md` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `docs/development/issue7/documentation.md` | `docs/development/issue7/documentation.md` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `docs/development/issue7/implementation-evidence.md` | `docs/development/issue7/implementation-evidence.md` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `docs/development/issue7/planning.md` | `docs/development/issue7/planning.md` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `docs/development/issue7/research.md` | `docs/development/issue7/research.md` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `docs/development/issue7/validation.md` | `docs/development/issue7/validation.md` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/Bootstrap.ps1` | `setup/deployment/Bootstrap.ps1` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/Build-Package.ps1` | `setup/deployment/Build-Package.ps1` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/Preflight.ps1` | `setup/deployment/Preflight.ps1` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/README.md` | `setup/deployment/README.md` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/Recover.ps1` | `setup/deployment/Recover.ps1` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/START-HERE.md` | `setup/deployment/START-HERE.md` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/Start-Deployment.ps1` | `setup/deployment/Start-Deployment.ps1` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/Test-Package.ps1` | `setup/deployment/Test-Package.ps1` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/Verify.ps1` | `setup/deployment/Verify.ps1` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/agent-handover.md` | `setup/deployment/agent-handover.md` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/builder.py` | `setup/deployment/builder.py` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/contracts.py` | `setup/deployment/contracts.py` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/deploy.py` | `setup/deployment/deploy.py` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/journal.py` | `setup/deployment/journal.py` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/manifest.schema.json` | `setup/deployment/manifest.schema.json` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/probe.py` | `setup/deployment/probe.py` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/provision.py` | `setup/deployment/provision.py` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/release_tests.py` | `setup/deployment/release_tests.py` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/sources.py` | `setup/deployment/sources.py` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/tests/Invoke-DeploymentTests.ps1` | `setup/deployment/tests/Invoke-DeploymentTests.ps1` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/tests/Invoke-PreflightFixture.ps1` | `setup/deployment/tests/Invoke-PreflightFixture.ps1` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/tests/Test-RuntimeAdmission.ps1` | `setup/deployment/tests/Test-RuntimeAdmission.ps1` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/tests/test_archive.py` | `setup/deployment/tests/test_archive.py` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/tests/test_contracts.py` | `setup/deployment/tests/test_contracts.py` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/tests/test_git_promotion.py` | `setup/deployment/tests/test_git_promotion.py` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/tests/test_journal.py` | `setup/deployment/tests/test_journal.py` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/tests/test_preflight.py` | `setup/deployment/tests/test_preflight.py` |
| 7 | `753258de98291e64dd7f73afdf2a74cf00623732` | `setup/deployment/tests/test_provisioning.py` | `setup/deployment/tests/test_provisioning.py` |
| 8 | `dc20ca462cffb54aff045bdf9cd579a04601274c` | `docs/development/issue8/api-catalog.md` | `docs/development/issue8/api-catalog.md` |
| 8 | `dc20ca462cffb54aff045bdf9cd579a04601274c` | `docs/development/issue8/research.md` | `docs/development/issue8/research.md` |

### Mechanical boundary

Deployment code, scripts, tests and support files remain byte-identical. Only documentation location, relative links, navigation and explicit consolidation provenance may change. Shared architectural records remain canonical. Moving material does not approve its content: issue 5 drafts, issue 6 review candidates, issue 8 unresolved strategy and issue 9 unexecuted experiments retain their own statuses. Issue 7 producer test evidence remains historical evidence, not a new package-build or clean-machine claim.

### Observed readiness

The dedicated binding returned issue 10/chore/Research on the assigned branch. Native git_status found only the two newly initialized consolidation workflow files before authoring. Read-only git ls-tree against each pinned SHA enumerated the table above. Source issue workflow state and deliverables are excluded. No source branch, worktree or service was changed.

## Approved Strategy

The owner explicitly requested consolidation on main into issue-owned documentation folders and confirmed inclusion of code and documents for issue 7. Co selected the mechanical boundary within that request:

| Boundary | Strategy | Compatibility / consequence |
| --- | --- | --- |
| Existing issue documents | Preserve content and status; relocate issue-specific reports to their owning issue folder | Update repository-relative links and navigation; retain exact source SHA in this inventory |
| Shared principles / discussion map | Preserve canonical architectural locations | Issue 6 links to these shared records; no duplicate divergent definitions |
| Deployment implementation | Preserve all 28 setup/deployment files byte-for-byte | Existing documented behavior and tests remain inherited, not reimplemented or newly runtime-certified |
| README | Combine issue 6 and issue 7 additions with development navigation | Preserve current working agreements and privacy/quality policies |
| Workflow state | Exclude original issue state; use only issue 10 lifecycle, neutralized through submit_pr | Original issues remain open at their actual phases |
| Publication | Reviewed consolidation PR to main | Preserve source refs; no force push, runtime change or deployment |

Stop and return to Co if behavioral code changes, missing source material, private content, competing writers or a new architectural decision become necessary.

## Expected Results

Every inventory row is present at its declared destination. A review of intentional documentation diffs accounts for location/link/provenance changes, while deployment bytes match their source. The development index exposes issues 5–9 and existing issue 2. Native offline Markdown links/fragments pass; the imported JSON Schema passes both configured schema checks. Any changed YAML needs its configured check and consumer admission. Validation executes repository_review once after final implementation changes and the configured test request; inactive tests are reported as unexecuted, never passing. Independent QA reviews each required boundary and the final exact revision before authorized main integration.

## Risks

### Blind merges import conflicting issue workflow state or stale README content.

Select explicit public paths from pinned Git objects; reconcile navigation separately and exclude original state.

### Relocation breaks links or upgrades historical claims by accident.

Compare content against source objects and execute native local-link checks; preserve historical approval status.

### Deployment source inclusion is mistaken for a fresh operational verification.

Preserve source bytes and identify original evidence as historical. Do not run packages or claim new live tests.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-29 | Codex (@imp researcher) | Record owner-authorized consolidation strategy and exact source-to-destination inventory. |
| 1.1 | 2026-10-29 | Codex (@imp researcher) | Correct inventory to 52 files by including the shared discussion map at its canonical path after independent review. |
