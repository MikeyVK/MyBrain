<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Thin e-Boekhouden MCP research inputs

**Status:** HISTORICAL REUSE INPUTS — function scope and provider strategy reopened  
**Version:** 0.2  
**Last Updated:** 2026-11-01

## Historical input boundary — 2026-11-01

Consolidation and the earlier workflow-shaped Design received their exact-revision reviews, but the owner has reopened the functional scope and provider-route strategy. Use [current per-function coverage](api-functional-coverage.md) and [expanded APK evidence](apk-api-contracts.md) before any replacement strategy/design. The preserved seams and constraints below remain historical reuse evidence, not the current implementation basis or a chosen route mix. No account operation or implementation is authorized.
## Purpose

Consolidate evidence and boundary constraints for the owner's later thin MCP design.

## Scope In

Deterministic capability inventory, retained-source boundaries, shared lifecycle requirements, data-contract constraints and expected acceptance outcomes.

## Scope Out

No MCP implementation, tool/signature/schema design, SDK/transport selection, business refactor, account operations or Research phase exit.

## Problem Statement

Repeated CLI/session/orchestration work should become reproducible tools while e-Boekhouden adapters retain one responsibility and accounting decisions remain outside interface plumbing. Existing tested scripts are evidence, not a ready process-lifetime server architecture.

## Goals

- Identify reusable deterministic work with exact retained symbols and evidence limits.
- Separate provider authentication, MCP process lifecycle, private audit storage and presentation.
- Preserve source identity, money/payment/file invariants and uncertain-write semantics in later design.

## Background

The owner requested a complete thin MCP design after consolidation, with deterministic work expressed as tools, SRP provider adapters and authentication/logging shared for process lifetime. The active branch remains Research; concrete design choices follow the governed boundary. The owner explicitly authorized default-disabled writer-source preservation; old private originals remain unchanged and no historical operation is replayed.

## Findings

### Deterministic capability and evidence inventory

These are capability candidates and observed reuse boundaries, not chosen MCP tool names or interfaces. "Retained" means source present; it does not mean production-ready. The [preservation inventory](toolkit-preservation.md) owns import and test dispositions.

| Boundary | Exact reusable source/symbol | Evidence / current gap |
| --- | --- | --- |
| Selected financial query and reference lookups | [probe_rest.py](../../../tools/eboekhouden/probe_rest.py) `read_record`, `project`; [preflight.py](../../../tools/eboekhouden/preflight.py) `Client`, `complete_pages`, `inspect_duplicates`, `map_ledgers` | Bounded GETs, exact identities and incomplete/duplicate outcomes. REST session creation/revocation are authentication side effects even on a bookkeeping-read operation. |
| Current App context and visible-to-internal mapping | [app_session.py](../../../tools/eboekhouden/app_session.py) `AppAuthentication`; [app_probe.py](../../../tools/eboekhouden/app_probe.py) `read_filtered_one` | A date-bounded filter POST is a query; context checks precede financial reads. Login/credential setup/admin switching are distinct concerns. |
| Archive list, selected content and link membership query | [archive_read.py](../../../tools/eboekhouden/archive_read.py) `read_metadata`, `project_listing`; [processed_invoice_probe.py](../../../tools/eboekhouden/processed_invoice_probe.py) `read_app_file`, `validate_file`; [probe_link_contract.py](../../../tools/eboekhouden/probe_link_contract.py) `linked_query`, `project_files` | Fixed origin, bounded reads and exact PDF identity/hash. Returned association reference is not the requested mutation number or App internal ID. |
| Pure identity, money, source and baseline checks | [catalogue_match.py](../../../tools/eboekhouden/catalogue_match.py) `identity_evidence`; [preflight.py](../../../tools/eboekhouden/preflight.py) `money`, `line_proposal`; [repair_contract.py](../../../tools/eboekhouden/repair_contract.py) `validate_source_contract`; [prepare_edit.py](../../../tools/eboekhouden/prepare_edit.py) `identity_mapping`, `field_diff`, `optimistic_check`, `verify_state` | Deterministic validation/comparison is reusable. A proposed ledger, supplier, VAT treatment or rounding exception still needs an explicit source/owner decision; the tool must not invent it. |
| Baseline/payment/file-graph observation | [repair_io.py](../../../tools/eboekhouden/repair_io.py) `RepairReads.capture`, `payment_status`, `compose_reads`, `ObservedAppReadTransport` | Redacted observations can precede validation. Capture currently orchestrates several domains; composition constructs concrete transports. Its restricted assumptions are not a generic paid-edit API. |
| Create, upload, link, guarded edits and hours commands | [book_one_invoice.py](../../../tools/eboekhouden/book_one_invoice.py) `validate_item`, `precheck`, `execute`, `verify_readback`; [upload_invoice.py](../../../tools/eboekhouden/upload_invoice.py) `execute`, `recover_once`; [link_invoice.py](../../../tools/eboekhouden/link_invoice.py) `execute`; [metadata_repair.py](../../../tools/eboekhouden/metadata_repair.py) `prepare`, `execute`; [hours_domain.py](../../../tools/eboekhouden/hours_domain.py) `HoursPlan`, `HoursExecutor`, `HoursReconciler`, `cleanup_plan` | Historical narrowly verified operations and default-disabled retained command source now exist. The owner authorized source preservation only, not execution. The current offline suite verifies synthetic contracts; it does not establish a current MCP command capability or new live authority. |

