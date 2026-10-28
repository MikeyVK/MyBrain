<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Storage registration model and constraints

**Status:** Design working draft — model checkpoint  
**Version:** 1.0  
**Last Updated:** 2026-10-28

## Purpose

Specify the logical records, typed payloads and PostgreSQL constraints needed to implement MyBrain registration without copying whole source descriptions for each change.

## Summary

One owner, one registry database, immutable revisions and transactional head-selection history. A source's combined historical state is (source item, published commit); unchanged components are shared by exact reference. An explicit result manifest freezes the revisions actually used. No custom persistent-tree or event-replay engine is required.

## Scalar and null conventions

All IDs are application-generated UUIDv4 strings, lowercase canonical spelling; the database type is uuid. IDs identify records, never imply equality of content or identity outside MyBrain. CommitId is a positive signed bigint rendered as a decimal JSON string, avoiding JSON precision loss. UtcTime is an RFC3339 UTC string with microsecond precision, stored as timestamptz. Hash is lowercase SHA-256 hex over an explicitly defined byte input. Unknown optional information is JSON null; absent required members, duplicate JSON keys, NaN/Infinity, unsafe integers and unrecognized core-envelope properties are rejected. Optional extension content lives only in the declared attributes object. Empty bytes, empty lists and empty text are valid and distinct from null.

