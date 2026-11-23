<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Stock Windows filter-loss and retained-policy restart probes

**Status:** RESEARCH MEASUREMENT — filter-loss/restart components; GUI pause/editor unestablished; active retention
**Version:** 1.0
**Last Updated:** 2026-11-08

## Purpose

Record meaningful R5 stock GUI measurements and the supported-control limits without changing the product contract.

## Scope In

The retained synthetic client/account/root; absent user filter, exact restoration, one normal GUI restart and final baseline readbacks.

## Scope Out

No unsupported UI helpers, force termination, new policy implementation, private/production data, backend restart, architecture choice or phase exit.

## Problem Statement

Further stock GUI pause/editor controls were desired, but their supported operability and retained policy/error behavior needed actual bounded evidence.

## Goals

- Measure only established GUI behavior and distinguish inaccessible controls from product failures.
- Preserve complete bodies, unique response joins, error records and exact readbacks.
- Restore an active functioning fixture while retaining account, files, journal and RAM backend.

## Background

R5 followed the frozen R4 background checkpoint under new original owner screen-control and fixture-dialog authority. Earlier R1–R4 results remain historical.

## Findings

### Scope, authority and current client

The owner separately authorized taking over the desktop and handling routine fixture login/security messages. R5 kept the existing synthetic localhost account, Personal CFAPI root, journal and RAM-only backend. It used the unchanged official Windows GUI **4.0.0.3642/9f701e**, Qt **6.11.1**, OpenSSL **3.6.3**, Windows 10 build **19045**, and real OpenCloud **9.0.0 rolling** from the [R3 runtime](stock-windows-gui-live-policy-probe.md#runtime-and-isolation). Executable SHA256 remained **AA621347CFFF26D8E69DC96D8A73C75279A8BFA7F6E860E4C0AF390A7F30ECC8**.

Read-only entry checks matched the actual copied executable, sole synthetic profile/account/root, valid source/served certificate DER fingerprint, four loopback listeners and HTTP 200 status/Graph readbacks. WTSInfoEx level/session checks reported UNLOCKED before desktop work. The ordinary Store client stayed stopped. No personal credentials/files, global trust, OS/security/privacy settings, VFS mode, client code or backend service configuration changed.

The protocol preceded content. Five bounded cases were declared: idle pause/resume, running pause/resume, stock exclude-editor Cancel versus OK, one normal client restart, and missing user-filter behavior. Only fresh R5 subpaths were used. Four tiny physical files plus control revisions generated less than 1 KiB, below the declared 32 MiB ceiling. These are fixture parameters, not product defaults.

### Supported GUI observation and its concrete boundary

A unique returned window identified the exact copied GUI. Text-only native accessibility showed Connected and the sole Personal root Success. A screenshot failed with FrameArrived timeout; after one documented fresh selection/activation recovery, capture again timed out. A fresh indexed right-click failed with **coordinate input geometry is unavailable**. A supported Tab returned without changing the observed focused element. The only secondary accessibility action was Raise on the top window; no relevant pause/editor action was exposed.

Thus idle/running GUI pause and exclude-editor Cancel/OK were **NOT ESTABLISHED**, not failed product behaviors. No pause, editor commit or Cancel occurred. No synthetic running batch was created for an inoperable pause control.

After the genuinely new client process, its default background startup exposed no returned window. One supported exact-copy --show command was issued. The next read-only window inventory did not complete within its requested 12-second timeout; its orchestration was stopped and the JavaScript kernel reset, with reset completion confirmed. No input was left pending. A separately slow read-only host query eventually confirmed UNLOCKED and the known listeners at 21:39:52 UTC. There was no further screenshot/keyboard diagnostic, blind input, custom UI helper or owner button request.

A separate supported native-app entry initially rejected an executable-path argument because Windows requires a returned windowId. Its actual documentation was then read, and one minimal native-window inventory was filtered to the exact copied executable without emitting unrelated entries. The documented getApp({windowId}) returned full accessibility state: Connected, Personal Success and observed focus. A fresh WTS check at 21:46:54 UTC was UNLOCKED, and a capability amendment preceded any input. The new-target screenshot timed out; after fresh focus observation, one supported Tab failed with **failed to activate captured window**. The alternative was stopped and completion acknowledged, with no pause/editor action or new case files. An initial local string-escaping error failed before inventory dispatch and is retained in the original transcript. Thus accessibility observation is supported; this trial did not establish activation/input, and it does not prove every possible native route unavailable.

### M: absent user filter and exact restoration

At **21:25:39.306 UTC** the disposable user filter was set to exactly `*.r5hold\n`, nine bytes (LF), SHA256 **F480858F13AD93F2F3BE5BCE77331B7F871C3064FB83B31850543C6759243083**. Before removing it, a fresh allowed control uploaded with exact independent readback; held.r5hold returned 404.

| Initial file | Body bytes | Marker |
| --- | --- | --- |
| control.txt | 31 | I9-R5-MISSING-CONTROL-20261108 plus LF |
| held.r5hold | 28 | I9-R5-MISSING-HELD-20261108 plus LF |

The byte-verified filter was preserved by renaming it to a fresh sibling in the same disposable profile at **21:27:07.932 UTC**. No ACL or security setting changed. An allowed control edit at **21:27:15.484 UTC** stimulated synchronization while the original filter path was absent.

The actual GUI started rounds at **21:27:25.500, 21:27:35.547 and 21:27:45.565 UTC**; each logged SyncEngine finished with ERROR and SyncResult::Error. At the independent 21:27:45 readback the old control body remained on the server; the new control marker had not arrived, and the held path remained 404. Indexed captures contain no content POST during the missing-filter interval. This is bounded error/blocked-sync evidence, not a useful live positive control during that error or proof of a full admission/recovery protocol.

At **21:28:29.580 UTC** the exact preserved nine-byte filter was restored and a new allowed recovery-control marker written. A 21:30:27 readback still saw the old control; it is retained as a nonmatching intermediate observation. Native logs then showed held content Excluded and **SyncResult::Success at 21:30:32.394 UTC**. The recovery-control readback at **21:31:17.323 UTC** was 200/exact. Authentication retries also occurred; no sole-cause or guaranteed recovery-delay claim follows.

This tests an absent valid user-filter file in the running GUI. It does not test malformed/partial syntax, startup with a missing file, an interrupted effective-revision transition or a general fail-closed security guarantee.

### N: one normal restart with the retained filter

After M recovered, strict host/SID, executable, account/root, journal, startup and protected-Store checks preceded a normal restart. Initial checker attempts used the wrong manifest field name (path instead of relative) and then mismatched leading separators. They stopped before any quit. The corrected comparison retained exact file-set/count, per-file length and SHA256 equality; actual protected Store files matched the original post-quit baseline. Failed checker records/diagnoses remain local; no Store data was changed or rebased.

The exact official copy's documented --quit was requested normally. The original process remained at the 15-second observation deadline, so no force termination or duplicate launch occurred. A later read-only check found zero GUI processes. This was a delayed normal exit, not a successful 15-second shutdown or a permanent quit failure. Closed synthetic configuration/journal copies were retained locally; account credentials/keychain and registered root stayed in their original synthetic profile.

One fresh launch of the same official GUI completed at **21:35:23.768 UTC**. It omitted --show/--showsettings for normal default background startup; no --background flag was invented. QEMU, observer and bootstrap remained running with their original identities. The startup value stayed at its recorded absent baseline. The actual new GUI completed **SyncResult::Success at 21:35:47.485 UTC**.

The same nine-byte extension filter persisted without a GUI Apply. Two fresh files were added after restart at **21:36:39.072 UTC**:

| New file | Body bytes | Independent readback at 21:37:05 UTC |
| --- | --- | --- |
| restart-control.txt, I9-R5-RESTART-CONTROL-20261108 plus LF | 31 | 200, exact saved hash |
| restart-held.r5hold, I9-R5-RESTART-HELD-20261108 plus LF | 28 | 404 |

This establishes one retained-filter/account/root/journal restart component. No pause had been achieved, so pause-state persistence is **NOT ESTABLISHED**. It is not an upgrade test or a substitute CLI synchronization batch.

### Final baseline and retained state

The filter was returned to its known functioning empty state at **21:40:32.512 UTC**, followed by the declared allowed final control edit. The two previously held R5 files and final control all returned 200 with exact saved hashes. The new GUI logged **SyncResult::Success at 21:41:15.165 UTC**.

A final read-only check at **21:42:24.010 UTC** confirmed the new sole GUI, same synthetic account/root/journal, unchanged protected Store digests, two original plus one synthetic registration, absent startup value and all five known backend/helper processes alive. The filter was empty. No account/root/credential removal, data deletion, ordinary-client resume, force kill or backend restart occurred.

The fixture remains **OWNER-DIRECTED ACTIVE RETENTION**. QEMU/backend state is still RAM-only on tmpfs, without a writable disk image; host restart or QEMU shutdown loses it. Durable preservation remains separate future work.

### Frozen request/body evidence

The unchanged observer segment was appended, never reset. **S2219–2370** contains **152 indexed requests and 152 unique joined response records**, without sequence gaps or unmatched indexed records:

| Evidence | Observed count |
| --- | --- |
| Methods | 122 GET, 18 PROPFIND, two MKCOL, ten POST |
| HTTP responses | 110 HTTP 200, eight 201, seventeen 207, eight 401, six 404 |
| Statusless transport-error records | Three: S2336/S2338/S2340 |
| File-content POSTs | Six complete bodies, 200 bytes total; all six 201 |
| Authentication POSTs | Four refresh forms, 5888 bytes total; all four 200 |
| PROPFIND metadata | 5002 bytes, not file content |
| Indexed body length/framing mismatches | Zero |
| Synthetic-path GET readbacks | Twelve, including preserved nonmatching intermediate observations |

S2336 and S2340 were Graph drives GETs; S2338 was a status GET. Their observer records contain ConnectionAbortedError/10053 and **no HTTP status**. Their cause is not established; a matched response record is not a successful HTTP response. No all-requests-healthy claim follows. The eight 401s were GET responses; the four token-refresh POSTs returned 200. Normal authentication refresh is not policy-activation recovery.

| File-content sequence | Bytes | Meaning |
| --- | --- | --- |
| S2255 | 31 | Initial M allowed control |
| S2294 | 40 | M restored-filter control |
| S2333 | 31 | N post-restart allowed control |
| S2361 | 28 | M held file released under final empty filter |
| S2362 | 42 | Final allowed control |
| S2363 | 28 | N held file released under final empty filter |

Request/response matching used unique sequence keys. Complete body markers and saved hashes were compared with independent server reads using the exact original IPv4/agent:false helper. The observer SHA256 remained **A0F9E6B755CF9AB05345617399FDE235A3637743A9C939E5B757D26C5A00E118**. Its timestamp is sampled after the complete Content-Length body read and body-file write, before forwarding; it is not a first-byte, request-start or effective-policy acknowledgement. Unsupported Transfer-Encoding/over-16-MiB limits and broader VFS/preview/analysis coverage remain as documented in the [R3 report](stock-windows-gui-live-policy-probe.md#complete-body-coverage-and-limits). No PUT, PATCH or DELETE appears in this indexed interval.

### Evidence index and remaining coverage

The existing ignored R3 evidence-index.json now indexes R5 protocol, original operation results, readiness, missing-file controls/restore, guard corrections, closed config/journal, restart observations, full measurement-summary.json, final readbacks and retained-state evidence. Old captures and R1–R4 reports remain intact. Raw credentials, authentication forms, host paths/identifiers and registration identities stay local-only.

W01/W02/P01 remain **PARTIAL** against the [unchanged full oracles](synchronization-policy-and-probe-contract.md#current-behavioral-probe-contract); the other nineteen cases remain NOT RUN. R5 adds missing-user-filter error/restoration and one retained-policy normal restart. GUI pause/finalization choices, editor Cancel/OK, pause persistence, full native wizard/shared policy, explicit effective revision, interrupted transition and upgrade behavior remain unestablished.

## Questions

- Establish an operable supported pause/editor control route before testing idle/running finalization or Cancel/OK.
- Keep effective-revision, interrupted-policy, upgrade and native/shared-wizard contracts open.
- Scope durable backend preservation separately before a host restart or QEMU shutdown.

## Approved Strategy

No client patch, fork, replacement workflow, rule compiler or maintenance strategy is selected. These bounded stock measurements remain Research evidence.

## Expected Results

W01/W02/P01 remain PARTIAL and nineteen cases NOT RUN. Keep the empty filter, active unpaused test client and retained RAM backend; no full-contract acceptance or phase exit follows.

## Related Documents

- [Canonical Research](<research.md>)
- [Current behavioral oracles](<synchronization-policy-and-probe-contract.md>)
- [R4 background measurements](<stock-windows-gui-background-probes.md>)
- [R3 GUI measurements](<stock-windows-gui-live-policy-probe.md>)
- [Isolation and retention history](<windows-gui-probe-isolation-assessment.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-08 | Codex (@imp researcher) | Record R5 supported-UI limits, missing-filter error/restoration, one retained-policy restart, transport errors and successful final active baseline. |
