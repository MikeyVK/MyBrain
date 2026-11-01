<!-- pgmcp:v1 id=design pv=1.0.0 pf=Uk1D2XWpiag1c6nn sf=WI5iXHBKVOU91bYE -->

# Thin local e-Boekhouden MCP design

**Status:** DESIGN — REVIEW CANDIDATE, NOT IMPLEMENTED  
**Version:** 1.1  
**Last Updated:** 2026-11-01

## Purpose

Define an implementation-ready thin MCP boundary following the independently reviewed research consolidation.

## Scope In

Local stdio server, typed deterministic queries/preparations and narrowly evidenced commands, per-process shared infrastructure, durable cross-process operation state, negative outcomes and test acceptance.

## Scope Out

No implementation, SDK installation, provider/account access, deployment, new operational authority, bank queue processing, sales workflow, tax filing, arbitrary CRUD, native browser automation endpoint or choice of the wider MyBrain application stack.

## Prerequisites

- Research consolidation revision 68bafa6750e64b99cc758f30377fa648566080eb received original independent QA GO. Design transition is authorized; old accounting work is closed.
- Implementation requires a later approved Planning/implementation assignment and separately authorized live acceptance. Static writer preservation is not execution authority.

## Problem Statement

The preserved research toolkit contains useful bounded, tested contracts, but its CLI orchestration, configuration, provider access and presentation are not a reusable MCP application architecture. Codex needs deterministic typed tools without embedding supplier, ledger, VAT, tax or text judgment in HTTP adapters, without per-tool authentication/logging setup, and without replaying closed operational work.

## Functional Requirements

- Expose explicit, bounded queries and source-bound prepared commands through one canonical reusable core and thin SDK handlers.
- Prefer official REST for financial reads and supported creates; deliberately route archive, evidenced narrow changes and hours gaps to App v4.
- Preserve exact identity, money, source descriptions, payment evidence and document graph; distinguish missing, incomplete, unknown and verified outcomes.
- Share authentication, transports and one durable audit/receipt facility for each process; coordinate commands across local processes.
- Default to no live commands, no old-plan replay and no accounting actions from checkout, import, help or startup.

## Nonfunctional Requirements

- Strict CQS, SRP, ISP, constructor injection, frozen extra-forbid DTOs, startup-only configuration and externally configured presentation.
- Secrets stay in host storage; private evidence/state stays outside tracked source; stdout contains MCP protocol only.
- Durable PENDING before dispatch, no automatic write retry or compensating rollback, bounded read-only reconciliation after uncertainty.
- Meaningful public-boundary fake tests and future runtime/handshake acceptance; this document does not claim an implemented server.

## Constraints

- Do not mix owner/LLM choices with adapter mechanics; no generic raw HTTP, SQL, eval or arbitrary field-patch tool.
- Native paid-invoice editing was a manual verified workflow, not a reusable App update contract. Do not expose it as a server capability.
- Keep existing isolated toolkit quality approval separate from future MCP package/runtime acceptance; no activation of unrelated app checks.
- Own command ports return None and persist their external responses internally; MCP command output comes from the separate receipt query.

## Options

### 1. Legacy CLI subprocess per tool

Invoke preserved scripts for each request.

**Pros:**

- Small wrapper surface; keeps reference behavior.

**Cons:**

- Repeated auth/log setup, subprocess/CLI schemas, mixed responsibilities and stale orchestration; rejects shared-lifetime mandate.

### 2. Local stdio canonical core and official SDK

One process per host registration, narrow application ports, official SDK framing and shared resources.

**Pros:**

- Small local deployment; clear lifetimes and typed tools; no network service or copied business core.

**Cons:**

- Requires deliberate extraction/refactoring and future supported-runtime/SDK handshake proof.

### 3. HTTP service or generic automation platform

Persistent network service with generic provider command routing.

**Pros:**

- Could centralize resources across hosts.

**Cons:**

- Adds service security/deployment, unrestricted scope and a new platform absent from owner need.

### 4. JSONL operation journals with file locks only

Retain source-keyed append/fsync and exclusive locks directly.

**Pros:**

- Proven useful legacy patterns; few dependencies.

**Cons:**

- Atomic multi-index operation/source/target claims and crash recovery require additional custom coordination.

### 5. Local SQLite operation store

One process writer owner with short atomic transactions and durable cross-process claims.

**Pros:**

- Standard library; unique constraints and event/receipt atomicity; no external service.

**Cons:**

- Local-filesystem constraint; migrations/backup/disk-failure and contention tests remain required.

## Decision

Choose local stdio with official Python SDK mcp==2.3.0, CPython 3.14, a canonical package with typed ports, and a local SQLite operation/evidence index. Retain the toolkit as reference; do not call its CLIs as production tool implementations.

## Rationale

This meets thin-local scope and explicit shared-resource requirements while separating decisions from transport. Python 3.14 is declared in the pinned SDK metadata; the preserved toolkit's tested 3.15 interpreter is not SDK compatibility proof. SQLite provides small cross-process coordination without pretending to fence the provider or external UI.

## Key Decisions

### Lazy provider authentication, composed once per process

