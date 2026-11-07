<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Synchronization policy decisions and behavioral probe contract

**Status:** RESEARCH CHECKPOINT — owner policy consolidated; integrated probes NOT RUN; technical strategy open  
**Version:** 1.0  
**Last Updated:** 2026-11-07

## Purpose

Consolidate the owner's accepted issue-9 policy and presentation choices, distinguish remaining usage decisions from technical unknowns, and define falsifiable behavioral probes before Design.

## Scope In

The integrated Windows-first native wizard, personal device/group policy, draft and activation behavior, offline reconciliation, all-action bulk safeguards, presentation and unexecuted proof obligations.

## Scope Out

No formal Design/API contract, selected implementation or compatibility route, application code, probe execution, production access, deployment, new storage decisions, or phase exit. Sharing with other users is a later direction only.

## Problem Statement

The required wizard now includes owner decisions that are more specific than the earlier research questions. Keeping those questions unchanged would reopen accepted choices or let an experiment silently invent the remaining policy.

## Goals

- Keep accepted choices auditable and separate from proposals, measured behavior and unresolved policy.
- Make the integrated behavior testable without assuming that manual stock-client settings prove external policy control.
- Identify only the remaining owner usage questions and the probes that depend on them.

## Background

This 2026-11-07 consolidation records the owner's policy discussion and request to update issue 9, the research and probe contract. The decisions below are user-experience requirements, not evidence that OpenCloud implements them. The canonical research entrypoint remains research.md. The source-pinned platform reports and completed stock CLI measurement keep their historical evidence status.

## Findings

### Authority and evidence boundaries

The owner accepted these choices in the discussion culminating in this consolidation. A later refinement supersedes an earlier suggestion where noted. This is the current behavioral baseline for all candidate implementations; it does not select a merge algorithm, rule language, client patch, protocol or screen layout.

| Evidence class | Current status |
| --- | --- |
| Owner decisions | The accepted behavior below constrains later probes and Design. |
| Source/release research | Pinned evidence remains in the [native assessment](native-wizard-update-feasibility.md) and [candidate comparison](windows-sync-candidate-comparison.md). No new platform verification is claimed here. |
| Executed component control | The [stock Windows CLI report](stock-windows-filter-probe.md) measured manually supplied filters and fresh batch starts only. |
| Integrated behavioral probes | All cases in this document are **NOT RUN**. An unmet policy prerequisite prevents a verdict for the affected case. |

### Accepted scope and integrated intention

| ID | Accepted behavior | Delimitation |
| --- | --- | --- |
| D01 | One personal owner uses one active operating/administration endpoint at a time; several devices may synchronize. | This does not impose one physical device or imply simultaneously effective policy everywhere. Offline devices still need later execution plans. |
| D02 | Unknown new content in an ordinary already-connected folder stays local until an applicable accepted rule or decision permits transfer. | A separate outside-sync-root workflow, after-upload rejection or server quarantine cannot substitute for that boundary. Previously accepted matching rules may handle later files automatically. |
| D03 | One native wizard, summary and confirmation combine local/cloud retention, device/group selection, supported availability, independently selectable MyBrain admission and present/future reusable scope. | MyBrain is not a detached later prompt. Visibility, download, offline retention, distribution eligibility and durable registration differ. Windows is first; mobile continuity remains in the research boundary. |
| D04 | Inventory includes all configured owner devices, including offline ones, with recognizable names, capabilities and truthful freshness. | Sessions/tokens/live connections alone are not a complete device inventory. Unknown/new devices are not silently selected or enrolled in a group. |
| D05 | Rule origin/local durable storage, intended execution reach, record disclosure/distribution, and observed application are separate. Rules may be authored, confirmed and saved offline using last-known knowledge. | An explicitly allowed server copy does not widen an origin-only rule's execution reach. A deliberately private local rule is not silently shared. Remote effects need connectivity. |
| D06 | Candidate discovery/worklists are operational observations; registration and lifecycle retain P18/P19/P38. Scope is not value and narrowing is not destruction. | Do not permanently register every cache or invent a second authoritative source registry. Cancel, wait, failed transfer, retry or narrower distribution do not authorize destruction of retained copies. |
| D07 | Sharing with other users is a later possible route, bounded to a Space/share and potentially presented in the same wizard. | It is outside current probe acceptance and does not introduce a whole-brain multi-user or per-entity-rights phase. |

