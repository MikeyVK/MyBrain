<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# MyBrain storage foundation: research consolidation

**Status:** Research consolidation — review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-28

## Purpose

Close the evidence index for the initial storage investigation without repeating the broad platform search or selecting a solution. The owner requested a dedicated PGMCP design lifecycle; this Research artifact records the inputs and strategy limits for that transition.

## Scope In

Accepted conceptual storage requirements; dated reusable research and its limits; repository separation from issue #5; compatibility and migration strategy boundaries; expected outcomes and unresolved questions for storage Design.

## Scope Out

Production implementation, schema or API design, implementation sequencing, live imports, real-data migration, deployment, runtime changes, model selection, semantic assessment and presentation/export applications. Those consumers remain in scope only for generic registration and storage-boundary needs.

## Problem Statement

The general MyBrain storage investigation outgrew the bounded email-ingestion trial in issue #5. Keeping new conceptual decisions under that trial would obscure authority and imply compatibility with an older proposed stack. A dedicated issue #6 must preserve the accepted baseline and earlier work while making the Research-to-Design boundary reviewable.

## Goals

- Carry the screened conceptual baseline and dated evidence into a main-based issue without claiming the earlier trial was completed.
- Preserve independent source and description histories, coherent metadata sets, lifecycle continuity and exclusive personal ownership.
- Identify precisely which reusable findings constrain Design and which earlier component choices remain proposals.
- Define reviewable storage-design outcomes without choosing schemas, libraries or runtime mechanisms.

## Background

The owner closed the initial conceptual research and requested Design under the maintained PGMCP process on 2026-10-28. ADR 0001 and the discussion map, revision 1.12 dated 2026-10-28, are the accepted baseline. The four comparison/gap/trial reports are dated 2026-10-24 and assessed revision 1.8; they retain that historical/proposal status. Their links point to maintained documents and must not be misread as immutable revision-1.8 snapshots. Later accepted principles govern any conflict.

Repository separation is a coordination implementation choice within the requested workflow housekeeping: issue #6 is initialized on feature/6-mybrain-storage-foundation with main as explicit parent. Issue #5 remains on its original branch with unfinished workflow preserved. No issue-5 phase deliverables were carried into this checkout. Local recovery material is deliberately outside the repository and is not a product or workflow artifact.

## Findings

### Evidence register and authority

| Input | Date and status | Reusable finding or requirement | Limit for this issue |
| --- | --- | --- | --- |
| [ADR 0001](../../architecture/decisions/0001-digital-brain-foundational-principles.md) and [discussion map](../../architecture/digital-brain-discussion-map.md) | Accepted principles / working agenda, revision 1.12, 2026-10-28 | Generic source registration, content/description independence, history, coherent metadata, same-registration lifecycle, staging view and exclusive owner control. | Accepted principles do not select physical schemas or demonstrate implementation. |
| [Platform comparison](open-source-platform-candidates.md) | Research assessment, 2026-10-24 | File synchronization, native use and extension interfaces are reusable; file services do not by themselves provide the full registration/history guarantees. | Recommendations are role-specific and not adoption; no current-version revalidation in this consolidation. |
| [Knowledge-core comparison](open-source-knowledge-core-candidates.md) | Research, 2026-10-24 | Definition/application separation, narrative authoring and historical stores offer reuse; audit history, validity and actual retained results are different guarantees. | Does not settle Wikibase's role or mandate a temporal engine. |
| [OpenCloud–Wikibase gap assessment](opencloud-wikibase-gap-analysis.md) | Research proposal, 2026-10-24 | Native file revision references, event signals and ETags are insufficient evidence of preserved MyBrain source versions; receipt, capture, registration and processing acknowledgments need distinct evidence. | Findings concern inspected versions and a provisional pair; earlier multi-party rights framing must be reconciled to P39. |
| [Earlier trial design](opencloud-wikibase-trial-design.md) | Proposed trial, 2026-10-24 | Synthetic capture, concurrent-change, historical-result, interruption and recovery scenarios are useful counterexamples. | Wikibase authority, SQLite journal, Python/FastAPI stack and trial topology are trial-only choices, not current architecture. No full trial execution is established by that document. |