Startup and capability discovery must not access credentials/accounts. Cache providers/clients and authenticate only on explicit provider use.

**Alternatives:**

- Eager login would turn startup into an account operation.
- Per-tool login repeats secrets/session setup and defeats lifecycle sharing.

### Read handlers receive query services only

SDK lifespan owns resources but cannot become a writable service locator passed down every read path.

**Alternatives:**

- A broad AppContext would make read-isolation a convention instead of an interface property.

### Short SQLite transactions, durable dispatch claims

No SQL transaction spans HTTP. A PENDING source/target claim survives process death and has no automatic TTL release.

**Alternatives:**

- PID/lease expiry cannot prove that a provider write did not complete.

### Fixed provider routing and conservative operation profiles

REST failures do not justify alternate writes; existing App evidence is narrow and inconsistent calculated fields must not round-trip.

**Alternatives:**

- Automatic REST→App fallback silently changes semantics.

## Production Design

## Responsibilities and package boundary

| Responsibility | Owner / LLM | Deterministic tool/core | Provider adapter |
| --- | --- | --- | --- |
| Supplier identity, ledger, VAT/tax treatment, private split | Supplies explicit choice and provenance; resolves ambiguity | Computes comparisons/conflicts, validates chosen IDs and preserves source | Translates documented IDs/fields only |
| Description and shortening | Approves meaning and any shortening | Exact source preservation, length/encoding validation, before/after diff | Sends approved text and validates provider shape; application/domain verifier compares the observed result |
| Book date, term and discount handling | Supplies rule/choice, including explicit 0 | Applies supplied rule; no silent defaults or settlement allocation | No judgment or mail/bank side effect |
| Paging, matching, money and duplicate evidence | Reviews unresolved candidates | Exact bounded arithmetic, complete coverage and identity checks | Reads/translates/validates once |
| Execution authority | Host/harness approvals and persistent owner mandate | Validates profile, enabled capability, plan and freshness | Never treats approved=true as authorization |

The proposed package is `src/mybrain_eboekhouden/`: `server` (SDK boundary/startup), `config` (one loader), `domain` (pure values/rules), `application` (query/preparation/command orchestration), `core/interfaces` (narrow external-system protocols), `adapters/rest`, `adapters/app`, `adapters/host`, `adapters/storage`, and `presentation`. It is independent of the preserved CLI package. No subprocess wrapper, SDK context in domain code, concrete constructor inside an action, or duplicate helper per operation.

The SDK registry is built at startup from typed handler instances. It exposes only configured capabilities. Each read handler receives its specific query interface plus the shared presenter; each command boundary receives its dedicated command service and ReceiptReader. Request context carries correlation/deadline only. Pure validators and calculators do not hold transports, writers or configuration loaders.

## Runtime and host integration

Use the official SDK's stdio transport and protocol negotiation. Select CPython 3.14 and pin mcp==2.3.0; use Pydantic v2 frozen models at >=2.12,<3, certifi as the explicit trust bundle and a future reproducible transitive lock. The design uses the stdlib HTTPS transport behind a port, preserving fixed-origin/TLS/redirect/body-size guards; it does not assume the SDK's httpx2 dependency has another library's API. SDK and HTTP package compatibility, wheel availability and cancellation behavior require future isolated execution. There is no SDK/runtime install or handshake evidence today.

SDK lifespan enters before requests and closes at process shutdown. Stdout is exclusively protocol; stderr carries sanitized diagnostics. Official Codex registration is local host configuration, represented only by this nonexecutable placeholder:

```toml
[mcp_servers.eboekhouden]
command = "<isolated-python>"
args = ["-m", "mybrain_eboekhouden.server"]
cwd = "<installed-package-root>"
tool_timeout_sec = 660
```

The host timeout is explicitly 660 seconds, above the server's 600-second absolute operation deadline including queue/auth/read/verification, with a 30-second cleanup reserve and final response margin. This replaces the documented host default of 60 seconds for this proposed registration. A per-HTTP timeout is at most 60 seconds and always clipped to remaining operation budget. Request-count limits are separate from elapsed seconds. Before PENDING, admission refuses a command if remaining budget cannot cover its bounded verification/cleanup; after dispatch a deadline/cancellation can still leave UNKNOWN and never permits replay. These are proposed settings, not executed timings.

No secret, real path, credential target or administration ID belongs in tracked launch examples. Host tool enable/disable and approval configuration remain local. Documentation of registration is not proof of actual host activation.

## Reuse and required refactoring

