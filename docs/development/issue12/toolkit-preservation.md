<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# e-Boekhouden toolkit preservation inventory

**Status:** Default-disabled research source preserved; final Research review pending  
**Version:** 0.2  
**Last Updated:** 2026-11-01

## Authority and scope

The owner explicitly authorized preserving existing tested writing functions as
source, with nothing executed against an account. The former operational run is
closed. This toolkit supplies no account authorization, MCP implementation,
application-stack selection, production claim or automatic old-plan continuation.
Original private sources remain unchanged; detailed private source-path/SHA mapping
is outside Git.

## Original-to-retained dependency closure

All 29 selected modules are retained under the flat
[toolkit source root](../../../tools/eboekhouden/README.md), with the callable
omissions below. Source and runtime paths are separated; only the fixed ignored
`.local-work/` is eligible for CLI config/input/output/journal/lock data.

| Original functional family | Retained modules |
| --- | --- |
| Shared boundaries | `probe.py`, `private_output.py`, `app_session.py` |
| Official REST and host credentials | `credential_store.py`, `probe_rest.py`, `setup_credential.py` |
| App selected reads/archive | `app_probe.py`, `archive_read.py`, `processed_invoice_probe.py` |
| Prebooking libraries and admitted REST commands | `preflight.py`, `catalogue_match.py`, `full_relation_names.py`, `relation_supplement.py`, `create_relations.py`, `book_one_invoice.py`, `reconcile_one_invoice.py`, `rest_create_command.py` |
| Archive upload | `upload_invoice.py` |
| Edit preparation and narrow ledger change | `prepare_edit.py`, `change_ledger.py` |
| Link query/command | `probe_link_contract.py`, `link_invoice.py` |
| Source-description and protected metadata contracts | `booking_source_guard.py`, `repair_contract.py`, `repair_io.py`, `metadata_repair.py` |
| Hours | `hours_cli.py`, `hours_domain.py`, `hours_io.py` |

The additional `toolkit_runtime.py` owns the fixed local work boundary and disabled
real-host gate. `quality/adapter.py` and `quality/bootstrap.py` are verification
sources, not accounting helpers. No empty scaffold is presented as functionality.
The retained dependencies are standard library plus pinned certifi; pytest and its
pinned adapter dependencies are isolated verification dependencies.

## Operation/route/evidence distinctions

| Capability | Preserved route/contract | Evidence and limitation |
| --- | --- | --- |
| Official financial/reference read | Session POST, bounded mutation/relation/ledger GET, own-session DELETE | Selected historical live evidence plus current fake-transport tests. Authentication side effects are separate from bookkeeping reads. |
| App context and selected read | Login POST, userinfo GET, bounded day-filter POST, internal-ID GET | Filter POST is a read query. Current administration and visible/internal mapping are checked; no silent admin switch. |
| Archive list/metadata/content | Bounded bestanden GET/list/detail/download | PDF/image magic, MIME, byte/size/hash, fixed TLS origin and identity controls. |
| Supplier creation | Explicit admitted POST `/v1/relation` and GET readback | Default dry-run, bounded explicit profiles, identity precheck/journal/no replay. No profiles or old owner decision is shipped. |
| Purchase invoice creation | POST `/v1/mutation`, type 1, strict GET readback | Bounded IN/EX/multirow/credit/private/reverse-charge contracts, source descriptions and explicit source-versus-booking evidence. Not payment or sales creation. |
| Archive upload and link | POST bestanden `upload` and `koppel`; `gekoppeld` POST is a query | Distinct received candidate ID versus verified file; before/after byte/link/full-REST checks. Shared PDF retention was a separate historical proof. |
| Guarded mutation change | PUT `/api/v4/mutaties` | Narrow tested ledger/text cases; not arbitrary updates. Header route still blocks missing/ambiguous outstanding, unsupported paid/EX cases and whitespace identifiers. |
| Archive rename | PUT `/api/v4/bestanden` with `id,naam` | No upload/move/new ID. Preserve bytes, metadata, all target links and full REST. Exact absent outstanding remains NOT_RETURNED, never paid/open zero. |
| Hours | GET detail, POST filter query; admitted POST/PUT `/api/v4/uren` | Separate historical hours scope and current synthetic tests. DELETE by ID is allowed only by receipt-owned synthetic cleanup, not a generic delete tool. |
| Native paid-description editing | Native UI/manual observation and protected before/after reads | Verified manual workflow; no reusable CLI/MCP endpoint preserved. |
| Bank-worklist processing, arbitrary paid update, sales workflow | No preserved supported command | Remains unavailable/unproved; public API documentation alone is not a tested helper. |

