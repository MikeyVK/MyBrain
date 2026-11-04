<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Local–cloud companion and incremental synchronization rules

**Status:** RESEARCH CHECKPOINT — strategy and runtime proofs pending  
**Version:** 1.0  
**Last Updated:** 2026-11-04

## Purpose

Investigate a practical local/cloud route that helps the owner establish synchronization and MyBrain intake rules incrementally while using the system.

## Scope In

Evidence-led interaction and responsibility boundaries; browser/OpenCloud reuse; local discovery and enforcement gaps; operational candidate metadata; offline rule propagation; options and a minimal synthetic experiment proposal.

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

### Research boundary and current evidence

The owner requested incremental help in establishing synchronization rules during ordinary use. This checkpoint starts with the local/cloud interaction and companion experience, ahead of the previously listed desktop upload experiment. "On the go" is treated as iterative rule building; using a phone or another device is an additional research scenario, not a newly imposed mobile requirement.

The preserved [2026-10-29 assessment](opencloud-admission-extension-feasibility.md) remains the historical source baseline, including its release pins and native-client limitations. This checkpoint does not reclassify source inspection as runtime evidence. Actual installed server, Web, desktop and SDK versions have not been inspected. No companion, queue, rule backend, native hold mechanism or MyBrain registration service has been implemented in this work.

### What the companion must help distinguish

