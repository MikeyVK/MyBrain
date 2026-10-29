<!-- pgmcp:v1 id=reference pv=1.0.0 pf=Q4Tx8SxSHKiKF_yz sf=WI5iXHBKVOU91bYE -->

# Garmin Personal API endpoint catalog

**Status:** Research candidate — owner strategy decision and independent review pending

**Version:** 1.1

**Last Updated:** 2026-10-29

## Purpose

Provide the complete public-specification endpoint inventory supporting issue #8 Research, with request boundaries, response shapes and unresolved semantics.

## Scope In

All 26 GET data paths in the observed public specification; authentication cross-reference, source pins and critical SDK differences.

## Scope Out

Live requests, account/device eligibility, implementation interfaces and guarantees not documented by Garmin.

## Sources

- [Official Swagger documentation][src-1]
- [Observed embedded specification JavaScript][src-2]
- [Official Personal API][src-3]
- [Official FAQ][src-4]
- [Pinned SDK][src-5]

[src-1]: <https://developer.garmin.com/gc-developer-program/personal/swagger-docs/>
[src-2]: <https://developer.garmin.com/component---src-pages-gc-developer-program-personal-swagger-docs-js-715115a6210d45afc282.js>
[src-3]: <https://developer.garmin.com/gc-developer-program/personal/personal-api/>
[src-4]: <https://developer.garmin.com/gc-developer-program/personal/personal-faq/>
[src-5]: <https://github.com/garmin/connect-personal-api-python/blob/ac111a0ff8e37dfbc24c616fcc27691520c7278b/pyproject.toml>

## API Reference

### Evidence and interpretation rules

Observed 2026-10-29 from Garmin's public embedded specification: OpenAPI dialect **3.0.1**, API title Garmin Connect Personal API, API version **1.0.0**, **26 paths**, all GET, **109 schemas**. The token POST is documented separately and is not a twenty-seventh data path. This is a source-inspection catalog, not an executed account/device coverage result.

| Evidence pin | Identity |
| --- | --- |
| Public Swagger JavaScript SHA-256 | `4ba5d8fcafdc877b78228285048cb67c43c5af40a4efb66f91f8032ca5861eea` |
| Decoded JSON UTF-8 SHA-256 | `1ba9d4c8ee0b6bc7e79fef21670bce435a29594801bb90231298224cdeaf3e8e` |
| Official SDK commit | `ac111a0ff8e37dfbc24c616fcc27691520c7278b` (2026-10-21) |

The JavaScript URL is content-labelled but mutable hosting remains possible; the hashes identify the observed edition. Extraction read the `wOaG` module's `JSON.parse` string, decoded its quoted literal with `ast.literal_eval`, then parsed JSON without executing JavaScript. No private account, key or live API request was used.

Servers: `https://personal.connectapi.garmin.com` and `https://personal.connectapi.garmin.cn`. Endpoint presence does not establish regional eligibility, accepted terms, device support, account access, data availability or retention. The specification has no `securitySchemes`; use the official authentication prose and pinned SDK, not an inference of anonymous access.

**Notation:** P = required path parameter; Q = query parameter, optional in the schema unless stated otherwise. Date parameters are strings `YYYY-MM-DD`; activity IDs are int64 in the API and require lossless handling. Every row is GET. JSON responses are `application/json` except the original download. “Unspecified” means no bound found in the inspected specification, not unlimited. Query dates omitted from `required` are not evidence that omission is a useful collector request: send exact scopes explicitly and retain them.

### Activity and configuration paths (7)

