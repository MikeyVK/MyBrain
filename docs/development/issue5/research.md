<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Research: lossless private email ingestion trial

**Status:** DRAFT — research complete for independent review; no phase approval claimed  
**Version:** 1.0  
**Last Updated:** 2026-10-22

## Purpose

Establish evidence, constraints and compatibility boundaries for the bounded trial in issue #5. This document does not select a production architecture.

## Scope In

The existing fixed sample of three conversations and eight messages; complete source preservation; private storage; separate provenance-bearing derivations; repeat import; resumable processing; archive-only retrieval.

## Scope Out

Mailbox changes, broader discovery, unselected chat/documents/photos, external AI uploads, UI, deployment, final platform selection, database replacement and production migration.

## Problem Statement

Connector access is transient access to source material, not a durable self-managed archive. The owner authorized saving the complete selected emails and verifying their recovery without source-data loss. A private PostgreSQL instance exists, but no message content or application schema has been imported.

## Goals

- Determine what source fidelity can be established at the connector boundary without treating a rendered message or a regenerated MIME document as the original.
- Separate preservation, extraction, interpretation and accepted correction; evaluate storage routes without deciding a general application architecture.
- Identify observable success and failure criteria, affected consumers and compatibility/migration constraints before Design.

## Background

The repository is a research-stage project with a development harness, public research and documentation/configuration policy; it has no existing ingestion application, schema, API, application tests or approved application quality bindings. The public research baseline is conceptual background, not an approved stack. The owner's bounded choices are reflected in issue #5; private source references and local runtime details are deliberately absent from this document.

## Findings

### Current evidence and limits

| Observation | Meaning |
| --- | --- |
| The fixed selection is resumable through a private selection manifest containing eight unique message references and a declared conversation count of three. | Selection metadata is not source preservation. Later acquisition must use that exact selection; it must not search for a replacement sample. |
| Native SQL against the existing private instance reported PostgreSQL 18.6 and zero non-system tables. The instance was stopped after the check. | The engine exists; an application schema and mail archive do not. |
| The admitted Gmail connector exposes `read_email(format="raw")` and parsed MIME reads. | A raw read is available; a successful tool envelope alone does not prove untruncated transport or durable storage. |
| Earlier source observations included multipart/HTML content and inline media. | Plain text alone cannot meet the full-source requirement. No claim of attachment completeness or semantic accuracy has yet been established. |

### Source fidelity and processing boundary

Gmail documents `raw` as the entire RFC 2822 message encoded in base64url, and exposes provider identity, thread identity and other metadata separately. Its message size is an estimate, so equality with that estimate cannot certify completeness. The preservation target is the exact decoded byte sequence returned by Gmail, not an unverifiable earlier sender-side wire image. The connector's complete structured result must be inspected privately for explicit truncation, errors or omitted raw content; never copy a shortened display into an archive. [Gmail message resource](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages)

