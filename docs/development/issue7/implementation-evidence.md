<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Portable deployment implementation evidence

**Status:** IMPLEMENTATION — final C_3 independent review requested
**Version:** 1.3
**Last Updated:** 2026-10-28

## Purpose

Record actual cycle evidence and remaining package obligations for issue 7.

## Summary

C_1-C_3 producer evidence is complete for frozen r6 with explicit proportional reuse of unchanged r5 core evidence; earlier verdict identities remain intact and new independent review is pending.

## C\_1 contract verification

`python -B setup/deployment/tests/test_contracts.py` at RED commit 694557f25aef6fea5b5da1e245a169775ba7cf3a: 15 intended assertion failures across eight tests; the executable CLI incorrectly admitted corruption, missing/extra files, wrong schema and unsafe/duplicate names. Current focused contract run: 14 tests passed, including preflight read-only behavior, actual ZIP extraction and source-original hash refusal. `python -B setup/deployment/tests/test_journal.py`: three tests passed for reruns/edits, live/stale locks and retained incomplete-stage quarantine.

## Authoring route and quality boundary

Normal python_class scaffolding refused persistence with configuration_choice_required on the deliberately deferred python_syntax binding, including report mode. Co authorized the existing technical setup/build route for deployment Python and PowerShell sources; no binding was enabled or relaxed. Manual syntax/public process evidence is distinct from native application gates. Required Markdown/YAML/schema checks remain required.

## Dependency observations

Official CPython 3.15.0 Windows x64 ZIP verified against the published release-manifest SHA-256 6b1a3f885ce416cf3a68af203e62203664eb5224d8d0c1d2a1945fddec5c500b. Binary-only fetch could not find a published PyYAML 6.0.3 wheel; the documented PYYAML_FORCE_LIBYAML=0 pure-Python local wheel is available with original source archive provenance. Full license/closure/target install evidence remains in C_2.

## Related Documents

- [Planning](<planning.md>)
- [Design](<design.md>)

## C_2 actual provisioning evidence

- RED e3fe25745ebab1a5173e3d9a82b450453ae68d68 exposed a source-restoration boundary that returned without creating required bytes. Current provisioning tests pass for exact restore/customization preservation, separate committed/working overlays with private-family exclusion, and parsed target-only role/binding rendering.
- Candidate 01 failed isolated sibling-module import before source restoration; candidate 02 restored source and installed the environment but stopped on package-consumer ownership accounting. Both failures were retained; neither is represented as completed setup. Corrections were applied to new candidates.
- Candidate 03 ran the public Bootstrap.ps1 with Windows PowerShell 5.1 and PATH empty. It used bundled CPython 3.15.0 x64 and the 49-wheel hash lock, downloaded the exact declared MinGit 2.56.0.4 fallback (e3bf78351fe777fba47ddee5950082f8a98bb0f02604fdc7ba3ee2cb68ffa877), initialized/added/committed standalone main and verified clean source status/no remote. New trial commit: 3f0114ac18422a3a13e347591a4247c79af4f2e6. pip check reported no broken requirements.
- The generated target registration was launched directly via STDIO, without source PGMCP variables or GitHub token. Native execution: Markdown positive passed/negative failed; YAML mapping positive passed/sequence negative failed; JSON Schema shape and metaschema positives passed/metaschema negative failed. Expected native exits were 0/1; sibling-only relative fixture was absent/refused. No active issue was created. This proves that generated launch route, not actual Codex host activation.
- Trial package manifest digest: 16fe2ab0584b1056dffac1fccb890399e20e04561ad6543a9344744d27f7bd42. This is candidate-directory evidence, not the final ZIP identity. Git fallback was exercised, not merely version-probed. Python/native dependencies and licenses are bundled; MinGit is a specifically declared primary-download fallback because its complete corresponding-source redistribution closure was not admitted. Package status is hybrid. MPL/LGPL/local-PyYAML corresponding source archives and all available wheel/runtime/native license notices are retained.
- Target login/trust/actual Codex activation and second-PC/VM evidence remain unavailable. No offline or clean-machine claim is made. Final archive extraction, rerun and interrupted public recovery remain C_3 obligations.

## C_3 rejected release and recovery correction