The component body is encoded as canonical UTF-8 using RFC8785 JCS profile mybrain-jcs/1. Decimal values needing more than IEEE754 precision use decimal strings under their contract; dates and large identifiers are strings. Canonicalization is for descriptions/requests only. It never replaces exact received source bytes, which are retained as a Payload. The same bytes in two items never merge their identities. Canonical-body equality may permit explicit reuse, not silent coalescing. See [RFC8785](https://www.rfc-editor.org/rfc/rfc8785.html).

## Registry tables

This is a relational contract, not an executable migration. All ordinary writes use the publisher; physical migrations and privileged destruction are separate capabilities. NOT NULL is the default below; '?' is the only nullable marker. No ON DELETE CASCADE is permitted for ordinary records.

| Table | Columns | Keys and constraints |
| --- | --- | --- |
| registry_clock | singleton smallint=1, last_commit bigint>=0 | PK(singleton); one row locked before publishing; sequence allocation is not a commit clock. |
| publication | commit_id bigint>0, operation_id uuid, recorded_at timestamptz | PK(commit_id), UNIQUE(operation_id); FK operation; timestamp is observation, not ordering authority. |
| item | item_id uuid, role text, created_commit bigint, head_revision uuid?, head_commit bigint? | PK(item_id); role in source/metadata/definition/assignment/relationship/representation/contract/receipt/package/binding/manifest; role immutable; head non-null at commit for an ordinary item. |
| revision | revision_id uuid, item_id uuid, parent_revision uuid?, contract_revision uuid?, canonical_body bytea, body jsonb, body_hash bytea, commit_id bigint | PK(revision_id), UNIQUE(item_id,revision_id), UNIQUE(item_id,commit_id); hash octet_length=32; jsonb object; FK item/publication; parent/head composite FK to same item's revision, DEFERRABLE INITIALLY DEFERRED. |
| head_selection | item_id uuid, commit_id bigint, revision_id uuid | PK(item_id,commit_id); FK(item_id,revision_id) to revision; append-only. Every new item or head change inserts exactly one row and updates item.head_revision in the same transaction. |
| revision_edge | from_revision uuid, field text, ordinal int>=0, target_item uuid, target_revision uuid? | PK(from_revision,field,ordinal); FK from revision; target item FK; exact targets use composite FK(target_item,target_revision); null target_revision means identity-only. |
| binding_index | revision_id uuid, subject_item uuid, subject_content_revision uuid?, slot text, member_item uuid, member_revision uuid, attached boolean | PK/FK revision; subject FK; optional exact subject revision belongs to subject; member composite FK; reflects the canonical binding body exactly. |
| payload | payload_id uuid, owner_item uuid, backend text, byte_length bigint>=0, sha256 bytea, inline_bytes bytea?, retained_key text?, prepared_operation uuid | PK(payload_id), UNIQUE(owner_item,payload_id); backend inline/retained-file; exactly one body location matches backend; bytea hash length32; inline length equals byte_length; retained_key server-generated and unique. |
| operation | operation_id uuid, request_hash bytea, request_body jsonb, state text, result jsonb?, publication_commit bigint?, created_at/updated_at timestamptz | PK(operation_id); state prepared/receiving/ready/committed/failed/in_doubt; committed iff publication_commit and result are set. State is recovery machinery, not source lifecycle taxonomy. |
| operation_attempt | operation_id uuid, attempt_no bigint, fencing_token uuid, outcome jsonb?, observed_at timestamptz | PK(operation_id,attempt_no); current attempt fenced by operation row lock. Immutable completed-attempt evidence; no unbounded blind retries. |
| outbox | task_id uuid, operation_id uuid, kind text, target jsonb, completed_at timestamptz? | PK(task_id); unique logical task key; publication-time insertion; adapters never infer authority from arbitrary source text. |

FKs cannot establish cross-row semantic constraints alone. The publisher validates canonical bytes/hash against body, same-item parent/head lineage, role/profile compatibility, edge extraction, binding projection, exact referenced closure and payload preparedness while holding the publication lock. It rejects missing, future or destruction-blocked references. Pinned-revision dependency edges must be acyclic; identity-only relationships may be cyclic. Batch references are validated by a bounded graph traversal (100,000 visited nodes/edges); larger requests return LIMIT_EXCEEDED before publication. Historical revisions do not become current solely by creation; explicit head changes are mandatory. item.head_commit is the commit_id of its most recent head_selection, including a selection that returns to an older revision. CAS compares both expected_revision and expected_head_commit (null/null only for an absent item), preventing ABA stale writes. New revisions parent the selected expected head; an explicit select-existing operation may choose an older revision without pretending its prior intermediate history disappeared.

The ordinary database role cannot UPDATE/DELETE immutable publication, revision, head_selection or completed attempt rows; it cannot execute DDL. Only the controlled publisher/maintenance interfaces receive the required narrowly scoped DB privileges. A transaction guard verifies exactly one publication marker for all immutable changes and consistent head projections. Privileged administrators remain trusted; this is not WORM or protection against host takeover.

## Typed revision bodies

Every row below defines a closed core object. Array order is preserved. Exactly referenced targets carry both item_id and revision_id; storage verifies ownership. The revision envelope supplies item/parent/contract/commit; bodies do not repeat those fields.

| Role | Required body members and cardinality | Optional/nullable members and interpretation |
| --- | --- | --- |
| source | content: ContentOrNull; parts: Part[0..10000] | attributes: object defaults {}; source type is not fixed by the envelope. Produced context is an ordinary source with declared derived origin. |
| metadata | attributes: object; basis: ExactRef[0..10000] | Observations versus supplied claims are explicitly distinguished by the governing metadata contract, never inferred from value shape. |
| definition | name: nonempty string; meaning_payload: PayloadRef; origin: Origin | Origin = known exact source/context reference(s), or unknown with an explicit reason. New definitions retain origin; reuse does not replace it. |
| assignment | definition: ExactRef; target: ItemOrExactRef; assessment: object; basis: ExactRef[0..10000] | confidence: {value: finite number, scale: ExactRef} or null. Scale is contract-described, not automatically probability. Assessment vocabulary/applicability is declared by contract; no universal truth flag. |
| relationship | predicate: ExactRef; from: ItemOrExactRef; to: ItemOrExactRef; attributes: object | It may link identity or pin versions; pinned targets are never silently advanced. |
| representation | input: ExactRef[1..10000]; method: ExactRef; payload: PayloadRef; attributes: object | For vectors attributes must declare model/version identity, dimension>0, scalar_encoding float32/float64, and coordinate-space contract. Payload length and finite values must match that contract; compatible comparison is a separate operation. |
| contract | name: nonempty string; document: PayloadRef; format: nonempty string | Registration stores the contract as data. No automatic code loading, network schema resolution or activation occurs. |
| receipt | observed_at: UtcTimeOrNull; connection: opaque nonempty string; claims: object; matches: ExactRef[0..10000] | package: ItemOrExactRefOrNull; recognition_contract: ExactRefOrNull; upstream_binding: {status: verified/unknown/conflicting, evidence: ExactRef[]} required. A later receipt is independent from a transport retry. |
| package | claims: object; contents: ItemOrExactRef[0..10000]; expected_scope: object | Scope/completeness evidence belongs to ordinary descriptions; a package need not correspond one-to-one with a source. |
| binding | subject: ItemOrExactRef; slot: metadata/label/representation/relationship/basis; member: ExactRef; attached: boolean | subject exact revision limits the attachment to that content state; identity-only subject spans states until explicitly revised/withdrawn. The binding's history is independent. |
| manifest | source: ItemOrExactRef; basis_commit: CommitId; members: ExactRef[0..10000]; purpose: nonempty string | records the actual selected members/result inputs, not an automatically expanded person's whole profile. |

ContentOrNull is null (no content admitted yet), {mode:retained,payload:PayloadRef}, or {mode:reference,locator:nonempty string}. A reference locator is opaque stored data, never automatically fetched; its availability/integrity assertions need evidence. Part = {position:nonnegative integer, role:nonempty string, target:ExactRef}; positions are unique within a source revision. A mixed email can retain raw message bytes and pin exact attachment-source revisions. Unknown or missing external parts can be represented by pinned candidate source revisions with null content, never by pretending their bytes exist. PayloadRef = {owner_item:UUID,payload_id:UUID}; no consumer-supplied storage path.

A record itself is digitally representable and can be a target of descriptions; a contract or definition can also be preserved as a raw source before semantic registration. The finite structural roles are service envelope types, not prescribed content categories or label meanings. Contract extensions use attributes or a new admitted structural profile, preserving existing schemas; malformed core objects are never silently accepted.

## Contracts, definitions and attachments

Every non-contract revision pins a governing contract revision. The contract revision FK is null only on a contract record, validated by the built-in contract-envelope/1 profile; this terminates bootstrap recursion. Bootstrap installs exact canonical core-contract documents as contract items and binds those revision IDs to known validators in trusted deployment configuration. All other contract text is inert until an explicit authorized admission maps it to a compatible trusted validator. Stored scripts cannot execute. Imported unknown formats remain raw source content or inert contract records; an unsupported typed write returns CONTRACT_NOT_ADMITTED, preserving universal raw registrability.

Definition is not application. An assignment pins the definition revision whose meaning was used. Advancing a definition head does not migrate assignments. Reassessment creates a new assignment revision and, only when explicitly requested, advances relevant binding(s) in the same publication. Withdrawal creates a new detached binding revision; it does not erase old assignments. User corrections are new attributed revisions; autonomous consumers must name their basis and expected heads.

Descriptions are reusable as exact metadata-set revisions. Sharing a set does not share future edits: a later set revision affects a source only through an explicit binding-head change. Lifecycle is ordinary contract-described metadata on the same source, including after admission. No separate candidate registry or intake database exists. Staging is a read-only selector over selected current metadata; its membership neither proves preservation nor authorizes processing/destruction. Reconciliation records evidence; it does not reinterpret a pending lifecycle label as completed work.

## Combined versions and current views

All successful publications are serialized by registry_clock. In a REPEATABLE READ, READ ONLY transaction, take a visible basis B=registry_clock.last_commit, then resolve each item's head as the head_selection with maximum commit_id<=B. One transaction's partial state is never visible. A source's registered combined version is (source_item_id,B); its source content is the selected source revision, plus selected current binding revisions for that source and exact selected source version. An identity-targeted binding applies across source content revisions until detached; exact-targeted bindings are limited to the matching source revision. Return pinned member revisions, never substitute member item heads. Historical lookup uses the same algorithm for an explicit retained basis B, subject to current authorization and destruction barriers.

No new row is required for every unchanged source whenever B advances. A component change stores only its new revision, head_selection and expressly changed bindings. Current views choose the newest visible B and may apply explicit caller selectors under their stored contract; storage does not choose semantic truth or automatically pick the newest address. If a new action uses address B instead of historical address A, the consumer selects under its action contract and submits a new manifest/source with the actual used revisions.

For stable pagination or an actual execution record, create an explicit immutable manifest whose exact members are selected under one visible B. A later query is not proof an earlier result existed. The common read returns its basis and actual member refs even if no result manifest is persisted. Historical combined views can later become partially unavailable after explicit destruction; the service reports that loss rather than silently reconstructing with new values.

## Indexes and storage sizes

Required B-tree indexes: revision(item_id,commit_id), head_selection(item_id,commit_id DESC), binding_index(subject_item,subject_content_revision), revision_edge(target_item,target_revision), publication(operation_id), payload(owner_item), operation(state,updated_at), outbox(completed_at). Add GIN jsonb_path_ops on metadata body attributes for explicitly supported equality/containment filters. Body/inline bytes are not duplicated into logs or operation outcomes. Source plaintext search/vector nearest-neighbor indexes are replaceable derived consumers, not an additional authority or mandatory dependency; exact ID/metadata/label retrieval is defined in the operation contract.

Inline content is limited to 1 MiB per payload; larger content always uses retained files. The threshold selects a backend, not a semantic source class. A generic retained-file stream supports up to the signed bigint byte-count range subject to configured free-space/quota admission; the wire API has explicit declared length and bounded buffers. Core JSON envelope maximum is 4 MiB, batch at most1,000 item revisions and10,000 parts/refs per body, with the graph bound above. A larger source remains registrable through file payload and opaque media type; it is not silently truncated into JSON. Ordinary commands return explicit LIMIT_EXCEEDED or INSUFFICIENT_STORAGE before claiming success.

PostgreSQL18 core is sufficient: uuid, bytea, jsonb, constraints, indexes and transactional locking. No specialized temporal/vector extension is required by this registration baseline. This is not a claim of unbounded throughput; serial publication favors correctness and simplicity for one personal brain. Benchmarks during implementation must report limits rather than silently weaken ordering.

## Related Documents

- [Design entry point](<design.md>)
- [Accepted principles](<../../architecture/decisions/0001-digital-brain-foundational-principles.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-28 | Codex (@imp designer) | Define implementable immutable registration, component and historical-view contracts. |
