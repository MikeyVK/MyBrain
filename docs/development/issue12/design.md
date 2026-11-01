<!-- pgmcp:v1 id=design pv=1.0.0 pf=Uk1D2XWpiag1c6nn sf=WI5iXHBKVOU91bYE -->

# Thin App-v4 endpoint MCP server design

**Status:** OWNER-SELECTED APP-ONLY DESIGN — REVIEW CANDIDATE, NOT IMPLEMENTED  
**Version:** 2.0  
**Last Updated:** 2026-11-01

## Purpose and accepted strategy

The owner selected App API v4 as the uniform provider route, using the APK as source and the inventoried functionality as the scope. This replaces the earlier workflow-shaped design and REST-default/readback requirement. The server exposes named technical provider operations with shared authentication/logging and **no bookkeeping logic**.

The [endpoint registry/admission catalogue](endpoint-design-catalogue.md) binds the source-backed endpoint families to all 57 functional groups and 23 configuration feature types. The [contract appendix](design-contracts.md) defines concrete technical schemas, interfaces and failure semantics. The [coverage research](api-functional-coverage.md) and [APK catalogue](apk-api-contracts.md) own evidence and gaps.

Version1.x remains in Git, including its independent review. Its business preparation, supplier matching, source-policy decisions, mandatory REST checks and operation-planning state machine are superseded, not inherited requirements. Historical REST helpers/proofs remain preserved and default-disabled; they are not imported, wrapped or invoked by this server.

## Completeness qualification after web-gap research

The subsequent [web-backend gap research](web-backend-gap-research.md) identifies concrete asset, filing, import-rule/processing, export, settings and archive-restore contracts in the separate browser JSON interface. Full 57-group/23-feature coverage through App-v4 is not positively established. This Design remains the owner-selected App-only endpoint baseline for admitted contracts, not a claim of complete web parity. No web/REST/UI fallback is added. If complete coverage is required, the unresolved routing/sufficiency decision must be settled before treating missing operations as implementable.

## Scope and exclusions

| In scope | Out of scope |
| --- | --- |
| Fixed typed App endpoint queries and provider commands | Arbitrary URL/method/headers, SQL/eval, generic unrestricted proxy |
| Provider-native filter, calculation, billing, bulk and send operations | Locally calculated VAT, prices, balances, discounts, returns or reports |
| Exact technical serialization, context/ID/shape checks, paging metadata, binary capture | Supplier matching, ledger/VAT/date/term/rounding choices or payment-completeness interpretation |
| Shared session/credential/HTTP manager, redacted audit, technical dispatch receipts | Book/upload/link/repair/approve/prepare business workflows or automatic source selection |
| Readback as separately callable App queries | Mandatory REST comparison, hidden REST/UI fallback, auto compensation/retry |
| Explicit source gaps and registration admission | Callable placeholder tools pretending to implement missing asset/tax/import/export functions |

The server does not decide whether to create an invoice, consume a bank row, select quote rows, apply a discount, send mail or process bookkeeping. A provider endpoint may do several of these when explicitly requested through its native fields. Its possible effects must be declared; forwarding a provider billing command is not a local billing implementation.

There are no account operations, source implementation, SDK installs, new financial tests or deployment in this Design work.

## Responsibilities and architecture

| Boundary | Own responsibility | Explicitly excluded responsibility |
| --- | --- | --- |
| Owner/LLM/harness | Select required operation and supplied provider values; authorize effects | Permission is not manufactured by an approved=true field |
| MCP handler | Shared codec admission, correlation/deadline, invoke one injected technical service, present typed result | Construct transports, decide accounts/VAT, run multi-operation invoice workflows |
| Technical query service | Resolve fixed registration, obtain context lease, perform bounded query, expose typed response | Hold a financial command port or persist proposals |
| Technical command service | Admit dispatch identity, persist PENDING, issue the one registered command and preserve its response/outcome | Return provider result from own command method; automatically retry or verify bookkeeping meaning |
| App adapter | Fixed route translation, source-backed DTO/JSON and HTTP handling | Select business values, recompute financial fields or silently round-trip GET objects |
| Session manager | Credentials, token generations, context binding, serialized refresh/MFA state | Expose tokens/passwords through tools/results/logs |
| Receipt/artifact storage | Durable technical dispatch/response and explicit bounded binary snapshots | Accounting plan/baseline/approval/source-deduplication engine |
| Shared audit/presenter | Redacted structured events and consistent protocol-visible errors | Per-tool logger/exception framework or raw financial payload logging |