### Current reuse versus architectural work still needed

The binding architecture requires SRP, narrow read interfaces, injected dependencies, CQS, immutable value contracts, import safety and separate presentation. Preservation of legacy evidence is not a claim that the old CLI layout meets a future server design. The governing CQS rule is strict: pure prepare/build queries return frozen values; persisting a proposal is a separate command. Command mutation and subsequent result-query must remain explicit at the boundary. A startup-owned ConfigLoader is the sole configuration reader; new models do not load files or own ClassVar singletons. Concrete dependencies are constructed at startup and injected. Preserve original exceptions/causes under redaction through the shared boundary/presenter rather than inventing per-tool exception frameworks.

| Current fact | Consequence for the requested thin layer |
| --- | --- |
| `preflight.Client` combines HTTPS/session state, route/call budgets and supplier-policy-derived paths. | It cannot be exposed wholesale as a provider-neutral decision service. Transport/authentication responsibilities and input/owner policy remain distinct boundaries. |
| `RepairReads.capture` coordinates REST, outstanding observations, App mapping, metadata, bytes and linked targets; `compose_reads` constructs concrete transports during work. | Reusable validation and bounded adapters exist, but lifecycle composition and deterministic orchestration still need an explicitly reviewed boundary. |
| `AppAuthentication` shares token/context on one object; it has no established expiry, concurrent-call or process-shutdown contract. REST CLIs authenticate/revoke per invocation. | Shared imports do not establish process-lifetime ownership. Provider expiry/refresh, tenant isolation, concurrent access and cleanup are unresolved; retry after an unknown command is not authorized by reauthentication. |
| [private_output.py](../../../tools/eboekhouden/private_output.py) `PrivateOutput` redacts, prints, saves and fsync-appends operation events. | Its durable audit value is reusable, but process-shared audit ownership and CLI/MCP presentation are separate. Printing to stdout is incompatible with an MCP stdio wire. |
| Existing functions often accept mutable dictionaries and expose deep chains such as `base.app.app`. | Future boundary DTOs/ports must be explicit and validated; copying the chain into tool handlers would preserve coupling rather than create a thin interface. No DTO/signature or refactor is selected here. |

### Distinct lifecycle and protocol constraints

The official [MCP tools specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) defines schema-described tools and structured results. Protocol failure, tool failure, a negative domain outcome and an uncertain external write are separate facts. Tool metadata is not enforcement or permission. Generic protocol retry guidance cannot override a journaled unknown bookkeeping write.

The pinned [Python SDK v2.3.0 lifespan source](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/v2.3.0/docs/handlers/lifespan.md) describes one shared context entered before requests and cleaned up at process shutdown. This supports researching startup-owned dependencies; it does not define provider-login expiry or durable audit semantics. MCP process lifetime, provider session lifetime and the local audit writer must remain distinct.

The [stdio contract](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio) reserves stdout for protocol messages; stderr can carry diagnostics. SDK wire logging is not durable operation evidence. The [pinned SDK project metadata](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/v2.3.0/pyproject.toml) declares Python >=3.10 and classifiers through 3.14. Compatibility with the toolkit's isolated Python 3.15.0 is unproved. Reading documentation is not SDK installation or a successful MCP handshake. SDK, transport and runtime selection remain Design questions.

### Data and uncertainty contracts that must survive

