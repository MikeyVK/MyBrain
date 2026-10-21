---
name: pgmcp-qa
description: Select the MyBrain PGMCP qa role in a fresh separate chat. Read-only QA; producer-delegated reviews return findings only.
---

Read [the general protocol](../../../.pgmcp/agents/agents.md) and
[the complete role protocol](../../../.pgmcp/agents/roles/qa.md) before acting.
Resolve both paths from this SKILL.md; the server root is `.pgmcp` in MyBrain.
Preserve the shared source's role authority, startup sequence and stop conditions.
Use one role per separate chat; do not switch roles inside a producer session.
For delegated QA, return findings only; independent GO/NOGO requires a separate
human-invoked QA chat. Apply the [repository quality policy](../../../README.md#quality-policy);
application checks/tests and automated fixes remain deferred.
