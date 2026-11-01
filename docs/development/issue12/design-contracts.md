<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# e-Boekhouden MCP boundary contracts

**Status:** HISTORICAL REVIEWED CONTRACTS — NOT CURRENT IMPLEMENTATION BASIS

The owner has reopened the functional scope and provider-route strategy. The prior Design GO at revision `1d2fc8da06ac41c49134e5ee1bc67e1a347413b5` remains historical evidence, not authority to implement this workflow-shaped design. Consult the [current per-function coverage research](api-functional-coverage.md) and [expanded APK contracts](apk-api-contracts.md) before a replacement strategy/design. No implementation or account operation is authorized by this document.

## Purpose

Specify immutable public contracts and narrow ports for the proposed local server. These are design declarations, not executable implementation.

The core accepts explicit business choices and frozen evidence. It never receives an untyped provider object, credentials, arbitrary URLs or caller-selected filesystem paths. Command ports return None; result queries expose separately persisted receipts.

## Declaration conventions

The following Python declarations specify Pydantic v2 contracts. Ellipses in Protocol signatures mean abstract declarations; no method bodies are supplied. Implementations must enforce the stated cross-field invariants at model/application boundaries. They may not substitute coercive float arithmetic or raw dictionaries. All nested collections are tuples of frozen models. Provider DTOs are private to adapters; unknown provider fields are preserved only in private redacted observations, and block writes until classified. Public inputs reject extra keys. Money and quantity are JSON strings, not JSON floating numbers. Dates use ISO calendar dates and identifiers never share a numeric alias across namespaces.

```python
from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Annotated, Literal, Protocol
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class FrozenModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

PositiveId = Annotated[int, Field(gt=0)]
Digest = Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
InvoiceNumber = Annotated[str, Field(min_length=1, max_length=100)]
HeaderText = Annotated[str, Field(min_length=1, max_length=50)]
MoneyText = Annotated[str, Field(pattern=r"^-?(0|[1-9][0-9]{0,15})\.[0-9]{2}$")]
Money = MoneyText
HoursNumber = Annotated[str, Field(pattern=r"^-?(0|[1-9][0-9]{0,5})(\.[0-9]{1,2})?$")]
Int32Id = Annotated[int, Field(ge=1, le=2147483647)]

class AdministrationBinding(FrozenModel):
    profile: str
    expected_app_administration: PositiveId
    owner_confirmed_rest_identity: str
    credential_version_seal_ref: str
    rest_credential_ref: str
    app_credential_ref: str
    binding_digest: Digest

class VisibleMutation(FrozenModel):
    number: PositiveId

class AppVersion(FrozenModel):
    internal_id: PositiveId
    visible: VisibleMutation

class FileIdentity(FrozenModel):
    file_id: PositiveId
    directory_id: Annotated[int, Field(ge=0)]

class ReceivedIdentity(FrozenModel):
    namespace: Literal["visible_mutation", "app_internal", "archive_file", "relation", "hour", "opaque_link_reference", "unknown_provider"]
    value: PositiveId
    verified: bool

class LinkReference(FrozenModel):
    response_reference: PositiveId
    semantics: Literal["opaque_association_reference"]
```

Credential references are local configuration only and never tool-result fields. AdministrationBinding is internal: tool inputs supply a configured profile alias. REST token-to-administration binding is configured provenance; it is not falsely described as a server-verified App administration. An App operation additionally verifies current user-info administration. A visible mutation number is never substituted for an internal App version ID. Link request target is the visible number; returned association reference has no assumed unlink meaning.
Public MoneyText is deliberately a strict string JSON schema. A pure boundary parser converts it once to finite Decimal for domain arithmetic, with no float intermediary; output serializer returns exactly two decimal places. Pydantic strict Decimal is not used as the tool JSON field. HoursNumber is separately parsed to Decimal with absolute value <=100000 and at most two decimals; monetary cent quantization is not imposed on hours.

## Snapshots, coverage and source choices

```python
class Coverage(FrozenModel):
    complete: bool
    pages: Annotated[int, Field(ge=0)]
    items: Annotated[int, Field(ge=0)]
    limit_reached: bool
    continuation: str | None
    stop_reason: str | None

class EvidenceRef(FrozenModel):
    evidence_id: UUID
    sha256: Digest
    captured_at: datetime
    schema_version: Literal["1"]
    binding_digest: Digest

class ObservationState(StrEnum):
    PRESENT = "present"
    NOT_RETURNED = "not_returned_by_api"
    UNKNOWN = "unknown"

class Outstanding(FrozenModel):
    state: ObservationState
    mutation: VisibleMutation
    relation_id: PositiveId
    total: Money | None
    paid: Money | None
    open: Money | None
    evidence: EvidenceRef

class SourceDescription(FrozenModel):
    full_text: str
    approved_header: HeaderText
    shortening_reason: str | None
    source_digest: Digest
    choice_provenance: str

class RowVat(FrozenModel):
    state: ObservationState
    amount: Money | None

class MutationRow(FrozenModel):
    index: Annotated[int, Field(ge=0)]
    provider_row_id: PositiveId | None
    ledger_id: PositiveId | None
    relation_id: PositiveId | None
    invoice_number: InvoiceNumber | None
    cost_center_id: PositiveId | None
    description: str | None
    amount: Money | None
    vat_code: str | None
    vat: RowVat
    not_returned_fields: tuple[str, ...]

class VatGroup(FrozenModel):
    code: str
    amount: Money

class MutationSnapshot(FrozenModel):
    visible: VisibleMutation
    type: Annotated[int, Field(ge=1, le=7)]
    booked_on: date
    header_ledger_id: PositiveId | None
    relation_id: PositiveId | None
    invoice_number: InvoiceNumber | None
    entry_number: str | None
    description: str
    payment_reference: str | None
    term_days: Annotated[int, Field(ge=0)] | None
    mode: Literal["IN", "EX"] | None
    rows: tuple[MutationRow, ...] | None
    vat_groups: tuple[VatGroup, ...] | None
    gross: Money | None
    net: Money | None
    vat_total: Money | None
    not_returned_fields: tuple[str, ...]
    protection: ProviderProtection
    evidence: EvidenceRef

class PaymentEvidence(FrozenModel):
    outstanding: Outstanding
    observed_payment_mutations: tuple[EvidenceRef, ...]
    coverage: Literal["exact_open_post", "observed_references_only"]
    complete_graph_proven: Literal[False]

class SourceRow(FrozenModel):
    index: Annotated[int, Field(ge=0)]
    full_description: str
    ledger_id: PositiveId
    relation_id: PositiveId | None
    cost_center_id: PositiveId | None
    amount: Money
    source_vat: Money
    vat_code: str

class PurchaseProposal(FrozenModel):
    source_key: Digest
    source_document: EvidenceRef
    invoice_number: InvoiceNumber
    invoice_date: date
    booking_date: date
    relation_id: PositiveId
    creditor_ledger_id: PositiveId
    term_days: Annotated[int, Field(ge=0)]
    mode: Literal["IN", "EX"]
    description: SourceDescription
    rows: tuple[SourceRow, ...]
    source_gross: Money
    source_net: Money
    source_vat: Money
    expected_groups: tuple[VatGroup, ...]
    expected_gross: Money
    expected_net: Money
    expected_vat: Money
    explicit_policy: RoundingDecision | None
```

