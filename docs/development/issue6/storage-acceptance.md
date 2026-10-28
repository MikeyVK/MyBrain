<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Storage acceptance and feasibility specification

**Status:** Design candidate — review requested  
**Version:** 1.2  
**Last Updated:** 2026-10-28

## Purpose

Define behavior-first evidence for implementation and independent review, using exact synthetic inputs and failure boundaries rather than tests that mirror internal table operations.

## Summary

All scenarios below are required proof obligations, not executed tests. The design is reviewable against exact outputs, preserved bytes, historical member selections and failure/release boundaries. Product readiness requires later native implementation evidence on the admitted stack.

## Fixture and oracle rules

Use only synthetic sources. FixtureT is the exact UTF-8 byte sequence represented by the escaped literal "{\"b\":2,\"a\":1}\r\n"; the original has that key order, spacing and final CRLF. A parsed derivative may have another representation but never replacesT. FixtureF is a deterministic binary file larger than 1 MiB containing zero bytes and repeated blocks, with a checked-in fixture recipe and independently calculated expected hash/length. FixtureM retains a synthetic message plus two exact attachment-source revisions. FixtureP is personP with recorded addressA, followed by addressB with later applicability; none is a real identifier.

Oracles use fixture bytes, previously captured API results and independently calculated canonical forms/digests, not private helpers, the same serializer twice or implementation-internal status flags. Record actual request/response bodies, received bytes, selected member revisions, basisUUIDs, operationIDs/incarnations and controlled fault positions without credentials. Compare public behavior and durable restart results; SQL inspection may supplement invariants but cannot replace end-to-end evidence. A failpoint setting is not proof the intended crash happened: retain process/transport/durability evidence.

No acceptance test executes arbitrary stored contract text or source content. Native OpenCloud and retained-payload flows have separate oracles. A reduced managed-route success never proves every native file operation is captured or protected.

## Required journeys and exact outcomes

