<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=WI5iXHBKVOU91bYE -->

# Consolidation validation

**Status:** REVIEW REQUESTED — native checks executed; application tests inactive  
**Version:** 1.0  
**Last Updated:** 2026-10-29

## Purpose

Record fresh evidence for mechanical source consolidation.

## Issue Number

#10

## Validation Status

PARTIAL

## Scope

Complete issue10 branch against main after final implementation dce01a3bcda50e30371c3fff9e23afccc37747de. Native checks ran; application tests remain inactive by repository policy.

## Evidence

### Branch native checks executed once after final implementation.

run_status passed. markdown_links passed/exit0, Lychee0.24.2, args --offline --cache=false --include-fragments; total744 unique449 successful368 excluded376 errors0 timeouts0 cached0. json_schema_shape and json_schema_metaschema each passed/exit0/errors[], check-jsonschema0.38.2/jsonschema4.26.0. YAML not_executed/not_applicable because no YAML changed; not a passing YAML check.

**Sources:**

**Invocation:** run_checks(scope='branch'); profile repository_review; configured arguments unchanged

### Configured test request executed without active tests.

error_code no_active_tests; selected_tests=[],results=[]. No passing tests or coverage evidence.

**Sources:**

**Invocation:** run_tests(scope='configured')

## Preservation

All52 selected files are present;48 byte-identical including28/28 deployment files. Four documents differ only in eight relative links. Issue1/2 and public-PDF baseline remain unchanged. Shared ADR/map paths remain canonical. No source branch or original issue/worktree was changed; only issue10 workflow is active and must be neutralized by submit_pr.

## Containment

No packages built, application executed, environment provisioned, private inputs processed, accounts changed or operational services altered.

## Caveats

- The branch check predates this new report; its enforced scaffold Markdown gate covers the added report without repeating the branch suite.
- External URLs are excluded by the approved offline policy; no new reachability claim.
- Historical issue7 runtime/package evidence remains inherited, not fresh clean-machine or product proof.
- Application checks/tests and automated fixes remain deferred by existing repository policy.

## Deferred Work

### Original research/design/runtime proofs remain unfinished where their own source documents say so.

Not introduced or solved by consolidation; main supplies reference material rather than a newly working or approved product. Sources and follow-up: original issues5,6,8,9 and imported documents. Co explicitly preserves their open phase/triage states.

### Application-test execution remains inactive.

Existing issue2 repository policy defers stack/test bindings. The actual configured request returned no_active_tests, never a pass. Follow-up remains with Co/issue2 when the application policy is approved.

## Related Documents

- [Import evidence](<implementation-evidence.md>)
- [Pinned source mapping](<research.md>)
- [Issue navigation](<../README.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-29 | Codex (@imp validator) | Record fresh branch-profile checks, inactive configured tests and scope limitations. |
