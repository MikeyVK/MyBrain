<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# App-v4 endpoint MCP technical contracts

**Status:** APP-ONLY ENDPOINT CONTRACTS — REVIEW CANDIDATE, NOT IMPLEMENTED  
**Version:** 2.0  
**Last Updated:** 2026-11-01

## Purpose and supersession

This appendix specifies the technical contracts for the [canonical design](design.md) and its [operation registry](endpoint-design-catalogue.md). Version1.x's purchase proposals, matching, financial validation, plan approval, repair, rounding decisions and REST baselines are superseded. Git retains them as historical evidence. No old business command model or operational authorization is imported.

## Frozen values and source schemas

```python
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Annotated, Generic, Literal, Protocol, TypeVar
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class FrozenModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

SchemaId = Annotated[str, Field(min_length=1)]
Digest = Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
Int32 = Annotated[int, Field(ge=-2147483648, le=2147483647)]
Int64Text = Annotated[str, Field(pattern=r"^-?(0|[1-9][0-9]*)$")]
NumberText = Annotated[str, Field(pattern=r"^-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?$")]

class AppMutationVersionId(FrozenModel):
    value: Int64Text

class VisibleMutationNumber(FrozenModel):
    value: Int32

class FileId(FrozenModel):
    value: Int32

class DirectoryId(FrozenModel):
    value: Int32

class AssociationId(FrozenModel):
    value: Int32

class AdministrationId(FrozenModel):
    value: Int32

class SchemaField(FrozenModel):
    json_name: str
    source_type: str
    nested_schema: SchemaId | None
    jsonnet_required: Literal[0, 1, 2, 3]
    null_value_handling: Literal["include", "ignore", "unspecified"]
    ignored_on_wire: bool

class SourceSchema(FrozenModel):
    schema_id: SchemaId
    source_assembly_sha256: Digest
    source_type: str
    inherited_schema: SchemaId | None
    fields: tuple[SchemaField, ...]
    enum_members: tuple[EnumMember, ...]
    schema_digest: Digest

class EnumMember(FrozenModel):
    name: str
    value: Int32
```

The registry schema is a frozen, explicit source-bound definition, not arbitrary reflection over the APK at runtime. ConfigLoader reads the maintained registry/schema resources once; startup validates inheritance, field references, enum members, required/null/ignore metadata, duplicate names and evidence digests before handler registration. Future implementation extracts/selects schemas from the pinned metadata, reviews them and versions the maintained resources. No APK/decompiler dependency or private evidence path is deployed with the server.

Public tool schemas are derived from this single registry. They are closed named object schemas, not an arbitrary body object. The admission result is a frozen schema-validated provider-value DTO, not an untrusted dict cast to a type. A technical dispatcher does not need bookkeeping field access. It forwards that already validated object through the registered codec.

```python
class JsonNull(FrozenModel):
    kind: Literal["null"]

class JsonBoolean(FrozenModel):
    kind: Literal["boolean"]
    value: bool

class JsonString(FrozenModel):
    kind: Literal["string"]
    value: str

class JsonNumber(FrozenModel):
    kind: Literal["number"]
    lexical: NumberText

class JsonArray(FrozenModel):
    kind: Literal["array"]
    items: tuple["FrozenJson", ...]

class JsonMember(FrozenModel):
    name: str
    value: "FrozenJson"

class JsonObject(FrozenModel):
    kind: Literal["object"]
    members: tuple[JsonMember, ...]

FrozenJson = JsonNull | JsonBoolean | JsonString | JsonNumber | JsonArray | JsonObject

class ValidatedPayload(FrozenModel):
    schema_id: SchemaId
    schema_digest: Digest
    value: JsonObject

class ResponseProjection(FrozenModel):
    schema_id: SchemaId | None
    known: FrozenJson | None
    unclassified: tuple[JsonMember, ...]
    warnings: tuple[SchemaDiagnostic, ...]

class SchemaDiagnostic(FrozenModel):
    path: str
    code: str
    original_type: str | None
```

