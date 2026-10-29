<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Garmin Personal API ingestion: technical research

**Status:** Research candidate — owner strategy decision and independent review pending

**Version:** 1.1

**Last Updated:** 2026-10-29

## Purpose

Assess a personal Garmin ingestion plugin against primary API evidence and MyBrain issue #6, leaving a reviewable Research candidate and explicit owner decisions.

## Scope In

Official Personal API protocol, complete endpoint catalog, SDK fit, generic storage integration boundaries, strategy options, unknowns and synthetic expected outcomes.

## Scope Out

Approved architecture, application interfaces/code, implementation planning, live authentication/import, personal data, new accounts, issue #6 edits, phase exit and publication.

## Problem Statement

MyBrain needs a technically grounded way to assess Garmin ingestion while its generic source-registration foundation is still a Design candidate. API convenience wrappers do not by themselves establish exact originals, durable admission, complete coverage, secure secrets or accountable history.

## Goals

- Identify actual API prerequisites and ambiguity without inventing quotas, availability or historical guarantees.
- Map source-specific capture to existing generic candidate contracts without creating a second authority.
- Present compatibility/custody choices and expected evidence for owner strategy decision and independent review.

## Findings

### Evidence status and current baseline

**Verified** below means documented by Garmin or observed in pinned source, not runtime-proved. **Proposal** means this producer's recommendation for owner consideration. **Unknown** means the inspected evidence does not settle the question. No release-date claim is necessary for feasibility.

The [accepted ADR 0001][adr] governs originals, identity, versioned meaning and exclusive personal ownership. Issue #6's [reviewed Research][base-research], based on `71a1a6c`, is an accepted input; its [Design v1.3][design] at `655e9563ba5536d24d9db3c98ef5819ae40feff4` remains an independently unapproved candidate. Its model, operations, preservation and acceptance documents were inspected at that immutable snapshot without copying or changing them. Recheck drift before later Design.

That candidate places registry and compact exact bytes in PostgreSQL 18, payloads above 1 MiB in protected retained POSIX files, and mutable working files in OpenCloud 7.2.4. OpenCloud is not the immutable authority. Application language/framework remains unselected. These are issue #6 candidate decisions, not choices adopted or tested by issue #8.

