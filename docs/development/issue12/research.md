<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# e-Boekhouden documentation-first connection research

**Status:** RESEARCH IN PROGRESS — strategy and live proof pending  
**Version:** 1.1
**Last Updated:** 2026-10-30

## Purpose

Establish the public API evidence needed for the owner's immediate supplier-invoice and bank-processing work through Codex or scripts.

## Scope In

Official public API documentation discovery, the separately assessed unofficial App API v4, and capability analysis, with detailed attention to creating versus editing mutations, received invoices, imported bank rows, matching, attachments and quarterly-review data.

## Scope Out

No live administration access, credentials, bookkeeping writes, actual invoice extraction, tax calculations/filing, connector implementation, MyBrain storage redesign or Research phase closure.

## Problem Statement

The owner needs to register received supplier invoices and work through already imported bank transactions before a quarterly return. Fast automation depends on distinguishing new bookkeeping entries from editing existing entries and consuming the bank worklist.

## Goals

- Index the discovered official REST and SOAP documentation and every declared business resource group.
- Identify the exact supported operations and gaps for the priority workflow, without inferring API capabilities from the UI.
- Present the smallest plausible automation routes and unresolved decisions, without implementing or claiming a connection.

## Background

Issue 12 was initialized independently from the storage-design work on the repository integration base. The owner now prioritizes mutation creation/editing and linking received invoices to all imported bank rows. The selected work is documentation-first research, not permission to alter financial records.

## Findings

### Current evidence boundary

The [API catalogue](api-catalog.md) inventories every declared REST business operation in the retrieved v1 specification: 39 operations on 24 business paths, plus two Swagger GET routes. It also covers both SOAP 5.7 manuals, the 20-operation live WSDL and its inline XSD, and official user-workflow documentation. Source retrieval was on 2026-10-30. It does not certify private documentation, current account entitlements or undocumented operations. The [App API v4 assessment](app-api-v4-assessment.md) separately examines 34 inferred operations from a pinned community repository. It provides attachment-linking and mutation-editing candidates but no proven bank-processing operation. These are not vendor-supported REST v1 extensions. The official iOS listing advertises unprocessed-bank-row management, so the missing processing route is a gap in the incomplete community evidence, not proof that the app lacks the function.

The owner excludes SOAP from the intended integration. Its documentation is retained as historical evidence only, not a fallback. The owner's report of a 2025 phase-out has not been independently established from a vendor announcement.

### Priority workflow: four distinct actions

| Action | What the inspected contract establishes | What remains unproved |
| --- | --- | --- |
| Register a supplier invoice | REST create mutation type 1 | Correct supplier, ledger, VAT and period choices for the owner's documents |
| Record a supplier invoice payment | REST type 4 accepts invoice-number/relation association on rows | Whether that consumes an already imported bank row — no such public contract was found |
| Correct an existing mutation | Official user manual describes UI editing | Official REST v1 declares no update/delete. Unofficial App v4 PUT is an editing candidate with unresolved identity and validation semantics; counterentries are not an equivalent edit |
| Reprocess the bank worklist | Manual section 1.4.3 describes reprocessing after later invoice entry | Current UI, match results and the broader impact on other pending rows require an authorized live check |

The owner clarified that all bank rows imported through the bank connection are relevant, not only incoming money. This includes supplier payments. Creating a payment mutation independently is not a safe substitute for processing an existing bank row: it could duplicate a payment or leave the queue item unprocessed.

### Minimal-route options, not an implementation design

| Route | Reuse / value | Limitation and consumer impact |
| --- | --- | --- |
| REST scripts or a thin agent interface | Documented structured reads, new invoice/mutation creation and reference lookups; usable from scripts and potentially Codex tools | Does not add undeclared mutation edits, bank-worklist processing or incoming archive uploads |
| API plus the documented UI worklist | Could register supplier invoices through the API, then use the existing reprocessing/manual screens for already imported bank rows and correction/attachment gaps | A proposal only. The all-rows command can affect other pending rows; verify the actual screen and review scope/results before any live action |
| App API v4 supplement | Inferred upload/link routes and PUT mutation request may fill two REST v1 gaps | Unsupported interface, incomplete schemas and authentication/ID uncertainties; bank processing still unproved. No acceptance or live proof |
| Historical SOAP | Documentation remains indexed for provenance | Excluded by owner; not an integration option or fallback |
| Reuse an existing connector | May reduce integration effort if its actual operations and maintenance fit | Not yet audited in this documentation-first checkpoint. A wrapper cannot establish vendor capabilities merely by naming tools |
| Build a general automation platform | Could orchestrate multiple services | No evidenced need for this larger scope; it would delay the owner's immediate use case |

A recommendation can favor the small hybrid option for a later proof, but no route has been accepted or implemented. The same interface-specific restrictions apply whether a request originates in a script or an agent tool.

### Interface and data questions affecting automation