Proposed isolated package:

- `server/`: official SDK stdio boundary and single startup composition.
- `configuration/`: one ConfigLoader, pure immutable configuration models.
- `core/interfaces/`: narrow provider-query, provider-command, session, receipt-reader/writer, artifact and audit ports.
- `contracts/`: frozen technical DTOs, source schemas and the one operation registry.
- `application/`: technical query/dispatch/context/artifact services; no bookkeeping domain.
- `adapters/app/`, `adapters/host/`, `adapters/files/`: concrete implementations created only at startup.
- `presentation/`: shared configured result/error projection.

SDK lifespan owns process resources, not a service locator passed to every request. Each registered handler is constructed with only its narrow service/query interface. Request context contains correlation/deadline, not the writable container. Shared lower-level transport can support both effects, but a query consumer receives only the read/query port and a registry view containing query registrations.

## Operation and schema registry

The registry is an immutable startup resource and the single source of operation names, route templates, input/output schema IDs, effects, source evidence, serializer profiles and inventory trace. The catalogue is the Design's authoritative finite registration specification. Implementation must expand grouped rows into separate explicit records and supply the complete source-bound schema/fixture for each enabled entry. Missing DTO/parameter/effect admission means no callable tool; it never becomes Any or caller-selected HTTP.

For example:

| Named operation | Technical effect | Provider request |
| --- | --- | --- |
| app_mutations_list | Query | POST /api/v4/mutaties/filter |
| app_mutations_create | Command | POST /api/v4/mutaties, caller's typed CreateMutatieDto |
| app_archive_upload | Command | JSON upload with explicitly selected artifact/filename/directory/scan flag |
| app_hours_invoice | Command | POST /api/v4/uren/factureren with supplied hour IDs |
| app_sales_invoices_calculate_totals | Query | Provider POST calculation; no local financial arithmetic |
| app_sales_invoices_mail | Command with outward effect | Provider mail endpoint; never availability-tested by sending |

Queries are not identified by HTTP GET alone: compiled filter/calculation POSTs have query semantics. Provider command/bulk/generate/send operations are not classified as safe queries merely because they return values. MCP annotations are hints, not authority or evidence of idempotency. Known payload flags may widen effects (mail, posting, scanning, cascading); descriptors list every possible effect and host policy may restrict them. The service validates declared effect scope, not the accounting correctness of the supplied values.

Adding an evidenced endpoint requires a registration, schema and fixture; no handler/session/logger branches per action. Changing a path/schema is a versioned contract change. Existing callers receive explicit schema/admission errors rather than silent remapping.

## Data fidelity and source contract

The appendix defines strict JSON-mode admission for SDK-decoded arguments, provider raw UTF-8 responses, immutable models and persisted result reconstruction. Do not pass an untrusted SDK dict directly into strict Python validation. JSON numbers are parsed without intermediate binary float; the technical DTO projection uses exact number text and explicit wire-number serialization. There is no cent quantization, sign/amount rule or accounting recomputation.

Preserve missing versus null versus zero, array order, string identifiers including leading zeros/whitespace, unknown response fields and changed App IDs. Client Required metadata is not automatically provider-required: Json.NET Default0, AllowNull1, Always2 and DisallowNull3 have different presence/null rules. Static client constraints are labelled as such; no invented server defaults are filled.

