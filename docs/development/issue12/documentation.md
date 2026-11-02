<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Issue 12 research closeout

**Status:** RESEARCH CLOSEOUT SNAPSHOT — independent review pending  
**Version:** 1.1  
**Last Updated:** 2026-11-02

## Purpose

Preserve the delivered e-Boekhouden research, screened toolkit and reviewed concept boundaries so later work can resume without implying a completed connector or bookkeeping system.

## Summary

The owner requested research-only branch closeout on 2026-11-02. Source preservation and concept design are delivered; Planning, MCP implementation and production acceptance were not performed. This is the review snapshot for that closeout, not a new provider or accounting architecture decision.

## Delivered scope and chronology

| Result | Entry point | Meaning at closeout |
| --- | --- | --- |
| Official REST/SOAP and community App evidence | [API catalogue](api-catalog.md), [App assessment](app-api-v4-assessment.md) | Historical interface comparison; SOAP excluded. |
| Screened helper preservation | [Preservation inventory](toolkit-preservation.md), [toolkit runbook](../../../tools/eboekhouden/README.md) | Existing REST-first/App-gap helpers retained with default-disabled live execution and synthetic tests. No new account authority. |
| Consolidated MCP inputs | [Reuse inputs](mcp-research-inputs.md) | Historical helper/lifecycle evidence, not a running server. |
| Function-first APK evidence | [57-group/23-configuration matrix](api-functional-coverage.md), [APK catalogue](apk-api-contracts.md) | Static contracts and explicit gaps; selected historical runtime observations remain narrowly qualified. |
| App-only technical concept | [Design](design.md), [contracts](design-contracts.md), [endpoint admission](endpoint-design-catalogue.md) | Owner-selected APK-backed App-v4 baseline; named technical endpoints, shared auth/logging and no local bookkeeping decisions. Unimplemented. |
| Later web-gap evidence | [Web-backend overlay](web-backend-gap-research.md) | Browser JSON `/v1/api/` is a third distinct family, separate from official REST and App-v4. It qualifies completeness, not route selection. |

Independent review accepted consolidation at `68bafa6750e64b99cc758f30377fa648566080eb`, the earlier workflow-shaped Design at `1d2fc8da06ac41c49134e5ee1bc67e1a347413b5`, the replacement App-only Design at `12e7fe8cd4f69de010c6209efcb93b08d9d5b492` and the screened web-gap research/publication at `aec2e7aa97d8d8582f3e783b128bce9351d99ef3`. These are historical scope/revision facts verified from the original reviewer replies. They do not approve this closeout snapshot or confer live execution authority.

## Reproduce offline evidence

Use this checkout's verified dedicated PGMCP connection, the [toolkit quality bootstrap](../../../tools/eboekhouden/quality/README.md) and its pinned isolated environment. Keep default native arguments; do not enable live operations or supply credentials. The scoped adapter confines source/test selection and refuses socket and host-credential API calls during tests.

| Native request | Observed on 2026-11-02 |
| --- | --- |
| `run_checks(scope="targets", targets=["tools/eboekhouden"], checks=["eboekhouden_syntax"], timeout_seconds=60)` | Passed; all 56 selected Python source/test/quality files parsed using CPython 3.15.0. |
| `run_tests(scope="targets", targets=["tools/eboekhouden/tests"], tests=["eboekhouden_research_tests"], timeout_seconds=240)` | Passed; 275 tests and 145 subtests, pytest 9.1.1, native exit 0. |
| `run_tests(scope="configured", timeout_seconds=240)` | Unavailable: `unsupported_input`, `EXPLICIT_NONEMPTY_SELECTION_REQUIRED`; no configured-suite pass is claimed. |

A later closeout format correction removed only surplus terminal empty lines, leaving exactly one final LF in seven retained files under `tools/eboekhouden/`: `full_relation_names.py`, `hours_domain.py`, `preflight.py`, `probe.py`, `relation_supplement.py`, `tests/test_quality_adapter.py` and `tests/test_upload_invoice.py`. Their complete preceding byte prefixes remain identical to `e2ee57339f425bd75d3b33f7f74a39d23bee87ef`; native AST admission passed for each edit. No implementation, fixture or behavioral change was made. Original extraction/hash facts and the behavioral results above remain historical snapshot evidence; current retained bytes include this explicit format-only delta. The unchanged behavioral suite is not repeated for terminal whitespace alone.

