<!-- pgmcp:v1 id=planning pv=1.0.0 pf=OSfLTQ1qMuWvM9fi sf=WI5iXHBKVOU91bYE -->

# Issue 1 documentation plan

**Status:** PLAN — owner-directed documentation execution  
**Version:** 1.0  
**Last Updated:** 2026-10-21

## Purpose

Reconcile PGMCP collaboration instructions with the owner's coordinator-led autonomous execution model.

## Scope In

Documentation and instruction configuration for issue 1, including portable source distribution and local derived role deployment.

## Scope Out

Application code/tests, server/harness implementation, launching actual multi-worktree product execution, blanket public deployment/merge authority, changing native quality policy.

## Prerequisites

- Owner-approved dedicated PGMCP server instance per worktree and at most one active mutating Imp per worktree.
- Owner direction that Co coordinates and delegates installation to Imp.
- Existing Qa chat independently appointed by the owner for substantive phase-boundary review.

## Summary

Implement shared policy plus portable/deployed consumer synchronization, then obtain independent review from the owner's existing MyBrain Qa chat. The owner authorized writing these instructions and requesting that review; this does not start a product-development run.

## Risks

### Instructions could imply new technical enforcement or permission grants.

State process-only enforcement limits, inherited permissions and explicit mandate provenance; QA checks negative scenarios.

### Ignored runtime source edits could disappear or drift.

Version portable generic sources and phase overrides, deploy exact copies and check parity.

## Work Units

### P1 — Shared policy and source ownership

**Goal:** Define the approved interaction, authority and isolation boundaries without implementing a server scheduler.

#### Deliverables

##### P1.1

Portable shared sources in setup/pgmcp/agents, including collaboration.md, with exact deployed .pgmcp/agents copies.

**Owner:** Imp

#### Exit Criteria

Explicit owner mandate, independent QA identity, revision-bound verdicts, dedicated server per worktree and one mutating Imp per worktree are coherent.

#### Verification

##### Preserve hard owner constraints and avoid invented enforcement.

**Method:** Source comparison and documented assignment/review scenarios.

**Expected Result:** Procedural requirements are distinguished from unimplemented runtime enforcement.

### P2 — Role, skill and phase instruction reconciliation

**Goal:** Remove contradictory manual-transfer requirements while retaining interactive operation and current non-production role boundaries.

#### Deliverables

##### P2.1

Three roles, five procedures, nine skills and complete affected phase instruction overrides reference the shared collaboration policy.

**Owner:** Imp

#### Exit Criteria

Co coordinates and delegates installation; Imp owns technical work; owner-appointed or properly mandated independent QA gives GO/NOGO; no blanket merge/publication authority.

#### Dependencies

- P1

#### Verification

##### Align active phase instructions with updated roles.

**Method:** Deploy reviewed contracts override, restart and inspect get_work_context.

**Expected Result:** Runtime phase instructions carry the explicit coordinated-mode interpretation.

### P3 — Codex mapping and deployed consumer consistency

**Goal:** Document actual tool contracts and deployment constraints, preserving machine-specific details locally.

#### Deliverables

##### P3.1

setup/pgmcp/README.md and codex-roles.yaml, reconciled local .codex/agents copies, README/AGENTS references and checked source parity.

**Owner:** Imp

#### Exit Criteria

Explicit chat/message authorization provenance, no assumed per-worktree routing, no hidden permission expansion, and repeatable Imp-owned deployment route.

#### Dependencies

- P2

#### Verification

##### Keep portable sources and local deployment aligned.

**Method:** Exact text comparison of generic sources, resolved config inspection, local role instruction comparison.

**Expected Result:** No stale human-only QA or unconfigured-quality claim remains in active consumers.

### P4 — Evidence and existing independent QA

**Goal:** Review realistic handoffs and ask the owner's existing Qa chat for an independent Documentation-to-Ready verdict.

#### Deliverables

##### P4.1

Review-exercises.md with observed document-walkthrough outcomes and limitations; committed revision handed to the existing MyBrain Qa chat.

**Owner:** Imp

#### Exit Criteria

Markdown/YAML checks appropriate to changed files pass; QA examines direct sources and returns findings and explicit GO/NOGO; any corrections use a new committed revision.

#### Dependencies

- P3

#### Verification

##### Cover intended collaboration behavior.

**Method:** Document walkthrough of assignment/review, NOGO/correction, owner boundary, interruption/resumption, unavailable capability, stale verdict, wrong server and competing writer.

**Expected Result:** No fake live orchestration or technical lock claim; runtime provisioning remains explicitly unproven.

## Related Documents

- [Research notes and owner constraints](<research-notes.md>)
- [Issue 1](<https://github.com/MikeyVK/MyBrain/issues/1>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-21 | @imp planner | Plan source, role, skill, phase and Codex deployment reconciliation and independent review. |
