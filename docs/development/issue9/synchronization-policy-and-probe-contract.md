<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Synchronization policy decisions and behavioral probe contract

**Status:** RESEARCH CHECKPOINT — owner policy consolidated; W01/W02 full cases PARTIAL, technical strategy open; owner-directed active fixture retention
**Version:** 1.6
**Last Updated:** 2026-11-08

## Purpose

Consolidate the owner's accepted issue-9 policy and presentation choices, separate deferred settings from technical unknowns, and define falsifiable behavioral probes before Design.

## Scope In

The integrated Windows-first native wizard, personal device/group policy, draft and activation behavior, offline reconciliation, all-action bulk safeguards, presentation, measured bounded stock GUI components and remaining proof obligations.

## Scope Out

No formal Design/API contract, selected implementation or compatibility route, application code, production access, deployment, new storage decisions or phase exit. This document supplies no standing runtime authorization; measured results below came from a separate owner-authorized synthetic probe. Sharing with other users is a later direction only.

## Problem Statement

The required wizard now includes owner decisions that are more specific than the earlier research questions. Keeping those questions unchanged would reopen accepted choices or let an experiment silently invent the remaining policy.

## Goals

- Keep accepted choices auditable and separate from proposals, measured behavior and unresolved policy.
- Make the integrated behavior testable without assuming that manual stock-client settings prove external policy control.
- Keep resolved usage policy separate from deferred parameters, technical unknowns and future research.

## Background

The initial 2026-11-07 consolidation recorded the owner's policy discussion and request to update issue 9, the research and probe contract. The owner subsequently resolved Q1–Q5 one by one, ending on 2026-11-08 with shared visibility/manageability of device-bound rules as the default. The decisions below are user-experience requirements, not evidence that OpenCloud implements them. The canonical research entrypoint remains research.md. The source-pinned platform reports and completed stock CLI measurement keep their historical evidence status.

## Findings

### Authority and evidence boundaries

The owner accepted these choices in the discussion culminating in this consolidation. A later refinement supersedes an earlier suggestion where noted. This is the current behavioral baseline for all candidate implementations; it does not select a merge algorithm, rule language, client patch, protocol or screen layout.

| Evidence class | Current status |
| --- | --- |
| Owner decisions | The accepted behavior below constrains later probes and Design. |
| Source/release research | Pinned evidence remains in the [native assessment](native-wizard-update-feasibility.md) and [candidate comparison](windows-sync-candidate-comparison.md). No new platform verification is claimed here. |
| Executed component control | The [stock Windows CLI report](stock-windows-filter-probe.md) measured manually supplied filters and fresh batch starts only. |
| Later GUI preparation and measurement | [R1/R2 isolation/readiness history](windows-gui-probe-isolation-assessment.md) remains unchanged in scope. [R3 actual GUI measurements](stock-windows-gui-live-policy-probe.md) then established finite stock hold and external-file activation components using supported accessibility and human handoffs. A later Graph GET returned 401, followed by successful refresh and Graph retries; the owner now directs active retention of R3 rather than immediate restoration. |
| Integrated behavioral probes | W01/W02 are **PARTIAL** against their full oracles, with positive bounded stock components. The other twenty cases are **NOT RUN**. No full wizard, effective-revision/interruption/recovery or shared-device acceptance follows. |

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
| D18 | The safety check covers **all bulk actions**, using number of files and total size per action with configurable limits. | It is not limited to MyBrain. Actions may have different impacts/settings for the same offering. Concrete limits remain deferred; only supported actions may be claimed. |
| D19 | Assess the whole logically related offering: nested content and multiple jointly offered folders. | Splitting filesystem notifications, executor batches or folders within that offering must not bypass assessment. The technical grouping/detection mechanism still needs research. |
| D20 | An additional cumulative check is accepted in principle, configurable per action alongside file-count/size limits. | Concrete limits, accumulation windows and exact scope values remain deferred. New unknown/growing offerings follow D35. No illustrative value is a product default. |
| D21 | Approval of a recognizable continuing flow becomes visible lasting policy for that flow and action. The same warning does not recur merely because another batch arrives, a time window resets or the device reconnects. | Normal future rules are bounded by recognizable conditions; wider scope is an explicit advanced choice under D26. No consent for other actions or unrelated flows follows. One-off approval follows D29. |