PRESENT outstanding requires all three amounts and exact returned mutation/relation identity. NOT_RETURNED requires all amounts absent and never means paid or zero. UNKNOWN, multiple or mismatched entries block any write. A rename may preserve exact NOT_RETURNED; full mutation PUT requires positive exact open-post evidence and the supported unpaid profile. A complete graph is not inferred from invoice-number search.

Money parser requires finite cent strings, bounded sign and exact arithmetic. Term 0 remains 0; no truthiness fallback. Invoice numbers remain strings including leading zeros. Preserve row order/count, signs, source VAT and source full text. Approved shortening is explicit and source-bound; headers within 50 characters remain literal source text. Currency is EUR in this initial profile; mixed or foreign currency is unavailable. Posting rows remain within the reference-tested 1–4-row conservative profile, not an API maximum (official create schema permits 500).

Missing row VAT may be accepted only when explicitly NOT_RETURNED and exact VAT-group, gross and net checks succeed; present null/wrong VAT fails. The historical one-cent lower-input-VAT case becomes a reusable but disabled-by-default policy contract: positive IN, one high-rate group, exact source-bound owner choice, unchanged gross, exactly lower one cent VAT and higher one cent net, no fabricated row allocation, no present row VAT. No tool chooses this policy. Private/mixed/VAT/ledger choices likewise arrive as supplied, provenance-bound decisions; calculation does not determine deductibility.
MutationSnapshot is the read DTO for types 1–7: fields absent from the type-specific provider response remain None with their field path in not_returned_fields. No net/term/mode/rows are synthesized. Create/modify preparation requires a separate complete purchase projection: all required type1 fields present and exact. Payment/general-journal snapshots remain readable without being forced into purchase semantics. Row ledger/amount/VAT fields likewise have a typed provider-presence projection where not supplied; an unknown required purchase field blocks the purchase projection.

## Reference, archive and hours models

```python
class Ledger(FrozenModel):
    id: PositiveId
    code: str
    name: str
    category: str
    active: bool | None

class Relation(FrozenModel):
    id: PositiveId
    code: str
    kind: Literal["B", "P"]
    name: str
    contact: str | None
    street: str | None
    postal_code: str | None
    city: str | None
    country_code: str | None
    vat_number: str | None
    registration_number: str | None
    email: str | None
    term_days: int | None

class SupplierDraft(FrozenModel):
    code: str
    kind: Literal["B", "P"]
    name: str
    contact: str | None
    street: str | None
    postal_code: str | None
    city: str | None
    country_code: str | None
    vat_number: str | None
    registration_number: str | None
    email: str | None
    term_days: Annotated[int, Field(ge=0)] | None

class SupplierChoice(FrozenModel):
    proposed: SupplierDraft
    source: EvidenceRef
    compared_catalogue: EvidenceRef
    identity_basis: tuple[str, ...]
    decision: Literal["existing", "new", "unresolved"]

class MatchCandidate(FrozenModel):
    relation: Relation
    equal_fields: tuple[str, ...]
    conflicting_fields: tuple[str, ...]
    classification: Literal["exact", "alias_evidence", "candidate", "conflict"]

class MatchResult(FrozenModel):
    candidates: tuple[MatchCandidate, ...]
    coverage: Coverage
    selected_id: PositiveId | None
    choice_evidence: EvidenceRef | None

class ArchiveFile(FrozenModel):
    identity: FileIdentity
    name: str
    media_type: str | None
    size: Annotated[int, Field(ge=0)] | None
    modified_at: datetime | None
    sha256: Digest | None
    protection: ProviderProtection
    evidence: EvidenceRef

class Attachment(FrozenModel):
    file: ArchiveFile
    target: VisibleMutation
    reference: LinkReference | None

class AttachmentGraph(FrozenModel):
    targets: tuple[VisibleMutation, ...]
    attachments: tuple[Attachment, ...]
    evidence: EvidenceRef
    complete_for_supplied_targets: bool

class HourSnapshot(FrozenModel):
    hour_id: Int32Id
    employee_id: Int32Id
    project_id: Int32Id
    activity_id: Int32Id
    day: date | None
    hours: HoursNumber | None
    kilometres: HoursNumber | None
    remarks: str | None
    employee_text: str | None
    project_text: str | None
    activity_text: str | None
    input_date_text: str | None
    not_returned_fields: tuple[str, ...]
    evidence: EvidenceRef

class HoursChoice(FrozenModel):
    employee_id: Int32Id
    project_id: Int32Id
    activity_id: Int32Id
    day: date
    hours: HoursNumber | None
    kilometres: HoursNumber | None
    remarks: str | None
    source_key: Digest
    source: EvidenceRef

class HourSearchResult(FrozenModel):
    items: tuple[HourSnapshot, ...]
    coverage: Coverage
```