Unknown response fields are retained in a bounded typed extension projection with a schema warning, not discarded. Unknown request fields are refused until the registry schema is updated. An App response with calculated zero values is returned as the observed provider data, not “corrected” with REST or guessed totals. No GET→PUT object roundtrip is implicit.

Path IDs are separate technical types: App internal mutation version ID, visible number, bank row ID, file/directory ID, association ID, quote/invoice/hour IDs and administration ID. Link kind and target namespace come from supplied source-backed fields; the server does not equate a numeric link kind with a bookkeeping mutation kind. A returned new internal ID is exposed with its namespace; caller can issue a separate named GET.

## Strict CQS and result access

Own provider/application command ports have the signature `execute(dispatch_id, typed_request) -> None`. The unavoidable external HTTP response is captured immediately by the adapter through the already injected receipt writer. No mutable last_response, callback/event bus or extra provider read just to construct a tool acknowledgement.

The MCP command handler invokes the command, then separately queries `receipt_reader.get(dispatch_id)`, then uses the shared presenter. This protocol response is a boundary projection, not a core command that saves and returns a domain aggregate. Provider result/ACK, HTTP status and schema warnings are observations, **not a claim that bookkeeping is financially correct**.

A named readback tool is an independent App query. There is no built-in read→prepare→approve→apply→verify workflow. Auth/current-context checks and response capture are technical infrastructure effects and do not perform business orchestration.

Binary download performs a provider query and an explicit local artifact command; its result comes from the separate receipt/artifact reader. Source import is also an explicit technical local command. Read services themselves do not secretly save a proposal or choose a source file.

## Process lifetime, authentication and context

Startup loads configuration once; validates private roots/registrations/schemas; constructs one audit writer, receipt/artifact services, shared HTTPS/session managers and Windows credential adapter; then injects handler instances. No import/help/checkout/startup login occurs. App credentials are read lazily once per configured credential reference per process, never per tool, and stay in manager-owned memory. No REST token/session/client dependency exists.

Authentication is lazy on the first explicit provider operation. Shared session state includes current App administration, nonsecret lease generation, token availability, challenge state and known/advisory expiry. Login/renew/userinfo responses containing secrets are consumed only by the auth manager; no raw auth response enters normal command receipts, output or audit. Token values never appear in launch environment, arguments or public configuration.

Serialized single-flight renewal admits one refresh for a generation. Where expiry is not authoritatively established, the client uses a conservative auth-invalid state; it does not invent an unlimited lease from missing expiry or trust an unvalidated JWT claim as provider truth. Refresh happens before a new dispatch when needed. An already-dispatched command is never replayed after auth failure, timeout or renewal.

MFA: a challenge produces a nonsecret AUTH_INTERACTION_REQUIRED result and pauses provider admission. The owner/operator supplies any one-time secret through the configured host credential-interaction channel, not an MCP argument or model-visible code. The manager completes the source-backed challenge once and validates context. No account security settings are modified.

Administration context is checked from source-backed userinfo after login/renew/explicit context selection and before command admission. A query cannot switch administration. Explicit selection uses only host-configured allowed aliases, drains old-generation leases and obtains exclusive context ownership. A context mismatch or incomplete binding blocks before dispatch; a mismatch observed afterwards is recorded without replay/rollback. API administration IDs are not equated with UI or other-family IDs.

Multiple processes share no in-memory auth state: each has its own manager/writer/connection. Configured local receipt identity and dispatch locking prevent the same dispatch ID being resent by two participating processes. They do not serialize external UI sessions or prove provider CAS/global exactly-once.

Logout is source-backed but provider-wide revocation scope is unproved. Default shutdown stops admission, drains bounded workers, closes local connections, flushes/closes writers and drops secrets. It does not automatically call a potentially broader logout or claim that a vendor session was revoked. An explicitly enabled host-auth logout operation records only safe status and clears local state; never automatically replay it after uncertainty.

