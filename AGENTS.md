# MyBrain workspace instructions

For PGMCP work, read and follow the maintained shared protocol at
[.pgmcp/agents/agents.md](.pgmcp/agents/agents.md). Resolve shared documentation
links from the original source files under `.pgmcp`, not from this entrypoint.
The bootstrap entry is [.pgmcp/docs/setup/agentic-bootstrap.md](.pgmcp/docs/setup/agentic-bootstrap.md).
Read the [repository agreements](README.md#working-agreements) and
[Git conventions](README.md#git-conventions) for MyBrain-specific document
locations, naming and handling of source material. Keep those agreements in the
README rather than duplicating the shared PGMCP protocol.

Use the assigned worktree's dedicated `pgmcp` server instance and connection.
Each worktree has its own workspace/server-data binding; never route a child
worktree through a parent's fixed-root connection. Co verifies assignment and
mutation ownership; at most one mutating Imp, including descendants, may be active
per worktree. Co delegates installation and environment provisioning to Imp.
Credentials come from the host environment; never copy them into tracked files.

Select one role in a separate chat and read its complete shared protocol:

- `$pgmcp-co`: [.pgmcp/agents/roles/co.md](.pgmcp/agents/roles/co.md).
- `$pgmcp-imp`: [.pgmcp/agents/roles/imp.md](.pgmcp/agents/roles/imp.md).
- `$pgmcp-qa`: [.pgmcp/agents/roles/qa.md](.pgmcp/agents/roles/qa.md).

The matching custom agents are `pgmcp-co`, `pgmcp-imp` and `pgmcp-qa`.
Read the [shared collaboration policy](.pgmcp/agents/collaboration.md) for
interactive/coordinated authority, direct routing, revision-bound verdicts and
resumption. Independent QA is directly owner-appointed or appointed by Co under
explicit original owner delegation; an owner-appointed QA remains independent when
Imp delivers the request. Imp-created preflight is findings-only. Keep producer
and independent reviewer in separate role contexts. Read-only instructions do not
change inherited sandbox permissions.

The [portable source/deployment map](setup/pgmcp/README.md) versions the generic
sources and phase override; effective `.pgmcp` and local `.codex` consumers must be
reconciled before activation. Host-specific launch paths and live chat mappings
remain local-only. Repository files cannot expand host/tool authorization.

Workflow entrypoints are `$pgmcp-start`, `$pgmcp-go`, `$pgmcp-create-issue`,
`$pgmcp-start-issue` and `$pgmcp-end-issue`. Each reads its complete shared
procedure from `.pgmcp/agents/workflows/` and preserves its authorization,
argument requirements, modes and stop conditions.

Follow the [repository quality policy](README.md#quality-policy) for required
documentation/configuration checks, deployment sources and evidence. Application
checks/tests and automated fixes remain deferred. Do not acknowledge unresolved
bindings or interpret healthy startup as quality readiness.

Workspace bootstrap is distinct from issue lifecycle work. Use the packaged
bootstrap for setup and connection verification; never fabricate an issue or
branch state for setup. Implementation of a real issue requires coordination
to prepare its branch and call `initialize_project` with an explicit parent.

Original private research PDFs must not be stored in this workspace. Machine-specific
setup records stay local-only. Only screened editions under `docs/research/public/`
may be published.
The same boundary applies to issues, PRs, attachments, `.pgmcp/state.json` and
`.pgmcp/deliverables.json`: durable branch state must not contain private evidence,
personal or customer identifiers, credentials, or private source locations.