Relation snapshots are reads; new supplier input is a separate SupplierDraft with no invented ID, explicitly supplied code/name/kind and optional contact/address/tax/term fields. Optional unknown fields are omitted, not filled with customer identity. Exact code uniqueness plus supplied vendor identity is checked afresh before create; aliases are candidates without silent selection. Source email is stored data only: no mail is sent.

Download persistence is a separate artifact command returning no value internally; its receipt/evidence query returns EvidenceRef plus bounded metadata, never raw PDF/base64 in the tool response. Source artifacts are imported only from the configured inbox through opaque evidence IDs; clients cannot choose output/ACL paths. Archive writes accept PDF/image magic+MIME under 5 MiB and a conservative 48-ASCII-character name including extension; original full name remains evidence. Existing longer/Unicode names remain readable. A shared PDF may be attached to several explicitly supplied targets; verify previous targets after each new link/change.

Hours and kilometres are nullable signed decimal strings, absolute value <=100000 and at most two decimals, not money. At least one is non-null for create/edit. Date is nullable in observed read shape but a valid calendar date is required for a command. Remarks/reference text/input-date text retain null versus absent and are preserved on edit. There is no evidenced billable or relation_id field. Reuse actual preserved hours DTO field semantics and supported range; no guessed employee/project/user ID equivalence. Reference values must be supplied or read through an evidenced contract. There is no general project/employee catalogue tool until its provider mapping is established. A marker search is bounded to one day and does not prove global absence.

## Operation plan, state and errors

```python
class OperationKind(StrEnum):
    SUPPLIER_CREATE = "supplier_create"
    PURCHASE_CREATE = "purchase_create"
    SOURCE_IMPORT = "source_import"
    FILE_DOWNLOAD = "file_download"
    FILE_UPLOAD = "file_upload"
    FILE_LINK = "file_link"
    LEDGER_CHANGE = "ledger_change"
    DESCRIPTION_CHANGE = "description_change"
    FILE_RENAME = "file_rename"
    HOURS_CREATE = "hours_create"
    HOURS_EDIT = "hours_edit"
    OWNED_HOURS_CLEANUP = "owned_hours_cleanup"

class OperationState(StrEnum):
    PREPARED = "prepared"
    BLOCKED = "blocked"
    PENDING = "pending"
    ACK_UNVERIFIED = "ack_unverified"
    VERIFIED = "verified"
    ALREADY_DESIRED = "already_desired"
    UNKNOWN = "unknown"
    MISMATCH = "known_mismatch"
    RECONCILED = "reconciled_verified"

class FieldChange(FrozenModel):
    path: str
    before: str | None
    desired: str | None

class PreparedPlan(FrozenModel):
    operation_id: UUID
    kind: OperationKind
    profile: str
    binding_digest: Digest
    source_key: Digest
    intent_digest: Digest
    rule_digest: Digest
    baseline: tuple[EvidenceRef, ...]
    changes: tuple[FieldChange, ...]
    claim_keys: tuple[Digest, ...]
    binding_version: str
    capability_profile_version: str
    intent: Intent
    expires_at: datetime
    plan_digest: Digest
    blocked_reasons: tuple[str, ...]

class SafeError(FrozenModel):
    code: str
    stage: str
    retryable_read: bool
    write_outcome: Literal["not_dispatched", "unknown", "observed"]
    original_type: str | None
    received_id: ReceivedIdentity | None
    diagnostic_evidence: EvidenceRef | None

class FrozenReceipt(FrozenModel):
    operation_id: UUID
    kind: OperationKind
    state: OperationState
    plan_digest: Digest
    source_key: Digest
    received_ids: tuple[ReceivedIdentity, ...]
    observations: tuple[EvidenceRef, ...]
    differences: tuple[FieldChange, ...]
    error: SafeError | None
    updated_at: datetime

class RequestContext(FrozenModel):
    correlation_id: UUID
    deadline: datetime
```

A public ApplyRequest is exactly profile, operation_id and plan_digest. The resolved plan contains a closed discriminated union of the twelve typed intents declared in this appendix, never arbitrary paths/JSON patches. Ledger change intent contains visible mutation, source ledger ID and desired ledger ID; description change contains SourceDescription; rename contains file ID, observed name and desired name; link contains file ID, visible target and supplied shared targets; create intents contain the exact purchase/supplier/hour proposals. File upload contains evidence ID, source SHA and desired name. Each intent is separately schema-versioned and included in intent_digest.

Canonical SHA-256 uses UTF-8 sorted-key compact JSON with Decimal serialized to exact fixed-point strings, tuple order retained, ISO dates and UTC timestamps; plan_digest excludes itself and includes all other fields. A host profile or rule change invalidates existing plans. No circular input/authorization hashes. Expiry is a stale-plan limit, never a claim that an in-flight write expired safely. A source key is derived from immutable source identity/hash plus operation kind/admin; changing alias, filename or operation UUID cannot clear an unresolved source gate.

