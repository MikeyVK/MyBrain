<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# OpenCloud sovereignty and dependency research

**Status:** Research — source inspection; independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-11-13

## Purpose

Assess the evidence for fully open-source application dependencies and viable independent synchronization routes.

## Scope In

OpenCloud server, web and desktop/mobile clients; build, distribution, online service and platform boundaries; feasible alternatives.

## Scope Out

No implementation, platform selection, runtime inspection, deployment modification, software installation, complete SBOM or legal opinion.

## Problem Statement

Source availability alone does not establish that every component of a distributed application or its operating environment meets a strict open-source and sovereignty requirement.

## Goals

- Identify direct evidence and unresolved dependency boundaries.
- Compare realistic independent paths without selecting a package or weakening accepted synchronization behavior.
- Specify evidence required to validate a chosen release and platform.

## Findings

## Assessment and boundaries

The publicly available server, web and client source is a credible open-source starting point, but the inspected sources are not a complete dependency or deployment audit. No mandatory closed third-party application library or external proprietary cloud service has been established by this inspection. This is not proof that none exists. Operating systems, bundled binaries, optional integrations, fonts, plugins, notifications, telemetry, signing and build dependencies must be assessed separately. OSS licences grant freedoms under conditions; “no licences” literally would not describe usable OSS. No package or architectural route is selected.

The owner clarified the acceptance boundary: the application, libraries and services must be open source; Windows, iOS and Synology DSM may remain as platforms. Thus those operating systems and their ordinary platform frameworks are disclosed boundaries, not automatic exclusions. Third-party runtimes or services selected as application dependencies still must satisfy the requirement. Build, update, signing and distribution dependencies need their own explicit verification; full hardware and firmware sovereignty is outside this stated boundary. An open application on an accepted closed host is therefore a feasible objective, not an entirely open device.

## Inspected source and distribution