This recursive JSON type exists only at the validated technical edge; there is no Any/unchecked Mapping escape in services. Object member names are unique. Missing field means no member; explicit null is JsonNull; zero is JsonNumber("0"), and arrays preserve order. Reference/enum/numeric schema checks precede ValidatedPayload construction. Unknown response fields retain typed values in unclassified with warnings, not silently discarded; unknown input members fail.

Source schema admission distinguishes client metadata from server requirements. Json.NET Required0(Default): presence not required;1(AllowNull): present required/null allowed;2(Always): present required/null forbidden;3(DisallowNull): **presence not required**, explicit null forbidden. Underlying nonnullable value types also reject null; nullable/reference types follow their source metadata. JsonIgnore properties are excluded. Inherited fields are resolved once. NullValueHandling.Ignore is recorded as client emission behavior, not proof that the server interprets omission as clearing or zero. This server preserves explicitly supplied null where its admitted schema permits it; it never fills absent fields/defaults or invents clearing semantics.

## Shared strict JSON-mode codec

Choose one pure JSON-mode boundary. SDK-decoded arguments must first be a finite JSON-compatible tree, deterministically encoded without default=str or NaN/Infinity, then admitted through model_validate_json(strict=True) or the equivalent JSON-mode TypeAdapter for envelope/union models. Do not send an untrusted SDK dict straight to strict Python model_validate. UUID/StrEnum/tuple/date-like technical values have explicit JSON representations.

The named provider body is validated against its SourceSchema, converted to frozen values and bound to schema digest. SDK representations of Double/Decimal fields are NumberText strings; Int64 fields use Int64Text strings to avoid host binary-number truncation. Int64Text syntax is additionally checked against the signed 64-bit range −9223372036854775808 through 9223372036854775807 during source-schema admission; regex alone does not establish that range. Int32 fields remain strict integers, never booleans or numeric strings. Transport writes number tokens for declared numeric fields only, not quoted strings. Provider raw UTF-8 JSON uses exact lexical/Decimal parsing without binary float and maps those numeric tokens to the documented string projection on output. There is no fixed cent precision, sign constraint, VAT calculation, rounding or blanket string conversion.

String identifiers and descriptions stay literal, including leading zeros, whitespace and Unicode. Provider DateTime fields use explicit ISO text projection with their original offset/date spelling; the server does not reinterpret a bookkeeping date or silently convert local midnight. Server event timestamps are separate timezone-aware values emitted in UTC. JSON/object/array/null structure is retained exactly at the value level. Duplicate keys and nonfinite JSON fail on raw admission; already-decoded SDK trees cannot recover duplicate-key history, so no such SDK-parser guarantee is invented.

Versioned persisted provider results are re-admitted by the same codec and schema version. Output uses model_dump(mode="json")/model_dump_json for technical envelopes plus the registered source-field serializers. Canonical request hashing uses the validated wire-value encoding, preserving array order and numeric lexical intent, with fixed object-key order. It is not a bookkeeping hash or source-duplicate rule.

```python
ModelT = TypeVar("ModelT", bound=FrozenModel)

class JsonCodec(Protocol):
    def admit_envelope(self, arguments: object, model: type[ModelT]) -> ModelT: ...
    def admit_body(self, content: bytes, schema: SourceSchema) -> ValidatedPayload: ...
    def encode_wire(self, value: ValidatedPayload) -> bytes: ...
    def project_response(self, content: bytes,
                         schema: SourceSchema | None) -> ResponseProjection: ...
    def encode_result(self, value: FrozenModel) -> bytes: ...
```

object above is the untrusted outer boundary, not a core payload. Implementations narrow it through actual runtime guards; no blind cast. Invalid input preserves the original schema diagnostic/cause under redaction, without logging rejected financial values or secrets. These are signatures without bodies.

## Representative concrete source seams

These tables declare the exact representative schemas from the compiled DTOs; they are not financial instructions or claims of server-required presence. For every property, implementation retains its actual JsonProperty Required/NullValueHandling metadata from the source. No SDK-required list is generated from Required3.

### Mutation create/update