| Preserved seam | Retain / adapt | Required boundary change |
| --- | --- | --- |
| preflight.Client; complete_pages, inspect_duplicates, money, map_ledgers | Pure pagination/money/identity rules and negative fixtures | Split TLS/session/call budget from catalogue/vendor policy; no batch orchestration |
| catalogue_match.shortlist / identity_evidence | Exact/candidate/conflict comparison | Choice remains supplied; no alias auto-selection |
| probe_rest / credential_store / app_session.AppAuthentication | Fixed routes, TLS, credential abstraction, admin observations | Process-owned clients/auth, expiry/lease/concurrency contract; no per-call setup |
| book_one_invoice.verify_readback / booking_source_guard | Strict rows/groups/term/source descriptions and uncertainty | Typed immutable inputs; no private historical policy/default replay |
| upload_invoice.execute/reconcile_readonly/recover_once | ACK allowlist, early unverified ID, source gate, PDF hash | Inject narrow ports/store; exceptional recovery is separately owner-bound, never general retry |
| change_ledger; metadata_repair; repair_contract | Narrow tested field changes and invariant comparisons | Explicit operation profiles; no raw GET→PUT, no ledger hack for text |
| RepairReads.capture / compose_reads | Observations-before-assert, payment/file graph comparison | Separate capture orchestration from concrete transport construction |
| link_invoice / probe_link_contract | Visible target versus opaque link reference, retention checks | Typed link DTO and shared reader, no guessed unlink |
| hours_domain HoursReader/ContextGuard/EventReader/EventWriter/SerialLock, plans/reconciliation | Existing narrow ports, pure validation and owned cleanup semantics | Replace dynamic mappings with frozen DTOs; separate persistence from reconcile query |
| hours_io SharedWire/AppContext/SharedEventWriter/ExclusiveFileLock | Shared wire concept, context guards, durable-event/lock patterns | Composition at startup; HoursCommand.send ACK return becomes execute→None with receipt writer; remove mutable last_user_info |
| private_output.PrivateOutput | Redaction, append/fsync and safe private paths | Separate durable evidence, audit events and terminal/SDK presentation |
| Native browser paid edits | Historical evidence/manual fallback description | No tool registration or implied API implementation |

Legacy exact batch sizes and scope constants are research limits, not provider limits or inherited mandates. Hours create/edit has separate historical evidence; receipt-owned synthetic cleanup is not generic deletion. The preserved code is not already SRP/DIP/CQS-compliant production code.

## Test Design

Tests exercise public application/port/SDK boundaries with immutable synthetic fixtures and injected fake credentials/transports/clocks/store. No account, real credential backend, browser or network access is permitted in deterministic suites. Retain meaningful reference edge cases and rebind them to canonical public interfaces; do not preserve private run counts or test incidental helper names.

| Acceptance | Observable test / oracle |
| --- | --- |
| N provider queries share resources | N calls use one configured writer/client/provider; lazy first login only, no credential read on import/start/help; no financial command port in read service construction |
| Auth lease/expiry | Fake expiresIn/clock, concurrent single-flight refresh, pinned generation remains valid until release, admin mismatch blocks, query retry bounded, command never replayed |
| CQS and presentation | All own command ports return None; ACK persisted before receipt query; wrapper makes no extra HTTP call; no mutable last response; shared redacted error/presenter |
| DTO/coverage | Shared strict JSON-mode codec for SDK values, provider projection and SQLite; UUID/date/enum/array roundtrip, MoneyText strings, bool-ID/extra/invalid rejection, stable digest; leading zeros/term0/credit/missing/null/coverage |
| Financial/source invariants | IN/EX/BI_EU_INK, rows/sign/order/groups, missing row VAT versus zero, approved source shortening, private split, explicit one-cent policy; wrong present VAT/groups fail |
| Writes and evidence failure | Disk failure before PENDING makes zero HTTP calls; after dispatch existing PENDING remains unresolved; crash windows, early ID unverified, mismatch distinct from UNKNOWN; never auto replay |
| Cross-process coordination | Two actual local processes on temp store contend for same admin/source/target; exactly one dispatch admission; new UUID/alias cannot bypass unresolved source; no TTL/PID release |
| Upload/link/change/rename | PDF magic/size/SHA, safe alias, exact IDs, shared 3/2/2 target retention, whitespace guard, missing outstanding blocks full PUT, rename NOT_RETURNED does not fabricate amounts |
| Hours | Existing public create/edit/plan/reconcile semantics, duplicate marker scope, server IDs and ownership; cleanup only bound synthetic receipt and latest state |
| SDK boundary/lifecycle | Future installed 3.14+SDK2.3.0 initialize/list/call/schema/error/structured output/cancel/shutdown harness; stdout only JSON-RPC; process cleanup/revoke bounded |
| Privacy/paths | Import fake tripwires, no host I/O; tracked-tree scan, reparse/traversal/root/tracked-source refusal, diagnostic secret redaction and bounded payload evidence |

The research preservation suite (275 tests plus 145 subtests on its own Python 3.15 environment) is reference evidence only. It does not execute this design or certify SDK compatibility. Future MCP tests require an explicitly approved isolated binding; current configured-empty-selection remains unavailable, not passing. No global MyBrain app checks or fixes are activated by this document.

## Contracts

### Stable capability catalogue and effect notation

All names below are proposed stable MCP tool names. Inputs are extra-forbid typed envelopes: a configured profile alias plus the named DTO. Q means bookkeeping query (may require technical authentication/audit effects); P is pure calculation from supplied frozen evidence; L is explicit local persistence; C is provider command with evidence effects. Every Q returns a typed result and Coverage/EvidenceRef where applicable. Every C input is ApplyRequest; its result is FrozenReceipt read after the command port returns None. All writes are default disabled.