## HTTP ownership and budgets

The process owns a reusable HTTPS client per configured context. A single connection mutex spans send, body read and close/discard: HTTPConnection is never concurrently accessed by workers. Authentication single-flight state is released during network I/O, and lease acquisition precedes taking the transport mutex; no lock-order inversion.

Use bounded worker execution around blocking stdlib HTTPS, not subprocesses. A replaced/disconnected connection is not permission to retry its request. Fixed HTTPS origin is appapi.e-boekhouden.nl, fixed source version /api/v4, no arbitrary redirects or caller headers. Source-proven exceptional version-validation routes are internal technical operations, not a raw proxy escape.

Request count, response bytes, timeout, worker queue and binary size are explicit resource limits, not vendor business limits. List tools request one typed provider page and return provider paging/hasMoreRows as observed; they do not infer global absence from an empty page or automatically scan all business records. Provider-native bulk is one explicit endpoint request, not a local per-record loop.

Design launch budget: host tool_timeout_sec660; server absolute deadline600 seconds including queue/auth/provider and local response work; final cleanup reserve30 seconds; per-HTTP timeout at most60 seconds clipped to remaining budget. Admit no new command if its technical send/capture budget cannot fit. After dispatch cancellation/time limit still leaves possible remote effects; the deadline is not rollback.

## Minimal dispatch journal, not an accounting state machine

Choose per-dispatch append-only JSONL receipts with exclusive filesystem locking and fsync, reusing the preserved technical journal/lock patterns. Reject retaining the former SQLite plan/source/target/business-baseline machine: no plan store, supplier/invoice duplicate policy, accounting approval or financial state belongs here. SQLite could offer atomic indexes, but would add coordination breadth unnecessary for a UUID-addressed single dispatch/result store.

A canonical UUID selects a private receipt file under the fixed validated root. Under an OS-backed cross-process exclusive lock, create/validate the header binding dispatch_id, operation name, stable profile/administration binding and canonical request digest. Auth/lease generation is recorded only as a dispatch observation, never an identity key. Commit PENDING and fsync before the sole provider send. Append observed response/status and persist the typed result through the shared writer before releasing the lock. Atomic file creation and lock acquisition enforce one admission for that UUID.

Same ID/same digest reads the existing receipt without another send; same ID/different operation/profile/digest is CONFLICT. A PENDING/incomplete file after crash is unresolved, even if a process/lock disappeared. No TTL or PID liveness clears it and no automatic replay follows. An UNKNOWN receipt is not a failed-request proof. Fresh explicit queries may investigate known IDs, but no generic reconciliation tool restarts a command.

New UUID means an explicitly new request: this server does not promise source/invoice/body deduplication or global exactly-once. The harness must reuse the same dispatch ID when retrying delivery of the same intended call. A changed ID is not silently interpreted as the old request; accidental duplicate business actions remain the caller/provider's responsibility. This is transparent technical delivery coordination, not an accounting-policy engine.

A short profile-level OS dispatch lock prevents overlapping local sends during context mutation. It is held only for the bounded technical operation, not a long SQL/network transaction or indefinitely waiting for human judgment. Crash releases OS locks, while persistent PENDING remains blocked for the affected dispatch ID. External clients and different explicitly new dispatches are not provider-fenced.

Before-dispatch evidence/storage failure causes zero sends. Failure/crash/disk-full after send can leave PENDING with no final append; the service must not promise it can durably record UNKNOWN on a full disk. No second POST/PUT/DELETE, automatic compensating mutation or generated recovery transaction occurs.

## Shared audit, result storage and errors

One structured audit writer is constructor-injected into session/transport/services; it owns event framing, UTC timestamps, correlation/dispatch IDs, operation name/effect, stage, status and bounded diagnostics. Stdout is SDK protocol only; sanitized diagnostics go to stderr. SDK notifications/wire diagnostics are not durable audit.

