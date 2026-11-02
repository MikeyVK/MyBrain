<!-- pgmcp:v1 id=issue pv=1.0.0 pf=C7ZyrWd13VGRh7Gy sf=WI5iXHBKVOU91bYE -->

## Unpublished issue proposal

- Proposed title: Decide MyBrain accounting scope, provider route and ledger ownership
- Type: feature
- Priority: medium
- Scope: architecture
- Parent: none
- Originating reference: #12

## Problem

Decide the accounting scope, authoritative ledger and provider route before resuming MyBrain accounting implementation. This is one unpublished follow-up issue draft, not an approved strategy change or an implementation assignment.

## Summary

Issue 12 preserves useful source research, a default-disabled offline-tested helper toolkit and an unimplemented App-only MCP concept. Full coverage of the 57 functional groups and 23 configuration feature types through App API v4 is unproved. The separate web JSON family supplies additional contract evidence, while an exploratory MyBrain accounting alternative remains undecided.

## Expected Behavior

A reviewed decision records the required functional subset and acceptance criteria; compares keeping the admitted App-only subset, further evidence for a uniform web route or deliberate App+web composition, and a separately scoped MyBrain accounting module using an existing or own ledger; and obtains the owner's route/kernel decision before new Design or implementation. Any accounting module must identify one canonical deterministic ledger, its domain API and MyBrain's source/history boundary. Resolve Dutch VAT/ICP and electronic filing scope, bankfeed versus file import, migration reconciliation and backup/restore proof separately. Only after strategy and Design review should an initialized issue plan implementation and synthetic end-to-end acceptance; no current full-coverage or effort estimate is implied.

## Actual Behavior

The owner-selected APK-backed App-only endpoint baseline remains in the retained Design, qualified by the web-gap overlay. It has no implemented MCP package, installed SDK handshake or production acceptance. Existing toolkit tests cover historical helper contracts, not that server or complete accounting behavior. MyBrain storage remains designed rather than fully implemented.

## Context

Deferred work only. Tryton, LedgerSMB and ERPNext are exploratory reuse candidates, not selected dependencies. Do not start account/credential access, data migration, live filing, bankfeeds or financial writes from this draft. Preserve the screened-only publication boundary and require separately authorized evidence for any future live operation.

## Related Documents

- [Research and strategy chronology][related-1]
- [Current App-only concept design][related-2]
- [Functional coverage matrix][related-3]
- [Web-backend gap evidence][related-4]
- [Preserved toolkit][related-5]

[related-1]: <research.md>
[related-2]: <design.md>
[related-3]: <api-functional-coverage.md>
[related-4]: <web-backend-gap-research.md>
[related-5]: <../../../tools/eboekhouden/README.md>