An existing applicable synchronization or MyBrain rule does not bypass the bulk safeguard. The owner may approve its large effect through the integrated decision; the resulting lasting continuing-flow rule must be understandable and inspectable.

### Presentation principles

| ID | Accepted principle | Observable consequence to test |
| --- | --- | --- |
| D22 | Present plain-language intention and effects first; disclose powerful details and exceptions progressively. | Beginners can understand what happens, where, when and how. Essential consequences are never hidden in advanced settings. Technical terms are not required to make a basic choice. |
| D23 | Explain device/group inheritance and visible exceptions, reusable scope and MyBrain in the same summary and confirmation. | The owner can explain why a device is included/excluded and what future input is allowed. No disconnected MyBrain decision. |
| D24 | Distinguish draft, saved/confirmed, active and pending per-device states from actual transfer, retained copy and MyBrain effects. | Do not present a globally simultaneous active revision or completed registration solely because a policy was saved. |
| D25 | An alert is a decision/learning moment. An approved continuing-flow rule is visible and editable; the owner can inspect why it applies, adjust it or pause it. | No repeated nag for the same approved flow, no hidden global suppression. A novice comprehension test checks expected outcomes before confirmation. |

Example labels or screen text discussed during brainstorming are illustrations, not an approved screen/API design.

### Policy resolutions accepted on 2026-11-08

These complete the one-by-one discussion of Q1–Q5. They refine the existing baseline rather than assert an OpenCloud capability.

| ID | Accepted behavior | Boundary preserved |
| --- | --- | --- |
| D26 | The normal wizard builds a recognizable bounded rule for future input. “Accept everything in future” is an explicit advanced/super-user choice within a visible chosen scope, action and destination. | Advanced/super-user describes interaction, not a new user/rights role. Wider permission is not blanket consent for other locations/actions. Exact rule conditions are selected for the use case; detection and rule representation remain technical research. |
| D27 | Evaluate both file count and total size for each action, with configurable limits. | Concrete values and cumulative windows are deferred. Virus/content checks, temporary/cache recognition and local-AI detection are future research input, not selected techniques or current acceptance obligations. |
| D28 | Demonstrably independent actions may proceed when another action warns, conflicts or waits. If independence is uncertain, the whole involved job waits. | Do not silently perform dependent parts or constrain the owner's remaining choice. Show executed effects separately from waiting work. |
| D29 | One-off approval belongs to the bounded job until completion or owner revocation, including interruption/restart/retry, subject to effective policy on resumption. | It covers the approved set, actions and destinations. Later-added files are outside it; changed files/effects are re-evaluated. The owner can inspect, pause or revoke it. No session expiry or numeric duration is introduced. |
| D30 | Work affected by an uncertain policy transition waits while the approved transition is recovered. Automatic recovery is allowed only when unambiguous, requiring no new decision and causing no conflict or bulk warning; otherwise ask the owner. | Preserve existing copies and completed effects. Independent actions follow D28. Ordinary unchanged offline use is not a failed transition and gains no fresh-permission lease requirement. |
| D31 | The owner may explicitly take over active administration when the previous endpoint is unreachable. Preserve its drafts as drafts and reconcile confirmed changes under the accepted rules. | Show which devices have not received the takeover. Ordinary synchronization under effective policy may continue. No instantaneous control of offline devices or distributed-lock/lease technology is selected. |
| D32 | A continuing shared current/last-known file/location overview is the default within admitted locations, including local-only files. Limited candidate/location information may reach the owner's own server/devices before content approval. | Visibility is not content availability or transfer permission. From the active management endpoint the owner may request policy for another device; if that source is offline, execution waits with truthful status and later reconciliation. |
| D33 | Inventory covers only consciously connected folders and locations. | No whole-device crawl, discovery outside admitted scope or elevated-rights policy is introduced. |
| D34 | Retain observed per-file location changes plus decisions and execution history. Foreground the current/last-known overview; history is accessible through details. Preserve synchronization history by default, with cleanup only on explicit owner initiative or consciously configured cleanup policy. | No default automatic expiry, promise of unobserved offline changes or full content-version backup. Cleaning this history does not delete actual files or MyBrain registrations; their retention rules remain separate. |
| D35 | For a new unknown/growing offering, first bound/inventory the whole logically related offering and assess it before execution by default. Phased execution is an explicit advanced possibility. | Established approved continuing flows retain their own scope/conditions. Recognition of an offering and when its extent is sufficiently known are technical questions; no hidden time/count default is selected. |
| D36 | All rules within admitted scope are shared visible/manageable by default, including origin/device-only rules. Offline local authoring remains possible; records distribute/reconcile when connected. | A shared record does not widen execution reach. A deliberately private local rule remains an explicit exception. MyBrain staging/admission is a separate applicable rule or decision inside the same integrated wizard; an operational observation is not thereby a durable source. |

