<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Windows synchronization candidates for the integrated wizard

**Status:** RESEARCH CHECKPOINT — Windows-first comparison; no candidate selected or runtime proof  
**Version:** 1.0  
**Last Updated:** 2026-11-05

## Purpose

Compare existing applications and controllable engines for issue 9's Windows-first integrated synchronization/rules wizard before choosing a design.

## Scope In

Unknown-file admission before content transfer, ordinary connected-folder work, integrated MyBrain choice, reusable rules, owner devices, Windows availability modes, external control and update preservation.

## Scope Out

No general MyBrain platform reselection, knowledge/AI/wiki/accounting comparison, storage redesign, installation, benchmark, live client/server modification, migration, selected architecture or phase exit.

## Summary

No examined stock app demonstrates the entire integrated wizard. Syncthing offers the clearest existing external device/configuration control for a new Windows wizard if changing the transport/topology is acceptable. Rclone UI plus rclone is the most relevant additional native Windows UI/transfer reuse candidate when retaining OpenCloud is important, but actual OpenCloud interoperability and controlled admission remain unproved. Nextcloud and Seafile supply useful existing sync UI yet do not establish a smaller complete wizard/update gap. These are conditional trial recommendations, not adopted replacements.

## Scope and evaluation method

The owner prioritized realizing the integrated wizard and rules with Windows first, and requested an alternatives check before Design. The [earlier platform research](../issue6/open-source-platform-candidates.md) supplies candidate discovery only. Its broad ranking for knowledge/workspace functions does not decide this narrower issue. In particular, Seafile's previously examined closed metadata/AI dependency does not disqualify an open-source Community synchronization path that does not require it.

