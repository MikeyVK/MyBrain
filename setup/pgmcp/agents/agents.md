<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# PGMCP — Agent Protocol

**Status:** Active

**Version:** 1.2

**Last Updated:** 2026-10-21

## Purpose

Provide the complete shared operational protocol for agents using PGMCP.

## Summary

One uniform instruction source for all supported host environments; deployment changes registration and format, not role authority or workflow policy.

## Deployment and Reading Route

This is the shared, host-independent PGMCP agent protocol. Start installation at
`<server-root>/docs/setup/agentic-bootstrap.md`; that checklist owns installation,
configuration and deployment of this instruction set.

All paths below use the selected server root; `.pgmcp` is the default. Workspace
artifact paths and issue identities come from the actual workspace and active
workflow context. Never import the PGMCP development repository's identity, approvals,
epic numbers, production paths or launcher settings.

Read the [coordinated collaboration policy](collaboration.md) for owner mandates,
inter-agent routing, independent QA and worktree isolation. It defines interactive
and coordinated operation without expanding host permissions.

Read the [coordination](roles/co.md), [implementation](roles/imp.md) or
[independent QA](roles/qa.md) protocol for the selected role. Invoke the procedures
under `workflows/` through the host's supported prompt, slash-command or skill
mechanism. Native host metadata and locations may differ; these role boundaries,
procedures and permissions do not. Runtime phase instructions remain owned by the
configured workflow contracts and returned by `get_work_context`.

## 🏛️ Architecture Contract (MANDATORY)

**Before writing production or test code that can affect an architectural boundary, read the applicable sections of:**
**`<server-root>/docs/coding_standards/ARCHITECTURE_PRINCIPLES.md`**

The applicable principles are a **binding contract**. Production and test code that
violates them is **REJECTED**, regardless of whether tooling gates pass. Before drafting
research, design, or planning artifacts, inspect the applicable boundaries in
`<server-root>/docs/coding_standards/DOCUMENTATION_STANDARD.md`.
Use the active phase, change blast radius, and referenced boundaries to select further
reading; do not load unrelated documents by default.

### Most common violations (quick reference):

| Violation | Correct pattern |
|---|---|
| Hardcoded phase/workflow names in Python | Read from config (WorkflowConfig / GitConfig) |
| `SomeManager()` inside `execute()` | Constructor injection via `__init__` |
| Write-capable interface for read-only consumer | Use narrow read-only interface (ISP) |
| `get_state()` calls `save()` | CQS violation — split the method |
| Module-level `Config.load()` | `ClassVar` + lazy init in `__init__` |
| if-chain on `phase == "implementation"` etc. | Registry or config-driven dispatch (OCP) |
| Value object without `frozen=True` | Add `@dataclass(frozen=True)` or `ConfigDict(frozen=True)` |
| Issue number extracted in state engine | Delegate to git conventions config class |

---

## 🔧 Tool Priority Matrix (MANDATORY)

**Never use `run_in_terminal` or default/built-in agent tools (e.g., `write_to_file`, `replace_file_content`, `multi_replace_file_content`) for these operations — use MCP tools instead:**

### Git Operations
| Action | ✅ USE THIS | ❌ NEVER USE |
|--------|-------------|------------|
| Create branch | `create_branch(issue_number, name, base_branch, branch_type)` | `run_in_terminal("git branch")` |
| Commit | `git_add_or_commit(workflow_phase, message)` | `run_in_terminal("git commit")` |
| Checkout | `git_checkout(branch)` | `run_in_terminal("git checkout")` |
| Push | `git_push(set_upstream)` | `run_in_terminal("git push")` |
| Merge | `git_merge(branch)` | `run_in_terminal("git merge")` |
| Delete branch | `git_delete_branch(branch, force, mode)` | `run_in_terminal("git branch -d")` |
| Stash | `git_stash(action, message)` | `run_in_terminal("git stash")` |
| Status | `git_status()` | `run_in_terminal("git status")` |
| Restore | `git_restore(files, source)` | `run_in_terminal("git restore")` |
| Fetch | `git_fetch(remote, prune)` | `run_in_terminal("git fetch")` |
| Pull | `git_pull(remote, rebase)` | `run_in_terminal("git pull")` |
| List branches | `git_list_branches(verbose, remote)` | `run_in_terminal("git branch -a")` |
| Diff stats | `git_diff_stat(target_branch, source_branch)` | `run_in_terminal("git diff --stat")` |
| Verify merge reachability | `check_merge(merge_sha)` | `run_in_terminal("git merge-base --is-ancestor")` |

