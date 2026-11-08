<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Windows GUI probe setup, isolation and host prerequisite

**Status:** HISTORICAL R1/R2 SETUP — later R3 components measured separately; R3 cleanup pending
**Version:** 1.4
**Last Updated:** 2026-11-08

## Purpose

Preserve the actual R1/R2 preparation, fresh-profile boundary, readiness failures and R1 restoration; link later R3 content measurements and their current pending-restoration boundary.

## Scope In

The unchanged official Windows GUI, supported package activation and configuration boundaries, a real disposable loopback server/observer, fresh synthetic profile entry, read-only session status and exact cleanup. The owner requested real graphical tests; preparation evidence is reported separately from their content and activation oracles.

## Scope Out

No personal account/file use, personal profile relocation, client patch, production infrastructure, global trust/network change, Windows feature/SDK installation, integration choice or phase exit. R1/R2 did not complete account/root connection or content measurement; separately authorized R3 results are linked below.

## Problem Statement

W01/W02 require one persistent real graphical Windows client with a synthetic ordinary connected root and complete upload-body observation. Entry must establish account/configuration isolation and an operable desktop before a content-hold or live-policy result can be measured.

## Goals

- Distinguish setup facts from the before-content and external-activation acceptance oracles.
- Preserve a reproducible minimal entry and restoration route for the eventual actual GUI run.
- Identify the concrete host prerequisite without changing accepted synchronization behavior or calling setup traffic a successful hold.

## Background

The owner authorized W01/W02 on 2026-11-08. Initial investigation did not establish a GUI profile flag and recorded an entry barrier. Further package/KnownFolder evidence and independent review established a smaller reversible route: preserve the existing Store profile in place, temporarily quit its client normally, and run the unchanged copied executable with a fresh unpackaged profile. Co authorized that bounded route under the original graphical-probe request.

This revision supersedes the earlier entry-only draft's claim that profile isolation itself remains the unresolved blocker. A fresh unpackaged process/profile was demonstrated. The subsequent read-only session query established a locked Windows desktop; no account/root connection or content run followed.

## Findings

### Environment and actual preparation

| Surface | Observed fact | Limit |
| --- | --- | --- |
| Official copied GUI | FileVersion/ProductVersion **4.0.0.3642**, client commit **9f701e**, Qt **6.11.1**, OpenSSL **3.6.3**, Windows 10 build **19045**. Copied executable SHA256 **AA621347CFFF26D8E69DC96D8A73C75279A8BFA7F6E860E4C0AF390A7F30ECC8** matched the installed official executable. | Matching bytes do not establish runtime package identity or a connected GUI. Those were checked separately where applicable. |
| Plugin layout | Complete retained official layout; the client reported Windows CFAPI available. No plugin was removed, patched or renamed. | Available CFAPI is not proof of an actual test root/provider or VFS transfer path. No root was connected. |
| Real backend | Retained QEMU/Alpine fixture ran real OpenCloud **9.0.0 rolling**, initialized successfully with new synthetic authentication. Guest memory bound **1536 MiB**, two virtual CPUs; no host mounts or bridging. | Disposable server readiness, not GUI synchronization proof. |
| Endpoint scope | Bootstrap, observer, backend forwarding and guest serial listeners were bound only to loopback. Backend and observer status requests returned HTTP 200. | The fixture TLS setting remained scoped to the disposable connection; no global trust change occurred. |
| Setup authentication | A synthetic app-token Basic-authentication Graph request succeeded. An earlier attempt using the token as Bearer returned HTTP 401. | Fixture preflight only; no personal credentials or GUI OAuth account were used. |
| Observer capture | Five setup requests/responses: four GET, one POST; four HTTP 200 and one HTTP 401. No request body bytes were recorded. | **This is not a zero-content hold result.** No positive GUI file upload ran, no connected root existed and no content-transfer coverage was established. |
| Empty test root | Fresh workspace-owned synthetic root created; no files or journal were added by a connected account. | It did not exercise discovery, watcher, queue, reconciliation, upload or retention. |

Machine-specific endpoints, process identities, package/account identifiers, profile paths, synthetic secrets and raw logs remain local-only. Independent QA receives the separate local evidence index; these are not repository/public evidence links.

### Source-supported entry and proven package separation

The [v4.0.0 GUI entry](https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/gui/main.cpp) registers show/quit/log/debug and CLI-forwarding options. It does not register --confdir or --multiple. It sets the normal application identity before reading configuration, constructs KDSingleApplication and can send commands to a primary instance. The [internal ConfigFile setter](https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/libsync/configfile.cpp) is therefore not an exposed GUI launch contract.

