<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Stock Windows batch client filter probe

**Status:** RESEARCH MEASUREMENT — stock CLI component; GUI, queued-job and shared-policy guarantees unproved  
**Version:** 1.0  
**Last Updated:** 2026-11-05

## Purpose

Measure whether an unchanged OpenCloud Windows synchronization engine can hold unknown content and apply a narrow permitted scope before upload, without modifying the personal client or a production server.

## Scope In

One synthetic local root and the same disposable server Space across batch invocations; explicit stock exclude files; actual outgoing upload bodies; startup reload, endpoint unavailability and retained copies.

## Scope Out

No live NAS, private content/accounts, personal sync configuration, host network/VPN change, global installation, client patch, native wizard, device distribution, server-policy reconciliation, GUI watcher/CFAPI or upgrade proof.

## Summary

The stock CLI held the tested unknown files under a pre-established catch-all exclusion. Gitignore-style !a.txt did not override it. A small manually written complement of the exact filename a.txt did permit only that file while the tested other and later unknown files remained local. Thus absent inclusion syntax does **not** prove that every positive policy projection is impossible.

Two actual upload POST bodies each contained the complete 19-byte control/allowed file, and independent server readbacks matched their hashes. Replacing the policy while the test endpoint was unavailable, then starting a fresh batch after reconnect, prevented the edited file from uploading. A missing explicit filter file caused startup abort before file-content upload.

These are bounded batch-engine results. No persistent GUI job was shown to be queued while offline, so queued-job cancellation remains unproved. No integrated wizard, live GUI reload or shared local/server policy reconciliation has been implemented or tested.

## Runtime identity and isolation

| Component | Observed identity |
| --- | --- |
| Windows client | Official Store payload copied with its program layout; actual --version reports OpenCloud 4.0.0.3642, source 9f701e6db2e101cb3247d3331647a60266e83b0f, Qt 6.11.1, OpenSSL 3.6.3, Windows 10 x86_64. Copied CLI and synchronization DLL hashes match the original payload. |
| Server | Actual OpenCloud 9.0.0 rolling executable inside the guest; version output, HTTPS status productversion and guest binary hash observed. The status API also has a compatibility version field; it was not mistaken for productversion. |
| Guest | Alpine virt 3.24.4, Linux 6.18.60-0-virt; QEMU 11.1.0, build v11.1.0-12130-ge470268ff4; TCG software emulation, two guest CPUs, 1536 MiB RAM. |
| Network/filesystem | No host filesystem mount or bridged network. Guest NAT for bootstrap; serial and all host listeners/forwarding bound to 127.0.0.1. Only synthetic server/account/root used. No host virtualization feature or global service installed. |
| Observer | Fixture-only Python 3.13 HTTPS relay; records Content-Length request bodies before forwarding to the real server. Source retained in ignored scratch, SHA256 A0F9E6B755CF9AB05345617399FDE235A3637743A9C939E5B757D26C5A00E118. |

Material identities:

| Artifact | Verified digest |
| --- | --- |
| opencloudcmd.exe | SHA256 A42D911EF61389A838BF3F85660F248EDACE468FD00920D7FE2E1345291B41F4 |
| OpenCloudLibSync.dll | SHA256 6B3A3EB192843C26AF5119DC78F8428F4EDB13C3D219D4A0ADF9D45868B48F21 |
| Official server 9.0.0 Linux amd64, 141766584 bytes | SHA256 2944B956461107CF8D73424C3602D83AC157988E28DC6CE95370C45633DE45C4 |
| Alpine virt 3.24.4 ISO, 70254592 bytes | SHA256 157D353F8E54252CAD2D9812A0D56BB7FA2231FC154A110E1D180D7480EF8B4F |
| Portable PeaZip 11.4.0 ZIP | SHA256 892426473D70E88738C869B336DD06534F84B7EEEC3374494514E7EE32B3B833 |