There are two encoding layers: the provider's base64url envelope and MIME Content-Transfer-Encoding inside the mail. MIME decoding yields derived part bytes and subsequent charset decoding yields derived text; neither operation authorizes rewriting the original mail bytes. MIME permits nested multipart structure and preamble/epilogue data. A rendered body or a parser's reserialization is therefore insufficient evidence of byte preservation. [RFC 2045](https://www.rfc-editor.org/rfc/rfc2045), [RFC 2046](https://www.rfc-editor.org/rfc/rfc2046)

A parsed Gmail part may carry an attachment reference rather than body data; Gmail supplies an unencoded part-byte size. The trial must reconcile every inline and attachment-bearing part with archived bytes and retrieve a selected message's separately exposed attachment only when required. External linked targets are outside this import scope; keep links as source content and report their targets as unarchived. [Gmail attachment resource](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages.attachments)

Python's standard email parser accepts bytes and exposes MIME structures and parsing defects. It is a candidate for extraction, not proof of universal interpretation. Parser defects, unsupported media and charset failures must remain visible without discarding a successfully archived source. Extracted reply links are claims derived from headers; unresolved or ambiguous targets must remain unresolved. A proposed conversation description is not an accepted fact. [Python parser](https://docs.python.org/3/library/email.parser.html)

### Small storage-route comparison

| Candidate within the existing private PostgreSQL trial | Cost and risk | Consumer impact |
| --- | --- | --- |
| Raw bytes in PostgreSQL binary storage, with separate registration and derivation data | One transactional store can simplify this small sample's consistency and recovery; binary growth increases database/backup volume. | Archive readers use the database; the trial does not establish suitability for large future media. |
| Private immutable files plus PostgreSQL registration | Natural fit for larger files; coordinating durable file writes and database registration adds orphan/missing-file recovery work. | Readers must recover both catalogue and files; a path or URL alone is not an archive. |
| Parsed bodies or JSON metadata as the only source store | Low initial effort, but loses exact headers, MIME structure or content; violates owner criteria. | Cannot supply full-source recovery; excluded by the approved preservation boundary. |

PostgreSQL `bytea` represents arbitrary byte sequences. `jsonb` provides flexible structured values but changes JSON representation, including key order and duplicates; it cannot stand in for the original message bytes. These are candidate capabilities, not a chosen table layout or a production recommendation. [Binary types](https://www.postgresql.org/docs/18/datatype-binary.html), [JSON types](https://www.postgresql.org/docs/18/datatype-json.html)

Database uniqueness and conflict handling can support repeat import, but do not define source identity by themselves. Distinguish provider identity, byte identity, metadata observations and processor-run identity. Re-reading identical bytes must not create a new source version; changing an extraction must not masquerade as a changed source. Unexpected different bytes for the same provider identity require retained evidence and an explicit conflict/version outcome, never silent replacement. [PostgreSQL INSERT](https://www.postgresql.org/docs/18/sql-insert.html)

### Blast radius

| Surface | Current boundary and likely impact |
| --- | --- |
| Production code, schema and public API | None exists for ingestion; no deployed consumer or data migration has been identified. New trial interfaces remain a Design concern. |
| Existing private runtime | Preserve the provisioned engine, empty database and fixed selection. No replacement, reinitialization or other database/service change. |
| Configuration and helpers | Existing PGMCP and quality bindings remain supported contracts. Future application/runtime configuration must not contain tracked credentials or private paths. |
| Tests | No application suite or bindings are approved. Meaningful synthetic checks for byte integrity, deduplication, MIME completeness and correction protection will require an explicit proportionate test admission before implementation; private acceptance checks report aggregates only. |
| Documentation | New public-safe issue deliverables; maintained repository agreements remain authoritative. No private evidence enters docs, state, deliverables, commits or attachments. |
| Agents, templates and enforcement | Existing role separation, native tools and phase reviews apply; no protocol/template/enforcement change is needed. |
| Downstream consumers | The owner reviews an aggregate trial report and retrieves a private archive. Search, future processors and UI must not become required dependencies of source recovery. |

## Questions

- Can the connector-to-private-storage path prove untruncated raw acquisition and MIME/attachment reconciliation for every selected message? Any omission must be surfaced rather than reconstructed.
- Which of the two viable raw-storage routes gives the smallest auditable recovery boundary for this sample? Design must decide without committing the product's future large-file architecture.
- What exact identity, correction-protection and failure/resume contracts provide meaningful verification? Design and Planning must define them before implementation.
- Application tests remain deferred by repository policy. Co must obtain the necessary bounded test admission/quality decision before application implementation; a disabled suite is not passing evidence.

## References

- [Issue #5 and acceptance criteria](<https://github.com/MikeyVK/MyBrain/issues/5>)
- [Repository working agreements](<../../../README.md#working-agreements>)
- [Repository quality policy](<../../../README.md#quality-policy>)
- [Portable quality bindings](<../../../setup/quality/checks.yaml>)
- [Gmail message resource](<https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages>)
- [Gmail message retrieval](<https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages/get>)
- [Gmail MIME body and attachment resource](<https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages.attachments>)
- [MIME transfer encodings: RFC 2045](<https://www.rfc-editor.org/rfc/rfc2045>)
- [MIME multipart structure: RFC 2046](<https://www.rfc-editor.org/rfc/rfc2046>)
- [Python byte-oriented email parsing](<https://docs.python.org/3/library/email.parser.html>)
- [PostgreSQL binary data](<https://www.postgresql.org/docs/18/datatype-binary.html>)
- [PostgreSQL JSON types](<https://www.postgresql.org/docs/18/datatype-json.html>)
- [PostgreSQL INSERT and conflict handling](<https://www.postgresql.org/docs/18/sql-insert.html>)

## Approved Strategy

The following strategy boundaries are owner-approved for this bounded experiment, derived from the explicit full-mail storage instruction, the isolated existing PostgreSQL trial and the fixed-sample/no-mailbox-change scope in [issue #5](https://github.com/MikeyVK/MyBrain/issues/5). This approval does not extend to a final production architecture.

| Boundary | Approved strategy and rationale | Alternatives and impact |
| --- | --- | --- |
| Existing application contracts and migration | Add an isolated private trial; preserve supported repository/harness contracts and the existing private database. No application consumer or source dataset is being migrated. | Replacing the database or changing harness contracts creates unrelated compatibility and recovery obligations; excluded. |
| Source fidelity | Preserve complete immutable raw source bytes and separate provider observations. No content normalization or parser reconstruction may replace the source. | Text-only storage is cheaper but loses required information; excluded. |
| Source/derivation/correction semantics | Preserve source-version provenance; keep extraction and proposed interpretation distinct from accepted facts/corrections; reprocessing may not overwrite accepted corrections. | In-place regeneration is simpler but changes accepted meaning invisibly; excluded. |
| Scope and side effects | Use only the fixed selection, keep Gmail unchanged, store operational content privately outside the repository and avoid external AI uploads. | Wider discovery or external processing expands exposure and authorization; excluded. |

No destructive migration, bridge or compatibility break is needed for these observed boundaries. Physical source placement, schema/interfaces, deduplication keys and bounded processor/error contracts remain Design decisions within the approved strategy. New evidence of a deployed consumer, an existing populated schema or a necessary compatibility break must return to Co for a strategy decision before that boundary proceeds.

## Expected Results

The acceptance evidence must distinguish source acquisition, durable storage, extraction and semantic claims:

- All eight selected messages are durably archived with full headers, MIME structure and embedded content. Record byte counts and cryptographic digests privately; demonstrate byte-for-byte equality after storage read-back for every message.
- Inventory and reconcile every MIME part, including inline media and nested parts, with required separately fetched content where applicable. Structural parse success and a matching storage digest prove neither original acquisition completeness nor attachment reconciliation. Explicitly truncated responses, missing parts or an unresolved transfer path prevent a full-import claim; successful archive read-back must not hide those failures.
- Retrieve all archived sources with connector acquisition disabled. Repeating the identical import leaves source and source-version counts unchanged while retaining traceable attempt outcomes.
- Reprocessing creates traceable versioned derivations or an explicit unchanged result, never a new source version merely because interpretation changed. Extracted text, reply relationships and proposed context each reference source version and processor version.
- A controlled correction-protection check demonstrates that reprocessing preserves an accepted correction. A synthetic test correction must be explicitly test data, never represented as an actual owner-accepted fact about the mail.
- An interrupted or failed processing attempt remains visible and can resume without loss or duplicate source records. Unknown/unsupported content retains source registration and archived bytes.
- Public evidence contains only aggregates and technical outcomes. Private locations, identifiers, source excerpts and identifying derivations remain outside repository/workflow artifacts. Genuine semantic quality and production recovery/security are not established by this sample.

## Evidence

### Existing private engine is real; import has not occurred

Bounded administrative inspection of the existing dedicated cluster, with credentials read privately and no schema writes. Neither private names nor paths are copied here.

- [Issue #5 and acceptance criteria](<https://github.com/MikeyVK/MyBrain/issues/5>)
- [Repository working agreements](<../../../README.md#working-agreements>)

**Invocation:** psql (read-only): SELECT current_database(); SELECT version(); SELECT count(*) FROM information_schema.tables WHERE table_schema NOT IN ('pg_catalog','information_schema'); SHOW listen_addresses; SHOW port; SHOW password_encryption; then pg_ctl stop/status on that dedicated instance.

**Observed Result:** Database connection succeeded; PostgreSQL 18.6; non-system tables=0; loopback-only; SCRAM; stop exit=0; final pg_ctl status exit=3 (not running).

### No ingestion application consumer is present in this starting snapshot

Repository inventory contains research, issue documentation, quality/PGMCP sources and harness lockfiles, with no ingestion source/test roots or application schema.

- [Repository working agreements](<../../../README.md#working-agreements>)
- [Repository quality policy](<../../../README.md#quality-policy>)
- [Portable quality bindings](<../../../setup/quality/checks.yaml>)

**Invocation:** rg --files excluding private/local server/runtime/environment directories; read README working agreements and quality policy.

**Observed Result:** No existing application API/schema migration identified. Inactive application tests remain an explicit policy boundary.

## Assumptions

- This trial evaluates the selected sample only. Connector capabilities and successful local SQL checks do not establish production readiness, comprehensive mailbox coverage, backups or semantic correctness.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-22 | @imp researcher | Document source-fidelity evidence, storage options, approved scope/compatibility strategy and unresolved Design/quality questions for issue #5. |
