<!-- pgmcp:v1 id=design pv=1.0.0 pf=Uk1D2XWpiag1c6nn sf=WI5iXHBKVOU91bYE -->

# MyBrain storage foundation: initial design frame

**Status:** Draft — Design in progress  
**Version:** 1.0  
**Last Updated:** 2026-10-28

## Purpose

Provide the entry point for the owner's storage-design discussion after Research review. This is an incomplete draft, not an implementable final design, a Design approval or permission to begin Planning or deployment.

## Scope In

Logical registration and storage responsibilities; identities and versions; metadata definitions/applications; relationships and combined states; lifecycle/work views; basic storage operations and file/database consistency questions.

## Scope Out

Implementation steps or cycles, production code, physical schemas, runtime/library/model selection, live imports or migrations, deployment, semantic interpretation, user interfaces and consumer-specific processing/export behavior.

## Problem Statement

MyBrain needs one coherent registration and history model across database-resident content, files and mixed sources. Native file versions, database updates and mutable descriptions must not silently redefine source identity, historical evidence or the current view. The concrete contracts that deliver that coherence remain to be designed.

## Functional Requirements

- Keep source identity, content version, copy/representation and receipt distinguishable; preserve originals separately from derivatives and references.
- Version descriptions and coherent metadata sets without conflating recording, receipt or applicability, and retain definition/origin separately from assignment/assessment.
- Preserve actual historical combinations while allowing current views and reuse of unchanged components.
- Keep lifecycle metadata on the same registration before and after intake; staging selects work rather than defining another source authority.
- Support generic recording of produced context, computational descriptions and contracts without performing their interpretation, calculation or enforcement within storage.
- Protect sole-owner memory with global access first and optional bounded disclosure later; no planned multi-party per-entity rights.

## Nonfunctional Requirements

- Make integrity, completeness, availability and unknown outcomes distinguishable across directly stored content and references.
- Define concurrent-change and interrupted-operation behavior before claiming a consistent combined version or completed effect.
- Preserve owner-explicit destruction, recovery and revocation obligations without claiming already disclosed information can be recalled.
- Reuse existing components where they meet the accepted contracts; do not equate native features or a valid document scaffold with proven guarantees.

## Constraints

- The Approved Strategy in research.md governs this draft; materially new compatibility or migration decisions return to the owner.
- OpenCloud/PostgreSQL is the candidate boundary to assess. Exact storage roles, schemas, interfaces and integration mechanisms remain open.
- The earlier OpenCloud–Wikibase trial remains a separate proposal; its canonical-store, journal and runtime choices are not adopted.
- ADR 0001 and the discussion map remain at their accepted revision 1.12; this draft does not silently amend those principles.

## Decision

No new technical direction is selected in this entry draft. The accepted principles and reviewed Research strategy constrain the discussion; options, trade-offs and final contract decisions must be developed and reviewed before Design can be completed.

## Questions

- What is the smallest complete source-registration contract, and what evidence permits admission or identity matching?
- What exactly changes a content version, a description-set version and a recorded combined state?
- When does a relationship bind to continuing identity, to particular recorded values, or to a view resolved under a use contract?
- Which coherent metadata sets should be reusable, and how are definition changes separated from reassessing existing applications?
- What may each generic storage operation acknowledge after concurrent edits, partial failure or a lost response?
- How should OpenCloud/PostgreSQL responsibilities satisfy preservation and recovery without silently adopting the older trial?
- What bounded release and owner-authorized destruction contracts can be specified without adding third-party entity rights?

## Production Design

### Logical responsibility areas to resolve

These areas organize discussion; they are not chosen services, tables or a deployment topology.

| Area | Accepted responsibility | Concrete design decision still open |
| --- | --- | --- |
| Registration and identity | One continuing registration across lifecycle changes; separate identity from received exemplars and representations. | Minimal registration contract, recognition evidence and correction of identity mistakes. |
| Content and reference versions | Identify exact preserved content and mixed-source components; a pointer alone does not preserve its target. | Version boundaries, integrity scope and file/database ownership of retained material. |
| Descriptions and metadata | Reusable versioned sets, definitions/origins and distinct applications/assessments. | Set boundaries, reuse and how corrections/withdrawal retain historical interpretation. |
| Relationships and compositions | Distinguish identity links, particular used versions and changing current views. | Reference semantics, composition boundaries and what constitutes a new recorded combined state. |
| Lifecycle and working views | Lifecycle metadata stays with the source; staging selects registrations needing work. | Transition conditions, evidence of completed work and re-entry without re-registration. |
| Storage operations | Register, retain a version, record a description or relationship, retrieve a historical/current view, and expose progress are conceptual needs. | Inputs, effects, read/write separation, acknowledgment and error contracts; these are not API signatures. |
| Cross-store consistency | Partial success must not masquerade as a complete combined state. | Visibility/commit boundary, concurrent updates, uncertain outcomes, reconciliation and combined recovery. |

### Candidate boundary

OpenCloud may supply file working copies and retention capabilities; PostgreSQL may hold directly stored content and structured registrations. This draft does not assign final authority or physical layout. The design must show how references, preserved versions and mixed compositions remain coherent regardless of their location. Earlier native-version/event findings remain evidence limits, not an adopted acquisition protocol.

## Test Design

Not yet a complete test design. Before Design exit, define durable behavioral evidence for historical reconstruction after independent changes, interrupted mixed-source updates, repeated receipt, uncertain completeness/availability, and owner-authorized destruction/revocation. No application tests are introduced or claimed here; concrete seams, fixtures and expected outcomes remain to be designed.

## State and Failures

Open: distinguish attempted from confirmed effects, pending work from unknown outcome, and current applicability from historical registration. No fixed status catalog, transition engine, transaction protocol or retry policy is selected. The contract must expose incomplete cross-store work without inventing a complete captured version.

## Planning Consequences

Planning remains pending. This draft is a discussion frame only; options, selected contracts, interface definitions, failure/recovery guarantees and durable validation design still require elaboration and independent Design review. No implementation sequence or cycle plan is established.

## Sources

- [Reviewed Research and Approved Strategy](<research.md>)
- [Accepted foundational principles, revision 1.12](<../../architecture/decisions/0001-digital-brain-foundational-principles.md>)
- [Discussion map](<../../architecture/digital-brain-discussion-map.md>)
- [Dated OpenCloud–Wikibase gap evidence](<../../research/public/opencloud-wikibase-gap-analysis.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-28 | Codex (@imp designer) | Start the storage Design discussion from reviewed Research; record logical boundaries and unresolved contracts without selecting a technical implementation. |