| Boundary | Required meaning, without choosing a schema |
| --- | --- |
| Identity | Administration binding, visible mutation number, current App internal/version ID, archive file ID and link reference retain distinct namespaces. Invoice numbers remain strings, including leading zeros and whitespace. |
| Source and intent | Preserve full source description, approved shortening, source PDF hash and explicit source-versus-booking explanation. No code-plus-number fallback that discards content. A plan binds exact intent and expected source/baseline hashes. |
| Money and VAT | Preserve mode, row order/count, signs, ledgers, relation, terms including zero, cost centres and group/total checks. Missing row VAT means not returned, never observed zero. A historical one-case rounding exception is not a general tolerance or tax rule. App calculated zero fields are not canonical financial input. |
| Payments and files | Missing outstanding rows do not establish paid/open zero or graph completeness. Header PUT can touch financial state; metadata rename has a narrower contract. Shared PDF links and byte identity require preservation across every affected target. |
| Commands and evidence | Durable PENDING precedes a possible write; one attempt, received identifiers and redacted observations survive errors. Unknown outcome blocks automatic repost/rollback/recreation. An archive absence read has a declared scope, not proof of failed upload. Source-keyed recovery requires separate explicit authority. |
| Capability gaps | Official REST is the default; App is a deliberate supplement only for an actual gap. No automatic interface fallback after errors. Bank-worklist processing remains unproved; manual native-browser paid editing is not an API tool. Independent row-text persistence and App identifier/whitespace normalization remain explicit limits. |

Process-lifetime sharing is per server process, not automatically across Codex chats/processes. Cross-process operation/journal coordination or an enforced single-writer policy remains an explicit design requirement; reusing lock/fsync patterns versus a small local state store is not selected here. Local locks coordinate only their actual shared paths, not concurrent provider UI/other-client writes. Pre/post comparison is neither provider compare-and-swap nor global exactly-once. The [MCP cancellation contract](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/cancellation) concerns request processing; cancellation or timeout after provider dispatch cannot establish accounting rollback or failed delivery. Preserve UNKNOWN and use bounded read-only reconciliation, never automatic POST/PUT replay or compensating rollback. Unsupported paid full-mutation PUT, bank-queue consumption, arbitrary updates and sales workflows must remain distinct from proved narrow capabilities. A raw-HTTP, SQL or eval escape hatch would bypass the intended capability boundary and is not part of this scope.

The original bookkeeping run is closed. Current work is static source preservation, public documentation and offline synthetic verification only; it supplies no credential access, browser action, accounting command, tax decision or permission to replay an old plan.

## Questions

- Which pinned SDK/runtime/transport combination satisfies an actual synthetic handshake and lifecycle check?
- What provider session-expiry/concurrency/cleanup behavior is supported without reissuing uncertain commands?
- Which immutable boundary contracts and narrow ports preserve the verified effects without carrying CLI policy/presentation into adapters?
- Which unsupported bank, paid-edit and independent-row-text cases remain explicitly unavailable rather than inferred from manual workflows?

## References

- [Preservation and omission inventory](<toolkit-preservation.md>)
- [Existing official API catalogue](<api-catalog.md>)
- [App-v4 assessment](<app-api-v4-assessment.md>)

## Approved Strategy

Owner requirements recorded on 2026-11-01: consolidate first; expose deterministic operations through a thin MCP boundary; keep provider adapters cohesive and accounting/owner decisions separate; share authentication/logging through the process lifetime. Previously accepted routing remains official REST first, with App-v4 only for demonstrated gaps. Preserve tested operation contracts rather than treating this preservation task as permission for a broad refactor. SDK/transport/runtime and concrete interface choices are not yet selected. Writer-source preservation is accepted as static, default-disabled research source only; final Research acceptance remains open.

## Expected Results

A later accepted design must demonstrate explicit query/auth/command/prepare/verify effects, schema-validated identities and immutable results, injected startup-owned dependencies, defined provider expiry/concurrency/cleanup and shared durable audit ownership, and stdout-safe presentation. Offline acceptance must cover tenant/ID mismatch, stale baselines, missing/ambiguous payment evidence, source-description loss, exact money/VAT/term/sign preservation, shared-file retention, uncertain outcomes without replay, redaction and shutdown. No test may access real credentials or an account. A synthetic installed SDK/runtime/lifecycle/handshake check must establish feasibility before compatibility is claimed. Final inventory must identify every omitted callable/test and the exact verified source snapshot.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-11-01 | Imp | Record owner strategy, retained symbols, lifecycle/contract gaps and primary MCP evidence. |
| 0.2 | 2026-11-01 | Imp | Index reopened function-first provider research; retain earlier reuse inputs as historical. |
