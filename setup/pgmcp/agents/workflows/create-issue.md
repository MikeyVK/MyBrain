<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# PGMCP create-issue Procedure

**Status:** Active

**Version:** 1.1

**Last Updated:** 2026-10-21

## Purpose

Define the shared create-issue procedure independently of host command or skill registration.

## Summary

Role: @co. Preserve the existing sequence, stop conditions and authority when adapting its registration to the environment.

## Protocol

Read [collaboration.md](../collaboration.md) for interactive/coordinated mode,
original owner authority, direct routing, dedicated server identity and mutation ownership.
Coordinated operation never expands host/tool permissions or producer review authority.

Guide through scaffolding a GitHub issue body and submitting it as a real GitHub issue.

## Required Input

Extract from the invocation argument:

- `ISSUE_TYPE` — the issue type (e.g. `feature`, `bug`, `refactor`). Valid values are injected at runtime into the `create_issue` tool schema — check the schema if uncertain.
- `DESCRIPTION` — short description (optional; used as a starting point for the title)

If ISSUE_TYPE is absent, Co may classify within explicit owner-delegated issue-authoring authority using the live schema and recorded objective. Otherwise ask the owner. Do not infer authority or invent an unsupported type.

---

## Step 1: Discover available fields

Call `scaffold_schema(artifact_type="issue")`.

Read the description of each optional field in the returned schema. Using `ISSUE_TYPE` as the selection criterion, select the optional fields whose descriptions match the character of this issue type. Skip fields that are not relevant.

Do not ask about fields you did not select unless the user volunteers them.

---

## Step 2: Collect content

Use conversation context or ask the user for:

- Publication `title` — concise issue title for `create_issue` (required; not a scaffold-context field)
- `problem` — what is wrong or needed (required)
- The optional fields selected in Step 1

---

## Step 3: Collect metadata

Use explicit assignment/mandate values or classify within verified owner-delegated metadata authority; otherwise ask the owner for:

- `priority` — valid values are injected at runtime from config into the `create_issue` tool schema. Use its explicit admitted default when one exists; otherwise ask rather than copying another workspace's priority.
- `scope` — valid values are injected at runtime from config into the `create_issue` tool schema. Ask if unclear.
- `is_epic` — `true` only when `ISSUE_TYPE` is `epic`. Default `false`.
- `parent_issue` — parent issue number (optional, positive integer).
- `milestone` — milestone title (optional).
- `assignees` — list of GitHub logins (optional).

Select priority/scope only from live admitted values and the mandate's objective. Record Co's rationale when choosing under delegation; uncertainty outside that authority requires an owner decision.

---

## Step 4: Scaffold the issue body

Call `scaffold_artifact` with the discovered issue-body context. Omit optional fields that were not supplied; preserve explicitly supplied empty values when the schema admits them and they express the caller's intent. Publication title, labels, priority and other envelope metadata belong to `create_issue`, not the scaffold context.

```
scaffold_artifact(
  artifact_type="issue",
  file_name="<slug-from-title>.md",
  context={
    "problem": "<problem>",
    # include admitted optional fields selected in Step 1 that the user provided
  }
)
```

Read the exact saved file returned by `scaffold_artifact`. Keep its technical provenance in the local artifact. For publication, remove only a recognized first-line `<!-- pgmcp:v1 ... -->` marker and its separating blank line; retain all other comments, content, internal whitespace and real newlines. If that first-line marker is absent, publish the file content as read. In interactive mode show the concrete publication body/title to the owner before submitting. In coordinated mode Co records/reviews that concrete body against the original mandate's issue-creation and repository publication scope. If that explicit authority is absent, request owner confirmation. Always apply the repository's public-safe material boundary.

> **Important:** Pass the exact reviewed publication body as `body` in Step 5. Perform only the provenance extraction above; do not retype or reconstruct the Markdown or convert real newlines to literal `\n` sequences.

---

## Step 5: Create the issue

After direct owner confirmation or verification of the original mandate's explicit scoped issue-creation/publication authority, submit with:

```
create_issue(
  issue_type="<ISSUE_TYPE>",
  title="<title>",
  priority="<priority>",
  scope="<scope>",
  body="<rendered markdown from Step 4>",
  is_epic=<true|false>,
  parent_issue=<number>,   # omit if not set
  milestone="<milestone>", # omit if not set
  assignees=["<login>"]    # omit if not set
)
```

Report the created issue number and URL to the user.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-21 | @imp implementer | Consolidate the existing procedure without host registration metadata; retain its role, sequence, review boundaries and explicit authorization. |
| 1.1 | 2026-10-21 | @imp documenter | Reconcile coordinated authority, direct handoff and bounded continuation. |