- Frozen build input 871fddcea32b591ca21c84494141dbd66b928e16 produced a real 80,131,754-byte r2 ZIP, SHA-256 d84bf85f66112473e91cb71b688b99ff2ff7209a2a4489c10c0871941ee1c322. This is a rejected trial, not the final accepted artifact.
- Windows PowerShell 5.1 Test-Package ran r2 with fresh extraction, empty PATH and deliberately wrong inherited Git/pip/PYTHONPATH/TEMP values. First bootstrap completed source/Git/environment/server/consumer/native verification; standalone Verify and Bootstrap rerun completed. Normal public Recover Resume then failed with PermissionError before the interruption case. No final archive-journey success was claimed.
- Diagnosis preserved r2 and its complete 641,203-byte pending journal, byte-identical to the current journal (both SHA-256 36975dcd07117423c2166f46b3bf84037b8632b1dc22628c0ddbb61c0327304a). A Windows reader without delete sharing reproduces WinError 5 exactly at atomic metadata replacement. The actual earlier lock holder was not captured and is not asserted.
- Correction skips unchanged metadata writes, checks unchanged target bytes during a bounded Windows replacement retry, and preserves pending metadata in quarantine only under explicit recovery after checking the writer is not live. Pending bytes are never silently deleted or adopted. Added meaningful regressions failed on old behavior, then all five journal tests passed. CLI execution failures now retain a full traceback.
- Current focused evidence: Contracts 14, Journal 5, Provisioning 5 and Archive 1 tests passed; manual Python compilation and PowerShell parsing passed. Native changed-family Markdown and both JSON Schema checks passed. A fresh corrected archive still requires its own actual public journey and independent digest-bound review.

## C_3 rejected r3 historical producer evidence

### Artifact identity and source cutoff

C_1 D_1.1-D_1.2, C_2 D_2.1-D_2.2 and C_3 D_3.1-D_3.2 have the implementation evidence below and in the earlier sections. Independent final-cycle/phase/archive review is requested; no GO is inferred. Validation and Documentation phase deliverables remain separately scheduled by Co.

| Item | Frozen value |
| --- | --- |
| Build-input revision | 3d1e4d855e1efdc18584ac3d7047347cced0fb5e |
| ZIP | `build/deployment/mybrain-windows-x64-20261028-r3.zip` |
| ZIP size | 80,133,775 bytes |
| ZIP SHA-256 | 01e1773d833775015616ff08fdde29b7ed39497caa0855d9aea5442d44468c78 |
| External outer digest | Same ZIP path plus `.sha256` |
| Manifest | `build/deployment/mybrain-windows-x64-20261028-r3/manifest.json` |
| Manifest SHA-256 | a89ed2727ed756271e09113b7cf24728a6473a09a6f8f073f6797c1f0a18d6ff |
| External final journey evidence | Same ZIP path plus `.verification.json` |
| Package handover | Staged `agent-handover.md` and `START-HERE.md` |
| Source capture UTC | 2026-10-28T12:10:09.992063+00:00 |

The ZIP contains the committed build input, not this later evidence update. Since that build input only this evidence document changes; no packaged runtime/source/instruction bytes are changed by this handover. Manifest and detached manifest digest avoid self-reference; the final own-archive report and outer digest remain outside the ZIP.

Original source refs are `feature/7-portable-workspace-deployment` at the build-input SHA, `main` at 84d5e0cbbe488fd45160de64d5faab9a97ba7687, and `feature/6-mybrain-storage-foundation` at 655e9563ba5536d24d9db3c98ef5819ae40feff4. Captured trees contain 69 deployment, 41 integrated and 53 active-storage source files; two historical workflow files per applicable source are separate provenance, never active target issue state. The donor source represents its frozen documentation/setup progress, not completed storage implementation.

One selected safe local original, `setup/local/find-postgresql-download.py`, is retained separately and exactly (SHA-256 537fcc9338408de2a7d25728d5660a671b7d2a09fa704513d0b6229fc8fe4dc2), alongside generated target configuration. Nine other local setup candidates have explicit screened exclusion reasons. Original history/worktree metadata, private runtime/account data and unsafe/private source candidates are excluded. Source roots and machine identifiers remain in ignored local capture/evidence only. Restored main is a newly committed standalone repository without origin, inherited active issue or inherited approval. Source snapshot provenance distinguishes original and new identities; safe later remote reconciliation is documented in the shipped instructions.

### Actual public release journey