| Source schema | Declared JSON fields and types |
| --- | --- |
| CreateMutatieDto | id:Int64; mutatieNummer:Int32; factuurNummer:String; grootboekRekeningCode:String; grootboekRekeningOmschrijving:String; datum:Nullable DateTime; bedrag:Double; shortMutatieSoortDisplayValue:String; boekstuk:String; omschrijving:String; soort:MutatieSoort; relatieId:Nullable Int32; grootboekRekeningId:Nullable Int32; isInclusiefBtw:Boolean; termijnInDagen:Nullable Int32; mutatieRegels:CreateMutatieRegelDto array; afschriftRegelId:Nullable Int32; bestanden:Int32 array |
| UpdateMutatieDto | Common source header/row fields above, excluding afschriftRegelId/bestanden; exact own schema, not a create-model shortcut |
| CreateMutatieRegelDto | index:Int32; tegenRekeningId:Int32; btwCode:String; kostenplaatsId:Nullable Int32; bedrag:Double; btw:Double; factuur:String; relatieId:Nullable Int32; omschrijving:String |
| MutatieDetailsDto | Source header plus mutatieRegels:MutatieRegelDetailsDto array and relatieDisplayName |
| MutatieRegelDetailsDto | Common source row plus openPostModel, kostenplaatsModel, bedragInclusief/bedragExclusief nullable Double and provider display fields |

Internal id and visible mutatieNummer are separate; a new returned internal ID is exposed, not assumed stable. The generic source kind enum 0–7 is not interpreted as a local booking recipe. Source bank-row and file IDs are forwarded if explicitly supplied. No amount/VAT/term/row-total validation beyond source type/shape is performed; provider error or zero field is retained. No automatic link/payment/create/delete chain follows.

### Archive

| Source schema | Declared JSON fields and types |
| --- | --- |
| UploadFileRequest | fileName:String; data:String(base64); directoryId:Nullable Int32; scan:Boolean |
| UploadFileResponse | originalFileName:String; saved:Boolean; scanned:Boolean; errorMessage:String; file:FileDto |
| FileDto | id:Int32; naam:String; datum:Nullable DateTime; directoryId:Nullable Int32; scanStatus:source enum |
| UpdateFileDto | id:Int32; naam:String; directoryId:Nullable Int32 |
| CreateUpdateDirectoryDto | id:Int32; parentDirectoryId:Int32; naam:String; setAsMenHInbox:Boolean |
| CreateFileKoppelDto | fileId:Int32; soort:KoppelSoortDto; koppelId:Int32 |
| GekoppeldRequestDto / GekoppeldResponseDto | Exact source names; request target domain and returned association reference retained separately |
| BulkMoveFolderDto | moveToFolderId:Int32; itemsToMove:Int32 array |

A source-backed static link response does not assign every numeric link kind a business meaning. UpdateFile directory changes are explicit broader writes than rename. saved=false/errorMessage, scanned=false, Boolean false and partial bulk bodies stay intact even after HTTP2xx. The receipt says RESPONSE_CAPTURED, not “upload/booking succeeded”. Unknown body shape does not trigger a second upload or local rename/repair.

The public upload convenience model is technical and explicit:

```python
class ArtifactHandle(FrozenModel):
    artifact_id: UUID
    sha256: Digest

class UploadToolRequest(FrozenModel):
    artifact: ArtifactHandle
    file_name: str
    directory_id: Int32 | None
    scan: bool
```

Only data encoding is supplied by the server. No automatic source, alias/48-character truncation, OCR or scan choice. Filename/resource limits are declared technical profile constraints, never mislabelled vendor maxima. Source content is bounded by configured bytes/type profile, not a financial document classification.

### Hours

| Source schema | Declared JSON fields and types |
| --- | --- |
| UurDto | id:Int32; datum:Nullable DateTime; medewerkerId/projectId/activiteitId:Int32; aantalUren/aantalKilometers:Nullable Double; opmerkingen:String; medewerker/project/activiteit:String; invoerDatum:Nullable DateTime |
| UrenFilterRequestDto | startPage:Nullable Int32; page/pageSize:Int32; period:PeriodDto; medewerkerId/projectId/activiteitId:Nullable Int32; searchTerm:String; filterType/source sort fields; nietGefactureerd:Boolean |
| FactureerUrenRequestDto | uurIds:Int32 array |
| FactuurInstellingenDto | uurEenheidId/kmEenheidId/factuurSjabloonId:Nullable Int32; regelTekst:String; betalingsTermijn:Nullable Int32; perPost/perEmail/incasseren/verwerken:Boolean |

