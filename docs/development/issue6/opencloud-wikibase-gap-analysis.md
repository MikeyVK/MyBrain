<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# OpenCloud and Wikibase: gap-closure research

**Status:** Research assessment  
**Version:** 1.0  
**Last Updated:** 2026-10-24

## Purpose

Investigate the concrete integration work and early falsification tests needed for a provisional OpenCloud–Wikibase combination against MyBrain's own research and accepted principles.

## Scope In

Native reuse, configuration, proposed extensions, ownership boundaries, capture and registration, versioned meaning, failure recovery, retrieval evidence, access, export/restore, clean interfaces and full conceptual traceability.

## Scope Out

Adoption, an Approved Strategy, formal design or implementation planning, installation, executable trials, live/private ingestion, original mail/NAS implementation and issue-phase progression.

## Summary

OpenCloud and Wikibase could reuse substantial file, synchronization and claim-editing capabilities. The missing work is a coherent MyBrain application boundary: preserve identifiable admitted states, link explicit definition/application versions, recover interrupted operations, retain actual retrieval evidence and enforce rights across every in-scope disclosure. These are substantial integration responsibilities, not proof that another general knowledge database is needed. Six early gates—capture consistency, all-route revocation, append-rule coverage, historical query basis, recovery and preservation-safe destruction—should determine whether this combination still saves enough work.

## Authority, baseline and evidence limits

This is a research proposal about a provisional pair, not a product selection. The [accepted ADR v1.8](../../architecture/decisions/0001-digital-brain-foundational-principles.md) governs requirements; the [discussion map](../../architecture/digital-brain-discussion-map.md) distinguishes recorded principles from functions merely named for later discussion. The two earlier [platform](open-source-platform-candidates.md) and [knowledge-application](open-source-knowledge-core-candidates.md) reports supply the comparison baseline. They are not superseded or silently converted into adoption decisions.

All four pages of the screened [public research baseline v0.1](../../research/public/research-baseline.pdf) were read. Its sections 06 and 08 motivate durable checkpoints, visible processing gaps and reconciliation after unknown outcomes; section 07 leaves migration authority open; section 11 separates PGMCP from runtime memory and authorization. Case management, work items and daily overviews remain exploratory consumers, not mandatory foundation entities. Its repeat-import aspiration is interpreted with later P20–P22: do not invent independent sources from repeated receipt, but retain receipt history and expose uncertain recognition. Its rebuildable-summary idea does not override P26/P25 preservation of actual produced context and earlier results.

The source baseline is **OpenCloud 7.2.4**, commit 1770793f2657e153836c32d32dd6d256b8531d3d, with its pinned **reva 2.46.8** dependency; and **Wikibase Suite 8.0.1**, its selected MediaWiki 1.46.0/Wikibase REL1_46 snapshot eaa851d89…. The newer rolling OpenCloud release was not substituted. Exact component licensing remains as qualified in the earlier reports; an actual deployment must recheck its required components and models. Evidence is documentation and source inspection on **2026-10-24**, not observed runtime behavior.

The labels below mean: **native**—implemented upstream mechanism; **configuration**—using supported settings/models; **proposed own code**—integration or extension that still must be built; **unproven**—the required guarantee has not been established; **owner boundary**—a deliberately open contract/authority decision. No person-day estimate is justified before prototypes expose the expensive paths. No candidate, test journey or failure injection was executed.

## Minimum responsibilities, without a second knowledge store

The following are responsibility boundaries, not mandatory microservices, products or a selected framework. Several can initially be modules in one process. Native services should remain reusable; a separate general-purpose knowledge database beside Wikibase is not the default proposal.

| Responsibility | Reuse | Least-change proposal and authority boundary |
| --- | --- | --- |
| Working files and source content | OpenCloud clients, Spaces, storage, file/version APIs. | Separate mutable working exemplars from identifiable admitted states. Protected snapshots may use the same backend; their preservation guarantee must be proved. |
| Authoritative semantic registration | Wikibase entities, identified statements, references, qualifiers and revisions. | Configure source/version, definition/application and context/contract roles; preserve registered meaning through a bounded extension where native mutable edits are insufficient. |
| Operation recovery | Native events and mutation responses are inputs. | A durable operation journal records intent, evidence, mappings and unresolved outcomes. Its store is open; it must not become a duplicate canonical label/claim database. |
| Recognition and intake | API identifiers and change signals. | Versioned contracts interpret source evidence, packages and receipts. Source-specific adapters expose limits rather than assuming universal identity or exactly-once delivery. |
| Contract consumption | Stored files/entities can represent contracts. | Separate activation, authority, scope and implementation binding from storage. A stored contract is not executable permission. |
| Processing and indexes | Reusable extractors, models and query/index services. | Workers consume registered versions and emit attributable derived artifacts. Indexes are replaceable projections; authoritative history is retained elsewhere. |
| Retrieval and result retention | Native exact entity revision reads and file APIs; SPARQL discovery. | A domain service records actual inputs/basis, response contract and result, and distinguishes index freshness from source coverage. |
| Rights and release | Native ACLs, Wikibase permissions and OpenCloud policy evaluation. | Coordinate rights changes and every in-scope release; close or adapt bypass routes. Authentication and one final check do not prove atomic revocation. |
| Interface and exchange | Native administrative/editor screens plus APIs. | A clean task-oriented UI and future MCP adapter share the same domain operations, receipts and rights boundary. Export/restore covers the combined information. |

