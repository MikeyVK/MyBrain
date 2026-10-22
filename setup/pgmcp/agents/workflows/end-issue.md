<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# PGMCP end-issue Procedure

**Status:** Active

**Version:** 1.1

**Last Updated:** 2026-10-21

## Purpose

Define the shared end-issue procedure independently of host command or skill registration.

## Summary

Role: @co. Preserve the existing sequence, stop conditions and authority when adapting its registration to the environment.

## Protocol

Read [collaboration.md](../collaboration.md) for interactive/coordinated mode,
original owner authority, direct routing, dedicated server identity and mutation ownership.
Coordinated operation never expands host/tool permissions or producer review authority.

Complete lifecycle exit only under verified original owner authority for the named repository, PR/base, merge and closure scope. A direct human invocation or an explicit scoped delegation in the original owner mandate can authorize Co. An agent hand-over alone never does. Obtain the required independent QA verdict for the exact PR head before merge and recheck head freshness, mutation ownership and host approval requirements.

## Required Input

- `PR_NUMBER` — required. Stop and ask if missing; do not guess.
- `ISSUE_NUMBER` — optional. Supply only when recovery requires an explicit issue target.
  When absent, derive from the PR body at the point a recovery step needs it.

## Working State

Assign these named values as you execute the sequence. Use these names throughout;
do not reference steps by number when referring to previously captured data.

| Name | Set in | Value |
|---|---|---|
| `HEAD_BRANCH` | step 1 | `head_branch` from first `get_pr` |
| `BASE_BRANCH` | step 1 | `base_branch` from first `get_pr` |
| `MERGE_SHA` | step 3 | `merge_sha` from second `get_pr` |
| `PR_BODY` | step 3 | `body` from second `get_pr` |
| `PARENT_WORKFLOW` | step 7 | `workflow` from `get_work_context`, or `""` when absent |
| `PARENT_ISSUE` | step 7 | `issue_number` from `get_work_context`, or `""` when absent |

## Common Sequence

Execute in this exact order. Do not skip steps. Stop at the first blocker and report it.

1. **Load PR metadata**
   `get_pr(pr_number=PR_NUMBER)`
   → set `HEAD_BRANCH` and `BASE_BRANCH` from the result.
   → if either is null or missing, stop and report the blocker before proceeding.
   → if `state == "merged"` and `merged_at` is not null, the PR is already merged:
     skip step 2 and go directly to step 3.

2. **Merge**
   `merge_pr(pr_number=PR_NUMBER)`
   → authoritative host-side merge signal. Do not use `git_diff_stat` as a substitute.
   → if the tool returns an error, stop and report; do not proceed to step 3.

3. **Capture post-merge metadata**
   `get_pr(pr_number=PR_NUMBER)`
   → called again because `merge_sha` is only populated after a completed merge.
   → set `MERGE_SHA` and `PR_BODY` from the result.
   → if `merged_at` is null or `MERGE_SHA` is null, stop and report; the merge did not complete.

4. **Return to parent branch**
   `git_checkout(branch=BASE_BRANCH)`
   → required before reachability verification and branch cleanup.

5. **Pull parent branch**
   `git_pull()`
   → brings `MERGE_SHA` into the local parent branch history.
   → if pull fails, stop and report; do not proceed to cleanup.

6. **Verify the merge commit is reachable**
   `check_merge(merge_sha=MERGE_SHA)`
   → confirms `MERGE_SHA` is present in the current branch history after pull.
   → if the result says the SHA is not reachable, stop and report; do not delete the branch.
   → do not substitute raw terminal git commands for this check.

7. **Load parent-branch coordination context**
   `get_work_context()`
   → set `PARENT_WORKFLOW` and `PARENT_ISSUE` if the result contains them.
   → if context is empty or does not load (expected on `main` and stateless branches),
     set `PARENT_WORKFLOW = ""` and `PARENT_ISSUE = ""` and continue; this is not an error.
   → do not use this call to look up PR metadata or child-branch state.

8. **Delete the closing branch**
   `git_delete_branch(branch=HEAD_BRANCH, mode="both")`
   → deletes both local and remote tracking refs in one step.
   → if the remote ref is already absent, `mode="both"` handles it silently; no retry needed.

9. **Process PR body closeout facts**
   Use `PR_BODY` captured in step 3. No additional tool call needed.
   Identify and note: delivered scope, `Closes #N` claims, deferred items, and
   any explicit non-closure rationale.
   → Output these facts clearly in the final chat response under a dedicated "Closeout Facts" header.

10. **Epic-parent update (conditional)**
    Execute only when `PARENT_WORKFLOW` is a tracked epic workflow.
    Skip silently when `PARENT_WORKFLOW` is `""` (e.g. `main` is the parent branch).
    `update_issue(issue_number=PARENT_ISSUE, body=<updated coordination state>)`
    → Update the epic description by:
      1. Marking the child issue as completed in the checklist.
      2. Appending/updating the `## Deferred Work (from Child Issues)` section with the deferred items from step 9.
    → if `PARENT_ISSUE` is `""` but `PARENT_WORKFLOW` is non-empty, stop and report the blocker.

11. **Next-issue routing**
    Interactive mode proposes the next logical step to the owner. Coordinated mode
    records delivered/deferred work, selects the next dependency-unblocked issue
    inside the original mandate, and dispatches the applicable authorized lifecycle
    entry/assignment. A new issue still follows the scoped create-issue procedure.
    For interactive recommendations:
    - **If deferred work was identified in step 9:**
      1. Present a drafted issue body (following the standard issue template: title, problem, expected, priority, scope, parent) specifically to track the deferred work.
      2. Recommend running the `/create-issue` workflow to submit it.
    - **If no deferred work was identified:**
      1. Recommend the next existing backlog issue based on epic sequencing and dependencies.
    → Only dispatch/mutate within verified original owner authority. If the next work,
      priority change, publication or merge is outside that scope, return the concrete
      decision to the owner instead of expanding the mandate.

## Recovery: Issue Still Open After Merge

Apply this block only when all three conditions hold:
1. `PR_BODY` contains a `Closes #N` claim
2. the merge is confirmed complete (`MERGE_SHA` is set)
3. the referenced issue is still open on GitHub

If `ISSUE_NUMBER` is not available, parse it from the `Closes #N` claim in `PR_BODY`.

```
close_issue(issue_number=ISSUE_NUMBER, comment="Closed via merged PR #PR_NUMBER")
```

`close_issue` is a recovery action only. It is not part of the normative sequence above.

## Guardrails

- Do not merge without direct owner authorization or original explicitly delegated merge authority for this exact project/base scope, a matching independent QA verdict and required host/tool approval.
- `merge_pr` is the only authoritative merge signal; `git_diff_stat` is not.
- `check_merge` is the only permissible reachability gate before branch deletion; raw git commands are not.
- Do not use `get_work_context()` as a source of PR or child-branch metadata.
- Do not call `close_issue` unless all three recovery conditions above are met.

## Output

Report after completing or stopping:
- PR number, merge result, and `MERGE_SHA`
- `HEAD_BRANCH` deleted, `BASE_BRANCH` used for checkout
- reachability result from `check_merge`
- branch cleanup result from `git_delete_branch`
- epic-parent update result (when applicable)
- next-issue recommendation (when relevant)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-21 | @imp implementer | Consolidate the existing procedure without host registration metadata; retain its role, sequence, review boundaries and explicit authorization. |
| 1.1 | 2026-10-21 | @imp documenter | Reconcile coordinated authority, direct handoff and bounded continuation. |
