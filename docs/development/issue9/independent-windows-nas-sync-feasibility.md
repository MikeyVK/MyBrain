<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Independent Windows synchronization client and NAS service feasibility

**Status:** Research checkpoint — no architecture choice; independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-11-13

## Purpose

Compare an independently owned synchronization path with adapting OpenCloud under the accepted issue 9 behavior and open-source boundary.

## Scope In

Windows-first synchronization admission, policy, client/service responsibilities, reusable OSS building blocks, maintenance and NAS resources.

## Scope Out

No installation, runtime experiments, production data or NAS access, implementation, strategy selection or research phase transition.

## Problem Statement

The accepted pre-transfer and integrated policy behavior is not yet proven by OpenCloud's existing clients; building an independent path offers control but transfers responsibility for synchronization correctness and ongoing maintenance.

## Goals

- Compare equivalent end-user behavior across alternatives.
- Identify possible open-source building blocks and unresolved dependency and integration boundaries.
- State a bounded synthetic discriminating proof.

## Findings

### Scope and evidence

The owner requested a feasibility comparison on 2026-11-13: an independently developed Windows client and NAS service, using open-source applications, libraries and services, versus adapting OpenCloud. Windows and DSM are accepted hosts; closed third-party application runtimes and services are not. [Sovereignty research](../../research/public/opencloud-sovereignty-and-dependency-audit.md) specifies the source, build and deployment audit boundary. This is research, not a selected architecture, build authorization, implementation schedule or claim of production readiness.

The issue's [accepted behavior and probe contract](synchronization-policy-and-probe-contract.md) remains authoritative: one integrated wizard including an independent MyBrain intake choice; local/cloud retention; device groups and visible exceptions; local and shared offline policy and reconciliation; all-action bulk safeguards; one active management endpoint; last-known location visibility; no whole-device crawl; hold undecided content before transfer. Only consciously connected roots are included. Discovering candidate metadata does not register a MyBrain source or authorize content transfer.

Source inspection is dated 2026-11-13. The [Windows candidate comparison](windows-sync-candidate-comparison.md) records Syncthing v2.1.7 and rclone v1.75.2; the [native integration assessment](native-wizard-update-feasibility.md) records OpenCloud Desktop v4.0.0. These snapshots are not a verified interoperable stack. The [stock GUI measurements](stock-windows-gui-live-policy-probe.md) demonstrate bounded filtering and external policy change while running, not the full integrated policy, transaction safety, wizard or all transfer paths.

### Feasibility conclusion

An own Windows client and NAS service are technically plausible using existing open-source building blocks and accepted operating-system APIs. The decisive potential advantage is ownership of the point before upload begins. This is an inference, not a measured guarantee. It also makes MyBrain responsible for synchronization correctness, security, updates and recovery. A first gating probe can be small; a trustworthy synchronization product is substantially larger. No evidence yet shows that the complete desired product is faster, cheaper or safer to build independently.

The comparable alternatives are:

| Boundary | Adapt OpenCloud plus own policy service | Own client and NAS service | Own policy/UI with a separate existing engine |
| --- | --- | --- | --- |
| First-byte enforcement | Modify and test all relevant internal upload paths, or prove an alternate race-free seam. Existing filtering tests do not prove a universal gate. | Build a controlled transfer executor, reject unknown work by default and verify identity/content before every path. Direct control, not yet implemented or proved. | Prove that the engine cannot bypass a default hold during initial scan, live changes, reconnect, retry, rename or restart. If it can, patch it or reject the route. A separate UI or ignore list is insufficient. |
| Wizard, groups, offline policy | Own policy and wizard still needed. Integrate desktop and later mobile flows; maintain modifications against upstream. | Native Windows host and policy implementation are owned. Equivalent Android/iOS experiences and their platform restrictions remain future work. | Own wizard and controller required. Existing device/folder management is not the accepted group and per-file policy. |
| File transfer, versions and recovery | Reuse existing sync/server behavior subject to verification; preserve version, conflict and delete behavior in the modified build. | Supply or adapt bidirectional transfer, conflicts, retries, versions, durable state and restore. OpenCloud/WebDAV, if retained, is a separately tested dependency. | Reuse verified engine mechanisms; storage compatibility, versions, deletion, recovery and safe policy changes remain to prove. |
| Updates | Rebase, rebuild, review and test each custom release; official binaries do not automatically contain the modification. | No OpenCloud-client rebase, but own protocol, OS, security, packaging and recovery maintenance indefinitely. | Track engine updates and public API compatibility; an engine fork adds merges. |
| Migration | Retain existing OpenCloud data if tested; an unmodified sync client on the same root can bypass the gate. | Using a new service requires individually verified transfer of files, versions, identities and permissions. No automatic equivalence. | Syncthing changes the peer topology; rclone changes execution semantics. Neither implies OpenCloud compatibility. |

### Responsibilities both paths must satisfy

