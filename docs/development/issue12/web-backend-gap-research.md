<!-- pgmcp:v1 id=reference pv=1.0.0 pf=Q4Tx8SxSHKiKF_yz sf=WI5iXHBKVOU91bYE -->

# Web-backend gap evidence and App-v4 completeness

**Status:** READ-ONLY WEB OBSERVATION + STATIC CONTRACT RESEARCH — NO ADMINISTRATIVE WRITES  
**Version:** 1.0  
**Last Updated:** 2026-11-01

## Result and strategy boundary

Full coverage of the inventoried web functions through App API v4 is **not positively established**. The inspected APK has broad App-v4 contracts, but specific gaps now have concrete contracts in a different web JSON interface. Finding such a web route does not prove that an undocumented App equivalent cannot exist. It does show why calling the current App-only catalogue complete would exceed the evidence.

The owner-accepted [App-only endpoint design](design.md) remains the chosen baseline, not permission to silently add web calls. Its completeness/admission boundary must include this report. No mixed route, uniform web replacement, missing financial calculation or native-UI fallback is selected here. These are research consequences requiring a subsequent strategy decision if complete web-function coverage is mandatory.

Three questions remain distinct:

| Question | Evidence-based answer |
| --- | --- |
| Can the evidenced mobile core use one App-v4 family? | Yes at static contract level; APK Production binding remains as documented in [K01](apk-api-contracts.md). This is not current runtime proof. |
| Is that one family proven to cover all 57 web groups and all 23 configuration feature types? | No. Web-only evidenced operations below remain absent from the bounded inspected App catalogues. Some other functions still lack a complete contract in either inspected source. |
| Can one MCP surface technically dispatch to several provider interfaces? | Architecturally possible, but not an accepted route change or proof of complete coverage. Shared authentication cannot be assumed across the distinct interfaces. |

## Evidence method and reproducibility

On 2026-11-01 the researcher downloaded nine exact browser-observed public JavaScript URLs with ordinary unauthenticated HTTPS GET, no cookies, headers carrying credentials or browser-state extraction. Each returned HTTP200 with a JavaScript content type. The main bundle explicitly declares the administration lazy import `./chunk-IXq3f3Xc.js`; that one relevant additional public chunk was downloaded under the same boundary. The downloaded sources were not locally executed; the ordinary web application did run in the coordinating researcher's authorized browser.

An initial sandbox socket refusal preceded successful authorized public downloads; it was not a provider response. A costly local text-search process was cancelled and replaced by bounded offset/literal extraction. Neither event involved an accounting request. All raw proprietary bundles and source-context extracts remain private, outside Git. Only concise interface metadata is reproduced.

The table identifies the downloaded UTF-8 text bytes. Offsets below are zero-based .NET string character offsets in that exact text, not line numbers or server revisions. Minification/build changes invalidate them.

| Source ID | Public asset basename | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| W01 | main-5VUGM46G.js | 925752 | A3973E5C668DCC0E4C305DA8FA50053871B7CC05B7BDF8631797CFACE1D47EA7 |
| W02 | chunk-OlmsPAN-.js | 749408 | 688112123990B377F63A22E18A6A893711CEA14A369932139DFE8A21121F2668 |
| W03 | chunk-IXq3f3Xc.js | 937704 | 83B7D0295388B65B33E04B03F138C5C51181F37AB6E7524C4168664A374FB1DB |
| W04 | chunk-C6Ihk1c2.js | 1111158 | BEC41D902B6DE970BF86AAE86A1293386C8593D431F60B4AB926B1FCB30B158E |
| W05 | chunk-Cc5wE70L.js | 2699 | 7A7E77E5480A3CBA9DD1FA80E9C175CFEF1996CD7B16590F28279B431C24718D |
| W06 | chunk-p3xIjgc-.js | 184457 | 8350A2018C871CB2308C1410D61369C26D7C8A4E98E3D26B9FB4E6A0FF8BACFE |
| W07 | chunk-D37BXNTD.js | 900 | 0DBF7A163C8B3AE8D4CB523969DEBE3F9DD57A0094A549931ED3E89521C30F9B |
| W08 | chunk-BDBv219g.js | 948 | BFE5788C76C144EF4428AE31FECF895E3D9F80DE9CA517F5BF3EC1B38DD05FD7 |
| W09 | chunk-B3XnnqJ5.js | 316 | 57B10EBFA57DFC94269A040D89F9DF61DCB65CE1B4DCAABBC16898615B3F9A7E |
| W10 | chunk-DlILOmTf.js | 46857 | E48F6708C682DB37664D43C61BE254CA204EA9B0D558C828E6B9C554AE6B9EB7 |