No request/response financial payload, password, token, OTP, Authorization header or raw user-info profile is logged. Ordinary receipts record technical metadata/digests plus a pointer to the **private typed provider-result store**, needed for CQS response access. This result store is not the audit log: it holds legitimate command results/unknown-field projections under the same protected retention controls. Auth responses never enter it. Raw unparsed bodies are not dumped into logs; parse/shape failures retain bounded original cause/status/field paths and content digest.

Capture safe HTTP facts and any schema-valid received ID before later validation raises. Unrecognized ACK is exposed as an observed/invalid-schema result or outcome-unknown state, never as an invented failure/retry instruction. The original exception/cause chain is preserved under shared redaction at the existing SDK boundary; no endpoint-specific exception hierarchy or logger framework.

Private configuration, artifacts and receipts live in a fixed local per-user runtime root outside Git/source. No MCP argument selects output/ACL/root paths. Reject system/root/tracked-source/network/reparse escapes. Retention may purge completed typed result data after a documented local period while keeping a digest/tombstone preventing same-ID replay; unresolved receipts are never automatically erased. No backup claim is made.

## Runtime, composition and host policy

Choose local stdio with official Python SDK mcp==2.3.0 and CPython3.14, whose classifier support is declared in the pinned SDK metadata. Pydantic>=2.12,<3 is the DTO admission choice; exact transitive dependency locks and actual install/handshake remain future acceptance. The SDK's httpx2 dependency does not imply compatibility with legacy httpx examples. The App transport remains an independently typed stdlib HTTPS adapter.

A placeholder local Codex registration uses an isolated interpreter and module launch, no secrets or real paths:

```toml
[mcp_servers.eboekhouden]
command = "<isolated-python>"
args = ["-m", "mybrain_eboekhouden.server"]
cwd = "<installed-package-root>"
tool_timeout_sec = 660
```

Host/harness approval policy and enabled operation/effect lists govern execution. Default distributed configuration enables no remote mutation or outward send. A supplied approved=true field is neither accepted nor authority. The server does not add a repeated custom approval UI or infer mandates from old runs. Query POSTs and auth technical side effects are disclosed; tool annotations are not authorization.

This package does not select the wider MyBrain application stack, activate general app checks or install/deploy an MCP server now.

## Reuse, alternatives and evidence

| Preserved source | Reuse as evidence/technical patterns | Not carried into endpoint core |
| --- | --- | --- |
| app_session, processed_invoice_probe transport | Fixed TLS/context/auth abstractions and bounded reads | Per-tool credential/login setup or financial interpretation |
| private_output, hours_io SharedEventWriter/ExclusiveFileLock | Redaction, append/fsync, lock and safe private-path patterns | CLI presentation and private run layouts |
| hours_domain HoursReader/ContextGuard/EventReader/EventWriter/SerialLock | Narrow ports and immutable values | Hours business plans, owned-cleanup workflow or command→ACK return |
| upload/link/change/repair helpers | Source endpoint/DTO and uncertainty lessons | Whole CLI wrappers, source-case guards, alias/rounding policies, REST snapshots |
| preflight/catalogue_match | Historical research only | Matching/ledger/VAT/duplicate decisions |
| REST source/proofs | Preserved historical reference | Any new server dependency or fallback |

Chosen over alternatives: App-only obeys the owner decision and the broader APK evidence. A deliberate REST mix was considered in research and is no longer the new design route. A generic HTTP proxy would defeat named typed scope; per-CLI subprocess wrappers would defeat shared lifetime and mix policy. A network service/NAS/UI platform is unnecessary; stdio stays local. JSONL receipts are sufficient for dispatch identity; the old SQLite planning machinery is intentionally removed.

## Test design and acceptance

These are future implementation acceptance obligations, not tests run by this Design.