Do not add billable/relation_id fields or apply money precision to hours/km. Existing source form limits are client-profile evidence, not universal server limits. The server does not create projects, select activities/rates or convert hours to invoice rows locally. POST /uren/factureren delegates the explicit native provider operation. General DELETE is a provider endpoint with declared effects, not an inherited authority from the older owned-synthetic cleanup proof.

Other families use their exact source schemas in the registry: RelatieCreateDto/RelatieUpdateDto, CreateFactuurDto/UpdateFactuurDto, CreateFactuurResponseDto, quote row/progress/conversion DTOs, subscription/update/billing DTOs and source report requests. They are not replaced by the mutation/hour schemas. Implementation admission requires the complete selected model/fixture, not all 229 source types.

## Operation descriptors, inputs and replies

```python
class Effect(StrEnum):
    QUERY = "query"
    REMOTE_WRITE = "remote_write"
    OUTWARD_SEND = "outward_send"
    PROVIDER_PROCESSING = "provider_processing"
    AUTH_CONTEXT = "auth_context"
    LOCAL_ARTIFACT = "local_artifact"

class OperationSpec(FrozenModel):
    operation_id: str
    tool_name: str
    method: Literal["GET", "POST", "PUT", "DELETE"]
    path_template: str
    path_schema: SchemaId
    query_schema: SchemaId
    body_schema: SchemaId | None
    response_schema: SchemaId | None
    effects: frozenset[Effect]
    source_client_method: str
    source_contract_digest: Digest
    inventory_ids: tuple[str, ...]
    admission: Literal["backed", "gated"]
    gating_reasons: tuple[str, ...]

class QueryEnvelope(FrozenModel):
    profile: str
    parameters: ValidatedPayload

class CommandEnvelope(FrozenModel):
    profile: str
    dispatch_id: UUID
    parameters: ValidatedPayload

class ConfirmedContext(FrozenModel):
    profile: str
    administration: AdministrationId
    principal_binding_digest: Digest
    generation: int

class ProviderReply(FrozenModel):
    http_status: int
    media_type: str | None
    body: ResponseProjection | None
    content_digest: Digest
    received_ids: tuple[ProviderIdentity, ...]

class ProviderIdentity(FrozenModel):
    namespace: str
    value: str

class RequestContext(FrozenModel):
    correlation_id: UUID
    deadline: datetime
```

The public SDK envelope does not accept caller schema_id/digest or ValidatedPayload as a bypass. Each named tool exposes profile/dispatch_id plus its concrete path/query/body fields, then the shared codec constructs the internal envelope using that tool's immutable registration. Namespace values are a closed registry enumeration, not free strings in actual input models. The generic declarations above specify reusable internal composition; registry construction resolves concrete schema/type bindings before exposure.

Reply metadata does not infer provider success: HTTP2xx plus saved=false, Booleanfalse or bulk errors is still exactly that provider response. An empty response is absent body, not false or an invented echoed update DTO. PutWithBoolResult is a client wrapper style, not proof that a full updated object was returned. Known response models are projected when present; unclassified valid JSON is preserved with diagnostics. No transport ACK becomes financial verification.

## Narrow interfaces and CQS

```python
class AppQueryPort(Protocol):
    def query(self, operation: OperationSpec, request: QueryEnvelope,
              context: RequestContext) -> ProviderReply: ...

class AppCommandPort(Protocol):
    def execute(self, operation: OperationSpec, request: CommandEnvelope,
                context: RequestContext) -> None: ...

class ReceiptReader(Protocol):
    def get(self, dispatch_id: UUID) -> DispatchReceipt: ...

class ReceiptWriter(Protocol):
    def pending(self, intent: DispatchIdentity) -> None: ...
    def capture(self, dispatch_id: UUID, reply: ProviderReply) -> None: ...
    def failure(self, dispatch_id: UUID, failure: TechnicalFailure) -> None: ...

class SessionQueryPort(Protocol):
    def state(self) -> SessionState: ...

class SessionCommandPort(Protocol):
    def acquire(self, request_id: UUID, profile: str) -> None: ...
    def select_context(self, dispatch_id: UUID, allowed_alias: str) -> None: ...
    def dispose(self) -> None: ...

class LeaseReader(Protocol):
    def get(self, request_id: UUID) -> ContextLease: ...

class AuditWriter(Protocol):
    def append(self, event: AuditEvent) -> None: ...

class ArtifactCommand(Protocol):
    def import_source(self, dispatch_id: UUID, basename: str,
                      expected_hash: Digest | None) -> None: ...
    def capture_download(self, dispatch_id: UUID,
                         source: BinaryResponseHandle) -> None: ...

class ArtifactReader(Protocol):
    def get(self, artifact_id: UUID) -> ArtifactHandle: ...
```