SafeError is a shared stable envelope, not an exception subclass per endpoint. The boundary preserves the original cause chain privately after credential/token/profile-field redaction and size caps. Public messages are sanitized stage/code summaries. Missing optional fields differ from invalid/null fields; provider shape failures remain visible and never become empty results.

## Narrow interface signatures and composition

Concrete public requests/results and tagged intents below complete the catalogue. A common ProfileRequest is frozen and contains only profile. Read requests extend it with their stated fields; they are not open dictionaries. SDK structured outputs are exactly the named frozen result models.

```python
class ProfileRequest(FrozenModel):
    profile: str

class ReadMutationRequest(ProfileRequest):
    target: VisibleMutation

class ApplyRequest(ProfileRequest):
    operation_id: UUID
    plan_digest: Digest

class ReferenceRequest(ProfileRequest):
    kind: Literal["ledger", "relation", "costcenter"]
    exact_code: str | None
    name_contains: str | None

class ReferencePage(FrozenModel):
    ledgers: tuple[Ledger, ...]
    relations: tuple[Relation, ...]
    cost_centers: tuple[CostCenter, ...]
    coverage: Coverage
    evidence: EvidenceRef

class CostCenter(FrozenModel):
    id: PositiveId
    code: str
    name: str

class MutationSearchRequest(ProfileRequest):
    invoice_number: InvoiceNumber

class MutationSearchResult(FrozenModel):
    items: tuple[MutationSnapshot, ...]
    coverage: Coverage
    evidence: EvidenceRef

class OutstandingRequest(ReadMutationRequest):
    relation_id: PositiveId
    invoice_number: InvoiceNumber

class AppMappingRequest(ReadMutationRequest):
    day: date

class ArchiveListRequest(ProfileRequest):
    directory_id: Annotated[int, Field(ge=0)]

class ArchiveListing(FrozenModel):
    directories: tuple[ArchiveDirectory, ...]
    files: tuple[ArchiveFile, ...]
    coverage: Coverage
    evidence: EvidenceRef

class ArchiveDirectory(FrozenModel):
    id: Annotated[int, Field(ge=0)]
    name: str

class ArchiveGetRequest(ProfileRequest):
    file_id: PositiveId

class HoursGetRequest(ProfileRequest):
    hour_id: Int32Id

class HoursFindRequest(ProfileRequest):
    day: date
    marker: str

class HourReadResult(FrozenModel):
    state: Literal["found", "not_found"]
    item: HourSnapshot | None

class SupplierMatchRequest(FrozenModel):
    identity: SupplierDraft
    candidates: tuple[Relation, ...]
    coverage: Coverage
    choice_evidence: EvidenceRef | None

class ValidationResult(FrozenModel):
    valid: bool
    blockers: tuple[str, ...]
    differences: tuple[FieldChange, ...]
    evidence: tuple[EvidenceRef, ...]

class IntentBase(FrozenModel):
    source: EvidenceRef

class SupplierCreateIntent(IntentBase):
    kind: Literal["supplier_create"]
    choice: SupplierChoice

class PurchaseCreateIntent(IntentBase):
    kind: Literal["purchase_create"]
    proposal: PurchaseProposal

class DownloadIntent(IntentBase):
    kind: Literal["file_download"]
    file: FileIdentity
    expected_sha256: Digest | None

class UploadIntent(IntentBase):
    kind: Literal["file_upload"]
    content: EvidenceRef
    sha256: Digest
    original_name: str
    archive_name: str
    destination: Literal[0]

class LinkIntent(IntentBase):
    kind: Literal["file_link"]
    file: FileIdentity
    target: VisibleMutation
    shared_targets: tuple[VisibleMutation, ...]

class RenameIntent(IntentBase):
    kind: Literal["file_rename"]
    file: FileIdentity
    observed_name: str
    desired_name: str
    shared_targets: tuple[VisibleMutation, ...]

class LedgerIntent(IntentBase):
    kind: Literal["ledger_change"]
    target: VisibleMutation
    row_index: Literal[0]
    old_ledger_id: PositiveId
    desired_ledger_id: PositiveId

class DescriptionIntent(IntentBase):
    kind: Literal["description_change"]
    target: VisibleMutation
    description: SourceDescription

class HoursCreateIntent(IntentBase):
    kind: Literal["hours_create"]
    choice: HoursChoice
    marker: str

class HoursEditIntent(IntentBase):
    kind: Literal["hours_edit"]
    before: HourSnapshot
    desired: HoursChoice

class OwnedHoursCleanupIntent(IntentBase):
    kind: Literal["owned_hours_cleanup"]
    hour_id: Int32Id
    create_operation: UUID
    latest_operation: UUID
    marker: str
    synthetic: Literal[True]

Intent = Annotated[
    SourceImportIntent | SupplierCreateIntent | PurchaseCreateIntent | DownloadIntent |
    UploadIntent | LinkIntent | RenameIntent | LedgerIntent |
    DescriptionIntent | HoursCreateIntent | HoursEditIntent |
    OwnedHoursCleanupIntent,
    Field(discriminator="kind")
]

class PrepareRequest(ProfileRequest):
    operation_id: UUID
    intent: Intent
    captured: PreparationEvidence
    rule_digest: Digest

class PlanStoreRequest(ProfileRequest):
    operation_id: UUID
    plan: PreparedPlan

class StatusRequest(ProfileRequest):
    operation_id: UUID

class PreflightRequest(FrozenModel):
    proposal: PurchaseProposal
    references: ReferencePage
    duplicates: MutationSearchResult

class Capability(FrozenModel):
    name: str
    enabled: bool
    effect: Literal["pure", "query", "local_command", "provider_command"]
    profile: str
    limit_description: str
    unavailable_reason: str | None

class CapabilityCatalogue(FrozenModel):
    capabilities: tuple[Capability, ...]

class CapabilitiesRequest(FrozenModel):
    pass
```

