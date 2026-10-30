<!-- pgmcp:v1 id=reference pv=1.0.0 pf=Q4Tx8SxSHKiKF_yz sf=WI5iXHBKVOU91bYE -->

# e-Boekhouden App API v4 assessment

**Status:** RESEARCH FINDINGS — unofficial evidence; no live proof  
**Version:** 1.0  
**Last Updated:** 2026-10-30

## Purpose

Assess the unofficial App API against attachment linking, existing-mutation editing and imported-bank-row processing, without account access.

## Scope In

Public repository metadata, README and inferred OpenAPI snapshot, inspected 2026-10-30.

## Scope Out

No authentication, financial requests, interception, implementation, live changes or strategy approval.

## Sources

- [Pinned README][src-1]
- [Pinned inferred OpenAPI][src-2]
- [Repository metadata][src-3]

[src-1]: <https://github.com/kozmoz/e-boekhouden-APP-API-v4/blob/6ca849003ed196ca10877d8854644e9c38cf3145/README.md>
[src-2]: <https://github.com/kozmoz/e-boekhouden-APP-API-v4/blob/6ca849003ed196ca10877d8854644e9c38cf3145/swagger.openapi.json>
[src-3]: <https://api.github.com/repos/kozmoz/e-boekhouden-APP-API-v4>

## API Reference

### Evidence and licensing boundary

This is an unofficial reconstruction of iPhone-app traffic, not a vendor-supported API contract. The inspected head is 6ca849003ed196ca10877d8854644e9c38cf3145 (2026-05-22); the repository was created that day, shows three commits and no release, and GitHub reports no license. The two-file tree contains no LICENSE. Public visibility is not permission to redistribute or reuse an implementation under an open-source license. Maintenance and continued compatibility are unproved. README names a different specification filename; the actual file is swagger.openapi.json. Its 103837-byte snapshot has SHA-256 cd9396bf90ffbf9a2241ed7741bda629f34f3903eba0991ac1719ba6697692a6, OpenAPI 3.0.3 and version 4.0-inferred. It describes 34 operations. Source examples are not fully sanitized despite the README claim; no example values, filenames, financial amounts or third-party identifiers are reproduced here.

### Capability assessment

| Requested action | Evidence grade | Conclusion |
| --- | --- | --- |
| Upload and link a file to a mutation | Explicit inferred routes and example exchanges | Plausible, considerably stronger than REST v1; target-kind and ID mapping still require proof |
| Edit an existing mutation | PUT with existing identifiers and captured success shape | Strong candidate for editing, not a guarantee for all fields/types or stable internal identity |
| Read imported bank rows | Explicit GET list and detail | Observed in inferred contract; not exercised here |
| Process or match imported bank rows | No processing route or queue-ID input found | Not established; new mutation creation is not equivalent |

“Observed” refers only to evidence retained by the repository author. No current account/runtime success is claimed.

### Files: relevant route inventory

| Method and path | Contract evidence and limitations |
| --- | --- |
| GET /api/v4/bestanden; GET /api/v4/bestanden/{directoryId} | Directory/file browsing |
| GET /api/v4/bestanden/bestand/{fileId}; GET /api/v4/bestanden/download/{fileId} | File/detail or download access; response completeness varies |
| GET /bestanden/search | search query; prefix differs from other routes and README base URL |
| POST /api/v4/bestanden/upload | fileName, data (base64 per README), directoryId, scan; success shape includes saved, scanned and file.id |
| POST /api/v4/bestanden/koppel | fileId, soort, koppelId; response includes fileId and koppelId |
| POST /api/v4/bestanden/gekoppeld | soort, koppelId; response files array has no informative item schema |
| DELETE /api/v4/bestanden/koppel/{linkId} | Removes a link; boolean response; how to obtain the exact link ID remains unclear |
| POST /api/v4/bestanden/directory | Directory creation |
| PUT /api/v4/bestanden; POST /api/v4/bestanden/bulkMove | Additional archive operations; not required to establish linking |
| DELETE /api/v4/bestanden/bestand/{fileId} | File deletion, distinct from unlinking; outside proposed proof scope |

One captured soort value is not a universal target-type definition. koppelId is not proved equal to REST v1 mutationId, the App internal id or displayed mutatieNummer. Linked-file retrieval must be matched to a known target before writes can be considered. Archive-mail delivery is distinct from Scan & Herken and is not itself evidence of automatic mutation linkage. No personal archive address is retained.