New local host configuration and a new operation-specific owner mandate are
necessary before any future account use. Real HTTPS constructors, host identity
and Windows credential backend access are blocked when config is absent/disabled.
No account access occurred during extraction/tests. Injectable fake transports,
identity readers and private-output path validators remain test seams.

## Exact omissions and test dispositions

| Original callable/test | Disposition |
| --- | --- |
| `probe.choose_candidate`, `probe.main` | Omit obsolete interactive search/password CLI; retain shared pure/secure-input/ACL functions. |
| `preflight.report`, `preflight.main` | Omit historical fixed-count/financing batch orchestration; do not relocate it. |
| `catalogue_match.collect`, `catalogue_match.main` | Omit old owner-confirmation/profile batch. `checked` is retained because admitted command readers require this generic hash-bound JSON dependency. |
| `full_relation_names.main`, `relation_supplement.main` | Omit old batch CLIs; retain bounded read library functions. |
| Catalogue incomplete-batch test | Replace `test_incomplete_catalogue_stops_before_details` with `test_incomplete_pagination_is_not_complete_coverage` through the retained pagination library. Its nested fake detail method is omitted with that old batch test. |
| Two-row VAT fixture label | Rename to `test_synthetic_two_rows_absent_vat_exact_group_total`; use synthetic amounts instead of the original operational values. Same representation/group invariant. |
| Test fixtures and CLI tests | Replace actual identifiers, dates, names/markers and copied operational amounts with synthetic values. Inject temp output/path and fake identity/backend explicitly; do not weaken real runtime guards. |
| Admission probes | Retired privately after actual native positive/negative evidence; excluded from deliverables/tests. |
| Four nested-environment adapter probes | Preserve their historical actual output privately; retain twelve portable adapter policy regressions instead. |

These are eight omitted helper callables, not eight omitted modules. The 21 retained
research test files contain 255 test methods, counting the one replacement and one
rename above. Eight new runtime/import tests and twelve retained scoped-adapter
tests yield the complete suite below. All original selected source/test bytes
were checked unchanged against their private source hashes after extraction.

## Current verification evidence

| Native invocation / scope | Actual observed result |
| --- | --- |
| `run_tests(scope="targets", targets=["tools/eboekhouden/tests"], tests=["eboekhouden_research_tests"])` | 275 tests and 145 subtests passed; Python 3.15.0 in toolkit `.venv`, pytest 9.1.1 and exact declared native test pins. |
| Scoped Python content edits and explicit toolkit syntax selection | Native AST admission; no report-mode Python. Invalid content and outside targets were separately refused at the reviewed bootstrap boundary. |
| Changed Markdown, explicit `markdown_links` | Native offline local-link/fragment checking; external URLs excluded, not falsely reported as network-verified. |
| Scoped YAML/examples, explicit `yaml_configuration` | Native mapping-root validation; effective adapter consumer admission independently checked at bootstrap. |
| Dependency lock, pytest.ini, exact two ignore rules | Named setup/report exception; not_executed/no registered validator, direct contents reviewed. No source/test/doc exclusion added. |
| Configured empty tests | Unavailable; never a complete-suite or configured pass. |

The full import test forbids host DLL/HTTP/subprocess/private-file/directory effects
in a fresh child while importing all 29 modules. Native test execution additionally
refuses socket operations and host credential symbols. This protects trusted
synthetic tests, not malicious arbitrary code. No SDK, MCP server or fresh account
integration was executed.

## Remaining architecture work and usage

Preserving legacy behavior does not make it directly MCP-ready: transport/session
and supplier policy remain coupled in preflight, capture composes multiple read
domains, and CLI presentation still exists. Authentication expiry/concurrency,
per-process shared audit ownership and cross-process coordination remain explicit
[Research inputs](mcp-research-inputs.md), not implemented server guarantees.
A generic raw HTTP endpoint or automatic retry would bypass the retained contracts.

Use the [fresh-chat and CLI runbook](../../../tools/eboekhouden/README.md) and
[portable quality source/deployment map](../../../tools/eboekhouden/quality/README.md).
Historical live proofs and old private journals are provenance only. Final review
still binds a committed source snapshot; no phase exit, push or production
authorization is implied.

## Version history

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1 | 2026-10-31 | Imp | Record partial admitted extraction and explicit omitted boundaries. |
| 0.2 | 2026-11-01 | Imp | Record approved default-disabled writer source, complete closure, dispositions and actual isolated offline suite. |