CapabilitiesRequest has no fields; the pass above means an empty schema declaration, not an implementation body. PreparedPlan contains intent: Intent. Its declaration and forward references resolve as one module schema, independent of display ordering.

```python
class MutationReader(Protocol):
    def read(self, target: VisibleMutation) -> MutationSnapshot: ...
    def exact_invoice(self, number: InvoiceNumber) -> MutationSearchResult: ...

class OutstandingReader(Protocol):
    def read(self, request: OutstandingRequest) -> Outstanding: ...

class ReferenceReader(Protocol):
    def read(self, request: ReferenceRequest) -> ReferencePage: ...

class AppMappingReader(Protocol):
    def resolve(self, request: AppMappingRequest) -> AppVersion: ...

class ArchiveReader(Protocol):
    def listing(self, directory_id: int) -> ArchiveListing: ...
    def metadata(self, file_id: PositiveId) -> ArchiveFile: ...
    def linked(self, target: VisibleMutation) -> AttachmentGraph: ...

class DownloadCommand(Protocol):
    def execute(self, operation_id: UUID, command: DownloadIntent) -> None: ...

class HoursReader(Protocol):
    def read(self, hour_id: Int32Id) -> HourReadResult: ...
    def find(self, day: date, marker: str) -> HourSearchResult: ...

class PlanCalculator(Protocol):
    def prepare(self, request: PrepareRequest) -> PreparedPlan: ...

class ReceiptReader(Protocol):
    def receipt(self, operation_id: UUID) -> FrozenReceipt: ...

class ProposalStoreCommand(Protocol):
    def execute(self, operation_id: UUID, plan: PreparedPlan) -> None: ...

class SupplierCreateCommand(Protocol):
    def execute(self, operation_id: UUID, command: SupplierCreateIntent) -> None: ...

class PurchaseCreateCommand(Protocol):
    def execute(self, operation_id: UUID, command: PurchaseCreateIntent) -> None: ...

class UploadCommand(Protocol):
    def execute(self, operation_id: UUID, command: UploadIntent) -> None: ...

class LinkCommand(Protocol):
    def execute(self, operation_id: UUID, command: LinkIntent) -> None: ...

class RenameCommand(Protocol):
    def execute(self, operation_id: UUID, command: RenameIntent) -> None: ...

class LedgerChangeCommand(Protocol):
    def execute(self, operation_id: UUID, command: LedgerIntent) -> None: ...

class DescriptionChangeCommand(Protocol):
    def execute(self, operation_id: UUID, command: DescriptionIntent) -> None: ...

class HoursCreateCommand(Protocol):
    def execute(self, operation_id: UUID, command: HoursCreateIntent) -> None: ...

class HoursEditCommand(Protocol):
    def execute(self, operation_id: UUID, command: HoursEditIntent) -> None: ...

class OwnedHoursCleanupCommand(Protocol):
    def execute(self, operation_id: UUID, command: OwnedHoursCleanupIntent) -> None: ...

class AuditWriter(Protocol):
    def append(self, event: AuditEvent) -> None: ...

class QueryHandler(Protocol):
    def invoke(self, request: RequestContext, query: ReadMutationRequest
               ) -> MutationSnapshot: ...

class ApplyHandler(Protocol):
    def invoke(self, request: RequestContext, command: ApplyRequest
               ) -> FrozenReceipt: ...
```

ApplyHandler is the MCP protocol boundary only: invoke the injected application command (None), then ReceiptReader, then shared presenter. No extra HTTP call merely to render an acknowledgement. The provider adapter internally captures unavoidable ACK/received ID through the already injected store, not a returned mutable response or callback/event bus.

A download provider port streams only into an injected evidence sink owned by DownloadCommand. Public archive_get returns metadata only; archive_download is explicit local-artifact command + provider query. For ordinary observation queries, low-level transport reads frozen provider DTOs; an explicit technical capture/audit command is composed at the protocol boundary, followed by pure projection. No core query method secretly saves a proposal or artifact.

Each handler is constructed once with only its narrow application interface. RequestContext contains correlation/deadline, not the lifespan resource container. No read interface receives a financial command port. Startup constructs all concrete deps; SDK async boundary uses bounded workers around synchronous ports, with no subprocesses.

Catalogue bindings: capabilities→CapabilitiesRequest/CapabilityCatalogue; references→ReferenceRequest/ReferencePage; mutation_get→ReadMutationRequest/MutationSnapshot; mutation_find→MutationSearchRequest/MutationSearchResult; outstanding→OutstandingRequest/Outstanding; mapping→AppMappingRequest/AppVersion; archive_list→ArchiveListRequest/ArchiveListing; archive_get→ArchiveGetRequest/ArchiveFile; archive_links→ReadMutationRequest/AttachmentGraph; hours_get→HoursGetRequest/HourReadResult; hours_find→HoursFindRequest/HourSearchResult; supplier_match→SupplierMatchRequest/MatchResult; purchase_preflight→PreflightRequest/ValidationResult; operation_prepare→PrepareRequest/PreparedPlan; plan_store→PlanStoreRequest/FrozenReceipt; operation_status and operation_reconcile→StatusRequest/FrozenReceipt; every provider apply including archive_download→ApplyRequest/FrozenReceipt with exactly its dedicated intent. No tool accepts raw URLs, headers, HTTP methods, SQL, arbitrary patches or output/ACL paths.

## Startup configuration contract

