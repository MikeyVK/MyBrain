<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Integrated native wizard and update feasibility

**Status:** RESEARCH CHECKPOINT — source evidence; native integration and update proofs pending  
**Version:** 1.1  
**Last Updated:** 2026-11-05

## Purpose

Assess how the owner-approved integrated synchronization/MyBrain wizard could be delivered in OpenCloud desktop and mobile applications while continuing to benefit from upstream updates.

## Scope In

Native interaction requirements, concrete source boundaries, upload-path coverage, device inventory, update/distribution implications and unexecuted falsification tests.

## Scope Out

No implementation, installation, running prototype, deployed-version inspection, account access, upstream contact, selected fork, automatic-upgrade claim or phase exit.

## Summary

The wizard experience is accepted: one native-app flow and one confirmation cover storage, selected devices and local availability, MyBrain registration, and reusable scope. Source inspection identifies places to integrate owned client code, but establishes no supported independent cross-client wizard/admission addon. Keeping upstream improvements is possible as a maintenance route to investigate; ordinary official binary updates are not evidence that a separately maintained feature will survive. Native integration and compatibility strategy remain undecided.

## Accepted interaction requirement

On 2026-11-05 the owner accepted a wizard offered by the desktop or mobile app before unknown new file contents reach the OpenCloud server. One set of files, directory or grouped selection receives one coherent summary and confirmation. The independent MyBrain choice belongs inside that same flow and reusable rule; it must not be deferred to an unrelated later feature.

| Question in the same wizard | Plain-language choice | Boundary |
| --- | --- | --- |
| Where to keep the files? | Keep only on this device; also keep in my cloud. | Undecided new content remains local; a matching accepted rule can handle later files automatically. |
| Which other devices? | Use on the named devices I select. | Include registered offline devices and show capabilities; origin-only concerns automatic distribution, not another person's access rights. |
| How to use them there? | Retrieve when opened; also use without internet. | Offer only supported device behavior; visibility, actual download and retained local copy differ. |
| Include in MyBrain? | Also include in MyBrain, or preserve the chosen storage/synchronization without admission. | This is independently selectable in the same confirmation, not a separate-time workflow. MyBrain processing semantics remain under the intake contracts. |
| How broadly does this apply? | Only these files; future files in this directory; a reusable rule. | Preview affected files and exceptions. Rule changes do not implicitly destroy existing copies. |

The app must show all devices registered for the owner's configuration, rather than only devices currently online. Future devices require an explicit rule-scope decision; no automatic inclusion default is selected. Saved intent, receipt on each device, effective rule application, transfer completion and MyBrain registration/processing need distinct truthful feedback. One user confirmation does not imply an instantaneous distributed transaction or simultaneous success.

