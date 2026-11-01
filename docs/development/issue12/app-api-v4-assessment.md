<!-- pgmcp:v1 id=reference pv=1.0.0 pf=Q4Tx8SxSHKiKF_yz sf=WI5iXHBKVOU91bYE -->

# e-Boekhouden App API v4 assessment

**Status:** HISTORICAL CHECKPOINT WITH EXPANDED EVIDENCE — provider strategy reopened  
**Version:** 1.2  
**Last Updated:** 2026-11-01

## Expanded evidence — 2026-11-01

The findings below describe the bounded 2026-10-30 community/read checkpoint. Current [functional coverage](api-functional-coverage.md) and the [whole-client APK catalogue](apk-api-contracts.md) supersede its completeness assumptions without rewriting that historical proof. Android3.9.0's compiled default host/version is the same App-v4 family. Its broader clients declare invoice/quote/subscription/reference/hours CRUD and report operations absent from the 33-path/34-operation community capture.

In particular, `MutatiesClient.Create` declares POST `/api/v4/mutaties` with `CreateMutatieDto.afschriftRegelId` and `bestanden`, plus a source-bank-row next-data query. This is now an identified static processing candidate; pending-row consumption, matching, atomicity and retry safety are still unproved. `UpdateMutatieDto` explicitly includes `relatieId`, unlike the incomplete old captured request. Selected later archive upload/link/rename, narrow mutation edits and hours outcomes are historical runtime evidence in the [preservation inventory](toolkit-preservation.md), not blanket current server guarantees. No new account/auth/API operation occurs in this update, and no present operational authority is revived.
## Purpose

Assess the unofficial App API against attachment linking, existing-mutation editing and imported-bank-row processing, with screened conclusions from separately authorized bounded read probes.

## Scope In

Public repository metadata, README and inferred OpenAPI snapshot, plus screened bounded runtime evidence and the owner-selected interface boundary, inspected on 2026-10-30.

## Scope Out

No new authentication or financial request in this documentation update; no interception, bookkeeping writes or production implementation. Private credentials, records and locations are excluded from these published findings.

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
| Link an existing archive file to a mutation | Explicit inferred routes and example exchanges | First future REST-gap investigation accepted; no live link or upload tested |
| Retrieve a selected known mutation | Bounded live login/current-admin/filter/detail/context proof | Identity mapping established for the sample; financial-field interpretation remains limited |
| Edit an existing mutation | PUT with existing identifiers and captured success shape | Strong candidate for editing, not a guarantee for all fields/types or stable internal identity |
| Read imported bank rows | Explicit GET list and detail | Observed in inferred contract; not exercised here |
| Process or match imported bank rows | No processing route or queue-ID input found | Not established; new mutation creation is not equivalent |

The route catalogue distinguishes the repository author's retained exchanges from the separately authorized bounded read proof. Neither establishes file-write, mutation-edit or bank-processing success.

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
| POST /api/v4/mutaties/filter | One-day bounded metadata lookup succeeded; response items resolve visible number to internal ID |
| GET /mutaties/search | Published inferred path; live search variants failed route binding and are not a working lookup contract |
| GET /api/v4/mutaties/btwperregel | VAT-per-row-related read |
| GET /api/v4/grootboekrekeningen/mutaties/{mutatieId}/pickerlist | Mutation-context ledger lookup |
| PUT /api/v4/mutaties | Request contains id, mutatieNummer, factuurNummer, grootboekRekeningId/code, datum, bedrag, boekstuk, omschrijving, soort, isInclusiefBtw, termijnInDagen and mutatieRegels |

Row inputs include index, tegenRekeningId, btwCode, bedrag, btw and omschrijving. The retained success exchange preserves a displayed mutation number but returns a different internal id. This supports an editing hypothesis while warning against identity-stability assumptions. The request lacks the response's relatieId; required fields, safe omission rules, all mutation types, ledger/VAT validation, period locks, concurrency and retry semantics are not established. Sending a partial object is not proved safe. Do not generate a client from this schema and infer reliable update semantics.

### Bank rows and settlement