### GitHub Operations
| Action | ✅ USE THIS | ❌ NEVER USE |
|--------|-------------|------------|
| Create issue | `create_issue(title, body, labels, milestone, assignees)` | `run_in_terminal("gh issue create")` |
| Get issue | `get_issue(issue_number)` | `run_in_terminal("gh issue view")` |
| List issues | `list_issues(state, labels)` | `run_in_terminal("gh issue list")` |
| Update issue | `update_issue(issue_number, ...)` | `run_in_terminal("gh issue edit")` |
| Close issue | `close_issue(issue_number, comment)` | `run_in_terminal("gh issue close")` |
| Create PR (atomic) | `submit_pr(title, body, draft)` | `run_in_terminal("gh pr create")` |
| List PRs | `list_prs(state, base, head)` | `run_in_terminal("gh pr list")` |
| Merge PR | `merge_pr(pr_number, commit_message, merge_method)` | `run_in_terminal("gh pr merge")` |
| Get PR | `get_pr(pr_number)` | `run_in_terminal("gh pr view")` |
| Create label | `create_label(name, color, description)` | Manual GitHub UI |
| Add labels | `add_labels(issue_number, labels)` | `run_in_terminal("gh issue edit")` |
| Create milestone | `create_milestone(title, description, due_on)` | Manual GitHub UI |

### File Operations
| Action | ✅ USE THIS | ❌ NEVER USE |
|--------|-------------|------------|
| Edit file | `safe_edit_file(path, operation, validation)` | `run_in_terminal("Set-Content")` |
| Scaffold code/docs | `scaffold_artifact(artifact_type, file_name, context)` | Manual creation |
| Inspect artifact context schema | `scaffold_schema(artifact_type)` | Guessing context fields or trial-and-error calls |

### Quality & Testing
| Action | ✅ USE THIS | ❌ NEVER USE |
|--------|-------------|------------|
| Run checks | `run_checks(scope, targets, profile, checks, args, timeout_seconds)` | `run_in_terminal("pylint")` or `run_in_terminal("mypy")` |
| Run tests | `run_tests(scope, targets, tests, args, timeout_seconds)` | `run_in_terminal("pytest")` |
| Apply fixes | `apply_fixes(scope, targets, fixes, args, timeout_seconds)` | Manual mass edits |

### Project & Phase Management
| Action | ✅ USE THIS | ❌ NEVER USE |
|--------|-------------|------------|
| Initialize project | `initialize_project(issue_number, issue_title, workflow_name, parent_branch)` | Manual .pgmcp/ file creation |
| Get project plan | `get_project_plan(issue_number)` | Manual .pgmcp/ file reading |
| Transition phase | `transition_phase(branch, to_phase)` | Manual .pgmcp/state.json edit |
| Force phase transition | `force_phase_transition(branch, to_phase, skip_reason, human_approval_message)` | Manual .pgmcp/state.json edit |

### Discovery & Admin
| Action | ✅ USE THIS | ❌ NEVER USE |
|--------|-------------|------------|
| Search code and docs | Host-native repository search | N/A |
| Get work context | `get_work_context()` | Manual file reading |
| Health check | `health_check()` | N/A |
| Restart server | `restart_server(reason)` | Process kill |

---

## 🚫 run\_in\_terminal Restrictions (CRITICAL)

**`run_in_terminal` is ONLY allowed for:**

✅ **Permitted (rare cases):**
- Development servers where no MCP tool exists (e.g., `npm run dev`, `python -m http.server`)
- Build commands explicitly requested by user
- Smoke tests / exploratory commands approved by user
- Python package installations via pip (when not using install_python_packages tool)