- REST uses API-token-to-session exchange; the Authorization prefix is inconsistent between vendor prose and security-scheme description. Validate it through a future read-only proof rather than selecting a claim from examples.
- API ledger IDs differ from displayed ledger codes. Purchase rows, payment rows and generated invoice-module objects have different contracts.
- Outstanding-invoice responses recommend mutationId/relationId while payment input still names invoiceNumber. Preserve the actual current contract; do not invent a migration field.
- Structured duplicate errors and optional payment-reference uniqueness are documented. Generic idempotency, queue consumption, transactional multi-step writes and a fixed REST rate limit were not established.
- The public user manual documents archive-file linkage and mutation edits in the UI; official REST v1 does not. App v4 has separately graded inferred candidates, not current-runtime guarantees. Its layout is not a live version guarantee.
- Mutations and VAT totals can support review, but no public VAT-return report or filing endpoint was found. The exact quarter, accounting treatment and final return checks are owner/accounting decisions outside this documentation inventory.

### Proportional blast radius

This checkpoint changes only the three issue-12 research/reference documents and its initialized workflow records. Existing MyBrain storage design, deployment code, quality policy, templates and agent protocols remain unchanged. No new application stack, service, database, credentials, accounting records or connector registration was introduced. Future downstream consumers are the owner using Codex, scripts using the vendor contract, and any selected minimal connector; all require the same operation-level distinctions.

## Questions

- Which minimal route should be adopted after the owner reviews the documented API/UI boundaries?
- Which concrete existing mutation fields need editing, and which pending bank rows or invoice exceptions are the first bounded use case?
- Which current administration permissions, token constraints and API entitlements are actually available?
- Can the documented reprocessing action safely serve the immediate workflow in the current UI, including unmatched/partial/batch payments and unrelated pending rows?
- Which existing open-source connector, if any, fits the proven subset without excessive infrastructure?

## References

- [Detailed official API catalogue](<api-catalog.md>)
- [Unofficial App API v4 assessment](<app-api-v4-assessment.md>)
- [Official REST documentation](<https://api.e-boekhouden.nl/scalar/>)
- [Official raw REST contract](<https://api.e-boekhouden.nl/openapi/v1.json>)
- [Official SOAP manual](<https://cdn.e-boekhouden.nl/handleiding/Documentatie_soap.pdf>)
- [Official bookkeeping manual](<https://cdn.e-boekhouden.nl/handleiding/Handleiding_boekhoudpakket.pdf>)

## Approved Strategy

PENDING — the owner has authorized documentation discovery and prioritized the workflow, but has not selected an API-only, hybrid UI/API, unofficial App API or connector strategy. SOAP is excluded by owner. Preserve existing vendor contracts and current administration data during research. No migration, accounting-correction policy, live write scope or Design transition is approved by this checkpoint.

## Expected Results

A reader can find the official documents, distinguish the 39 REST operations and 20 SOAP operations, identify the supplier-invoice creation contract and understand the official REST v1 gaps, the unofficial App API attachment/edit candidates, and why imported-bank-row processing remains unproved. A later bounded proof must establish the actual authentication spelling and read access first, then validate the selected workflow with explicit scope and synthetic or otherwise owner-authorized data. Evidence must distinguish bookkeeping outcomes from queue status and prevent duplicate payment creation; this document does not sequence that implementation.

## Consumers

### Owner in Codex

Request narrowly scoped accounting work and review proposed changes

**Impact:** Needs clear read/create/edit/process distinctions rather than a generic unrestricted API promise.

### Automation scripts

Use documented API operations reproducibly

**Impact:** Must resolve actual IDs, handle session expiry and duplicates, and avoid treating new payment records as bank-worklist consumption.

### Any selected connector

Expose the proven vendor capability subset

**Impact:** Cannot invent missing edit, attachment or bank-queue contracts; selection and implementation remain future work.

## Risks

### Duplicate financial effects from retries or recording a new payment while the imported bank row already exists.

Keep the bank-worklist gap explicit; require later verification of existing entries, operation semantics and results rather than blind POST retry.

### UI reprocessing affects more pending rows than the intended invoice set.

Treat the manual action as a proposal and verify current screen, affected scope and outcomes before an owner-authorized live use.

### A generic connector or generated client hides schema/prose differences and unsupported actions.

Compare its actual source/tool surface against the catalogue and prove the minimal read path before writes.

### Financial data or tokens leak into repository evidence.

No account access in this checkpoint; use public sources and generic summaries only, keep complete vendor downloads ignored, and keep future secrets/data outside Git and chat.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.1 | 2026-10-30 | Codex (@imp researcher) | Add pinned unofficial App API findings; scope REST gaps and mark SOAP historical/excluded. |
| 1.0 | 2026-10-30 | Codex (@imp researcher) | Record official API coverage and the documented creation/editing/bank-worklist boundaries for the owner's prioritized automation needs. |
