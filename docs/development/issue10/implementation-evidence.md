<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Consolidation implementation evidence

**Status:** REVIEW REQUESTED — implementation evidence  
**Version:** 1.0  
**Last Updated:** 2026-10-29

## Purpose

Describe the actual mechanical import and distinguish it from historical product/package evidence.

## Summary

All 52 inventory files are present. All 28 setup/deployment source files match their pinned Git-object bytes. Four imported Markdown files differ only in the relative links listed below. No application, package, NAS or live integration was executed.

## Import and exact comparison

The [Research inventory](research.md) records each source SHA, source path and destination. Native git_restore selected only public paths from the four fixed commits. Five reports were moved to their owning issue folders. A read-only comparison used git show <source SHA>:<source path> bytes against each destination: 52 rows, zero missing destinations, 28/28 deployment files byte-identical, 48/52 total source files byte-identical. The four remaining differences are only eight relative-link replacements:

| File | Intentional changes |
| --- | --- |
| issue6/research.md | Four supporting-report links now resolve in its own folder |
| issue6/opencloud-wikibase-gap-analysis.md | Two PDF links point to the retained public PDF |
| issue6/opencloud-wikibase-trial-design.md | One PDF link points to the retained public PDF |
| issue9/opencloud-admission-extension-feasibility.md | One storage-design link resolves to the sibling issue6 folder |

README combines the issue6 conceptual/research links and issue7 deployment link, adjusted for canonical issue locations, plus the new development index and issue9 assessment. Existing working agreements are preserved. The development index explicitly preserves document-specific historical statuses; no original issue is closed or advanced.

## Focused native checks

Executed through the exact dedicated worktree connection:

| Invocation | Observed result |
| --- | --- |
| run_checks(scope=targets, checks=[markdown_links], targets=29 Markdown files: 27 imported Markdown files plus README.md and docs/development/README.md) | passed, Lychee 0.24.2, configured offline/cache=false/include-fragments |
| run_checks(scope=targets, targets=[setup/deployment/manifest.schema.json], checks=[json_schema_shape,json_schema_metaschema]) | both passed, check-jsonschema 0.38.2 |

Scaffolding this evidence document separately executes its enforced Markdown-link gate. The full branch profile and configured-scope test request belong to Validation and have not yet been executed. No YAML was imported or changed. Existing issue7 test/package reports remain historical; byte-preservation does not prove a new Windows install or clean-machine run.

## Preservation and exclusions

Issue1/2 baseline documents and the public PDF are unchanged. Shared ADR/discussion-map canonical paths are retained. Original issue .pgmcp/state.json and .pgmcp/deliverables.json were not imported; only issue10's own lifecycle is active. Original branches/worktrees remain untouched. Credentials, machine configuration, package archives, dependencies, private runtime data and source identifiers are excluded.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-29 | Codex (@imp implementer) | Record exact import comparison, intentional link differences and focused native checks. |
