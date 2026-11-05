<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Integrated native wizard and local–cloud rule coordination

**Status:** RESEARCH CHECKPOINT — strategy and runtime proofs pending  
**Version:** 1.3  
**Last Updated:** 2026-11-05

## Purpose

Investigate an integrated native-app wizard and a practical local/cloud route that help the owner establish synchronization and MyBrain intake rules together, with Windows first and an existing-application comparison before Design.

## Scope In

Evidence-led interaction and responsibility boundaries; browser/OpenCloud reuse; local discovery and enforcement gaps; operational candidate metadata; local and shared policy, offline authorship and reconciliation; options and a minimal synthetic experiment proposal.

## Scope Out

No architecture selection, Design, implementation plan, code, deployment, live account or NAS access, package installation, client configuration change, production experiment or phase transition.

## Problem Statement

OpenCloud provides file storage and synchronization, but the owner needs assistance turning unfamiliar local content into deliberate, reusable synchronization and intake rules. The first question is how local observations, a companion interface and effective device actions can form an understandable feedback loop while preserving the exact connected-folder admission requirement. Existing source research alone does not establish that loop or a native upload hold.

## Goals

- Preserve the historical extension assessment and provide issue 9 with a canonical Research entrypoint.
- Investigate incremental rule building and the local/cloud responsibilities without silently selecting a new workflow or transfer architecture.
- Identify reusable supported surfaces, decisive gaps, strategy choices and small tests with explicit evidence limits.

## Background

On 2026-11-04 the owner prioritized research into a local/cloud route and a companion for rule construction. Coordination initialized the standalone feature issue with parent main and Research active. The already consolidated assessment remains unchanged. This document records the new investigation order, not completed tests or an approved implementation strategy.

## Findings

### Accepted integrated native wizard

On 2026-11-05 the owner accepted a wizard presented by the desktop or mobile app before unknown new file content reaches the server. One flow, summary and confirmation cover where files are kept, selected devices and supported on-demand/offline use, whether MyBrain registers them, and the rule's present/future scope. The MyBrain choice is independently selectable inside the same wizard and reusable rule; it must not become an unrelated later prompt. The app needs the owner's registered-device view, including offline devices and their capabilities. One confirmation records a coherent intention; asynchronous device actions and MyBrain processing retain separate truthful status.

The [native integration and update assessment](native-wizard-update-feasibility.md) records the accepted experience, pinned desktop/Android/iOS source evidence, device-inventory gap, maintenance options and unexecuted probes. A separate Web dashboard remains useful supporting interaction or shared-content reuse, but alone no longer represents the requested native presentation host. No client integration, fork or update strategy has been selected.

### Windows-first application comparison

The owner next prioritized realizing the wizard and rules on Windows and asked whether existing applications fit issue 9 better before starting Design. The [Windows synchronization candidate comparison](windows-sync-candidate-comparison.md) reuses the earlier platform shortlist only within this issue's synchronization/admission scope. It compares the OpenCloud baseline, Nextcloud, Seafile Community, Syncthing and rclone, including the distinct native Rclone UI application. The MyBrain knowledge, wiki, AI and accounting layers are excluded. Seafile's earlier AI/metadata dependency finding does not disqualify its separate Community sync path.

No ready application was established to implement the complete integrated wizard. Conditional first challengers are externally controlled Syncthing for device/configuration reuse if a topology change is acceptable, or Rclone UI plus a controlled rclone protocol route if OpenCloud retention is important. These reduce different parts of the custom work; neither has passed the admission, device or upgrade proof. Nextcloud/Seafile remain useful comparisons without a demonstrated smaller complete gap. No backend, engine or client strategy is selected. A first Windows-only proof can precede mobile implementation, whose continuity costs remain visible.

### Local rule authorship, intended reach and shared application

On 2026-11-05 the owner accepted a further behavioral distinction: a synchronization rule can be created, confirmed and durably saved on a device without an active server connection. Where the rule originates and is stored does not determine its intended reach. A rule authored offline may be local-only or intended for selected other devices or a device group, where that group mechanism is supported. This requirement selects neither a central policy master nor a merge engine.