### Draft, activation and already-running work

| ID | Accepted behavior | What remains distinct |
| --- | --- | --- |
| D08 | Normal strategy: edit/save a draft while the existing active policy remains valid; explicit Apply uses a controlled pause, activation/confirmation and resumption. | Opening the normal editor does not silently activate a draft or revoke the valid old policy. Saved draft, confirmed intent and per-device active behavior differ. |
| D09 | Explicit alternatives remain: pause before editing, or prepare the change for a later maintenance moment. Do not silently change strategy. | These are owner-selectable workflows, not an automatic fallback selected for the owner. |
| D10 | Prefer pausing only affected work; use a wider pause if necessary; automatic client restart is the last alternative. | This is an investigation preference, not proven support, a no-restart guarantee or an implementation choice. |
| D11 | At finalization, offer handling choices relevant to actual running work: finish current files; finish a clearly bounded already-planned round; or interrupt and re-evaluate outstanding work. | All three remain selectable. No universal default, fixed cutover deadline, immediate revocation from confirmation, or rollback of already-sent bytes was selected. If nothing relevant runs, do not force an irrelevant choice. |
| D12 | Finalization explicitly plans later execution/reconciliation on offline or unreachable devices. | One accepted decision is not an instantaneous distributed transaction. Show each device's pending/received/evaluated/effective result without claiming remote success. |

D11 supersedes treating a recommended single stopping mode as the owner's universal policy. Measurements must distinguish actual running files, a real bounded engine round, pending work and discovery before engine startup; a failed offline connection is not evidence of a queued synchronization job.

### Reconciliation and group policy

| ID | Accepted behavior | Guard against an unintended interpretation |
| --- | --- | --- |
| D13 | A returning device may automatically execute the approved plan and resume if it has no local policy changes, conflicts or bulk warnings. | Do not ask for confirmation solely because the device reconnected. Missing evidence of receipt/application still cannot be reported as success. |
| D14 | Already-confirmed local/server changes may merge automatically only when demonstrably independent in effect, with no conflicts or bulk warnings. Ambiguity goes to the owner. | Unapplied drafts stay drafts. Different folders alone do not prove independence. No timestamp-wins, server-wins, local-wins or selected merge engine follows. One active administrator does not remove stale confirmed offline changes. |
| D15 | Reconciliation applies both at reconnect and on relevant policy changes during an active connection. Preserve both sides' changes and re-evaluate outstanding work at the applicable activation/transfer boundary. | A stale queued decision cannot bypass the selected activation plan. Unknown, unavailable or conflicting policy does not itself grant new permission. |
| D16 | Deliberately adding a device to a group causes it to inherit group policy. Group policy is the base, with explicit visible device exceptions allowed to override it. | Group inheritance is not automatic enrollment. Later group changes must not silently erase device exceptions. |
| D17 | Compatible/equivalent group instructions combine; true contradictory overlaps go to the owner. | No fixed ranking between groups is selected. Re-evaluate effective overlaps as membership or policy changes. |

### Bulk safeguards and lasting learning