Windows PowerShell 5.1 ran the following against the actual r3 ZIP, with empty PATH and deliberately wrong inherited Git repository/configuration, pip install-routing, PYTHONPATH and TEMP/TMP values:

```powershell
& setup/deployment/Test-Package.ps1 -Archive build/deployment/mybrain-windows-x64-20261028-r3.zip -Destination 'tmp/i7 release r3'
```

The driver completed with exit 0 and `local_archive_journey_verified`. It checked members before fresh extraction, exact extracted inventory/hash/source reconstruction and the unchanged outer digest. Initial Preflight returned 0; initial Bootstrap returned the expected 2/`local_tooling_verified_host_activation_pending`. Its subsequent recorded public outcomes were:

| Operation | Observed result |
| --- | --- |
| Verify | 2; local tooling verified, host activation pending |
| Bootstrap rerun | 2; same expected pending state |
| Recover Resume on complete destination | 2; same expected pending state |
| Bootstrap after editing owned README | 4; changed_owned_output, edited bytes preserved |
| Bootstrap into foreign destination | 4; foreign_destination, sentinel preserved |
| Recover Resume after actual environment-process interruption | 2; completed with four partial environment files retained exactly in quarantine |
| Recover DiscardStaging on verified stage bytes | 0; verified_staging_discarded |
| Recover DiscardStaging after changing stage bytes | 4; changed_staging_preserved, exact changed bytes preserved |
| Final Verify | 2; same expected pending state |

The interruption terminated only the test's own launched process tree after the environment stage was running and its real venv Python existed. Recovery then completed all stages. The test restored/removed only its own known edit fixtures; unrelated sentinel bytes remained unchanged. The rejected r2 ZIP/logs/pending metadata remain preserved and are not reused as final verification evidence.

The empty-PATH missing-Git route downloaded only the declared pinned fallback, then actually initialized, added, committed and status-checked the restored standalone repository. Bundled CPython 3.15.0 x64 created a new venv and installed the exact hash-pinned 49-wheel closure without index/source compilation; harness 4.0.0 and pip consistency were verified. No copied venv or source Git/Python executable was required.

The actual generated target STDIO registration executed four native positives (Markdown, YAML, JSON Schema shape/metaschema) with exit 0 and three intended negatives with exit 1. The sibling-only fixture was absent/refused and no active issue existed. The actual generated launch rejected inherited poison; synthetic source/global PYTHONPATH was not imported, Git inspection did not bind to the unrelated repository and pip did not create the redirected install/index outputs. Managed temporary/cache output belongs to the target. No host/global configuration was changed.

### Focused checks and reproduction index

Focused technical evidence passed: Contracts 14, Journal 5, Provisioning 5 and Archive 1 tests, including both Windows metadata regressions. Their drivers are `setup/deployment/tests/Invoke-DeploymentTests.ps1 -Suite Contracts`, `-Suite Provisioning` and `-Suite Archive`. Python syntax compilation and native PowerShell parsing passed. These are authorized deployment build/smoke results; inactive application checks/tests were not represented as passing.

Changed-family native Markdown and schema shape/metaschema checks passed before freezing. The generated final manifest instance additionally passed `run_checks(scope="targets", targets=["build/deployment/mybrain-windows-x64-20261028-r3/manifest.json"], checks=["json_schema_shape"], args={"json_schema_shape":["--schemafile","setup/deployment/manifest.schema.json","--force-filetype","json","--output-format","JSON"]})`: check-jsonschema 0.38.2, exit 0, no errors. The initial incorrectly shaped caller argument was rejected before execution, then corrected to the admitted per-check object. Final evidence editing uses the enforced native Markdown gate. Unchanged YAML source needs no duplicate source check; actual generated YAML/native consumer admission was exercised.

Primary review entrypoints:

- [Public build/bootstrap/recovery documentation](../../../setup/deployment/README.md), [detailed target instructions](../../../setup/deployment/START-HERE.md) and [short target handover](../../../setup/deployment/agent-handover.md).
- [Manifest/schema contract](../../../setup/deployment/manifest.schema.json), [contract enforcement](../../../setup/deployment/contracts.py) and [journal/recovery](../../../setup/deployment/journal.py).
- [Fixed source/archive builder](../../../setup/deployment/builder.py), [source reconstruction](../../../setup/deployment/sources.py), [actual provisioning](../../../setup/deployment/provision.py) and [generated launch/native probe](../../../setup/deployment/probe.py).
- [Actual archive journey](../../../setup/deployment/release_tests.py), [contract tests](../../../setup/deployment/tests/test_contracts.py), [journal regressions](../../../setup/deployment/tests/test_journal.py), [provisioning tests](../../../setup/deployment/tests/test_provisioning.py) and [archive test](../../../setup/deployment/tests/test_archive.py).