Actual query/command registry views are distinct types: AppQueryPort rejects command descriptors before dispatch and receives no AppCommandPort. Session commands are technical auth effects; token material is held behind the private auth port, never in ContextLease or tool output. Query/capture coordination sits at the protocol/technical boundary; a pure receipt query never saves a receipt. Provider commands invoke the injected ReceiptWriter immediately and return None. The MCP handler then reads the receipt and presents it; it makes no extra API query merely to return an acknowledgement.

```python
class DispatchIdentity(FrozenModel):
    dispatch_id: UUID
    operation_id: str
    profile_binding: Digest
    administration: AdministrationId
    request_digest: Digest

class DispatchReceipt(FrozenModel):
    identity: DispatchIdentity
    phase: Literal["PENDING", "RESPONSE_CAPTURED", "OUTCOME_UNKNOWN", "NOT_DISPATCHED"]
    observed_generation: int | None
    reply: ProviderReply | None
    failure: TechnicalFailure | None
    updated_at: datetime

class TechnicalFailure(FrozenModel):
    stage: str
    original_type: str
    safe_message: str
    dispatched: Literal["no", "possible", "yes"]
    diagnostic_codes: tuple[str, ...]

class SessionState(FrozenModel):
    phase: Literal["unauthenticated", "challenge", "ready", "invalid", "closed"]
    confirmed: ConfirmedContext | None
    expiry_known: bool
    expires_at: datetime | None

class ContextLease(FrozenModel):
    lease_id: UUID
    confirmed: ConfirmedContext
```

Dispatch deduplication identity uses stable operation/profile/administration/request digest. Auth generation is an observation only, not an identity key: a restarted process with a new login generation must return the existing same-ID receipt instead of conflict/replay. Received IDs remain namespace-labelled; unknown IDs are not coerced into visible mutation numbers.

AuditEvent contains schema version, event/correlation/dispatch UUIDs, UTC time, nonsecret profile/context digest, operation/effects, stage, HTTP status/diagnostic codes and result digest. It contains no body/secrets. BinaryResponseHandle is an internal bounded stream owned by the transport, not a caller pathname. Shared presentation uses the SDK boundary and original redacted cause, not per-operation exception frameworks.

## Receipt durability and local artifact contracts

One writer instance per process owns append/result persistence. A canonical receipt filename is derived from dispatch UUID under the configured local root, not supplied by caller. OS cross-process lock plus exclusive creation protects the header and PENDING fsync before send. Typed result storage is separate from redacted audit. Same-ID receipt access is stable across login/restart; a different digest conflicts. Incomplete/corrupt/PENDING files fail closed for that ID; no TTL/alias/PID cleanup causes replay.

No source-key, invoice duplicate, payment completeness, plan/baseline or repair policy is stored. New UUID is a new explicit request, not a promised business-idempotency key. Provider bulk partial failures remain in the captured response; no automatic failed-subset replay. Provider errors, timeouts, cancellation and post-send capture failure never authorize a second write or compensation.

Host/operator intake copies a selected file into the fixed protected inbox, supplies its actual basename and optionally an expected hash. The import command rejects traversal/separators/device/alternate-stream names, symlink/reparse/nonfile/system/source escapes, reads bounded bytes and computes its own hash. It persists immutable artifact bytes; upload consumes that artifact. No manual hash computation, automatic source matching or output/ACL argument is required.