| ID | Accepted behavior | Remaining boundary |
| --- | --- | --- |
| D18 | The safety check covers **all bulk actions**, with potentially different settings for each action. | It is not limited to MyBrain. Upload, distribution, download/offline retention and registration may have different impacts for the same offering. Only actions actually supported by a candidate may be claimed. |
| D19 | Assess the whole logically related offering: nested content and multiple jointly offered folders. | Splitting filesystem notifications, executor batches or folders within that offering must not bypass assessment. The exact grouping/detection rule is still open. |
| D20 | An additional cumulative check is accepted in principle, with configurable capability per action. | Measures, limits, accumulation windows and unknown/growing scope behavior are not yet selected. No illustrative number is a default. |
| D21 | Approval of a recognizable continuing flow becomes visible lasting policy for that flow and action. The same warning does not recur merely because another batch arrives, a time window resets or the device reconnects. | This is not global disabling, blanket consent for other actions, or permission for an unrelated flow. Flow recognition, scope changes and renewed assessment boundaries remain open. One-off approval lifetime remains open. |

An existing applicable synchronization or MyBrain rule does not bypass the bulk safeguard. The owner may approve its large effect through the integrated decision; the resulting lasting continuing-flow rule must be understandable and inspectable.

### Presentation principles

| ID | Accepted principle | Observable consequence to test |
| --- | --- | --- |
| D22 | Present plain-language intention and effects first; disclose powerful details and exceptions progressively. | Beginners can understand what happens, where, when and how. Essential consequences are never hidden in advanced settings. Technical terms are not required to make a basic choice. |
| D23 | Explain device/group inheritance and visible exceptions, reusable scope and MyBrain in the same summary and confirmation. | The owner can explain why a device is included/excluded and what future input is allowed. No disconnected MyBrain decision. |
| D24 | Distinguish draft, saved/confirmed, active and pending per-device states from actual transfer, retained copy and MyBrain effects. | Do not present a globally simultaneous active revision or completed registration solely because a policy was saved. |
| D25 | An alert is a decision/learning moment. An approved continuing-flow rule is visible and editable; the owner can inspect why it applies, adjust it or pause it. | No repeated nag for the same approved flow, no hidden global suppression. A novice comprehension test checks expected outcomes before confirmation. |

Example labels or screen text discussed during brainstorming are illustrations, not an approved screen/API design.

## Questions

- Q1–Q5 below are the remaining usage-policy questions, not a reopening of D01–D25. Resolve only those needed for a particular bounded experiment before executing it.

## Approved Strategy

The owner has approved D01–D25 as behavioral direction. This consolidation selects no native integration, backend/topology change, formal policy schema, synchronization algorithm or update-maintenance strategy. Remaining product choices are limited below; technical strategy decisions still require evidence and the appropriate owner decision before Design. This is a mid-Research checkpoint, not phase acceptance.

## Expected Results

### Current behavioral probe contract

Every row is **NOT RUN**. These are Research oracles, not formal interfaces or an implementation plan. An unresolved policy blocks only cases that depend on that boundary. A bounded synthetic probe may explicitly declare illustrative thresholds/windows as fixture parameters, never as silent product defaults or substitutes for a missing usage decision. Before a bounded run, record the actual OS/client/server/Web/SDK/executor versions, the claimed seam, supported paths/actions, synthetic fixtures, request/body observation points, unmodified control and retention-safe cleanup. Observe the initial TUS POST as well as later requests. Missing coverage is insufficient evidence, not a zero-byte result. A mock or policy-only roundtrip must be labelled partial.