| ID | Action and independent observation | Required outcome / counterexample caught |
| --- | --- | --- |
| A01 Direct structured text | AdmitT, retrieve exact content, parse only into a separate derivative; restart then retrieve again. | Original bytes including CRLF/key order matchT; derivative has independent identity/basis. JSONB reserialization cannot pass as original. |
| A02 File and native working copy | Explicitly admitF from an owner-authorized stream, edit/restore/delete the ordinary OpenCloud working file, then read retainedF. | Captured payload/hash remains unchanged; native working-file availability is separate; no promise every native edit was admitted. |
| A03 Mixed source | PublishM with DB-inline raw message and two retained file attachments; query before/after each injected fault. | New complete combination appears atomically after final publication; no half-new attachment set is reported as the old/new complete version. |
| A04 Candidate first | Register null-content source and pending lifecycle metadata, fail its later large upload, then resume/complete. | Same sourceID remains; staging finds ordinary metadata, no candidate registry; leaving staging does not delete history; capture completeness remains explicit. |
| A05 Retry versus receipt | Lose committed response; repeat same operation; later register another genuine receipt of the same message. | Transport retry replays one result/publication; later receipt is separately retained without invented independent source. |
| A06 Equal content independent identity | Admit equal-byte sources with distinct provenance; compare hashes. | Hashes match, sourceIDs/provenance do not merge; independent payload ownership remains distinguishable. |
| A07 Concurrency and ABA | Two owner tools mutate same head; then head returns to earlier revision and an old token is retried. | Exactly one conflicting write succeeds; stale selection-publication token conflicts even when revisionID is again equal. |
| A08 Independent attachments | Two owner tools add different binding items at nearby bases. | Both explicit additions survive current selection; source bytes are unchanged and no whole-set last-writer loss occurs. |
| A09 Branch preservation | From selectedR2, store branchR3 parentR1 without selection, then explicitly selectR3. | R2 remains current until CAS selection; R1/R2/R3 histories and prior basis selections remain reconstructible. |
| A10 Definitions and judgments | Revise label meaning, metadata set and vector independently; reassess one assignment, detach another. | Old assignments retain pinned definition meaning; only explicitly advanced bindings change; historical use remains. Confidence belongs to its assignment, not definition or truth. |
| A11 Address history and new use | A historical shipment pins addressA; metadata aboutP gains applicableB; a new action submits manifest usingB. | Shared person identity connects records; historical shipment remainsA; new manifest names actualB; newest timestamp alone is not the action contract. |
| A12 Unrelated publication | Read source combination atB1, publish unrelated item, read atB2. | Different basisUUIDs but equal composition fingerprint and same selected refs; no invented semantic source revision. |
| A13 Unknown references | Register an opaque reference and an incomplete expected attachment; run query with no coverage assessment. | Reference is preserved as reference, bytes not claimed; completeness unknown/incomplete under explicit scope; empty results never prove external nonexistence. |
| A14 Payload faults | TruncateF; exceed declared length; wrong digest; disk full; unsupported directoryfsync/no-replace; zero-length input. | No false publication; ready/failed evidence exact; zero bytes valid; incompatible durability is rejected without fallback. |
| A15 Boundary crashes | Crash before/after filefsync, promotion, ready-row commit and registry commit; destroy connection after successful commit. | Reconciliation finds correct operation/payload, neither overwrites nor auto-purges orphan; public registry is wholly before/after; lost success queries the original result. |
| A16 Upstream mutation | Alter upstream/native file during an explicit received stream without an atomic provider binding guarantee. | Received bytes may be retained exactly; upstream version binding stays UNKNOWN/conflicting, never manufactured from stat/ETag equality. |
| A17 Lifecycle interpretation | Mark ordinary lifecycle pending/failed/withdrawn and later add new work. | Metadata history remains with source; working view changes/re-entry follow its contract; no deletion or completed-byte claim follows a status label. |
| A18 Session revocation | Pause a long response between release units; revoke session; attempt another unit using old authorization/historical snapshot. | Effective revocation commit follows prior release units; zero later units accepted by owned transport, including metadata; old snapshot cannot bypass current checks. |
| A19 Destruction race | Pause reads before their first unit with an old query snapshot, prefetched plaintext, an open descriptor and queued output; destroy the item, finish removal, remove its barrier, then resume. Also race publication/backup, barrier cancellation and a new request after completion/restart/restore. | Exclusive hold linearizes barrier+durable generation changes. Every old read context fails before another protected unit even after barrier removal, cannot refresh its generation, and discards old bytes/descriptors/snapshot/cache. New reads do a fresh existence lookup and cannot obtain removed content. Restore's new incarnation rejects old contexts. No later publication references blocked material; prior delivered units cannot be recalled. |
| A20 Scope and shared copies | With historical R1, current R2 and an unselected branch, request include_versions:false or a revision-only selector; then preview whole-item deletion of a reused component without its outside-scope histories; request physical_media. | include_versions:false returns422 UNSUPPORTED_DESTRUCTION_SCOPE; unknown revision-selector properties return422 INVALID_ENVELOPE. Both reject before plan/guard/barrier/effects; no head-only default. Whole-item preview includes R1/R2/branch and owned payloads. SHARED_DEPENDENCY exposes outside-scope conflicts; unsupported physical guarantee is rejected before effects, without automatic widening. |
| A21 Destruction with backups and receipts | Execute owner-approved scope, advancing generation from G to G+1; observe the first202 receipt, independently preserve/confirm its anchor, then leave one backup unreachable. Lose the execute/confirmation reply, recover by receipt GET keyed by the already known execute operation UUID (without a received job-ID), and retry exact execute. Race another generation mutation at receipt release; try injecting old source bytes into the receipt. | The mandatory first acknowledgment is a closed post-commit CustodyControlReceipt, not409 solely because its own mutation advanced generation. It is freshly read under locks held through release, contains only allowed control fields and cannot reuse/retag old source buffers. Concurrent generation mutation waits for that bounded release or precedes its fresh read. Lost responses recover the durable job/anchor without duplicate effects; revoked/expired sessions release no receipt. Until independent anchor confirmation, deletion remains pending. Active removal may succeed later but the whole job remains pending_copies while one copy is unreachable; no completed all-copy claim. |
| A22 Backup consistency | Capture exported DB snapshot while new objects publish; crash during file copying; restore a completed backup. | Incomplete capture lacks complete marker. Complete backup restores all exact referenced files/history for its snapshot and excludes later additions; roles/config/secrets requirements explicit. |
| A23 Restore identity and replay | Restore at earlier cutoff; replay old write/cursor token and query a missing old publicationUUID after new commits. | New incarnation rejects replay; missing basis explicit, never mapped by reusedordinal; surviving UUID references resolve unchanged; outbox effects reconcile before writes reopen. |
| A24 Guard rollback | Supply a valid older HMAC journal and an independently held newer freshness anchor; also test missing anchor/key. | Valid signatures alone do not prove latest; stale/missing freshness authority keeps restore offline. Old backup cannot silently reactivate destroyed content. |
| A25 Generic safety and limits | Submit stored script, remote schema ref, cyclic semantic relationship, cyclic containment, malformed roles/FKs, over-limit batch and JSON containing escaped U+0000 in a nested value and property name. Also submit malformed UTF-8/unpaired surrogates; separately admit the original offending document as exact Payload bytes under a valid source envelope. | Script/unknown contract inert; semantic cycles preserved, containment cycles rejected. UTF-8 deployment/profile admission is checked; offending structured envelopes return422 INVALID_ENVELOPE with safe reason/pointer before intent/payload/publication. No replacement or silent normalization. The separate raw-byte admission retrieves byte-for-byte original content, including binary zero bytes, after restart. Existing candidate/history remains unchanged by rejected requests. |
| A26 Control bootstrap/rotation | Create owner session; rotate using new client-known secret; lose response; use old then new secret; pause old-key session creation across rotation. | Old control/session credentials fail; new key resolves generation; secret plaintext absent from operation intents/logs; no unauthenticated network bootstrap; an old-key create cannot insert an unrevoked session after rotation. |