| Tool | Input → output | Effect / fixed provider route | Evidence / bounds / negative outcome |
| --- | --- | --- | --- |
| eb_capabilities | empty → CapabilityCatalogue | P; none | Declared enabled/unsupported profiles and limits; no login |
| eb_source_import | SourceImportRequest → FrozenReceipt | L; configured inbox only, no provider | Host/operator stages file and supplies exact basename; tool computes hash/magic/size and persists snapshot, no arbitrary path |
| eb_references | profile, kind ledger/relation/costcenter, filters → ReferencePage | Q; GET /v1/ledger, /relation, /costcenter and detail by ID | Official schema; ledger/relation research evidence. Full catalogue explicitly paged; costcenter schema-only until fixture acceptance |
| eb_mutation_get | profile, VisibleMutation → MutationSnapshot | Q; GET /v1/mutation/{id} | probe_rest; exact detail, type1..7 accepted for read |
| eb_mutation_find | profile, exact invoice string → MutationSearchResult | Q; GET /v1/mutation?invoiceNumber=... plus details | preflight, all types, bounded complete paging; partial/mismatch blocks clear result |
| eb_outstanding_get | profile, exact target/relation/invoice → Outstanding | Q; GET /v1/mutation/invoice/outstanding?credDeb=C&invoiceNumber=... | Exact identity; absent NOT_RETURNED, never paid0; no general bank scan |
| eb_app_mapping_get | profile, visible/day → AppVersion | Q; POST /api/v4/mutaties/filter then GET /mutaties/{internalId} | Day max2×20, exact visible match, admin before/after; search routes unavailable |
| eb_archive_list | profile, directory ID → ArchiveListing | Q; GET /api/v4/bestanden[/directoryId] | archive_read; one selected level, caps/coverage, no recursive implicit scan |
| eb_archive_get | ArchiveGetRequest → ArchiveFile | Q; GET /api/v4/bestanden/bestand/{id} | Metadata only; typed identity and shape validation |
| eb_archive_download | ApplyRequest/DownloadIntent → FrozenReceipt | L + provider Q; GET /api/v4/bestanden/download/{id} | Explicit local artifact persistence; fixed MIME/magic/5MiB/no redirect; binary not tool text |
| eb_archive_links_get | profile, visible target → AttachmentGraph | Q; POST /bestanden/gekoppeld | Read POST; kind1 target domain observed, returned koppelId opaque, exact target scoped |
| eb_hours_get | profile, hour ID → HourSnapshot or explicit NOT_FOUND | Q; GET /api/v4/uren/{id} | hours_reader; only documented/observed 404 means absent |
| eb_hours_find | profile, day/marker → HourSearchResult | Q; POST /api/v4/uren/filter | Bounded day/paging, no broad absence inference |
| eb_supplier_match | candidates + supplied identity + Coverage → MatchResult | P; none | catalogue_match; conflicts/aliases visible, no implicit choice |
| eb_purchase_preflight | PurchaseProposal + reference/duplicate/source evidence → ValidationResult | P; none | Source full text/IDs/amount/groups; no I/O/default VAT choice |
| eb_operation_prepare | discriminated Intent + captured evidence/rules → PreparedPlan | P; none | Exact supported kind, hash/changes/blockers; no persistence |
| eb_plan_store | operation_id, PreparedPlan → FrozenReceipt | L; none | Command→None then receipt query, immutable plan; no provider request |
| eb_operation_status | profile, operation_id → FrozenReceipt | Q local store; none | Current recorded state, not a fresh provider assertion |
| eb_operation_reconcile | profile, operation_id → FrozenReceipt | C local-state + Q provider | Read-only provider reconciliation then separate journal command; never repeats original write |
| eb_supplier_create | ApplyRequest → FrozenReceipt | C; POST /v1/relation, GET by returned ID | create_relations individual supplier; exact code+identity precheck, no fixed9 mandate/mail |
| eb_purchase_create | ApplyRequest → FrozenReceipt | C; POST /v1/mutation type1, GET returned ID | book_one_invoice; 1–4 rows conservative profile/IN/EX/credit/mixed supplied choice; strict financial readback |
| eb_archive_upload | ApplyRequest → FrozenReceipt | C; POST /api/v4/bestanden/upload | Reviewed JSON fileName/data(base64)/directoryId/scan=false contract retained in adapter; ACK not proof, metadata+download hash mandatory; no scan/book |
| eb_archive_link | ApplyRequest → FrozenReceipt | C; POST /api/v4/bestanden/koppel | Existing file+visible target, kind1; prior exact query/already desired skip; all shared targets re-read |
| eb_mutation_ledger_change | ApplyRequest → FrozenReceipt | C; PUT /api/v4/mutaties | Narrow one-row IN/high-rate unpaid profile; only row ledger delta; App ID re-resolved after |
| eb_mutation_description_change | ApplyRequest → FrozenReceipt | C; PUT /api/v4/mutaties | Supported unpaid IN profile, exact positive open evidence, whitespace guard; source header only; no independent row-text guarantee |
| eb_archive_rename | ApplyRequest → FrozenReceipt | C; PUT /api/v4/bestanden {id,naam} | ID/name only; preserve bytes/directory/full linked REST/graph; missing open post recorded, not zero |
| eb_hours_create | ApplyRequest → FrozenReceipt | C; POST /api/v4/uren | hours create contract, explicit employee/project/activity choices, marker/source admission and readback |
| eb_hours_edit | ApplyRequest → FrozenReceipt | C; PUT /api/v4/uren | Existing exact hour baseline; supplied supported-field delta, all protected fields compared |
| eb_hours_owned_cleanup | ApplyRequest → FrozenReceipt | C; DELETE /api/v4/uren/{id} | Disabled restricted test-maintenance capability only; own synthetic create/latest receipts+marker required, never generic user-hour deletion |