| Surface | Evidence and concrete scope | Conclusion and remaining gap |
| --- | --- | --- |
| Server | OpenCloud publishes its [Apache-2.0 server](https://github.com/opencloud-eu/opencloud) and the [v4.0.0 Go manifest](https://github.com/opencloud-eu/opencloud/blob/v4.0.0/go.mod) lists many direct and indirect modules. | Public source and a versioned manifest do not establish licence, origin or necessity of every module or every deployed image component. The actual installation version and image were not inspected. |
| Web | [Web v8.2.2 manifest](https://github.com/opencloud-eu/web/blob/v8.2.2/package.json) declares AGPL-3.0 and includes commands for licence checking; its [lockfile](https://github.com/opencloud-eu/web/blob/v8.2.2/pnpm-lock.yaml) pins dependency resolutions. | The check has exclusions and was not executed here. An available upstream command, source manifest and lockfile are evidence to review, not a complete passed binary audit. |
| Windows desktop | [Desktop v4.0.0 CMake](https://github.com/opencloud-eu/desktop/blob/v4.0.0/CMakeLists.txt) requires Qt and other libraries, enables update notification by default, and lists both off and Windows CFAPI virtual-file plugins; [project licence](https://github.com/opencloud-eu/desktop) describes GPL version 2 or later for the program. | Off is a listed build/plugin choice, not evidence that the installed binary uses it or that every sync mode retains required behavior. Qt availability under OSS terms is not proof of all shipped components. Windows is a separate closed-platform dependency. |
| Android | The pinned [1.2.5 app manifest](https://github.com/opencloud-eu/android/blob/cf6d451c713182d2962c22d6bbcb7659825fed75/opencloudApp/build.gradle) declares AndroidX, including Custom Tabs for OAuth/OIDC, plus other libraries. Its [version catalog](https://github.com/opencloud-eu/android/blob/cf6d451c713182d2962c22d6bbcb7659825fed75/gradle/libs.versions.toml) names their versions. [F-Droid](https://f-droid.org/en/packages/eu.opencloud.android/) describes version 1.2.5 as GPL-2.0-only and F-Droid-built and signed from its indicated source. | Strong evidence that an alternative distribution exists; not proof of feature parity, every transitive licence, a Google-free runtime, or all device firmware. The inspected app manifest alone does not establish a mandatory Firebase or Play Services dependency. Test the exact variant on the chosen device. |
| iOS | The pinned [third-party notice](https://github.com/opencloud-eu/ios/blob/c958854e1c3e695552f383de3f401cac41753d1c/THIRD_PARTY.txt) names the GPLv3 SDK and components under MIT and Apache terms. An existing [web-app view](https://github.com/opencloud-eu/ios/blob/c958854e1c3e695552f383de3f401cac41753d1c/OpenCloudAppShared/Client/Actions/Implementations/ClientWebAppViewController.swift) uses Apple's WebKit framework. | The app source being GPL does not make iOS, Apple's framework, normal build/signing or device open. The existing view does not establish how a new wizard must be built. The notice mentions a distribution exception that needs separate verification. |
| Distribution and add-ons | The vendor lists a self-hosted [Community Edition](https://opencloud.eu/en/subscription-support) and commercial offerings including proprietary Helm charts. [Collaboration integrations](https://docs.opencloud.eu/docs/next/dev/server/services/collaboration/information/) exist. | Do not treat commercial charts or optional office products as mandatory. Conversely, do not assume a specific installed deployment excludes them without an inventory. |

Different versions above are independent snapshots, not an asserted compatible release set. Recheck source tags, resolved commits and actual selected artifacts before building. The Android and iOS source pins are exact commits; their relationship to any installed binary has not been established. The desktop and web versions are pinned by release tag; a release audit should additionally record resolved commit and image or installer digest.

An [ownCloud Infinite Scale licence page](https://doc.owncloud.com/ocis/9.0/developer/license.html) states that source is Apache-2.0 while its stable, supported vendor-distributed binaries are covered by a non-OSS freemium EULA. This is an example of why source and distributed artifact must be checked separately. It describes ownCloud, not OpenCloud, and must not be transferred to OpenCloud without independent evidence.

## Browser and platform trade-offs

An embedded web wizard is a possibility, not proof of a chosen dependency. [Qt WebView](https://doc.qt.io/qt-6/qtwebview-index.html) documents Qt WebEngine or Microsoft WebView2 on Windows and a system web view on iOS. [Qt WebEngine](https://doc.qt.io/qt-6.8/qtwebengine-licensing.html) has open-source licensing choices and further component licence obligations; validate the specific build and codecs. [Microsoft describes WebView2 runtime licence terms and diagnostic data](https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/data-privacy); choosing that runtime would conflict with a strict open-source runtime boundary. Neither possibility proves the present OpenCloud desktop requires WebView2.

On iOS, the inspected existing client uses Apple system frameworks; those frameworks and iOS belong to the accepted platform boundary, not proof that the application itself fails the requirement. Android's AOSP path and Linux desktop/server can reduce proprietary platform dependencies, but actual hardware drivers, firmware, notification services and tested support vary. A browser-based interface does not itself enforce pre-transfer synchronization rules. Third-party embedded browser runtimes must be separately audited against the application dependency requirement.

## Feasible independent routes, not selected designs

1. **Own policy service and open web wizard, adapted upstream clients.** Keep the server as a replaceable storage service if its exact deployed stack passes audit. A separately maintained policy service and wizard can own rules and presentation, while client modifications are needed wherever the existing synchronization engine otherwise transfers undecided bytes. Existing open client source is reusable, subject to licence and per-release merge costs. No supported pre-transfer hook covering all clients has been proved.
2. **Own policy service, wizard and independent sync clients.** Use a fully audited open protocol implementation or independently implement clients, potentially retaining a compatible server behind a replaceable interface. This avoids dependence on upstream client internals, but requires building and maintaining safe file observation, pre-transfer holds, retries, conflicts, offline operation, authentication, file availability, errors and native device integration. WebDAV alone is not an implementation of those behaviors or a complete OpenCloud interoperability guarantee.
3. **Evaluate other open engines.** [Syncthing security documentation](https://docs.syncthing.net/users/security.html) describes configurable global discovery, enabled by default, and its information exposure. Automatic updates are also enabled by default; a GUI upgrade check may remain even when automatic upgrades are disabled unless the documented build switch is used. An alternative local or self-operated topology needs its own connectivity and egress tests. Syncthing is a candidate for a focused comparison, not a demonstrated implementation of the integrated policy, wizard, OpenCloud compatibility or supported iOS experience. Prior platform comparisons should be revisited per version rather than assumed unchanged.

The accepted issue 9 experience stays in scope for each alternative: one integrated choice for device/group synchronization and separate MyBrain staging/admission; local and shared policy with offline drafting and safe reconnection; hold undecided content before transfer; bounded and cumulative bulk safeguards; visible device status, history and errors; no whole-device crawl. A web page cannot replace a native-client enforcement point. No existing candidate has been proved to deliver the whole behavior without adaptation.

## Acceptance evidence still needed

Before an actual stack can be accepted as fully open under a defined boundary:

1. Identify each deployed server image, web bundle and desktop/mobile package with exact versions, immutable image/installer digests, source commit and build configuration; include enabled extensions and optional products. Inspect actual dependencies, system libraries, bundled assets and fonts rather than only package root licences.
2. Generate and review per-target recursive source/build/runtime SBOMs, licence texts and provenance, including transitive packages, plugins and native shared libraries. Check source availability, modification/rebuild and redistribution rights, copyleft obligations and exceptions. Reconcile SBOMs to the actual binaries and their build options; absence from a single manifest is not evidence of absence.
3. Rebuild selected artifacts in an isolated environment with documented open tools, compare output or attest meaningful non-reproducible differences, and verify how updates and security patches can be independently obtained. Distinguish source compilation, signing and store distribution; prove no commercial build service is essential.
4. In an isolated synthetic deployment, record outbound DNS and network traffic during startup, login, normal sync, crashes and updates. Disable or replace optional telemetry, fonts, discovery, relays, authentication and update services; demonstrate intended operation with external services unavailable. A named SDK alone does not prove a remote service is required or active.
5. Test client and OS-specific first-byte hold, offline draft/reconciliation, concurrent or interrupted transfers, groups and device exceptions, bulk approval, origin-only location visibility and MyBrain choice. Test actual upgrade and migration behavior and update impact. Check native mobile background and file-access limits on each supported platform.
6. Record platform and hardware dependencies transparently under the owner's stated boundary, while rejecting non-open application libraries and services. Repeat the review for releases and modifications; retain evidence and explicit unresolved exceptions.

This is source/document review only. No software was installed, no binaries or deployment were scanned, no sync/network experiment ran, and no private content was accessed. Prior runtime tests are separate evidence and do not establish licence completeness.

## Questions

- Which exact build, signing and update dependencies satisfy the stated application and service boundary on each accepted platform?
- Which exact release artifacts, deployment configuration and supported devices should be audited?
- Which integration seam can hold content before transfer without sacrificing maintainable updates?

## Risks

### Treating source licence or a repository manifest as a complete deployment audit.

Reconcile recursive SBOM, binary, image and network evidence for each selected release.

### Assuming a native wizard and synchronization interception follow automatically from an open web interface.

Perform client-specific first-byte and upgrade tests against accepted behavior.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-13 | PGMCP research implementer | Record bounded source audit, sovereignty boundaries, independent routes and acceptance evidence. |