| ID | Probe and controlled variation | Required observation or falsifier | Policy prerequisite |
| --- | --- | --- | --- |
| W01 | Live Windows GUI discovers new files and nested folders inside an already-connected ordinary root; edit existing content, defer/close the wizard and make the policy service unavailable. | Grouped local discovery and **zero content bytes before an applicable accepted decision** on all claimed routes. Inspect requests, logs and previews for only the explicitly permitted candidate facts; excluded content must not leak through an analysis call. Measure watcher/VFS/discovery/retry paths and initial request bodies. Reactive filtering, notification, server rejection/quarantine or unknown observation coverage cannot prove the hold. | Q5 before candidate facts leave the device; Q4 for uncertainty about an active version after an interrupted policy change. |
| W02 | Activate a changed policy through the claimed external control/integration seam while the real GUI process is alive. Compare with a stock/manual-settings control. | External activation is distinguishable from manually editing supported settings. Observe the actual effective revision and ensuing requests. Fresh CLI starts or saved exclude files alone do not prove live GUI activation, atomic replacement or race-free enforcement. | Q4 where failed/uncertain activation must be resolved; supported seam remains a technical unknown. |
| W03 | Normal editor: save/change/cancel a draft while the valid old policy is active; explicitly Apply. Also exercise pause-before-edit and later-maintenance alternatives. | No draft is applied silently; chosen strategy and pause/activation/resume status are visible. Old active policy remains valid during normal drafting. Measure whether targeted pause works; record wider pause/restart requirements rather than assuming the preference is available. | Q4 for failed activation/handover, not for reopening the accepted normal strategy. |
| W04 | Establish real running transfers and a separately observable bounded planned round. Exercise each of the three finalization choices; repeat with no relevant running work. | Finish current files, finish the identified bounded round, or interrupt/re-evaluate remaining work as selected. Show what can already have been sent; do not claim byte rollback or impose a universal choice. No irrelevant choice when idle. A failed preflight is not a queued round. | Q3 if a warning/failure overlaps work; Q4 if activation fails. |
| W05 | One grouped native decision includes storage, devices/groups, supported availability, MyBrain and reusable scope; then add matching files and a cache exception. | One summary/confirmation keeps the whole intention. Accepted matching rules can handle later content automatically; excluded caches are not permanently registered. Actual effects remain distinct from saved intention. | Q5 for worklist metadata disclosure/retention; Q1–Q3 when exercising bulk or continuing approval. |
| W06 | Edit/replace content after a snapshot-specific individual approval and before actual send; compare with a reusable class rule and changed metadata/scope. | Individual permission does not silently float to changed content. Re-evaluate which accepted decision/rule applies; known class matches do not acquire a fabricated universal per-file approval or hash requirement. | Q3 for one-off scope/lifetime across retries; no universal identity/hash mechanism selected. |
| R01 | Create and confirm the complete rule offline using explicitly cached inventory; restart; compare origin-only versus selected-device/shared intention. | Local durable choice survives, including MyBrain and intended reach. Show stale knowledge and pending remote effects. An allowed server copy does not widen origin-only execution. | Q5 for record disclosure; Q4 for interrupted policy changes or unresolved confirmed changes. |
| R02 | Finalize a change while one device is unreachable, then return that device with no local policy changes, conflicts or bulk warnings. | Approved later execution plan is visible; the returning device executes/resumes automatically and reports actual receipt/evaluation/effect. Reconnection alone causes no extra prompt. | Q4 for the plan's uncertain/failure edges; the clean automatic path is accepted. |
| R03 | From one reconciled baseline, make already-confirmed local and server changes demonstrably independent in effect. Include a broader group rule to disprove a naive different-folder test. Also retain an unapplied local draft. | Independent confirmed changes can merge automatically without lost change or unnecessary prompt; drafts do not auto-activate. Assert independence over effects, not just pathname separation. | No new group/merge preference needed; technical evidence must demonstrate the independence claim. If uncertain, use R04. |
| R04 | Create conflicting or ambiguously interacting confirmed local/server changes, both on reconnect and while connected. | Preserve both and ask the owner; no implicit winner or new permission from the conflict. Pending work is re-evaluated against the resolved applicable plan. | Q3 for blocking/partial effects; Q4 for uncertainty and failure continuation. |
| R05 | Deliver duplicate/older revisions; interrupt exchange before/after save, receipt and activation; restart/retry with real outstanding GUI work. | No lost intention, stale permission restoration, unintended duplicate effect or false completion. Receipt is not application. Apply the chosen in-flight boundary rather than retroactive byte rollback. | Q3/Q4 for affected work and recovery behavior. |
| R06 | Use offline, retired/new devices, changed server folders and unknown capabilities; change active management endpoint with stale confirmed changes and drafts. | Inventory is truthful; unsupported availability/current counts are not invented; one active administration endpoint does not silently discard other devices' policy or pretend unreachable work is complete. | Q4 for control handover or uncertain activation; Q5 for disclosure. |
| G01 | Deliberately add a device to a group; reconnect an offline member; apply an explicit device exception and change the base group policy later. | Inherit the group base only after deliberate membership. Keep the exception visible and effective without silently erasing it. Observe receipt and actual per-device effect separately. | Q4 only for unconfirmed/unreachable application edges. |
| G02 | Combine equivalent/compatible group instructions, then a true contradiction; change membership or a broader rule. | Compatible instructions combine; true contradictions go to the owner, with no fixed group ranking. Expose device exceptions and re-evaluate changed overlap. | Q3 for the work blocked during a contradiction. Group precedence is already decided. |
| B01 | Offer a large allowed set in one folder, nested folders and multiple jointly offered folders; split arrival notifications/batches while preserving the logical offering. Test each claimed bulk action, including MyBrain and non-MyBrain effects. | Assess the whole offering and each action's impact; existing rules or batching cannot bypass the check. Different action impacts/settings are visible; unsupported actions are declared. | Q2 for measures/limits/grouping and growing/unknown scope; Q3 for what waits or can proceed. |
| B02 | A recognizable flow arrives in individually small groups that cumulatively cross the guard. Approve the continuing flow/action, then repeat across batches, a time-window boundary and reconnect. | Cumulative assessment works without fragmentation bypass. Continuing approval creates visible lasting policy and prevents the same warning merely from a new batch/time window/reconnect. No global suppression. | Q1 for recognizable same-flow scope; Q2 for accumulation; Q3 for any one-off approval comparison. |
| B03 | After continuing approval, offer an unrelated flow, a newly requested action or changed circumstances outside approved scope; compare with the unchanged approved flow. | Guard remains available outside approved scope; no widened consent. Continued matching input retains its lasting approval. New assessment follows the approved scope/drift policy. | Q1 for boundaries requiring renewed decision; Q2/Q3 for impact and blocking behavior. |
| U01 | A beginner reviews simple and advanced cases, group exceptions, bulk approval, drafts and offline pending devices; ask them to explain effects before confirming. | They can explain what goes where, when, which devices/groups/exceptions matter, what MyBrain will do, what is permanently allowed and what remains pending. Essential effects are visible without advanced controls; powerful details remain available. | Relevant Q1–Q5 choices for the presented scenario. No fixed screen design or numeric comprehension threshold selected. |
| T01 | After proving the required admission/activation seams, observe origin-only versus all-client eligibility on a second existing, new and reconnected client. | Measure visibility/placeholders, actual downloaded bytes and offline retention separately. A server copy does not prove distribution permission; manual client selection is not shared enforcement evidence. Deliberate groups/exceptions remain visible, with no silent enrollment. | Q4/Q5 only where activation/disclosure edges are exercised; no external-user sharing involved. |
| P01 | Narrow a rule/distribution scope, cancel/defer a wizard, interrupt/retry or fail a transfer/reconciliation after copies exist. | Retained local/server content is not destroyed by those policy actions. Distinguish visibility/placeholder, bytes, offline retention and registration. Separate deletion cannot be inferred from sync scope changes. | No new deletion policy needed for this non-destruction oracle. |
| X01 | Exercise every claimed platform entry path and an actual admitted version upgrade/update route; retain decisions, pending work and group exceptions. | Re-run relevant admission/activation/retry oracles on the actual versions. Source compilation, Web success, same-version restart or official update installation alone cannot prove preserved custom behavior. Unsupported routes/versions remain explicit. | Technical compatibility strategy and bounded execution mandate first; relevant unresolved usage prerequisites still apply. |