All assets use the origin `https://secure20.e-boekhouden.nl/`. W01/W02/W03/W04 carry the principal evidence used here; downloading a source is not evidence that every operation it contains was traced.

Private metadata identities: source-index SHA256 `9625FAC016C1B792E082304D0ACC63A74BF027EE43A57A97F0D5C078EEA9D8D2`; all-route-source-extract SHA256 `608856C041179FA862EDCF016B0851DF49E52843EDBB6D7C918BCE9A8B4A73D5`. These are evidence fingerprints, not published raw-source attachments or executable plans.

## Interface families and source binding

W01@27320 configures the browser environment template as `https://secure20.[EbDomein]/v1/api`, alongside a legacy secure-host family. W04@200019 resolves the current host/domain and exposes `getApiUrl()` and the `apiUrl` getter. W01@9198xx explicitly lazy-loads W03 for administration and W02 for bookkeeping.

| Interface | Meaning | Important boundary |
| --- | --- | --- |
| Official integration REST | `api.e-boekhouden.nl/v1` | Historical comparison source; not the web JSON API merely because both contain v1. |
| App API | `appapi.e-boekhouden.nl/api/v4` | APK-backed accepted design route; not shown to serve the missing web routes below. |
| Web JSON | browser host `/v1/api/` | Angular service/form contracts investigated here; authentication/support/lifecycle differs and is not admitted for new execution. |
| Legacy web | secure-host ASP/frame/navigation URLs | A navigation link, export form or frame route is not automatically a JSON endpoint. |