The owner subsequently clarified that rules can be authored, confirmed and durably saved offline using last-known devices, server folders and policy. Origin/local storage, intended local-only or shared reach, and actual application are separate. The canonical [local/shared policy requirements](research.md#local-rule-authorship-intended-reach-and-shared-application) and [offline/reconciliation probe contract](research.md#offline-and-reconciliation-probe-contract) govern reconnect and connected-policy-change cases for every native integration candidate. These accepted behaviors do not choose precedence, offline use of prior rules, group enrollment, a central master or a merge algorithm.

The native app is the required presentation host. Reusing shared wizard content or an embedded Web view is an option to investigate, but opening a separate dashboard alone does not satisfy the native-flow requirement or stop native uploads.

## Evidence baseline and limits

Sources were inspected on 2026-11-05. The actual installed apps and their server/SDK combinations remain unknown. The [historical assessment](opencloud-admission-extension-feasibility.md) retains its earlier release pins unchanged.

| Surface | Inspected baseline | Evidence limit |
| --- | --- | --- |
| Desktop | v4.0.0, shown as the latest release by the inspected [release page](https://github.com/opencloud-eu/desktop/releases/tag/v4.0.0). | Source/release evidence, not installed-version or runtime proof. |
| Android | Source commit cf6d451c713182d2962c22d6bbcb7659825fed75. | Current source snapshot; no store-release or installed-version equivalence claimed. |
| iOS | Source commit c958854e1c3e695552f383de3f401cac41753d1c. | Current source snapshot; no installed/store-version equivalence claimed. |
| iOS SDK | Submodule commit bf88add68e55abb21c00f2af51e24f51b2206a8a from the app snapshot's [dependency entry](https://api.github.com/repos/opencloud-eu/ios/contents/ios-sdk?ref=c958854e1c3e695552f383de3f401cac41753d1c). | Source dependency identity only; no app/SDK runtime compatibility test. |
| Server support surfaces | v7.2.4 auth-app, graph, clientlog and Web configuration. | Bounded interface inventory, not an exhaustive proof that all possible device APIs are absent. |

## Desktop integration evidence

| Inspected source | Observation | Consequence for the wizard/update route |
| --- | --- | --- |
| [FolderWizard](<https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/gui/folderwizard/folderwizard.cpp>) | The native Qt wizard selects local root, Space and selective synchronization during setup. | Existing native presentation can be extended in an owned build; it is not already an ongoing admission wizard for newly arriving sets. |
| [SyncEngine reconciliation](<https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/libsync/syncengine.cpp#L529>) | aboutToPropagate is emitted, followed by propagator construction/start without a documented asynchronous pending decision. | A notification handler is not a demonstrated hold. A synchronous internal signal handler/provider integration remains possible but unproved; absence of an awaited result is not impossibility. Adding an admission seam or proving a supported exclusion-based barrier needs direct investigation. |
| [Initial TUS upload](<https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/libsync/propagateuploadtus.cpp#L75>) | makeCreationWithUploadJob passes an upload device as the initial POST body. | Gating only a later chunk can be too late for the before-first-content-byte requirement. |
| [VFS loader](<https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/libsync/vfs/vfs.cpp#L165>), [VFS setup/interface](<https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/libsync/vfs/vfs.h#L43>) | Real provider plugins exist; the loader checks VFS type and exact full-client version. Setup exposes engine/journal references. | An internal provider wrapper may be worth testing, but is version-coupled and not evidence of a general stable wizard/approve/defer addon ABI. Do not claim plugins are impossible. |
| [Shell socket API](<https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/gui/socketapi/socketapi.h>) | Status, sharing, availability/hydration and account commands are exposed. | These do not establish a universal pre-upload decision handshake or a catalogue of all devices belonging to the owner. |
| [External branding](<https://github.com/opencloud-eu/desktop/blob/v4.0.0/THEME.cmake>), [updater selection](<https://github.com/opencloud-eu/desktop/blob/v4.0.0/src/gui/updater/updater.cpp>) | Build-time branding/OEM configuration and configurable update URLs/platform updaters exist. | A custom build/update channel is a real packaging surface. Branding alone does not add admission behavior; an official replacement binary does not promise to retain custom source changes. |

A pre-established default-deny/positive-allowlist projection must be tested separately from a reactive watcher adding exclusions after discovery. The former has not been proved safe across traversal, reload, edits, retries and all selected roots; the latter can lose a race with upload. Neither is selected here.

The release notes for v4.0.0 include a Qt 6.11 dependency transition and plugin-loading changes. That is concrete compatibility risk, not a measured estimate of maintaining this wizard. Upstream source reuse and a custom update channel remain distinct from unmodified official auto-updates preserving the feature.

## Android and iOS integration evidence

| Platform / route | Source evidence | Research implication |
| --- | --- | --- |
| Android manual upload | [UploadFilesFromContentUriUseCase](<https://github.com/opencloud-eu/android/blob/cf6d451c713182d2962c22d6bbcb7659825fed75/opencloudApp/src/main/java/eu/opencloud/android/usecases/transfers/uploads/UploadFilesFromContentUriUseCase.kt>) stores queued transfers and calls the one-file upload use case. | A foreground wizard could be integrated before owned queue admission; this is an inference requiring a build and network proof. |
| Android automatic and document-provider paths | [AutomaticUploadsWorker](<https://github.com/opencloud-eu/android/blob/cf6d451c713182d2962c22d6bbcb7659825fed75/opencloudApp/src/main/java/eu/opencloud/android/workers/AutomaticUploadsWorker.kt#L278>), [DocumentsStorageProvider](<https://github.com/opencloud-eu/android/blob/cf6d451c713182d2962c22d6bbcb7659825fed75/opencloudApp/src/main/java/eu/opencloud/android/presentation/documentsprovider/DocumentsStorageProvider.kt#L208>) use separate background/write-close routes. | Changing the visible file picker alone misses other upload paths. Pending decisions, execution and resumed/retried work need coverage. No externally installable admission plugin was established in the inspected source. The [lowest PUT operation](https://github.com/opencloud-eu/android/blob/cf6d451c713182d2962c22d6bbcb7659825fed75/opencloudComLibrary/src/main/java/eu/opencloud/android/lib/resources/files/UploadFileFromContentUriOperation.kt#L38) remains reusable transport, rather than a place to mix wizard UI with policy. |
| iOS grouped manual import | [ImportFilesController](<https://github.com/opencloud-eu/ios/blob/c958854e1c3e695552f383de3f401cac41753d1c/OpenCloud/Import/ImportFilesController.swift#L91>) offers a native grouped location picker, then schedules SDK import calls. | Existing native interaction is a useful owned integration point, not the accepted complete wizard already implemented. |
| iOS Share and File Provider | [ShareExtensionViewController](<https://github.com/opencloud-eu/ios/blob/c958854e1c3e695552f383de3f401cac41753d1c/OpenCloud%20Share%20Extension/ShareExtensionViewController.swift#L327>), [FileProviderExtension](<https://github.com/opencloud-eu/ios/blob/c958854e1c3e695552f383de3f401cac41753d1c/OpenCloud%20File%20Provider/FileProviderExtension.m#L746>) separately call core import. | Every claimed path must consult the same accepted intent/rules before its transfer becomes eligible; changing only the main-app picker is insufficient. |
| iOS media uploads | [MediaUploadQueue](<https://github.com/opencloud-eu/ios/blob/c958854e1c3e695552f383de3f401cac41753d1c/OpenCloud/Media%20Uploads/MediaUploadQueue.swift#L74>) persists jobs and requests scheduling. | Photo/media paths need their own coverage instead of inheriting a manual-import result. |
| iOS extension mechanism | [SDK extension manager](<https://github.com/opencloud-eu/ios-sdk/blob/bf88add68e55abb21c00f2af51e24f51b2206a8a/OpenCloudSDK/Extensions/OCExtensionManager.m#L40>) registers extensions in-process. [Apple's app-extension guide](https://developer.apple.com/library/archive/documentation/General/Conceptual/ExtensibilityPG/ExtensionCreation.html) describes extensions shipped within their containing app. | Reusable SDK code and bundled Share/File Provider extensions do not establish injection of an independent plugin into the installed official app. |

Mobile background work cannot be assumed able to present a modal wizard immediately. [Android restricts background activity launches](https://developer.android.com/guide/components/activities/secure-bal); an app notification and later foreground interaction are ordinary possibilities. Apple's [extension lifecycle/background-transfer guidance](https://developer.apple.com/library/archive/documentation/General/Conceptual/ExtensibilityPG/ExtensionScenarios.html) also separates short-lived UI from queued transfers. A research candidate is to retain unknown work pending and offer the same integrated native wizard when a permitted foreground interaction is available. Known accepted rules may already handle a class automatically. This preserves the before-transfer condition without promising an unrestricted background popup; pending persistence has not been implemented or tested.

Android's [update contract](https://developer.android.com/google/play/app-updates) requires a matching application ID, compatible signing identity and an admitted version code. A derivative signed with an unrelated key cannot simply inherit the official signed update stream as if unchanged. Apple app extensions are packaged with their containing app; an independently built app/extension needs its own legitimate signing/distribution route. The inspected [iOS setup guide](https://github.com/opencloud-eu/ios/blob/c958854e1c3e695552f383de3f401cac41753d1c/SETUP.md) calls for app/group identifiers and signing setup; its older toolchain examples are not current build acceptance. Apple's [version update guidance](https://developer.apple.com/help/app-store-connect/update-your-app/create-a-new-version/) uses the app's existing record. This research does not choose a store, acquire a signing identity or establish official vendor distribution support.

Retained-copy semantics need explicit proof. The inspected iOS manual-import cancellation removes local import copies; this does not establish deletion of the original source, but existing Cancel cannot simply be equated to Keep locally or Wait. Android's manual path records a MOVE local-behavior value while passing COPY to its subsequent upload use case; the actual retention outcome needs a trial rather than inference from labels. No wizard exit, narrowing rule or failed upload may silently destroy the only retained copy.

## All-device knowledge is an additional unproved contract

The required device list must represent named owner-registered devices, including offline devices, their supported availability modes, rule targets and application feedback. Tokens and login sessions are not that authoritative inventory.

The inspected [auth-app API](<https://github.com/opencloud-eu/opencloud/blob/v7.2.4/services/auth-app/README.md>) lists token records with identifiers, creation/expiry and labels. The [Graph service overview](<https://github.com/opencloud-eu/opencloud/blob/v7.2.4/services/graph/README.md>) documents user/group/role/Space surfaces; the [clientlog service](<https://github.com/opencloud-eu/opencloud/blob/v7.2.4/services/clientlog/README.md>) describes notifications delivered through SSE. The [Web options](<https://github.com/opencloud-eu/opencloud/blob/v7.2.4/services/web/pkg/config/options.go>) can link logout to an external identity provider's sessions/devices view. None of these inspected surfaces established the complete device-catalogue/capability/effective-policy contract required by the wizard. This is a bounded gap finding, not a universal claim of absence.

Reusing an existing device-enrollment source or providing a small owner-controlled catalogue are research options. The exact authority, device lifecycle, capability freshness and acknowledgement contracts remain open. This does not introduce multi-party or per-source access rights. The Uppy Companion setting in Web configuration is an external-cloud import helper; its name is not evidence of this MyBrain client companion.

## Ways to preserve updates

| Route to investigate | Fit to integrated native experience | What update preservation actually means |
| --- | --- | --- |
| Maintainer-supported UI/admission contract | Best fit if native presentation and every claimed transfer path are supported. No such complete independent contract was established here. | Upstream accepts and maintains the contract; a separately versioned wizard/policy module is tested against supported host versions. Acceptance and delivery are unknown. |
| Minimal maintained native changes with reusable shared logic | Can target existing desktop and mobile UI/queue boundaries. Needs separate platform integration and a complete bypass inventory. | Rebase or otherwise integrate upstream changes, rebuild, sign/package and run regression/upgrade checks. A small diff still has an ongoing maintenance cost. |
| Desktop version-bound provider/internal wrapper | A possible bounded desktop experiment, not a cross-platform solution or proven hold. | Rebuild against the exact supported client version; verify UI, provider modes, startup/retry and upload paths on every admitted upgrade. |
| Separate companion using owned transfers | Can reuse storage/protocols and reduce native patching on routes it owns. | Official clients may keep receiving their updates, but the separate workflow does not satisfy the accepted native-app experience by itself. It requires an explicit owner reconsideration if proposed as a replacement. |

A shared wizard can reuse user-facing vocabulary and policy descriptions, but a shared screen alone cannot unify platform-specific queues, filesystem access and enforcement. Shared policy/rule backend work is still unimplemented. No fork, external contribution, SDK stack, rule schema or compatibility strategy is selected by this checkpoint. A separate mobile app identity/signing/App Group also leaves access to existing app data, re-enrollment and migration of retained local copies unresolved; an in-place replacement of the official app is not assumed.

## Small proofs required before a maintainable-solution claim

These are proposed tests, not executed results. Use synthetic data and isolated roots/accounts. Before running anything, select actual client/server/SDK versions and the exact claimed integration seam; establish a stock control and independently observe all relevant requests, including creation bodies.

| Proof | Required observation |
| --- | --- |
| One integrated decision | One grouped native flow/summary/confirmation includes storage, device choices and supported availability, MyBrain yes/no and reusable scope. No separate later MyBrain prompt is required to complete the intention. |
| Unknown and known classes | Closing/defer/unavailable policy leaves unknown content pending with no content upload; one accepted reusable rule handles subsequent matching files without per-file manual review. |
| Complete upload-path control | Desktop discovery/edit/retry and initial TUS POST, Android manual/automatic/provider routes, iOS main import/Share/File Provider/media scheduling are tested or explicitly declared unsupported. |
| Mobile background behavior | Background discovery retains pending work until an allowed native interaction; terminating/restarting the app/extension does not release unapproved transfers or lose the decision. Cancel, wait, local-only and success cleanup preserve the intended retained copy. |
| Real device inventory | A second registered, offline, new and retired device is represented truthfully; unsupported availability choices are explained. Saved intent is distinguished from receipt, applied rule and actual result. |
| Consistent intent and independent execution | One confirmed rule retains both synchronization and MyBrain choices. Partial failure is visible without silently splitting off or dropping the MyBrain intention. This is not an assumed distributed transaction. |
| Snapshot and rule changes | Edit/replace between individual approval and send, deliver older rule revisions and reconnect stale devices; no stale permission silently authorizes changed content. Rule narrowing does not delete retained copies. |
| Actual version upgrade | Use two explicitly selected real client/host versions and the intended signed update path. Preserve decisions/pending work, re-run native entry routes and verify the wizard and hold survive. Source compilation or a same-version restart alone is insufficient. A stock update that cannot load the custom integration must leave undecided content held rather than silently resume uncontrolled synchronization. |

The pending observation-to-source-registration boundary still follows P18/P19/P38 in the [foundational principles](../../architecture/decisions/0001-digital-brain-foundational-principles.md). A worklist must not silently become a second authoritative source registry or permanently register every excluded cache. Metadata disclosure, offline use of prior rules, retention and future-device defaults remain policy questions.

## Research conclusion and decision boundary

The accepted user experience can be described clearly and there are concrete owned-code integration points to test. The evidence does not establish an update-independent addon that delivers the entire requirement inside unchanged official apps. The strongest long-term route to investigate is a maintainer-supported native UI/admission contract; a small maintained native change set is a plausible fallback with its own release obligations. These are recommendations for investigation, not adopted implementation strategy.

Before Design, the owner must choose the acceptable maintenance/compatibility route based on proof, and resolve device authority, candidate disclosure and offline rule applicability. This checkpoint stays in Research. No prototype, upstream acceptance, binary upgrade or compatibility matrix has been demonstrated.

## Related Documents

- [Canonical issue-9 research](<research.md>)
- [Preserved earlier source assessment](<opencloud-admission-extension-feasibility.md>)
- [Issue 9](<https://github.com/MikeyVK/MyBrain/issues/9>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-05 | Codex (@imp researcher) | Record the accepted integrated native wizard and assess desktop/mobile seams, device inventory and update-maintenance alternatives. |
| 1.1 | 2026-11-05 | Codex (@imp researcher) | Link accepted offline/local/shared policy distinctions and the canonical unexecuted reconciliation probe contract. |
