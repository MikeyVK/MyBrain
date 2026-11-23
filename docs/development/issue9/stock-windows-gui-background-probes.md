<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Stock Windows GUI background filter and running-work measurements

**Status:** RESEARCH MEASUREMENT — bounded background GUI components; owner-directed active retention
**Version:** 1.0
**Last Updated:** 2026-11-08

## Purpose

Record unattended synthetic background measurements without interfering with the owner's desktop.

## Scope In

The retained actual graphical Windows client, finite extension/folder/move fixtures, one bounded running-work retry, retention samples and a policy-only observation.

## Scope Out

No GUI input, browser/auth interaction, process restart/stop, new policy implementation, private content, strategy selection or phase exit.

## Problem Statement

R3 coupled external filter replacement with root activity and did not establish representative names, running propagation or a filter-only observation window.

## Goals

- Measure eligible actual GUI behavior through background fixture changes only.
- Distinguish complete-body timestamps, effective policy and observed retained copies.
- Preserve instrumentation failures and finite/full-contract limits.

## Background

R4 was separately owner-authorized after R3 active retention. Historical R1/R2/R3 findings and the corrected R3 HTTP sequence remain unchanged.

## Findings

### Scope and runtime

R4 continued the retained graphical Windows client documented in the [R3 report](stock-windows-gui-live-policy-probe.md#runtime-and-isolation): official OpenCloud 4.0.0.3642/9f701e, Qt 6.11.1, OpenSSL 3.6.3, Windows 10 build 19045; real OpenCloud 9.0.0 rolling in QEMU/Alpine. The executable, profile, account, journal and single ordinary Personal CFAPI root stayed the same. Read-only host checks at entry and 19:40:14 UTC matched the same sole GUI process and four loopback listeners. The served localhost certificate matched its retained source DER fingerprint and was valid.

The owner asked for independent background tests while using the PC. R4 used no Computer Use, keyboard/mouse, window activation, browser, authentication/security interaction, GUI Apply, process restart/stop or OS setting changes. Only declared synthetic subpaths and the disposable user filter were changed. No CLI synchronizer substituted for the actual GUI. Small materialized files were tested; placeholder, hydration and every-VFS-path behavior remain unestablished.

### Predeclared cases and parameters

The initial protocol preceded A/B; one B2 amendment followed the observed B1 instrumentation failure, and D was separately declared before its files. The fixture content ceiling was 32 MiB. Each batch offered 64 files of 65,536 bytes (4 MiB); two batches plus one late file and tiny controls stayed below 9 MiB of unique generated content. These counts, sizes and the 120-second D window are synthetic parameters, not product defaults.

| Case | Declared variation | Bounded result |
| --- | --- | --- |
| A | Filter extension, folder, nested file and excluded-source rename/move; matched and unmatched controls. | Positive finite filtering/release component; no general compiler claim. |
| B1 | Tighten policy on first observed batch upload. | Instrumentation failed before the filter change; cutover NOT ESTABLISHED. Its actual uploads remain evidence. |
| B2 | One sharing-safe retry, all files created before first observed upload, then exclude its directory. | Running propagation proved; admitted round continued, later file held; copies retained. |
| C | Missing/invalid/partial policy without focus-stealing or restart. | DEFERRED: nonmodal behavior not proved under the owner's no-interference constraint. |
| D | Release a held file by filter-only change, leave the root untouched for 120 seconds, then one control edit if still held. | No release in the fixed window; upload observed after the planned edit. |

### A: finite extension, folder and rename/move behavior

At 19:01:50.497 UTC the filter became exactly `*.r4hold\nr4-held-dir\n` (21 bytes, LF), before the five files in a unique connected-root subdirectory. Flat and nested allowed controls returned server 200 with exact bytes. Flat/nested .r4hold files and a child of r4-held-dir returned 404. Renaming an excluded flat source to another .r4hold name remained excluded/404.

The three never-uploaded excluded sources were then renamed/moved to permitted names: renamed.txt, nested/released.txt and moved-from-held-dir.txt. All three returned 200 with exact saved markers/hashes. Five complete file POST bodies totaled 142 bytes. The watcher logged the excluded paths. This covers these concrete extension/folder/nested names and movements, not arbitrary patterns, an automatic positive-rule compiler or moving an already-uploaded source.

### B1: failed trigger instrumentation

B1 created 64 files over about 19 seconds. Its reader used a sharing-incompatible live-log read and exited before changing the filter. The 64 actual content POSTs (S1195–1261, interspersed with other requests) all returned 201; independent first/last readbacks matched. Files were retained. Because no policy-change event occurred, this is not a running-work cutover result and no queue was inferred for files that did not yet exist.

### B2: running work and the observed boundary

B2 precomputed its 4 MiB payloads in memory and verified the sharing-safe reader before creating a fresh 64-file batch inside the connected root. Per-file creation records span 19:15:11.408–19:15:12.081 UTC. All 64 existed before the first captured file body, S1318 at 19:15:23.432.

At the 19:15:23.494 observation, S1318 and S1319 had complete captured bodies but no response records yet; a contemporaneous engine-log snapshot contained six concrete propagating/starting jobs. This establishes running work, not that all 64 were individually queued. The external filter write at **19:15:23.553 UTC** appended the exact directory line r4-b2-20261108 to A's two rules.

All 64 batch POSTs ultimately returned 201. **59 complete-body capture timestamps were after the filter write.** The observer samples time_ns after reading the complete request body and writing its body file, before forwarding; these are not first-byte or request-start timestamps. The filter write is not an acknowledged effective-revision boundary. The observation therefore describes continued admitted-round propagation, not a violation of a promised instantaneous cutover.

A subsequently added 65,536-byte late.bin returned 404 while a permitted outside control returned 200/exact. Earlier first/last batch files still matched both saved local hashes and independent server readbacks under the narrower policy. This supplies a bounded **P01 retention component**, not wizard cancel/defer, interruption/retry, placeholder, history or MyBrain-registration retention.

At 19:21:53.310 UTC the filter was restored to empty and the outside control edited. By 19:22:16.229 the late file and control returned 200/exact. No prior batch or server copy was deleted.

### D: policy-only observation versus a root change

D first established one allowed control (200/exact) and one held file (404), saving the held host hash before waiting. The client had finished its initial round before the filter-only write.

The only agent mutation at **19:27:30.6282219 UTC** was replacing the filter with an empty file. The fixed window ended at **19:29:30.6282219 UTC**. No agent root write, rename, touch or held-file read occurred during it. The independent observer recorded **15 requests, S1504–1518**, with no held-content body. The decoded native log contained no sync-start line in this window. It did show eight ignored Desktop.ini watcher lines; the app/OS therefore had its own root activity. Routine connectivity/authentication requests continued, including a successful refresh. This was not a disconnected-client inference.

The read-only polling tool timed out and reset its JavaScript kernel; the GUI, observer and backend were not reset. The declared window was reconstructed from the unchanged observer UTC records and BOM-aware UTF-16 native log. Later diagnostics extended elapsed wall time but did not extend that primary window. Using the exact original IPv4 request helper, the held path was still 404 and the control 200 before the single planned edit at **19:38:43.859 UTC**.

After that allowed control edit, S1580/S1581 captured complete new-control/held bodies at **19:38:58.293/19:38:58.297 UTC**, both 201. S1585/S1586 readbacks were 200; the held hash matched its prewait value and the new control bytes matched. Release followed the root-change control temporally. This finite observation does not prove that policy-only changes never reload, that this was the only possible trigger, or an acknowledgement/revision/latency guarantee.

### Complete-body evidence and gaps

The frozen R4 prefix is **S1105–1594**, joined by unique request/response sequence keys. It contains **489 indexed requests and 489 matching response records**:

| Evidence | Count or bytes |
| --- | --- |
| Methods | 275 GET, 53 PROPFIND, 14 MKCOL, 147 POST |
| Responses | 255 HTTP 200, 153 HTTP 201, 53 HTTP 207, 10 HTTP 401, 18 HTTP 404 |
| Marker-matched content POSTs | 139, totaling 8,454,432 bytes; all indexed responses 201 |
| Other POSTs | Eight token-refresh forms, totaling 11,776 bytes; all 200 |
| PROPFIND metadata | 13,844 bytes; not file content |
| Indexed length mismatches, framing/transport errors, unmatched responses | Zero in the indexed records |

**Coverage is incomplete at S1178:** a zero-byte body file exists without request or response rows near the B1 sharing failure. Its method, endpoint and outcome were not inferred. Thus the whole R4 interval does not support an exhaustive zero-content/zero-error claim. The decisive A, B2 and D intervals have indexed body and response evidence, with separate positive controls/readbacks. No PUT, PATCH or DELETE appears in the indexed prefix.

The unchanged observer SHA256 is **A0F9E6B755CF9AB05345617399FDE235A3637743A9C939E5B757D26C5A00E118**. It records complete Content-Length bodies before forwarding and rejects unsupported Transfer-Encoding or bodies over 16 MiB; these 64 KiB files do not establish every chunked/TUS/large-file route. A received complete body proves its bytes had reached the observer by capture time, not when its first byte left the client.

Ten GET responses were 401 (Graph/notifications); eight later refresh POSTs were 200. The final example is S1588 Graph GET 401, S1592 refresh POST 200, S1593/S1594 Graph GET 200. Causes and long-term authentication stability remain unproved. Raw forms stay private. Normal refresh is distinct from interrupted policy-activation recovery.

### Instrumentation qualifications and evidence index

B1's sharing failure, the empty unindexed S1178 body, the initial wrong UTF-8 log decode, a corrected timestamp-width parser and the D polling timeout are retained in local evidence. After the kernel reset, an initial re-created localhost readback helper returned misleading 404s; those diagnostic negatives are excluded. The exact original IPv4/agent:false helper and recorded personal-space route recovered 200/exact controls before interpreting D. No credentials were created or repaired.

Ignored/local-only evidence is indexed by the existing R3 evidence-index.json under its R4 section. The R4 directory retains protocol.json, protocol-b2-amendment.json, protocol-d.json, per-case manifests/events/readbacks, measurement-summary.json, decoded/superseded diagnostic records and final-retained-readiness.json. Original capture files and R1/R2/R3 reports remain preserved. Host identities, paths, root/account IDs, secret forms and credentials are not publishable attachments.

### Current coverage and operational disposition

W01, W02 and P01 are **PARTIAL** against their full unchanged oracles; their bounded measured components above are positive. The other **nineteen** behavioral cases remain NOT RUN. B2 supplies actual running propagation evidence but not all accepted finalization choices, effective-policy acknowledgement or interruption/recovery. C remains deferred; wizard/group/shared-device/prototype-dependent cases remain unmeasured.

The final policy is the known functioning empty filter with successful control/readbacks. The same GUI/account/root/profile/journal, all fixture files, QEMU/backend, observer and bootstrap remain **OWNER-DIRECTED ACTIVE RETENTION**; the ordinary Store client remains stopped. No cleanup, unregister, stop/start or power/autostart change was performed. The backend remains RAM-only on tmpfs without a writable QEMU disk: host restart or QEMU shutdown loses backend state. Durable preservation remains separate future work.

## Questions

- Establish explicit revision acknowledgement, activation/finalization choices and interruption/recovery before full W02 acceptance.
- Establish the native wizard/shared policy and full retention/history behavior before full W01/P01 acceptance.
- Scope durable backend preservation separately; current retention is RAM-only.

## Approved Strategy

No integration, fork, rule compiler, replacement topology or maintenance strategy is selected. These are bounded Research measurements only.

## Expected Results

W01/W02/P01 remain PARTIAL; other nineteen cases NOT RUN. Leave the known empty test filter and existing active fixture intact; independent revision-bound QA and strategy approval remain separate.

## Related Documents

- [Canonical Research](<research.md>)
- [Current unchanged behavioral oracles](<synchronization-policy-and-probe-contract.md>)
- [Earlier R3 GUI measurements](<stock-windows-gui-live-policy-probe.md>)
- [Historical isolation and retention](<windows-gui-probe-isolation-assessment.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-08 | Codex (@imp researcher) | Record R4 finite filtering, B1 failure/B2 running-work boundary and retention, fixed-window D activation observation, complete indexed body accounting and coverage gap. |