This is 29 distinct tools, not 27 proven MCP endpoints. Route spellings and field translations must be pinned to the retained adapter contracts during implementation; a catalogue row does not broaden evidence. ReferencePage/ArchiveListing/MutationSearchResult wrap typed tuples plus Coverage and evidence; validation returns typed blockers/conflicts, never raw provider JSON. Supplied page/detail/call budgets cannot be enlarged through tool arguments.

Unsupported: bank-import/worklist consumption and settlement, paid full mutation PUT, App EX/exceptional rounding/general field editing, automatic supplier/ledger/VAT selection, separate row-description guarantees, arbitrary sales/create-delete/update, outbound invoice email, generic hours deletion and raw HTTP/SQL/eval. A documented endpoint without accepted semantics/fixtures remains disabled. Manual native paid-edit evidence is not registered as an API tool. No REST error causes App fallback.

### Authentication and lifecycle

Startup loads config once, validates protected local roots, opens the operation store, constructs one AuditWriter/evidence facility, fixed-origin REST/App clients and host credential providers, then injects narrow adapters/services/handlers. No login at startup. The SDK lifespan owns these objects once per server process; request contexts never recreate them. One provider authentication acquisition covers N sequential tools while valid, not N logins.

REST authentication is POST /v1/session and own DELETE /v1/session cleanup, even for bookkeeping queries. A shared auth manager uses expiresIn, a monotonic deadline with bounded skew and remaining-request budget. Single-flight renewal is guarded per profile. Each operation pins an immutable lease generation; old generations are retired only after holders release, then own-session revoke is bounded. Command admission reserves enough valid lease lifetime or renews before dispatch. No renewal/re-auth error automatically replays a command.

App auth preserves fixed login/user-info and current-admin checks. Expiry/logout semantics are not documented sufficiently: no JWT-clock guess, invented logout or blanket revocation promise. A rejected lease is invalidated. A safe query may acquire a new lease and retry that bounded query once when explicitly classified; a dispatched command remains UNKNOWN and is reconciled, never resent. Secret material is memory-only and neither audit/config DTO nor tool result. Reset drops local App token references; shutdown does not claim a vendor logout.

Current-admin checks bind App context before/after relevant operations; lease generation changes invalidate prepared transport context. REST credential origin is configured separately and never inferred from App numeric IDs. Administration switching and credential installation are not implicit read-tool actions. Initial platform support is the existing Windows host credential provider; fake providers are constructor-injected for tests.

On shutdown stop new commands, drain bounded in-flight workers, capture what is safely observable, release query leases, best-effort revoke own REST sessions, close clients/store/writer. A timeout after dispatch does not become canceled bookkeeping; persistent PENDING remains unresolved if no final write can be recorded.

### Cross-process state, audit and authority

Use one local SQLite store per canonical host account/administration binding, shared across Codex processes. The fixed protected per-user root is not an MCP input. One dedicated writer owner per process serializes all mutation/audit/evidence-index requests through short transactions; immutable query connections are separate. Blocking provider calls run in bounded workers; no SQLite transaction or event-loop lock remains held across HTTP. The store schema owns unique operation_id, immutable plan_digest, server-derived source claims and canonical target claims.

Source keys are recomputed by the service from normalized provider binding, operation kind and immutable source identity/hash; caller source_key is checked, not trusted as a gate. Supplier identity uses exact supplied code plus source identity; purchase identity includes relation+literal invoice string and source digest; upload identity uses original bytes SHA independent of alias; existing-object changes claim visible mutation/file/hour identity. Conservative admin-scoped command serialization prevents overlapping command kinds while a write is unresolved. Aliases cannot create another coordination namespace for the same verified administration. A second local store/config bypass is unsupported and prohibited by startup root/binding checks; no provider-global enforcement is claimed.

Atomic reserve checks operation/source/target uniqueness and stores the complete intent/baseline; a short transaction commits PENDING before dispatch. Repeated same operation ID+same digest returns its receipt without another send; same ID+different digest is CONFLICT. A new UUID/source alias cannot bypass an unresolved canonical source/target claim. Verified identical desired intent is ALREADY_DESIRED after required fresh observations, not blind repetition. PENDING/UNKNOWN claims have no TTL/PID expiry: process death cannot prove provider failure. Read reconciliation may record verified state and release the claim; unresolved cases need an explicit operator disposition contract, never automatic replay. No additional recovery write is authorized by status/reconcile.