### Mutation editing: relevant route inventory

| Method and path | Evidence |
| --- | --- |
| GET /api/v4/mutaties/{mutatieId} | Header and detailed mutatieRegels response |
| POST /api/v4/mutaties/filter | Mutation lookup/filtering |
| GET /mutaties/search | search and mutatienummer query parameters; unresolved prefix inconsistency |
| GET /api/v4/mutaties/btwperregel | VAT-per-row-related read |
| GET /api/v4/grootboekrekeningen/mutaties/{mutatieId}/pickerlist | Mutation-context ledger lookup |
| PUT /api/v4/mutaties | Request contains id, mutatieNummer, factuurNummer, grootboekRekeningId/code, datum, bedrag, boekstuk, omschrijving, soort, isInclusiefBtw, termijnInDagen and mutatieRegels |

Row inputs include index, tegenRekeningId, btwCode, bedrag, btw and omschrijving. The retained success exchange preserves a displayed mutation number but returns a different internal id. This supports an editing hypothesis while warning against identity-stability assumptions. The request lacks the response's relatieId; required fields, safe omission rules, all mutation types, ledger/VAT validation, period locks, concurrency and retry semantics are not established. Sending a partial object is not proved safe. Do not generate a client from this schema and infer reliable update semantics.

### Bank rows and settlement

GET /api/v4/afschriftregels returns afschriftRegels with id, boekDatum, bedrag and omschrijving. GET /api/v4/afschriftregels/{afschriftregelId} adds importDatum and rekeningNummer. No list pagination/filter contract is established. The vendor's [iOS App Store version history](https://apps.apple.com/nl/app/e-boekhouden-nl/id1078225120) advertises management of unprocessed bank rows in the 3.3.x/3.4.0 release history. That is primary functional evidence that the app can work with this queue, not a published processing endpoint. App release versions must not be equated with API v4. These are the only afschriftregels routes in the incomplete community snapshot; their absence cannot prove that a processing API does not exist. No matching, processing, consumption or retry contract is present, and PUT mutaties has no declared afschriftregelId. additionalProperties:true does not establish that an invented queue field will work. POST /api/v4/openposten/crediteuren and /debiteuren are additional open-item reads in the inferred surface, not bank-worklist processing. Do not create an independent payment for an existing bank row as a substitute: it can duplicate bookkeeping while leaving the row pending.

### Authentication, administration and schema quality

POST /api/v4/auth/login has username/password and loginOk/token/twoFactorCodeRequired response fields. POST /api/v4/auth/renew mentions previousToken with credentials; the retained exchange failed. GET /api/v4/auth/userinfo and GET /api/v4/administraties provide identity/administration discovery. POST /api/appversion/validate is also present. The scheme is HTTP Bearer JWT, distinct from REST v1's session contract. Two-factor completion, token lifetime/revocation, choosing/binding the correct administration and read-only permissions are not adequately specified. Never assume credentials or identifiers transfer between interfaces.

Several inferred schemas omit required lists; empty arrays have unknown item shape. Renew properties contain literal strings instead of valid schema objects. Search paths omit /api/v4 despite the server being the host origin. Responses and error coverage are sparse. Captured HTTP success and permissive schemas do not establish a complete callable contract or current service support. README capture instructions were not followed; no interception or device-session extraction occurred.

### Proportional next evidence and route options

The shortest plausible supported route remains official REST v1 for documented creation/reads plus the existing UI for unproved actions. The App interface could narrow attachment and editing gaps, but requires explicit owner acceptance of an unsupported interface and further evidence; it does not currently remove the bank-processing gap. SOAP is excluded by owner and is not a fallback.

Before any financial-write proposal, a separately authorized read-only proof should establish authentication/2FA without leaking credentials, correct administration, a known mutation's App/REST/display identifiers, linked-file target semantics, actual search URL and bank-row visibility. Such a proof cannot prove write semantics; any subsequent synthetic write test would need separate scope and rollback/reconciliation evidence. No account requests are authorized or performed by this research. No Approved Strategy, implementation sequence or Research phase exit is implied.

## Related Documents

- [Research](<research.md>)
- [Official API catalogue](<api-catalog.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-30 | Codex (@imp researcher) | Assess pinned App API evidence and limits for files, edits and bank processing. |