Each crash journey must be tested after process restart with real PostgreSQL/filesystem adapters as well as a deterministic unit-level failure model. The read/write operation contracts are public seams; no regression test calls private implementation methods or merely asserts a table declaration. The source-specific intake adapter and external consumer semantics require their own future tests and cannot be inferred from these storage tests.

## Requirement and research coverage

| Requirement family | Normative contract and acceptance coverage |
| --- | --- |
| P01–P05, P34: breadth, origin, originals, generic registration | Model roles/raw payloads/references; A01–A06,A13,A25. |
| P06–P11, P20–P24: attributable meaning, exactness, identity, contract revision, validity | Exact refs, role/profile validation, branch/head selection and metadata sets; A06–A12,A25. |
| P12,P18,P22,P31–P32: durability, repeated intake, completeness and partial usability | Prepare/publish custody, explicit evidence and partial views; A03–A05,A13–A16,A22. |
| P13–P17,P19,P30,P39: owner control, authorized scope, preservation/destruction and revocation | Owner sessions, bounded release, explicit preview/execute, no entity-rights graph; A17–A24,A26. |
| P25–P29,P33,P35–P38: historical results, context, label origin/application, contract boundary, lifecycle | Pinned component refs, manifests, inert contracts and ordinary lifecycle metadata; A04,A09–A13,A17,A25. |
| Research: mixed stores, concurrent change, lost responses and recovery | Atomic registry publication after durable preparation; A02–A03,A07–A09,A14–A16,A19,A22–A24. |
| Research: reuse without old-trial adoption | OpenCloud working-copy and PostgreSQL/retained-file boundary; A02,A16 and native dependency admission below. |

No cell is a PASS statement. Independent QA reviews design feasibility and research conformity first; implementation evidence must later establish each oracle on exact admitted revisions/platforms.

## Implementation admission and evidence boundaries

Before application tests can count as proof, Planning must bind the selected implementation language/framework/driver and native test/check rules under the repository policy; this Design does not execute or choose an incidental harness runtime. Record PostgreSQL 18 full patch/build/OCI digest, required settings, actual filesystem/kernel and rename/fsync behavior, storage limits, core-contract/validator versions and any OpenCloud/reva adapter versions. Pin actual approved dependencies rather than silently using rolling latest. The core JSON/HTTP/relational contracts remain implementable without requiring an ANN database, new event store, model or UI framework.

Required admission proofs include native constraint rejection, role privileges, synchronous crash recovery, directory/file durability, no-replace promotion, memory-bounded upload/read, UTF-8/JSONB profile admission and raw-byte fallback, session/custody release-generation fencing and backup/restore reconstruction. A host failing a required primitive is unsupported until a conforming adapter is provided; a placeholder 'healthy' service or schema validation cannot waive the contract.

These are planned native proofs, not an unresolved choice of semantics. This documentation task executes only the required offline Markdown checks and privacy/readback review. No application benchmark, fault scenario, source import, model comparison or NAS operation has been executed. Main-design review status and a passing Markdown check do not mean product readiness.

## Related Documents

- [Design](<design.md>)
- [Model](<storage-model.md>)
- [Operations](<storage-operations.md>)
- [Preservation and recovery](<storage-preservation.md>)
- [Research expectations](<research.md#expected-results>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-28 | Codex (@imp designer) | Specify synthetic end-to-end oracles, failure injection and ADR/Research traceability for the complete storage contract. |
| 1.1 | 2026-10-28 | Codex (@imp designer) | Extend A19/A20/A25 for paused old reads after barrier removal, unsupported partial-version destruction and JSONB-incompatible text with exact raw retention. |
| 1.2 | 2026-10-28 | Codex (@imp designer) | Extend A21 to prove first post-commit control acknowledgment, lost-response recovery and continued exclusion of old source buffers. |
