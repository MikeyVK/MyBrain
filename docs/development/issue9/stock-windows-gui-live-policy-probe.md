<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Stock Windows GUI hold and live external filter measurement

**Status:** RESEARCH MEASUREMENT — bounded GUI components observed; cleanup and independent review pending
**Version:** 1.0
**Last Updated:** 2026-11-08

## Purpose

Record the actual owner-requested graphical W01/W02 component measurements, complete body/readback evidence and their limits.

## Scope In

One unchanged stock Windows GUI, one fresh synthetic localhost account, one ordinary connected CFAPI root, a pre-established finite filter, and its external live change.

## Scope Out

No integrated native MyBrain wizard, shared device policy, interruption/recovery, private accounts or files, production infrastructure, client patch, strategy selection, phase exit or completed restoration claim.

## Problem Statement

Earlier CLI batches and GUI preparation did not prove a persistent graphical client's hold or an external policy change while that client remained alive.

## Goals

- Distinguish measured stock GUI components from the full W01/W02 behavioral contracts.
- Retain exact request-body and independent server-readback evidence without publishing private runtime material.
- Keep incomplete cleanup, authentication failure and remaining coverage visible.

## Background

The owner requested the first two graphical Windows probes on 2026-11-08. R1/R2 setup and readiness history remains in the isolation assessment. R3 proceeded through supported accessibility observation and human native-button/security handoffs.

## Findings

### Bounded result

| Contract case | Observed component | Current classification |
| --- | --- | --- |
| W01 | A pre-established stock filter held newly added flat/nested files and an edit to the held flat file inside an already-connected ordinary root. A permitted edit uploaded in the same interval. | **PARTIAL** for the full case; positive evidence for this finite stock-filter component. |
| W02 | Replacing the user filter externally while the same graphical client stayed alive released held and newly added files, with complete initial upload bodies and matching server readbacks. | **PARTIAL** for the full case; positive evidence for this local external-file activation component. |

No native MyBrain decision wizard, shared candidate/location index, central device policy, effective-revision acknowledgement, interrupted activation, uncertain-transition hold, recovery, arbitrary rule compiler or upgrade contract was established. The other twenty behavioral cases remain NOT RUN.

### Runtime and isolation

The complete unchanged official Windows GUI was OpenCloud **4.0.0.3642**, commit **9f701e**, Qt **6.11.1**, OpenSSL **3.6.3**, on Windows 10 build **19045**. Its executable SHA256 was **AA621347CFFF26D8E69DC96D8A73C75279A8BFA7F6E860E4C0AF390A7F30ECC8**. No plugin was removed or patched. The real disposable server was OpenCloud **9.0.0 rolling** in retained QEMU/Alpine, with 1536 MiB guest RAM and two CPUs; listeners were loopback-only, without host mounts or bridging.

After the original Store client quit normally, actual-process checks established sole unpackaged execution (package query 15700), the same host user, zero restored accounts/roots, protected Store-file digest preservation and unchanged existing sync roots. Only a fresh synthetic localhost account was connected. Its first-account startup entry was restored immediately to the original absent state.

Manual synchronization setup selected only Personal. The stock wizard appended a Personal child directory within the admitted disposable root. The actual configuration and new CFAPI registration both resolved there; the two original registrations remained present. The recorded mode was **cfapi**, with one journal and one root. Desktop.ini and the synchronization log were generated locally. The test files were small materialized local files; no explicit dehydration, remote hydration or all-VFS coverage follows.

### Supported GUI operation and human assistance

Native accessibility observation worked without screenshots. Accessibility set_value visibly changed the server/root fields. A click reported coordinate input geometry is unavailable; keyboard input did not produce observed advancement. The owner therefore performed the necessary native wizard button/radio actions. Browser Use completed the ordinary synthetic localhost login and consent through the graphical client's actual callback flow.

