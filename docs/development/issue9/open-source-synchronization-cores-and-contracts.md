<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Open-source synchronization cores and service contracts

**Status:** Research checkpoint — independent review requested; no technology selection  
**Version:** 1.0  
**Last Updated:** 2026-11-13

## Purpose

Investigate reusable sync cores and boundaries for independent clients and self-hosted storage.

## Scope In

Open-source file sync engines, APIs, storage contracts, security, history, admission and Windows-first evaluation.

## Scope Out

No installation, deployment, runtime experiments, private data, final technology selection or phase transition.

## Problem Statement

A synchronization service must provide reusable contracts and recovery without transferring unapproved content or silently imposing a fixed client or storage model.

## Goals

- Compare source-backed candidates and independent client/server boundaries.
- Identify exact evidence limits and security, license and integration risks.
- Propose equivalent synthetic tests without selecting a final stack.

## Findings

### Question, scope and evidence quality

The owner asked on 2026-11-13 for open-source synchronization services with a core and sharp contracts, enabling storage on the server and clients on different platforms to be developed separately. The operational requirement is a personal Windows-first system with a self-hosted NAS service, later Android/iOS, and a single integrated wizard for synchronization, device/group policy and the independent MyBrain intake decision. Local/offline policies, reconciliation, bulk safeguards, pre-content admission and transparent recovery remain those in the [policy and probe contract](synchronization-policy-and-probe-contract.md). The [independent client/NAS assessment](independent-windows-nas-sync-feasibility.md) compares ownership and effort; this research identifies concrete engine contracts.

Distinguish a sync **engine** (detect, reconcile and act), a **library/SPI** (embed or replace storage), an on-wire **protocol**, and a **transport/store**. A documented interface does not make implementations interchangeable or establish crash safety. Source and vendor documentation were inspected 2026-11-13. Candidate release snapshots are independent and not a tested compatible deployment. All runtime, platform, memory, security and interoperability claims need verification. No software was installed or executed, and no real NAS or private data was accessed.

The owner requires the app, libraries and services to be open source; Windows, iOS and DSM are accepted hosts. A project licence is not a recursive licence/SBOM audit of shipped binaries, build tools or optional services. The [sovereignty audit](../../research/public/opencloud-sovereignty-and-dependency-audit.md) states what remains to verify. External hosted discovery, relays, identities or updates are distinct from open-source code and must not be mandatory third-party dependencies.

### Longlist and triage