The first three owner choices describe distribution; MyBrain registration is a separate choice. They are not a four-step promotion ladder.

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
| Incremental rule interface | OpenCloud Web apps can supply routed views, navigation and focused UI extensions. Version-7.2 documentation identifies shared host dependencies and a version-sensitive app skeleton. [Web guide](https://docs.opencloud.eu/de/docs/dev/web/extension-system/getting-started/), [extension overview](https://docs.opencloud.eu/de/docs/next/dev/web/extension-system/). | A separately packaged companion UI is a credible reuse route. Static frontend loading does not provide a durable candidate/rule/device-status backend. A minimal MyBrain-owned backend module is a candidate, not a selected extra standalone product. |
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
2. Local observations make a grouped candidate worklist available. The companion shows what it knows and when it last heard from the workstation. It need not upload file contents to ask whether an unfamiliar subtree should synchronize.
3. While working, the owner chooses a candidate group and drafts a reusable rule: for example keep generated caches local, allow selected project documents on the server, and decide MyBrain registration separately. The UI previews the currently known matching scope, exclusions and conflicts before acceptance.
4. The same UI could be opened elsewhere. If the workstation is offline, a rule can be saved as a desired change, while local receipt and application remain visibly pending. New unobserved files or an exact current match count must not be invented from old inventory.
5. The workstation receives the applicable rule revision, re-evaluates its current local state and reports the result. Receipt, successful evaluation and an observed transfer are different evidence.
6. Where a transfer boundary has actually been proved, the executor performs the permitted action. A changed file, overlapping rule or invalid decision returns to a visible unresolved state rather than silently inheriting a stale individual approval.
7. Subsequent observations can match the reusable rule without repeated per-file review. New exceptions remain visible. Changing a rule must not imply deletion of already retained local or server copies.

This journey is a proposal for evaluation. It does not select a rule language, pattern syntax, precedence rule, database, message broker, device protocol, content-hash algorithm or cryptographic approval mechanism. Content-based classification or an LLM may later propose a rule only through separately admitted processing; candidate discovery must not quietly send excluded content to previews, logs or an analysis service.

### Rule usefulness and operational truth

A companion is useful only if the owner can understand both a rule's intended reach and its actual effect. Research must test local feedback during rule construction, coarse folder decisions, reusable classes, exceptions and a preview against the presently observed inventory. The companion should help explain why an existing or draft rule matches or does not match, and distinguish a proposed draft from accepted and locally effective revisions. A preview can be stale; an apparently matching filename is not a durable identity.

Investigate distinct evidence for a saved intention, the targeted devices, each device's received revision, local evaluation and the observed synchronization result. These are research distinctions, not final DTO fields or a prescribed state machine. A remote rule edit cannot instantly alter a disconnected workstation. The treatment of previously accepted rules while disconnected, expired decisions and conflicting edits requires an explicit owner policy before implementation. Unknown content must not gain new transfer permission solely because policy is unavailable.

Candidate names, relative paths and grouping metadata can themselves expose private information. The minimum centrally visible information, optional redaction and retention need a deliberate decision. "Metadata only" must not be equated with harmless or public. Synthetic experiments must inspect request bodies, logs and previews as well as final storage.

### Options and update consequences

| Route | Useful reuse | Strict connected-folder admission and central distribution | Cost and compatibility question |
| --- | --- | --- | --- |
| Stock sync plus a companion dashboard | Existing storage, sync setup and Web app integration; incremental advice and owner-visible choices. | A dashboard does not establish enforcement before the native client's first content byte. Central per-device policy remains unproved. | Smallest apparent integration surface, but cannot be represented as satisfying the complete requirement without a demonstrated seam. |
| Owned local observation/transfer adapter plus companion | Reuse OpenCloud storage/protocols and possibly an existing transfer executor; own the rule roundtrip. | Can aim to gate paths it owns. Running stock sync over the same area introduces an independent upload route. Moving candidates outside all sync roots changes the required workflow and needs the owner's decision. | Packaging, filesystem semantics, conflict/version handling and operational recovery need proof. No new universal sync engine is assumed necessary. |
| Supported upstream hold contract or maintained client integration plus companion | Keep ordinary client behavior where an actual candidate/hold/resume seam exists. | Best alignment to transparent connected folders if proved. Existing source evidence does not establish a delivered stable contract; each Web/mobile/native route still needs coverage. | Upstream acceptance is unknown. A version-bound integration needs an explicit maintenance and regression commitment. |
| Browser-only companion with deliberate folder sessions | Small deliberate interactions in supported browsers. | Does not demonstrate unattended cross-device discovery or enforcement after the browser session ends. | Useful bounded route, with browser/permission/lifetime constraints; any relaxed workflow must be explicit. |

No route is selected. Building the companion interface and closing the native synchronization gap are related but independently falsifiable questions. A successful local/cloud rule roundtrip cannot be used as proof that an unchanged OpenCloud desktop client obeys it.

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

- Which native/client integration route can satisfy the unchanged connected-folder hold with acceptable maintenance, or would the owner explicitly accept a changed workflow?
- What may an offline device continue under a previously accepted rule, and when does a changed rule become effective for that device?
- Which candidate facts may leave the device before content admission, including paths, counts, grouping and optional previews?
- Does a companion belong inside OpenCloud Web or a separate MyBrain view, given host-version coupling and the still-unimplemented shared backend?

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

The owner approved the investigation direction: first study local/cloud interaction and a companion that helps construct rules. No native integration, replacement workflow, transport, rule contract or candidate-storage architecture is approved. Compatibility and policy decisions remain pending; stay in Research and do not start Design.

## Expected Results

This document is an initial evidence and experiment proposal only. Research remains open. The smallest proposed test separates the rule roundtrip from the native enforcement proof; neither has run.

### Proposed decisive experiment

Use an isolated synthetic selected directory and a disposable test server, plus a controlled browser session. Before execution, record actual OS, OpenCloud server/Web/desktop, SDK and any executor versions; the exact claimed seam; fixtures; network/request observation points; an unmodified control run; and retention-safe cleanup. A mock executor may establish orchestration only and must be labelled as such.

| Probe | Controlled variation | Pass, fail or insufficient-evidence boundary |
| --- | --- | --- |
| Candidate roundtrip | Create a synthetic document, a source file and a cache subtree; send only admitted candidate facts to the companion. | UI represents the grouped observations and their freshness. Content or excluded paths appearing in requests/previews/logs fails the declared metadata boundary. Missing observation coverage is insufficient evidence. |
| Incremental rule construction | Preview and accept one reusable rule plus a cache exception; add a second matching file. | Known matches/exceptions and unresolved overlaps are understandable; the second file is evaluated without fabricated per-file owner approval. This alone does not prove transfer enforcement. |
| Device receipt and effect | Save a rule, deliver it, then independently observe local evaluation and the executor result. | Saved, received, evaluated and observed effect remain distinguishable. A successful HTTP response without local evidence is insufficient. |
| Offline and unavailable service | Disconnect the workstation or rule service, create candidates, change a rule centrally, restart, then reconnect. | Pending/stale status is truthful; queued work survives according to the declared trial contract; no unknown content acquires new permission. Continued use of prior accepted rules must follow the owner-approved offline policy. |
| Stale/conflicting decisions | Deliver older revisions after newer ones; edit or replace content between an individual approval and transfer; overlap two rules. | Stale individual approval does not float to changed content. Undecided precedence is reported rather than invented. No universal hash/token implementation is assumed. |
| Native transfer gate | With the claimed ordinary connected-folder integration, create/edit while approval is pending or service unavailable; include initial TUS bodies. Compare with stock-client control. | Zero content bytes leave before approval if that guarantee is claimed. Reactive ignore, server rejection or quarantine cannot pass this oracle. An unobserved upload route is insufficient evidence. |
| Distribution follow-up | Only after the required seams are proved, use a second, new and reconnected test client for origin-only versus all-client eligibility. | Observe item visibility, bytes and offline retention separately; no unintended deletion of retained copies. Central enforcement cannot be inferred from manual client setup. |

Only local/browser/cloud orchestration need be in the first minimal roundtrip. Shared Web Uppy, full native bypass inventory, platform breadth and update compatibility retain the separate obligations in the historical assessment and issue #9. A phone is optional for this first proof; another browser session is enough to test the investigated remote-control distinction. Do not point a trial at production sync roots, accounts or the live NAS.

### Decisions needed before Design

The owner must choose the admissible native/client compatibility route or explicitly accept a workflow change, decide offline use of prior rules and their effective boundary, and approve the centrally visible candidate information. Test results may narrow these choices. An experiment protocol and a working UI would not close Research without those strategy decisions and independent phase review.

## Assumptions

- The companion serves the exclusive owner; no third-party per-entity rights model is introduced.
- Actual installed product versions and the usable local transfer seam remain unknown.
- A local component and outbound channel are research candidates, not a mandate to install services or open network ports.

## Related Documents

- [Preserved OpenCloud extension assessment](<opencloud-admission-extension-feasibility.md>)
- [Foundational principles](<../../architecture/decisions/0001-digital-brain-foundational-principles.md>)
- [Storage-foundation design](<../issue6/design.md>)
- [Issue 9 acceptance scope](<https://github.com/MikeyVK/MyBrain/issues/9>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-04 | Codex (@imp researcher) | Initialize issue-9 Research entrypoint and investigate local/cloud companion responsibilities, reuse options and bounded unexecuted proof obligations. |