❌ **FORBIDDEN (use MCP tool instead):**
- **File operations** → use `safe_edit_file` / `scaffold_artifact`
- **Git operations** → use `git_*` tools (see matrix above)
- **Test execution** → use `run_tests` tool
- **Quality checks** → use `run_checks` / `apply_fixes` tool

**Default rule: If unsure, ask yourself "Is there an MCP tool for this?" If yes → use it. If no → ask user permission first.**

---

## 🧪 Workflow-Driven Test Strategy

The active workflow contract and approved plan determine whether strict
RED → GREEN → REFACTOR applies. Use strict TDD for behavior changes when the contract
requires it; do not force artificial TDD cycles onto mechanical, documentation-only, or
test-maintenance work.

Treat test code as first-class code under the same architecture, typing, and quality
standards. Design durable regression coverage, prefer adapting valuable existing tests,
and avoid workflow-only tests that become maintenance ballast.

During implementation, run the narrowest tests and gates that prove the changed surface.
Run branch- or workspace-wide verification only at the workflow phase that owns it.
Reuse fresh evidence until later changes invalidate it. Follow the active plan for commit
boundaries and required verification.

Before committing or presenting evidence, perform a pre-commit reality check: verify whether
tests and evidence genuinely prove the deliverable against its design and planning contract,
or merely create shallow or tautological asserts to satisfy tooling.

---

## ⚖️ Prime Directives

1. **Issue-First Development:** Perform issue work on its initialized issue branch, never directly on the workspace's protected base branch. Coordination creates or selects the real issue, creates/checks out its branch and calls `initialize_project` with the explicit parent.
2. **Workflow Enforcement:** Always `initialize_project` before work. Use `transition_phase` for progression.
3. **Workflow-Driven Testing:** Follow the active workflow and plan; add or adapt tests only when they provide durable evidence.
4. **Tools > Manual:** Never manually create a file if `scaffold_artifact` exists. Never manually parse status if `get_work_context` exists.
5. **Artifacts and Conversation:** Write Code/Docs/Commits in **English**. Use the user's chosen conversation language; do not impose the PGMCP development workspace's personal language preference.
6. **Owner Authority:** Verify the original owner mandate for each decision/action class. Coordinated continuation and independent QA follow [collaboration.md](collaboration.md). Push, merge, closure and publication need explicit scoped authority and remain subject to host/tool approval. `force_phase_transition` requires approval + reason.
7. **Quality Gates:** Use the scope and timing required by the active phase and plan. Reuse fresh passing evidence unless subsequent changes invalidate it.
8. **Type-Checking Consistency:** Resolve typing issues using `<server-root>/docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md`. No global disables; targeted ignores only as last resort.
9. **Cache Reads and Hashes:**
   - Use tool summaries for routine success and status.
   - Read cached DTOs only for needed diagnostics or structured fields; never reconstruct DTOs from summaries.
   - Reuse already-read results until invalidated.
   - Check result size before paging; stop blind multi-megabyte downloads.
   - Verify SHA-256 once for multipart assembly or an explicit identity requirement; do not hash routine actions.
10. **Execution Budgets:**
   - Use the active phase's required scope; keep normal calls focused.
   - For required full-suite runs, raise timeout_seconds to fit the workload; do not split solely to fit a short timeout.
   - Keep the client window large enough for the whole call, stopping and response delivery; follow <server-root>/docs/setup/README.md.
   - Preserve native arguments and required coverage; report timed-out or incomplete runs as incomplete.

---

## 🧭 Strategy Approval Gate (MANDATORY)

Compatibility, migration, and breakage strategy is decided at the end of Research, not later.

