<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# e-Boekhouden research toolkit

**Status:** Source preserved for offline research; live execution disabled by default  
**Version:** 0.3
**Last Updated:** 2026-11-01

This isolated Python toolkit preserves screened research helpers and their synthetic
regressions. It is not a MyBrain application-stack decision, an MCP server, a
production-readiness claim or authority to continue a closed administrative run.
The owner explicitly authorized preserving existing writing functions as source,
with nothing executed against an account.

## Fresh-chat bootstrap

1. Resolve this checkout's dedicated PGMCP connection locally and call its
   `get_work_context`. Verify issue, branch, phase, assigned role and mutation owner;
   do not substitute another worktree's connection.
2. Read the [preservation inventory](../../docs/development/issue12/toolkit-preservation.md),
   [MCP research inputs](../../docs/development/issue12/mcp-research-inputs.md),
   [proposed MCP design](../../docs/development/issue12/design.md) and
   [quality bootstrap](quality/README.md). Historical private plans are not inputs.
3. Create `.venv` using CPython 3.15.0 without system site packages and install
   [requirements.lock.txt](requirements.lock.txt). This environment is independent
   of the PGMCP server environment and does not change global PATH.
4. Review/reconcile the maintained scoped quality sources to the ignored local
   adapter/configuration, reload each named consumer and verify actual admission.
5. Run native explicit toolkit syntax targets and the complete test directory:
   `run_tests(scope="targets", targets=["tools/eboekhouden/tests"], tests=["eboekhouden_research_tests"])`.
   Configured empty selection is unavailable, never a passing test.
6. Stop at offline inspection unless a new owner task explicitly authorizes account
   access. No credential setup, browser action, login, upload or write follows from
   checkout, import, help, a passing test or this document.

## Source and private runtime

All helper imports are flat within this directory. `toolkit_runtime.SOURCE_ROOT`
identifies code; only the fixed ignored `.local-work/` subtree may hold CLI runtime
configuration, inputs, receipts, journals and locks. Semantic areas are `rest`,
`app`, `prebooking`, `uploads`, `edits`, `ledger`, `links`, `metadata` and
`hours`. The boundary rejects source/system targets, traversal and symlink/reparse
ancestors before ACL/output actions.

Real credential/identity backends and the real HTTPS constructor require ignored
`.local-work/host-config.json` with `allowLiveOperations` explicitly true. Absence
or false blocks them. [Disabled-host example](examples/disabled-host.example.yaml)
is reviewable YAML data, not a runtime file; runtime configuration is JSON. A new
mandate and reviewed operation-specific inputs are also necessary: enabling a
local boolean is not authorization. Credentials remain in exact-key host Windows
Credential Manager entries; never in config, arguments, environment, logs or Git.
Tests inject fake backends/path validators rather than weakening the host boundary.

[Example context](examples/synthetic-context.example.yaml) contains fictional IDs
and a future date only. No real source snapshots, supplier profiles, PDFs, journal,
received ID, owner exception or executable write plan is distributed.

## Existing entrypoints

Append `--help` to inspect argument syntax without starting an account operation.
The table describes preserved capabilities, not commands to run now. Scripts require
new private, hash-bound inputs and explicit host configuration. Unlisted library
modules have no preserved batch CLI.

| Module | Existing modes / effect | Private area |
| --- | --- | --- |
| `probe_rest.py` | `--number`: one official REST read; own transient session cleanup | rest |
| `app_probe.py` | `--number --date`: App context-confirmed bounded day lookup/detail | app |
| `archive_read.py` | `--admin-id [--directory-id]`: bounded metadata read | app |
| `processed_invoice_probe.py` | `lookup --invoice-number`; `download --file-id --admin-id` | app |
| `create_relations.py` | `--manifest-sha256`, dry-run; explicit `--apply` creates only admitted profiles | prebooking |
| `book_one_invoice.py` | `--input --input-sha256`, dry-run; `--apply` one purchase invoice | prebooking / bound case |
| `reconcile_one_invoice.py` | Offline hash-bound receipt reconciliation, append-only journal; no account calls | prebooking / bound case |
| `upload_invoice.py` | Dry-run; explicit `--apply`; read-only reconcile; separately bound one-extra recovery | uploads / source-SHA case |
| `prepare_edit.py` | Prepare/verify; `--capture-readonly` is an account query; apply intentionally refused | edits |
| `change_ledger.py` | Dry-run; explicit admitted one-row ledger-only `--apply` | ledger |
| `probe_link_contract.py` | One source-bound link-membership query; no link write | links |
| `link_invoice.py` | Dry-run, `--read-check`, one explicit `--apply` existing-file link | links |
| `metadata_repair.py` | `header`/`rename` with explicit `--prepare` or hash-bound `--apply` | metadata |
| `hours_cli.py` | prepare-create/edit/owned-cleanup, read/query-marker, dry-run apply, explicit apply, reconcile | hours |
| `setup_credential.py` | Explicit local credential setup only; not implicit authentication/read | rest |

Bounded legacy limits, such as admitted profile batches, row counts, source recovery
sets and selected MIME types, are helper scope limits, not vendor API limits.
Cleanup of hours records remains receipt-owned synthetic cleanup, never generic
deletion. No native-browser editing implementation or generic raw-HTTP tool is
included.

## Evidence and remaining limits

The complete explicit native test-directory selection passed **275 tests and
145 subtests** in the isolated environment. This comprises 255 retained/replaced
research test methods, twelve scoped-adapter regressions and eight runtime/import
checks. Full module-import checks deny host/runtime effects; actual tests are
offline and credential-free. The inventory records exact invocation and omissions.

Official REST is the default for accounting truth and supported operations. App-v4
is an incompletely captured supplement only for actual REST gaps. Preserve
number/internal-ID namespaces, fresh baselines, money/terms/VAT, positive payment
evidence and all shared PDF links. Missing outstanding is not paid/open zero.
App updates can replace IDs and normalize invoice-number whitespace. Separate
row-text persistence, arbitrary updates and bank-worklist processing are not proved.

Shared modules are legacy reuse, not established process-lifetime ownership or
MCP-ready architecture. PrivateOutput still contains CLI presentation; SDK/transport,
expiry/concurrency and server audit lifetimes are specified in the proposed
[MCP design](../../docs/development/issue12/design.md); they remain unimplemented.
The independent Research consolidation GO binds revision
`68bafa6750e64b99cc758f30377fa648566080eb`, not the new Design's acceptance. Unknown
writes remain uncertain: durable PENDING precedes dispatch, preserve received
identifiers/observations and never automatically replay, roll back or recreate.
Local locks and readback comparisons do not guarantee provider CAS or global
exactly-once behavior.

## Version history

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1 | 2026-10-31 | Imp | Extract admitted readers/libraries and verification sources. |
| 0.2 | 2026-11-01 | Imp | Preserve explicitly authorized default-disabled command source, complete offline closure and fresh-chat runbook. |
| 0.3 | 2026-11-01 | Imp | Link proposed Design and distinguish implemented research preservation from future MCP lifecycle. |