### Explicit remaining limits and target-agent message

The distribution is hybrid: the only declared online dependency is primary MinGit 2.56.0.4 at its fixed Git-for-Windows release URL, SHA-256 e3bf78351fe777fba47ddee5950082f8a98bb0f02604fdc7ba3ee2cb68ffa877, used when adequate Git is missing. It was not redistributed because complete corresponding-source closure was not admitted. Runtime/wheels/native tool licenses/notices and applicable MPL/LGPL/PyYAML source archives are retained; the locally built pure-Python PyYAML wheel and its source provenance are disclosed. No target compiler or unpinned latest/index fallback is assumed.

Generated direct launch/native proof does not establish actual Codex host activation. Target Codex installation/sign-in if absent, project trust and loading/verifying each intended named role connection remain explicit host actions. No clean second-PC/VM or fully offline test was performed. No current implementation blocker remains; independent C_3/archive review, later scheduled phase work and those external host facts remain pending. No Validation transition, remote publication or private-data migration occurs here.

Exact target-agent message:

> Verify the ZIP against the supplied outer SHA-256, read START-HERE.md, and run Preflight.ps1, Bootstrap.ps1 and Verify.ps1 into one new Windows x64 destination using the same -Destination. Preserve conflicts; read installed AGENTS.md and effective PGMCP bootstrap/protocols. Report actual local/native results and remaining Codex login/trust/named-connection activation. Exit 2 is expected only with local_tooling_verified_host_activation_pending. Do not import private data/accounts, invent issue state, inherit old QA or force-push/overwrite origin.

## C_3 correction after independent runtime-inventory NOGO

Original Qa_a verdict MIGRATION-I7-IMPLEMENTATION-QA-1 rejected source revision 1254c854fa2fbc1e50e3017158a20637a11cb1d9 and r3 ZIP digest 01e1773d833775015616ff08fdde29b7ed39497caa0855d9aea5442d44468c78. Its P1 identified a pre-interpreter admission gap: expected CPython files were hashed, but unexpected runtime files were not rejected until later. R3 and all prior reports remain rejected historical trials, despite their successful ordinary journeys. QA's additional complete-installation probe was not executed and supplies no evidence.

The narrowly scoped correction compares the complete local runtime file and directory inventory to the verified CPython archive before any interpreter invocation, then checks every expected original hash. Unknown contents receive no extension/cache exemption; conflicts are preserved. The previous ordinary installed runtime had no extra managed byproducts outside that archive inventory.

The safe [native regression](../../../setup/deployment/tests/Test-RuntimeAdmission.ps1) uses an inert extra text file, an empty extra directory and modified inert license bytes. Meaningful RED 1c373d3a71ccf08cc2e3e24763e13d8290908029 returned extra_file_admitted and extra_directory_admitted; no interpreter was started by that RED. The first draft test harness had stopped on the downstream missing helper and was corrected before recording meaningful RED. GREEN subsequently passed: Bootstrap, Verify and Recover each returned 4/runtime_inventory_mismatch for the inert extra; file/directory/changed-license contents and unrelated sentinel were preserved. Exact baseline admission succeeded again. Structural ordering inspection confirms inventory admission precedes the interpreter call. The regression command used the verified CPython ZIP and fresh ignored destinations.

The existing generated-launch probe was changed to inert context.txt only. No startup module, executable payload or code marker probe is repeated; historical marker claims in the r3 section are not new correction evidence. Ordinary generated-launch/native/root and inherited Git/pip environment checks remain active. Existing focused tests all passed again (14 Contracts, 5 Journal, 5 Provisioning, 1 Archive); Python syntax compilation and native PowerShell parsing passed. A newly frozen archive and complete normal actual-ZIP journey are still required before this correction's handover.

## C_3 bounded Git-stage promotion correction