The journal needs operational facts such as an operation's uncertain outcome and its confirmed upstream identity/revision. That is different from independently maintaining “the current meaning of L” outside Wikibase. A reconciliation view can be disposable; durable registration remains authoritative in its chosen system. How journal records themselves receive identity/history and appropriate access is an open realization question under P34, not permission to create another authority by accident.

## Source capture: native versions are useful but not permanent source-version authority

OpenCloud has usable version APIs, not only a browser history screen: reva's [version endpoint](https://github.com/opencloud-eu/reva/blob/e54d2d903dbd331c8f103ddad39ab2b6ecd1d054/internal/http/services/owncloud/ocdav/versions.go) lists revisions and serves returned revision keys. However, the inspected [POSIX revision implementation](https://github.com/opencloud-eu/reva/blob/e54d2d903dbd331c8f103ddad39ab2b6ecd1d054/pkg/storage/fs/posix/tree/revisions.go) can rename an earlier revision key on timestamp collision and requires a live current node to retrieve a revision. [RestoreRevision](https://github.com/opencloud-eu/reva/blob/e54d2d903dbd331c8f103ddad39ab2b6ecd1d054/pkg/storage/pkg/decomposedfs/revisions.go) removes the selected revision file/metadata after restoration. A previously saved native version URL therefore cannot simply be declared MyBrain's permanent source-version identity.