- Research must identify the affected boundaries, consumers, strategy options, and the cost / risk / impact trade-offs for each relevant boundary.
- Research must not close until an Approved Strategy is recorded. In interactive mode obtain the human decision. In coordinated mode Co may decide only when the verified original owner mandate explicitly delegates that strategy class; record the delegation/rationale and obtain independent QA at the phase boundary.
- The Approved Strategy must be explicit per affected boundary, not left as a vague issue-wide assumption.
- Design may not start until an Approved Strategy exists for the boundaries it will shape.
- Planning, implementation, and QA must treat the Approved Strategy as binding input.
- No later phase may silently switch between preserve compatibility, temporary bridge, or clean break.
- If later evidence makes the Approved Strategy unsound, stop the affected boundary and reopen the decision through Co. Decide within verified delegated authority or escalate to the owner; never change strategy by stealth.

---

## 📋 Workflow Types

| Workflow | Phases | Use Case |
|----------|--------|----------|
| `feature` | research, design, planning, implementation, validation, documentation, ready | New feature development |
| `bug` | research, design, planning, implementation, validation, documentation, ready | Bug fixes |
| `docs` | planning, documentation, ready | Documentation-only changes |
| `refactor` | research, design, planning, implementation, validation, documentation, ready | Code refactoring |
| `hotfix` | implementation, validation, documentation, ready | Emergency fixes |
| `chore` | research, implementation, validation, documentation, ready | Lightweight maintenance and housekeeping |
| `epic` | Read the active configured workflow contract through `get_work_context` (SSOT for phase order) | Large multi-issue features |

**Workflow Selection:** Use `initialize_project(issue_number, issue_title, workflow_name="feature|bug|refactor|docs|hotfix|chore|epic", parent_branch="<explicit base branch>")` to start.

---

## 🏗️ Scaffolding (Always Use Templates)

**NEVER use `safe_edit_file` to create code or documentation from scratch. Always use `scaffold_artifact`.**

The live `scaffold_artifact` and `scaffold_schema` input schemas enumerate admitted `artifact_type` values. Select a registered ID there; do not infer an alias from an old example or a filesystem path. Pass `file_name` as the exact output basename, including its extension, and provide `context` matching the selected schema.

Use the selected workspace's configured template-suite root; the default is `<server-root>/template_suite/`. It supplies template packages, while the live tool schema defines which IDs an agent may invoke.

**Schema discovery:** Before calling `scaffold_artifact` with an artifact type whose context fields are not already in your working context, call `scaffold_schema(artifact_type=...)` first. It returns the full JSON Schema for the `context` parameter — required and optional fields — enabling first-time-right scaffolding without a failed call. If you call `scaffold_artifact` with wrong or missing context fields, the error response contains the same schema; use it to correct the call immediately.

---

## 🤝 Three-Agent Model

PGMCP uses three specialized roles in independent sessions supported by the selected environment to prevent role contamination and context pollution.

### Roles

| Agent | Role | Allowed operations |
|-------|------|--------------------|
| `@co` | Coordination authority and epic workflow owner | Read all; issue/label/milestone admin; epic docs/contracts/prompts edits; epic lifecycle mutations, phase transitions, commits, quality gates, PR submission, and merge within the approved narrow allowlist |
| `@imp` | Child-issue implementation executor | Production code and test work on non-epic branches; cycle execution; commits; phase and cycle transitions |
| `@qa` | QA authority — read-only | Read files; run tests; run quality gates. **No edits, no commits** |

### Sub-roles

**`@co` sub-roles:** coordination: `triager` (default), `backlog-reviewer`, `tracker`, `issue-author`; epic lifecycle: `epic-researcher`, `epic-planner`, `epic-designer`, `epic-coordinator`, `epic-documenter`, `epic-releaser`

**`@imp` sub-roles:** `researcher` (default), `planner`, `designer`, `implementer`, `validator`, `documenter`

**`@qa` sub-roles:** `design-reviewer` (default), `plan-verifier`, `verifier`, `validation-reviewer`, `doc-reviewer`

Declare your active sub-role in the invocation text.

Example: `@imp implementer: start cycle C_LOADER.5 for issue 257`

### @co Operating Modes

- **Owned-branch epic execution:** `@co` owns the epic branch end-to-end and may edit epic docs/contracts/prompts, perform lifecycle mutations, phase transitions, commits, quality gates, PR submission, and merge after approval.
- **Background coordination:** `@co` reads status, updates issue coordination state, and hands child technical work to `@imp` without taking over the implementation branch.