R4 build input 2453a3edd798d1d1263c33d4070577348c1fcfb0 produced a real 80,141,153-byte ZIP, digest 05982ebf5a39c9cef08f1243aa2282993ff1af6a70c759491dd2f852a6a9c7b6. Its initial ordinary journey passed bootstrap/verify/rerun/normal resume/conflicts but stopped at its own taskkill exit 128. That driver's older error did not expose native stdout/stderr, so the exact reason is not asserted. A single fresh r4b repetition stopped before interruption on WinError 5 promoting managed Git staging. Neither is complete final-journey evidence, and both logs/trees remain preserved.

Read-only diagnosis found the r4b staging inventory exactly 375/375 files/hashes matching pinned MinGit; destination absent, no remaining own test processes. Archive/file streams close before promotion and no Git execution/validation occurs between extraction and rename. The earlier lock holder/cause remains unknown; no antivirus or own-validation cause is claimed.

Co scheduled a narrow correction to this proven managed promotion seam. Meaningful RED fcc0bc008fdb391fcc4e148687ead88e774396bd kept the original rename behavior behind the selected seam and exposed real Windows sharing failures plus changed/foreign staging admission. GREEN [Git promotion tests](../../../setup/deployment/tests/test_git_promotion.py) passed six inert cases: temporary reader without delete sharing then release, persistent lock with finite refusal, foreign destination, changed bytes, unexpected bytes and stage change during waiting. No executable startup fixture is involved.

Only Windows errors 5/32/33 receive at most 20 attempts and 19 waits of 50 ms (0.95 seconds wait budget). Before each attempt, the caller's owned stage is checked for reparse paths, unchanged owner metadata, absent destination and exact archive file/directory membership/hashes. Changed/foreign content stops, permanent lock preserves the original OSError chain and diagnostic, and no byte is removed/adopted/overwritten. The existing public journal exclusive lock remains held by the caller.

The actual interruption driver now exposes its own taskkill step, PID, return code, stdout and stderr on every nonzero outcome. It does not accept exit 128 or change the existing interruption conditions. Contracts 14, Journal 5, Provisioning 5, Git promotion 6 and Archive 1 tests all passed (31 total); Python compilation and native PowerShell parsing passed. Runtime inventory and inert generated-launch probe remain unchanged from the bounded P1 correction. New r5 archive/manifest/actual journey evidence remains required before final review.

## C_3 r5 historical review handover

This supersedes the rejected r3 and incomplete r4/r4b journey evidence for review. Producer verification is complete; independent final C_3/implementation/archive review remains required.

| Item | Final frozen identity |
| --- | --- |
| Build-input revision | 39eb07fb385c9c5fc3090037891bfa3d0d918930 |
| ZIP | `build/deployment/mybrain-windows-x64-20261028-r5.zip` |
| Size | 80,145,620 bytes |
| Outer SHA-256 | dbbeacb4768e3e1b435779cd35ae7383732ab9a0e3122baa4ba15c066ab0a590 |
| Detached outer digest | Same ZIP path plus `.sha256` |
| Manifest | `build/deployment/mybrain-windows-x64-20261028-r5/manifest.json` |
| Manifest SHA-256 | f7897648d7f6add3fc003b5c8923a8abed86cc786e66302ffa91f0fae66f6e9b |
| External own-archive journey report | Same ZIP path plus `.verification.json` |
| Capture UTC | 2026-10-28T13:20:07.820057+00:00 |

Deployment source is the build-input SHA above, original ref `feature/7-portable-workspace-deployment`. Original main and active-storage cutoffs remain respectively 84d5e0cbbe488fd45160de64d5faab9a97ba7687 and 655e9563ba5536d24d9db3c98ef5819ae40feff4; selected local original bytes/exclusions remain as recorded earlier. The final source snapshot contains the committed corrections, while this subsequent final evidence edit remains outside the frozen ZIP. After build input only this evidence file changes. Historical state/QA remains provenance, not active issue/approval; new standalone Git has no origin.

On Windows 10 build 19045, Windows PowerShell 5.1 ran:

```powershell
& setup/deployment/Test-Package.ps1 -Archive build/deployment/mybrain-windows-x64-20261028-r5.zip -Destination 'tmp/i7 release r5'
```

The one fresh r5 journey completed with exit 0/`local_archive_journey_verified`. PATH was empty; wrong inherited Git/pip/PYTHONPATH/TEMP values pointed only to an inert context fixture. No startup module/payload/marker-code execution probe was performed. Archive membership, extraction, exact hashes and source reconstruction were verified from these actual ZIP bytes.

