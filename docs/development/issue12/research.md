<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# e-Boekhouden documentation-first connection research

**Status:** OWNER-ACCEPTED APP-ONLY STRATEGY — endpoint Design review candidate  
**Version:** 1.5
**Last Updated:** 2026-11-01

## Current function-first research — 2026-11-01

- [Per-function REST/App/APK coverage](api-functional-coverage.md): all 57 generic functional groups with separate operation coverage, 23 configuration feature types, bounded gaps and concrete follow-ups. No private administration values are published.
- [Expanded APK contract catalogue](apk-api-contracts.md): all compiled mobile client groups, exact Production App-v4 binding and static method/path/DTO evidence. The APK is client evidence for App-v4, not a third independent API family.
- Following functional web and APK research, the owner accepted App API v4 as the uniform route on 2026-11-01. The [current endpoint design](design.md), [technical contracts](design-contracts.md) and [registry/admission catalogue](endpoint-design-catalogue.md) implement that strategy without bookkeeping logic. Earlier REST-default/workflow designs remain historical. Missing function contracts remain unavailable, not locally invented accounting logic.
- Consolidation received independent GO at `68bafa6750e64b99cc758f30377fa648566080eb`; the previous Design received independent GO at `1d2fc8da06ac41c49134e5ee1bc67e1a347413b5`. Those verdicts cover their exact earlier scope/revisions, not this reopened strategy.
- Current work is static/public-source research and screened documentation. No APK execution, current account/API/credential operation, implementation or phase transition occurs.

## Historical consolidation index

- [Toolkit preservation and callable/test omissions](toolkit-preservation.md): current default-disabled source consolidation and isolated offline verification; final Research review pending.
- [Thin MCP research inputs](mcp-research-inputs.md): deterministic capability inventory, exact retained symbols, process/authentication/audit lifecycle constraints and remaining design evidence.
- The findings below are the original 2026-10-30 documentation/read-only checkpoint. Statements such as “no file linking or mutation editing tested” describe that checkpoint, not all subsequent research. Later separately authorized private work established selected narrow creation/upload/link/edit/rename/hours outcomes and manual native-UI editing; no universal API or accounting-correctness claim follows. Their public-safe preservation inventory distinguishes historical live observations from current offline tests.
- The owner has closed the administrative run. Current authorization is preservation, offline checks and Research toward a later thin MCP design, with no live account/credential/browser actions or replay of old plans. No current MCP server, production readiness, completed consolidation or Research exit is claimed.

## Historical checkpoint purpose

Establish the public API evidence needed for the owner's immediate supplier-invoice and bank-processing work through Codex or scripts.

## Scope In

Official public API documentation discovery, the separately assessed unofficial App API v4, and capability analysis, with detailed attention to creating versus editing mutations, received invoices, imported bank rows, matching, attachments and quarterly-review data.

## Scope Out

No new account operations in this documentation checkpoint. Separately authorized private read-only feasibility results are summarized without credentials, identifiers or financial details. Bookkeeping writes, actual invoice extraction, tax calculations/filing, production connector implementation, MyBrain storage redesign and Research phase closure remain outside scope.

## Problem Statement

The owner needs to register received supplier invoices and work through already imported bank transactions before a quarterly return. Fast automation depends on distinguishing new bookkeeping entries from editing existing entries and consuming the bank worklist.

## Goals

- Index the discovered official REST and SOAP documentation and every declared business resource group.
- Identify the exact supported operations and gaps for the priority workflow, without inferring API capabilities from the UI.
- Record the selected interface strategy, bounded connection evidence and unresolved capabilities without treating read success as write readiness.

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
| App API v4 supplement | Inferred upload/link routes and PUT mutation request may fill two REST v1 gaps | Accepted only as a deliberate supplement for demonstrated REST gaps. Bounded login/filter/detail reads succeeded; financial-field semantics and writes remain unproved |
| Historical SOAP | Documentation remains indexed for provenance | Excluded by owner; not an integration option or fallback |
| Reuse an existing connector | May reduce integration effort if its actual operations and maintenance fit | Not yet audited in this documentation-first checkpoint. A wrapper cannot establish vendor capabilities merely by naming tools |
| Build a general automation platform | Could orchestrate multiple services | No evidenced need for this larger scope; it would delay the owner's immediate use case |

The owner selected REST as the default on 2026-10-30, with App v4 investigation only for demonstrated REST capability gaps. UI worklist automation and a production connector remain undecided. Routing is capability-based, not an automatic fallback after a REST error; technical failures do not authorize alternate-interface writes or retries.

### Interface and data questions affecting automation

- REST uses API-token-to-session exchange. Vendor prose and security description differ on the Authorization prefix; a bounded live session/read/revocation succeeded, without establishing universal header compatibility.
- API ledger IDs differ from displayed ledger codes. Purchase rows, payment rows and generated invoice-module objects have different contracts.
- Outstanding-invoice responses recommend mutationId/relationId while payment input still names invoiceNumber. Preserve the actual current contract; do not invent a migration field.
- Structured duplicate errors and optional payment-reference uniqueness are documented. Generic idempotency, queue consumption, transactional multi-step writes and a fixed REST rate limit were not established.
- The public user manual documents archive-file linkage and mutation edits in the UI; official REST v1 does not. App v4 has separately graded inferred candidates, not current-runtime guarantees. Its layout is not a live version guarantee.
- Mutations and VAT totals can support review, but no public VAT-return report or filing endpoint was found. The exact quarter, accounting treatment and final return checks are owner/accounting decisions outside this documentation inventory.

