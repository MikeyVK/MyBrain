# MyBrain workspace instructions

For PGMCP work, read and follow the maintained shared protocol at
[.pgmcp/agents/agents.md](.pgmcp/agents/agents.md). Resolve shared documentation
links from the original source files under `.pgmcp`, not from this entrypoint.
The bootstrap entry is [.pgmcp/docs/setup/agentic-bootstrap.md](.pgmcp/docs/setup/agentic-bootstrap.md).
Read the [repository agreements](README.md#working-agreements) and
[Git conventions](README.md#git-conventions) for MyBrain-specific document
locations, naming and handling of source material. Keep those agreements in the
README rather than duplicating the shared PGMCP protocol.

Use the workspace-local `pgmcp` MCP connection. Its environment is `.venv`, its
workspace is this repository and its server-data root is `.pgmcp`.
Credentials come from the host environment; never copy them into tracked files.

Select one role in a separate chat and read its complete shared protocol:

- `$pgmcp-co`: [.pgmcp/agents/roles/co.md](.pgmcp/agents/roles/co.md).
- `$pgmcp-imp`: [.pgmcp/agents/roles/imp.md](.pgmcp/agents/roles/imp.md).
- `$pgmcp-qa`: [.pgmcp/agents/roles/qa.md](.pgmcp/agents/roles/qa.md).

The matching custom agents are `pgmcp-co`, `pgmcp-imp` and `pgmcp-qa`.
A producer-delegated QA review returns findings only. Independent GO/NOGO
requires a separately invoked QA chat; do not switch producer and QA roles
inside one chat. The QA protocol is read-only; do not assume a custom-agent
file changes the parent session's filesystem permissions.

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