Limited metadata may, for example, describe a name, location, type or size; these examples do not select an exhaustive schema. Sharing here is between the owner's own devices/server, not with other users. The location overview distinguishes known presence, actual content availability and freshness. The policy/history overview must not claim an unobserved offline event or completed remote action.

## Questions

The previously open Q1–Q5 areas are now resolved at this behavioral level; the [resolution ledger](#remaining-product-policy-questions) retains their identifiers and the old link anchor. Concrete settings, exact scope values and technical evidence remain separate. No new owner vote is identified as necessary for the listed behaviors merely because those values have not become product defaults.

## Approved Strategy

The owner has approved D01–D36 as behavioral direction, including the Q1–Q5 resolutions. No native integration, backend/topology change, formal policy schema, synchronization algorithm or update-maintenance strategy is selected. Concrete policy settings remain configurable/deferred; technical strategy decisions still require evidence and the appropriate owner decision before Design. This is a mid-Research checkpoint, not phase acceptance.

## Expected Results

### Current behavioral probe contract

W01/W02 have the bounded coverage below; the other twenty rows remain **NOT RUN**. These are Research oracles, not formal interfaces or an implementation plan. Q1–Q5 now supply accepted behavioral expectations rather than unanswered votes. A bounded synthetic probe must declare its selected scope, settings and limits/windows where relevant as fixture parameters, never as silent product defaults. A genuinely new policy question blocks only the case that needs it and must be identified explicitly. Before a bounded run, record the actual OS/client/server/Web/SDK/executor versions, the claimed seam, supported paths/actions, synthetic fixtures, request/body observation points, unmodified control and retention-safe cleanup. Observe the initial TUS POST as well as later requests. Missing coverage is insufficient evidence, not a zero-byte result. A mock or policy-only roundtrip must be labelled partial.

| Current coverage | Status | Measured and still missing |
| --- | --- | --- |
| W01 | **PARTIAL** | New/edited/nested held markers stayed local under a pre-established finite stock filter while a permitted GUI edit uploaded; complete bodies and independent readbacks were observed. Full integrated wizard/candidate sharing, service-outage and every claimed path remain unestablished. |
| W02 | **PARTIAL** | External user-filter replacement took effect while the same GUI lived, without Apply/restart; held/new content uploaded with exact readbacks, first completed round about 18.17 seconds after the write. Explicit effective revision, interruption, uncertain-transition hold and recovery remain unestablished; a later Graph GET returned 401, then refresh POST and Graph retries returned 200. This authentication recovery is distinct from policy-activation recovery. |
| Other twenty cases | **NOT RUN** | No result is supplied by the bounded stock components. |
| R3 runtime disposition | **OWNER-DIRECTED ACTIVE RETENTION** | The earlier Escape/pending-restoration checkpoint is historical. The owner chose to keep the probe account/root/GUI and backend helpers active and leave the ordinary Store client stopped. A read-only 18:37:28 UTC check found the known processes/listeners and local status 200. Backend state is RAM-only; host restart or QEMU shutdown would lose it. Durable preservation is separate future work; no restoration or new test is claimed. |

The [GUI report](stock-windows-gui-live-policy-probe.md) contains exact versions, fixture states, body/readback counts, observation bounds and current retention disposition. The following full oracles are unchanged.

| ID | Probe and controlled variation | Required observation or falsifier | Parameters or technical evidence still needed |
| --- | --- | --- | --- |
| W01 | Live Windows GUI discovers new files/nested folders inside an already-connected ordinary root; edit existing content, defer/close the wizard and make the policy service unavailable. | Grouped discovery and **zero content bytes before an applicable accepted decision** on every claimed path. Default limited candidate/location sharing is allowed only within admitted scope; inspect requests/logs/previews for no excluded content or analysis-call leak. Measure watcher/VFS/discovery/retry and initial bodies. Reactive filtering/server rejection cannot prove the hold. | Declare admitted roots and limited metadata fixture; establish an observable live GUI seam. Missing request coverage is insufficient evidence. |
| W02 | Activate changed policy through the claimed external seam while the real GUI is alive; compare with stock/manual settings. Interrupt activation. | External activation and actual effective revision are observable. Uncertain affected work waits; recover the approved transition automatically only if unambiguous/no new decision/conflict/bulk warning, otherwise ask the owner. Fresh CLI starts or saved filters alone do not prove live activation/race safety. | Actual activation/pause seam and failure observation; preserve completed effects. No new policy vote for the recovery default. |
| W03 | Save/change/cancel a draft under valid old policy; explicitly Apply. Also use pause-before-edit and later-maintenance alternatives. | No silent draft activation or strategy switch. Old policy remains valid during normal drafting. Targeted pause preference versus wider pause/restart feasibility is measured; pending/active status stays truthful. | Actual controllable pause boundary; select synthetic active work. Ordinary unchanged offline use does not require fresh server permission. |
| W04 | Establish real running files and a bounded already-planned round; exercise all three finalization choices and idle behavior. Introduce a warning in one action. | Finish current files/identified round or interrupt/re-evaluate as selected; no imposed universal choice or byte rollback. Demonstrably independent actions may continue; if independence is uncertain, the whole involved job waits. Show completed versus waiting effects. Failed preflight is not a queued round. | Real GUI queue/round evidence and independent/dependent fixture actions; no numeric deadline selected. |
| W05 | One native decision includes storage/devices/groups/availability/MyBrain/reuse; add matching input and a cache exception. Compare a normal bounded future rule with explicit advanced broad permission. | Same summary/confirmation, no detached MyBrain step. Limited shared visibility does not create staging/admission or content permission. Reusable matches need no fabricated per-file review; broad future permission visibly stays within chosen scope/action/destination. Caches are not automatically permanent sources. | Selected recognizable rule conditions and admitted metadata; implementation of the integrated flow remains unproved. |
| W06 | Approve one bounded job, interrupt/restart/retry, add new files and change an approved file/effect. Compare with an established future rule; inspect/pause/revoke approval. | One-off consent survives with its approved set/actions/destinations until completion or revocation, subject to effective policy. New files are excluded; changed content/effects are re-evaluated. No session expiry, universal hash or per-file manual approval is invented. | Declare the approved set and identity/change observations; no numeric consent duration is needed. |
| R01 | Author/confirm a complete rule offline; restart. Compare device-only execution, shared rule records and an explicit deliberately private local exception. | Complete intent survives, including MyBrain and reach. Rules are shared visible/manageable by default when connected, including device-only rules; shared record never widens execution. Private exception remains private. Staleness/pending remote effects are visible. | Record projection/privacy fixtures and actual persistence/reconciliation mechanism. |
| R02 | Finalize with an unreachable device; return it without local policy changes/conflicts/bulk warnings. Also interrupt an approved transition before return. | Clean approved plan executes/resumes automatically with receipt/evaluation/effect evidence. For uncertain transition, affected work waits and unambiguous recovery may proceed automatically; doubt goes to owner. No new confirmation solely because of reconnect. | Observe actual active revision/recovery; distinguish ordinary offline return from interrupted activation. |
| R03 | From a shared baseline, create effect-independent confirmed local/server changes; include a broad group rule that defeats naive folder separation and an unapplied draft. | Demonstrably independent confirmed changes merge automatically without conflict/bulk warning; draft stays draft. Preserve both changes and prove independence in effect. Ambiguity uses R04. | Explicit independent/dependent effects and observable merge/application evidence; no chosen merge algorithm. |
| R04 | Create conflicting/ambiguous confirmed changes while connected and on reconnect; include independent and dependent actions. | Preserve both and ask owner. Only demonstrably independent actions continue without constraining the remaining choice; uncertainty holds the whole involved job. No implicit winner/new permission; re-evaluate affected work under the resolved plan. | Independence/conflict fixtures and actual blocked/completed-effect observations. |
| R05 | Duplicate/out-of-order revisions; interrupt before/after save, receipt and activation; restart/retry with real GUI work and retained copies. | No lost intent, stale permission, repeated unsafe effect or false completion. Uncertain affected work waits; approved recovery is automatic only when unambiguous/no new decision/conflict/bulk warning, otherwise owner. Preserve completed effects and the selected in-flight boundary. | Actual interruption points, effective-revision and retained-effect evidence. |
| R06 | Explicitly take over management while prior endpoint is unreachable; retain its draft/confirmed edits, reconnect it, and include stale device/folder/capability knowledge. | Takeover does not require previous endpoint release. Show pending receipt; drafts stay drafts and confirmed changes reconcile under accepted rules. Ordinary effective-policy sync may continue. No instantaneous offline control, discarded change or invented capability/current count. | Reliable management identity/handover mechanism remains technical; actual disconnected-device evidence required. |
| G01 | Deliberately add a group member; reconnect an offline member; keep a device exception across changed group policy. | Inherit only after deliberate membership; visible exception is not silently erased. Shared record visibility does not change device-bound execution. Observe receipt/effect separately. | Actual membership/effective-rule seam and pending-application observation. |
| G02 | Compatible/equivalent groups, then true contradiction; change membership/broader rule with independent work also present. | Combine compatible instructions; contradiction goes to owner, without fixed group ranking. Only demonstrably independent actions proceed; doubt holds the involved job. Re-evaluate overlap while retaining visible device exceptions. | Controlled effect/conflict/independence fixtures. Group precedence and waiting default are settled. |
| B01 | Offer count-heavy and size-heavy sets across nested/multiple folders; split notifications/batches; grow a new offering during discovery. Exercise each claimed bulk action and an explicit advanced phased path. | Assess file count and total size per action over the whole related offering. Default new unknown/growing offering is first bounded/inventoried and assessed **before execution**. Phased execution is explicit advanced behavior. Independent actions follow D28; batching/old rules do not bypass the check. Established flows retain their own conditions. | Explicit synthetic limits and offering boundary fixture. Reliable detection/sufficiently known extent remains technical; no hidden time/count default. |
| B02 | Cumulative small offerings cross configured per-action limits; approve a bounded continuing flow/action; repeat across batch/window/reconnect boundaries. | Cumulative assessment resists fragmentation. Approval creates visible lasting scoped policy and prevents the same warning merely from a new batch/window/reconnect. It does not suppress unrelated actions/flows. | Selected recognizable conditions, count/size limits and any cumulative window are declared fixture parameters, not defaults. |
| B03 | Compare unchanged continuing scope with unrelated/new-action/out-of-scope input; inspect normal bounded versus advanced broad permission. | Matching established input keeps lasting approval; noncovered effects get the required new decision/check. Advanced broad rule remains explicit and bounded to selected scope/action/destination. Independent continuation versus whole-job wait follows D28. | Explicit selected rule boundaries/change fixtures; actual recognition is technical evidence, not a reopened scope vote. |
| U01 | A beginner reviews normal/advanced rules, bulk consent, group exceptions, draft/active states, offline takeover and shared local-only inventory; open history details. | Before confirmation they can explain what goes where/when, MyBrain's independent choice, future permission and waiting work. Essential effects are visible; history is reachable through details without dominating the current location view. Show executed versus waiting and visible editable/revocable permissions. | Scenario-specific selected settings; no fixed screen design or numeric comprehension threshold selected. |
| T01 | After proving seams, use second existing/new/reconnected clients for origin-only versus all-client eligibility; request from A that files on B become available on A, with B offline. | Shared inventory enables the remote request without implying content availability. Source-offline work waits; return uses approved reconciliation. Measure visibility/placeholders, bytes and offline retention separately; no silent enrollment or inference from manual setup. | Real inventory/policy/execution seam and source availability observations; no other-user sharing. |
| I01 | Within admitted locations, observe per-file placement/moves, including changes outside wizard jobs, plus decisions/execution; keep a source offline, restart, and compare no cleanup with explicit owner cleanup or consciously configured cleanup. Include outside-scope files. | Current/last-known overview is shared by default, including local-only files, with freshness. Retain **observed** per-file location changes plus decisions/effects behind details by default; no automatic expiry. Outside-scope files are not crawled; no unobserved offline history/full content backup is claimed. History cleanup does not delete files or MyBrain registrations. | Declare observation points and, only for configured-cleanup comparison, explicit synthetic cleanup settings. Persistence/location identity/history completeness remain technical. |
| P01 | Narrow distribution/rule scope, cancel/defer wizard or interrupt/fail/retry after copies/history exist. | No destruction of retained files/server copies merely from these policy actions. Distinguish content, placeholders, offline copies, synchronization history and MyBrain registration. Default preserved history is not an automatic MyBrain source. | Actual retention behavior; explicit history-only cleanup is isolated in I01, not implied by scope narrowing. |
| X01 | Cover claimed platform entry paths and an actual admitted upgrade; retain rules, pending jobs, group exceptions and location/history records. | Re-run applicable gate/activation/retry oracles. Compilation, Web success, same-version restart or official update installation alone cannot prove preserved custom behavior. Unsupported routes/versions are explicit. | Compatibility strategy, bounded execution mandate and actual versions first; defer parameters only for cases that need them. |

A first Windows proof may precede mobile implementation. Shared Web/Uppy upload routes retain their separate coverage obligations from the [historical assessment](opencloud-admission-extension-feasibility.md); Web or a custom upload-screen result cannot substitute for the native wizard/hold. No production roots, accounts or live infrastructure belong in these synthetic runs.

The earlier 2026-11-08 [R1/R2 attempts](windows-gui-probe-isolation-assessment.md) established setup/readiness facts only. R3 subsequently used supported accessibility observation and set_value with explicit human native-button/security handoffs; screenshots were not needed for those observations. Before interrupting an ordinary client, confirm both an unlocked session and a supported observable GUI-control route appropriate to the next actions. At a locked desktop, request normal owner unlock. Use bounded supported calls and stop at the desktop-control skill's recovery/interruption boundary; never leave an action behind a Promise.race timeout. These are harness prerequisites, not product policy to stop synchronization when Windows locks. The owner subsequently chose active retention after the R3 Escape interruption; no GUI input was resumed for that decision. Any later stop/restore or new test requires a separate bounded assignment.

The decisive small stock GUI hold and local external-file activation components are now measured separately from the earlier CLI batches. Full W01/W02 acceptance remains open. This contract does not prescribe a queue, central-master store or message broker; integrated candidate feedback, explicit policy state and the remaining enforcement/recovery paths must still be demonstrated.

### Remaining product-policy questions

**Q1–Q5 have been resolved at the behavioral level.** This heading/anchor remains for existing references; the table is now a resolution ledger, not five unanswered votes. No additional owner policy decision is identified for the listed behaviors beyond explicit use-case/trial parameter choices. This does not claim that every future feature policy or technical strategy is settled.

| Earlier area | Accepted resolution | Deferred settings or evidence / relevant probes |
| --- | --- | --- |
| Q1 — Continuing approval scope | Recognizable bounded future rules are normal; explicit advanced broad scope remains limited to the chosen action/destination. Lasting approval survives new batches/windows/reconnects within its conditions. | Select actual conditions/scope for the use case. Reliable recognition is technical; no universal flow-detection algorithm selected. W05/B02/B03/U01. |
| Q2 — Bulk impact and accumulation | File count **and total size per action**, configurable limits; whole-offering assessment. New unknown/growing offering is bounded/inventoried before execution by default; phased execution is explicit advanced. | Concrete limits, accumulation windows and sufficiently known extent/detection evidence remain deferred. Synthetic parameters must be explicit. B01–B03/U01. |
| Q3 — Intervention and one-off consent | Independent actions may continue only demonstrably; doubt holds the involved job. One-off approval stays with its bounded set/actions/destinations through restart/retry until completion/revocation, checked against effective policy; later additions excluded and changed effects re-evaluated. | Actual dependency/identity/effect evidence, selected job scope. No fresh session expiry or numeric lifetime needed. W04/W06/R04/R05/G02/B01–B03/U01. |
| Q4 — Uncertain activation and handover | Affected work waits; recover approved transition automatically only when unambiguous without new decision/conflict/bulk warning, otherwise owner. Explicit management takeover is allowed with unreachable previous endpoint; preserve drafts/confirmed changes and show pending receipt. | Real active-revision, recovery and single-management enforcement seam; no fresh permission lease for ordinary unchanged offline use. W01–W04/R01–R06/G01/U01. |
| Q5 — Candidate, location, history and policy records | Default shared limited inventory and manageable rule records within consciously connected locations, including local-only files/device-bound rules. Deliberately private local rule is explicit exception. Observed per-file location/decision/execution history is retained by default; cleanup only explicit or consciously configured. Content and MyBrain staging/admission keep their own applicable decision/rule in the same wizard. | Exact record projection, identifiers/observation coverage and any deliberately configured cleanup period are later details. No whole-device inventory, default expiry or durable MyBrain registration from mere visibility. W01/W05/R01/R06/T01/I01/U01. |

Separate technical unknowns remain: integrated native admission and explicit policy-revision/pause/activation contracts beyond the measured stock filter components, action/dependency granularity, reconciliation and management handover enforcement, admitted-location discovery/metadata projection and history persistence, the observation-to-registration transition under P18/P19/P38, mobile coverage, OpenCloud/executor interoperability and native packaging/updates. These require source/runtime evidence, not reopening accepted usage choices.

Virus/content checks, temporary/cache classification and possible local AI are **future research input only**. No detection technique, reliability guarantee or implementation requirement is selected for the current probes.

The maintenance/compatibility choice (supported extension/upstream contract, maintained native integration or explicitly changed workflow/topology) still requires Research evidence and the appropriate strategy approval before Design. No candidate is adopted or universal Research completion declared. Other-user sharing remains deferred.

## Assumptions

- Future runtime probes require a separate bounded assignment and synthetic isolated data. This contract records the separately authorized R3 result without granting further runtime or cleanup authority.
- Shared location/rule/history behavior does not select a database/schema, protocol, default numeric value, time limit, detection technique or screen layout.

## Related Documents

- [Canonical issue-9 research](<research.md>)
- [Measured stock Windows filter probe](<stock-windows-filter-probe.md>)
- [Measured stock Windows GUI components](<stock-windows-gui-live-policy-probe.md>)
- [Native integration/update source assessment](<native-wizard-update-feasibility.md>)
- [Windows candidate comparison](<windows-sync-candidate-comparison.md>)
- [Foundational principles](<../../architecture/decisions/0001-digital-brain-foundational-principles.md>)
- [Issue 9](<https://github.com/MikeyVK/MyBrain/issues/9>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-07 | Codex (@imp researcher) | Consolidate accepted personal synchronization/group/bulk/presentation policies, remaining usage questions and the current unexecuted behavioral probe contract. |
| 1.1 | 2026-11-08 | Codex (@imp researcher) | Resolve Q1–Q5 from owner replies, add shared admitted-location/rule/history defaults and takeover/recovery/consent behavior, and revise unexecuted probes without selecting implementation or numeric defaults. |
| 1.2 | 2026-11-08 | Codex (@imp researcher) | Link actual isolated GUI preparation and locked-desktop prerequisite; add unlock-before-stop and bounded UI-execution safeguards without changing unexecuted behavioral expectations. |
| 1.3 | 2026-11-08 | Codex (@imp researcher) | Record unlocked window discovery but failed supported capture/recovery; preserve all NOT RUN oracles and require operable capture before ordinary-client interruption. |
| 1.4 | 2026-11-08 | Codex (@imp researcher) | Record bounded positive W01/W02 GUI components as PARTIAL full cases, remaining twenty NOT RUN, initial HTTP attribution (corrected in 1.5) and pending cleanup; admit supported accessibility/handoffs without changing oracles. |
| 1.5 | 2026-11-08 | Codex (@imp researcher) | Correct HTTP sequence attribution to transient Graph 401 followed by successful refresh/retries; preserve full-case PARTIAL and cleanup PENDING without claiming policy-recovery proof. |
| 1.6 | 2026-11-08 | Codex (@imp researcher) | Record owner-directed active fixture retention, superseding the pending restoration decision; preserve behavioral oracles and disclose volatile backend state. |
