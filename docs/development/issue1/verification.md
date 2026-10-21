<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Issue 1 instruction verification

**Status:** DOCUMENTATION EVIDENCE — independent QA requested  
**Version:** 1.0  
**Last Updated:** 2026-10-21

## Purpose

Record focused verification of the documentation and deployed instruction consumers before independent QA.

## Summary

Required selected Markdown and YAML checks passed. Exact generic-source and phase-override parity was observed; all three local role TOML files parsed and matched their portable fields; all eight existing skills passed the structural helper. These facts do not prove runtime multi-worktree coordination or independent acceptance.

## Native checks

- run_checks(scope="targets", targets=["README.md","AGENTS.md",".agents/skills/pgmcp-qa/SKILL.md",".agents/skills/pgmcp-co/SKILL.md",".agents/skills/pgmcp-imp/SKILL.md",".agents/skills/pgmcp-go/SKILL.md",".agents/skills/pgmcp-end-issue/SKILL.md",".agents/skills/pgmcp-start/SKILL.md",".agents/skills/pgmcp-start-issue/SKILL.md",".agents/skills/pgmcp-create-issue/SKILL.md","setup/pgmcp/agents/agents.md","setup/pgmcp/agents/collaboration.md","setup/pgmcp/agents/roles/co.md","setup/pgmcp/agents/roles/imp.md","setup/pgmcp/agents/roles/qa.md","setup/pgmcp/agents/workflows/start.md","setup/pgmcp/agents/workflows/go.md","setup/pgmcp/agents/workflows/create-issue.md","setup/pgmcp/agents/workflows/start-issue.md","setup/pgmcp/agents/workflows/end-issue.md","setup/pgmcp/README.md","docs/development/issue1/planning.md","docs/development/issue1/research-notes.md","docs/development/issue1/review-exercises.md"], checks=["markdown_links"]): passed, configured offline local-link/fragment policy using Lychee 0.24.2.
- run_checks(scope="targets", targets=["setup/pgmcp/contracts.yaml","setup/pgmcp/codex-roles.yaml"], checks=["yaml_configuration"]): passed, check-jsonschema 0.38.2 with declared prerequisites.
- Normal scaffold/edit enforce checks passed on new/changed Markdown and YAML artifacts. This evidence document is also checked on scaffold.
- No application tests, new native binding acknowledgements or automatic fixes were run for this documentation-only issue.

## Structural and deployment observations

Read-only Python inspection compared all ten setup/pgmcp/agents Markdown source files byte-for-byte with their .pgmcp/agents counterparts: all equal. setup/pgmcp/contracts.yaml exactly matched .pgmcp/config/contracts.yaml. YAML structure inspection confirmed the override changes only phase_instructions/handover_template for 39 phases in seven workflows; phase gates and native policies are inherited unchanged. restart_server followed by get_work_context showed the new coordinated-mode preamble in the active documentation phase.

The runtime TOML reader parsed all three local .codex/agents/pgmcp-*.toml files; their name/description/developer_instructions fields matched setup/pgmcp/codex-roles.yaml. safe_edit_file(validation="report") had written those TOML changes with validation_status=not_executed because no native TOML pre-write binding is configured. The subsequent parse/parity inspection is separate structural evidence, not a native check pass.

The skill-creator scripts/quick_validate.py helper was run through the workspace Python on each of pgmcp-co, pgmcp-create-issue, pgmcp-end-issue, pgmcp-go, pgmcp-imp, pgmcp-qa, pgmcp-start and pgmcp-start-issue. All eight returned 'Skill is valid!'. This validates frontmatter/naming/placeholders, not behavior or QA authority. The earlier nine-skill inventory count was corrected with no change to the intended existing target set.

## Review coverage and limitations

The [review exercises](review-exercises.md) trace assignment/review, direct owner-appointed QA, NOGO/correction, owner decision, interrupted writer, wrong-server binding, unavailable channel, stale verdict, concurrent descendant writer and next-issue routing through the written instructions. Outcomes are document walkthroughs, not live tool delivery or technical lock tests.

Current-worktree source/config deployment was verified. No extra worktree/server instances or actual product were started. Actual per-worktree MCP routing, positive/sibling-negative isolation checks, hard writer exclusion and long-running product completion remain separate runtime admission/execution work. The model is conditionally feasible and procedurally specified; a server-enforced independent verdict gate or OS read-only isolation is not implemented. Keep those distinctions in the independent review.

## Review identity and frozen snapshot

The owner requested the existing MyBrain Qa chat and had already appointed it independently for substantive phase-boundary GO/NOGO. The review request will name the final committed branch/revision and the original owner authorization. During same-worktree review, Imp will stop mutations and inspect the returned verdict. Any required correction creates a new committed revision for renewed QA. No producer GO, independent approval or phase progression is claimed here.

## Related Documents

- [Plan](<planning.md>)
- [Review exercises](<review-exercises.md>)
- [Portable source/deployment map](<../../../setup/pgmcp/README.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-21 | @imp documenter | Record exact verification selections, deployment parity and remaining operational limits. |
