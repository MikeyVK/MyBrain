<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Portable Windows workspace deployment

**Status:** MAINTAINED — deployment implementation
**Version:** 1.2
**Last Updated:** 2026-10-28

## Purpose

Build and verify the screened workspace/tooling package for issue 7.

## Summary

Use the [target handover](START-HERE.md) for installation. The implementation preserves the [approved contracts](../../docs/development/issue7/design.md) and [cycle plan](../../docs/development/issue7/planning.md). Generated data/artifacts stay in ignored build or target-local directories.

## Delivered scope

The package supplies development workspace/Git and fixed source snapshots, CPython 3.15 x64, PGMCP 4.0.0, native quality tooling and target-local role/binding configuration. The frozen active-storage source is issue 6 research/design/storage-model/operations/preservation/acceptance documentation for future PostgreSQL 18 implementation, with no app/src, API/UI or migrations. Its sole selected local helper, setup/local/find-postgresql-download.py, finds vendor URLs; it does not download/install/provision PostgreSQL. No PostgreSQL server, MyBrain schema/empty product storage or running application/API/UI is installed or proven. Continue authorized product development from the retained issue 6 design inputs; database/product setup needs separate implementation and verification. No private operational data is included.

## Build and verify

Build-Package.ps1 -Destination <new-staging-path> -Sources <local-spec.json> creates the distribution directory, adjacent ZIP and external SHA-256 file. Use the verified build environment (-Python when not running from a provisioned source workspace). The local spec supplies primary_root, artifact_root, fixed named source entries (id/root/ref/role), individually screened local_sources and explicit excluded_candidates; actual host roots/spec stay local-only. Source refs resolve to full SHAs. Stable safe working differences are preserved separately with exact bytes, base and operations; changes after the frozen ref are disclosed rather than silently merged.

Test-Package.ps1 -Archive <actual.zip> -Destination <new-disposable-path-with-spaces> inspects/extracts the actual archive, verifies inventory, bootstraps and runs the public rerun/conflict/interruption/recovery journey. Its external .verification.json names that exact outer digest. Never embed final own-archive evidence back into the same ZIP. Changed bytes require fresh hashes, extraction and affected independent QA.

Preflight checks usable Git through version and required builtin-command availability in an isolated read-only child. Existing owned target Git is hash/inventory-checked before probing; a hash-verified cached fallback avoids network. Otherwise an 8-second, at-most-three-redirect HEAD probe checks only the exact declared primary URL, without body download or credentials. Unproved prerequisites return pending exit 2, and changed cached/owned bytes remain conflicts. The internal transport seam lets public Preflight tests exercise deterministic reachable/unavailable/unproved outcomes; those fixtures are distinct from live HEAD evidence.

## Focused technical evidence

Invoke tests/Invoke-DeploymentTests.ps1 -Suite Contracts, Provisioning or Archive with the verified Python environment. The suites test public command behavior and source/journal/archive APIs using synthetic data; they are separate from deferred application bindings. Compile Python without retained bytecode and parse PowerShell with the native parser. Required configured Markdown/YAML/JSON Schema gates remain applicable; no inactive application-test pass is inferred.

Run `tests/Test-RuntimeAdmission.ps1 -RuntimeArchive <verified-CPython-zip> -Destination <new-disposable-space-path>` for the native startup boundary regression. It checks exact runtime files/directories and original hashes, using only inert additional text and an empty directory. Bootstrap/Verify/Recover must refuse extras before interpreter invocation and preserve conflicts. The ordinary generated-launch/native checks use inert inherited-context fixtures; no startup-module or marker-code execution probe is used.

The Provisioning suite also exercises managed Git-stage promotion with real Windows readers without delete sharing. The implementation retries only Windows access/sharing conflicts, at most 20 attempts with 19 waits of 50 ms, and rechecks exact stage inventory/hashes, owner continuity and absent destination each time. Permanent locks or changed/foreign content stop without overwriting or deleting bytes. Actual interruption tests still reject every nonzero taskkill result and expose its step/returncode/stdout/stderr.

## Containment and privacy

The manifest inventories every admitted file except itself and its detached digest; external ZIP digest is delivered separately. Hashes detect byte changes but do not authenticate the sender. Native preflight and the Python verifier reject unsafe/duplicate/archive-link/reparse paths and conflicting destinations. Managed pip/Git/Python variables and temporary/cache output are scoped to the owned destination. The generated isolated proxy guard also sanitizes the actual child launch; native tests deliberately poison inherited context. Original private runtime, personal/provider manifests, credentials/caches, private PDFs and raw Git history are excluded. Selected safe original setup/source bytes remain exact alongside generated consumers.

## Later development

This package creates local standalone main with a scoped synthetic import author, no origin and no active issue. Preserve original provenance; historical workflow/QA is not valid approval for new snapshot commits. Later authenticated remote work needs a separate verified authoritative base, Co-created issue branch and reviewed source-only deltas/conflict checks. No force-push, silent unrelated-history merge, remote overwrite or private export is part of setup.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.2 | 2026-10-28 | @imp implementer | Clarify delivered development/tooling coverage, remaining PostgreSQL/product work and read-only Git/network prerequisite outcomes. |
| 1.1 | 2026-10-28 | @imp implementer | Document safe exact-runtime admission regression and bounded Windows Git-stage promotion; retain strict interruption diagnostics. |
| 1.0 | 2026-10-28 | @imp implementer | Document the bounded source/artifact build, actual archive verification and target-local privacy/recovery/authority contracts. |