### Screened read-only feasibility evidence

Separately authorized private probes established official REST session creation, retrieval of one selected existing mutation and revocation of that temporary session. The owner checked that selected REST result against the actual UI and accepted it as correct for that sample; this is not a universal correctness claim for every type or field.

A separate App login using its own Windows Credential Manager entry, current-administration confirmation, one-day metadata filter, internal-ID detail read and administration checks also succeeded. The observed App internal ID differs from the visible mutation number used by REST; the namespaces must remain distinct. Published search paths failed route binding in live attempts; the declared filter query with an explicit date worked instead. No complete administration scan was used.

Some App summary/calculated monetary fields were inconsistent with the official REST result and the owner's UI check, while common identity/base-row information agreed. The inferred App schema does not define those monetary fields sufficiently to explain the difference. This does not prove changed bookkeeping or a specific App bug. Use REST for financial interpretation; do not round-trip that App response into PUT as if it were a validated write contract.

Credentials were kept locally in separate Windows Credential Manager entries; session values remained in process memory. App logout is not documented and was not claimed. No file linking, mutation editing, bank processing or other bookkeeping write was tested. No private evidence or source location is published here.

### Proportional blast radius

This checkpoint changes only the three issue-12 research/reference documents and its initialized workflow records. Existing MyBrain storage design, deployment code, quality policy, templates and agent protocols remain unchanged. This documentation update introduces no application stack, service, database, credentials, accounting records or connector registration. The separately authorized local research probes and credentials remain outside published repository artifacts. Future downstream consumers are the owner using Codex, scripts using the vendor contract, and any selected minimal connector; all require the same operation-level distinctions.

## Historical questions — earlier REST-first checkpoint

- What minimal production integration should implement the accepted REST-first capability routing?
- Which concrete existing mutation fields need editing, and which pending bank rows or invoice exceptions are the first bounded use case?
- Which permissions and entitlements are required for each future capability beyond the proved read subset?
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

OWNER ACCEPTED — 2026-11-01: use App API v4 uniformly, with the APK as primary contract evidence, and the inventoried functions as scope. Expose named technical provider operations through a thin MCP boundary, without bookkeeping decisions or workflows, and share authentication and logging per process. Reads, writes and readback use App; no mandatory REST comparison or implicit REST/UI fallback. Source gaps remain unavailable pending contract admission. See the [endpoint design](design.md) and [catalogue](endpoint-design-catalogue.md). This is design authority, not account execution authority.

### Historical strategy — 2026-10-30 (superseded for the new server)

The following earlier boundaries are retained as history:

- Use official REST as the default for ordinary data retrieval, interpretation of financial amounts and writes that its supported contract provides. The owner verified the selected read sample in the UI; retain operation-specific validation rather than asserting all REST output is infallible.
- Investigate App v4 only as a narrow, deliberate supplement where an actual REST capability is missing. The first future target is linking an existing archive file to a mutation. App reads may establish the identity mapping needed for such a capability, not become a duplicate general financial data source.
- Do not automatically switch interfaces after REST authentication, validation or network errors. A technical failure does not justify an alternate write or retry.
- Keep SOAP excluded. Preserve current administration data and supported contracts.

This accepts interface responsibilities, not a file-link write, an accounting-correction policy, a complete connector design or Research phase exit. File-target semantics, linking outcomes and any future write still need their own bounded evidence and review.

## Expected Results

A reader can find the official documents, distinguish the 39 REST operations and 20 SOAP operations, identify the supplier-invoice creation contract and understand the official REST v1 gaps, the unofficial App API attachment/edit candidates, and why imported-bank-row processing remains unproved. The bounded read path is established for the selected sample. Further evidence must address only the deliberately selected capability gap with explicit scope and synthetic or otherwise owner-authorized data. Evidence must distinguish bookkeeping outcomes from queue status and prevent duplicate payment creation; this document does not sequence that implementation.

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

This checkpoint publishes only screened conclusions from public contracts and separately authorized private read probes. Keep credentials, real records and private locations outside Git, issues and public evidence.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.2 | 2026-10-30 | Codex (@imp researcher) | Record owner-accepted REST-first boundaries and screened read-only feasibility evidence; retain unproved supplemental capabilities. |
| 1.1 | 2026-10-30 | Codex (@imp researcher) | Add pinned unofficial App API findings; scope REST gaps and mark SOAP historical/excluded. |
| 1.0 | 2026-10-30 | Codex (@imp researcher) | Record official API coverage and the documented creation/editing/bank-worklist boundaries for the owner's prioritized automation needs. |

### Current index revision

2026-11-01, version 1.3, Imp: add preservation/MCP Research entrypoints and distinguish the historical documentation/read-only checkpoint from later narrowly authorized observations and current offline-only work.
| 1.4 | 2026-11-01 | Imp | Reopen function-first coverage and route strategy; index full APK evidence while retaining earlier findings and verdict boundaries as history. |
| 1.5 | 2026-11-01 | Imp | Record owner-accepted uniform App-v4 endpoint strategy and supersede earlier routing for the new Design. |