| Distinction | Required meaning |
| --- | --- |
| Origin and local durable storage | Identify where a rule was authored and preserve the confirmed combined choice locally, including after restart. Offline authorship is possible using locally available knowledge. |
| Intended reach | Distinguish local-only policy from a choice intended for selected devices or a supported group. Neither a server copy of a rule nor its originating device automatically determines that reach. New devices are not silently selected or enrolled. |
| Actual application | Distinguish locally saved/accepted intent, locally effective behavior, sharing, receipt and evaluation on each intended device, and actual content transfer or MyBrain registration. These are evidence distinctions, not a prescribed state schema. |

The same native wizard must allow rules for files, folders, file types and other supported scopes using last-known clients, server folders and policy. Its one summary and confirmation retain storage, device availability, MyBrain admission and reusable scope together. The interface must disclose stale inventory and uncertain capabilities; it may not invent unseen files, current counts, device receipt or completed registration. Local-only intended application must not silently become shared application merely because its rule record is reconciled or stored on the server. Policy-record disclosure/distribution is a separate choice: an explicitly permitted server backup or shared representation can still describe origin-only application. Reconciliation must not force sharing of a deliberately private local rule. The allowed record-distribution policy remains open; no default is selected.

Locally executable effects may apply while disconnected within the explicitly accepted offline policy. Full server transfer, policy distribution and remote application require the relevant connection. Saving or accepting a rule is therefore not proof that all its effects have occurred. The treatment of prior accepted rules while offline remains a policy decision; unknown, unavailable or conflicted policy must not itself grant new transfer permission.

Reconciliation is required both on reconnect and when relevant local or server-registered policy changes during connected work. Compare changes against the last reconciled state, preserve local and server changes, distinguish compatible changes from unresolved overlaps, and report which decisions/effects remain pending. Do not silently choose latest-timestamp-wins, server-wins or local-wins, or treat every overlap as already resolved. The precedence and compatibility rules remain to be established explicitly. Queued work must be re-evaluated against the applicable reconciled policy before a later transfer; an obsolete or unresolved rule must not provide a bypass. Changes of rule scope, delivery retries and policy reconciliation do not authorize deletion of retained content.

