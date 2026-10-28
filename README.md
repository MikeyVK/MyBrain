# MyBrain

MyBrain is a research-stage project for a sovereign AI second brain: an environment
that connects original sources, knowledge, current obligations and authorized
execution across personal and business contexts.

Case management is the first application candidate. Scope, migration strategy,
application stack, hosting and model processing remain research questions.

## Start here

| Read | Purpose |
| --- | --- |
| [Foundational principles](docs/architecture/decisions/0001-digital-brain-foundational-principles.md) | Owner-accepted conceptual principles and open design details. |
| [Discussion map](docs/architecture/digital-brain-discussion-map.md) | Functions and shared aspects for conceptual brainstorming, with discussion coverage. |
| [Public research baseline](docs/research/public/research-baseline.pdf) | Privacy-screened concepts, open questions and synthetic evaluation cases. |
| [Open-source platform candidates](docs/research/public/open-source-platform-candidates.md) | Evidence-based platform comparison and proposed synthetic validation. |
| [Open-source knowledge-core candidates](docs/research/public/open-source-knowledge-core-candidates.md) | Application-focused comparison of claim registration, context, history and reusable knowledge components. |
| [OpenCloud–Wikibase gap assessment](docs/research/public/opencloud-wikibase-gap-analysis.md) | Concrete reuse boundaries, remaining integration work and proposed falsification tests against MyBrain's principles. |
| [OpenCloud–Wikibase trial design](docs/research/public/opencloud-wikibase-trial-design.md) | Proposed synthetic architecture, contracts and independent managed/native trial oracles. |
| [Repository structure](#repository-structure) | Locations for maintained documents and development tooling. |
| [Working agreements](#working-agreements) | Naming, source handling and publication boundaries. |
| [Git conventions](#git-conventions) | Issues, branches, commits and reviews. |
| [Agent instructions](AGENTS.md) | Shared PGMCP protocol, roles and workflow entrypoints. |
| [Agent collaboration](#agent-collaboration) | Mandated Co/Imp/QA interaction and isolated parallel worktrees. |
| [Quality policy](#quality-policy) | Required documentation/configuration evidence and explicit deferrals. |
| [Workspace setup](#workspace-setup) | The development harness and local environment. |

## Research baseline

The [public research edition](docs/research/public/research-baseline.pdf) is a
conceptual synthesis with synthetic evaluation cases. It omits names, operational
identifiers, account-specific observations, private links, exact administrative
counts and personal infrastructure details. It is not a complete copy of the
private inputs, an approved architecture or evidence of tested product behavior.

Original source PDFs must not be stored in this workspace or distributed through
Git. Private source material must not be copied into a public issue, pull request,
workflow-state file or attachment. Publication permission applies to the
screened edition only. Review each future edition independently.

## Repository structure

| Location | Contents and ownership |
| --- | --- |
| `README.md` | Project entrypoint, documentation index and repository agreements. |
| `AGENTS.md` | Entry to the workspace's maintained shared agent instructions. |
| `docs/research/public/` | Deliberately prepared and screened research editions. |
| Other paths under `docs/research/` | Ignored as a precaution; original private PDFs are excluded from the workspace. |
| `docs/development/issue<number>/` | Public-safe phase deliverables for real issues. |
| `docs/architecture/decisions/` | Architectural decision records when decisions are made. |
| `.agents/skills/` | Versioned references to shared PGMCP roles and procedures. |
| `setup/` | Portable quality and PGMCP collaboration sources; machine-specific records are ignored. |
| `requirements-pgmcp.lock.txt` | Development-harness dependencies, not application dependencies. |
| `.pgmcp/`, `.codex/`, `.runtime/`, `.venv/` | Local server data, machine configuration, Python runtime and environment. |

Create future directories with their first real artifact. Documentation locations
above are conventions, not claims that each future artifact already exists.
Introduce source, test and deployment directories after the relevant decisions;
the development harness does not choose an application stack.

## Working agreements

### Names and links

- Use lowercase directories and lowercase `kebab-case` names for new authored documents.
- Retain conventional filenames such as `README.md`, `AGENTS.md` and `SKILL.md`.
- Keep original private source PDFs outside this workspace; publish only screened derivatives.
- Use repository-relative Markdown links for published repository documents.
- Write maintained code, documentation and commit messages in English. Conversation
  follows the owner's language; private original sources retain their own language.
- Use UTF-8, LF line endings, one final newline and no trailing whitespace in authored text.

### Research, status and decisions

- Separate observations, source claims, interpretations, proposals and accepted decisions.
- Record document status and revision history with truthful authorship and dates.
- Keep cross-project public research in `docs/research/public/` and public-safe formal
  phase deliverables in the relevant real issue directory.
- Record accepted architectural decisions as ADRs under `docs/architecture/decisions/`,
  with alternatives and consequences. Do not publish private supporting evidence.
- Keep project-specific agreements here. [AGENTS.md](AGENTS.md) references the maintained
  shared PGMCP protocol rather than duplicating it.

### What belongs in Git

| Include | Exclude from Git |
| --- | --- |
| Maintained project documentation and accepted public-safe decisions. | Original research PDFs (also excluded from the workspace) and private source mappings. |
| Screened research editions under `docs/research/public/`. | Other content under `docs/research/`, including `private/`. |
| Portable `.agents/skills/` entrypoints and reviewed configuration examples. | Machine-specific `.codex/` registration and role deployment. |
| `.gitignore`, `.gitattributes`, `.python-version` and dependency lockfiles. | `.venv/`, `.runtime/`, downloaded packages and installation reports. |
| Future application source, meaningful tests and deployment scripts. | Credentials, real `.env` values, raw mailboxes, customer records, live databases, logs and backups. |

The research directory uses an explicit publication allowlist: only `public/` is
eligible for tracking. This is a storage boundary, not a claim that everything
placed there has been reviewed. Examine content, metadata, links and identifiers
before staging. New public examples must be synthetic and clearly identified.

`.gitattributes` normalizes authored text to LF and treats PDFs as binary evidence.
`.gitignore` neither removes already tracked content nor erases earlier commits.
Before any visibility change, review every published ref and its complete history,
including binary documents, attachments and commit metadata.

`.pgmcp/state.json` and `.pgmcp/deliverables.json` remain versioned branch-local
artifacts. Their contents must be public-safe too: retain public plans and lifecycle
facts, not private evidence, customer details or private source locations. PGMCP
neutralizes both files before PR submission. Bootstrap has no issue state.

Keep actual local configuration outside Git. Share reviewed portable templates
without credentials when needed. Use `.env.example` only for placeholders.
Local private-history backups must never be pushed, attached or mirrored.

## Git conventions

- `main` is the integration base. Do real issue work on registered issue branches.
- Coordination selects a real issue, creates and checks out its branch, and calls
  `initialize_project` with the explicit parent. Use the returned branch identity.
- Use configured branch types: `feature`, `bug`, `refactor`, `docs`, `hotfix`, `chore`
  and `epic`, according to actual issue scope.
- Use concise English commit messages with a configured type and clear outcome.
  PGMCP owns workflow-specific formatting for governed issue work.
- Keep commits focused and review their full content before publication.
- Use separate implementation and independent QA chats as defined in [AGENTS.md](AGENTS.md).
- Do not force-push or merge as a setup shortcut. A privacy-driven history replacement
  requires explicit owner approval and a guarded remote update. Preserve the screened
  replacement until verified; do not retain copies of source material the owner asked to remove.
- Remote branch protection must be verified after repository visibility or plan changes.
  These written agreements do not themselves configure GitHub protection.

## Agent collaboration

[Shared collaboration policy](setup/pgmcp/agents/collaboration.md) defines
interactive operation and owner-mandated coordinated execution. Co coordinates
the issue graph and role assignments, delegates technical installation/work to
Imp, and requests independent QA at required phase boundaries. QA returns
revision-bound GO/NOGO to the authorized participants; producer preflight remains
findings-only. One context keeps one role.

Every worktree requires its own PGMCP server instance and correctly bound
connection with a distinct name for each admitted worktree. Each worktree may
have its own independent QA context. At most one mutating Imp, including delegated
implementation workers, may be active per worktree. Co manages assignment/release and serializes shared
integration actions. Different admitted worktrees can run their own Imp in parallel.
Co reconstructs durable progress from Git and existing workflow/planning evidence;
overviews are disposable. Live agent/tool status governs safe handoff. The original
independent QA-chat verdict suffices at required review boundaries; no additional
Co progress register, verdict store or technical QA gate is required.

The [portable deployment map](setup/pgmcp/README.md) identifies reviewed generic
sources, the PGMCP 4.0.0 phase-instruction override and local Codex role consumers.
Version generic sources under setup/pgmcp; deploy exact reconciled copies to each
worktree's .pgmcp. Keep actual host paths, chat IDs and credentials local. Rebase
reviewed workspace changes when upgrading package sources; do not silently replace
them with an older packaged protocol.

A short owner prompt may select the documented autonomous local product profile.
It delegates bounded local work and role routing, with installation executed by
Imp. Public deployment, spending, push/PR publication, merge and closure need
explicit scoped authority. Host permissions and tool-specific authorization remain
in force. The current issue documents this model; it does not establish live
multi-worktree isolation, a technical writer lock or guaranteed unattended delivery.

## Quality policy

The owner approved the documentation/configuration quality policy in issue #2 on
2026-10-21. [Quality setup](setup/quality/README.md) documents the reviewed native
bindings, pins, deployment and verification. Local .pgmcp/config overrides deploy
those sources; packaged defaults remain unchanged.

| Surface | Required evidence |
| --- | --- |
| Maintained Markdown | Native offline local-link and heading-fragment validation. External URLs are excluded. |
| Changed YAML configuration | Native mapping-root validation plus actual consumer admission after configuration reload. |
| Changed JSON Schema | Separate native Draft 2020-12 envelope and metaschema validation. |
| Application checks and tests | Deferred until the application stack, source/test roots and quality rules are approved. |
| Automated fixes and native Commitlint | Deferred until a specific policy is approved; retain PGMCP commit conventions. |

Use explicit file-family targets during implementation. Normal scaffolding and
guarded editing use enforce; report is a diagnostic/setup exception and can persist
failed or unvalidated content. In Validation, run the repository_review profile on
the branch once after final implementation changes, plus the workflow-required
configured-scope test request. Tests are currently inactive: no active tests is no
passing test evidence. Required applicable checks must execute and pass before
acceptance. An unavailable or unexecuted required check remains a blocker.

Only branch scope applies the per-check target include/exclude policies; other scopes
must select appropriate file families explicitly. Exclusions cover server data,
machine settings, environments, dependencies, downloads, local records and generated
or disposable output. They do not prevent link resolution to referenced files.

Native checks, tests and fixes have separate evidence. An acknowledged binding,
successful tool envelope, empty selection, clean Git status or healthy MCP startup
does not establish quality readiness. Future policy changes require an explicit
owner decision, reviewed portable sources and fresh evidence for affected boundaries.

## Workspace setup

The repository is [MikeyVK/MyBrain](https://github.com/MikeyVK/MyBrain).
PGMCP **4.0.0** is the development harness. Its workspace environment uses CPython
**3.15.0**; these versions do not prescribe the application's runtime.

```powershell
& '.\.venv\Scripts\python.exe' -m pip check
& '.\.venv\Scripts\pgmcp.exe' --version
```

The initialized server root is `.pgmcp`. Codex reads workspace registration from
`.codex/config.toml`; `GITHUB_TOKEN` comes from the host environment. Machine paths,
installation narratives, verification logs and private recovery bundles stay local.

Use separate chats with `$pgmcp-co`, `$pgmcp-imp` and `$pgmcp-qa`. Read the complete
shared source protocols through [AGENTS.md](AGENTS.md) before governed issue work.
A fresh workspace must provision the pinned harness and deploy its shared instruction
sources; copied configuration filenames alone do not establish an active connection.
