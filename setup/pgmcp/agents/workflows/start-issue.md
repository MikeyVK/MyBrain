<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# PGMCP start-issue Procedure

**Status:** Active

**Version:** 1.1

**Last Updated:** 2026-10-21

## Purpose

Define the shared start-issue procedure independently of host command or skill registration.

## Summary

Role: @co. Preserve the existing sequence, stop conditions and authority when adapting its registration to the environment.

## Protocol

Read [collaboration.md](../collaboration.md) for interactive/coordinated mode,
original owner authority, direct routing, dedicated server identity and mutation ownership.
Coordinated operation never expands host/tool permissions or producer review authority.

Bootstrap explicit lifecycle entry. This prompt models branch entry, not background coordination around work already in progress. Co first assigns Imp to provision a newly admitted worktree's dedicated server/environment when needed; no product work or fabricated issue state is allowed during bootstrap. Confirm provisioning is quiescent, acquire the lifecycle mutation interval, and use that worktree's verified connection for every step.

## Required Input

Extract from the invocation argument:
- `ISSUE_NUMBER` — the GitHub issue number
- `WORKFLOW_TYPE` — an identity admitted by this workspace's live branch/workflow schemas and configured contract; do not copy another workspace's vocabulary.

If `WORKFLOW_TYPE` is missing, call `get_issue(ISSUE_NUMBER)` and derive it from authoritative issue context.
If `ISSUE_NUMBER` is missing, stop and ask for it. Do not guess from branch names or free-form text.

## Common Sequence

Execute in this exact order. Do not skip steps.

1. **Read the issue**
   `get_issue(ISSUE_NUMBER)` → obtain the complete operation from structured data or the returned resource URI; record its `title`, `labels` and stated scope. Do not reconstruct it from the inline summary.

2. **Determine base branch**
   If the issue body or labels contain a `parent_issue` number:
     a. Call `git_list_branches(remote=True, verbose=False)`
     b. Filter results for a branch matching `*/{parent_issue_number}-*`
        (e.g. parent_issue=320 → match `epic/320-production-readiness-tracker`)
     c. If exactly one branch matches, use it as `base_branch`
     d. If zero or multiple branches match, stop and report the ambiguity to the user
   If no parent_issue, use the explicitly selected, owner-approved base branch
   admitted by this workspace. Consult its branch policy; if the parent is missing
   or ambiguous, ask before creating the branch. Do not assume a branch called main.

3. **Create the branch**
   `create_branch(issue_number=ISSUE_NUMBER, branch_type=WORKFLOW_TYPE, name="<short-slug-from-title>", base_branch=<derived above>)`
   → record the actual branch identity returned by the tool; the configured conventions own its format.
4. **Switch to the branch**
   `git_checkout(branch=<actual branch identity returned by create_branch>)`

5. **Initialize the project**
   `initialize_project(issue_number=ISSUE_NUMBER, issue_title="{title}", workflow_name=WORKFLOW_TYPE, parent_branch=<base_branch derived in step 2>)`

## Epic-Owned Path

Use this path only when `WORKFLOW_TYPE` is `epic`.

6. **Load startup context**
   `get_work_context()`
   → record branch, workflow, and first phase.
   → if startup context does not load cleanly, stop before the first commit or push and report the blocker.

7. **Verify project plan and workflow contract**
   `get_project_plan(issue_number=ISSUE_NUMBER)`
   → if the workflow or phase contract is missing or inconsistent, stop before the first commit or push and report the blocker.

8. **First commit**
   `git_add_or_commit(workflow_phase="<first phase from get_work_context>", message="Start issue: {title}")`
   → use the initialized workflow phase returned by `get_work_context`; do not guess or hardcode the phase name.

9. **Push**
   `git_push(set_upstream=true)`

## Non-Epic Path

Use this path for `feature`, `bug`, `refactor`, `docs`, `hotfix`, and `chore` workflows.

6. **Verify project plan and hand-off boundary**
   `get_project_plan(issue_number=ISSUE_NUMBER)`
   → if the initialized plan is missing or inconsistent, stop and report the blocker.

7. **Hand off to @imp at the initialized-branch boundary**
   `@co` owns lifecycle entry through steps 1–6 (branch creation, checkout, project initialization, and plan verification), then ends that lifecycle mutation interval.
   The branch is fully initialized by the time `@co` stops: `create_branch`, `git_checkout`, and `initialize_project` have all completed.
   `@imp` starts on an already-initialized branch and can call `get_work_context()` unconditionally as its first action.
   Do not make the first commit or push on the non-epic path from Co.
   In coordinated mode Co sends the complete assignment directly to the authorized
   Imp context and transfers the single mutation slot after lifecycle tools finish;
   in interactive mode return the hand-over to the owner. Imp verifies original
   mandate, dedicated instance, actual branch/issue and phase before acting.

## Guardrails

- If `@co` is merely coordinating around ongoing `@imp` work, use a normal `@co` session instead of this prompt.
- Do not skip the `get_work_context` or `get_project_plan` stop-go checks where this prompt requires them.
- Do not silently widen the non-epic flow into full owned-branch execution.

## Output

After completing or stopping the flow, report:
- branch name
- workflow
- first phase when available
- whether the flow stopped at the `@co` hand-off or completed full owned-branch bootstrap
- push result when applicable
- blockers

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-21 | @imp implementer | Consolidate the existing procedure without host registration metadata; retain its role, sequence, review boundaries and explicit authorization. |
| 1.1 | 2026-10-21 | @imp documenter | Reconcile coordinated authority, direct handoff and bounded continuation. |