The [offline and reconciliation probe contract](#offline-and-reconciliation-probe-contract) makes these behavioral requirements falsifiable. It is an unexecuted Research protocol, not a Design contract, API or selected merge algorithm.

### Existing OpenCloud settings and the shared-policy gap

The following additional primary sources were inspected on 2026-11-05. Desktop v4.0.0 and server v9.0.0 are separate source snapshots, not a claim about installed versions or a tested version pair.

| Inspected surface | Observed behavior and bounded conclusion |
| --- | --- |
| Desktop settings | [ConfigFile::getValue](<https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/libsync/configfile.cpp>) first reads local settings and falls back to GlobalConfig; [GlobalConfig](<https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/libsync/globalconfig.cpp>) can read system settings and Windows policy registry paths. The inspected ConfigFile::skipUpdateCheck call uses the Windows policy mechanism for update checks. This is not evidence that arbitrary synchronization/device-group policy is inherited from the server. |
| Local excludes | [IgnoreListEditor::slotUpdateLocalIgnoreList](<https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/gui/ignorelisteditor.cpp>) writes the user-scope excludes file, reloads excludes and schedules discovery/synchronization for ready folders. A local excludes file may be an execution projection; saving it or scheduling work does not establish per-device distribution, reconciliation or a before-content hold. |
| Server policies | The [policies service](<https://github.com/opencloud-eu/opencloud/blob/v9.0.0/services/policies/README.md>) describes proxy, event and gRPC authorization checks. Server request authorization is distinct from clients receiving and applying the owner's synchronization and availability rules. |
| Server settings | The [settings service](<https://github.com/opencloud-eu/opencloud/blob/v9.0.0/services/settings/README.md>) persists registered setting values and describes profile settings, roles and assignments. Its extensibility is not a delivered synchronization-device policy controller or group-inheritance contract. |

No complete device-group synchronization inheritance, offline policy exchange and effective-application contract was established in these inspected surfaces. This bounded finding does not prove that extension is impossible. It does mean that a local exclude experiment alone cannot establish the required shared-policy behavior.

### Research boundary and current evidence

The owner requested incremental help in establishing synchronization rules during ordinary use. This checkpoint starts with the local/cloud interaction and companion experience, ahead of the previously listed desktop upload experiment. "On the go" includes iterative rule building and the subsequently accepted offline authorship/reconciliation requirements; using a phone or another device is an additional research scenario, not a newly imposed mobile requirement.

The preserved [2026-10-29 assessment](opencloud-admission-extension-feasibility.md) remains the historical source baseline, including its release pins and native-client limitations. This checkpoint does not reclassify source inspection as runtime evidence. Actual installed server, Web, desktop and SDK versions have not been inspected. No companion, queue, rule backend, native hold mechanism or MyBrain registration service has been implemented in this work.

### What the companion must help distinguish

The first three owner choices describe distribution; MyBrain registration is an independent dimension in the same integrated wizard, summary and confirmation. They are not a four-step promotion ladder or separate-time workflows.

| Choice | Meaning under investigation | Required distinction |
| --- | --- | --- |
| Local only | Retain content on its originating workstation. | A centrally visible candidate must not imply content upload. |
| Server and originating machine | Retain a server copy and synchronize automatically on that originating device. | Existing local folder selection does not prove central enforcement on other devices. |
| Eligible for other connected devices | Permit distribution under accepted rules and explicit device selection. | Eligibility, placeholder visibility, content download and offline retention differ. |
| MyBrain registration | Admit a source/version under the intake and lifecycle contracts. | A server file, discovery record or accepted synchronization rule is not itself a completed source registration. |

The [foundational principles](../../architecture/decisions/0001-digital-brain-foundational-principles.md) remain authoritative: P18 separates observation, receipt and successful capture; P19 separates intake scope from value and gives scope narrowing no destructive effect; P38 keeps a registered intake candidate and its lifecycle on the same source registration. Any pre-admission local observation/worklist is a research proposal whose lifetime and exact observation-to-registration boundary remain open. Do not infer either that every discovered file is already registered or that every candidate belongs in a new non-source registry. This research neither makes excluded caches permanent MyBrain sources nor selects a second source authority or replacement lifecycle.

### Evidence-supported separation of responsibilities

| Concern | Existing evidence | Research inference or gap |
| --- | --- | --- |
| Incremental rule interface | OpenCloud Web apps can supply routed views, navigation and focused UI extensions. Version-7.2 documentation identifies shared host dependencies and a version-sensitive app skeleton. [Web guide](https://docs.opencloud.eu/de/docs/dev/web/extension-system/getting-started/), [extension overview](https://docs.opencloud.eu/de/docs/next/dev/web/extension-system/). | A Web app can support the companion or shared interaction content, but the accepted wizard must be offered by the native client. Static frontend loading supplies neither a native upload hold nor a durable candidate/rule/device-status backend. A minimal MyBrain-owned backend module is a candidate, not a selected extra standalone product. |
| Local discovery | A supported browser session can request a user-selected directory; availability and user-activation restrictions vary. [Directory picker](https://developer.mozilla.org/en-US/docs/Web/API/Window/showDirectoryPicker). | Browser-only interaction can help deliberate local selection. It does not establish durable discovery after the browser closes or supervision of unmodified native clients. A local process is the candidate boundary for autonomous workstation observation. |
| Browser lifetime | The Service Worker draft binds execution to events and permits idle termination. [Lifetime](https://w3c.github.io/ServiceWorker/#service-worker-lifetime). | An installed PWA alone is not proof of a continuously running filesystem observer. A browser on another device observes that device's permitted files, not an offline workstation's disk. |
| Local/cloud communication | WebSocket starts with a client handshake and supports two-way messages. [RFC 6455, section 1.3](https://www.rfc-editor.org/rfc/rfc6455.html#section-1.3). | Device-initiated authenticated HTTPS requests or a secure persistent channel can be investigated without an inbound workstation listener. Neither option supplies durable decisions, application acknowledgements or conflict semantics by itself. No networking deployment or circumvention is proposed. |
| Before-content admission | The historical assessment found no documented independent approve/defer contract for the inspected stock native clients; the initial TUS request can already carry content. | A watcher next to an unmodified sync client is not a proved hold. The actual transfer owner or a demonstrated native seam must enforce the decision. A Web screen or server quarantine cannot prove that boundary. Pre-established default-deny exclusion rules differ from reactive exclusions; whether stock ignore semantics can form a safe positive allowlist across traversal, reloads and edits remains unproved and should be tested rather than ruled out. |
| Existing transport reuse | OpenCloud's historical 4.0 migration guide uses rclone with WebDAV; rclone documents per-call filters and remote-control operations. [Migration](https://docs.opencloud.eu/docs/4.0/admin/maintenance/migrate/), [rclone RC](https://rclone.org/rc/). | A constrained local transfer adapter could reuse an executor rather than reimplement transport. This does not establish bidirectional sync semantics, a stock-client hold or per-device distribution. Raw RC exposes broad filesystem power and must not be treated as the cloud/browser-facing companion API. |
| Credentials | OpenCloud 7.2 documents expiring, revocable App Tokens but explicitly says they reach all user data. [App Tokens](https://docs.opencloud.eu/docs/user/admin/app-tokens/). | They are not evidence of folder-limited device credentials. Owner identity, device enrollment, token custody and backend authorization remain separate future contract decisions. |

Primary pages above were inspected on 2026-11-04. The Web guide labels itself 7.2, the overview is rolling, the migration example is 4.0, and the Service Worker source is an Editor's Draft dated 2026-10-29. These are bounded documentation observations, not installed-version or compatibility claims. Existing source-pinned Uppy evidence remains in the historical assessment; shared Web upload interception still needs its own experiment.

### Concrete incremental journey to investigate

All names and content in this example are synthetic.

1. The owner selects a permitted local work area containing a document, source files and a generated cache subtree. Enrollment must establish how this area is governed; discovery must not be mistaken for an already-proved upload hold inside an ordinary connected folder.
2. Local observations make a grouped candidate worklist available. The native wizard and supporting companion show what they know and when they last heard from each device. It need not upload file contents to ask whether an unfamiliar subtree should synchronize.
3. While working, the owner chooses a candidate group and drafts a reusable rule: for example keep generated caches local, allow selected project documents on the server, and choose MyBrain registration within the same wizard. The UI previews currently known matching scope, devices, availability, registration and conflicts, then presents one combined summary and confirmation.
4. The device can create, confirm and save that complete combined rule while offline using last-known devices, server folders and policy. Its origin and intended reach remain separate: it can be intended only here or for selected other devices. Locally executable effects may apply under the accepted offline policy; unavailable server transfer, distribution and remote application remain pending. Stale inventory must be visible without invented files or current match counts.
5. On reconnect, or a relevant policy change while connected, compare local and server changes against the last reconciled state. Preserve both sides' changes, recognize compatible changes and expose unresolved overlaps without an invented winner. Re-evaluate current local content and queued work before any newly permitted transfer. Receipt, successful evaluation and an observed effect remain different evidence.
6. Where a transfer boundary has actually been proved, the executor performs the permitted action. A changed file, overlapping rule or invalid decision returns to a visible unresolved state rather than silently inheriting a stale individual approval.
7. Subsequent observations can match the reusable rule without repeated per-file review. New exceptions remain visible. Changing a rule must not imply deletion of already retained local or server copies.

This journey is a proposal for evaluation. It does not select a rule language, pattern syntax, precedence rule, database, message broker, device protocol, content-hash algorithm or cryptographic approval mechanism. Content-based classification or an LLM may later propose a rule only through separately admitted processing; candidate discovery must not quietly send excluded content to previews, logs or an analysis service.

### Rule usefulness and operational truth

A companion is useful only if the owner can understand both a rule's intended reach and its actual effect. Research must test local feedback during rule construction, coarse folder decisions, reusable classes, exceptions and a preview against the presently observed inventory. The companion should help explain why an existing or draft rule matches or does not match, and distinguish a proposed draft from accepted and locally effective revisions. A preview can be stale; an apparently matching filename is not a durable identity.

The [local/shared policy distinction](#local-rule-authorship-intended-reach-and-shared-application) governs evidence for saved/accepted intention, intended devices, receipt, evaluation, local effectiveness, synchronization and MyBrain registration. A remote edit cannot instantly alter a disconnected workstation. Previously accepted offline rules, expiration, precedence and conflicting changes still require explicit policy before implementation. Unknown, unavailable or conflicted policy must not grant new transfer permission; a successful reconciliation response alone is not native enforcement evidence.

Candidate names, relative paths and grouping metadata can themselves expose private information. The minimum centrally visible information, optional redaction and retention need a deliberate decision. "Metadata only" must not be equated with harmless or public. Synthetic experiments must inspect request bodies, logs and previews as well as final storage.

### Options and update consequences

| Route | Useful reuse | Strict connected-folder admission and central distribution | Cost and compatibility question |
| --- | --- | --- | --- |
| Stock sync plus a companion dashboard | Existing storage, sync setup and Web app integration; incremental advice and owner-visible choices. | A dashboard does not establish enforcement before the native client's first content byte. Central per-device policy remains unproved. | Smallest apparent integration surface, but cannot be represented as satisfying the complete requirement without a demonstrated seam. |
| Owned local observation/transfer adapter plus companion | Reuse OpenCloud storage/protocols and possibly an existing transfer executor; own the rule roundtrip. | Can aim to gate paths it owns. Running stock sync over the same area introduces an independent upload route. Moving candidates outside all sync roots changes the required workflow and needs the owner's decision. | Packaging, filesystem semantics, conflict/version handling and operational recovery need proof. No new universal sync engine is assumed necessary. |
| Supported upstream hold contract or maintained client integration plus companion | Keep ordinary client behavior where an actual candidate/hold/resume seam exists. | Best alignment to transparent connected folders if proved. Existing source evidence does not establish a delivered stable contract; each Web/mobile/native route still needs coverage. | Upstream acceptance is unknown. A version-bound integration needs an explicit maintenance and regression commitment. |
| Browser-only companion with deliberate folder sessions | Small deliberate interactions in supported browsers. | Does not demonstrate unattended cross-device discovery or enforcement after the browser session ends. | Useful bounded route, with browser/permission/lifetime constraints; any relaxed workflow must be explicit. |

No integration route is selected. The accepted native wizard brings all choices together; implementing its presentation and proving native synchronization control are related but independently falsifiable questions. A successful local/cloud rule roundtrip cannot be used as proof that an unchanged OpenCloud desktop client obeys it.

### Blast radius and retained boundaries

| Surface | Impact of this checkpoint | Later affected boundary to investigate |
| --- | --- | --- |
| MyBrain source storage and lifecycle | Principles and issue-6 design unchanged; no runtime claimed. | Admission of operational candidates versus durable registration, receipt and version evidence. |
| OpenCloud storage and versions | No installation, upgrade, deletion rule or copy/archive mechanism changed. | Exact protocol/Space/version behavior of admitted transfers. |
| Client and Web integrations | No client modifications or executable extension added. | Discovery, decision enforcement, app/host versions, native bypasses and per-device distribution. |
| Rules and companion backend | Evidence/options only. | Policy ownership, persistence, revision application, conflict handling, local/cloud recovery and UI explanations. |
| Authentication/logging | No credentials accessed, no new service/connection activated. | Exclusive owner access, device credentials, metadata minimization and structured shared diagnostics. |
| Repository/docs/quality | One canonical Research entrypoint and index update; historical assessment retained. No app source, tests, templates or quality configuration changed. | Any later prototype needs a bounded assignment, selected versions and applicable application checks before execution. |

## Questions

- Which Windows-first candidate and integration boundary can satisfy the unchanged connected-folder hold with acceptable maintenance; must OpenCloud remain the storage/transport endpoint, or may a changed topology be compared?
- What may an offline device continue under a previously accepted rule; how are compatible changes, precedence, unresolved overlaps and effective application defined without silently discarding local or server changes?
- Which supported device/group scope, enrollment defaults and deletion semantics are acceptable? Device enrollment is not implied by creating or sharing a rule.
- Which candidate facts may leave the device before content admission, including paths, counts, grouping and optional previews?
- Which native integration and update-maintenance route can host the integrated wizard and control all claimed upload paths; which shared or supporting Web views are useful without replacing that native flow?

## References

- [OpenCloud Web app guide, documentation 7.2](<https://docs.opencloud.eu/de/docs/dev/web/extension-system/getting-started/>)
- [OpenCloud extension overview, rolling documentation](<https://docs.opencloud.eu/de/docs/next/dev/web/extension-system/>)
- [Browser selected-directory boundary](<https://developer.mozilla.org/en-US/docs/Web/API/Window/showDirectoryPicker>)
- [Service Worker lifetime, Editor's Draft](<https://w3c.github.io/ServiceWorker/#service-worker-lifetime>)
- [WebSocket handshake and two-way channel](<https://www.rfc-editor.org/rfc/rfc6455.html#section-1.3>)
- [Historical OpenCloud rclone migration example](<https://docs.opencloud.eu/docs/4.0/admin/maintenance/migrate/>)
- [rclone remote-control capabilities and limits](<https://rclone.org/rc/>)
- [OpenCloud App Token scope](<https://docs.opencloud.eu/docs/user/admin/app-tokens/>)

## Approved Strategy

The owner approved the investigation direction and, on 2026-11-05, the integrated native wizard experience: storage, device availability, MyBrain admission and reusable scope are selected in one flow and confirmation. The owner subsequently prioritized Windows and requested an existing-application comparison before Design. The owner also accepted offline local rule authorship, separation of origin/storage from intended reach and actual application, and reconciliation on reconnect or relevant local/server policy changes. Study the local/cloud interaction and native client integration/update routes; the comparison does not select an engine, replacement backend or broader MyBrain platform. No native integration, replacement workflow, transport, formal rule contract or candidate-storage architecture is approved. The accepted offline/shared-policy behavior does not select a central master, merge algorithm, precedence, deletion policy or device-enrollment default. Compatibility and policy decisions remain pending; stay in Research and do not start Design.

## Expected Results

This document is an evidence and experiment proposal only, extended by the Windows-first alternatives comparison. Research remains open. The smallest proposed test separates the rule roundtrip from the native enforcement proof; neither has run.

### Proposed decisive experiment

This section is the linkable behavioral probe contract for issue 9. Every probe below is **NOT RUN**; the offline/reconciliation cases are detailed in the dedicated subsection.

Use an isolated synthetic selected directory and a disposable test server, plus a controlled browser session. Before execution, record actual OS, OpenCloud server/Web/desktop, SDK and any executor versions; the exact claimed seam; fixtures; network/request observation points; an unmodified control run; and retention-safe cleanup. A mock executor may establish orchestration only and must be labelled as such.

| Probe | Controlled variation | Pass, fail or insufficient-evidence boundary |
| --- | --- | --- |
| Candidate roundtrip | Create a synthetic document, a source file and a cache subtree; send only admitted candidate facts to the companion. | UI represents the grouped observations and their freshness. Content or excluded paths appearing in requests/previews/logs fails the declared metadata boundary. Missing observation coverage is insufficient evidence. |
| Integrated wizard and incremental rules | In the native app preview and confirm storage, devices/availability, MyBrain choice and reusable scope together; add a second matching file and a cache exception. | One summary/confirmation records all choices; no separate later MyBrain prompt. Known matches/exceptions and unresolved overlaps are understandable; later matches need no fabricated per-file review. This alone does not prove transfer enforcement. |
| Device receipt and effect | Save a rule, deliver it, then independently observe local evaluation and the executor result. | Saved, received, evaluated and observed effect remain distinguishable. A successful HTTP response without local evidence is insufficient. |
| Offline authorship and policy reconciliation | Execute the [offline and reconciliation cases](#offline-and-reconciliation-probe-contract) with local-only and shared intentions, independently changed local/server rules, and connected policy updates. | Local durability, intended reach and actual application remain distinguishable. Both sides' changes are preserved; compatible changes and unresolved conflicts are visible. New permission arising solely from unknown/unavailable/conflicted policy, unintended deletion or a stale queued-transfer bypass fails. |
| Stale/conflicting decisions | Deliver older revisions after newer ones; edit or replace content between an individual approval and transfer; overlap two rules. | Stale individual approval does not float to changed content. Undecided precedence is reported rather than invented. No universal hash/token implementation is assumed. |
| Native transfer gate | With the claimed ordinary connected-folder integration, create/edit while approval is pending or service unavailable; include initial TUS bodies. Compare with stock-client control. | Zero content bytes leave before approval if that guarantee is claimed. Reactive ignore, server rejection or quarantine cannot pass this oracle. An unobserved upload route is insufficient evidence. |
| Distribution follow-up | Only after the required seams are proved, use a second, new and reconnected test client for origin-only versus all-client eligibility. | Observe item visibility, bytes and offline retention separately; no unintended deletion of retained copies. Central enforcement cannot be inferred from manual client setup. |

A first Windows-only proof can isolate the wizard, rule handling and local/client/cloud coordination before mobile implementation. A browser-only orchestration proof must be labelled partial and cannot substitute for the accepted native wizard. Shared Web Uppy, full native bypass inventory, platform breadth and update compatibility retain the separate obligations in the historical assessment and issue #9. A phone is optional for this first proof; another browser session is enough to test the investigated remote-control distinction. Do not point a trial at production sync roots, accounts or the live NAS.

### Offline and reconciliation probe contract

Use synthetic files, folders, file-type rules, retained copies and test devices only. Establish a known last-reconciled policy and record which inventories and capabilities are current or cached before each case. Fixtures must include changes that the declared trial policy treats as compatible, overlapping changes requiring resolution, and queued work awaiting a decision. If the necessary offline/precedence policy is not approved, report that part as insufficient evidence instead of inventing a result. **All cases are NOT RUN.**

| Case | Controlled variation | Required observable result or falsifier |
| --- | --- | --- |
| Complete rule authored offline | Disconnect before opening the native wizard; use last-known devices/server folders, confirm the full storage/device/availability/MyBrain/scope choice, then restart the app/device. | The same accepted intention survives locally, including MyBrain choice and intended reach. Staleness and unperformed remote effects stay visible. A server roundtrip required merely to save, lost choice, or falsely reported remote success fails. |
| Offline local-only intention | Create or edit a rule expressly limited to the originating device, then reconnect after a separate server rule changed. | Local intent and relevant server changes remain distinguishable and preserved. Reconciliation does not silently publish that local-only rule as shared intent or turn a remote change into proof of local application. |
| Offline shared intention | Offline, create/edit a rule intended for selected known devices or a supported group; keep one target offline through origin reconnect. | Offline creation does not restrict the intended reach to the origin. Sharing/receipt/evaluation and actual effects are separately observed; the offline target remains pending rather than falsely effective. |
| Compatible local and server changes | From the recorded baseline, change distinct scopes independently, then reconnect. | Both changes remain available and are evaluated for compatibility under the declared policy; no whole-side replacement silently loses either change. A compatible case is not reported completed without application evidence. |
| Overlapping local and server changes | Independently change the same effective scope in incompatible ways. | Preserve both changes and expose the unresolved overlap without implicit timestamp/server/local precedence. The unresolved state grants no new transfer permission or deletion authority. |
| Policy changes while connected | Change local policy, then server-registered policy while discovery or queued work is active. | Reconciliation also occurs without a disconnect event. Pending/effective status and actual execution reflect re-evaluation; an old decision may not silently authorize later queued transfer. |
| Duplicate and out-of-order delivery | Repeat a policy/change delivery and deliver an older one after a newer one. | Delivery does not duplicate rule effects, silently restore obsolete permission or discard an outstanding local/server change. Receipt alone is not evidence of application. |
| Disconnect/retry during reconciliation | Interrupt after local save, during exchange and before/after a reported application; restart and retry. | Durable intentions and unresolved changes remain visible without false completion or repeated unsafe effects. Retry does not bypass the required reconciliation/re-evaluation. |
| Stale device/folder inventory | Use cached entries for an offline/retired device, a changed server folder or an unknown capability. | The wizard permits a truthful draft/confirmed intention where possible, discloses uncertainty and does not invent unseen files, exact current counts or supported capabilities. Final application remains pending where it cannot be established. |
| Queued transfer under obsolete policy | Queue under an accepted rule, narrow/change it locally or on the server, or introduce an unresolved overlap before retry/reconnect. | Re-evaluate against the applicable reconciled policy before the later transfer. The queued approval is not a bypass; observe all claimed real request paths when asserting a before-content result. |
| New/offline device and intended group | Add a test device or reconnect an existing one after shared rules changed; test only explicitly declared enrollment/group semantics. | Recognizable inventory, intended membership, receipt and effective revision remain distinct. No automatic device selection/inheritance is inferred from product defaults; unsupported group behavior is reported. |
| Preservation across policy changes | Change distribution scope, exclude a previously included subtree, cancel the wizard, reconcile and retry. | Retained local/server copies are not deleted merely because policy changed or narrowed. Any separate deletion semantics remain unselected and require explicit authorization. |

These observations can establish rule orchestration and truthful user feedback only. To claim native before-first-byte enforcement, separately execute the native transfer-gate oracle against every claimed path, including initial request bodies, restart, retries and changes after approval. A mock executor, local exclude file, policy-exchange response or server rejection is insufficient evidence of that guarantee. One user confirmation still does not imply an instantaneous distributed transaction.

### Decisions needed before Design

The owner must choose the admissible native/client compatibility route or explicitly accept a workflow change, decide offline use of prior rules and their effective boundary, precedence/compatibility and conflict handling, supported device/group enrollment scope and separate deletion semantics, and approve the centrally visible candidate information. Test results may narrow these choices. An experiment protocol and a working UI would not close Research without those strategy decisions and independent phase review.

## Assumptions

- The companion serves the exclusive owner; no third-party per-entity rights model is introduced.
- Actual installed product versions and the usable local transfer seam remain unknown.
- A local component and outbound channel are research candidates, not a mandate to install services or open network ports.

## Related Documents

- [Windows synchronization candidate comparison](<windows-sync-candidate-comparison.md>)
- [Native wizard integration and update feasibility](<native-wizard-update-feasibility.md>)
- [Preserved OpenCloud extension assessment](<opencloud-admission-extension-feasibility.md>)
- [Foundational principles](<../../architecture/decisions/0001-digital-brain-foundational-principles.md>)
- [Storage-foundation design](<../issue6/design.md>)
- [Issue 9 acceptance scope](<https://github.com/MikeyVK/MyBrain/issues/9>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-04 | Codex (@imp researcher) | Initialize issue-9 Research entrypoint and investigate local/cloud companion responsibilities, reuse options and bounded unexecuted proof obligations. |
| 1.1 | 2026-11-05 | Codex (@imp researcher) | Record the accepted integrated native wizard with MyBrain choice in the same confirmation; link platform/update evidence and retain pending strategy/proof limits. |
| 1.2 | 2026-11-05 | Codex (@imp researcher) | Record Windows-first priority and link the issue-9-only application/engine comparison with conditional unexecuted trial recommendations. |
| 1.3 | 2026-11-05 | Codex (@imp researcher) | Distinguish offline local rule authorship, intended reach and actual application; add bounded OpenCloud policy evidence and an unexecuted reconciliation probe contract. |