The accepted [wizard requirement](native-wizard-update-feasibility.md#accepted-interaction-requirement) remains unchanged: one native-client flow, summary and confirmation cover storage, selected devices and supported availability, MyBrain admission, and present/future reusable scope. Unknown new content in an ordinary connected directory must stay local until an applicable decision; later matching files need not require manual per-file approval.

This comparison separates built-in capability, public external control, custom UI/integration work, unproved behavior and an explicit workflow/backend change. An unknown is not scored as absent; feature count is not a feasibility verdict. Source and documentation were inspected on 2026-11-05. No app was installed, exercised, upgraded or benchmarked. Mobile is a continuity consideration rather than a requirement to complete the first Windows proof.

## Version and required-component register

| Candidate | Inspected source/version | Open-source boundary for this investigation |
| --- | --- | --- |
| OpenCloud baseline | Desktop v4.0.0 and the pinned Android/iOS evidence in the [native assessment](native-wizard-update-feasibility.md). | Existing open-source client/server path; no new closed dependency is selected. |
| Nextcloud Desktop | [Released v35.0.0](https://github.com/nextcloud/desktop/releases/tag/v35.0.0); later default-branch search used only to locate files, with decisive claims re-read at that tag. | [Desktop GPL-2.0-or-later](<https://github.com/nextcloud/desktop/blob/v35.0.0/README.md>); the earlier research identifies the separate AGPL server. Additional optional apps are not needed or credited here. No claim that this is today's recommended installer. |
| Seafile Community sync | GUI [v9.0.21](https://github.com/haiwen/seafile-client/releases/tag/v9.0.21), daemon source af6539cebf8484fcd07a4cab7ddfdfc425034a76, Seahub source 34dcc22f791cae4a3197635fb8f7c1a57a9033b6. | [GUI Apache-2.0](<https://github.com/haiwen/seafile-client/blob/v9.0.21/LICENSE>), [sync daemon GPLv2 with an OpenSSL permission](<https://github.com/haiwen/seafile/blob/af6539cebf8484fcd07a4cab7ddfdfc425034a76/LICENSE.txt>), Community server/Web component licenses identified by the [official contribution guide](https://manual.seafile.com/11.0/contribution/). These independent snapshots are not a verified packaged combination. Pro/AI/metadata services are outside the needed path. |
| Syncthing | [v2.1.7](https://github.com/syncthing/syncthing/releases/tag/v2.1.7), d6d0181f7d466381c4b39ec8fd944c364f939b32, Windows assets available. | [MPL-2.0 engine](<https://github.com/syncthing/syncthing/blob/d6d0181f7d466381c4b39ec8fd944c364f939b32/LICENSE>). A chosen native wrapper and its dependencies would need their own admission; no proprietary wrapper is required by the engine. |
| rclone | [v1.75.2](https://github.com/rclone/rclone/releases/tag/v1.75.2). | [MIT engine](<https://github.com/rclone/rclone/blob/v1.75.2/COPYING>); Windows support and protocol use must be verified in the selected proof. |
| Rclone UI | [v3.7.5](https://github.com/rclone/rclone-ui/releases/tag/v3.7.5), 453cc0c7dbc8cf355058ce92cc577b8002f97985, Windows release assets. | [Apache-2.0 application source](<https://github.com/rclone/rclone-ui/blob/453cc0c7dbc8cf355058ce92cc577b8002f97985/LICENSE>). Some distributed features have license checks; source licensing, price and vendor-free/offline operation are separate questions. The exact required feature/build chain remains to be checked. |

This is a named-component source screen, not a complete dependency or installer audit. A paid feature is not automatically closed-source. A public GUI repository alone also does not prove that every required daemon, driver or distributed feature is open and usable on the selected path.

## Capability comparison

Legend: **Existing** is documented/source-observed; **Custom** requires MyBrain-facing work; **Unproved** needs a targeted proof; **Change** alters the current OpenCloud/native workflow or backend.

| Candidate | Native Windows UI and ordinary files | Reusable control before unknown content leaves | Device knowledge | Update boundary |
| --- | --- | --- | --- | --- |
| OpenCloud stock client | Existing native UI, local sync roots and supported availability modes. | Exclusions/internal seams exist; a full durable admission hold is Unproved. Integrated wizard is Custom. | Complete owner device/capability/effective-policy catalogue Unproved. | Existing updater; internal/provider integration remains version-coupled. |
| Nextcloud stock client | Existing native UI, ordinary sync and Windows virtual-file modes. | Existing exclusions and internal propagation signals; no complete public wizard/hold contract established. Integrated wizard is Custom. | Login/session records and local account configuration do not establish the required effective per-device rule controller. | Existing official updates; VFS provider version check and a custom native UI still require compatibility work. |
| Seafile Community sync | Existing native GUI and ordinary local library sync. | Existing library/global auto-sync controls and ignore file. Per-set pre-content gate across initial clone, edits and retry is Unproved; wizard is Custom. | Existing server device list is useful partial reuse; device capabilities and applied per-file policy remain Unproved. | GUI/daemon split helps reuse; RPC compatibility and a custom GUI/update path still need proof. |
| Syncthing engine with own Windows wizard | Existing Windows engine and browser GUI; native wizard/host is Custom. Ordinary peer folders remain real files. | Public REST configuration and first-match positive inclusion/exclusion are promising; pre-established deny behavior plus safe incremental changes still need proof. | Existing configured-device catalogue includes offline peers; folder membership is not a complete per-file device-policy system. | Own UI can call an unmodified, independently updated engine; API compatibility still needs testing. |
| rclone executor with own UI | Existing engine; own native wizard/observer is Custom. Ordinary source files can be retained. | Explicit invocation and per-call filters can form an owned route; no concurrent stock-sync bypass may remain. Stable-snapshot/retry proof is needed. | Account/remotes do not establish the owner's device catalogue. | Engine updates can remain separate; controller/protocol compatibility and bidirectional semantics need proof. |
| Rclone UI plus rclone | Existing native Tauri Windows host, operation forms, previews and scheduler. | More UI reuse than a new empty frontend; unknown-file discovery/hold, shared admission and integrated MyBrain rule remain Custom/Unproved. | Filesystem volume/remote records do not establish the owner-device requirement. | Separate native UI and engine update routes; UI modifications still need upstream acceptance or an owned release path. |

All rows still need a single coherent MyBrain choice inside the wizard. The fact that a stock product does not already know MyBrain is not itself a reason to reject reuse; the comparative question is how narrowly that choice and enforceable rule control can be added.

## Nextcloud and Seafile: useful apps, no demonstrated complete gap reduction

Nextcloud has a mature native synchronization surface, but the inspected [sync signal](<https://github.com/nextcloud/desktop/blob/v35.0.0/src/libsync/syncengine.h>) is an internal mutable propagation-vector signal, while the [VFS loader](<https://github.com/nextcloud/desktop/blob/v35.0.0/src/common/vfs.cpp#L200>) requires the expected full client version. These permit internal integration research, not a demonstrated forever-stable general addon contract. Its [ignored-files editor](https://docs.nextcloud.com/server/stable/user_manual/en/desktop/usage.html) and [exclude implementation](<https://github.com/nextcloud/desktop/blob/v35.0.0/src/csync/csync_exclude.cpp>) are useful existing controls; safe positive admission across Windows traversal/reload/VFS behavior remains Unproved. A native setup or large-folder confirmation is not automatically a new-local-file upload wizard.

The normal [Nextcloud client](<https://github.com/nextcloud/desktop/blob/v35.0.0/README.md>) is intended for Nextcloud Server. Connecting it unchanged to OpenCloud with all its expected discovery/login/sync features was not established. Moving to the normal supported Nextcloud stack would be a backend decision with migration cost, without a demonstrated issue-9 wizard advantage. The broad earlier integrated-platform recommendation is therefore insufficient reason to switch for this scope.

Seafile provides a clearer GUI/daemon boundary: the [GUI RPC client](<https://github.com/haiwen/seafile-client/blob/v9.0.21/src/rpc/rpc-client.cpp>) uses a local named pipe and controls global or library auto-sync; the [daemon RPC surface](<https://github.com/haiwen/seafile/blob/af6539cebf8484fcd07a4cab7ddfdfc425034a76/include/seafile-rpc.h>) exposes library/property/manual-sync operations. This may reduce GUI/engine coupling, but turning auto-sync back on is not proof that all newly unknown files stay held. Initial library setup, existing-file changes and retries need admission coverage.

Its [ignore-file documentation](https://help.seafile.com/syncing_client/excluding_files/) describes client-side exclusions and important already-synced/server-origin behavior. Do not treat it as a complete per-device central rule language or infer a safe allowlist from exclusion support alone. The inspected [DevicesView](<https://github.com/haiwen/seahub/blob/34dcc22f791cae4a3197635fb8f7c1a57a9033b6/seahub/api2/views.py>) and [TokenV2 device model](<https://github.com/haiwen/seahub/blob/34dcc22f791cae4a3197635fb8f7c1a57a9033b6/seahub/api2/models.py>) genuinely list named user device records, platforms/client versions and last access; that is useful partial reuse beyond an unlabelled token list. It does not establish device capabilities, rule-application acknowledgements or a MyBrain source registration.

The Seafile Community sync path deserves consideration on its own merits. It normally uses the Seafile server/protocol rather than acting as a generic OpenCloud client. SeaDrive's virtual-drive path is distinct from ordinary sync; its exact Windows daemon/driver/source and availability behavior were not fully admitted here, so the table does not credit unverified on-demand parity or declare that entire path closed.

## Syncthing: strongest device/control reuse if topology may change

The [REST API](https://docs.syncthing.net/dev/rest.html) is used by its GUI and other processes; it is an external control surface with an explicit subject-to-change warning. [Configured devices and folders](https://docs.syncthing.net/rest/config.html) provide offline inventory independently of live connections. The [FAQ](https://docs.syncthing.net/users/faq.html#i-dont-like-the-gui-or-the-theme-can-it-be-changed) explicitly allows replacing GUI assets and describes engine updates. This supports a candidate in which a native Windows wizard talks to an otherwise unmodified engine, avoiding a core sync-engine fork; the native host is still new or adapted work.

[First-match ignore rules](https://docs.syncthing.net/users/ignoring.html) support positive inclusion before a catch-all exclusion, with traversal caveats. The pinned [scanner](<https://github.com/syncthing/syncthing/blob/d6d0181f7d466381c4b39ec8fd944c364f939b32/lib/scanner/walk.go#L333>) skips ignored paths before hashing/indexing, so the engine's database/events do not supply a complete inventory of unknown excluded candidates. A local observer/worklist remains necessary. The [.stignore update implementation](<https://github.com/syncthing/syncthing/blob/d6d0181f7d466381c4b39ec8fd944c364f939b32/lib/model/model.go#L2232>) writes rules and schedules a scan; HTTP success is not independent proof that a decision is effective for every relevant path.

This catalogue is each instance's configured peer view, not an automatically complete account-wide inventory of every owner device. Owner enrollment/aggregation and capability freshness remain integration work. Configured folder sharing is folder-level and local ignore files do not automatically synchronize. Applying a centrally authored per-file/device rule to an offline peer, and acknowledging its effective state, remain MyBrain integration work. Normal fully synchronized peer folders do not establish an on-demand placeholder contract.

Syncthing speaks its peer protocol, not OpenCloud WebDAV. A NAS peer can preserve an ordinary folder, but writing directly into OpenCloud's managed internals is not an acceptable compatibility shortcut. Retaining OpenCloud presentation/storage would require a separately proved supported bridge, or the owner must explicitly select a changed topology. Mobile continuity needs its own maintained-client investigation later; it does not block a first Windows-only proof.

## rclone and Rclone UI: strongest additional Windows UI reuse while investigating OpenCloud retention

Rclone supports explicit transfer operations and [per-call filters](<https://github.com/rclone/rclone/blob/v1.75.2/docs/content/rc.md>), with [ordered positive/negative rules](<https://github.com/rclone/rclone/blob/v1.75.2/docs/content/filtering.md>). An owner-controlled executor can wait before starting a permitted transfer instead of reacting after another client starts. That is a candidate architectural advantage, not tested proof; unknown-file discovery, file stability, retries and all competing paths still matter.

There is a concrete OpenCloud compatibility caveat. The old OpenCloud 4.0 migration guide shows vendor=opencloud, but inspected [rclone v1.75.2 WebDAV vendor handling](<https://github.com/rclone/rclone/blob/v1.75.2/backend/webdav/webdav.go>) has no corresponding specialized vendor case. Generic WebDAV or Infinite Scale behavior may be testable, but the correct URL/Space/authentication, timestamps/checksums and transfer-version semantics cannot be assumed. The earlier historical documentation is not proof of drop-in interoperability.

[Rclone's bundled GUI](<https://github.com/rclone/rclone/blob/v1.75.2/docs/content/gui.md>) is a browser-based Beta frontend, not the required native wizard. **Rclone UI is a distinct existing native application**: its [Tauri configuration](<https://github.com/rclone/rclone-ui/blob/453cc0c7dbc8cf355058ce92cc577b8002f97985/src-tauri/tauri.conf.json>) defines Windows packaging/update identity, and [operation previews](<https://github.com/rclone/rclone-ui/blob/453cc0c7dbc8cf355058ce92cc577b8002f97985/src/components/operation/useOperationDryRun.ts>) expose a useful existing interaction pattern. Its [scheduler](<https://github.com/rclone/rclone-ui/blob/453cc0c7dbc8cf355058ce92cc577b8002f97985/src-tauri/src/scheduler/runner.rs>) runs stored operations through a private authenticated local rclone process. This is a material candidate for adapting an existing Windows UI rather than building every screen from scratch.

Rclone UI has Apache-2.0 source, while its [license-validation code](<https://github.com/rclone/rclone-ui/blob/453cc0c7dbc8cf355058ce92cc577b8002f97985/lib/license.ts>) contacts a vendor service and [Copy scheduling](<https://github.com/rclone/rclone-ui/blob/453cc0c7dbc8cf355058ce92cc577b8002f97985/src/pages/Copy.tsx#L126>) gates some multi-source behavior on license state. That is not a claim that the source is closed or all operations need payment; the selected prebuilt or own-build path must establish the actually required features and offline dependencies. A modified UI cannot rely on official UI updates preserving unaccepted changes.

The engine's [copy operation](<https://github.com/rclone/rclone/blob/v1.75.2/docs/content/commands/rclone_copy.md>) does not delete destination files and is suitable to investigate a small one-way admission proof. It is not complete bidirectional synchronization. [Bisync](<https://github.com/rclone/rclone/blob/v1.75.2/docs/content/bisync.md>) requires resynchronization after relevant filter-file changes, with copy/delete/rename implications; dynamically refining rules must not silently trigger destructive or unexpected merge behavior. Raw RC has broad local authority and is not the cloud/browser-facing rule API.

## Small additional screening and continuity

| Candidate | Relevant existing behavior | Why it does not advance ahead of the main trials |
| --- | --- | --- |
| FreeFileSync / RealTimeSync | Native comparison/review/sync and reusable filters are useful wizard UX prior art. | Current [official licensing FAQ](https://freefilesync.org/faq.php) distinguishes personal/Donation use and a business edition; an unrestricted required Windows distribution chain was not established. The inspected [connection guide](https://freefilesync.org/manual.php?topic=ftp-setup) does not establish an OpenCloud WebDAV path. Do not infer that every historical source edition is closed, or that every present installer is an unrestricted open-source fit. |
| Unison | Open-source pairwise synchronization and a review-before-propagation model. | [v2.54.0 release notes](https://github.com/bcpierce00/unison/releases/tag/v2.54.0) qualify GTK GUI continuity. No complete owner-device catalogue, OpenCloud path or integrated MyBrain wizard was established; pairwise synchronization alone does not close those gaps. |
| ownCloud desktop family | Related native sync architecture and reusable ordinary-file experience. | The prior OpenCloud comparison already identifies the family-level internal/ignore/provider problem. No materially better independent wizard contract was established in this bounded screen; a separate full survey is not justified before the leading proofs. |

Future Android/iOS continuity should be costed after the Windows route is better known. Official versus community app maintenance, signed distribution and supported file-provider/background paths require explicit per-platform checks. A Windows engine/API advantage does not establish mobile parity.

## Conditional recommendation and first comparison

No backend, client fork or rule contract is selected. The conditional order for small proofs is:

| Owner boundary | Most useful first challenger | What must be proved before preferring it |
| --- | --- | --- |
| Retain OpenCloud storage; adapt or create a Windows native UI if needed. | Rclone UI plus a controlled rclone/OpenCloud protocol path, compared with the OpenCloud native integration baseline. | Actual protocol compatibility, unknown-content hold, grouped integrated decision and reusable filters with retained copies. Own UI work and per-device catalogue must remain visible costs. |
| Allow a changed synchronization topology to obtain stronger external control and device reuse. | Syncthing engine behind a native Windows wizard. | Pre-established deny rules, independent candidate discovery, per-device application/acknowledgement, safe rule changes and retained-copy behavior. OpenCloud coexistence needs a supported explicit boundary. |
| Keep the official native client's ordinary update experience and existing workflow. | Continue the OpenCloud supported-seam/upstream-contract proof. | An actually supported UI/admission boundary or an accepted maintained native delta. Nextcloud has not demonstrated a complete smaller gap; Seafile adds a separate backend without proving its per-file hold. |

Seafile is a secondary engine/UI comparison if library-based workflow and server replacement are acceptable. Nextcloud remains a credible file platform, but its broader app ecosystem does not supply an issue-9-specific reason to migrate. This recommendation ranks the next evidence to collect, not product completeness, performance or long-term total cost.

## Common falsification criteria

All proposed runs use synthetic directories and isolated processes/accounts. No experiment has run in this checkpoint.

| Proof | Common oracle |
| --- | --- |
| Unknown file inside an already governed ordinary directory | Install the declared default policy before starting the engine; create files, nested directories and edits while undecided. Observe initial and retried requests, not just final server contents. Zero content leaves before an applicable decision if that guarantee is claimed. |
| Integrated native set decision | One wizard and confirmation include storage, device availability, MyBrain yes/no and reusable scope, with an impact preview. A generic copy dialog or later separate MyBrain prompt does not pass. |
| Incremental rules | Admit a class, add later matching and non-matching files, change exclusions and reconnect. Verify engine-specific filter, rescan and bidirectional semantics without unintended deletion or replay. |
| Device truth | List registered offline/new/retired devices and distinguish accepted intent from each device's actual applied rule and available copy. Folder membership or a saved configuration response alone is insufficient. |
| Large excluded subtree | Group observations without transferring excluded contents or permanently registering every cache in MyBrain. Engine-skipped paths must not disappear from an alleged complete candidate inventory. |
| OpenCloud interoperability | Where claimed, verify actual supported API/protocol, Space/URL mapping, credentials, retained versions and failure handling. Never bypass the application by writing managed internal storage. |
| Independent updates | Use actual admitted engine/UI versions and the intended update path; preserve pending decisions/rules and repeat the admission/device probes. Replacing a modified official UI binary cannot be assumed safe. |

P18/P19/P38 remain authoritative: scope is not value, narrowing is not destruction, and any registered source retains its lifecycle. Operational observation-to-registration boundaries and candidate disclosure remain explicit open questions. The owner-approved Windows priority and integrated wizard are established; compatibility/topology, offline policy and required feature-chain decisions remain open before Design.

## Related Documents

- [Canonical issue-9 research](<research.md>)
- [Native wizard and update assessment](<native-wizard-update-feasibility.md>)
- [Earlier broad platform research, reviewed unchanged](<../issue6/open-source-platform-candidates.md>)
- [Issue 9](<https://github.com/MikeyVK/MyBrain/issues/9>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-05 | Codex (@imp researcher) | Compare Windows-first native applications and externally controlled engines against the integrated issue-9 wizard and update requirements. |
