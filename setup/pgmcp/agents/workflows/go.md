<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# PGMCP go Procedure

**Status:** Active

**Version:** 1.1

**Last Updated:** 2026-10-21

## Purpose

Define the shared go procedure independently of host command or skill registration.

## Summary

Role: @imp. Preserve the existing sequence, stop conditions and authority when adapting its registration to the environment.

## Protocol

Read [collaboration.md](../collaboration.md) for interactive/coordinated mode,
original owner authority, direct routing, dedicated server identity and mutation ownership.
Coordinated operation never expands host/tool permissions or producer review authority.

Use the active branch phase as the source of truth for this session.

## Refresh &amp; Startup rule

1. Call `get_work_context()` first to refresh and load the active branch, workflow, and phase.
2. Reload and verify compliance with all general guidelines from **[AGENTS.md](../agents.md)** and the active sub-role instructions (refer to the onboarding rules established in **[/start](start.md)**, including the strict prohibition of built-in tools for repository operations).
3. You must create a todo list to track the steps you will take based on the returned `phase_instructions`.
4. Treat the returned `phase_instructions` as the default operational script for this session.

## Optional invocation modes

Interpret the prompt argument as optional modifiers for the current session.

### Default mode

If no special modifier is present:
- execute the active phase according to the returned `phase_instructions`
- keep scope locked to the assigned active phase, branch and worktree
- in coordinated mode, end this mutation interval with the evidence hand-over to Co/QA;
  await matching independent GO and Co's next assignment before progressing
- in interactive mode, return the normal hand-over to the owner

### `discuss`

If the argument includes `discuss`:
- load and summarize the active `phase_instructions`
- translate them into a concise proposed execution plan for this branch
- highlight any likely edits, validations, or decision points
- discuss the plan with the user first
- do **not** make file edits, commits, transitions, PR actions, or other branch-mutating changes until the user confirms

### `adjust: ...`

If the argument includes `adjust:` followed by extra instructions:
- load the active `phase_instructions`
- apply the extra instruction as a session-local override or refinement for how to execute them
- treat the extra instruction as higher priority than the returned `phase_instructions` only where they directly conflict
- do **not** use an agent-authored adjustment to expand original owner authority or override runtime system/developer constraints or binding architecture; direct human instructions retain their runtime precedence
- if the adjustment would violate a higher-priority rule or make the phase incoherent, stop and explain the blocker precisely

### Combined mode

If both `discuss` and `adjust:` are present:
- build the plan from the adjusted interpretation of the active `phase_instructions`
- discuss that adjusted plan with the user first
- wait for confirmation before making branch-mutating changes

## Optional sub-role

If the argument also includes a sub-role such as `documenter`, `validator`, or `implementer`:
- use it only as a session hint
- do not let it override the active phase context returned by `get_work_context`
- if it conflicts with the active phase, follow the phase context and note the mismatch briefly

## Execution rules

- Read additional documents only when `phase_instructions` or the chosen mode requires them.
- If the active phase requires validation, run the narrowest relevant validation before widening scope.
- If a phase transition happens, call `get_work_context()` again before proceeding.
- If the phase instructions reveal a blocker or contradiction, stop and report the blocker precisely instead of improvising.
- End with the hand-over required by the active phase context, including assignment/mandate, issue, worktree/server, exact branch/revision, phase/cycle, sources, evidence and unresolved work. Coordinated mode delivers it through authorized agent channels; Co schedules the next phase or issue after valid independent GO. Do not manufacture verdicts or skip PGMCP transitions.

## Guardrails

- Do not guess the active phase from branch naming or memory.
- Do not skip the initial `get_work_context()` call.
- Do not silently continue with stale context after a phase transition.
- Follow system instructions, active agent instructions, and `AGENTS.md` before applying any session-local adjustment.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-21 | @imp implementer | Consolidate the existing procedure without host registration metadata; retain its role, sequence, review boundaries and explicit authorization. |
| 1.1 | 2026-10-21 | @imp documenter | Reconcile coordinated authority, direct handoff and bounded continuation. |