Final documentation/configuration verification uses `run_checks(scope="branch", profile="repository_review")` after content is final. Its actual result belongs in the revision-bound hand-over; this document does not predeclare that result. Required Markdown checks use native offline local links/fragments; external URLs are excluded. MyBrain application tests/checks and automated fixes remain deferred under the [repository policy](../../../README.md#quality-policy). The explicit complete toolkit selection above supplies the approved toolkit test evidence.

`git_fetch(remote="origin", prune=false)` succeeded for closeout. At inspection, `main` and `origin/main` both resolved to `49b534db1f3eacfb8fd8bcdbca09f6d130727449`; no incoming main drift required reconciliation. No merge or rebase was performed during snapshot preparation.

## Precise limitations and deferred work

Full coverage of all inventoried functions through App-v4 remains unproved. Concrete web contracts do not demonstrate App equivalents, complete web parity, shared authentication, supported integration use or runtime correctness. A uniform web route and App+web composition remain unselected alternatives. The App-only baseline is retained only for admitted evidence, with gaps unavailable.

There is no MCP implementation, installed SDK handshake, endpoint-server test suite, deployment, current live test, bookkeeping engine or complete storage product. Toolkit regression results prove preserved helper behavior under fakes; they do not prove the later MCP design, Dutch accounting correctness or provider-wide idempotency. Unknown command outcomes remain uncertain; no automatic replay, compensation or account operation follows from this closeout.

A [single follow-up issue draft](follow-up-issue-draft.md) preserves the deferred route, ledger/kernel and implementation decisions. It has not been published as a new issue. Future work needs a separately authorized scope and normal strategy/Design/Planning review.

## Exploratory MyBrain accounting feasibility

This brief note preserves the final feasibility discussion; it is exploratory, not an ADR or a selected build. Invoices, suppliers, documents and payments can share a data environment. That does not by itself supply accounting guarantees. The design inference is that one canonical deterministic ledger must own balanced postings, corrections, closed periods and reproducible financial outcomes; MyBrain may retain sources, versions and provenance around it. Source changes must not silently repost historical transactions. MyBrain's [storage Design](../issue6/design.md) is designed, not fully implemented.

| Reuse candidate from the discussion | Bounded evidence and unresolved fit |
| --- | --- |
| Tryton | [Accounting concepts](https://docs.tryton.org/latest/modules-account/design/index.html) include balanced posting and cancellation moves; [RPC](https://docs.tryton.org/latest/server/topics/rpc.html) offers a programmable boundary. Actual MyBrain integration and Dutch completeness remain unproved. |
| LedgerSMB | [First-party feature list](https://www.ledgersmb.org/index.php/content/features) includes ledger, invoices, bank reconciliation, hours and assets. This is candidate evidence, not an audited integration contract. |
| ERPNext | A broader reuse candidate; the [official deployment database section](https://github.com/frappe/helm/blob/main/erpnext/README.md#database) requires MariaDB for ERPNext. It is not evidence that ERPNext can share a proposed PostgreSQL store. |

Dutch VAT/ICP calculations and corrections, SBR/Digipoort/certificate-based electronic submission, bankfeeds, migration reconciliation and full restore each need separate proof. [Belastingdienst software-filing guidance](https://www.belastingdienst.nl/wps/wcm/connect/bldcontenten/belastingdienst/business/tax_return/filing_digital_tax_returns/filing-tax-returns-using-accounting-software/) distinguishes the software-submission requirements; a Dutch chart or VAT table alone does not establish compliance. No candidate is selected, installed or tested here, and no reliable implementation duration is claimed.

## Auditable closeout route

The proposed direct route is Design → ready solely for owner-requested research closeout. Planning and implementation are deliberately unperformed; final offline validation and this closeout documentation are still produced. A forced transition must record that reason and the original owner authority after independent review of the exact snapshot. It must not present skipped implementation or general application tests as completed. This snapshot performs no phase transition, push, PR submission, merge or issue closure; Co schedules the authorized lifecycle only after the matching independent verdict.

Only screened source/metadata, synthetic fixtures and public links belong in the published ref. Raw private logs, APK/JavaScript source extracts, invoices, credentials, account identifiers and private machine/source locations remain excluded from Git, workflow state and publication.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-02 | Codex (@imp designer) | Index delivered research, offline reproduction, deferred decisions and exploratory own-accounting feasibility for research-only closeout. |

| 1.1 | 2026-11-02 | Codex (@imp designer) | Record the seven-file terminal-newline-only correction and preserve historical behavioral/source-hash evidence scope. |