Initial Preflight returned 0 and initial Bootstrap returned expected 2/`local_tooling_verified_host_activation_pending`. All nine subsequent public operations matched their required outcomes: Verify, Bootstrap rerun and normal Recover Resume returned expected 2; edited owned README and foreign destination each returned 4 with bytes preserved; Recover Resume after actual interruption returned expected 2; verified staging discard returned 0; changed staging discard returned 4 preserving bytes; final Verify returned expected 2. Exact codes are in the external report.

Both fresh Git promotions completed. The controlled own-process taskkill passed its unchanged strict nonzero-refusal condition, rather than accepting exit 128. It stopped the real running environment stage; resumed bootstrap preserved four partial environment files exactly in quarantine and completed every stage. Unrelated sentinel remained unchanged. The previous r4/r4b trees/logs remain untouched and are not represented as successful journeys.

Real target-local CPython 3.15.0 x64, harness 4.0.0, hash-pinned wheel install and pip consistency were observed again. The empty-PATH route used the exact online MinGit fallback to initialize/add/commit/status-check standalone main. Generated direct STDIO launch again executed four native positives with exit 0 and three intended negatives with exit 1, refused/omitted the sibling-only fixture and created no active issue. This is ordinary inert-context launch/root/native evidence, not a repeat of any historical startup-marker probe.

The safe runtime regression was rerun on the final frozen input using `tests/Test-RuntimeAdmission.ps1 -RuntimeArchive <verified CPython ZIP> -Destination 'tmp/i7 runtime r5'`: passed. Extra inert text caused Bootstrap/Verify/Recover each to return 4/runtime_inventory_mismatch before interpreter startup; exact fixture bytes and sentinel were preserved. Unknown empty directory and changed original license bytes were refused/preserved, and exact baseline admission succeeded again. The runtime launcher itself is unchanged from the P1 GREEN and included byte-for-byte in the verified r5 manifest.

All 31 focused deployment tests and syntax/parser checks passed for these inputs. Native final manifest-instance validation passed with the same explicit per-check schema arguments recorded earlier, now targeting r5 manifest.json; check-jsonschema 0.38.2 exited 0. Final evidence edits pass enforced Lychee 0.24.2 with configured offline/fragment arguments. No changed YAML/schema source or deferred application check/test is claimed as newly executed.

Package handover entrypoints remain staged `START-HERE.md` and `agent-handover.md`; the exact copyable target-agent message is recorded above and unchanged. The package remains hybrid only for its enumerated pinned Git download. Licenses/source notices and public-safe source-byte retention remain intact. Actual Codex login/trust/named-host activation, clean second-PC/VM and fully offline proof remain unavailable and explicitly pending. No remaining producer implementation blocker is claimed; independent C_3/archive review and later Co-scheduled phase work remain open. Review requested; no Validation transition or remote publication.

## C_3 read-only Preflight and coverage correction

Original Qa_a verdict MIGRATION-I7-IMPLEMENTATION-QA-2 rejected review revision 7c1e65eec46524d1a259bd9a210257599c026629 and r5 digest dbbeacb4768e3e1b435779cd35ae7383732ab9a0e3122baa4ba15c066ab0a590 solely on P2: missing Git/network availability checks in native Preflight. Earlier runtime P1, safe inventory/Windows sharing cases and the complete r5 journey/native/source/license evidence were independently accepted where unchanged; that does not turn r5's overall NOGO into GO.

Meaningful RED 1a7893f6191345cabb62bc3bb5b6407df9c665d4 observed public Preflight returning 0 when required transport was unavailable/unproved and omitting required Git/network facts. Test-host preparation issues (inherited PS7 module path and native null/empty environment representation) were resolved before that RED; they are not behavior proof.

GREEN [Preflight tests](../../../setup/deployment/tests/test_preflight.py) now pass five tests/six paths: actual suitable host Git without download/network probe, required fallback with exact declared-URL deterministic reachability, unavailable and throwing/unproved transport returning 2/git_download_unverified, verified owned cache without network, and changed cache returning 4 while preserving bytes. All paths compare package/target file bytes and caller routing/parent environment before/after; absent destinations remain absent. Transport fixtures do not prove live connectivity. A separate real Windows PowerShell 5.1 source-level HEAD to the exact pinned Git URL returned HTTP 200 without requesting a response body; fresh r6 archive-level evidence remains pending.