Binary GET and explicit artifact capture use the same command/receipt-reader separation. Query data, command ACK/result and downloaded bytes are private data returned to the authorized caller, not financial payload audit logs. Auth responses are excluded entirely from ordinary result persistence. Unknown write data cannot always be stored after disk failure; prior PENDING is the conservative surviving fact.

## Configuration contract and startup

```python
class ResourceLimits(FrozenModel):
    maximum_request_bytes: int
    maximum_response_bytes: int
    maximum_binary_bytes: int
    maximum_json_depth: int
    http_timeout_seconds: int
    operation_deadline_seconds: int
    cleanup_reserve_seconds: int
    maximum_workers: int

class AdministrationAlias(FrozenModel):
    alias: str
    administration: AdministrationId

class ServerConfig(FrozenModel):
    schema_version: Literal["2"]
    credential_reference: str
    principal_binding_digest: Digest
    default_administration_alias: str
    allowed_administrations: tuple[AdministrationAlias, ...]
    enabled_operations: frozenset[str]
    allowed_effects: frozenset[Effect]
    writes_enabled: bool = False
    transport: Literal["stdio"]
    private_root: Literal["per_user_local"]
    limits: ResourceLimits
    registry_digest: Digest
```

ConfigLoader is the sole reader and constructor at startup. Models do not load files or own ClassVar/singleton configuration. Credentials are host-backed Windows references, not values. Examples contain no actual administration, host path or account. Startup validates positive bounded resource limits, known operation/effect/schema IDs, duplicate aliases, supported fixed origin/version and private-root containment; malformed combinations fail before exposing tools. This is technical config consistency, not an accounting approval engine.

Credentials are lazy/shared once per process. All concrete implementations and handler registrations are created at startup and injected. No secret-bearing login/renew/challenge response is a normal receipt. MFA secrets use an external host interaction channel and never MCP arguments. Explicit context switching drains leases; no implicit admin selection on a query. Provider logout scope remains uncertain, so ordinary shutdown disposes locally without an unproved global revocation action.

## Required future verification

- Fixed named registry expansion and all57/23 coverage/admission references; no missing-schema callable placeholders.
- Strict JSON-mode envelope/provider/result roundtrip; exact number text; Int32 versus Int64 text; UUID/enum/array admission; Required3 optional-presence semantics; unknown preservation and input rejection.
- One selected provider request, no REST calls/bookkeeping calculations/local business loops; native provider bulk/calculation requests forwarded unchanged.
- N calls share credentials/session/connection/audit; refresh single-flight, MFA pause, explicit context leases and safe shutdown.
- CQS None returns, immediate capture, separate receipt query; 2xx/false/partial/empty bodies unchanged, never generic functional success.
- Two-process same-dispatch race, crash/PENDING, digest conflict, generation change/restart, disk failure, no TTL/replay/compensation.
- Artifact basename/bytes/hash/size/root guards; no auto source/alias/scan; no secrets or raw financial audit; stdout JSON-RPC only.
- Actual future CPython3.14/SDK2.3.0 stdio harness and pinned install. No such runtime evidence is claimed here.

No method bodies, production code, SDK installation, live requests or implementation cycle sequence are supplied by these declarations.

## Sources

- [APK contract evidence](apk-api-contracts.md)
- [Endpoint registry/admission catalogue](endpoint-design-catalogue.md)
- [Function evidence](api-functional-coverage.md)
- [Canonical architecture](design.md)
- [Json.NET Required semantics](https://www.newtonsoft.com/json/help/html/T_Newtonsoft_Json_Required.htm)
- [Pydantic strict JSON-mode behavior](https://docs.pydantic.dev/latest/concepts/strict_mode/)

## Version History

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 1.0 | 2026-11-01 | Imp | Historical workflow-shaped contracts. |
| 1.1 | 2026-11-01 | Imp | Close historical strict-JSON/inbox gaps. |
| 1.2 | 2026-11-01 | Imp | Mark earlier contracts historical after functional scope reopened. |
| 2.0 | 2026-11-01 | Imp | Replace with App-only technical registry, data-fidelity, CQS/receipt/auth/artifact contracts; no bookkeeping workflows. |
