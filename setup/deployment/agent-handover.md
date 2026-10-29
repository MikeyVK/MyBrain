<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Short target-agent task

**Status:** TARGET HANDOVER
**Version:** 1.1
**Last Updated:** 2026-10-28

## Purpose

Copy the task below to the target PC's local agent.

## Summary

Verify the ZIP against the outer SHA-256 supplied with it, then read START-HERE.md. Install only this screened workspace/tooling/setup package into one new Windows x64 destination: run Preflight.ps1, Bootstrap.ps1 and Verify.ps1 with that same -Destination. Preserve existing work and stop on conflicts, integrity/privacy failures or unavailable prerequisites. Read the installed AGENTS.md and effective PGMCP bootstrap/protocols. Report actual local/native results and remaining Codex login, project trust and named-connection activation. Require Preflight exit 0; its exit 2 means an unresolved prerequisite. For Bootstrap/Verify, exit 2 is expected only with local_tooling_verified_host_activation_pending. Do not import private data/accounts, invent an active issue, inherit old QA or overwrite/force-push origin. Keep original source provenance distinct from the new standalone Git identity.

## Coverage to report

This restores a standalone development workspace/Git, CPython 3.15, PGMCP 4, quality tools and role/binding configuration. The active-storage snapshot contains PostgreSQL 18 design/operations/acceptance documents for future implementation; it has no app/src, API/UI or migrations. Its only selected local helper finds vendor URLs and does not download/install/provision PostgreSQL. Bootstrap does not create a PostgreSQL server, MyBrain schema/empty product storage or running app. Continue from the retained issue 6 design documents under fresh issue authority; report remaining product implementation/setup separately.

Preflight exit 2 for unproved Git/network prerequisites means stop before Bootstrap. Its HEAD probe does not download an artifact or create the destination. Do not report development tooling as a complete MyBrain application.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.1 | 2026-10-28 | @imp implementer | Clarify delivered development/tooling coverage, remaining PostgreSQL/product work and read-only Git/network prerequisite outcomes. |
| 1.0 | 2026-10-28 | @imp implementer | Provide a short standalone task for the target local agent. |