A first Windows proof may precede mobile implementation. Shared Web/Uppy upload routes retain their separate coverage obligations from the [historical assessment](opencloud-admission-extension-feasibility.md); Web or a custom upload-screen result cannot substitute for the native wizard/hold. No production roots, accounts or live infrastructure belong in these synthetic runs.

W01/W02 are the decisive missing evidence about the stock Windows GUI and an external activation seam. The earlier CLI control proves neither. This contract does not prescribe a new queue, central-master store or message broker. Actual candidate feedback and before-content enforcement must be observed independently.

### Remaining product-policy questions

These five areas are deduplicated. A bounded probe needs the applicable answer, not necessarily the whole future product policy. Do not execute an unresolved case using a hidden default.

| ID | Remaining owner choice | Why it matters / affected probes |
| --- | --- | --- |
| Q1 — Continuing approval scope | What identifies the same continuing flow and action; how is the lasting scope bounded; which change in origin, content class, destination, membership or other circumstance is material enough to require renewed assessment? These are questions, not predefined identity fields. | B02/B03 and the relevant W05/U01 scenario. Lasting approval itself is decided; recognition and drift are not. |
| Q2 — Bulk impact and accumulation | For each action, which impact measures, limits, accumulation/grouping boundaries or windows apply; how are unknown counts and an offering that grows after its preview treated? | B01–B03/U01. Whole related offerings and cumulative capability are accepted; metrics and values are not. |
| Q3 — Intervention and one-off consent | When a warning, contradiction or uncertain partial outcome needs a decision, which related work waits, may independent actions proceed, and how are partial effects presented? What scope/lifetime does a one-off approval have across retry or restart, as distinct from lasting continuing-flow policy? | W04/W06/R04/R05/G02/B01–B03/U01. This does not replace the three accepted in-flight choices with a universal default. |
| Q4 — Uncertain activation and handover | After a failed/interrupted policy change, pending reconciliation or management handover, how is the active version established, which unfinished effects wait or recover, and how are unreachable devices, stale confirmed changes and drafts handled? | W01–W04/R01–R06/G01/U01. Normal drafting and clean automatic reconnection are decided. Ordinary disconnection with unchanged last-active policy does not itself introduce a fresh server-permission requirement; uncertain new policy cannot grant new permission. |
| Q5 — Candidate and policy disclosure | Which candidate/policy facts may be retained locally or shared before content admission, which local rule records may be backed up/shared, and for how long may those records remain? | W01/W05/R01/R06/U01. Metadata is not automatically harmless, and a server copy does not expand execution reach. P18/P19/P38 and private local intention remain binding; existing source/lifecycle choices are not reopened. |