Native upload handling is a substantial reuse seam: [the upload store](https://github.com/opencloud-eu/reva/blob/e54d2d903dbd331c8f103ddad39ab2b6ecd1d054/pkg/storage/pkg/decomposedfs/upload/store.go) locks an existing node, checks If-Match and can preserve the old revision before overwrite. That does not establish a generic “stat ETag, GET those exact bytes” capture protocol. The [download handler](https://github.com/opencloud-eu/reva/blob/e54d2d903dbd331c8f103ddad39ab2b6ecd1d054/internal/http/services/owncloud/ocdav/get.go) contains an explicit stat/read race concern and does not establish conditional If-Match forwarding; [ETag generation](https://github.com/opencloud-eu/reva/blob/e54d2d903dbd331c8f103ddad39ab2b6ecd1d054/pkg/storage/pkg/decomposedfs/node/node.go) uses identity/mtime information rather than a cryptographic content digest. Hashing the downloaded material records a fingerprint for integrity comparisons; without the appropriate trusted comparison it does not prove equivalence to an earlier stat result or an external provider version.

The least-change proposal is a stable MyBrain registered-version identity pointing to verified retained bytes and evidence of their acquisition. A separately identified admitted snapshot can live in a protected namespace on the same OpenCloud backend. A strong digest supports integrity verification against the retained capture; it must not become the sole criterion for shared item identity or origin. Equal-content independent items and repeated receipt occurrences remain distinguishable.

The acquisition route is still a gate. Capturing an authorized upload payload, reading a stable protected object, or using an upstream-supported snapshot operation are alternatives to investigate. A two-pass read/hash loop is not automatically a consistent snapshot under concurrent writes. If a received payload cannot reliably be matched to a provider version, preserve the received material and record that uncertainty; do not silently claim A_v1 was captured. Reference-only registration remains possible under P34, but must not claim preservation of the target or weaken P03 for an admitted original.

External filesystem writes require special caution. The [defaults](https://github.com/opencloud-eu/opencloud/blob/1770793f2657e153836c32d32dd6d256b8531d3d/services/storage-users/pkg/config/defaults/defaultconfig.go) disable watching and filesystem revision creation; [assimilation](https://github.com/opencloud-eu/reva/blob/e54d2d903dbd331c8f103ddad39ab2b6ecd1d054/pkg/storage/fs/posix/tree/assimilation.go) can skip a same-path/same-mtime observation and copies external revisions asynchronously. The supported write route and capture boundary must be explicit. Do not promise every local save or offline keystroke. OpenCloud's [conflict guidance](https://docs.opencloud.eu/docs/user/desktop-client/common-functionality/file-conflicts/) also leaves conflict copies local unless explicitly uploaded: centrally complete intake cannot include unknown local branches.

## A consistent failure model and honest acknowledgments

The proposal separates evidence milestones rather than presenting one green “synced” state. Their exact status vocabulary and storage schema remain open.

| Milestone | What may be acknowledged | What is not implied |
| --- | --- | --- |
| Observed or received | A signal/package/payload was encountered within a stated connection and scope. | Identity match, complete preservation, semantic registration or processing. |
| Recognized | A specific versioned contract supports a match, difference or explicitly unresolved identity. | That all content has been stored, or equal content means the same item. |
| Preserved capture or preserved reference | The agreed received bytes are durably retained and verified, or the reference itself is registered with explicit limits. | The reference target is preserved; the captured payload is a verified provider version. |
| Semantically registered | Confirmed source/version/receipt links and upstream identities/revisions have been durably associated. | Every processor or index has completed; all external receipt history is known. |
| Processed | One declared method/contract/version completed, partially completed or failed for specified inputs. | Every method succeeded or the output is true. |
| Returned | A particular response artifact/release attempt was recorded under its response and access contract. | The recipient read it, delivery completed after a broken connection, or later rights can recall copies. |

OpenCloud events help trigger work and recover observations. Its [event-history defaults](https://github.com/opencloud-eu/opencloud/blob/1770793f2657e153836c32d32dd6d256b8531d3d/services/eventhistory/pkg/config/defaults/defaultconfig.go) use NATS JetStream KV with TTL 0 in this baseline, contrary to the [live documentation's memory-default description](https://docs.opencloud.eu/docs/dev/server/services/eventhistory/information/). The [event-history service](https://github.com/opencloud-eu/opencloud/blob/1770793f2657e153836c32d32dd6d256b8531d3d/services/eventhistory/pkg/service/service.go) can log failed writes and continue; successful signal handling does not prove durable capture. The separate [main NATS stream](https://github.com/opencloud-eu/reva/blob/e54d2d903dbd331c8f103ddad39ab2b6ecd1d054/pkg/events/stream/nats.go) has a seven-day MaxAge default; that does not mean KV event history expires after seven days. Neither history nor queue retention preserves vanished source bytes. Reconciliation must compare the intended intake scope with durable registrations and retained material, not merely an empty queue.

Across OpenCloud and Wikibase there is no demonstrated cross-system commit. If capture succeeds and semantic registration fails, retain an incomplete operation and its preserved material for retry/reconciliation; do not declare a complete source version or delete the material as an orphan by default. If registration succeeds but the response is lost, record the outcome as in doubt rather than blindly creating again. Scope-limited work may continue elsewhere while the affected operation is unresolved.

Reordered or duplicated events should re-evaluate the durable operation and recognition evidence. A repeated receipt can add provenance without adding another independent source. Checkpoints advance only for the responsibility actually completed. Proposed retry limits, escalation and journal-retention policy are open; “retry forever,” silent dropping and exactly-once claims unsupported by the source contract are all unsuitable defaults.

## Wikibase: versioned domain records and no-fork enforcement candidates

A minimal candidate model distinguishes continuing identities/current views from registered version and event objects. A source may be opaque; binary/large content stays externally preserved and linked. Package, receipt, source identity and source version remain separate roles. These are proposed meanings built with native items, statements, qualifiers and references, not a chosen ontology, property catalog or mandatory status list.

For label L, keep origin W_v1 distinct from definition L_v1 and application AP1 to A_v1. Reuse preserves origin; renaming a display label does not silently revise meaning. A later meaning change produces L_v2, while AP1 still resolves L_v1. Rich assessment/withdrawal history can use separately identified events referring to AP1; simpler applications can use statement GUIDs where their contracts suffice. No universal confidence score, rationale document, passage citation or complete inference chain is introduced. Uncertain and contradictory applications coexist; selection under one use contract does not erase alternatives.

This is more than configuration if immutable registered states are required. Normal Action API and REST editing share [MediaWikiEditEntity](https://github.com/wikimedia/mediawiki-extensions-Wikibase/blob/eaa851d89d36136ab718f1fe5fa81a8b770c0d59/repo/includes/EditEntity/MediaWikiEditEntity.php). An extension can use its edit filters and the lower [MultiContentSave seam](https://github.com/wikimedia/mediawiki/blob/1.46.0/includes/Storage/PageUpdater.php) to compare proposed content with the authoritative parent and reject changes/removals/redirects of registered version/event records. Mutable current views and new versions can remain editable. This is a credible supported extension route, not an executed all-route guarantee.

There are verified bypass categories. [Old-revision import](https://github.com/wikimedia/mediawiki/blob/1.46.0/includes/Import/ImportableOldRevisionImporter.php) inserts through the revision store rather than the ordinary PageUpdater save path. [Item merging](https://github.com/wikimedia/mediawiki-extensions-Wikibase/blob/eaa851d89d36136ab718f1fe5fa81a8b770c0d59/repo/includes/Interactors/ItemMergeInteractor.php) saves items separately and uses an ignore-constraints flag; [property datatype changes](https://github.com/wikimedia/mediawiki-extensions-Wikibase/blob/eaa851d89d36136ab718f1fe5fa81a8b770c0d59/repo/includes/PropertyDataTypeChanger.php) also need lower-level protection. [Page deletion](https://github.com/wikimedia/mediawiki/blob/1.46.0/includes/Page/DeletePage.php) has a separate abortable pre-hook; revision visibility, purging and privileged maintenance have further boundaries. Native page deletion archives revisions and is not owner-authorized actual destruction across the combined system.

Least change means a bounded preservation extension plus restricted or controlled imports/maintenance, not pretending UI hiding enforces history. Test native UI, Action/statement APIs, REST, undo/rollback, merge, import and deletion. Administrators with raw database/filesystem access form an explicit operational trust boundary. Whether the necessary restrictions preserve enough native usability is an owner decision; unrestricted native routes are not proved safe and no unavoidable core fork has been established.

Concurrency needs equal precision. Action baserevid may participate in automatic conflict merging, so it is not simply strict If-Match. Lower [entity storage](https://github.com/wikimedia/mediawiki-extensions-Wikibase/blob/eaa851d89d36136ab718f1fe5fa81a8b770c0d59/repo/includes/Store/Sql/WikiPageEntityStore.php) protects an individual save against a racing revision. REST also has request preconditions. Neither proves a multi-entity transaction or a cross-product commit.

A lost successful create response is especially important: [REST EntityUpdater](https://github.com/wikimedia/mediawiki-extensions-Wikibase/blob/eaa851d89d36136ab718f1fe5fa81a8b770c0d59/repo/domains/crud/src/Infrastructure/DataAccess/EntityUpdater.php) allocates a fresh entity identity for a new creation. Client UUIDs, external-ID properties or statement GUIDs do not inherently enforce unique source identity. The minimal honest coordinator serializes an operation, records its operation identity and stops new-create retries while its outcome is in doubt. Reconcile against authoritative primary data, not an empty lagging search result. A stronger PHP API/extension with a unique operation-key mapping is plausible, but atomic coupling of that mapping to the native revision commit and recovery is additional own code requiring fault tests.

## Contracts, processing and a reproducible retrieval basis

Stored contract K_v1 is another registered artifact. Proposed activation records separately identify its authority, scope, effective conditions and the interpreter/configuration actually used. Merely uploading a document cannot activate its instructions. Source content, including apparent commands or prompts, remains data rather than authorization, as the public baseline already distinguishes. Activation within an owner's established rule may be automatic; this proposal adds no blanket per-operation approval.

Processing consumes an identified registered input version and emits a separately registered output/context version, with the relevant method, contract and model/configuration basis and visible limitations. Reprocessing under K_v2 leaves the old result understandable. Unknown provider/model details stay unknown; opaque internals need not be reconstructed. Dependency changes flag possible reconsideration without automatically declaring all derived outputs false. An owner correction needs an explicit versioned scope/rule so automation can preserve it.

A useful Wikibase construction avoids automatically adding another temporal database: immutable source, definition, application and assessment versions remain ordinary current items in the full statement graph. Old meaning can remain queryable as explicit data rather than relying entirely on historical graph snapshots. This costs domain modeling, append protection and query logic, but reuses the existing graph.

Native [revision-specific entity reads](https://github.com/wikimedia/mediawiki-extensions-Wikibase/blob/eaa851d89d36136ab718f1fe5fa81a8b770c0d59/repo/includes/LinkedData/EntityDataRequestHandler.php) take an entity/revision pair; redirect handling can otherwise resolve a current target. Keep namespace, identity and revision together and pin referenced definitions/contracts explicitly. A full RDF dump means full statement structure, not every old entity revision.

WDQS is an asynchronous projection. Discovering candidates there and checking each through authoritative APIs can improve result correctness but cannot prove that no eligible item was missing from the index. A strict published query cut needs a sealed input/assessment manifest and proved projection coverage, or another justified query mechanism. If that grows into a second authoritative knowledge store, reconsider the pair instead of stacking it silently. Do not narrow the declared retrieval scope after the fact merely to call an incomplete index complete.

Q_A must retain its actual response artifact and the actual versioned selection basis: participating sources/descriptions/applications, contracts, applicability, method/scope, relevant processing configuration and assessed completeness. Large results/manifests can be preserved artifacts with registrations, not giant entities. Record a constructed result separately from release attempts or uncertain delivery; a connection break does not establish what the recipient read. A saved expression, current citations, query timestamp or rerun is not Q_A's actual historical result.

## Access: reuse native policy, prove the whole release boundary

OpenCloud's [policy service](https://docs.opencloud.eu/docs/dev/server/services/policies/information/) reuses OPA/Rego evaluation, gRPC checks and proxy/postprocessing integration. The pinned [proxy policy middleware](https://github.com/opencloud-eu/opencloud/blob/1770793f2657e153836c32d32dd6d256b8531d3d/services/proxy/pkg/middleware/policies.go) evaluates admission and then calls the next handler. That is valuable native request control, not a response-chunk fence or evidence that revocation stops every running disclosure.

Authentication needs route-specific treatment. [App-token documentation](https://docs.opencloud.eu/docs/dev/server/services/auth-app/information/) states that disabling a user in an external identity provider does not invalidate those app tokens. The [auth-service documentation](https://docs.opencloud.eu/docs/dev/server/services/auth-service/information/) describes an internal administrative service user with broad stat visibility; it must not be called a least-privilege integration account. A narrower delegated/normal-principal route needs proof of its actual effective rights. Particular group/user-info caches are additional routes to inspect, not evidence that every share update has one universal delay.

Wikibase page/entity permissions and a private wiki remain useful. Shared SSO does not unify search, graph, export, history and source-byte rights. MediaWiki's own [authorization-extension guidance](https://www.mediawiki.org/wiki/Security_issues_with_authorization_extensions) calls for testing secondary paths; it does not imply private wikis are impossible.

The proposed closure records rights/versioned policy alongside sources and semantic registrations and coordinates every disclosure in a declared managed boundary: content, metadata, existence/counts, history, thumbnails/downloads, context, cached/derived outputs and future AI/MCP results. Reuse native ACL/policy machinery where it supplies the needed operation. Own release coordination must serialize effective revocation with disclosure; a final check followed by an unfenced send still has a race. Work may continue internally while further release is denied. Already delivered information cannot be recalled.

Every in-scope rights mutation must participate in that same boundary, or the relevant native UI, Graph/API, sharing, administrator and service paths must be restricted or synchronously adapted. Asynchronous event propagation/cache invalidation alone is insufficient. A restricted managed-access profile is a trial candidate, not an accepted loss of native editing/sync functionality or a weakening of P30. The exact effective point, release boundary, rights scope and derivative propagation remain owner contracts. Whole-route atomic revocation is currently **unproven** and should be an early stop/go experiment.

## Recovery, migration and explicit destruction

OpenCloud's [backup guidance](https://docs.opencloud.eu/docs/admin/maintenance/backup/) requires stopping the instance for a consistent backup and preserving configuration, system/metadata and blobs. POSIX identities also depend on extended attributes/sidecar information. Its [data export](https://docs.opencloud.eu/docs/admin/maintenance/dataexport/) is useful file/metadata reuse, not automatically a complete MyBrain package. Wikibase backups, full-history XML and current JSON/RDF exports serve different purposes.

The combined recovery package needs the actual dependency closure for its declared scope: stable source/version identities, preserved bytes or explicit unavailable-reference markers, receipt/recognition evidence, definitions/applications/assessments, contract/activation records, result/manifests, relevant rights and operational reconciliation state. This is a proposed contract, not a chosen archive format or another store. Backup coordination can use quiescence/checkpoints and manifests; two unrelated successful backups do not establish a coherent cut.

Restore must first hold disclosure closed until rights, destruction decisions and recovery state are reconciled. An old backup must not silently resurrect revoked grants or information the owner explicitly destroyed within the declared scope. P16 requires actual destruction across that chosen scope, not retaining hidden backup content while calling it deleted. Any minimal marker or destruction record has to respect that scope; details remain open.

Native preservation settings are not enough by themselves. Configuring automatic purge off can help, but the [trash purge path](https://github.com/opencloud-eu/reva/blob/e54d2d903dbd331c8f103ddad39ab2b6ecd1d054/pkg/storage/fs/posix/trashbin/trashbin.go) can destroy content and revisions, and restoration itself changes native revision availability. Working-copy deletion, withdrawal, hiding, access revocation and actual destruction need distinct supported routes. Migration must preserve identities and version links or carry an explicit mapping; connector-independent restoration and Q_A recovery are decisive tests.

## A clean interface and future MCP without parallel authority

Reusing Wikibase does not require a Wikidata-like everyday screen. A small interface can present source registration/progress, context, definitions and applications with their relevant history and uncertainty. Keep unrelated administration optional. OpenCloud's [sidebar extension](https://docs.opencloud.eu/docs/dev/web/extension-system/extension-types/right-sidebar-panel-extensions/) is a potential place to display related context without rebuilding all file interaction; a separate task view is another option to compare.

The concrete file journeys from the [platform assessment](open-source-platform-candidates.md#synthetic-validation-before-a-platform-decision) remain part of the pair's usability trial: hydrate ordinary local files, disconnect, open/edit them in native applications and reconnect; on a new/mobile device, preview compatible content, download the original, use a supported native edit/return route and register the returned state. Show changed, recognized, registered and processed outcomes separately. A placeholder, preview or successful transfer alone is not evidence of all these outcomes.

The UI and a future MCP adapter should call the same versioned domain operations and return the same durable outcome evidence. They must not become raw bypasses around capture, append protection or rights. Official [MCP authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) concerns transport-level delegated access; it is not MyBrain's complete object/processing policy. Its [tool model](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) can expose bounded operations and schemas. Token audience/authority, input validation and unsafe source instructions need the same boundary as the web path. No SDK, transport deployment or mandatory confirmation pattern is selected here.

## Concrete synthetic example

Let a synthetic source A have admitted bytes A_v1 and two receipt occurrences, R1 and R2. A repeated package P2 can refer to A_v1 and another item; P2 is not another A. The recognition contract may support the repeat match, or leave it unresolved without losing the receipt evidence.

Produce context W_v1 from A_v1 and register it as a source. Create label identity L with origin W_v1 and definition L_v1. Application AP1 connects L_v1 to A_v1 uncertainly; AP2 can contest that fit. L_v1 itself is not made uncertain by AP1. Reuse L on another source without changing its origin or demanding a new rationale document on every use.

Q_A selects an explicit permitted basis and preserves its actual response plus manifest. Later narrow/withdraw AP1, record an owner correction, and create L_v2 only if meaning truly changes. Add A_v2 and reprocess under a changed contract/model into a new context version. Q_B's current-applicability response may differ. Q_A must still resolve A_v1, W_v1, L_v1, the assessment states actually used and its actual retained result, within current access rights.

Inject failures between capture and registration, and lose the successful new-entity response. The outcome is either a confirmed mapping or visibly in doubt pending authoritative reconciliation, not another blind new entity. A local offline branch is not centrally captured until brought through the declared intake. Revoke a right after retrieval but before release, restore a backup into a fenced environment, then exercise owner destruction in a separate fixture. Each operation tests a distinct contract; no one successful happy path establishes the whole system.

## Traceability to all accepted principles

This table maps the pair, not a claim of implementation completion. **Covered** denotes a bounded native capability clearly present; **partial** means reusable mechanisms cover only part of the principle; **outside pair** assigns processing/application responsibility beyond the two stock products; **unresolved** flags a decisive unproved guarantee or open contract. None is a runtime acceptance verdict. Proposed closures remain proposals; no fixed schema or status vocabulary is adopted.

| Principle | Pair status | Reuse, missing behavior and proposed boundary |
| --- | --- | --- |
| P01 Broad extensible foundation | Partial | Generic files/items support many domains; minimal source registration must avoid a forced domain ontology or required understanding. |
| P02 Origin versus capture | Partial | Native metadata helps; receipt, source claims, observation and origin need distinct registrations and recognition contracts. |
| P03 Preserve admitted original | Unresolved | Native versions help but can move/disappear. Prove acquisition and retained admitted snapshots before acknowledging preservation. |
| P04 Minimal registration | Partial | Items/links can register opaque sources. Keep observations distinct from supplied authorship/identity claims and visibly unknown facts. |
| P05 Three functional domains | Partial | File content, statements and indexes can be separated. Proposed contracts govern functions without imposing a pipeline or fourth domain. |
| P06 Attribution and uncertainty | Partial | Statements/qualifiers/references are native; domain author/method/context and uncertainty must be modeled, not inferred from editor account. |
| P07 Similarity versus exact conditions | Partial | Exact structured selection is reusable; similarity/model comparison remains a processing responsibility with declared applicability. |
| P08 Stable identity/version change | Partial | File/entity identities and revisions exist. Registered source, meaning, representation and contract versions need explicit binding and append protection. |
| P09 Evolving reference frame | Partial | Version objects can preserve definitions/contracts; current queries must not silently reinterpret historical applications. |
| P10 Dependencies/corrections | Partial | Links can record dependencies; re-evaluation and preservation of scoped owner corrections require operational rules. |
| P11 Generic versioned contracts | Partial | Contract artifacts can be stored/versioned. Their interpretation and activation are separate own-code responsibilities. |
| P12 Durability/usability | Unresolved | Clients, APIs and editors are reused; combined integrity, restoration, cross-device usability and declared recovery limits need proof. |
| P13 Owner control/durations | Partial | Native rights help; processing/sharing/destruction, derivative propagation and separate access/retention/validity need explicit contracts. |
| P14 Autonomous upkeep | Outside pair | Workers/rules must maintain meaning within authorized scope, retaining corrections. No blanket manual-review requirement is introduced. |
| P15 Preserve before relevance | Outside pair | A later authorized mail adapter must preserve within scope before classification, including spam; this research resumes no mail ingestion. |
| P16 Explicit owner destruction | Unresolved | Native delete/purge is not the declared combined destruction lifecycle. Scope across snapshots, derivatives/backups and irreversible effect remains open. |
| P17 Connection distinct from intake | Covered, bounded | APIs provide exchange capability. Connection grants neither source authorization nor intake/completeness; outbound conditions remain separate. |
| P18 Intake/completeness | Partial | Events/enumeration are inputs. Durable checkpoints, reconciliation, coverage and failure handling belong to the adapter contract. |
| P19 Selectivity as scope | Outside pair | Versioned intake criteria must distinguish outside/undetermined membership from low value; narrowing never destroys preserved material. |
| P20 Item/state/exemplar | Partial | Native IDs help; copies, branches, repeated receipts and revisable identity matches require explicit evidence and relationships. |
| P21 Transfer packages | Partial | Existing transfers and items can be reused; package/occurrence models must allow many-to-many source/version relationships. |
| P22 Recognition contracts | Unresolved | Identifier/ETag/time semantics and consistent acquisition need source-specific proof; known, unchanged and completely captured remain separate. |
| P23 Description contracts | Partial | Explicit version links can cover all three domains. Meaning, targets, justified operations and reassessment need configured model/consumer rules. |
| P24 Validity versus chronology | Partial | Assessment events can retain effective conditions independently of recording time; no timestamp/rank automatically supersedes alternatives. |
| P25 Traceable actual retrieval | Unresolved | Exact revisions and full statements help; coherent selection coverage, version manifests and actual retained responses need own-code proof. |
| P26 Context as stored source | Partial | Preserve context artifact/version and its derivation, then register it like other sources; processing remains separate. |
| P27 Label origin versus use | Partial | L links to W_v1 once; AP1 links L_v1 to A_v1. Reuse preserves origin without universal per-use rationale. |
| P28 Applicability history | Partial | Append assessments/withdrawal rather than erasing AP1; historical use and current applicability must query differently. |
| P29 Method versus response | Outside pair | Domain retrieval/response contracts decide selection versus disclosed content; no mandatory bundle of all descriptions is assumed. |
| P30 Atomic direct revocation | Unresolved | Native ACL/OPA and page permissions are ingredients; whole-route mutation/release fencing is unproved and an early falsification gate. |
| P31 Scoped completeness | Outside pair | Adapter/processing/query contracts distinguish complete, incomplete and unknown coverage without exposing inaccessible existence. |
| P32 Partial-result usability | Outside pair | Contract or authorized recipient can assess sufficiency; UI must expose limits without overriding access or mandatory constraints. |
| P33 Application uncertainty | Partial | Existing claim primitives support AP1 uncertainty/dispute; configured models and query rules must preserve alternatives separately from L_v1. |
| P34 Universal registrability | Partial | Opaque bytes/references, contracts, journals and results can receive registrations. Reference preservation must not claim target preservation. |
| P35 Storage versus operation | Partial | Both products can store artifacts/results; contract activation, comparison eligibility and execution stay operational responsibilities, with retrieval rights still enforced. |

## Traceability to discussion functions and shared aspects

The map's coverage labels describe conceptual discussion, not approved product features. In particular F10/F12 name broader exchange/use questions; case-management, budgeting, bookkeeping and external action tools are not added as foundation requirements here. All shared S aspects have principle-level coverage, with realization details open.

| Map aspect | Pair status | Scope of this assessment and remaining responsibility |
| --- | --- | --- |
| F01 Origin observation/intake | Partial | Receipt recognition, capture acknowledgments and reconciliation proposed; source-specific guarantees unproved. |
| F02 Minimal factual registration | Partial | Opaque source/reference registration using native items/files; no mandatory source classification. |
| F03 Storage/preservation | Unresolved | Native storage reused; protected admitted state, integrity and preservation-safe operation proof required. |
| F04 Identify/distinguish | Partial | Identity/version/exemplar/package roles and revisable matches; native identifiers alone insufficient. |
| F05 Description contracts | Partial | Definition/application/contract versions and activation boundary proposed; concrete schemas remain open. |
| F06 Connect/jointly select | Partial | Shared descriptions/full-statement queries reused; joint membership does not establish truth or unique rationale. |
| F07 Compute/compare | Outside pair | Contract consumer and model/representation workers; storage can retain their inputs/results. |
| F08 Retrieve/find | Unresolved | Exact version retrieval, published query cut, response evidence and access/completeness gates need proof. |
| F09 Process/derive/evaluate | Outside pair | Optional processors produce registered contexts and explicit coverage, with correction/dependency rules. |
| F10 Export/exchange | Partial; broader function named | Combined recovery package considered; general outbound exchange guarantees and action integrations remain open. |
| F11 Present across devices | Partial; partially discussed | Reuse file clients and focused semantic UI; accessible cross-device evidence/history interaction needs user testing. |
| F12 Use information | Outside pair; broader function named | Retrieval usability is covered conceptually; case/action/financial applications are later consumers, not new pair requirements. |
| F13 Connection/channels | Covered, bounded | Native APIs/clients supply connection seams; authorization, intake and outbound conditions remain separate. |
| F14 Intake scope/selectivity | Outside pair | Adapter scope contracts, unknown membership and future-only/backfill choices; no value-driven deletion. |
| F15 Transfer packages | Partial | Explicit package/receipt-to-item/version relationships proposed; provider semantics and completion guarantees open. |
| S01 Origin/provenance | Partial | Receipt/source/derived origins and label origin version separated; matching evidence must be retained. |
| S02 Context/time/validity | Partial | Independent recorded/effective times and assessment events; not latest-wins. |
| S03 Identity/versions/frame | Partial | Append-protected versions/contract links; controlled identity correction and branching need tests. |
| S04 Dependencies/re-evaluation | Partial | Versioned dependency links plus proposed reconsideration, without automatic falsity or invented rationale. |
| S05 Uncertainty/conflicts/exactness | Partial | AP1/AP2 coexistence and use-specific selection; source statements and assessments stay distinguishable. |
| S06 Owner control/authorization | Unresolved | Native rights plus all-route release coordination; scope and exact effective/release boundaries remain open. |
| S07 Upkeep/correction | Outside pair | Operational rules preserve scoped owner corrections; autonomous use under those rules remains possible. |
| S08 Durability/integrity/recovery | Unresolved | Separate coverage judgments, crash outcomes and combined restore; successful storage alone is insufficient. |
| S09 Preservation/destruction | Unresolved | Preserve by default; no automatic destruction from hiding, withdrawal, low relevance or scope narrowing. |
| S10 Generic contracts/framework | Partial | All digital artifacts registrable; recognition/description versions distinct from activation and enforcement. |

## Cheap falsification experiments and dependencies

These proposed experiments are ordered to expose disqualifying costs early, not an approved issue plan. Use synthetic isolated fixtures and reference judgments. Rights and preservation are required from the first meaningful slice; they are not optional late hardening. Settings, payload scope, expected outcomes and admitted operation routes must be recorded before a trial.

| Experiment/dependency | Proposed operation | Expected evidence and falsifier |
| --- | --- | --- |
| G1 Acquisition/version gate | Upload A/B/C rapidly with colliding times; race stat/download with overwrite; rename, copy, restore an earlier version, delete a working exemplar. Include same-path/preserved-mtime external change separately. | Every acknowledged admitted version resolves its intended verified bytes. Wrong bytes under an acknowledged version, moved native keys treated as stable, or a successful ack before durable capture falsifies the route. No all-keystroke claim. |
| G2 Whole-route access gate | Pause downloads/generated output before release; revoke through every in-scope native/UI/API/admin/token route. Repeat with cached search/counts/history/thumbnails/public links and stale sessions. | No further in-scope disclosure after the defined effective point. One bypass or check/send race falsifies the claimed boundary; narrower managed access requires an explicit trade-off decision. |
| G3 Append/provenance gate | Attempt to change sealed A_v1/L_v1/AP1 through normal UI/APIs, import, merge, datatype change, rollback, deletion and admitted maintenance. Then add a legitimate correction/new version. | Prior state remains unchanged or the operation is explicitly controlled; permitted corrections remain possible. A bypass or an invariant enforced only by UI hiding falsifies the extension claim. |
| G4 Failure/idempotency gate | Duplicate/reorder events, restart during copy, exhaust storage, interrupt between capture/registration, drop a successful new-create response and replay. Simulate queue expiry/history gaps. | One confirmed registration or visibly in-doubt work with preserved evidence; distinct receipts survive. Blind duplicate creation, false completion or unrecoverable acknowledged bytes falsifies recovery. |
| G5 Historical query gate | Execute the A_v1/W_v1/L_v1/AP1/Q_A example, then withdraw/revise, delay/rebuild WDQS and change model/contract for Q_B. | Q_A's actual artifact and used states remain recoverable; Q_B can differ. Current substitutions, missing index items called complete or redirect-to-current confusion falsify historical semantics. |
| G6 Combined recovery gate | Restore into fresh identities/hosts without the source connector; preserve xattrs/sidecars and all linked semantic/result artifacts. Reconcile an interrupted journal operation. | Old source/version links, correction scope, contracts and Q_A still resolve; disclosure stays closed until rights/destruction are reconciled. Two inconsistent successful backups are failure, not recovery proof. |
| G7 Owner destruction gate | Destroy only a named synthetic scope, then inspect live versions, derivatives and included backups; separately restore an older backup. | The chosen content is actually gone within scope and cannot silently reappear. Retaining hidden copies while claiming destruction, or destroying on ordinary withdrawal, falsifies the lifecycle. |
| G8 Usability/exit gate | Register, review uncertainty, author context and retrieve history through a clean UI. Hydrate ordinary files, edit offline in native apps and reconnect; test new/mobile preview, original download and supported edit/return. Export/re-import a small package; include an opaque file and offline branch. | Actual local files/originals and returned edits are verified; changed, recognized, registered and processed states remain distinct. Incomplete work is visible; IDs survive or map explicitly. Placeholders, inaccessible originals, silent unregistered edits or lost semantics falsify the claimed journey. Rebuilding most native interaction argues against the pair. |

G1/G2/G3 should precede a broad implementation commitment. A small end-to-end slice can then combine G4/G5/G6; repeat rights/destruction tests on its real routes. Optional processing and MCP follow the same contracts after that slice works. Backup/restoration is exercised throughout, not treated as a final documentation exercise. Failures may justify a supported upstream extension, a narrower admitted route or reconsidering one component; none licenses silently weakening the accepted principles.

## Build versus reuse recommendation

Continue only with a bounded, evidence-producing comparison of this provisional pair. Reuse is substantial: OpenCloud's clients, file service and supported storage APIs; Wikibase's statements, entity editing, references and ordinary revisions; and existing authentication/policy/query machinery. Do not rebuild these merely to get a cleaner screen.

The own work is nevertheless **a sizable application integration**, not “just a connector”: durable capture/registration recovery, explicit version/application/contract modeling, preservation enforcement, trustworthy query basis/results, whole-route rights and combined recovery. Maintenance must include upstream API/hook compatibility and the admitted native routes. There is no measured basis yet for a calendar estimate or a claim that wrappers will be cheap.

Reconsider the combination if consistent capture needs invasive storage changes, source/meaning invariants cannot cover required native operations, atomic revocation requires sacrificing essential native client behavior, or historical completeness requires a second authoritative knowledge database. Also reconsider if the custom interface/recovery/policy code effectively replaces most of the applications. A component substitution or narrower useful role can preserve reuse value; installing more stores and services by default would merely conceal the mismatch.

This report adopts no stack, ontology, journal store, policy engine implementation, schema, status vocabulary or formal issue strategy. Original mail/NAS implementation remains paused. The remaining owner decisions concern admitted capture/access routes, retention/destruction/recovery scope, identity/validity/contract semantics, required completeness and usable native versus custom interaction. The proposed tests make those trade-offs concrete; none has been executed.

## Related Documents

- [Public research baseline v0.1](<../../research/public/research-baseline.pdf>)
- [Foundational principles, ADR 0001 v1.8](<../../architecture/decisions/0001-digital-brain-foundational-principles.md>)
- [Digital brain discussion map](<../../architecture/digital-brain-discussion-map.md>)
- [Open-source platform candidates](<open-source-platform-candidates.md>)
- [Open-source knowledge-core candidates](<open-source-knowledge-core-candidates.md>)
- [Repository agreements](<../../../README.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-24 | MyBrain research collaboration (Imp consolidation) | Initial evidence-based gap assessment for the provisional pair, complete principle/aspect mapping and proposed falsification journeys; no trials executed or architecture adopted. |