Git suitability checks version >=2.51 and required builtin commands in an isolated bounded read-only child, rather than only git --version. Existing owned local Git inventory/hashes are checked before probing; verified cached prerequisites avoid network. Only a needed fallback triggers the exact declared primary HTTPS HEAD, bounded to an eight-second async wait and at most three redirects, with no credentials/default-auth or artifact download. Missing/unproved availability remains pending, while changed owned/cache bytes stop as conflicts. Preflight never creates the destination.

Included START-HERE, short agent handover and deployment README now state the exact delivered dev-workspace/CPython/PGMCP/native-quality/roles/bindings scope. The active-storage snapshot contains future issue 6 PostgreSQL 18 design/operations/acceptance inputs, with no app/src/API/UI/migrations; the sole selected local helper only finds vendor URLs. Bootstrap does not install PostgreSQL, a MyBrain schema/empty product storage or a running application/API/UI. No new database/application setup or private-data transfer is introduced.

Co relayed the owner's explicit proportional verification: refresh r6 archive extraction/membership/hash/source and affected native Preflight/docs/syntax/inventory boundaries. Reuse the independently observed r5 recovery/native/whole-journey evidence only for byte-identical core, retaining its own source/ZIP identity and overall P2 NOGO. Do not rerun unchanged recovery/native flows automatically, and do not relabel them as r6 execution or independent approval. The new r6 digest still requires a matching independent exact-revision/archive verdict.

## C_3 final r6 proportional review handover

This is new producer evidence for r6, not a blanket inheritance of old QA. Original QA-2 remains an overall NOGO on r5's Preflight P2 until a matching new independent verdict addresses this revision and ZIP.

| Item | Frozen value |
| --- | --- |
| Build input | ecdb66717c7887427f7a5ca4819ff2dd3b7fae95 |
| ZIP | `build/deployment/mybrain-windows-x64-20261028-r6.zip` |
| Size | 80,158,029 bytes |
| Outer SHA-256 | 96529ff8f3ed018d3d6d4b903eca3cbcf465525a8a9cd67f8ba989ac13f65e01 |
| Manifest | `build/deployment/mybrain-windows-x64-20261028-r6/manifest.json` |
| Manifest SHA-256 | a947202f79d5eff65cd5c7af554c0a0c4e1228ff0b90a5d44df7b72a782198f5 |
| Detached outer digest | Same ZIP path plus `.sha256` |
| External scoped verification | Same ZIP path plus `.verification.json` |
| Capture UTC | 2026-10-28T14:08:46.866656+00:00 |

The actual ZIP was inspected before fresh extraction into `tmp/i7 release r6/package`; all 385 members and inventory/hashes passed. PackageVerifier checked source reconstruction; 167 deployment/integrated/development source files were additionally compared directly with their original immutable Git objects. Main 84d5e0cbbe488fd45160de64d5faab9a97ba7687 and donor 655e9563ba5536d24d9db3c98ef5819ae40feff4 cutoffs remain unchanged. Historical workflow files and the separately retained selected local original remain distinguished by provenance/hash, without raw ancestry or active issue inheritance. No donor mutation occurred.

Fresh actual-package public Preflight evidence:

| Case | Result |
| --- | --- |
| Real host Git 2.51, required commands available | 0/preflight_verified; no download/network needed |
| Empty PATH, absent Git and new destination | 0/primary_reachable from actual bounded HEAD of the exact declared primary URL; download/network explicitly required |
| Missing Git, deterministic unavailable transport | 2/git_download_unverified; destination absent |
| Missing Git, deterministic throwing/unproved transport | 2/git_download_unverified; destination absent |
| Actual pinned MinGit cache prepared by the test before Preflight | 0/verified_target_cache; no transport call or download |
| Exact owned local MinGit inventory prepared by the test before Preflight | 0/target_verified_inventory; real read-only Git probe succeeded, no transport call or download |

Every case compared package/target file inventories and caller state before/after. Preflight made no destination and downloaded no artifact. The cached/local fixtures were prepared by the verifier, not by Preflight. Unavailable/unproved tests are deterministic transport fixtures, not physical network-disconnection evidence. The actual missing-Git case separately used the real default HTTP HEAD implementation. A separate source-level live HEAD also observed HTTP 200; no response-body download or credential enumeration was performed.