The focused [issue #6 assessment][intake-assessment] at `0f31bb9` is research evidence, not accepted architecture/runtime proof. It separates metadata candidate/control-plane records from lifecycle on the same source; stock-client pre-upload hold from server quarantine; and centralized policy from one shared binary plugin. Reusable filters may authorize classes of new files: revalidate conditions at transfer and register the received version; snapshot-specific approval cannot float to changed bytes. No universal per-file manual approval, hash or token scheme is selected. Its host-specific policy reload finding—7.2.4 evaluation versus 9.0.0 startup—adopts no upgrade.

The immediate blast radius is two research documents and initialized branch state. Production code, application tests, configuration, helpers, agent instructions, templates and enforcement stay unchanged. Future affected consumers include owner credential management, collectors, generic registration/retrieval, operational recovery, custody/backup and optional tools; downstream interpretation/model disclosure needs separate authority. Harness Python does not select the product runtime.

### API prerequisites, access and security

Garmin's [Personal API instructions][personal] require an owner Garmin Connect account, self-generated key and acceptance of presented terms. They describe no separate commercial developer-application approval for this personal route; actual eligibility and terms acceptance were not exercised. The [FAQ][faq] restricts the intended use to one's own data and excludes commercial multi-user applications.

Key lifetimes are selectable 30/90/180 days or one year; keys are shown once. Revoking a key invalidates its related tokens. Access tokens last 24 hours or until key expiry, whichever is earlier; there is no refresh token. Renew by exchanging a still-valid key. The exact POST path is `/personalapitoken-service/personal-api/personal-api-key/token` with `Authorization: ApiKey <key>`. Pinned [auth.py][auth] consumes the response as stripped **raw JWT text**, not a JSON envelope; [client.py][client] sends `Authorization: Bearer <token>` for reads.

The [catalog](api-catalog.md) records both .com and .cn servers. Proposal: select region explicitly, allow only approved HTTPS hosts, bind secret references/cache and opaque subject namespace to that region, and reject credential-bearing redirects or arbitrary response-host discovery. A configured base URL is not evidence that a credential is safe there. Account/subject continuity across key rotation is unverified; a changed or unverified subject requires reconciliation before appending to an existing identity. JWT expiry decoding alone does not authenticate subject identity.

The catalog distinguishes 26 GET data paths from the token POST. It covers activity summaries, workouts/original ZIPs, wellness, sleep, HRV, weight/goals, nutrition, profile, zones, Fitness Age and cycle data. Endpoint listing does not establish account/device availability or authorize collecting every dataset. Sensitive dataset selection, including cycle/nutrition/media, belongs to the owner's capture scope.

Proposal: protect keys and optional token caches in a host secret facility, pass references rather than values through configuration, and keep credentials out of Git, receipts, tool arguments/results and diagnostics. Authentication failure pauses collection; it does not authorize destroying admitted history. Ingestion consent does not imply permission for external models, training, sharing or commercial reuse. Presented terms and downstream disclosure need independent review at implementation admission; this research supplies no legal conclusion.

### Technical requirements and unresolved semantics

| Verified source boundary | Consequence / proposed requirement |
| --- | --- |
| Steps/stress windows maximum 28 days; sleep summaries/hydration/Body Battery 31 days; V2 daily summaries one year. Other maxima often unspecified. | Split finite calendar scopes within documented maxima. Do not confuse a maximum request interval with historical retention. Clarify inclusive edge counting and “one year”. |
| Activity offset search defaults limit=99, start=0, excludeChildren=true. SDK helper uses 20. | Send explicit parameters; include multisport children or state their exclusion. Offset drift under inserts/edits can skip/repeat records; no snapshot/tie order is promised. |
| Bare arrays, `.data`, `.hrvSummaries`, and HRV 204 differ. Weight range includes adjacent entries outside scope. | Parse per endpoint contract after capture. Record status and exact requested coverage; graph context does not extend covered windows. Empty/204 is an observation, not deletion or permanent absence. |
| HRV strings omit offset/Z; activity local/GMT strings lack suffix; beginTimestamp explicitly epoch milliseconds. ConnectDate/ConnectTimestamp are nested objects. | Keep original spelling, zone claims and local date separately from normalized observation time. No guessed timezone; field-specific interpretation remains attributable. |
| Sleep timestamp schema string/date-time conflicts with “in ms” prose. Weight explicitly kilograms; several other units/array positions underspecified. | Preserve ambiguous fields without coercion. Do not import unofficial grams, flatten nested timestamps or assume sample layout. Lossless opaque IDs must survive int64 values beyond safe JavaScript numbers. |
| ZIP download promises original format, not FIT for every activity. | Preserve original archive before members. Later extraction needs traversal/symlink rejection, bounded expansion/count/size, format checks and explicit partial results. |
| No quota, 429/Retry-After contract, ETag, modifiedSince, webhook, request-ID header or historical/deletion guarantee found. | Treat these as unknown, not permanent non-support. Propose configurable finite retries/backoff, bounded backfill and overlap/reconciliation; invent no numeric quota or SLA. |

Later evidence should resolve these uncertainties proportionally:

| Unknown / contradiction | Bounded evidence needed before claiming the capability |
| --- | --- |
| Eligibility, regional terms and subject binding | Owner-authorized account check plus applicable terms; documented subject continuity through key rotation/region change. |
| Rate limits and transient/auth error classification | Provider clarification or separately authorized bounded synthetic/live probe; redact bodies/identifiers. Stop rather than retry indefinitely. |
| Pagination ordering, revisions/deletions and historical horizon | Provider contract or controlled late-sync/edit/page-drift observations; otherwise retain explicit incomplete/unknown coverage. |
| Time/unit conflicts and no-data behavior beyond documented HRV | Provider clarification and synthetic fixtures representing every admitted shape; DST/leap/range cases. |
| Original ZIP contents, size and interrupted downloads | Public/synthetic safe/unsafe archives and bounded fault evidence; no full-FIT promise. |
| `heartRateZones` GET defaults `generateDefaults=true` | Provider clarification: does Garmin generate/persist state or only return computed defaults? Strict no-effects claims beyond its advertised read-only intention remain unproven. |
| Core storage operability | Issue #6 independent review and later admitted native proofs; source inspection cannot establish a running registrar. |

Proposed retry classification: malformed requests need correction; 401 may permit bounded token renewal with a valid key, while unresolved 403/subject/region failures stop collection. Transient server/network failures and any observed throttling need finite backoff and a total deadline; honor a valid Retry-After only within configured bounds. These are proposed policies, not Garmin guarantees. Bound decoded response bytes, download size and extraction resources as well as connection/read timeouts.

An upstream GET retry may observe changed bytes: revalidate reusable rules and preserve actual bytes, rule version and observation. Once a core operation intent is frozen, retries cannot substitute a different request fingerprint or payload. Resolve the original operation first; preserve any genuinely new response as a separately attributable observation, without disguising it as replay of the old committed result.

### Mapping to issue #6 without changing its contracts

This is a proposed compatibility mapping, not new envelopes, database tables or executable interface definitions.

| Garmin concern | Generic registration mapping and source | Remaining boundary / consumer impact |
| --- | --- | --- |
| Raw response | Exact **HTTP application entity bytes before JSON parsing** become source Payloads under the [model][model]. Declare capture after HTTP transfer framing and Content-Encoding decoding; record selected safe media/encoding provenance and convention version. | This does not claim TLS/wire-byte fidelity or compressed-wire preservation. Decoding failures remain failed/partial capture; reserialized JSON is never the original. |
| Activity archive | ZIP payload first; extracted members are separately pinned sources/representations and package contents, following model source/parts and [preservation][preservation]. | Member validity/completeness cannot replace original archive custody. Plugin supplies bytes; core alone chooses the 1 MiB backend boundary. |
| Provider claims and observation | Original fields stay provider claims in contract-described metadata. Receipt carries attributable observation time, connection reference and unknown/verified/conflicting upstream binding; package carries expected scope. | Provider activity time, collection observation, durable registration and applicability are different facts. Safe receipt fields exclude auth/error-body dumps. |
| Enduring identity | MyBrain-generated UUIDs stay independent of provider IDs/hash. Recognition considers region + opaque subject + dataset + opaque provider ID, or scoped day/request variant where no ID exists. | A daily key identifies a logical scope, not a Garmin revision. Different endpoints/flags or caller todayDate must not collide. Exact subject verification remains open. |
| Content versus repeat intake | Immutable captured content, metadata-set versions, receipts and representations keep independent histories; exact member/binding references preserve their basis. | A later scheduled observation is a new receipt even when bytes match. Equal content permits explicit reuse, not automatic identity merging. Changed prior-day bytes retain history. |
| Contracts and interpretation | Pin provider schema snapshot/hash and transformation/recognition versions as inert contract/method references and bindings under model contracts. | Trusted admission controls validators. Stored contract text is not executable; unsupported shapes remain raw with explicit processing failure. Do not reclassify malformed source JSON as invalid raw bytes. |
| Staging and operational state | Pending lifecycle metadata stays on the same registration; candidate/control-plane records are not a second source registry. Staging is a selector. Operational connection/cursor/retry state remains recoverable bookkeeping. | Cursor advances only after durable admission of its exact scope. A prepared operation or downloaded temporary file is not publication; failure preserves honest pending evidence. |
| Publication/retry | Use candidate [prepare/upload/commit operations][operations], durable intent before payload I/O, atomic publication and original operation ID to resolve lost replies. | Transport retry preserves request identity; it is not another receipt. Reconciliation must resolve an uncertain committed result before refetching/recreating it. |
| Concurrency/history | Reuse core CAS revision + selection-publication UUID, exact dependencies and historical selections; restore changes service incarnation. | No last-writer overwrite, ABA acceptance or replay of old retry/cursor contexts after restore. Current views do not rewrite historical results. |
| Custody/ownership | Reuse owner sessions and [preservation/destruction/recovery][preservation] controls, including known temporary/derived/backup copies. | No direct SQL/OpenCloud archive writes or second authority. Remote Garmin remains outside local destruction control; owner-approved suppression must prevent silent reimport. |

A request-window response can cover several daily logical records. Preserving one raw response and linking exact extracted representations avoids inventing a provider original for each parsed row. Receipt/package completeness must identify dataset, dates, filters, child scope and relevant observation, not a generic “Garmin synchronized” flag.

Garmin inference: the connector owns network fetch, so owner-authorized dataset/date/subject/rule scope can gate download separately from post-fetch storage admission. Content-dependent rules need authorized inspection; unknown content cannot promise a zero-fetch decision.

Proposal: use finite owner-selected backfill, overlapping recent windows and bounded periodic reconciliation. Record attempted, missing, partial, admitted and unknown scopes independently. Late synchronization can revise prior days; reaching a last offset or receiving 204 cannot prove complete account history. Do not infer deletion from absence. Destruction needs a deliberate owner-controlled recapture policy: retained suppression is itself sensitive control data; if the owner requires no residual identifiers, stopping the affected capture scope may be necessary. This gap belongs at the intake/custody boundary, not a silent core contract change.

### Plugin capability and packaging options

Language-neutral responsibilities are transport/auth, endpoint collection and coverage interpretation, generic registration, and operational recovery state. These are conceptual capabilities, not prescribed classes/services. An optional MCP facade could invoke authorized collection/status operations; MCP provides neither storage authority nor permission to expose credentials or health payloads.

| Packaging option | Benefit | Cost/risk and consumer consequence |
| --- | --- | --- |
| In-process adapter | Fewer process/deployment boundaries; straightforward shared runtime and bounded streaming. | Shared memory/failure domain and dependency conflicts; credential lifetime shares host process. Requires the eventual runtime choice. |
| Isolated worker through generic storage API | Runtime choice and failure/resource isolation; can use official SDK without imposing Python on MyBrain. | Additional secret delivery, process supervision and network/lost-reply recovery; must preserve generic idempotency/CAS semantics. |
| Optional MCP invocation facade | Familiar tool entry for bounded owner-authorized actions and status. | Adds authorization, output limits and disclosure surface; raw payloads/secrets must not become default tool output. It can front either option above. |

The [SDK manifest][manifest] requires Python >=3.12 and requests and declares Apache-2.0. Reuse offers maintained endpoint/auth conveniences. However [client.py][client] returns parsed JSON, buffers full ZIP downloads and provides no built-in automatic retry. [auth.py][auth] writes newly obtained tokens to a plaintext cache with no disable-cache option; [_credentials.py][credentials] warns about permissive POSIX modes but performs no Windows ACL check. [downloads.py][downloads] publishes a complete buffered file but does not establish the core's fsync/custody contract. HTTP errors carry response text and URLs; routine request logs also expose paths/query scopes.

Wrapped/adapted SDK reuse therefore needs explicit pre-parse byte capture, bounded stream/timeout/size controls, secret-cache policy (optional/memory-only caching requires adapted/replacement authentication), host restrictions, retry classification and redacted diagnostics. A thin independent transport offers direct control and language freedom but owns more protocol maintenance and drift tracking. Neither is selected here. SDK inspection was read-only; its code was not installed/executed against Garmin.

[personal]: https://developer.garmin.com/gc-developer-program/personal/personal-api/
[faq]: https://developer.garmin.com/gc-developer-program/personal/personal-faq/
[adr]: https://github.com/MikeyVK/MyBrain/blob/655e9563ba5536d24d9db3c98ef5819ae40feff4/docs/architecture/decisions/0001-digital-brain-foundational-principles.md
[base-research]: https://github.com/MikeyVK/MyBrain/blob/655e9563ba5536d24d9db3c98ef5819ae40feff4/docs/development/issue6/research.md
[design]: https://github.com/MikeyVK/MyBrain/blob/655e9563ba5536d24d9db3c98ef5819ae40feff4/docs/development/issue6/design.md
[intake-assessment]: https://github.com/MikeyVK/MyBrain/blob/0f31bb9a3c278de71fa44674fcf5208f00f8db06/docs/research/public/opencloud-admission-extension-feasibility.md
[model]: https://github.com/MikeyVK/MyBrain/blob/655e9563ba5536d24d9db3c98ef5819ae40feff4/docs/development/issue6/storage-model.md
[operations]: https://github.com/MikeyVK/MyBrain/blob/655e9563ba5536d24d9db3c98ef5819ae40feff4/docs/development/issue6/storage-operations.md
[preservation]: https://github.com/MikeyVK/MyBrain/blob/655e9563ba5536d24d9db3c98ef5819ae40feff4/docs/development/issue6/storage-preservation.md
[auth]: https://github.com/garmin/connect-personal-api-python/blob/ac111a0ff8e37dfbc24c616fcc27691520c7278b/src/garmin_personal_api/auth.py
[client]: https://github.com/garmin/connect-personal-api-python/blob/ac111a0ff8e37dfbc24c616fcc27691520c7278b/src/garmin_personal_api/client.py
[credentials]: https://github.com/garmin/connect-personal-api-python/blob/ac111a0ff8e37dfbc24c616fcc27691520c7278b/src/garmin_personal_api/_credentials.py
[downloads]: https://github.com/garmin/connect-personal-api-python/blob/ac111a0ff8e37dfbc24c616fcc27691520c7278b/src/garmin_personal_api/downloads.py
[manifest]: https://github.com/garmin/connect-personal-api-python/blob/ac111a0ff8e37dfbc24c616fcc27691520c7278b/pyproject.toml

## Approved Strategy

**PENDING for every boundary below.** The original mandate authorizes research; it does not delegate strategy approval or phase exit to this producer. Preferred options are proposals for explicit owner decision and independent review. They are not adopted architecture. No live migration or compatibility break is authorized.

| Boundary / affected consumers | Viable options, cost and risk | Preferred proposal; approval |
| --- | --- | --- |
| Storage contracts / registrar and downstream readers | Extend/bypass core for Garmin (fast specialization, incompatible authority/history); preserve generic contracts (adapter mapping and admission work). | Preserve issue #6 contracts, subject to its review; return genuine gaps for decision. **Pending**. |
| Provider identity and raw preservation / recognition, history, parsing | Parsed-only/provider-ID identity (less storage, loses exact evidence and region separation); raw capture + independent UUIDs/pinned interpretation (more bytes/contracts). | Preserve entity bytes/ZIP plus explicit namespace and unknown upstream version. **Pending**. |
| Sync coverage and retries / owner, scheduler, recovery | One-pass offsets/last-day watermark (cheap, misses drift/late changes); bounded overlap/reconciliation (more requests and state, still no universal completeness). | Finite scopes and classified retries, original operation identity, explicit coverage. **Pending**. |
| Capture authorization / owner, collector, admission | Per-record manual approval (high friction); reusable scoped rules (revalidation/inspection risk). | Gate fetch by authorized dataset/date/subject/rule scope; retain separate storage admission. **Pending**. |
| Secrets and region / credential operator | SDK plaintext/default-host behavior (convenient, leakage/routing risk); protected secret references and explicit host/subject binding (platform integration cost). | Protected credentials, region allowlist, stop on unresolved identity. **Pending**. |
| Custody/destruction / storage, backup, collector | Resume sync after local deletion (simple, recreates data); owner-controlled suppression or stop affected collection (sensitive residual state or reduced coverage). | Reuse core destruction plus explicit recapture policy; no stronger erasure claim. **Pending**. |
| Optional tools / owner, MCP/model caller | No facade (smallest disclosure surface); bounded facade (convenience, authorization/output review); broad raw-data tools (maximum leakage). | Keep optional and bounded; no default raw-data/credential exposure or implicit model consent. **Pending**. |
| SDK/packaging / runtime and operations | Adapt SDK versus thin transport; in-process versus isolated worker as compared above. | Require byte fidelity/resource/secret proof; defer stack/topology selection. **Pending**. |

Rollback of a future collector should stop new acquisition and reconcile pending operations by original identity, preserving admitted history. Disabling collection is reversible; destruction is owner-approved and irreversible within its declared guarantee. No data migration, core replacement or rollback script is proposed.

## Expected Results

**Specified, not executed.** These synthetic obligations complement issue #6's [acceptance candidate](https://github.com/MikeyVK/MyBrain/blob/655e9563ba5536d24d9db3c98ef5819ae40feff4/docs/development/issue6/storage-acceptance.md); they do not replace native storage proofs or constitute an implementation plan.

| Scenario | Expected observable result |
| --- | --- |
| Retry and lost publication reply | Same incarnation/operation/request yields one durable publication and receipt; query original operation resolves lost success. Conflicting fingerprint does not create a duplicate. |
| Unchanged repeat versus changed historical day | Scheduled repeat has independent observation evidence and may reuse exact content deliberately; changed old-day bytes retain previous content/bindings and historical views. |
| Changed response / rule reload | Retry after changed bytes or rule reload rechecks current authorized scope; obsolete snapshot approval cannot authorize new bytes. Preserve actual bytes, rule version and observation; reusable rules require no blanket per-record manual approval. |
| Shifting offset pages and multisport children | Duplicate IDs do not duplicate identities; skipped/uncertain pages remain visible coverage gaps. Explicit child setting prevents a false all-activities claim. |
| Late sync, missing day, empty array and 204 | Scope/status evidence differs from failed transport, deletion and complete history; later data can be admitted without rewriting prior observations. |
| Leap day, DST, range edges and large IDs | Original local dates/offset-free times survive; no guessed instant or double-counted boundary; int64 identity remains exact beyond JavaScript safe integer range. |
| Malformed JSON / unknown schema | Exact raw bytes remain admissible via valid core envelope; parsing failure is attributable and no invented normalized record appears. |
| Unsafe ZIP / expansion bound | Archive preserved; unsafe path/symlink, excessive members or expansion fails bounded extraction without writing outside custody or claiming complete members. |
| Expiry, revocation, subject change | Bounded renewal only where authorized; revoked/expired key stops capture, existing history remains; changed/unverified subject cannot contaminate prior namespace. |
| Partial download / publication failure | No truncated payload is reported admitted; pending recovery remains visible; operational cursor never outruns durable scope admission. |
| CAS/ABA and restore incarnation | Stale selection token conflicts even after head returns; restored service rejects old write/retry/cursor contexts before reconciliation. |
| Destruction and resumed sync | Owner policy suppresses recapture or stops scope; temporary/derived/backup copies are accounted for; local removal is not remote Garmin erasure. |
| Coverage honesty | Out-of-range weight context, unsupported datasets, missing pages and unknown retention never produce a false complete-account result. |

## Evidence

### Feasibility and remaining decisions

A personal read-only ingestion plugin is technically plausible against the documented protocol and candidate generic storage boundary. The evidence does not establish runtime feasibility, complete history or preservation guarantees in a deployed system. The most consequential constraints are original-byte capture, uncertain provider revisions/coverage, credential lifecycle and intake suppression after destruction.

The next decision is explicit owner strategy per boundary, followed by independent Research review on the committed candidate. Provider clarifications and later authorized synthetic/native proof should target the uncertainty register. Issue #6 review drift must be reconciled before Design. Product code, stack choice, live account access, implementation sequencing, push/PR and phase transition remain outside this assignment.

### Source, privacy and quality evidence

Public Swagger extraction matched the catalog's JavaScript/decoded-JSON SHA-256 pins; the seven exact SDK files were fetched at the immutable commit and hashed. API/FAQ pages were read on 2026-10-29. Original/private PDFs, credentials, personal records and live error bodies were neither obtained nor included. All described scenarios are synthetic expectations; none was executed. Immutable issue #6 references avoid absent local sibling links.

Version 1.1 evidence, observed 2026-10-29 through `pgmcp-garmin`: `run_checks(scope="targets", targets=["docs/development/issue8/research.md","docs/development/issue8/api-catalog.md"], checks=["markdown_links"], timeout_seconds=120)`. Both concrete files were selected; run_status and markdown_links were `passed`, native Lychee **0.24.2**, adapter **2.0.0**, native exit code **0**. The native report counted 29 link occurrences: 3 successful local links, 26 excluded external occurrences, 0 errors/timeouts. Configured arguments were unchanged: `--offline --cache=false --include-fragments`. This records actual execution, not external URL reachability or semantic approval.

Application checks/tests and automatic fixes remain deferred under the [repository quality policy](../../../README.md#quality-policy). No empty selection is reported as passing evidence. Producer consistency/privacy review is findings-only and cannot issue independent GO.

- [Complete 26-path catalog and immutable SDK/specification pins](<api-catalog.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-29 | Codex (@imp researcher) | Document primary API evidence, issue #6 mapping, strategy options and synthetic proof obligations; leave approval and independent review pending. |
| 1.1 | 2026-10-29 | Codex (@imp researcher) | Incorporate focused intake-assessment evidence and pending capture authorization; clarify heart-rate-zone side-effect uncertainty and mandatory SDK caching; refresh documentation-check evidence. |