| Boundary | Observable fake/harness acceptance |
| --- | --- |
| Registry completeness | All57/23 IDs accounted for; every enabled operation has fixed expanded path, source method/schema/effects; GAP entries produce no tool; no action if-chain |
| JSON/schema | Strict JSON-mode UUID/date/enum/array admission; exact numeric lexical roundtrip; missing/null/zero; Required0/1/2/3; inherited DTO fields/JsonIgnore; unknown-response preservation/unknown-input rejection |
| Thin operation semantics | Exactly selected endpoint and supplied values; no REST call, account/VAT math, matching, source selection, hidden business readback or local bulk loop |
| Shared lifecycle | N calls reuse one credential read/session manager/transport/audit; refresh single-flight, challenge pause, old lease/context draining, no command replay |
| CQS | Command ports return None; immediate private result capture then separate receipt reader; no mutable last_response or extra provider call to format ACK |
| Uncertainty/durability | Failure before PENDING sends0; crash windows and disk-full retain unresolved dispatch; same UUID replay blocked across two processes; different digest conflict; no TTL/compensation |
| Query isolation | Query handlers constructed without command ports; fixed query registry including POST filters/calculations |
| Effects | Mail/billing/process/cascade/scan/deletion metadata and payload effect checks; never actually send in unit tests |
| Binary handling | Explicit source basename/artifact selection, unchanged bytes/hash, traversal/reparse/size refusal, no auto alias/OCR |
| Errors/privacy | Original cause retained, no secrets/financial payload audit, bounded result/quarantine, stdout only protocol |
| Runtime | Future actual isolated3.14+SDK2.3.0 initialize/list/call/error/cancel/shutdown harness; source metadata is not installation proof |

Use representative mutation/archive/hours public boundary fixtures and selected catalogue families. No ceremonial tests of private helper layout, no real credentials/network/accounts in deterministic suites. Historical toolkit275tests+145subtests do not prove this new server or broaden provider semantics. Existing isolated-toolkit check approval does not silently enable general MyBrain application tests.

## Standards and planning consequences

SRP/ISP/DIP and external ports under core/interfaces follow the maintained coding standards; strict CQS is explicit, config models are pure, ConfigLoader is the sole startup reader, presentation is shared/configured. Constructor injection and no import-time I/O remain mandatory. Standard links resolve through the reconciled local .pgmcp deployment, not a claim that those runtime files publish with GitHub docs.

Planning can now implement the stated technical boundaries and admission obligations without inheriting the old invoice workflow. It must preserve the owner-selected App-only route, source gaps and technical uncertainty semantics. This document defines architecture/contracts/acceptance, not an implementation cycle sequence. There is no phase progression, live command authority or publication of private source data here.

## Sources and related documents

- [Endpoint registry and inventory admission](endpoint-design-catalogue.md)
- [Concrete technical contracts](design-contracts.md)
- [Accepted strategy and source chronology](research.md)
- [Function-by-function evidence](api-functional-coverage.md)
- [APK method/path/DTO evidence](apk-api-contracts.md)
- [Preserved source and tests](toolkit-preservation.md)
- [Architecture Principles](../../../.pgmcp/docs/coding_standards/ARCHITECTURE_PRINCIPLES.md)
- [Documentation Standard](../../../.pgmcp/docs/coding_standards/DOCUMENTATION_STANDARD.md)
- [Official SDK2.3.0 metadata](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/v2.3.0/pyproject.toml)
- [Official process lifespan](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/v2.3.0/docs/handlers/lifespan.md)
- [MCP tools specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [MCP stdio](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio)
- [MCP cancellation](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/cancellation)
- [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)

## Version History

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 1.0 | 2026-11-01 | Imp | Historical workflow-shaped local MCP design. |
| 1.1 | 2026-11-01 | Imp | Close historical JSON-mode/inbox contract gaps. |
| 1.2 | 2026-11-01 | Imp | Mark earlier design historical after scope reopened. |
| 2.0 | 2026-11-01 | Imp | Replace with owner-selected App-only technical endpoint design, shared infrastructure and no bookkeeping workflows. |