The retained expired fixture certificate was rejected by the owner. A new certificate was generated only for the owned observer, in new scratch paths and a fresh capture segment; its source and served DER fingerprints matched and its validity covered the run. The owner accepted the renewed app-scoped test warning. No global certificate store or security setting was changed. A first automatic approval review rejected initializing the ordinary-path filter; read-only host/SID, post-baseline creation, empty-file, fresh-account and protected-profile evidence established that it was the new disposable profile, and a guarded retry was approved. Personal credentials were not read or used.

Thus a supported observable accessibility surface plus explicit human handoffs was sufficient for this run. The historical screenshot failures remain true; an image-only prerequisite would incorrectly exclude the observed working route.

### Declared fixtures and filter

All contents below are literal UTF-8/ASCII without a final newline. The policy before account/root connection was the byte-exact finite a.txt complement in the [CLI report](stock-windows-filter-probe.md#exact-filter-states). It permits that flat filename while excluding the other tested names and parent directory. This is a manually declared finite fixture, not a general positive-policy compiler.

| File/state | Bytes | Marker |
| --- | --- | --- |
| a.txt, first control | 26 | I9-GUI-CONTROL-20261108-R3 |
| a.txt, active hold control | 31 | I9-GUI-LIVE-CONTROL-20261108-R3 |
| unknown.txt, added under hold | 26 | I9-GUI-UNKNOWN-20261108-R3 |
| unknown.txt, edited under hold | 31 | I9-GUI-UNKNOWN-EDIT-20261108-R3 |
| nested/unseen.txt | 25 | I9-GUI-NESTED-20261108-R3 |
| a.txt, external-change control | 35 | I9-GUI-EXTERNAL-CONTROL-20261108-R3 |
| external-release.txt, added after change | 27 | I9-GUI-EXTERNAL-20261108-R3 |

The initial protocol was revised before any declared content to use the reviewed a.txt complement and then to record the wizard's actual Personal child. Before the hold interval, an allowed edit was declared as the live control. Before external mutation, the empty-filter change, new unknown and allowed-edit markers were recorded. All cases used the same GUI entry, account, root and journal; no CLI batch, restart, outside-root staging or manual Apply substituted for activation.

### Recorded sequence and results

S identifies the renewed-observer capture segment. UTC times below are measurement facts, not product deadlines.

| Stage | Requests | File-content evidence | Independent result |
| --- | --- | --- | --- |
| C00, S77–85; began 16:25:48.977 | 9: 6 GET, 2 PROPFIND, 1 POST | S78 initial POST contained the complete 26-byte first control. | Server GET returned 200 with the exact marker/hash. |
| W01 component, S86–96; 16:26:39.491–16:27:46.343 | 11: 8 GET, 2 PROPFIND, 1 POST | S87 contained only the complete 31-byte permitted control edit. No tested held marker appeared in any captured request body. | Permitted edit GET 200 and exact bytes; flat/nested held paths GET 404. Both held local contents remained. |
| W02 component, S97–127; external write 16:27:50.975, capture ended 16:29:57.028 | 31: 21 GET, 4 PROPFIND, 1 MKCOL, 5 POST | S100/S101/S102/S104 contained complete bodies of 35/27/31/25 bytes: permitted control, new unknown, edited held unknown and held nested file. | Four server GETs returned 200 with exact corresponding markers. |

During W01 the live watcher logged ignored flat/nested paths; discovery/propagation reported them Excluded. Two sync rounds completed successfully while the permitted edit transferred. The hold observation lasted about 67 seconds; it was not inferred from a disconnected or idle client.

W02 changed only the synthetic user filter from the complement to an empty file through an external guarded filesystem write. Ordinary local file changes stimulated discovery. The first resulting sync completed at **16:28:09.144 UTC**, about **18.17 seconds** after the external write. No GUI Apply or restart occurred. This establishes observed effective behavior for that local-file seam; it does not establish an explicit policy revision protocol, a stable external control API or instantaneous/race-safe activation.

At **16:29:34.779 UTC**, later in the W02 capture, a **POST /konnect/v1/token** with refresh_token grant returned **401**. Its 1472-byte body was authentication data, not file content; raw values remain private scratch. This later failure does not undo earlier exact upload/readback observations, but sustained authentication and any later round success are not claimed. Its cause was not investigated or repaired in this bounded measurement.

### Complete-body coverage and limits

Across S77–127 there were **51 requests**: 35 GET, 8 PROPFIND, 1 MKCOL and 7 POST. Six POSTs contained file content, totaling **175 bytes**. The remaining POST was the 1472-byte token-refresh form. Eight PROPFIND XML bodies totaled **2211 bytes**; metadata bodies are not file content. No PATCH, PUT or DELETE occurred in this interval. Status totals were 33 HTTP 200, 7 HTTP 201, 8 HTTP 207, 2 intentional readback 404 and 1 token-refresh 401.

The observer captured each Content-Length body before forwarding. Declared/observed lengths matched, and every measured request had a response record; there were zero recorded framing, incomplete-body or transport errors. The unchanged observer source SHA256 was **A0F9E6B755CF9AB05345617399FDE235A3637743A9C939E5B757D26C5A00E118**. Its [documented limit](stock-windows-filter-probe.md#observation-and-quality-limits) rejects Transfer-Encoding and bodies above 16 MiB; unobserved/unsupported routes would invalidate a zero-content claim. No general chunked/TUS-mode or large-file coverage follows from these six small initial POSTs.

The server readbacks are independent of local file existence and GUI success text. Six positive readbacks matched their markers; the two W01 absence checks returned 404. The observer does not retain all upload headers, and this run does not exhaustively trace OS file access or every possible preview/analysis route.

### Interruption and restoration status

After the summary and W02-end record were written, the final native accessibility read reported a physical Escape stop. No later GUI automation was issued in that turn. The measurements above had already completed. That final GUI snapshot did not complete.

**Cleanup/restoration is PENDING at this document checkpoint.** The last verified runtime still had the synthetic GUI/account/root and fixture processes active, with the original client stopped. Account/credential/root cleanup, preservation of closed journals, quarantine of the new normal profile, protected Store pre-resume verification, original package resumption and fixture shutdown are not yet verified. A read-only host check at **16:37:36 UTC** confirmed the same sole synthetic GUI, original two plus one synthetic registration, absent OpenCloud startup value, new normal profile parents and the three known fixture helpers still active; the original packaged GUI was absent. A later explicitly authorized cleanup continuation must record its actual outcome. This report does not claim a restored host or completed review.

Raw journals, captures, protocol versions, readbacks, synthetic credentials and host-specific preservation metadata remain ignored/local-only. The local evidence index retains the fresh-entry checkpoint and now indexes measurement-summary.json, measurement-stages.jsonl, per-case/readback artifacts and the explicit pending-cleanup snapshot. Neither raw credentials nor machine/account/root identities belong in Git, issue text or attachments.

## Questions

- Complete the explicitly authorized restoration and verify its actual outcome.
- Determine explicit effective-revision, uncertain-activation, interruption/recovery and maintained integration/update contracts before claiming full W02 or selecting a strategy.
- Establish the integrated candidate/wizard/MyBrain behavior and broader platform/VFS/rule coverage before claiming full W01.

## Approved Strategy

No native integration, fork, replacement workflow or maintenance strategy is selected. The two bounded stock components provide Research evidence only; independent review and affected strategy approval remain necessary before Design.

## Expected Results

W01 and W02 remain PARTIAL against the full current behavioral contract. Their recorded small stock components have positive runtime evidence. The other twenty cases remain NOT RUN. Cleanup and independent review are pending.

## Related Documents

- [Canonical issue-9 research](<research.md>)
- [Current behavioral probe contract](<synchronization-policy-and-probe-contract.md>)
- [Historical GUI setup and isolation](<windows-gui-probe-isolation-assessment.md>)
- [Historical stock CLI measurement](<stock-windows-filter-probe.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-08 | Codex (@imp researcher) | Record actual stock GUI hold/external activation, complete body/readback counts, late authentication failure and pending restoration without claiming full W01/W02. |