1. **Windows observer and inventory:** only enrolled locations are scanned. Initial inventory, live detection and recovery reconciliation track names and last-known locations. [ReadDirectoryChangesW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-readdirectorychangesw) can lose notifications on buffer overflow; uncertain state requires a rescan. Handle moves, renames, case, links, inaccessible/locked paths and restart. Shared candidate metadata is sensitive and must not silently include content.
2. **Policy and user interaction:** preserve local drafts and last-known devices for offline authoring; reconcile confirmed shared changes and device acknowledgements on reconnect. Drafts remain drafts. Conflicting group rules and uncertain merges wait for the owner. One native app flow presents device/group, availability, one-off/future scope, bulk consequences and the separate MyBrain choice. A web presentation alone cannot enforce transfer.
3. **Gate and transfer:** deny undecided content on every upload, retry, restart and alternate path. Bind decisions to relevant paths, destinations, operations and content state. Concurrent changes create a check/use race: timestamp comparison alone does not prove the bytes later sent match the approved content. Test a stable snapshot or equivalent, and defer when identity cannot be established. Other independent upload processes can bypass the gate, so require one controlled transfer authority or equivalent isolation. Already-sent bytes cannot be recalled.
4. **Coordination, storage and recovery:** authenticate the shared policy, acknowledgements, last-known inventory and transfers. Distinguish discovery, receipt, durable storage and MyBrain staging. Define and test versions, trash, conflict copies and restoration. Narrowing policy must not silently delete existing copies. Backups and restore tests are independent of sync.
5. **Security and reliability:** use audited TLS/authentication, protect credentials, apply least privilege, validate paths and links, limit resource use and omit secrets and file contents from logs. Verify expected sizes and hashes, retain previous good copies after interruptions and test crash consistency. Checksums detect mismatch but do not authenticate a malicious sender. Clearly show stale offline knowledge and actual availability.

Concurrent edits, crashes during metadata/content commits, changed rules and retries demand deterministic handling without overwriting the only valid copy. Bulk approval covers the actual bounded action set, not merely one request, and may need reassessment after material changes. These obligations apply to all routes; an existing engine may supply some tested mechanisms.