SQLite uses FULL synchronous durability, local filesystem locking, foreign keys and bounded busy timeout; event append, receipt head and claim state change share one transaction. Private content-addressed evidence is atomically written/fsynced before its store reference; a crash may leave an unreferenced private artifact, never a reference to silently omitted evidence. Disk/permission failure before PENDING causes zero provider writes. After dispatch, capture/storage failure leaves PENDING and an in-memory diagnostic; do not promise durable UNKNOWN when disk is full. Evidence retention/rotation never deletes unresolved claims or their source/journals automatically. Export/backup is a separate future maintenance contract, not a current backup claim.

A single structured AuditEvent envelope contains schema_version, event_id, operation_id or query correlation, profile alias/binding digest, UTC timestamp, stage, semantic effect, state, safe diagnostic code, typed ID references and evidence digests. Secrets/auth headers/passwords/tokens/user-info profiles/raw arbitrary responses never enter it. Redacted private observations are captured before validation can raise; public errors expose bounded stage/code and evidence handles, not private bodies. SDK wire logs/notifications and stderr diagnostics are not the durable audit. A configured shared presenter maps typed results consistently.

Harness/host approval and persistent owner mandates govern execution. Server configuration enables named capabilities but is not itself proof of current human permission. No custom repeated approval UI, approved=true argument or silent policy engine is introduced. Local claims cannot serialize external UI/other clients, implement provider CAS or guarantee global exactly-once. Fresh pre/post comparisons expose drift; they cannot eliminate a concurrent external race.

### Read, prepare, dispatch and reconciliation semantics

1. Explicit query authenticates lazily if needed, performs only its bounded route, captures sanitized observations before shape/identity assertions, then returns immutable values with exact coverage. Authentication and local evidence are disclosed technical side effects. Incomplete or invalid provider response is not an empty result.
2. Pure preparation validates supplied choices and evidence, computes field-level before/desired changes and a canonical plan digest. Persisting that proposal is a distinct local command. A plan is not authority and cannot contain raw provider JSON or arbitrary paths.
3. Apply resolves the stored plan, checks current config/rule/source digests, enabled capability and authority boundary, acquires canonical claims, and freshly captures full baseline. Known-old must match exactly; already-desired is an explicit no-write result. Missing/multi/unknown payment or identity blocks before PUT.
4. Commit PENDING with exact payload/intent digest and known IDs, fsync, then dispatch once. Capture HTTP status/content-type/allowlisted ACK facts and received IDs before subsequent predicates. ACK_UNVERIFIED is not success. No unknown ACK/timeout triggers another POST/PUT.
5. Verify with official REST as financial truth and targeted App/file/hour reads. Compare intended fields and every protected field, row order/count, money/VAT/groups/relations/ledger/date/term/costcenter/invoice strings/payment state/metadata/bytes/shared links. Rename allows only name and evidenced modified timestamp. Re-resolve App version after update; never reuse old internal ID.
6. All matching evidence yields VERIFIED. An observed unintended delta is MISMATCH with preserved before/after; an unobservable dispatch outcome is UNKNOWN. Both stop further writes in that command series; no rollback/recreate/automatic correction. If an ACK is unreadable, safely read the known object anyway and record RECONCILED only when all exact checks pass.
7. Reconcile is provider-read-only plus explicit local journal update. A found upload needs exact byte hash/admin/directory; multiple/mismatch/no-match remains unresolved. No-match is not proof that the old POST failed. Exceptional owner-approved extra upload is a separate future immutable recovery intent with previous hashes and one-extra source gate; it is never a default retry.

Full mutation PUT is financially broad even for text. Never send App GET calculated zero fields back; use only the evidenced write profile and explicit preserved identity/financial fields. Missing outstanding never means paid0; paid/EX/general updates remain unavailable. Invoice-number whitespace blocks App mutation PUT because normalization was observed. A source-description repair cannot silently change identifiers. Separate row texts are not promised because observed provider processing may overwrite/project them; verify actual header and report row result honestly.

The source/policy exception for a lower one-cent VAT total is explicit evidence, not a tolerance. Financial source versus booking figures remain distinct; no invented row allocation. Discounts/open balances, bank matching and quarterly filing remain outside tools that create invoices or rename documents. File linking must preserve every supplied previous target, including shared document groups. Query filters/path/ID namespaces are fixed by contract, not guessed grids. Cancellation after send is an operation-state concern, not provider rollback.

## Flow

SDK request schema → narrow handler → query/preparation or application command → fixed REST/App port → immediate private observation/receipt capture → exact validation/readback → frozen result via shared presenter. Human/LLM decisions enter as supplied typed evidence-bound choices; no adapter chooses them.

## State and Failures

PREPARED/BLOCKED are local states before dispatch. PENDING is committed before the write; ACK_UNVERIFIED records response facts; VERIFIED/ALREADY_DESIRED are evidenced success/no-write; UNKNOWN and MISMATCH retain claims for read-only reconciliation. Crash with PENDING is conservatively unresolved. No clock expiry, lost lock, cancellation or auth refresh authorizes replay.

## Preservation

Keep research toolkit and its historical evidence boundaries immutable as reference. Refactor selected generic contracts into one canonical core only under later implementation authority; no old batches/profiles/plans are imported or executed. Private config/evidence stays local; tracked examples are synthetic.

