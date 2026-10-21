<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Issue 2 implementation evidence

**Status:** IMPLEMENTATION EVIDENCE — review pending  
**Version:** 1.0  
**Last Updated:** 2026-10-21

## Purpose

Record focused native verification and persistence facts for the owner-approved quality tooling change.

## Summary

These are implementation observations, not independent QA approval. Branch-wide checks and the configured-scope workflow test invocation remain for Validation. No application suite or automated fixes were executed.

## Configuration and native identity

The three local overrides checks.yaml, tests.yaml and fixes.yaml were compared as exact text with their [portable sources](../../../setup/quality/checks.yaml); all matched. Restart plus get_work_context succeeded after deployment. The rules resource reported default_profile=repository_review and python_tests active=false. Packaged defaults and server code were not changed.

| Native adapter | Observed identity during selected analysis |
| --- | --- |
| markdown_links | Lychee 0.24.2; adapter 2.0.0; configured --offline --cache=false --include-fragments. |
| yaml_configuration, json_schema_shape, json_schema_metaschema | check-jsonschema 0.38.2, orjson 3.13.0, ruamel.yaml 0.18.16, jsonschema 4.26.0. |

The official Lychee Windows archive SHA-256 matched 32975d1493ee1a975d6bb41e4fb56fe419cb442ded628bb772ba2e614acfacad before installation. The first parser incorrectly assumed hash-first checksum formatting and stopped; inspection of the certutil-style checksum and official release asset digest resolved the parsing issue before any executable was installed.

Before provisioning, run_checks(scope="targets", targets=[".pgmcp/config/checks.yaml"], checks=["yaml_configuration"]) returned run_status=incomplete and unavailable/dependency_unavailable. The same selection returned passed after provisioning. This was native inability, not a completed negative check.

After provisioning, run_checks(scope="targets", targets=["README.md","AGENTS.md"], checks=["markdown_links"]) returned passed with native exit 0 and the configured offline arguments. External URLs were excluded as intended.

## Synthetic fixture contract

All paths in the verification table are workspace-relative. Fixtures are deliberately disposable, public-safe and ignored under tmp/issue2-quality/. They are not application tests.