In the following tables every relative route has **web JSON prefix /v1/api/**. Case and query parameter spelling follow the source. GET is not a guarantee of query semantics: callers expose some side-effecting GET operations. No direct authenticated endpoint probe was made; ordinary authorized browser navigation produced the reads separately listed below. secure20 is the observed host, not a universal fixed host for all accounts: W04 also branches for secure21/22 and domain/environment replacement.

W01@28300 generic service maps get/getAll/getById to GET, insert to POST, update to PUT, delete to DELETE and bulkDelete to POST. Such expansion is used below only where a concrete controller instance and the corresponding method call were inspected. Grid and file-download wrappers are labelled as wrappers where the complete inner transport was not traced; no verb is guessed from their name.

## Missing-function contracts found in the web source

| Evidence / inventory | Concrete route and method evidence | Request/form or result evidence | App-v4 comparison / remaining boundary |
| --- | --- | --- | --- |
| WG01 Assets: BK010 / BE006 | W03@473419 asset service: GET `vasteactiva/{id}`, POST `vasteactiva`, PUT `vasteactiva?recalc={boolean}`, DELETE `vasteactiva/{id}`. W03@156591/156989 grid/export wrappers. W03@157737 POST `vasteactiva/boeken`. | Asset body projected at W03@489xxx: group, description, acquisition date/value, residual value, years, monthly/yearly booking, asset/depreciation ledger references, depreciation start, opening book value, advanced flag. Edit forwards recalc separately. Booking caller reports depreciation entries; this is a mutation, not report retrieval. | No corresponding asset/depreciation contract in the inspected APK/community App catalogues. Backend validation, response shapes and atomicity not established. |
| WG02 Asset groups/schedules: BE006 | W03@136373 concrete `vasteactivagroep` generic-service instance with insert/update/delete calls; GET/POST/PUT root and DELETE detail. `vasteactivamutatie/gridtable/{assetId}` and export wrapper W03@148305/148639; concrete `vasteactivamutatie` service W03@146xxx. | Group fields name, years and asset/depreciation ledger IDs. Asset form requires a description of at most50 characters; source checks whole years and residual-value constraints. These are observed web-client constraints, not a new local accounting policy or universal vendor limit. | App counterparts not established. Full schedule mutation contract remains incomplete; do not infer all CRUD from a generic class alone. |
| WG03 Asset report: BK010 | W02@249189 grid wrapper `overzicht/vasteactiva`; period parameters are constructed by the report. | Header/result field names distinguish acquisition value, depreciation, book value and period boundaries. | Native report route exists; no local reconstruction or proven App parity. |
| WG04 VAT periods/history: BK012/BK014 | W02@8188 history grid wrapper `aangifte/gridtable`, @8460 export wrapper `aangifte/export`; GET `aangifte/{id}/andersbetaald` @8951, GET `aangifte/pay/{id}` @9537, payment-status grid wrapper @9970. | Caller contexts distinguish history, marking otherwise paid and starting a payment flow. The latter two are **not safe reads** solely because GET is used. | No filing/history/payment counterpart established in inspected App catalogues. Browser observation of oldest/last-period URLs alone does not establish their method/body contract. |
| WG05 VAT calculation/processing/sending: BK012 | W02@583432 GET `btw-aangifte/aangifte` with constructed period query; @587710 POST `btw-aangifte/verwerk`; @588440 POST `btw-aangifte/createandsend`. | UI distinguishes provider calculation, bookkeeping processing and submission confirmation; processing observes returned mutation identifiers. Current form/rubric fields are forwarded. | These are distinct provider effects; no server-side reimplementation or App equivalent established. No submission was performed. |
| WG06 ICP: BK013 | W02@172160 GET `IcpOpgave/nextperiod`; GET `icpopgave/{year}/{periodType}/{periodId}`, GET `icpopgave/{id}`, PUT `icpopgave` @209675. GET `icpopgave/{year}/{periodType}/{periodId}/cansend` and **GET `icpopgave/dosend/{year}/{periodType}/{periodId}`** @210283. | dosend is called only after a submit confirmation, and its result is presented as sent. Separate line GET/POST/PUT `icpopgave/regels` and DELETE detail appear @180920–189234. | Definite static submission effect despite GET. No App ICP contract established; no endpoint request or filing test. |
| WG07 Bank/import rules: BK017 | W02@130541 GET `importregel/{id}`; @135220 POST and @135368 PUT `importregel`; @142199 DELETE detail; @142534 POST `ImportRegel/bulk/delete`; grid @143590. | Source form maps description criteria, direction, amount bounds, mutation kind, VAT code, ledger, optional cost centre and active state. List bulk-delete handles partial deleted count explicitly. | Existing App bank-row entry candidates do not prove automatic-rule management. No rule changed; response/error contract incomplete. |
| WG08 Pending import processing: BK004 | W02@104814 service GET `import/countImport`, DELETE `import/{id}`, POST `import/bulk/delete`, GET `import/opmerking/{id}`, PUT `import/opmerking`; grid/export @117082/118014. POST `import/verwerk` @118362; POST `import/bulk/wegboeken` @319296. | Reprocess list action submits absent body; post-import paths submit explicit importIds and observe countMutatie/countErrors. Write-off request includes ids, mutation kind, VAT code, ledger and optional cost centre; response updatedIds/errorMessages can be partial. | APK create-with-afschriftRegelId remains an App candidate, not equivalent proof of reprocess-all, rules, export or atomic queue consumption. |
| WG09 File imports: BK018 / BE005 / FA013 / RE003 | W04@808261/812781/814307 generic controller wizard `{controller}/importstep1`, `ImportStep2`, `ImportStep3`; W02 post-once `importfile/import` followed by `import/verwerk`. | Import workflow has staging/mapping/duplicate options and may perform a second provider mutation for processing. Generic wizard does not alone establish every controller specialization. | No complete App CSV/XLS/XLSX wizard equivalent; no file uploaded or import executed. Do not replace with locally decided booking logic. |
| WG10 Reports/exports: BK005–007/BK011 / BE009 | W02@16422/17099 liquidity grid/export; @60596 ledger report route. W03@13138 download `exportxaf/` with periodStart/periodEnd/periode/versie. @666350 builds `rapportagesoftware/export/{format}`, `exportxaf`, `rgscode/foexport/{year}`, `rgscode/rgsexport/{year}`. | Source separates year/period and export-format parameters, optional RGS validation and provider-produced downloads. File-service wrapper is traced at caller level; complete download transport/format contracts remain to admit. | App balance/P&L/ledger DTOs do not prove liquidity, columns, auditfile or software-export parity. No export created. |
| WG11 Templates: BE007 | W03@319228 invoice-template grid; @320880 download detail; invoice editor URL @502311 and language read @499874; quote editor/download @554709/543480; reminder download @562788; email detail GET `EmailSjabloonAb/{id}` @518113. | Editing/layout output is distinct from picker/details. Editor navigation is not proof of a standalone save API; source service save bindings need completion. | App email-template detail does not prove invoice/quote/reminder layout CRUD. No template changed or copied. |
| WG12 Configuration: BE003 and CFG crosswalk | W01@38266 GET `setting/{key}?acc={bool}`; POST `setting/settings?acc={bool}` for selected reads; PUT `setting?acc={bool}` and PUT `setting/settings?acc={bool}` for updates; GET `instellinggroep?forAcc={bool}`, GET `instelling?forAcc={bool}&ids=...`. | Concrete service distinguishes selected/multiple reads, setters and group/definition lists. Presence of a generic setter does not prove writable rights, valid values or all23 setting semantics. | App usersettings/administration flags remain narrow reads; no generic App setter inferred. No account configuration values published. |
| WG13 Closed periods/budgets: BE010 | W03@40801 concrete `afgeslotenperiode` service, @523375 update/insert: PUT/POST root; grid/export @41565/41883. `budgetscenario` service @267678/306746/525698; GET and POST `budget/scenario/{id}` @307330/309563. | Period body startDatum/eindDatum/opmerking and optional ID; budget name/year and detailed scenario rows. Client permission checks are observed, not a full authorization contract. | No App counterparts established; no closures/budgets created or altered. |
| WG14 Archive restore: BK015 | W01@3318xx folder service: **GET `folder/{id}/undelete`**, POST `folder/bulk/undelete`, DELETE detail, POST bulk/delete; directory/filename PUT and folder/file lists/link reads also defined. | unDelete is restoring state, not query; bulk takes the selected folder/file identifiers. includeDelete/includeDeleted are distinct source flags. | Concrete web restore exists; neither FileDto nor App delete/Boolean response establishes an App undo endpoint. IDs must not be equated across families. |
| WG15 Opening balances: BE002 | W03@581930/582206 POST/PUT `beginbalans/openpost`; GET `beginbalans/getopenpost/{id}`; grid/export by type @587789/588262. | Open-item editor includes invoice/relation fields and explicit whitespace removal on the client. Browser also observes main balance/sum routes; complete main-write contract not yet traced. | New App mutation does not by itself establish opening-balance parity. No balance operation executed. |

## Read-only browser corroboration

The coordinating researcher independently opened/reloaded the relevant views and observed resource URLs, without reading account payloads into this report. These observations corroborate route use, not HTTP verbs, response schemas or write execution:

| View | Observed web JSON resources (prefix /v1/api/) |
| --- | --- |
| Asset report /bookkeeping assets | `vasteactiva/any`, `overzicht/vasteactiva`, `gebrokenBoekjaar` |
| VAT period / history | `aangifte/oudsteAangifte`, `aangifte/last/ob`, `aangifte/gridtable` |
| ICP period | `IcpOpgave/nextperiod` |
| Pending imports / automatic rules | `import/gridtable`, `import/countImport`, `setting/user.use-memoriaal`, `importregel/gridtable` |
| Opening balances / settings | `beginbalans/beginbalans`, `beginbalans/saldobeginbalansopenpost/{type}`, `instelling`, `instellinggroep` |
| Templates / closed periods | `factuursjabloon/gridtable`, `afgeslotenperiode/gridtable` |
| Audit/software-export forms | `gebrokenBoekjaar`; no download/export action invoked |
| Archive | `folder/directory`, `folder/{id}/header`, `folder/{id}/filelist`; deleted-items control left unchanged |

This is a source/observation overlay. No account state, record count, identifiers, provider configuration or financial values are reproduced. Three additional shared script names were observed on the opening-balance view but not downloaded: the existing bounded evidence was sufficient and no complete client/server contract is inferred from them.

Additional effect counterexample W09: createIncassobestand uses GET `incassobestand/create` with account/holder/execution-date query fields to create a collection file. This is a provider command despite GET, not a safe discovery probe. Likewise the postOnce client wrapper used in several examples is not evidence of provider idempotency, atomic consumption or retry safety. Query values and real account details are deliberately omitted.

## Existing-core overlap and authentication limits

The web family is not limited to the gaps. W01 contains existing invoice bulk-delete POST `factuur/normaal/bulk/delete` around279333; generic relation and ledger services around87299/70447; archive read/link/directory/rename/download functions around3318xx. W02 has bank-worklist and report operations. This supports investigating a uniform web interface as an alternative, **not** claiming that all existing App core operations, rights or response contracts already have web parity.

W01@602610 registers a process/application auth service whose startup checks call POST `auth`. The response is projected into currentDomain, administration/subscriber/accountant identity, permissions and settings. W01@923815 binds that service and HTTP providers. This static shape does not establish App-token reuse, safe context switching, expiry/renewal behavior, web-login automation or a public integration support contract.

The same service declares POST `auth/login` with a login request, then calls the host-provided setJwtToken function; GET `auth/switch/{id}` changes its administration context and GET `auth/changeLanguage/{value}` changes language. Its logout method throws rather than establishing a complete logout implementation. These source facts do not authorize invoking them or establish a reusable session protocol.

W04@69500 contains Angular's same-origin XSRF interceptor: it skips GET/HEAD and cross-origin requests and can use configured cookie/header token names. This is framework behavior present in the bundle, not proof that every server endpoint requires or accepts one particular CSRF mechanism. In particular it does not make side-effecting GETs safe. No cookie value, browser session, token or user-info response was inspected. A complete web authentication/CSRF/tenant lifecycle would need its own narrowly authorized source/contract admission before any connector implementation.

## Functional sufficiency and follow-ups

| Option | Supporting evidence | Unresolved cost / decision |
| --- | --- | --- |
| Keep uniform App-v4 for the evidenced subset | Broad APK client family and accepted endpoint registry; shared mobile lifecycle can remain isolated. | Must explicitly omit uncovered web operations; cannot promise full inventory coverage. Seek exact additional App contracts for each missing sub-operation, not guessed URL probes. |
| Investigate one uniform web interface | Actual gap routes plus existing-core overlap, provider-generated reports/calculations and submission operations. | Current source is partial across lazy modules and legacy frames; full DTO/auth/CSRF/context/effect/coverage contracts and integration-use support remain unproved. Not chosen here. |
| Deliberate App + web composition | Uses each demonstrated provider operation without recreating accounting rules. | Requires an owner-approved departure from uniform App routing, separate interface/auth/ID bindings and per-operation mapping. Does not solve remaining untraced contracts automatically. |

Concrete next evidence obligations: complete web DTO/request/error and authentication bindings for any selected operation; determine whether each missing sub-operation has an exact App source equivalent; distinguish report versus export versus processing/submission; resolve legacy/frame save contracts without interpreting URL availability as API support; retain partial/nullable results and source-defined effects. No broad arbitrary-HTTP tool or bookkeeping calculation fills a missing endpoint.

The [57-group/23-configuration matrix](api-functional-coverage.md) remains the complete functional taxonomy. This report is a bounded gap overlay, not a replacement inventory or a claim that every web/backend route has been enumerated. The static researcher made no account/API/auth requests. The separately observed normal browser frontend made its own auth/status/logging requests while views opened; this report does not claim that no POST occurred anywhere. No agent-directed administrative mutation, write button, manual accounting API command, purchase, payment, filing, export, import or restore was performed.

## Sources

- [Public main bundle](https://secure20.e-boekhouden.nl/main-5VUGM46G.js)
- [Public bookkeeping bundle](https://secure20.e-boekhouden.nl/chunk-OlmsPAN-.js)
- [Declared public administration bundle](https://secure20.e-boekhouden.nl/chunk-IXq3f3Xc.js)
- [Public shared runtime bundle](https://secure20.e-boekhouden.nl/chunk-C6Ihk1c2.js)
- [APK family/contracts](apk-api-contracts.md)
- [Functional coverage](api-functional-coverage.md)
- [Endpoint registry/admission](endpoint-design-catalogue.md)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-01 | Imp | Record public web-source gap evidence and bounded App-only completeness consequences without execution or route reselection. |