| Exact path | Capability and parameters/defaults | 200 schema/shape and completeness limits |
| --- | --- | --- |
| `/activity-service/activity/{activityId}` | Detailed activity summary; P activityId. | `ActivitySummaryDTO` object; summary/metadata/measurements/split summary, not full recorded samples. 400/401/403/404/500 documented. |
| `/activity-service/activity/{activityId}/workouts` | Workouts performed; P activityId. | `ActivityWorkoutDTO[]`; empty array explicitly means no workouts found for that activity. 400/401/403/404/500. |
| `/activitylist-service/activities/search/activities` | Offset search; all filters below are Q. No maximum page size/window specified. | Bare `SummarizedActivityDTO[]`; empty matching result documented. No total, snapshot, cursor or deterministic tie order promised. 400/401/403/500. |
| `/download-service/files/activity/{activityId}` | Original activity format; P activityId. | `application/x-zip-compressed`, no response schema or error table. Preserve ZIP first; no universal FIT-member guarantee or size bound. |
| `/biometric-service/heartRateZones/v2` | Zone configuration; Q generateDefaults=true. | Bare `HeartRateZonesDTO[]`; generated defaults are not measured activity. Whether generation only computes defaults or also persists state is unverified; GET alone does not prove absence of effects. Only 200 described. |
| `/userprofile-service/userprofile/settings` | Current profile settings; no parameters. | `UserSettingsDTO` object; no historical profile/version promise. |
| `/fitnessage-service/fitnessage/v2/{calendarDate}` | Fitness Age as of date; P calendarDate; Q fullHistoryScan=true. False considers preceding 28 days relative to target. | Bare `FitnessAgeDTO[]`; latest available as of target is not proof of measurement on target. Full-history scan is not an account-wide retention guarantee. |

The activity search exposes these **32 query parameters**, with units and constraints where stated:

| Parameters | Defaults, format and meaning |
| --- | --- |
| start, limit | int32; 0 and 99 respectively. Offset is zero-based; 99 is a default, not a documented maximum. |
| favorite | int32=-1; 1 favorites, 0 non-favorites, -1 no filter. |
| sortOrder, sortBy | sortOrder=desc, asc/desc case-insensitive. sortBy prose default startLocal; schema has no default. Example fields name/distance/duration. No stable tie-break promise. |
| excludeChildren | boolean=true; excludes child legs of multisport activities. Explicit false or an expressly limited scope is necessary before claiming child coverage. |
| search | Name/description text. |
| activityType, activitySubType | Parent type and child subtype keys respectively; if combined they must match. |
| eventType | Event classification key; e.g. race/training/recreation. |
| minDistance, maxDistance | Inclusive int64 meters. |
| minDuration, maxDuration | Inclusive int64 timer seconds. |
| minElevation, maxElevation | Inclusive int64 elevation gain meters. |
| startDate, endDate | Inclusive local activity start dates. No maximum interval specified. |
| upperLatitude, rightLongitude, lowerLatitude, leftLongitude | Double decimal degrees. All four required to apply box; latitude [-90,90], longitude [-180,180]. 400 description mentions maximum diagonal distance without specifying its value. |
| lowerMaxDepth, upperMaxDepth | Inclusive int64 bounds on maximum dive depth, centimeters. |
| decoDive | Boolean decompression status; omit for no filter. |
| minElapsedDuration, maxElapsedDuration | Inclusive int64 elapsed seconds including pauses. |
| minBottomTime, maxBottomTime | Inclusive int64 dive bottom seconds. |
| minAvgPower | Inclusive int64 watts. |
| excludedActivitySubType | Repeated string-array query; multiple excluded subtypes. |
| requiredField | Repeated string-array query; all listed fields must be non-null. |

### Daily wellness and sleep paths (11)