Separate technical unknowns are the actual live GUI hold/reload/pause seam, achievable action granularity, independence assessment, candidate/inventory persistence and the technical observation-to-registration transition under existing P18/P19/P38, mobile path coverage, OpenCloud/executor interoperability and the native packaging/update route. Source evidence and measurements must answer them; they are not additional owner policy votes.

The maintenance/compatibility choice (supported extension/upstream contract, maintained native integration or an explicitly changed workflow/topology) remains a later Research strategy decision after evidence. No candidate is adopted here. Other-user sharing is deferred and is not a prerequisite for these personal-use probes.

## Assumptions

- All future runtime probes require a separate bounded assignment and synthetic isolated data; this documentation task executes none.
- No new permanent registry, numeric default, time limit, policy granularity or screen layout is selected by this checkpoint.

## Related Documents

- [Canonical issue-9 research](<research.md>)
- [Measured stock Windows filter probe](<stock-windows-filter-probe.md>)
- [Native integration/update source assessment](<native-wizard-update-feasibility.md>)
- [Windows candidate comparison](<windows-sync-candidate-comparison.md>)
- [Foundational principles](<../../architecture/decisions/0001-digital-brain-foundational-principles.md>)
- [Issue 9](<https://github.com/MikeyVK/MyBrain/issues/9>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-07 | Codex (@imp researcher) | Consolidate accepted personal synchronization/group/bulk/presentation policies, remaining usage questions and the current unexecuted behavioral probe contract. |