Reproduction/index: `build/deployment/verify-r6.py` is the ignored local verifier; its digest-bound report sits outside the ZIP. It invokes the extracted `Preflight.ps1 -Destination <fresh path>` for real host/HEAD cases and the [public fixture harness](../../../setup/deployment/tests/Invoke-PreflightFixture.ps1) for deterministic transport refusal/no-call cases. The new [Preflight tests](../../../setup/deployment/tests/test_preflight.py) passed five tests/six paths, including changed-cache preservation. The affected `Invoke-DeploymentTests.ps1 -Suite Contracts` passed 24 tests (14 existing contracts, 5 existing journal cases, 5 new Preflight tests). Python syntax compilation and native PowerShell parsing passed.

The safe native `Test-RuntimeAdmission.ps1` was rerun for r6 input: passed. Inert extra text still caused Bootstrap/Verify/Recover each to return 4/runtime_inventory_mismatch; extra directory/changed original bytes were refused and preserved; exact baseline and sentinel were retained. No startup/payload/marker-code probe was repeated.

Reuse is narrow and explicit: comparison against r5 proved 14 packaged core files unchanged, all 12 pre-existing shared helper functions unchanged, the non-Preflight dispatch tail unchanged and dependency closure identical. This includes runtime admission, ownership/extraction, Python provisioning/journal/Git promotion, actual native probe and recovery/interruption driver. Their independently observed r5 full journey/native/license evidence remains attached to build input 39eb07fb385c9c5fc3090037891bfa3d0d918930, review revision 7c1e65eec46524d1a259bd9a210257599c026629 and ZIP dbbeacb4768e3e1b435779cd35ae7383732ab9a0e3122baa4ba15c066ab0a590. It is not relabeled as r6 execution or approval. New Bootstrap/Verify/recovery/native integration was not rerun because the executed core/dispatch is byte-identical and the owner explicitly requested proportional verification of the actual Preflight/documentation delta.

Native r6 manifest-instance validation passed with the earlier explicit schemafile arguments, check-jsonschema 0.38.2 exit 0. Changed source Markdown/handover documents passed enforced Lychee 0.24.2; no YAML/schema source changed. Deferred application bindings remain unchanged and no application-test pass is claimed.

Included START-HERE and agent-handover are now self-contained about coverage: development workspace/Git, CPython/PGMCP/quality/roles/bindings are supplied; issue 6 storage documents are future PostgreSQL 18 implementation inputs and the selected helper is only a vendor-URL finder. PostgreSQL server, MyBrain schema/empty product storage and a running app/API/UI remain unimplemented/unproven. Hybrid pinned Git, target login/trust/actual named-host activation and absent second-PC/VM/offline proof remain explicit.

Current copyable target-agent message:

> Verify the outer ZIP SHA-256 and read START-HERE.md plus agent-handover.md. Restore only the development workspace/tooling/setup into one new Windows x64 destination. Require Preflight exit 0 before Bootstrap and Verify; a prerequisite exit 2 means stop, while local_tooling_verified_host_activation_pending after setup means host actions remain. Preserve conflicts and original source provenance, read installed AGENTS/PGMCP protocols and report actual results. This does not install PostgreSQL, a MyBrain schema/storage or a running app/API/UI; continue authorized development from the retained issue 6 design inputs. Do not import private data/accounts, invent issue state, inherit old QA or overwrite/force-push origin.

Only this final evidence document changes after the frozen build input; packaged bytes remain unchanged. Review requested for the new exact revision/ZIP; Validation and later scheduled work remain pending. No phase transition or remote publication.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.3 | 2026-10-28 | @imp implementer | Correct read-only Git/network Preflight and coverage, record fresh r6 archive/affected proof and explicitly bounded reuse of independently observed r5 core evidence. |
| 1.2 | 2026-10-28 | @imp implementer | Record independent runtime NOGO, inert admission correction, bounded Git-stage regressions, preserved failed r4 journeys and successful frozen r5 actual-archive evidence. |
| 1.1 | 2026-10-28 | @imp implementer | Freeze r3 artifact/source identity and actual extracted public journey; preserve rejected r2 and recovery evidence, native checks and honest host/network limits. |
| 1.0 | 2026-10-28 | @imp implementer | Record meaningful RED and focused public contract/journal behavior evidence; disclose authoring and dependency observations. |
