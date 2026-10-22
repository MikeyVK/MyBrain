<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# PGMCP start Procedure

**Status:** Active

**Version:** 1.1

**Last Updated:** 2026-10-21

## Purpose

Define the shared start procedure independently of host command or skill registration.

## Summary

Role: explicitly selected @co, @imp or @qa. Preserve the existing sequence, stop conditions and authority when adapting its registration to the environment.

## Protocol

Read [collaboration.md](../collaboration.md) for interactive/coordinated mode,
original owner authority, direct routing, dedicated server identity and mutation ownership.
Coordinated operation never expands host/tool permissions or producer review authority.

This command forces the agent to initialize its session, synchronize its internal instruction set, and verify compliance with the active workspace rules.

## Step-by-Step Sequence

1. **Check Active Context**:
   Call `get_work_context()` to retrieve the current active branch, workflow, phase, issue number, and sub-role hint.

2. **Read Project Rules**:
   Read **[AGENTS.md](../agents.md)** to load and align with all general workspace-level guidelines and tool restrictions.

3. **Read Sub-Role Instructions**:
   Read the specific sub-role rule file corresponding to the argument passed (e.g. `/start co`, `/start imp`, `/start qa`) or the file mentioned in the command:
   - If argument is `co`: read **[co.agent.md](../roles/co.md)**.
   - If argument is `imp`: read **[imp.agent.md](../roles/imp.md)**.
   - If argument is `qa`: read **[qa.agent.md](../roles/qa.md)**.
   - Alternatively, if a file is explicitly mentioned or @-mentioned, read that file.

4. **Verify Tool Priority and Built-In Tool Restrictions**:
   Re-read and verify the **Tool Priority Matrix** and **run_in_terminal Restrictions** from **[AGENTS.md](../agents.md)**. Confirm that:
   - Git, GitHub, File, Quality, and Test operations MUST use MCP tools.
   - Built-in agent tools (e.g., `write_to_file`, `replace_file_content`, `multi_replace_file_content`) are strictly forbidden for repository operations when a corresponding MCP tool exists.
   - Running terminal commands via `run_in_terminal`/`run_command` is strictly restricted.

5. **Verify Assignment**:
   Compare the original owner mandate/appointment, role, issue/branch, phase/cycle,
   assigned worktree and dedicated server instance. Imp must hold the single mutation
   assignment before writes. QA confirms exact revision and stable producer state.
   Keep actual host/chat bindings local-only. Stop affected work on mismatch.

6. **Acknowledge and Report**:
   Output a formal startup confirmation block to the user detailing the synchronized state:
   ```markdown
   ### 🚀 Agent Startup Confirmation
   * **Branch**: `<active_branch>`
   * **Active Role / Sub-role**: `<active_role_from_context>`
   * **Workflow Phase**: `<active_phase>`
   * **Understanding of Rules**: Confirmed reading of `AGENTS.md` and the active sub-role instructions.
   * **Tool Priority Compliance**: Verified that Git, GitHub, File, Quality, and Test operations MUST use MCP tools, built-in agent tools (like `write_to_file`) are prohibited for repository actions, and terminal executions are strictly restricted.
   ```

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-21 | @imp implementer | Consolidate the existing procedure without host registration metadata; retain its role, sequence, review boundaries and explicit authorization. |
| 1.1 | 2026-10-21 | @imp documenter | Reconcile coordinated authority, direct handoff and bounded continuation. |
