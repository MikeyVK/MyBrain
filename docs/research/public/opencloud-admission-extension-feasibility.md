<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# OpenCloud admission extension feasibility

**Status:** Focused source assessment — independent review requested; not an architecture decision  
**Version:** 1.0  
**Last Updated:** 2026-10-29

## Purpose

Assess whether a central MyBrain admission policy can be integrated across OpenCloud clients and server while retaining ordinary core updates, especially for a new file created inside an already connected desktop folder.

## Scope In

Public source/documentation inspection of desktop, Web, server, Android and iOS extension boundaries; implications for metadata-first admission and continued core updates.

## Scope Out

No addon installation, custom-client build, application tests, live inspection, deployment or upgrade. No amendment of the accepted storage Design, lifecycle model or Approved Strategy.

## Summary

Supported extension surfaces exist, but the inspected stock clients do not expose a documented independent pre-upload approve/defer contract. Web apps and server policies/postprocessing are useful, distinct boundaries. A metadata-only candidate workflow outside all native sync roots can preserve stock-client updates, but changes the requested transparent connected-folder experience. Exact transparent behavior requires an upstream-supported hold protocol or maintained client integration. This is a focused source assessment, not an accepted architecture or runtime proof.

## Requirement and interpretation

The current mandatory experience under investigation is: a user creates or edits a file inside an ordinary already-connected local folder; MyBrain discovers a candidate and can hold approval before the file's first content byte is uploaded by any applicable client route. A central policy should serve all supported devices, including offline/retry cases, while minimizing divergence from the maintained core product. No relaxation of this connected-folder experience has been authorized.

These are different guarantees: client-side hold before content transfer; server-side refusal before an upstream handler; server quarantine after bytes arrive; and registration in MyBrain. They must not be described as interchangeable. A metadata candidate/control plane before admission is a proposed extension workflow, not an accepted second source registry or a rewrite of the existing same-registration lifecycle principle.

The assessment treats "not found" as a bounded source result, not proof that an internal wrapper is impossible. No installed application version or actual device behavior has been inferred from repository tags.

## Inspected baselines and moving documentation