A single ConfigLoader reads one private config at process startup. Models have no I/O, singleton, ClassVar cache or from_file method. Environment is a host launch concern; credentials never travel in launch args/env/tool inputs. The loader reads only a fixed profile path under the protected local state root, not a path selected by an MCP caller.

```python
class Limits(FrozenModel):
    page_size: Annotated[int, Field(ge=1, le=1000)]
    maximum_pages: Annotated[int, Field(ge=1, le=5)]
    detail_reads: Annotated[int, Field(ge=1, le=500)]
    maximum_pdf_bytes: Annotated[int, Field(gt=0, le=5242880)]
    call_timeout_seconds: Annotated[int, Field(ge=1, le=60)]
    maximum_requests: Annotated[int, Field(ge=1, le=600)]
    operation_deadline_seconds: Annotated[int, Field(ge=1, le=600)]
    cleanup_reserve_seconds: Literal[30]
    write_name_ascii_limit: Literal[48]

class HostProfile(FrozenModel):
    alias: str
    binding: AdministrationBinding
    enabled_commands: tuple[OperationKind, ...]
    limits: Limits

class ServerConfig(FrozenModel):
    schema_version: Literal["1"]
    profiles: tuple[HostProfile, ...]
    writes_enabled: bool = False
    state_root_alias: Literal["per_user_local"]
    presenter: Literal["structured"]
    transport: Literal["stdio"]
```

Default writes_enabled is false and enabled_commands empty in distributed examples. Startup refuses duplicate profile aliases or inconsistent credential/admin aliases, nonlocal state storage and unsafe runtime paths. Actual absolute paths, credential target strings and administration IDs remain local. Runtime root is a validated fixed per-user local application-data subdirectory, with canonical source/work-root separation, no system/root/tracked-source/reparse escape. No caller can request ACL changes. Windows Credential Manager is the initial host adapter; another platform requires an explicit implementation and tests, not an advertised portable credential claim.

Reference reads use fixed vendor origins and reject redirects. Limits are bounded operation profiles, not evidence of vendor maximums. Exact-ID reads are small; day filters use at most two pages of 20. Catalogue reads use explicit complete pagination; caps return INCOMPLETE and prohibit absence/duplicate-clear conclusions. Configured maximum-call budgets reserve enough capacity for verification and own REST session cleanup before dispatch. No global PATH change or inherited site packages are part of this design.

## Durable event and credential-binding declarations

```python
class AuditEvent(FrozenModel):
    schema_version: Literal["1"]
    event_id: UUID
    operation_id: UUID | None
    correlation_id: UUID
    profile: str
    binding_digest: Digest
    occurred_at: datetime
    stage: str
    effect: Literal["query", "authentication", "local_artifact", "command"]
    state: OperationState | None
    code: str
    evidence: tuple[EvidenceRef, ...]
    received_ids: tuple[PositiveId, ...]

class CredentialLease(FrozenModel):
    lease_id: UUID
    generation: PositiveId
    binding_digest: Digest
    provider: Literal["rest", "app"]
    expires_at: datetime | None

class AuthenticationCommand(Protocol):
    def acquire(self, invocation_id: UUID, profile: str) -> None: ...
    def release(self, lease_id: UUID) -> None: ...
    def shutdown(self) -> None: ...

class LeaseReader(Protocol):
    def lease(self, invocation_id: UUID) -> CredentialLease: ...

class OperationAdmissionCommand(Protocol):
    def reserve(self, operation_id: UUID, plan_digest: Digest) -> None: ...

class ObservationCaptureCommand(Protocol):
    def execute(self, correlation_id: UUID, observation: EvidenceRef) -> None: ...

class ReconcileQuery(Protocol):
    def evaluate(self, receipt: FrozenReceipt,
                 observations: tuple[EvidenceRef, ...]) -> ValidationResult: ...

class ReconcileRecordCommand(Protocol):
    def execute(self, operation_id: UUID,
                validation: ValidationResult) -> None: ...
```

CredentialLease is an internal opaque handle; no token is a field. Auth acquire/release are technical commands; a transport consumes a lease through a private credential-access port, not through tool-visible secret values. App leases can have unknown expiry; that absence never means unlimited validity.

Local owner-confirmed REST binding is explicitly weaker than a freshly provider-verified identity. The initial implementation does not infer an administration from the vault target name, App ID, UI administration number or a rotated token. Before use, the host adapter compares a local keyed seal of the current secret version to a separately owner-activated binding record; seals/keys are private and never logged or returned. Changed/unavailable seal fails closed before REST login. Rebinding requires an explicit host-owner procedure confirming the new token's intended administration and version; no tool performs rebind or switches administration. GET /v1/administration exists, but no unverified assumption about its exact identity fields substitutes for this activation prerequisite. A future provider-identity validator requires schema/evidence acceptance before it can strengthen the assurance label.

All datetime fields require an explicit UTC offset and are emitted in UTC. Unknown provider date fields are not assigned a clock-derived substitute. Amounts on nonpurchase mutations can remain absent; write validators require the exact complete supported type projection. The raw adapter boundary may preserve an unknown field privately for diagnostics, but neither tool output nor core logic accepts arbitrary Mapping/Any.

## Complete input/output binding and protection details

The following additional declarations close artifact import and protected-provider projection. They do not add arbitrary filesystem access or raw JSON outputs.