| Exact path | Capability, parameters and maximum request window | 200 schema/shape and caveats |
| --- | --- | --- |
| `/sleep-service/sleep/dailySleep` | Single sleep day; Q date. | `DailySleepDTO` object; timestamp type/prose conflict below. |
| `/sleep-service/sleep/dailySleepSummariesByDate` | Q startDate/endDate; maximum **31 days**. | Bare `DailySleepDTO[]`; no guarantee every requested day exists. |
| `/usersummary-service/stats/hydration/daily/{startDate}/{endDate}` | P startDate/endDate; maximum **31 days**. | Bare `UserDailyHydrationDTO[]`. |
| `/usersummary-service/stats/steps/daily/{startDate}/{endDate}` | P startDate/endDate; maximum **28 days**. | Bare `StepsDailyStatDTO[]`. |
| `/usersummary-service/stats/stress/daily/{startDate}/{endDate}` | P startDate/endDate; maximum **28 days**. | Bare `MultiValueWellnessChartItemDTO[]`. |
| `/usersummary-service/usersummary/daily` | Single summary; Q calendarDate. | `UserDailySummaryDto` object; distinct from V2 list envelope. |
| `/usersummary-service/v2/dailysummaries` | Q startDate/endDate; maximum **1 year**. | `ApiDocumentListUserDailySummaryV2DTO` object containing `.data: UserDailySummaryV2DTO[]`; one day still uses envelope. Calendar-year versus fixed-day arithmetic needs clarification. |
| `/wellness-service/wellness/bodyBattery/reports/daily` | Q startDate/endDate/chunks; maximum **31 days**. chunks int32, no default/bound given; controls daily intervals' minimum/maximum readings. | Bare `BodyBatteryDailyReportDTO[]`; aggregated intervals are not every underlying sample. 400/401/403/500. |
| `/wellness-service/wellness/daily/spo2acclimation/{calendarDate}` | Single day; P calendarDate. | `DailySpO2AndAcclimationDTO` object. 400/401/403/500. |
| `/wellness-service/wellness/dailyHeartRate` | Single day; Q date. | `DailyHeartRateDTO` object with descriptors/readings and nested date/timestamp objects. 400/401/403/500. |
| `/wellnessactivity-service/activity/summary/range/{fromDate}/{untilDate}` | P fromDate/untilDate, explicitly inclusive; maximum unspecified. | Bare `WellnessActivitySummaryDTO[]`; do not equate with full activity search/download coverage. 400/401/403/500. |

The SDK describes its range helpers as inclusive. The spec explicitly says inclusive for activity search, weight and wellness activity. Other window endpoints name date ranges and maxima without consistently defining edge counting. A later admission proof must check adjacent windows, DST, leap days and inclusive day counts rather than treating SDK documentation as a provider guarantee.

### HRV, weight, nutrition and cycle paths (8)

| Exact path | Capability and parameters/defaults/window | 200 schema/shape and caveats |
| --- | --- | --- |
| `/hrv-service/hrv/{calendarDate}` | Single HRV day; P calendarDate. | `HrvChartDTO` object; **204 No data** explicitly documented. Offset-free timestamps below. |
| `/hrv-service/hrv/daily/{fromDate}/{toDate}` | P fromDate/toDate; maximum unspecified. | `HrvDailySummaryDTO` object containing `.hrvSummaries: HrvSummaryDTO[]`; **204 no data** documented. |
| `/weight-service/weight/all/{startDate}/{endDate}` | P startDate/endDate, inclusive user-local dates; maximum unspecified. | Bare `DateWeightDTO[]`, all entries within range. Distinct from range aggregate. |
| `/weight-service/weight/range/{startDate}/{endDate}` | Same required inclusive local dates; Q includeAll=false. True includes all daily entries, false latest per day. Maximum unspecified. | `WeightRangeDTO`: dailyWeightSummaries, totalAverage, previousDateWeight, nextDateWeight. Previous/next may be **outside** requested interval; retain as context, never requested coverage. |
| `/goal-service/goal/user/effective/weightgoal/{startDate}/{endDate}` | P startDate/endDate; maximum and explicit inclusivity unspecified. | `UserGoalsRangeDTO` object, effective goals/ranges. 400/401/403/500. |
| `/nutrition-service/food/logs/{date}` | P date, user's local timezone; Q includeGoals=true, includeNutrition=true, includeMedia=true; mealId int64 optional. | `DailyNutritionSummaryDTO` object; media flag does not authorize recursive fetching of arbitrary response URLs. |
| `/periodichealth-service/menstrualcycle/summary/{calendarDate}` | P calendarDate. | `MenstrualCycleSummaryDTO` object. 400/401/403/500. Account/device/feature availability unverified. |
| `/periodichealth-service/menstrualcycle/dayview/{calendarDate}` | P calendarDate; Q todayDate (caller reference date), reducedResponse=false, skipbm=false, includeAnalysis=false. | `DetailedMenstrualCycleDayDTO` object; caller's todayDate and flags affect results, so date alone is not the full request identity. 400/401/403/500. |

### Cross-cutting ambiguities and SDK drift