| Surface | Inspected reference | Limitation |
| --- | --- | --- |
| Desktop | [v4.0.0](https://github.com/opencloud-eu/desktop/releases/tag/v4.0.0), released 2026-09-03; additional main snapshot 7d5321aa3c68350d6c2d29039ef32af911d7be4d | Main is not the release ABI. No runtime/build proof. |
| Server | [v7.2.4](https://github.com/opencloud-eu/opencloud/tree/v7.2.4), with [reva v2.46.8 dependency](https://github.com/opencloud-eu/opencloud/blob/v7.2.4/go.mod) | Source pin, not deployed configuration verification. |
| Web / extension SDK | [v7.1.5 source](https://github.com/opencloud-eu/web/tree/v7.1.5) and official version-7.2 documentation | Independently inspected source; host/SDK compatibility must be checked for the actual deployment. |
| Android | [v1.2.5 tag](https://github.com/opencloud-eu/android/tree/v1.2.5), fd3e3f75332f368b9ad5e1518f7c36c5973174b0, 2026-06-27 | GitHub latest-release metadata pointed to v1.2.0, 2026-04-01; tag is not proof of store/installed version. |
| iOS | [v1.2.5 tag](https://github.com/opencloud-eu/ios/tree/v1.2.5), 1a21f8301a6041ea58bfc8dbd8b70bdb35356bcc, 2026-09-29; embedded SDK b1338108db81146317a826074bcc2667afbf41db | No GitHub release record found; no installed/store-version claim. |

Assessment date is 2026-10-29. Official documentation with main/next URLs is mutable; versioned source links are preferred for code claims. The [official lifecycle page](https://docs.opencloud.eu/docs/next/admin/resources/lifecycle/) then listed Production 7.2.4 and Rolling 9.0.0, released 2026-10-27. That is context for maintenance, not a proposal to upgrade an existing installation.

## Capability and support matrix

| Surface | Actual extension/control boundary | Pre-first-content-byte gate for stock native clients? | Status and maintenance |
| --- | --- | --- | --- |
| Desktop VFS providers | Placeholder, hydration, pinning and filesystem metadata integration | No independent candidate/approve/defer API found | Real C++ plugins, exact full-client-version match and fixed provider modes; internal integration is version-coupled. |
| Desktop shell socket / CLI | Status/share/pin/hydration or controlled batch sync | No documented admission handshake found | Separate automation is possible; not a universal live-folder hold. |
| Web SDK app | Routes, navigation, application viewport and registered extension types | Only for uploads the custom app itself owns | Documented separately packaged frontend; host-shared dependencies and SDK versions still constrain updates. |
| Server OPA/Rego policy | Method/path/name/user/stage request authorization; deny before next handler | Does not stop bytes leaving a native device | Documented middleware, useful server enforcement; not arbitrary client candidate identity/content authorization. |
| Server custom postprocessing | NATS processing steps before making a completed upload available | No: invoked after all upload bytes arrive | Documented custom service boundary; needs handler, event-version pins and recovery. |
| Stock Android | Worker, document-provider and communication-library upload paths | No externally installable veto contract found | Owning/replacing a path or maintained native integration is required. |
| Stock iOS | App-bundled share/File Provider paths and embedded SDK extensions | No external plugin that changes another installed app found | Own app/SDK integration is viable; cannot assume control over stock routes. |
| MyBrain mobile app / selected-directory companion | Own admission UI and upload initiation | Can hold its own upload before calling the transport | Proposal requiring platform-specific adapters and proofs; does not transparently govern all other apps. |
| Dashboard / PWA | User-selected files and platform-dependent directory permissions | No control over stock native uploads | Appropriate control UI, not a universal local filesystem monitor. |

Evidence for these distinctions is detailed below. A documented extension facility is not automatically a supported admission contract, and separately installed packaging does not imply zero maintenance.

## Desktop: real plugins, missing independent admission contract

The [VFS plugin factory](https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/libsync/common/plugin.h) and [loader](https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/libsync/vfs/vfs.cpp#L165) are real. The loader expects type vfs and metadata Version equal to the full client version; its modes are off/cfapi/openvfs. The [VFS interface](https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/libsync/vfs/vfs.h) handles placeholders and related filesystem behavior, not an independent approve/defer result.

Counterevidence to a categorical "plugins are impossible": VfsSetupParams exposes SyncEngine and journal access. A version-matched wrapper could potentially use internal C++ paths without editing core source text. That has not been proved viable or impossible; it remains private, provider-specific integration, not a stable separately installable admission ABI.

The [sync-engine sequence](https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/libsync/syncengine.cpp#L529) emits aboutToPropagate, then constructs and starts propagation without awaiting an external pending/approve decision. A notification alone is therefore not a hold contract. The [shell socket v1.1 surface](https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/gui/socketapi/socketapi.h) exposes status/sharing/pinning/hydration; the [CLI](https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/cmd/cmd.cpp#L136) controls batch synchronization, not the required handshake.

Reactive exclusion is unsafe as the admission mechanism: [folder startSync](https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/gui/folder.cpp#L827) loads ignores, while the [ignore editor](https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/gui/ignorelisteditor.cpp#L84) reloads/enqueues discovery; a later watcher update can lose the race with first upload. [Selective-sync journal semantics](https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/libsync/common/syncjournaldb.h#L141) treat excluded local folders as absent/deleted for synchronization, not candidate-held files. These facilities must not be relabeled as a guaranteed admission barrier.

## Server and Web: useful supported seams with different timing

The documented [Web extension system](https://github.com/opencloud-eu/docs/blob/main/versioned_docs/version-7.2/dev/web/extension-system/getting-started.md) supports independent apps with routes/navigation and extension points. [Server Web configuration](https://github.com/opencloud-eu/opencloud/blob/v7.2.4/services/web/README.md) loads packaged static assets/manifests using app configuration; it does not inject arbitrary dynamic backend code. The [v7.1.5 SDK](https://github.com/opencloud-eu/web/blob/v7.1.5/packages/extension-sdk/src/index.ts) uses Module Federation/shared host modules, not a generic import-map ABI. [Build/publish guidance](https://github.com/opencloud-eu/docs/blob/main/versioned_docs/version-7.2/dev/web/extension-system/build-and-publish.md) describes compatible dependencies and minOpenCloud/maxOpenCloud metadata; host Vue/Pinia and Web packages remain coupled. An app can own an upload/admission screen but cannot thereby veto another client.

[OPA policy documentation](https://github.com/opencloud-eu/opencloud/blob/v7.2.4/services/policies/README.md) and [proxy middleware](https://github.com/opencloud-eu/opencloud/blob/v7.2.4/services/proxy/pkg/middleware/policies.go) establish an actual server deny boundary. The supplied policy inputs concern request method/path/name/user/stage, not an arbitrary local candidate record, origin or approved content digest. Middleware denial is not proof that no request content already traversed the network.

[Custom postprocessing](https://github.com/opencloud-eu/opencloud/blob/v7.2.4/services/postprocessing/README.md) is a documented NATS service extension after all bytes have arrived, before normal availability. Its custom handler can continue/abort/retry processing, so it can contribute to server-side quarantine. The README calls the reply PostprocessingFinished, while the inspected [event type](https://github.com/opencloud-eu/reva/blob/v2.46.8/pkg/events/postprocessing.go) and [service implementation](https://github.com/opencloud-eu/opencloud/blob/v7.2.4/services/postprocessing/pkg/service/service.go) use PostprocessingStepFinished. Implement against the pinned actual schema, not the illustrative name; no general forever-stable internal event ABI was established.

An [app provider](https://github.com/opencloud-eu/opencloud/blob/v7.2.4/services/app-provider/README.md) opens files by MIME/application, not a universal admission veto. A proposed [ctx.hook veto issue](https://github.com/opencloud-eu/opencloud/issues/3465) is not evidence of a shipped extension contract.

Upload coverage must include [TUS](https://github.com/opencloud-eu/docs/blob/main/versioned_docs/version-7.2/dev/server/apis/http/tus_upload.md), WebDAV and copy/move routes. The desktop's [initial TUS POST](https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/libsync/propagateuploadtus.cpp#L75) can already carry bytes; waiting for a later PATCH is insufficient for a before-first-byte guarantee.

## Mobile: one logical policy, different owned adapters

Android's [automatic upload worker](https://github.com/opencloud-eu/android/blob/v1.2.5/opencloudApp/src/main/java/eu/opencloud/android/workers/AutomaticUploadsWorker.kt#L280), [document-provider close path](https://github.com/opencloud-eu/android/blob/v1.2.5/opencloudApp/src/main/java/eu/opencloud/android/presentation/documentsprovider/DocumentsStorageProvider.kt#L209) and [PUT operation](https://github.com/opencloud-eu/android/blob/v1.2.5/opencloudComLibrary/src/main/java/eu/opencloud/android/lib/resources/files/UploadFileFromContentUriOperation.kt#L38) expose implementation paths, not an independently installable admission plugin. The communication library is reusable code, not a demonstrated stable plugin ABI.

iOS's [bundled Share Extension](https://github.com/opencloud-eu/ios/blob/v1.2.5/OpenCloud%20Share%20Extension/ShareExtensionViewController.swift#L327), [File Provider](https://github.com/opencloud-eu/ios/blob/v1.2.5/OpenCloud%20File%20Provider/FileProviderExtension.m#L747) and [photo-upload flow](https://docs.opencloud.eu/docs/user/ios-app/general/settings/auto-upload-photos-and-videos/) are separate native routes. [SDK extension registration](https://github.com/opencloud-eu/ios-sdk/blob/b1338108db81146317a826074bcc2667afbf41db/OpenCloudSDK/Extensions/OCExtensionManager.m#L77) uses an in-process array; [Apple app extensions](https://developer.apple.com/library/archive/documentation/General/Conceptual/ExtensibilityPG/ExtensionCreation.html) ship inside their containing app, rather than injecting behavior into another installed app.

An own MyBrain app could hold approval before invoking [SDK import/upload](https://github.com/opencloud-eu/ios-sdk/blob/b1338108db81146317a826074bcc2667afbf41db/OpenCloudSDK/Core/OCCore.h#L484). This is an architectural inference requiring a prototype, not a shipped cross-client solution. It governs its own uploads; stock photo/share/provider flows must be explicitly disabled, replaced or integrated if the same policy must cover them.

Do not overstate operating-system limits: iOS supports user-granted [recursive chosen-directory access](https://developer.apple.com/documentation/uikit/providing-access-to-directories?language=objc), and Android [Storage Access Framework trees](https://developer.android.com/training/data-storage/shared/documents-files) provide chosen-tree access subject to restrictions. Neither establishes an unrestricted universal monitor. [Browser File System Access](https://developer.chrome.com/docs/capabilities/web-apis/file-system-access) is permission/platform dependent; a dashboard/PWA does not supervise unmodified stock native uploads.

## Viable alternatives and update costs

| Route | Fit to strict connected-folder requirement | Core-update implications |
| --- | --- | --- |
| Outside-root staging plus MyBrain companion | Does NOT meet transparent creation inside an ordinary connected folder. Candidates stay outside ALL sync roots; only an approved stable snapshot enters a dedicated synced tree. | Stock client updates remain available; companion APIs, filesystem behavior and approval-to-snapshot binding still need compatibility tests. This workflow change needs an owner decision. |
| Custom MyBrain desktop/mobile client or thin internal integration | Can target exact behavior on the paths it owns; every required native entry path still needs coverage. | Maintain/pin native adapters, packages, signing and regression matrix. A thin version-bound VFS wrapper is an unproved variant, not necessarily a textual full fork. |
| Upstream supported candidate/hold/approve-resume protocol | Best long-term fit if accepted, implemented and maintained across required clients. | No such independent contract found in inspected releases. Upstream acceptance/timing are unknown; not a dependency that can be assumed delivered. |
| Web-owned upload UI plus server policy/postprocessing | Supports centralized control of owned uploads and server availability. | Independently packaged Web app/service, with explicit host/event compatibility. Does not satisfy before-first-byte hold for ordinary unmodified native folders. |
| Server quarantine alone | Can delay availability after arrival. | Useful defense/control boundary, but changes the pre-transfer guarantee; requires explicit acceptance rather than being called equivalent. |

The policy/candidate backend may be part of the existing MyBrain application; a mandatory second product is not implied. A proposed central policy service can return a common logical decision, while desktop/mobile/Web adapters own platform-specific discovery, snapshot and transport behavior. It is not one shared binary plugin. Before upload, a grant must correspond to the exact approved snapshot; edits, renames, retries and expiry must not authorize different bytes accidentally. This is a feasibility requirement, not an adopted token/schema design.

Continued updates mean supported release lanes, version pins, compatibility bounds and regression evidence, not unattended latest-version installation. In particular, [OpenCloud 7.x upgrade guidance](https://docs.opencloud.eu/de/docs/next/admin/maintenance/upgrade/upgrade-7.x.x/) warns about older Web-app compatibility. Policy loading also changes between the inspected [7.2.4](https://github.com/opencloud-eu/opencloud/blob/v7.2.4/services/policies/README.md) and [9.0.0](https://github.com/opencloud-eu/opencloud/blob/v9.0.0/services/policies/README.md) descriptions. No upgrade, addon or runtime change is proposed here.

## Required falsification tests and open decision

These are unexecuted tests for a later authorized prototype:

| Proof | Required counterexample coverage |
| --- | --- |
| Before-first-byte hold | Create/edit inside each claimed ordinary sync folder with the policy service unavailable or undecided; observe actual network requests including TUS creation bodies. Zero content bytes must leave before approval if that guarantee is claimed. |
| Approval binds exact bytes | Edit/replace/rename during scanning and between approval/upload; revoke/expire a decision; retry after lost response. A grant cannot silently apply to another snapshot or identity. |
| Cross-device bypass inventory | Exercise desktop providers, CLI, Web, Android camera/manual/document routes and iOS Share/File Provider/photo routes. Explicitly unsupported paths must not remain an unnoticed parallel bypass. |
| Offline/restart/concurrency | Disconnect policy/device, restart during hold, use two clients and conflicting decisions. Demonstrate durable pending state and deliberate failure behavior, not a reactive-ignore race. |
| Server timing | Prove actual request-denial and postprocessing availability boundaries separately; cover WebDAV/TUS/copy/move and failed/retried custom events. Postprocessing cannot pass a pre-transfer oracle. |
| Update compatibility | Rebuild/repackage against each admitted host/client version, verify metadata bounds and event schemas, then repeat behavioral gates. No supported packaging claim substitutes for tests. |
| Scope and privacy | Prove that proposed metadata-only candidates do not transfer excluded content through logs, previews or an analysis service; distinguish candidate control records from admitted source authority. |

The current requirement remains the transparent ordinary-connected-folder experience. The research recommendation is to pursue a small upstream-supported client admission contract first, with candidate hold, approve/resume and exact-snapshot revalidation; upstream acceptance and delivery are unknown. A maintained version-bound client integration is the fallback to investigate, not an already proven addon. Outside-all-syncroots staging is a workflow-changing alternative that would require a separate owner decision; it is not the current solution. Feasibility and update cost must be demonstrated before claiming a sustainable cross-client implementation.

Source inspection supports the boundary assessment only. No extension was installed, built or executed; no platform network/fault/update test ran. The native documentation check validates local links/heading fragments and excludes external URLs; it does not verify these application guarantees.

## Related Documents

- [Accepted storage design (unchanged)](<../../development/issue6/design.md>)
- [Source-registration principles (unchanged)](<../../architecture/decisions/0001-digital-brain-foundational-principles.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-29 | Codex (@imp researcher) | Consolidate version-pinned desktop, server/Web and mobile extension evidence, compatibility costs, alternatives and unexecuted proof obligations. |