```python
class SourceImportRequest(ProfileRequest):
    operation_id: UUID
    inbox_entry: str
    expected_sha256: Digest | None = None
    provenance: str

class SourceImportIntent(IntentBase):
    kind: Literal["source_import"]
    inbox_entry: str
    expected_sha256: Digest
    provenance: str

class SourceImportCommand(Protocol):
    def execute(self, operation_id: UUID, command: SourceImportIntent) -> None: ...

class ProtectedFieldDigest(FrozenModel):
    path: str
    sha256: Digest

class ProviderProtection(FrozenModel):
    contract_id: str
    full_projection_sha256: Digest
    fields: tuple[ProtectedFieldDigest, ...]
    unknown_fields: tuple[str, ...]
```

SourceImportRequest is a separate explicit local artifact command, not provider apply. The source-inbox intake protocol below defines how its basename is obtained; no MCP inbox-listing tool is implied. The command computes the bounded source bytes' SHA itself and, if supplied, compares expected_sha256. It stores an immutable artifact through the shared writer, and its existing receipt exposes EvidenceRef. No credentials or provider calls occur. Intent/OperationKind include source_import; DownloadIntent is a separate artifact command with provider-read effects. Public tools remain incapable of arbitrary local file reads.

MutationSnapshot, HourSnapshot and ArchiveFile each additionally carry protection: ProviderProtection. The adapter owns the complete known provider field schema and classifies every field; a field unclassified by that schema makes unknown_fields nonempty and blocks writes. A canonical private full observation and per-field digests cover protected provider fields not convenient in public views (including payment/row/cost-center/reference/record-entry fields). Core verification compares these frozen digests against an explicit allowlist of intended text/ledger differences, never drops unmodeled fields or interprets an absent value as zero. No arbitrary provider body crosses into core. A read of a nonpurchase type can report its absent paths; a command requires its complete classified supported projection.

All nullable read fields retain not_returned_fields/presence metadata. A semantic null is not the same as a missing key; the raw typed provider DTO retains that distinction. The hours snapshot exactly mirrors the evidenced id/datum/medewerkerId/projectId/activiteitId/aantalUren/aantalKilometers/opmerkingen/medewerker/project/activiteit/invoerDatum set, including stored nullable reference text. No billable or relation field is sent. Source-controlled examples use synthetic IDs only.

PreparedPlan also contains server-derived claim_keys: tuple[Digest, ...], derived binding version and capability profile version; caller cannot supply or change these keys. An apply resolves intent from the stored plan, not a new caller payload. canonical source identity for an existing target is independent of mutable input descriptions; purchase identity additionally claims exact relation plus literal invoice string, upload claims byte SHA independent of name. A new source hash with an identical existing logical target does not create write permission.

The table in the main design is authoritative for stable tool names. eb_source_import uses SourceImportRequest/FrozenReceipt; eb_archive_download and every provider write use ApplyRequest/FrozenReceipt. Reconcile command accepts StatusRequest, performs read-only provider observations through the query ports, then explicit ReconcileRecordCommand; it does not call the original writer. CapabilityCatalogue and all other listed DTOs are schema-complete closed models; forward references resolve before SDK schema registration.

## Explicit rounding-decision contract

```python
class RoundingDecision(FrozenModel):
    policy: Literal["owner_one_cent_lower_group_vat"]
    source: EvidenceRef
    owner_decision: EvidenceRef
    proposal_payload_digest: Digest
    source_gross: Money
    source_net: Money
    source_vat: Money
    booking_gross: Money
    booking_net: Money
    booking_vat: Money
    mode: Literal["IN"]
    vat_code: Literal["HOOG_INK_21"]
    source_group_count: Literal[1]
    requires_row_vat_not_returned: Literal[True]
```

This decision's invariants are exact: positive source gross; booking gross equals source gross; source VAT minus booking VAT is exactly 0.01; booking net minus source net is exactly 0.01; source and booking each balance; original rows/payload remain unchanged. Any missing hash/decision, increased VAT, larger delta, other mode/group/sign or present row VAT blocks. The decision is input evidence for a separately permitted command, not a new grant of execution authority or general fiscal rule.

No mutation/class method bodies are specified here. The empty CapabilitiesRequest schema can equivalently be declared with an empty field set in the eventual Pydantic package. Forward references (Intent, ProviderProtection, RoundingDecision, AuditEvent and SourceImportIntent) are resolved once before registry/schema exposure; they are not runtime service locators.

## Pure preparation evidence

```python
class PreparationEvidence(FrozenModel):
    mutations: tuple[MutationSnapshot, ...]
    references: ReferencePage | None
    outstanding: tuple[Outstanding, ...]
    files: tuple[ArchiveFile, ...]
    attachments: tuple[AttachmentGraph, ...]
    hours: tuple[HourSnapshot, ...]
    duplicates: MutationSearchResult | None
```

PlanCalculator receives frozen captured values, not just handles requiring a hidden store read. It performs no filesystem/provider/audit mutation. Preflight likewise receives actual reference and duplicate results. Stored evidence handles bind the plan, but are not the calculator's I/O mechanism. At plan persistence/apply the application verifies that referenced artifacts exist in the local trusted evidence store, that their digests match supplied values and that the profile/source bindings agree; forged caller snapshots cannot authorize a dispatch. Fresh prewrite reads remain required. Reference/duplicate incompleteness produces blockers.

## Shared strict JSON-mode codec

Choose one shared pure JsonBoundaryCodec for MCP inputs, provider DTOs, persisted SQLite JSON and output serialization. Pydantic's [strict-mode documentation](https://docs.pydantic.dev/latest/concepts/strict_mode/) distinguishes Python-object and JSON validation; strict Python validation is not the selected wire admission route. No SDK-decoded dict goes directly to strict model_validate.