The QEMU package matched the publisher's [SHA512](https://qemu.weilnetz.de/w64/qemu-w64-setup-20260811.sha512). [QEMU's download page](https://www.qemu.org/download/#windows) links the Windows builder; its NSIS installer was extracted with the portable PeaZip 7z backend and **never executed**. [PeaZip's portable release](https://github.com/peazip/PeaZip/releases/tag/11.4.0), the [Alpine release directory](https://dl-cdn.alpinelinux.org/alpine/v3.24/releases/x86_64/) and [official OpenCloud release](https://github.com/opencloud-eu/opencloud/releases/tag/v9.0.0) identify the acquired artifacts. No claim of latest installed or general version compatibility follows.

Initial sandbox inventory could not see the real package. Outside-sandbox read-only metadata corrected that finding. Direct execution from the installed package path did not establish a usable invocation; its identified probe process was stopped. The unchanged complete program copy ran help/version and the batches successfully. No startup-hang diagnosis was established. Guest startup initially lacked a loopback address; configuring **guest** lo resolved its explicit bind error. These are setup observations, not product filter failures.

## Recorded protocol and reproduction boundary

The control/hold/allow/offline/retraction oracles and finite-pattern fixture were recorded before content tests. The missing-explicit-filter startup case was added as a separately identifiable case before executing it.

1. Use the verified full client program layout and a fresh synthetic root, plus the real disposable server. Keep the same root, Space and journal across the batches; no outside-root staging or root swap is substituted.
2. Boot the verified guest with the ISO kernel/initramfs and readonly ISO. The actual host bindings were serial 127.0.0.1:22320, artifact-only bootstrap HTTP 127.0.0.1:18080, backend 127.0.0.1:19201 forwarded to guest 19200, and observer HTTPS 127.0.0.1:19200. No host paths are mounted in the guest.
3. Initialize the real server with a fresh synthetic admin password. Runtime settings were OC_URL=https://localhost:19200, PROXY_HTTP_ADDR=0.0.0.0:19200, OC_INSECURE=true, PROXY_ENABLE_BASIC_AUTH=true, GOMEMLIMIT=768MiB and GOMAXPROCS=2. Use the normal full server stack. Obtain a one-hour app token through /auth-app/tokens?expiry=1h and verify a Graph read. Tokens/passwords are not published.
4. Keep advertised localhost:19200 reachable inside the guest for issuer/self-discovery. The host observer uses its own fixture-generated self-signed certificate and forwards HTTPS to the loopback backend. Certificate acceptance is scoped to the synthetic fixture; no global trust store or production TLS is changed.
5. Record request bodies before forwarding, then run each batch with its explicit filter path and synthetic token in the child environment. Retain stderr, exit status, policy text, request sequences and independent content readbacks. The tested CLI shape was:

```text
OPENCLOUD_TOKEN=<one-hour synthetic app token>
opencloudcmd.exe --user admin --exclude <explicit-policy-file> --non-interactive --trust --verbose 0 https://localhost:19200 <synthetic-space-id> <same-synthetic-root>
```

The inspected [CLI source](https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/cmd/cmd.cpp) checks server status, OCS capabilities and Graph Spaces before the engine starts. Bare WebDAV was not substituted. It creates a fresh account for each batch; this is not the persistent GUI connection. No --confdir/--multiple isolation flag was assumed. Existing preferences may be read, and fresh UUID cache/crash artifacts can be created outside the synthetic root; total filesystem confinement was not proved. The inspected CLI path does not restore a GUI account or request its keychain credentials; this is a source-bound distinction, not exhaustive OS file-access tracing.

## Exact fixture contents

Each content is the literal ASCII/UTF-8 marker below, **without a terminal newline**. All names and contents are synthetic.

| File/state | Bytes | Literal content | SHA256 |
| --- | --- | --- | --- |
| control.txt | 19 | I9-CONTROL-20261105 | 3C82648E19063E4EC916B40EE7904E156E39D602C2EFF173CB18568E21772F32 |
| a.txt, initially permitted | 19 | I9-ALLOWED-20261105 | 3FE5BC79DEB417D129C6FAC05E03103DF4FC3DB568249F38E873254023E06D3A |
| a.txt, edited offline | 21 | I9-A-OFFLINE-20261105 | 0E1BADFFB3442D1FB7E500C7564BB87B0118283A19B9AEE7A48AFBD98E64C4DD |
| unknown.txt | 19 | I9-UNKNOWN-20261105 | F722D0A2D367CABB405E6AC348F8F124BBB981223EA21DDF9B82251E5598464A |
| newdir/unseen.txt | 18 | I9-NESTED-20261105 | 1CC8E30588951865E91BB14104F599195EA859BF8473D6283D5142C0CB40D799 |
| later.txt | 17 | I9-LATER-20261105 | 9454296095CAE315D8D59A1E8212CF34097271166B66D49EE57F246E05EA9C42 |
| another-dir/a.txt | 24 | I9-LATER-NESTED-20261105 | D72C4125FA2F8E4BF5402E015212F5002440ADE3741F634828F1C21781E60246 |
| missing-policy.txt | 26 | I9-MISSING-POLICY-20261105 | 9D5C8E4187034EF2FD86009558ECA8FB576CCB9149A36CE2246A39AEAFF02B19 |

## Exact filter states

The control used an empty file. The unknown hold used a single * line. The Gitignore-style counterexample used * and !a.txt on separate lines. The finite exact-filename counter-hypothesis used:

```text
[!a]*
a[!.]*
a.[!t]*
a.t[!x]*
a.tx[!t]*
a.txt?*
a
a.
a.t
a.tx
a.txt/
```

The [exclude implementation](https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/libsync/csync_exclude.cpp) OR-combines exclusions and translates bracket [!...] as a negated character class; it does not implement leading ! as a Gitignore inclusion override. The [header](https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/libsync/csync_exclude.h) separates exclusion filtering from selective-sync blacklists.

The finite fixture is not a general compiler, folder policy language or proof for arbitrary names, Unicode, many allowed paths, VFS or concurrent rule edits. It permits the exact flat filename a.txt in this test; the excluded parent prevents another-dir/a.txt from inheriting that permission. Generated broader projections remain a research question.

## Observed results

M and R identify the main and restarted-observer capture sequences. HTTP counts exclude separate readback GETs.

| Case | CLI exit / observed HTTP requests | Observed file-content upload | Bounded interpretation |
| --- | --- | --- | --- |
| 01 Control, empty excludes; M1–5 | 0 / 5 | POST body 19 bytes, exact control marker; server readback hash matches. | Observer detects actual content in the initial upload request, not only final storage. |
| 02 Pre-established * before adding a.txt, unknown.txt and newdir/unseen.txt; M7–10 | 0 / 4 | No POST/PATCH/PUT content request. | Stock batch held these unknowns inside the same root. |
| 03 * plus !a.txt; M11–14 | 0 / 4 | No content upload. | Leading ! did not override catch-all. This alone is not impossibility of every positive projection. |
| 04 Finite exact complement; M15–19 | 0 / 5 | POST body 19 bytes, exact initial a.txt marker only; readback hash matches. | Narrow stock-pattern permission worked for this fixture. |
| 05 Later later.txt and another-dir/a.txt under the existing complement; M21–24 | 0 / 4 | No content upload. | These new unknowns stayed local on the next batch scan. No autonomous watcher claim. |
| 06 Test observer stopped; a.txt edited and * saved locally; fresh offline batch | 1 / no receiving observer | Connection refused during preflight. | Server backend stayed healthy. No engine queue was established; not queued-job evidence. |
| 07 Observer restarted, then fresh batch with saved *; R1–4 | 0 / 4 | No content upload. | Explicit filter reread at batch start kept the edited local a.txt from replacing the retained server version. No automatic reconciliation claim. |
| 08 Deliberately absent explicit --exclude path, fresh missing-policy.txt; R7–9 | 1 / 3 | No content upload; “Cannot load system exclude list or list supplied via --exclude”. | Narrow startup abort for a missing explicit filter file; not general shared-policy outage behavior. |
| Retract an already queued persistent GUI upload | NOT ESTABLISHED | No qualifying engine queue observed. | Remains unproved; a file waiting on disk is not that queue. |

Separate readbacks were M6, M20 and R5–6. Across those 33 captured requests there were two file-content POST bodies totaling 38 bytes, zero PATCH/PUT and zero DELETE requests. Six 290-byte PROPFIND XML bodies were metadata; zero **file content** does not mean zero HTTP body bytes. Captured declared and actual lengths matched; no observer framing/transport/status error was recorded in these measured requests.

Before guest teardown, control.txt and the original server a.txt still matched their earlier readback hashes; the local a.txt retained its 21-byte offline edit. All seven final named local fixture files remained. Policy narrowing did not delete those copies.

## Observation and quality limits

The observer logs method/path, sequence, body byte count, declared length, digest and raw synthetic body before forwarding; Authorization headers are not logged. It also records partial Content-Length bodies as an observation error. Unsupported Transfer-Encoding returns 501; oversized (>16 MiB), invalid or otherwise unobserved framing is not complete body evidence. Such cases must yield insufficient evidence, not a positive zero-byte conclusion. None occurred in these small measured uploads. Protocol-specific upload headers were not retained; the directly observed claim is the complete file body in the initial POST, not all possible TUS modes or native routes.

Temporary observer source/raw captures stay ignored locally; its SHA256 above identifies the source supplied for independent review. Native enforce scaffolding was blocked by the unrelated e-Boekhouden syntax adapter as unavailable/unsupported_input. The README's diagnostic/setup report-mode exception persisted this fixture-only script with that result still unavailable. Python 3.13 interpreter syntax compilation exited 0, and the real control/readback exercised it. This does not activate application checks or establish production quality. The committed report preserves the screened protocol/results, not a turnkey portable instrumentation package.

Successful batches emitted a system-time-zone warning. Expected failed preflight/filter startup also emitted a QWaitCondition shutdown warning. These were preserved in local diagnostics, not converted into synchronization success or suppressed as quality evidence.

## Cleanup and open work

The exact probe-owned observer, bootstrap HTTP server and QEMU processes were stopped after identity checks. All four probe loopback ports were checked closed; no known probe process remained. Raw synthetic records, copied tools, observer source, fixtures and logs remain in ignored local scratch for independent review. The RAM-only server ended with its guest; no production data was touched and no host trust/network/virtualization setting changed. Possible fresh UUID cache/crash artifacts outside scratch were not exhaustively inventoried or deleted; shared personal cache parents were not cleaned.

Still unproved: the integrated native wizard/MyBrain decision, persistent connected-folder GUI behavior, GUI-triggered live exclude reload, cancellation/re-evaluation of a truly queued upload, snapshot races, broad filter compilation, client/device policy exchange and conflicts, capabilities/availability, cross-device/mobile behavior and update preservation. Source storage/lifecycle principles P18/P19/P38 are unchanged. No patch, integration strategy, merge algorithm or phase transition follows automatically from this result.

## Related Documents

- [Canonical issue-9 research](<research.md>)
- [Offline and reconciliation contract](<research.md#offline-and-reconciliation-probe-contract>)
- [Native integration and update assessment](<native-wizard-update-feasibility.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-05 | Codex (@imp researcher) | Record the authorized stock CLI protocol, measured body/retention results, missing-filter startup behavior and explicitly unproved GUI/queue/shared-policy boundaries. |