The Windows [Cloud Files API](https://learn.microsoft.com/en-us/windows/win32/cfapi/build-a-cloud-file-sync-engine) supports Explorer placeholders and hydration through an accepted platform interface. Microsoft says its sample is not production code and leaves merges/synchronization to the provider. Ordinary full local files are a smaller initial scope; cloud-only placeholders, on-demand hydration and pinned offline availability need separate implementation and verification. Windows-first proof does not establish mobile equivalence.

### Concrete provisional comparison stacks

These are competing **research fixtures**, not selected technologies or approved deployments. The listed project licences do not establish a complete transitive source, binary or runtime audit.

| Component | OpenCloud-adaptation fixture | Independent-client/service fixture | Remaining evidence |
| --- | --- | --- | --- |
| Native Windows host | OpenCloud Desktop v4.0.0, C++/Qt; its [program licence](https://github.com/opencloud-eu/desktop/blob/v4.0.0/README.md) is GPL-2.0-or-later. | A small C++/Qt native client with owned file observation, consent and transfer authority. A native wizard is one experimental presentation only; the owner's desired uniform shared wizard with integrated client experience must still be tested. | [Qt](https://doc.qt.io/qt-6/licensing.html) offers OSS terms varying by module; audit exact build, dependencies and redistribution. Do not silently require Microsoft WebView2 or another closed app runtime. |
| Shared policy/NAS | An independent locally hosted service plus existing OpenCloud server if its selected artifact passes audit. The [server v4.0.0 manifest](https://github.com/opencloud-eu/opencloud/blob/v4.0.0/go.mod) declares Go 1.24.6; the server project is Apache-2.0. | A small independently maintained locally hosted service written in a candidate such as Go, using an authenticated API and managed file storage. [Go source](https://go.dev/doc/install/source) is BSD-style. | The server, API, TLS, credentials, operational state, server-side storage semantics and dependencies still require explicit design and audit. Neither proposal assumes an external proprietary service. |
| Local operational state | Own local policy/draft/acknowledgement and candidate state, interoperating with the adapted client. | Same responsibilities, with a candidate such as [SQLite](https://www.sqlite.org/copyright.html), whose deliverable code is public domain. | [SQLite WAL](https://www.sqlite.org/wal.html) cannot be treated as a shared database file over a network filesystem. Backup, restoration, migrations and consistency across file content and metadata remain work. |
| File observation | Reuse and test OpenCloud's existing watcher and safe integration seam. | Candidate Go [fsnotify](https://github.com/fsnotify/fsnotify/blob/main/README.md), whose source describes BSD licensing, or direct Windows APIs. | fsnotify is a Go library and is not automatically callable inside a C++ Qt client: an adapter, separate Go process, or an alternative watcher is required and unproved. It does not recursively watch subdirectories automatically. Overflow, restart, rename and rescan remain application responsibilities. Exact selected versions and transitive dependencies are unverified. |
| Sync engine and historical versions | Reuse OpenCloud transfers/versions while maintaining required pre-transfer enforcement. | Implement a bounded transfer path or investigate a reusable OSS engine; reuse is not automatic policy compliance. | Compare identical versions, conflict, deletion, restore, race and crash requirements; quantify only after tests. |

An alternative component candidate is [Syncthing v2.1.7](https://github.com/syncthing/syncthing/blob/d6d0181f7d466381c4b39ec8fd944c364f939b32/LICENSE), MPL-2.0, but its [ignore file](https://docs.syncthing.net/users/ignoring.html) is local and first-match; this is not shared group policy or a proved fail-closed control seam. Its [versioning](https://docs.syncthing.net/users/versioning.html) is optional and concerns incoming replacements/deletions, not a complete history of local edits. Its [FAQ](https://docs.syncthing.net/users/faq.html) explains that on reconnect a peer can see only the latest synchronized state, not every intermediate change while disconnected. Discovery, relay and update network defaults, OpenCloud interoperability and iOS support remain separate concerns. [rclone v1.75.2](https://github.com/rclone/rclone/blob/v1.75.2/COPYING), MIT, is a transfer candidate; a copy command alone is not a complete continuous bidirectional engine. A controller and a verified gate are required for either.

[.NET licence information](https://github.com/dotnet/core/blob/main/license-information.md) distinguishes source and distributed binaries; [Avalonia's FAQ](https://github.com/AvaloniaUI/avalonia-docs/blob/main/tools/faq.md) distinguishes its open framework and other tools. A Microsoft runtime distribution or commercial Avalonia component must not be assumed to meet the application dependency rule. No recursive SBOM, binary verification, toolchain build, licence compatibility ruling or runtime proof was performed. Do not create custom cryptography as a shortcut.

### NAS feasibility and resource limits

The evaluation target is a NAS with 6 GB total RAM; available headroom changes over time. A compact NAS service and locally hosted state are plausible in principle, but the runtime, indexing, scans, transfers, retained versions, containers and cache have not been measured. DSM support, CPU architecture, storage I/O, persistent volumes, backups and restart behavior need testing on the actual deployment. Disk capacity does not prove adequate memory or performance. A first proof does not need to assume a full database/search stack.

### Relative effort and maintenance

Compare the same accepted Windows-first experience, not a basic copy against a complete product. There is no defensible person-day estimate without measured seams, team capacity, test scope and security requirements. The following qualitative comparisons are hypotheses:

| Work | Adapt OpenCloud | Independent client/service | Separate existing engine |
| --- | --- | --- | --- |
| Small first-byte probe | Potentially less construction if a suitable seam works; race measurement still needed. | A small observer, gate, request recorder and fake service can be constructed, but no full sync is thereby supplied. | Potentially less engine work if an external seam prevents every bypass; this remains unproved. |
| Useful Windows release | Reuse tested transfers and shell, then build policy/wizard and maintain patches. | More responsibility for sync, state, transport, conflicts, security, packaging and recovery. | Reduced work only for verified engine capabilities; controller, UI and integration remain. |
| Full agreed behavior | Shared policy, groups, offline reconciliation, bulk handling and later mobile work remain, plus upstream merge testing. | All policy work plus long-term ownership of end-to-end correctness, device support, security and maintenance. | Policy work remains; gains depend on gate, engine, storage and mobile evidence; modifying engine brings fork costs. |
| Long-term | Rebase/retest each supported release to inherit fixes. | Maintain and patch owned implementation and dependencies. | Maintain controller/API compatibility and potentially a fork. |

This is not a timeline or a conclusion that a route wins. Fewer unwanted product features can simplify the experience, but does not remove the hard correctness obligations of synchronization.

### Smallest discriminating follow-up proof

Proposal only, not executed or authorized as deployment: synthetic files, an isolated Windows directory and an instrumented local fake service with no personal data. With one owned transfer path, start default-deny, observe a newly created file and assert zero file-content bytes reach the fake service before bounded approval. Confirm approved bytes and digest after approval; modify another file after approval and before reading/sending, and require a new or still-applicable decision. Include restart/interruption, rename and simulated lost-notification rescan; an already permitted synthetic file is a positive control. Observe headers and bodies separately so allowed candidate metadata is not mistaken for file content. Record versions, fixture values, expected and actual state, hashes and explicit failure criteria.

This tests whether one owned transfer path can meet the gate under selected failures. It does not prove a usable sync client, safety across every filesystem, OpenCloud interoperability, distributed policy, NAS capacity, mobile behavior or security. A separate apples-to-apples OpenCloud-seam or external-engine trial needs equivalent fixtures, byte-level observation and race tests. No installation, production NAS access or modifications were performed.

## Related Documents

- [Issue 9 research](<research.md>)
- [Native wizard and update feasibility](<native-wizard-update-feasibility.md>)
- [Policy and probe contract](<synchronization-policy-and-probe-contract.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-13 | PGMCP research implementer | Compare owned Windows and NAS synchronization responsibilities, open-source candidates and bounded experiments. |