[Qt's Windows standard paths](https://github.com/qt/qtbase/blob/v6.11.1/src/corelib/io/qstandardpaths_win.cpp) use Windows KnownFolders. [Microsoft's package virtualization description](https://learn.microsoft.com/en-us/windows/msix/desktop/desktop-to-uwp-behind-the-scenes) explains why packaged and unpackaged processes can see different application-data locations. No environment-variable redirect, binary identity trick or guessed portable flag was used.

The actual copied-process check, completed **before any account connection**, established:

- The copied executable was the sole OpenCloud GUI process and returned APPMODEL_ERROR_NO_PACKAGE (15700).
- The launcher, copied process and restoration baseline belonged to the same Windows user; KnownFolder mappings were checked in that actual host context.
- Its new ordinary application-data configuration contained zero restored accounts and zero roots.
- The protected Store configuration/cache file sets and hashes matched the baseline taken after the original client's normal exit.
- The existing Windows sync-root registration set was unchanged.

This proves a fresh-profile startup boundary for this host and copied binary. It does not prove that every supported client version is portable or that account, credential, root and shell effects after connection have been tested. The actual account/root stage remains unexecuted.

### Controlled normal shutdown and restoration

The [GUI normal quit path](https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/gui/main.cpp) and [application cleanup](https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/gui/application.cpp) were reviewed before the temporary stop. The original package identity was verified against its running process.

Direct execution of the installed Store executable returned AccessDenied. Sandboxed normal package activation then returned **0x80070490**, leaving the original running. The same exact, bounded [IApplicationActivationManager::ActivateApplication](https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nf-shobjidl_core-iapplicationactivationmanager-activateapplication) call with --quit and AO_NONE succeeded through normal host approval. The original exited normally; no forced termination or profile substitution was used.

An attempted fingerprint while that original process was still active encountered an access error in a cache file. It yielded no usable baseline and was discarded. The real preservation baseline was taken only after confirmed normal exit. A normal quit may flush settings; byte preservation is evaluated from that post-quit baseline until pre-resume, rather than falsely from a changing live file.

The probe created only previously absent ordinary application-data directories, a new no-account configuration and a workspace-owned empty root. The complete copied GUI reached SetupWizardController's ServerUrlState in its log. Supported show and visible-start attempts did not yield a targetable Computer Use window. Setup processes were normally quit between those entry attempts; none is represented as the same-PID W01/W02 experiment.

### Decisive desktop prerequisite

The final Computer Use launch request used the exact copied executable path. No usable launch outcome was obtained before the coordinated interruption. Subsequent calls must use supported timeouts/cancellation. Subsequent process inspection found no remaining OpenCloud test GUI. The Computer Use JavaScript kernel was reset to terminate stale execution; no further app input or unlock attempt followed.

A read-only WTSQuerySessionInformationW query for WTSInfoEx checked the returned level and session before interpreting SessionFlags. It returned **WTS_SESSIONSTATE_LOCK (0)**. [Microsoft documents this as locked](https://learn.microsoft.com/en-us/windows/win32/api/wtsapi32/ns-wtsapi32-wtsinfoex_level1_w) on the observed Windows version. Process/window inventory alone had been insufficient; MainWindowHandle 0 and a wizard log are not proof that no modal exists or that the desktop is usable.

The observed locked desktop is a concrete unmet execution prerequisite. The evidence does not attribute every earlier launch/window symptom solely to that lock or prove that unlocking will resolve all later setup steps. The owner must unlock Windows normally before a new bounded continuation can verify actual GUI operability. No password is requested in chat and no authentication or safety barrier is bypassed.

### Later unlocked-desktop readiness attempt

After the owner reported normal Windows unlock, a second bounded continuation checked the interactive session **before any client stop or backend start**. WTSInfoEx returned UNLOCKED. Normal original-package --show activation succeeded, and Computer Use list_windows returned the original OpenCloud status window. Read-only window inventory therefore worked; this alone did not prove that the screen could be captured or operated.

An accessibility-only get_window_state request, submitted with an explicit 20-second node-tool timeout, produced no usable state before coordinated interruption. The JavaScript kernel was reset before further actions. A fresh read-only session check still returned UNLOCKED and confirmed the original client remained running, without any probe listener.

A screenshot-only state request then returned the concrete error **“FrameArrived timed out: timed out waiting on channel”**. The one recovery attempt refreshed the returned window selection and requested supported window activation/capture; it returned **“window capture timed out: timed out waiting on channel”**. That error does not establish which recovery substep completed. These later calls used explicit node-tool timeouts and short-yield outer execution, so their responses could be monitored without leaving a background action behind a racing timeout.

Windows automation stopped at the skill's recovery boundary, and the JavaScript kernel was reset. A final read-only check still confirmed UNLOCKED, the original installed client running, no ordinary synthetic profile directories and no probe listeners. No backend, synthetic GUI profile, account/root, file or transfer was created in this second attempt. No restoration stop/resume was necessary because the ordinary client was never stopped.

This second attempt resolves the former locked-session prerequisite but exposes a separate **Computer Use capture failure**. It does not establish a defect in OpenCloud synchronization, an impossible native hold, a policy-activation result or a general failure of every desktop-control route. At that R2 checkpoint W01/W02 still required an operable supported observation/control surface. The later R3 accessibility/handoff route is recorded below; a screenshot is not the only supported observation.

### Observer and content-proof boundary

The unchanged observer described in the [historical CLI measurement](stock-windows-filter-probe.md#observation-and-quality-limits) was reused with fresh records. It captures complete Content-Length bodies before forwarding, including initial upload POST bodies, and does not log Authorization headers. Unsupported transfer framing or bodies beyond its bounded size invalidate a zero-content inference.

A later content run must establish a positive **GUI** upload and independent server readback, distinguish metadata XML from file-content bodies, inspect status/transport/framing errors and preserve the same real measured GUI PID/profile/root across hold and external-change cases. None of those GUI content controls ran here. Old CLI records cannot fill that gap.

### Later R3 accessibility and actual measurement

After the application restart, supported native accessibility returned usable current state without screenshot capture. Accessibility set_value changed visible non-sensitive fields; mouse geometry was unavailable and keyboard advancement was not observed. The owner performed the native button/radio/security actions, and Browser Use completed the synthetic localhost login. Only one Personal CFAPI root inside the admitted disposable directory was connected, with the exact automatic startup-value effect restored immediately.

The [separate GUI measurement report](stock-windows-gui-live-policy-probe.md) records positive small stock components: pre-established filtering held added/edited/nested unknown content while a permitted edit uploaded; external filter replacement then released held/new files without Apply or restart in the same GUI. Six initial content POSTs totaled 175 bytes with matching positive server readbacks. W01/W02 remain PARTIAL against the full oracles; the other twenty cases remain NOT RUN. A later Graph GET returned 401, followed by a successful refresh POST and successful Graph retries. The raw sequence join does not establish the cause or long-term authentication stability.

Physical Escape stopped the final accessibility read after the summary was written. **R3 restoration is PENDING.** A read-only host check at 16:37:36 UTC still found the same synthetic GUI, original two plus one synthetic registration, absent startup value, new normal profiles and active fixture helpers; the original client was stopped. None of the R1 completed-restoration statements below describes R3.

## Questions

The former observation prerequisite was satisfied in R3 by supported accessibility with explicit handoffs. Current open work is verified restoration, the integrated wizard/candidate/shared-policy contract, explicit effective revision and interruption/recovery, and broader rule/platform/VFS/update coverage. These do not reopen accepted product policy.

## Approved Strategy

No native integration, replacement workflow, topology or maintenance strategy is selected. The reviewed reversible fixture-entry route was used for R1 setup and later R3 component measurements. W01/W02 acceptance remains unchanged; a fresh profile, healthy backend or manual GUI settings alone cannot satisfy it.

## Expected Results

### Required protocol for continuation

| Step | Required evidence |
| --- | --- |
| Interactive desktop preflight | Before stopping the ordinary client, confirm read-only that the interactive Windows session is unlocked and that the next GUI actions have a supported observable accessibility/screenshot route or explicit human handoff. If locked, request normal owner unlock and do not launch the GUI. This is a harness prerequisite, not product behavior on Windows lock. Bound each Computer Use call to at most 60 seconds through supported timeout/cancellation; prove cancellation/kernel quiescence before restoration and never leave an action behind a Promise.race timeout. |
| Fresh isolated entry | Recheck current user/package/KnownFolder and original-profile preservation; do not overwrite retained synthetic quarantines. Confirm the actual graphical process, fresh account/root namespace and operable window before content. |
| Positive GUI control | Connect only the disposable account and ordinary synthetic root. Record an actual GUI upload including the initial content-bearing request, plus independent real-server readback. |
| W01 | Pre-establish the supported hold before newly added, edited and nested content enters the already-connected ordinary root. Observe live discovery and claimed transfer paths. Separate a stock ignore primitive from the requested MyBrain candidate/wizard/index. |
| W02 | Save a changed policy through a demonstrated external seam while the same measured GUI lives. Measure activation and transfer effect. Any manual GUI Apply/reload/rescan control is reported separately, not as external-controller proof. |
| Cleanup | Preserve synthetic raw evidence; normally stop only test GUI instances, remove only their admitted account/root effects, restore exact startup/profile metadata and resume the original client. Stop only owned fixture processes/listeners. |

### Recorded outcome

**Historical R1/R2 only.** The following outcomes retain their original attempt scope. Later R3 components and pending cleanup are reported above and in the separate measurement report.

| Case | Status | Actual evidence |
| --- | --- | --- |
| Real loopback backend/observer readiness | **Observed** | Successful initialization and status/Graph preflight; synthetic setup traffic only. |
| Fresh unpackaged no-account profile entry | **Observed** | Actual process/package/user/config/hash/root-set checks completed before account connection. |
| Operable connected GUI/root | **NOT ESTABLISHED** | First attempt confirmed a locked session. Later UNLOCKED preflight found the original status window but capture and its one recovery failed before any test fixture/client interruption. No account or sync root connected. |
| Positive GUI upload/readback | **NOT RUN** | No file control, content-bearing upload, readback or content-coverage measurement. |
| W01 — hold before first transfer | **NOT RUN — desktop/account/control prerequisites unmet** | No watcher/queue/VFS/content-hold result; neither PASS nor FAIL inferred. |
| W02 — external changed-policy activation while GUI runs | **NOT RUN — desktop/account/control prerequisites unmet** | No external activation or manual-Apply control result. |
| Other twenty integrated contract cases | **NOT RUN** | No additional policy/probe behavior executed by this attempt. |

### Completed restoration

**R1 only; R3 restoration remains pending.** No synthetic **GUI** account, GUI credential/Windows-keychain entry or Windows sync-root registration was created. The disposable server's separate synthetic administrator and app-token preparation remains local-only. The exact startup value and existing root set remained unchanged. Before resuming the original client, the protected Store file sets/digests matched the post-quit baseline. Only the two newly created ordinary synthetic profile directories were moved to their prechecked, absent host sibling quarantines; no protected Store profile was copied, moved or edited.

Normal original-package activation succeeded. Follow-up metadata confirmed the original packaged executable, expected existing account/root status and absence of a normal synthetic profile that could shadow it. Normal post-resume application writes are not claimed identical to the frozen pre-resume baseline.

The guest shut down normally. A PowerShell stop-cmdlet error left the two owned observer/bootstrap processes running; after repeating their exact process/command guards, only those owned processes were terminated. Final inspection found no owned fixture process and no listener on any reserved probe port. Unrelated processes and the resumed ordinary client remained running. The synthetic raw evidence and reviewed plan remain local-only for QA.

## Related Documents

- [Actual R3 graphical component measurements and cleanup status](<stock-windows-gui-live-policy-probe.md>)
- [Current behavioral W01/W02 contract](<synchronization-policy-and-probe-contract.md#current-behavioral-probe-contract>)
- [Canonical issue-9 research](<research.md>)
- [Historical stock CLI evidence, unchanged](<stock-windows-filter-probe.md>)
- [Native integration source assessment](<native-wizard-update-feasibility.md>)
- [Issue 9](<https://github.com/MikeyVK/MyBrain/issues/9>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-08 | Codex (@imp researcher) | Initial untracked entry-only draft: record official binary/source isolation investigation without content execution. |
| 1.1 | 2026-11-08 | Codex (@imp researcher) | Supersede the initial profile barrier with actual fresh unpackaged entry, real fixture preparation, locked-desktop finding and completed restoration; retain W01/W02 as NOT RUN. |
| 1.2 | 2026-11-08 | Codex (@imp researcher) | Retain the first locked attempt and restoration; add actual unlocked readiness/capture failures with no second client interruption or content execution. |
| 1.3 | 2026-11-08 | Codex (@imp researcher) | Preserve historical R1/R2 facts; link actual R3 accessibility/handoff and GUI components, initial HTTP attribution (corrected in 1.4) and pending restoration; remove image-only prerequisite. |
| 1.4 | 2026-11-08 | Codex (@imp researcher) | Correct QA's HTTP attribution finding: Graph GET 401, refresh POST and subsequent Graph GETs 200; preserve R1/R2 history and R3 pending restoration. |