| Boundary | Observed fact | Consequence for later evidence |
| --- | --- | --- |
| Auth | Global and China servers listed; no OpenAPI security scheme. [auth.py](https://github.com/garmin/connect-personal-api-python/blob/ac111a0ff8e37dfbc24c616fcc27691520c7278b/src/garmin_personal_api/auth.py) consumes stripped raw response text as JWT. [constants.py](https://github.com/garmin/connect-personal-api-python/blob/ac111a0ff8e37dfbc24c616fcc27691520c7278b/src/garmin_personal_api/constants.py) defines token path. | POST `/personalapitoken-service/personal-api/personal-api-key/token` with `Authorization: ApiKey <key>`; data uses `Bearer <token>`. Do not assume JSON token envelope or cross-region key portability. |
| Timestamp shapes | `HrvChartDTO` explicitly describes ISO8601 strings without offset/Z. Activity local and GMT strings lack suffix; `beginTimestamp` explicitly epoch milliseconds. | Preserve originals plus field-specific interpretation; no generic “all Garmin times are milliseconds” conversion. |
| Nested dates | `ConnectDate` and `ConnectTimestamp` are objects with `date: date-time` and `localDate: date`; heart-rate DTO references them. | Flattening into one timestamp loses calendar context. |
| Sleep conflict | `DailySleepDTO` start/end GMT/local timestamp schema says string/date-time; descriptions say “in ms”. | Unresolved contradiction; later synthetic compatibility fixtures and provider clarification, no guessed coercion. |
| Units | `DateWeightDTO.weight` explicitly kilograms. Other composition fields do not all state units; heart-rate arrays use descriptors and generic nested objects. | Do not import unofficial grams or assume sample tuple layout. Preserve field units/unknowns separately from normalized values. |
| SDK search | [client.py](https://github.com/garmin/connect-personal-api-python/blob/ac111a0ff8e37dfbc24c616fcc27691520c7278b/src/garmin_personal_api/client.py) helper defaults limit=20 versus spec=99; no excludeChildren argument on helper. | Use explicit page/filter scope; generic get can address more API options but returns parsed JSON. |
| SDK endpoint coverage | No dedicated single daily usersummary or weight /all helper; weight helper uses /range with includeAll=true. | SDK wrapper inventory is not the endpoint catalog. |
| Response fidelity | SDK get returns `response.json()`, empty content becomes None; download returns fully buffered `response.content`. | Need byte capture before decoding JSON, status-aware no-data handling and bounded streaming; SDK values cannot reconstruct original serialization. |
| Operational guarantees | No documented numeric quota, 429/Retry-After contract, modifiedSince, ETag, webhook, request-ID header, stable pagination, complete-history horizon, retention or deletion/revision feed found in this edition. | All remain unknown; bound retries/history requests and distinguish missing data from deletion. Unlisted errors may still occur. |

Pinned SDK source hashes (UTF-8 source bytes as downloaded; paths relative to repository):

| File | SHA-256 |
| --- | --- |
| src/garmin_personal_api/auth.py | `cd19c94497206c248fe2ba95d1613f8ef8d69dbb53d0fb2b5c4fa20526ac074f` |
| src/garmin_personal_api/client.py | `87594c35a073448df1644262eeb34a945a668e76b3f50b8a340b2243f523585a` |
| src/garmin_personal_api/constants.py | `41082139e0fb9f5fdf44e98050963e661887d9e2487c5c170c9b43606bb2eded` |
| src/garmin_personal_api/api_keys.py | `1ae6088bbcf6bbb3385db23d0cc01fe333e3b16689d74caaa200de40fa62cdcb` |
| src/garmin_personal_api/_credentials.py | `282d1fc2d998eb2b1027c738ce77ef5815beffd158dbc06312e0544704ad1fbe` |
| src/garmin_personal_api/downloads.py | `22bc4d8fa2af9a5657ae451b01e4c2681c145371a7a2c6fe5a0f24b0432a0ecf` |
| pyproject.toml | `daf2b4c8a25afc392d1e839ba47f98ff0723aa143e1dc43e5ec0578a05cce534` |

No live access, benchmarks or synthetic application scenarios were executed. Native offline documentation-check evidence belongs to the companion research document; it does not verify external URL reachability.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-29 | Codex (@imp researcher) | Catalog all 26 public GET paths, exact parameter/shape boundaries, source hashes and unresolved SDK/specification semantics. |
| 1.1 | 2026-10-29 | Codex (@imp researcher) | Make the unresolved effect of generating heart-rate-zone defaults explicit without asserting server-side mutation. |