At the MCP boundary, the codec first accepts only a finite JSON-compatible value tree: string keys, JSON scalars, lists and objects, with no Python UUID/date/Enum/tuple/custom objects. It encodes deterministically to UTF-8 JSON with sorted keys, no default=str, no NaN/Infinity and no coercion of values, then calls the selected model's model_validate_json(strict=True), or TypeAdapter.validate_json(strict=True) for a tagged union. MoneyText and HoursNumber remain JSON strings. Numeric amounts, bool-as-ID, numeric-string IDs, extra fields, unknown enum values, invalid UUIDs and invalid date/datetime strings are rejected. Valid JSON UUID/date/datetime/StrEnum strings and arrays enter the declared immutable types and frozen tuples. Datetime admission additionally requires an explicit offset; canonical output converts it to UTC. Internal already-typed core values use their types directly, not an untrusted-dict shortcut.

Provider response bytes take the same JSON-mode typed admission, preceded only by a route-schema-specific lexical projection. Parse bounded UTF-8 JSON with exact Decimal number parsing, integer tokens as integers, duplicate-key rejection and nonfinite rejection: no intermediate binary float. The adapter's declared provider monetary/quantity fields are converted from their exact numeric tokens to canonical fixed-point JSON strings, only when exactly representable at the field precision; no rounding, numeric-ID-to-string conversion or blanket cast is allowed. Unknown fields remain privately observed and block writes as already specified. Nonmonetary JSON types retain their original kind. The projected UTF-8 JSON is admitted through the own provider DTO's strict JSON-mode codec, then explicitly mapped to frozen core values. This schema-specific numeric translation is provider representation handling, not a new VAT/amount rule.

SQLite stores versioned canonical JSON from validated frozen models, not Python repr/pickle or a raw provider dict. Rehydration checks the schema version and uses the identical strict JSON-mode admission. Model output uses model_dump(mode="json") or model_dump_json with configured canonical serializers; tuple arrays, enum strings, UUID strings, ISO dates, UTC datetimes and MoneyText are explicit wire forms. Canonical hashing uses the deterministic shared encoding of that validated JSON value, never a float conversion or default=str. Nested core values remain frozen after roundtrip.

```python
from typing import TypeVar

ModelT = TypeVar("ModelT", bound=FrozenModel)
JsonScalar = str | int | float | bool | None
JsonValue = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]

class JsonBoundaryCodec(Protocol):
    def admit_arguments(self, value: JsonValue, model: type[ModelT]) -> ModelT: ...
    def admit_json(self, content: bytes, model: type[ModelT]) -> ModelT: ...
    def encode(self, value: FrozenModel) -> bytes: ...

class ProviderProjectionCodec(Protocol):
    def project(self, content: bytes, contract_id: str) -> bytes: ...
```

These are pure signatures without bodies. JsonValue exists only at the outer protocol codec; application/domain models never accept it as an escape hatch. ProviderProjectionCodec has a closed startup registry of known route contracts; contract_id is not an MCP argument. Invalid shape/encoding/version preserves the original ValidationError/cause under the shared redacted diagnostics envelope, with field paths and bounded codes; no secrets or rejected values are blindly logged.

Acceptance: valid JSON UUID, date, offset datetime, declared enum and nested arrays produce UUID/date/datetime/StrEnum and frozen tuple results; the same shapes passed directly as an untrusted Python dict are not a supported admission route. Numeric money, bool ID, extra key, invalid UUID/date/enum and nonfinite input fail. Duplicate keys fail on raw JSON admission (provider/SQLite); already-decoded SDK argument trees contain no recoverable duplicate-key history, so no additional claim is made for that SDK parsing stage. Provider decimals with long lexical precision never pass through float and must either map exactly or fail. MCP→core→canonical SQLite JSON→core→canonical output has identical semantic values and stable digest; UTC normalization and null-versus-missing behavior are asserted. These are future public-boundary fake tests, not claimed SDK execution today.

## Source-inbox intake protocol outside MCP

The fixed protected inbox is configured by the host at startup. An owner/operator, or the already-authorized host harness using its native file tools, copies the selected source into that inbox without changing the original. That staging action returns the actual staged single basename; alternatively the operator reads that basename through the host's normal directory listing. The operator/harness passes this exact basename to source_import. No server-issued token or absent MCP listing capability is required. The word opaque means the server interprets it only as that basename, never as an arbitrary path or an administration identifier.

SourceImportRequest.inbox_entry and SourceImportIntent.inbox_entry have the same basename-only contract: nonempty, no separators, drive prefix, traversal components, control characters, dot/dot-dot entry, Windows device/alternate-stream name or symlink/reparse escape. The configured inbox itself is validated against source/system/root escapes. At open the command verifies a regular file and containment, reads bounded bytes from the validated handle, computes SHA-256 itself and validates magic/MIME/size. Optional request expected_sha256 is only a caller consistency check, not a demand for manual hashing. The command fills the resolved SourceImportIntent.expected_sha256 from the bytes it actually read before persisting the intent; the operator does not supply that internal mandatory digest. The command persists the exact imported bytes and source basename/provenance as a new immutable EvidenceRef, with its own operation receipt. Upload subsequently consumes those snapshot bytes, never reopens a mutable inbox path.

The staging actor cannot select an output path or ACL target through MCP. Missing/changed/nonfile/oversize/hash-mismatch input stops without provider access. Private originals remain outside tracked source; no source-path value is copied into public docs. The host staging protocol is an explicit external prerequisite, not a hidden new tool or broader automation platform.

## Version History

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 1.0 | 2026-11-01 | Imp | Concrete proposed DTOs, tool bindings and port signatures. |
| 1.1 | 2026-11-01 | Imp | Define shared strict JSON-mode codec, exact provider numeric projection and external inbox intake; correct intent count. |
| 1.2 | 2026-11-01 | Imp | Mark reviewed contracts historical; current functional/provider evidence precedes replacement design. |