## Transition and Cleanup

No automatic migration of old operational journals into executable plans. Receipt-owned synthetic hours cleanup requires original creation/latest-state ownership and remains disabled otherwise. Shutdown releases only locally safe resources; no bookkeeping rollback/delete/compensation or invented App logout.

## Validation

### Strict CQS and injection

**Method:** Inspect signatures and public fake-boundary tests against contract appendix.

**Expected Result:** Own commands return None; query consumers have no command ports; only startup constructs concrete dependencies.

### Routing and evidence alignment

**Method:** Map every tool to retained source symbol, pinned provider route and supported operation profile.

**Expected Result:** No catalogue-only/manual UI capability promoted to general write; unsupported routes not registered.

### Cross-process/no-replay

**Method:** Future two-process crash/claim fixture suite with injected provider barriers and disk failures.

**Expected Result:** One admitted dispatch; persistent unknown claims; no TTL, alias or new UUID bypass.

### SDK/runtime feasibility

**Method:** Future isolated Python3.14 install/lock and official SDK stdio harness.

**Expected Result:** Real initialize/list/call/schema/cancellation/shutdown evidence; docs are not runtime proof.

### Document correctness

**Method:** Native Markdown checks and public-safe diff review on Design artifacts.

**Expected Result:** Valid local links, truthful evidence/unknown boundaries and no private data/source paths.

## Risks

### App v4 is a community-observed contract with incomplete monetary/update semantics.

Expose only narrow evidenced profiles; REST before/after is mandatory; no GET roundtrip/fallback.

**Consequence:** Some desired edits remain unsupported/manual.

### External UI can change records between baseline and write.

Fresh exact comparisons, durable source claims, strict post-state and uncertainty stop.

**Consequence:** No provider CAS/global exactly-once guarantee.

### Local crash/disk failure after dispatch loses final receipt.

PENDING committed first; safe read-only reconciliation and retained claims.

**Consequence:** Human resolution may remain necessary; no blind retry.

### SDK declared support is not installed compatibility.

Separate future Python3.14/SDK2.3.0 handshake acceptance and lock.

**Consequence:** Runtime pin may need a reviewed compatible update.

## Planning Consequences

The design defines cohesive production/test boundaries and acceptance obligations, not implementation cycles or patch steps. Later Planning must preserve these contracts, resolve actual runtime/schema feasibility, schedule independent revision-bound review and keep live acceptance separately owner-authorized. No account operation or product implementation follows merely from this Design document.

## Standards traceability and exact reuse sources

| Standard / constraint | Design consequence | Acceptance |
| --- | --- | --- |
| ARCHITECTURE_PRINCIPLES §1.5/§6 SRP/ISP/DIP | External system contracts live under core/interfaces; concrete constructors startup only; read handlers have no financial command dependency | Composition/port fake tests and interface inspection |
| ARCH §5 strict CQS | Own command ports return None; separate frozen receipt reader; proposal persistence/download artifact capture explicit | Command/query call graph and no extra provider acknowledgement request |
| ARCH §15.1 error/presentation boundary | One SDK boundary, shared presenter, original redacted cause, no bespoke exception hierarchy | SafeError/privacy/stdout tests |
| Configuration/style rules | One ConfigLoader; pure frozen models, no import I/O/singletons or config methods | Schema/import/loader tests |
| DOCUMENTATION_STANDARD / quality policy | Research evidence versus future acceptance explicit; normal native document checks; no global app-check activation | Revision-bound Design review |

These standards are in the maintained [coding standards](../../../.pgmcp/docs/coding_standards/README.md), [Architecture Principles](../../../.pgmcp/docs/coding_standards/ARCHITECTURE_PRINCIPLES.md) and [Documentation Standard](../../../.pgmcp/docs/coding_standards/DOCUMENTATION_STANDARD.md). The source paths below identify concrete symbols for reuse; they do not imply those legacy modules satisfy the new architecture unchanged.

- [preflight](../../../tools/eboekhouden/preflight.py): Client, complete_pages, inspect_duplicates, map_ledgers, money; [catalogue matching](../../../tools/eboekhouden/catalogue_match.py): shortlist, identity_evidence.
- [REST create](../../../tools/eboekhouden/rest_create_command.py): RestCreateCommand; [purchase](../../../tools/eboekhouden/book_one_invoice.py): precheck, execute, verify_readback; [source guard](../../../tools/eboekhouden/booking_source_guard.py): source binding.
- [shared App authentication](../../../tools/eboekhouden/app_session.py): AppAuthentication; [repair reads](../../../tools/eboekhouden/repair_io.py): RepairReads.capture, compose_reads; [metadata repair](../../../tools/eboekhouden/metadata_repair.py): prepare, execute.
- [upload](../../../tools/eboekhouden/upload_invoice.py): UploadAPI, execute, reconcile_readonly, recover_once; [link](../../../tools/eboekhouden/link_invoice.py): execute; [link reader](../../../tools/eboekhouden/probe_link_contract.py): linked_query, project_files.
- [hours domain](../../../tools/eboekhouden/hours_domain.py): HoursReader, HoursCommand, ContextGuard, EventReader, EventWriter, SerialLock, HoursExecutor, HoursReconciler, cleanup_plan; [hours I/O](../../../tools/eboekhouden/hours_io.py): SharedWire, AppContext, SharedEventWriter, ExclusiveFileLock.
- [private writer](../../../tools/eboekhouden/private_output.py): PrivateOutput; [runtime boundary](../../../tools/eboekhouden/toolkit_runtime.py): fixed SOURCE_ROOT/private runtime separation.