GET /api/v4/afschriftregels returns afschriftRegels with id, boekDatum, bedrag and omschrijving. GET /api/v4/afschriftregels/{afschriftregelId} adds importDatum and rekeningNummer. No list pagination/filter contract is established. The vendor's [iOS App Store version history](https://apps.apple.com/nl/app/e-boekhouden-nl/id1078225120) advertises management of unprocessed bank rows in the 3.3.x/3.4.0 release history. That is primary functional evidence that the app can work with this queue, not a published processing endpoint. App release versions must not be equated with API v4. These are the only afschriftregels routes in the incomplete community snapshot; their absence cannot prove that a processing API does not exist. No matching, processing, consumption or retry contract is present, and PUT mutaties has no declared afschriftregelId. additionalProperties:true does not establish that an invented queue field will work. POST /api/v4/openposten/crediteuren and /debiteuren are additional open-item reads in the inferred surface, not bank-worklist processing. Do not create an independent payment for an existing bank row as a substitute: it can duplicate bookkeeping while leaving the row pending.

### Authentication, administration and schema quality

POST /api/v4/auth/login has username/password and loginOk/token/twoFactorCodeRequired response fields. POST /api/v4/auth/renew mentions previousToken with credentials; the retained exchange failed. GET /api/v4/auth/userinfo and GET /api/v4/administraties provide identity/administration discovery. POST /api/appversion/validate is also present. The scheme is HTTP Bearer JWT, distinct from REST v1's session contract. Two-factor completion, token lifetime/revocation, choosing/binding the correct administration and read-only permissions are not adequately specified. Never assume credentials or identifiers transfer between interfaces.

A separately authorized App login, actual current-administration confirmation, explicit one-day filter query, internal-ID detail read and context checks succeeded. Credentials were stored locally in a distinct Windows Credential Manager entry; they are not interchangeable with the official REST API token. Unexpected 2FA remained a stop condition. No account identifiers or credential details are published.

Several inferred schemas omit required lists; empty arrays have unknown item shape. Renew properties contain literal strings instead of valid schema objects. Search paths omit /api/v4 despite the server being the host origin. Responses and error coverage are sparse. Captured HTTP success and permissive schemas do not establish a complete callable contract or current service support. README capture instructions were not followed; no interception or device-session extraction occurred.

### Financial interpretation and identity boundary

The live App internal ID differed from the selected visible mutation number used by official REST. This confirms a namespace distinction for that sample, not that file-link koppelId necessarily equals either value.

The owner verified the official REST sample against the actual UI. Some App summary/calculated monetary fields were inconsistent with that result, while common identity/base-row information agreed. Official REST defines row amount through inExVat and aggregate VAT totals per VAT code; the inferred App fields bedrag, btw, bedragInclusief and bedragExclusief have no comparable descriptions. The discrepancy does not prove modified bookkeeping, a particular bug or a universal App limitation. It does mean that the read object is not a validated financial-write payload and must not be round-tripped into PUT.

### Proportional next evidence and route options

OWNER ACCEPTED — 2026-10-30: official REST is the default for ordinary reads, financial interpretation and supported writes. App v4 may supplement only an actual missing REST capability; the first future target is linking an existing archive file to a mutation. Identity/mapping reads may support that task, rather than duplicating general financial retrieval. The supplement remains unofficial and capability-specific. SOAP stays excluded.

The selected read proved login/current context and a bounded identity mapping; the declared date filter worked where published search paths did not. File-target semantics and existing-file linkage still need their own bounded investigation, outcome verification and review. No file link, upload, mutation edit or bank-processing write was tested. Do not automatically switch to App after a REST authentication, validation or network error, or retry an alternate write because of such a failure. This accepted interface boundary does not authorize a write, imply a production implementation sequence or complete the Research phase. App JWT persistence/logout is not established; only process-memory use and process closure are claimed.

## Related Documents

- [Research](<research.md>)
- [Official API catalogue](<api-catalog.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.1 | 2026-10-30 | Codex (@imp researcher) | Record screened live read findings and accepted supplemental role; separate identity and monetary interpretation limits from untested writes. |
| 1.0 | 2026-10-30 | Codex (@imp researcher) | Assess pinned App API evidence and limits for files, edits and bank processing. |
| 1.2 | 2026-11-01 | Imp | Preserve old checkpoint; link broader APK contracts, source-bank-row create candidate and bounded later runtime evidence. |