### Role Sessions

- **Coordination / epic ownership** → use `@co`. Use `@co` either for owned-branch epic execution or for background coordination around child work. Produce a Co → Imp hand-over only when delegating child technical implementation.
- **Implementation** → use `@imp` for child technical work. Execute the current cycle. Produce an Imp → QA hand-over.
- **Review** → use `@qa`. Findings on epic-owned branches route back to `@co`; findings on child technical work route back to `@imp`.

Never mix roles in one context. Co directly routes stable role contexts under verified owner authority and delegates installation to Imp. Use one dedicated PGMCP server per worktree and at most one active mutating Imp in that worktree; admitted worktrees may run in parallel.

### Delegation and Review Authority

Use harness-supported delegation for bounded tasks when explicitly requested or authorized by applicable instructions. The producer remains accountable for scope, evidence and integration. Every mutating implementation worker, including descendants, counts against the one-active-mutating-Imp limit per worktree.

The [collaboration policy](collaboration.md) defines authority: owner-appointed QA or a separate QA appointed by Co under explicit owner delegation may issue independent GO/NOGO. Delivery by Imp does not revoke an existing owner appointment. Imp-delegated preflight remains findings-only. Co routes results and schedules authorized progression only after a matching valid verdict.

### Startup Protocol

Each agent has its own startup protocol defined in its `.agent.md` file. Normal chat sessions call
`get_work_context` as the first tool invocation. `start-issue` and `end-issue` are explicit
lifecycle-boundary exceptions that may run their scripted bootstrap or exit sequence before
control returns to a normal `get_work_context`-first session. See:
- [`@co` startup](roles/co.md)
- [`@imp` startup](roles/imp.md)
- [`@qa` startup](roles/qa.md)

### Hand-Over Contract

Use phase/review hand-overs as navigation and evidence indexes, never as binding truth or producer
approval. Include the mandate/assignment, issue, worktree/server alias, branch/revision,
phase/cycle, sources, evidence, mutation owner, reply destination and open work required
by [collaboration.md](collaboration.md). Keep phase- and workflow-specific content under this common structure:

```text
### <Workflow> / <Phase> Hand-over

#### Scope
- completed and intentionally excluded work

#### Deliverables
- authoritative artifacts and material inputs, with clickable repository-relative links

#### Evidence
- exact relevant checks and outcomes

#### Open Work
- blockers, questions, risks, and deferred work, or None

#### Review Request
- Review requested
```

Pre-implementation hand-overs link primary artifacts and material inputs. Implementation
hand-overs link changed files while useful; for large diffs, link primary review entry
points and tests and identify the branch diff as the complete inventory. Never claim
PASS, GO, approval, or readiness as fact. Co → Imp remains limited to child technical
delegation; epic review and lifecycle continuation remain with `@co`.

---

## 📚 Key Documentation

- **`<server-root>/docs/reference/tools/README.md`** — All MCP tools with parameters and examples
- **`<server-root>/docs/reference/copilot-agent-instructions-model.md`** — How instruction files cooperate with phase-gate-mcp
- **`<server-root>/docs/coding_standards/QUALITY_GATES.md`** — Validation standards
- **`<server-root>/docs/coding_standards/ARCHITECTURE_PRINCIPLES.md`** — Binding architecture contract
- **`<server-root>/docs/coding_standards/TYPE_CHECKING_PLAYBOOK.md`** — Typing issue resolution order

---

**Remember: These rules are enforced. Violations will be rejected by the user. When in doubt, consult the Tool Priority Matrix or ask the user.**

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-21 | @imp implementer | Consolidate existing PGMCP instruction content into one shared source; remove host metadata and fixed workspace assumptions. |
| 1.1 | 2026-10-21 | @imp implementer | Use the canonical start-issue procedure name for the lifecycle startup exception. |
| 1.2 | 2026-10-21 | @imp documenter | Add mandate-bound coordinated authority and isolated worktree execution. |