MCP tool input/output schemas are generated from the explicit frozen DTOs, with structuredContent and a shared tool-error mapping. One shared strict JSON-mode codec deterministically re-encodes the SDK's JSON-compatible argument values before model_validate_json(strict=True); it never sends the SDK dict directly to strict Python model_validate. Provider numeric projection and versioned SQLite reconstruction use the same JSON-mode admission, as specified in the contract appendix. Source import uses the explicit host/operator staging-and-basename protocol there, not an unimplemented listing tool. SDK protocol errors remain SDK concerns; domain/provider failures are safe typed tool results with isError as appropriate. readOnlyHint describes bookkeeping effect, with authentication/audit effects disclosed; annotations are hints, never permission or idempotency guarantees. UNKNOWN command outcomes must not be marked safe to retry.

### Resolved design details and residual evidence gaps

The SDK/runtime, local coordination and module boundaries above are chosen design decisions. Remaining implementation acceptance gaps are actual installed SDK/3.14 compatibility, provider schema validation against synthetic fixtures, complete optional-field projections on nonpurchase types, bounded shutdown under cancellation and process-crash/disk durability. They do not authorize broader endpoints or accounting tests now.

REST profile binding uses a local owner-activated credential-version record, not the same vault target string as proof after token rotation. Changed/missing version seal blocks before authentication until the owner rebinds the token/admin identity. App administration and REST identity are separate namespaces; a future GET /v1/administration identity validator needs accepted field semantics. The public catalogue reports this assurance limitation explicitly.

The SQLite writer owns its connection on one dedicated thread; worker threads submit bounded typed persistence commands and wait for the commit outcome. The SDK event loop does not execute blocking SQLite fsync or HTTP. Cross-process uniqueness and source/target claim acquisition occur in short transactions, and no HTTP occurs inside them. Source IDs supplied by callers are re-derived/checked using canonical trusted content; new operation IDs with an identical unresolved logical purchase key, file SHA or object target cannot bypass a claim. Only explicit read reconciliation or separately authorized operator disposition can close an unresolved claim; no automatic TTL, PID liveness inference or provider fencing claim.

### Transport ownership and local documentation dependency

Each shared provider/profile client owns a single HTTPS connection guarded by a transport mutex spanning send, response read and close/discard. An HTTPConnection is never used concurrently by worker threads. A failed/closed connection is replaced under that mutex; replacement does not authorize request replay. REST and App clients are distinct; authentication acquisition completes before a business request takes the connection mutex. Auth renewal single-flight state is protected separately, but its mutex is released during network I/O, avoiding lock-order inversion. SQL writer ownership and transport ownership are independent; no SQL transaction spans an HTTP call. Read concurrency is bounded and may serialize on the provider client; thin correctness is preferred over speculative throughput.

The coding-standard links above resolve through this checkout's reconciled .pgmcp runtime/bootstrap documentation. They are local maintained dependencies, not claims that hidden runtime paths publish as GitHub document links. Native offline local-link PASS proves their presence in this workspace only; the versioned design/toolkit documents remain the public-safe artifact set. Public protocol/SDK links below are primary documentation sources, not installed execution evidence.

Graph preservation covers all explicitly observed and locally receipt-known targets for a file. The service unions those targets with supplied references and refuses a purported complete graph whose evidence is incomplete. No full reverse-graph guarantee is invented where the provider exposes only target-scoped lists; unclassified file-link metadata or an unresolved dependency blocks the affected write. External concurrent links remain outside local atomic control, as with external mutation edits.
## Sources

- [MCP tools and annotations](<https://modelcontextprotocol.io/specification/2026-07-28/server/tools>)
- [MCP stdio](<https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio>)
- [MCP cancellation](<https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/cancellation>)
- [Pinned SDK release](<https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.3.0>)
- [Pinned process lifespan](<https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/v2.3.0/docs/handlers/lifespan.md>)
- [Pinned SDK runtime metadata](<https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/v2.3.0/pyproject.toml>)
- [Codex MCP host configuration](<https://learn.chatgpt.com/docs/extend/mcp?surface=cli>)

## Related Documents

- [Approved Research strategy](<research.md>)
- [Preserved toolkit and evidence inventory](<toolkit-preservation.md>)
- [MCP research constraints](<mcp-research-inputs.md>)
- [Concrete contract appendix](<design-contracts.md>)
- [Toolkit bootstrap and limitations](<../../../tools/eboekhouden/README.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-01 | Imp | Complete local MCP architecture, capability contracts, lifecycle, coordination and acceptance design. |
| 1.1 | 2026-11-01 | Imp | Close strict JSON-mode serialization and explicit host/operator inbox intake contracts following independent review. |