| Candidate and inspected version | Kind / likely reuse | Initial assessment and exclusion or shortlist reason |
| --- | --- | --- |
| [SharpSync v1.0.4](https://github.com/Oire/sharp-sync/tree/v1.0.4) | C#/.NET sync library, storage and policy interfaces, Apache-2.0 project. | Most direct candidate for independently owned clients and storage: interface and upload-path source inspected. Release published 2026-09-10; it is a small, recently released project, not demonstrated production maturity. Default behavior and plan errors are important gaps. Detailed below. |
| [Syncthing v2.1.7](https://github.com/syncthing/syncthing/tree/v2.1.7) | Go peer-to-peer engine, daemon/API plus specified BEP; MPL-2.0 project. | Mature comparison for proven operational mechanisms; protocol and daemon are not a storage SPI or a pre-upload approval guarantee. |
| [Seafile Community](https://manual.seafile.com/11.0/overview/components/) | Separate client and server services; sync platform. Desktop v9.0.21 and daemon snapshot in [existing comparison](windows-sync-candidate-comparison.md). | Mature client/server reference with its own object model; independently replaced backend and gate remain unproved. Assess selected Community edition and indirect dependencies. |
| [CubSync v0.3.1](https://github.com/cubsync/CubSync/tree/v0.3.1) | Kotlin engine, RemoteBackend SPI, Windows/Android, headless JVM; Apache-2.0 project. | Structurally promising research sample, but early and first-party LAN transport has no authentication or encryption. Not an accepted secure transport; only local/LAN backends found in tag. |
| [Pydio Cells Sync](https://github.com/pydio/cells-sync/blob/6fae51e73ebbd0e22b8aa8bb9985e046e33a5e2b/README.md) | Go desktop sync with endpoint abstractions; project GPLv3. | Interesting endpoint design but concrete cells/v4 dependency and Windows webview path complicate independent reuse. Exact headless/build route and security require testing. |
| [Mutagen v0.18.1](https://github.com/mutagen-io/mutagen/blob/v0.18.1/LICENSE) | Go daemon, pairwise file-sync sessions. | Three-way merge and resumable operation are relevant; official binary includes SSPL code. A build without SSPL is documented but its functionality and dependencies must be audited before consideration. |
| [Unison v2.54.0](https://github.com/bcpierce00/unison/blob/v2.54.0/README.md) | OCaml two-replica synchronizer, Windows and POSIX, normally SSH. | Valuable failure/conflict and delta benchmark. Its conventional pairwise workflow is not yet an independent server storage SPI or native integrated wizard; exact licence tree and embedding require further audit. |
| [rclone v1.75.2](https://github.com/rclone/rclone/blob/v1.75.2/COPYING) | Go transfer tool with many backend drivers, MIT project. | [Bisync](https://rclone.org/bisync/) provides a two-way batch mechanism, conflict policies and recovery switches. It is not an always-on governed client/core or guaranteed pre-byte hold. Backend differences and interrupted runs matter. |
| [CouchDB replication](https://docs.couchdb.org/en/stable/replication/protocol.html) | Specified JSON document replication, not a native file synchronizer. | Potential model for structured policy metadata, not a substitute for file walking, versioned filesystem sync or consent. No technology choice. |
| [Lazync](https://www.lazync.org/) | Free Pascal/Lazarus self-hosted server plus Windows client; project says GPL-3.0. | Explicitly alpha; its own status says local deletes/renames and full offline multi-device conflict resolution are incomplete. Architectural reference only, not a safe choice for irreplaceable data. |
| [OpenCloud Desktop v4.0.0](native-wizard-update-feasibility.md) | Existing C++/Qt client and Go server, documented baseline. | Existing bounded synthetic filtering measurements but no general asynchronous approval seam or full policy; compare on the same acceptance tests rather than assume a fork is unnecessary. |

Unison is the file synchronizer at bcpierce00/unison, not the unrelated programming language project of the same name. Tags cited here pin source snapshots, not verified binaries, build chains, mobile support or every applicable licence. The longlist is representative, not a claim of exhaustive discovery.

### SharpSync: closest public library contracts, with critical caveats

The [v1.0.4 ISyncEngine](https://github.com/Oire/sharp-sync/blob/v1.0.4/src/SharpSync/Core/ISyncEngine.cs) exposes GetSyncPlanAsync, SyncFilesAsync, SyncFolderAsync, SynchronizeAsync, local/remote notifications, pause/resume and progress. [ISyncStorage](https://github.com/Oire/sharp-sync/blob/v1.0.4/src/SharpSync/Core/ISyncStorage.cs) defines list, read/write streams, delete, move, hash and connection checks. These are real source interfaces, not proof of a stable network protocol or independently deployable server. The project describes local, WebDAV, SFTP, FTP and S3 backends; backend-specific transactions, change detection, remote atomicity and custom NAS/server compatibility remain untested. Plain FTP is not a secure route for private data.

The [implementation](https://github.com/Oire/sharp-sync/blob/v1.0.4/src/SharpSync/Sync/SyncEngine.cs) was read directly. Its constructor defaults to a filter described in source as sync-everything. GetSyncPlanAsync catches general exceptions, logs them and returns an empty Actions list: a consumer cannot safely equate an empty plan with verified absence of candidates. SyncFilesAsync detects changes again before it executes; the presented plan is not by itself a frozen, content-bound execution token. UploadFileAsync opens the local stream and passes it to the remote WriteFileAsync. Pause is documented to finish the current file first. Consequently neither the interface names nor a preview demonstrate a fail-closed gate, approval of exactly those bytes, live revocation or protection from alternate transfer entrypoints. A wrapper or fork may need explicit typed plan errors, an enforced content-bound gate, stable snapshots and careful revalidation, without trusting a later timestamp alone.

The [project manifest](https://github.com/Oire/sharp-sync/blob/v1.0.4/src/SharpSync/SharpSync.csproj) targets net8.0 and lists versions for sqlite-net-pcl, WebDav.Client, SSH.NET, AWSSDK.S3 and FluentFTP. Its comment explicitly says sqlite-net-pcl brings a native SourceGear SQLite library, despite the README's broad no-native-dependencies wording. Audit the actual recursive packages, build/runtime binaries and [.NET distribution terms](https://github.com/dotnet/core/blob/main/license-information.md), including secure backend and mobile feasibility. No native Windows client, Android/iOS binding, NAS service, group policy, MyBrain wizard, retained source history or production maturity is established by this library.

**First discriminating test, proposed only:** use v1.0.4 with synthetic local and instrumented fake storage. Deny unknowns by construction; assert no WriteFileAsync content before explicit approval. Inject plan-listing failure and require visibly failed/held rather than empty-success. Change bytes between preview and execution, retry after interruption, test conflicting and selected/unselected paths, and ensure no independent full-sync path bypasses the gate. Check read-only preview and metadata egress too. A successful test establishes only the tested wrapper/engine configuration.

### Syncthing: mature engine, but peer rather than interchangeable storage

Its [BEP v1 specification](https://docs.syncthing.net/specs/bep-v1.html) describes a cluster of peer folder models, metadata/block hashes and block requests on authenticated TLS. The [REST API](https://docs.syncthing.net/rest/index.html) offers external control, but API access does not make the internal engine a stable embedded library or arbitrary server-storage adapter. Device keys protect peer connections; external discovery and relay defaults must be explicitly assessed and may be disabled/replaced subject to connectivity. The [ignore rules](https://docs.syncthing.net/users/ignoring.html) are local to each root; they are not shared group policy, acknowledgement or an atomic decision handshake.

[Versioning](https://docs.syncthing.net/users/versioning.html) is disabled by default and archives replaced/deleted versions received from another device, not every prior edit on the originating device. Its [FAQ](https://docs.syncthing.net/users/faq.html) notes that reconnecting peers can see only the latest resulting state, not every intermediate change. Sync is not a backup. The normal implementation publishes file metadata and block hashes as part of its peer model; the required distinction between allowable candidate metadata and prohibited content must be tested. An off-the-shelf iOS route, NAS footprint under load, a cross-device MyBrain policy wizard and fail-closed first-byte enforcement have not been established.

**First discriminating test, proposed only:** run isolated pinned peers and a controller with a previously installed default-deny, expose a synthetic root, and instrument actual requests/content through initial scan, a live new file, policy edit, offline/reconnect, restart, rename and retry. A positive control transfers only the permitted file. Induce stale policy and process crash. If any unknown content escapes or a restart opens a gap, unmodified daemon/control API is insufficient; investigate a source-level gate or remove the route from consideration.

### Seafile Community: structured platform, not automatically a swappable core

The [component documentation](https://manual.seafile.com/11.0/overview/components/) describes a web frontend separately from the server daemon which handles data upload, download and synchronization; it documents HTTPS deployment. The [data model](https://manual.seafile.com/14.0/develop/data_model/) describes managed filesystem objects and blocks, not an automatically interchangeable ordinary-files directory. The [licensing page](https://manual.seafile.com/latest/introduction/contribution/) distinguishes project components and editions. Desktop v9.0.21 and daemon snapshots were examined in the [existing comparison](windows-sync-candidate-comparison.md); exact selected server/client pair and its indirect licensing need verification.

This is a credible more established comparison when retaining a full service is acceptable. However the separation between web/frontend and daemon does not prove a public stable contract for replacing the storage engine or desktop sync, atomic local admission, the requested portable wizard or all backend editions under OSS terms. Conflict, version retention, deletion and backup policies must be tested for the chosen deployment. No seamless migration of existing OpenCloud files or history is implied.

**First discriminating test, proposed only:** in an isolated Community server with documented exact version and synthetic dataset, verify ordinary-file/export and version restore semantics, then instrument all initial and retried client uploads against a pre-established deny rule. Compare rule changes and watcher/restart races with the same fixture used for OpenCloud and SharpSync. Client or server edits become part of the measured fork cost.

### CubSync: useful SPI example, currently insecure first-party transport

The [v0.3.1 architecture](https://github.com/cubsync/CubSync/blob/v0.3.1/docs/ARCHITECTURE.md) and [RemoteBackend source](https://github.com/cubsync/CubSync/blob/v0.3.1/core/src/commonMain/kotlin/io/github/cubsync/core/spi/RemoteBackend.kt) define list/stat/hash/delete/rename plus read/write streams, capability bits and a staged commit/abort contract. These are promising explicit boundaries and include a resume offset. They are source contracts, not proof each backend actually provides durability, safety or reliable end-to-end resume.

The project repository was created in October 2026 and is early-stage; age alone does not establish quality. The tag's module inventory lists local and first-party LAN backends only. Although its README discusses WebDAV, SMB, SFTP and FTP as possible implementations, [architecture](https://github.com/cubsync/CubSync/blob/v0.3.1/docs/ARCHITECTURE.md) describes adding WebDAV as future work; do not credit those implementations as already shipped. The [README security statement](https://github.com/cubsync/CubSync/blob/v0.3.1/README.md) explicitly says its LAN protocol is unauthenticated and unencrypted. It is therefore not a safe NAS transport for the target as delivered; a secured implementation must be built and proven, not assumed from the SPI. The [versioning policy](https://github.com/cubsync/CubSync/blob/v0.3.1/docs/VERSIONING.md) allows protocol/API change before 1.0. Desktop/Android builds are project statements; iOS and complete shared presentation support are not established. JVM overhead on 6 GB NAS and actual test coverage/maturity remain unknown.

**First discriminating test, proposed only:** inspect the planner-to-write seam with an in-memory backend and fault injection, proving deny-before-openWrite, immutable approval under changes and crash-safe commit. Independently implement or select an authenticated encrypted backend only after licence review, and then test downgrade, certificate/authentication failure and path escape. The existing insecure LAN protocol must never be represented as acceptable just because the lab is local.

### Pydio Cells Sync and Mutagen: secondary contract comparisons

[Pydio Cells Sync source](https://github.com/pydio/cells-sync/blob/6fae51e73ebbd0e22b8aa8bb9985e046e33a5e2b/README.md) describes combinations of local, S3, Cells and NodeProvider/NodeReceiver gRPC endpoints. Its pinned [go.mod](https://github.com/pydio/cells-sync/blob/6fae51e73ebbd0e22b8aa8bb9985e046e33a5e2b/go.mod) nevertheless depends on cells/v4 and webview_go. The repository contains a Windows WebView2-related directory. A headless/open replacement UI and a non-Cells backend may be possible, but actual code coupling, compatible server contract and selected Windows runtime are not established. The inspected main snapshot is from 2024; project currency, ownership and security maintenance need fresh verification. First test: compile/source-audit a pinned headless test configuration, replace one endpoint with a fake and prove policy gate before network writes. This is a proposal, not an installation result.

[Mutagen documentation](https://mutagen.io/documentation/synchronization/) describes a daemon with pairwise sessions, three-way reconciliation and separate endpoint roles. Its default two-way-safe mode can still propagate certain changes; do not conflate conflict safety with the owner's deletion and approval requirements. The [v0.18.1 licence](https://github.com/mutagen-io/mutagen/blob/v0.18.1/LICENSE) states official binaries from v0.17 include SSPL code by default and describes a build without that flag. The latter is only a possibility; verify every resulting feature, dependency, source and distribution before treating it as meeting the open-source rule. First test: audit the exact non-SSPL build and verify that the desired OS/NAS, security and pre-first-byte gate are present without proprietary service. No implementation or binary has been tested.

### Comparative interpretation and initial ranking

1. **SharpSync for the first contract-focused code experiment**, because the inspected storage interface, plan and explicit file-sync entrypoints are closest to the requested separate client/storage responsibility. This is a provisional research ranking, not a recommendation for production. Its default-allow, empty-plan-on-error, plan/re-execution race, .NET/native dependency and mobile uncertainty are significant. If fail-closed behavior requires invasive changes or the runtime fails the open-source audit, reassess.
2. **Syncthing as the robust operations and failure benchmark**, not as a proven interchangeable server backend. Its peer protocol and existing engine give a strong contrast for interruption, transport and conflict behavior; centralized device policy, independent storage and content gate are still custom or unproved.
3. **Seafile Community and current OpenCloud as integrated-platform controls**, useful to compare mature server/client behavior and the cost of maintaining a patch. Their source separation does not automatically grant a stable replaceable core. Candidate placement can change once realistic gate, history, resources and licence tests are available.
4. **CubSync as an SPI reference only until secure transport and maturity are demonstrated**; Pydio and non-SSPL Mutagen builds are secondary investigations. No candidate is confirmed to satisfy all requirements.

This order favors fit to the requested contract, not product maturity, and must not be read as a verified safety rating. Own policy, integrated user flow, group/device registry, offline reconciliation, bulk consent, MyBrain boundary, audit, packaging and backups remain MyBrain work in every route. A transport library, a protocol and a finished server are not equivalent deliverables.

### Consistent synthetic benchmark and acceptance gates

Use one isolated synthetic dataset and request/body instrumentation for each serious candidate, with no production access. Specify source and binary digests, dependencies, server/client versions, settings and actual test hardware. A versioned baseline must include positive and negative controls, exact expected/actual results and errors, with content bytes distinguished from limited metadata:

1. New nested unknown file and a permitted control: no unknown content before consent, on initial scan, live addition, restart and reconnect. Test unsupported/missing filter or failed plan as fail-closed.
2. Selected bounded set, unrelated file, and content changed after approval: compare actual bytes and content identity; no leakage by preview, retry or an alternate running client. Check continuing approved flows and bulk limits separately.
3. Offline local draft and independently confirmed shared change; group overlap and device exception; apply/reconnect with acknowledgement and ambiguous conflicts held for owner. Show last-known versus current data and explicit independent MyBrain choice.
4. Interrupt at several transfer stages and during server state commit; check authenticated reconnect, partial data, expected hashes, stable retry, storage quota, power/restart simulation, two-device simultaneous edits, deletions and restore. Verify old copies survive and model state matches actual files.
5. Exercise directory watcher overflow/reinventory, rename, symlink/path traversal, case changes, large directory, continuously written file and an inaccessible source. Assess history of source updates, not just latest sync state.
6. Measure idle/peak RAM and CPU on a 6 GB target and separately under realistic other-service load, disk I/O, throughput, startup, recovery and update/rebase effort. Disclose sample sizes and fixture limits; no universal threshold or performance claim is implied.
7. Audit selected source and binary SBOM, licences and build reproducibility; deny internet while checking required local operation and record egress, TLS, identity and updates. Mobile platforms and native packaging need separate tests.

The smallest first step is a focused synthetic SharpSync contract test and an equivalent OpenCloud or Syncthing comparison; the proposed work has not been performed. No result here selects a product or authorizes a phase transition.

## Related Documents

- [Issue 9 research](<research.md>)
- [Policy and probe contract](<synchronization-policy-and-probe-contract.md>)
- [Independent client/NAS assessment](<independent-windows-nas-sync-feasibility.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-13 | PGMCP research implementer | Compare source-inspected synchronization cores, contracts, risks and equivalent synthetic tests. |