### Consolidated storage boundary

- Preserve originals or explicitly described references; a retained reference does not establish target preservation, completeness or direct availability (P03, P31, P34).
- Enduring identities connect independently versioned source content, metadata, label definitions/applications and computational descriptions. Hash equality alone does not establish shared origin or identity (P20, P36).
- Version history is the basis. Metadata such as receipt, registration and validity may be versioned as coherent sets while retaining their distinct meanings; no specialized bitemporal or event-sourcing mechanism is required (P24, P37).
- Candidate and admitted information retain the same registration and lifecycle history. Staging is a working view, not a second authority; detailed common intake and lifecycle contracts remain to be designed (P18, P22, P35, P38).
- Historical combined states retain the actual versions/values used. Current views may use newer applicable information without rewriting those records. Unchanged components need not be fully copied (P36).
- Produced wiki context is itself a versioned source. Rich narrative meaning need not be forced into fields; extraction, assessment and vector calculation remain outside storage, while their inputs/results can be recorded (P26, P35, P37).
- The owner is the sole internal user. Global owner access precedes optional bounded disclosure; per-entity multi-party rights are not a planned phase. Existing scoped revocation requirements still apply to granted authority (P13, P30, P39).
- OpenCloud plus PostgreSQL is the current candidate direction to assess, not a completed proof or an approval of a database schema, library, runtime or model. Wikibase's future role remains deferred.

### Blast radius and consumers

This reconciliation changes documentation and branch-local workflow artifacts only. No application production code, tests, runtime settings, connector or data store is introduced. README gains only the existing screened document-index entries. Agent protocols, template packages, enforcement configuration and quality policy are consumed unchanged. Future storage Design consumes this baseline; knowledge processing, contextualization, presentation, export and external actions consume generic registration needs rather than becoming storage implementations. The development-harness language and environment do not select the application stack.

## Questions

- What logical registration and reference/version boundaries cover database records, file content and mixed compositions without full-copy cascades?
- What concrete common intake/lifecycle contracts distinguish observations, receipt, preserved material, registration, work remaining and unknown outcomes?
- Which metadata sets should evolve together, and how do contracts retain independent validity and historical interpretation?
- How can supported OpenCloud acquisition routes bind retained bytes to a precise version under concurrent edits, and what guarantees remain unknown?
- What is the least additional mechanism needed for preservation, coordinated file/database recovery and owner-explicit destruction?
- What bounded owner-delegated routes and release boundaries satisfy P30/P39 without a multi-party entity-rights model?

## References