For generic_doc scaffolds, each request uses target_path="tmp/issue2-quality", force_target=true, title="Disposable issue 2 link fixture", purpose="Exercise PGMCP validation with synthetic local links.", one section with heading="Target" and content="Synthetic local fragment target.", and document_metadata status="DISPOSABLE" with revision 1.0 dated 2026-10-21 authored by @imp implementer. The table gives each file_name, validation mode and exact summary. The valid summary is [Repository agreements](../../../README.md#working-agreements) in the rendered fixture via ../../README.md#working-agreements, plus a self-link to #target.

The YAML fixture starts with data={"synthetic":true} and header_comment="Disposable synthetic issue 2 fixture." Schema S is:

```json
{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","properties":{"synthetic":{"type":"boolean"}}}
```

For safe edits, the table records the exact operation payload. Native check requests omit caller args and use the effective configured arguments in [checks.yaml](../../../setup/quality/checks.yaml).

## Observed focused verification

| Observation | Tool | Exact selection / content difference | Observed result |
| --- | --- | --- | --- |
| valid markdown scaffold enforce | `scaffold_artifact` | `generic_doc; tmp/issue2-quality/valid.md; enforce; summary="[Repository agreements](../../README.md#working-agreements) and [Target](#target)."` | written=true; validation=passed; markdown_links: passed |
| missing path scaffold enforce | `scaffold_artifact` | `generic_doc; tmp/issue2-quality/blocked-path.md; enforce; summary="[Missing](./missing.md)"` | written=false; validation=failed; error=validation_blocked; markdown_links: failed |
| missing fragment scaffold enforce | `scaffold_artifact` | `generic_doc; tmp/issue2-quality/blocked-fragment.md; enforce; summary="[Missing](#nonexistent-heading)"` | written=false; validation=failed; error=validation_blocked; markdown_links: failed |
| invalid markdown scaffold report | `scaffold_artifact` | `generic_doc; tmp/issue2-quality/report-invalid.md; report; summary="[Missing](./missing.md)"` | written=true; validation=failed; markdown_links: failed |
| missing fragment edit enforce | `safe_edit_file` | `tmp/issue2-quality/valid.md; enforce; {"op":"replace","target_content":"[Target](#target)","replacement":"[Target](#nonexistent-heading)"}` | written=false; validation=failed; error=validation_blocked; markdown_links: failed |
| missing fragment edit report | `safe_edit_file` | `tmp/issue2-quality/valid.md; report; {"op":"replace","target_content":"[Target](#target)","replacement":"[Target](#nonexistent-heading)"}` | written=true; validation=failed; markdown_links: failed |
| native markdown negative | `run_checks` | `{"scope":"targets","targets":["tmp/issue2-quality/valid.md","tmp/issue2-quality/report-invalid.md"],"checks":["markdown_links"]}` | run=failed; markdown_links: failed |
| repair fragment edit enforce | `safe_edit_file` | `tmp/issue2-quality/valid.md; enforce; {"op":"replace","target_content":"[Target](#nonexistent-heading)","replacement":"[Target](#target)"}` | written=true; validation=passed; markdown_links: passed |
| mixed unresolved batch | `run_checks` | `{"scope":"targets","targets":["tmp/issue2-quality/valid.md"],"checks":["markdown_links","python_lint"]}` | run=incomplete; error=configuration_choice_required; markdown_links: not_executed (not_started); python_lint: not_executed (configuration_choice_required) |
| inactive focused tests | `run_tests` | `{"scope":"targets","targets":["tmp/issue2-quality/valid.md"],"tests":["python_tests"]}` | error=configuration_choice_required; python_tests: not_executed (configuration_choice_required) |
| inactive default focused tests | `run_tests` | `{"scope":"targets","targets":["tmp/issue2-quality/valid.md"]}` | error=no_active_tests |
| yaml scaffold positive | `scaffold_artifact` | `yaml_configuration; tmp/issue2-quality/fixture.yaml; enforce; data={"synthetic":true}` | written=true; validation=passed; yaml_configuration: passed |
| yaml list-root report | `safe_edit_file` | `tmp/issue2-quality/fixture.yaml; report; {"op":"rewrite","content":"- synthetic\n"}` | written=true; validation=failed; yaml_configuration: failed |
| yaml native negative | `run_checks` | `{"scope":"targets","targets":["tmp/issue2-quality/fixture.yaml"],"checks":["yaml_configuration"]}` | run=failed; yaml_configuration: failed |
| schema scaffold positive | `scaffold_artifact` | `json_schema; tmp/issue2-quality/fixture.schema.json; enforce; schema=S` | written=true; validation=passed; json_schema_shape: passed; json_schema_metaschema: passed |
| schema invalid metaschema report | `safe_edit_file` | `tmp/issue2-quality/fixture.schema.json; report; {"op":"replace","target_content":"\"type\": \"boolean\"","replacement":"\"type\": \"definitely-not-a-json-schema-type\""}` | written=true; validation=failed; json_schema_shape: passed; json_schema_metaschema: failed |
| schema native negative | `run_checks` | `{"scope":"targets","targets":["tmp/issue2-quality/fixture.schema.json"],"checks":["json_schema_shape","json_schema_metaschema"]}` | run=failed; json_schema_shape: passed; json_schema_metaschema: failed |

Filesystem observations confirmed valid.md and report-invalid.md existed, while blocked-path.md and blocked-fragment.md did not. Reading valid.md before and after the rejected enforce edit showed identical content. The later report edit persisted the broken fragment, native analysis failed, and the enforce repair passed.

YAML's list-root fixture failed the object-root requirement. The schema fixture's invalid type preserved a valid dialect envelope: json_schema_shape passed while json_schema_metaschema failed. Those are separate checks with separate native outcomes.

In the mixed unresolved check batch, markdown_links was not_started and python_lint was configuration_choice_required, with no adapter/native invocation. Explicitly selecting inactive python_tests still encountered its unresolved choice; omitting the explicit test selection returned no_active_tests with no result rows. Neither result constitutes passing test evidence.

## Fixes and scope limits

apply_fixes was not called. The owner-approved policy defers automatic fixes, so no fix prerequisites or application tests were provisioned. The fixture experiments prove the selected documentation/configuration boundaries only. They do not establish application behavior, external URL availability, remote protection, independent QA approval or full branch validation.

## Final file checks and cleanup

Final focused checks used configured arguments and passed:

- run_checks(scope="targets", targets=["README.md","AGENTS.md",".agents/skills/pgmcp-co/SKILL.md",".agents/skills/pgmcp-imp/SKILL.md",".agents/skills/pgmcp-qa/SKILL.md","docs/development/issue2/research.md","docs/development/issue2/implementation-evidence.md","setup/quality/README.md"], checks=["markdown_links"]): passed, Lychee 0.24.2.
- run_checks(scope="targets", targets=["setup/quality/checks.yaml","setup/quality/tests.yaml","setup/quality/fixes.yaml","setup/quality/dependencies.yaml"], checks=["yaml_configuration"]): passed, check-jsonschema 0.38.2 and its declared prerequisites.

The evidence update itself is checked by safe_edit_file(validation="enforce") before persistence. No full-suite or branch-wide run was performed in Implementation; those belong to Validation. The three portable overrides remained exact text matches to their deployed local copies.

The complete contents of new configuration/setup/evidence files and the tracked README/instruction/state diff were reviewed for scope and unsupported claims. README, AGENTS and all three role skill entrypoints now reference the current repository policy. Shared server protocols and historical Research were reviewed as context, not rewritten to imply later quality approval.

The resolved cleanup target was verified as the exact workspace tmp/issue2-quality directory before recursive removal. Filesystem inspection confirmed that directory no longer existed. Only the intended public-safe source/documentation changes and branch-local workflow state are included in the implementation commit. Application tests, automatic fixes, native Commitlint and external URL checks remain explicitly deferred with revisit triggers in the maintained setup guide.

## Related Documents

- [Approved Research](<research.md>)
- [Portable checks](<../../../setup/quality/checks.yaml>)
- [Native pins](<../../../setup/quality/dependencies.yaml>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-21 | @imp implementer | Record deployed binding identity and disposable positive, negative, unavailable and unexecuted observations. |