- [Issue #6: Design the MyBrain storage foundation](<https://github.com/MikeyVK/MyBrain/issues/6>)
- [Foundational principles, current accepted baseline](<../../architecture/decisions/0001-digital-brain-foundational-principles.md>)
- [Discussion map](<../../architecture/digital-brain-discussion-map.md>)
- [Repository agreements and quality policy](<../../../README.md>)
- [Public research baseline](<../../research/public/research-baseline.pdf>)

## Approved Strategy

The following records owner-approved conceptual preservation and scope limits, supported by the accepted ADR and the explicit request to close initial research and enter Design. It does not authorize a live migration or approve a solution. Repository branch mechanics are Co's housekeeping choices, not quoted owner requirements.

| Boundary | Alternatives and impact | Approved strategy and authority |
| --- | --- | --- |
| Accepted meaning and history | Reinterpret earlier records under current definitions, reducing history cost but losing traceability; or preserve independent versions and historical basis, with additional storage/reconstruction obligations. | Preserve accepted distinctions and histories under P08, P20, P24, P36–P38. No silent reinterpretation or mandatory temporal engine. |
| Earlier trial and new lifecycle | Continue or rebase the new foundation onto issue #5, inheriting unrelated assumptions; or separate it from main and retain the trial independently. | Owner requested an appropriately scoped PGMCP design lifecycle. Co selected main-based issue #6 and preserved the unfinished trial; no change of trial scope or completion claim. |
| Existing runtime and production data | Migrate or replace live stores now, creating compatibility and rollback obligations; or preserve them while researching/designing only. | No operational migration or compatibility break is authorized. This issue's current assignment is documentation/Design entry only. Any actual migration requires a later explicit strategy decision. |
| Content, references and derivatives | Treat extracted text, a pointer or native revision URL as a replacement original; or distinguish retained bytes, references and derivatives with explicit guarantees. | Preserve original/derivative and direct/reference boundaries under P03/P34; establish concrete acquisition/version guarantees during Design before any implementation. |
| Candidate reuse | Adopt the old Wikibase/SQLite trial wholesale, carrying its model and runtime coupling; or assess file/database reuse against current principles. | Evaluate OpenCloud/PostgreSQL under the current issue scope; no implicit Wikibase, schema, library, model or specialized history-engine adoption. Reuse findings as evidence rather than inherited decisions. |
| Ownership and disclosure | Grow into multi-party entity rights, adding internal entitlements; or preserve sole-owner memory with bounded authorized disclosure routes. | P39 explicitly chooses global owner access first and optional bounded routes later. Entity-level rights require explicit owner reconsideration; no current rights migration or technology selection. |

No unsupported compatibility promise or required new breakage strategy was identified for this documentation-only consolidation. If Design uncovers a materially different migration or compatibility boundary, return it for an explicit decision before shaping that boundary.

## Expected Results

Forthcoming Design should provide a traceable, reviewable storage contract rather than merely select products:

- Map accepted requirements to source identities, independently versioned content/descriptions, reusable metadata sets, label definitions/applications, computational descriptions, generated context and stored contracts.
- Explain same-registration lifecycle and staging-view semantics, unknown completeness and availability, and historical combined states versus current views.
- Assess direct database content, file content and mixed compositions against exact acquisition, integrity, concurrent change and identifiable-version requirements.
- Define storage responsibility and failure/recovery guarantees, preserving explicit owner destruction and distinguishing attempted effects from confirmed outcomes.
- Evaluate OpenCloud/PostgreSQL reuse and remaining gaps without importing the older trial's authority or runtime decisions.
- Preserve sole-owner access and bounded disclosure semantics while leaving consumer processing, presentation and action execution outside storage.

These are Design acceptance expectations, not claims of implemented behavior or a sequence of implementation tasks.

## Risks

### Older reports can be mistaken for adopted architecture or current capability evidence.

Keep dated status and version limits explicit; current accepted principles govern and new choices belong to reviewed Design.

**Consequence:** Otherwise historical trial assumptions could silently determine the new storage model.

### Native revision links or successful event handling can be mistaken for durable captured source versions.

Require explicit acquisition, preservation and reconciliation guarantees in Design; retain synthetic counterexamples.

**Consequence:** History could refer to bytes that were not preserved or cannot be retrieved.

### Formal closure could be mistaken for product readiness or permission to migrate live data.

Stop at the Research review boundary; no runtime, import or migration effects are authorized here.

**Consequence:** Unproven guarantees could be presented as delivered behavior.

## Assumptions

- Accepted ADR revision 1.12 is authoritative for conceptual requirements; proposals in older reports remain evidence only.
- No broad new candidate search is needed to consolidate the existing initial research. Targeted unresolved evidence may be investigated during subsequent design decisions.
- First publication of this new issue branch still requires scoped owner authority; the earlier branch-maintenance permission named issue #5.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-28 | Codex (@imp researcher) | Consolidate the owner-closed initial storage research and accepted principles for independent Research review before Design; preserve earlier trial boundaries. |
