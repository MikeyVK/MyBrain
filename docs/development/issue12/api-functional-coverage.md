<!-- pgmcp:v1 id=reference pv=1.0.0 pf=Q4Tx8SxSHKiKF_yz sf=WI5iXHBKVOU91bYE -->

# Function-by-function REST and App-v4 coverage research

**Status:** REOPENED FUNCTION-FIRST RESEARCH — ROUTE STRATEGY NOT YET CHOSEN  
**Version:** 1.0  
**Last Updated:** 2026-11-01

## Purpose

Reopen technical coverage from a function-first taxonomy, comparing official REST v1, the incomplete community App-v4 capture and broader static APK contracts. This evidence supersedes assumptions used by the earlier workflow-shaped design; it does not select or implement a replacement architecture.

## Scope In

57 generic functional groups and 23 configuration feature types; read/create/change/delete/link/generate/send/export distinctions; source identity, bounded gaps and concrete follow-up.

## Scope Out

No account configuration, provider selection, record values, private inventory paths, real financial examples or credentials. No live API/auth/browser operations, APK execution, new financial tests or implementation in this research.

## Sources

- [Official REST OpenAPI][src-1]
- [Pinned community App-v4 capture][src-2]
- [Expanded APK contract catalogue][src-3]
- [Historical bounded runtime evidence and synthetic preservation][src-4]
- [Official app feature description][src-5]
- [Official store feature history][src-6]

[src-1]: <https://api.e-boekhouden.nl/openapi/v1.json>
[src-2]: <https://github.com/kozmoz/e-boekhouden-APP-API-v4/blob/6ca849003ed196ca10877d8854644e9c38cf3145/swagger.openapi.json>
[src-3]: <apk-api-contracts.md>
[src-4]: <toolkit-preservation.md>
[src-5]: <https://www.e-boekhouden.nl/app>
[src-6]: <https://apps.apple.com/nl/app/e-boekhouden-nl/id1078225120>

## API Reference

### Evidence model and source versions

This is a generic functional taxonomy, not a publication of the inspected administration's configuration or records. Function IDs preserve the private inventory's crosswalk without its values or usage counts. A row is split by operation: a read or create does not make the whole web group supported.

| Grade | Meaning |
| --- | --- |
| D | Declared in the refreshed official REST specification; not necessarily executed |
| C | Described in the pinned community capture; observational/incomplete, not vendor documentation |
| A | Concrete compiled APK client/getter/HTTP-wrapper/DTO evidence; static intended contract |
| E | Endpoint constant or partial candidate only; caller/operation semantics still unresolved |
| HV | Separately authorized historical runtime verification, narrow as listed below; not a new test or universal guarantee |
| NF | No corresponding operation found within the identified inspected catalogue; not a universal absence claim |
| U | Unknown semantic/detail/coverage; explicit follow-up required |

REST refreshed 2026-11-01: OpenAPI 3.1.1/version v1, UTF-8 SHA-256 C9F8CB8893796B347AE75CAE516DF98817FCCB9889E426308858E7554D341AF9, 39 business operations on 24 paths plus two Swagger paths. Community revision 6ca849003ed196ca10877d8854644e9c38cf3145, Git blob 7d339beabba2273d29d5ff4c55473b178d8937d7, 33 paths/34 operations. It is not a complete App service catalogue. APK source identity and full Production binding are in the linked static catalogue: Android3.9.0 is a client release, not another API version. Static counts (217 selected client-method records/41 types) are not unique routes or runtime requests.

Historical verification labels refer to retained-source/evidence inventory, not private records:
- H1: selected REST reads/reference resolution, session cleanup, supplier creation and bounded type1 purchase creates, with strict financial checks on the tested variants.
- H2: selected App auth/context, day-filter lookup and visible/internal mutation mapping; narrow ledger/text updates. Internal IDs changed after updates; invoice-number whitespace normalization occurred. Paid full-PUT, arbitrary fields and independent row-text preservation remain unproved.
- H3: selected archive metadata/content/upload/link/rename and retained links for shared documents. No generic move/delete/restore/scan guarantee.
- H4: selected hours read/create/edit and receipt-owned synthetic cleanup. This is not general deletion authority.

The official app page/store release notes corroborate broad functional intent (including invoice output, hours billing, subscriptions, pending bank rows and configuration entities). They are not endpoint or current permission evidence. No new account requests or operational authorizations arise here.

### Three different route questions

| Question | Evidence-backed answer |
| --- | --- |
| Is the APK another independent API? | No for the inspected default client family: Production appapi.e-boekhouden.nl/api/ + v4/ is the same App family as the community capture and historical App helpers. REST v1 is separate. This does not mean every possible environment/version is identical. |
| Is one provider route family proved for all 57 web groups? | No. App-v4 has substantially broader core contracts than the earlier capture suggested, but filing/history, fixed assets, imports/rules, exports and several administration settings remain gaps. REST does not fill all of them either. |
| Could one uniform functional MCP surface dispatch internally? | Yes as an architectural possibility, independently of App-only versus deliberate mixed routing. It is not implemented or proved by this research, and dispatch cannot manufacture missing function contracts. |

App-only is a serious core candidate: one client family covers mutations, source-bank-row candidates, archive, quotes, sales invoices/queues, subscriptions, hours, relations, products and provider-calculated reports. It avoids duplicating provider credentials/ID mappings merely to offer one functional interface. Against it: unsupported/public-contract status, incomplete required-field/money/concurrency semantics, untested mail/processing/cascade effects and narrower historical execution proof.

REST+App is also a candidate: official REST has clearer supported financial/create/reference contracts and historical strict readback experience, while App supplies genuine gaps. Costs are separate authentication/identity models and capability-level routing. It is not automatic fallback on REST errors and does not solve functions absent from both inspected families. REST invoice creation with immediate email is not App queue manipulation; REST payment creation is not bank-worklist consumption.

No current route choice follows from the old REST-default policy or the earlier thin-tool design. Those remain historical reviewed artifacts. A new capability-specific strategy must follow this coverage review and the owner's priorities; unknown web/backend functions need additional contract research rather than invented local bookkeeping calculations.

### Bookkeeping — BK crosswalk

Paths in App columns are /api/v4-relative unless a full path is shown. Kxx keys refer to the static catalogue. NF is bounded to the listed source versions.

| ID / generic function | Official REST v1 (D unless HV) | Community App-v4 (C) | APK extended static evidence (A unless E) | Remaining boundary / follow-up |
| --- | --- | --- | --- | --- |
| BK-001 Received-invoice entry | GET/POST /v1/mutation, type1; H1 selected creates/readback | Filter/detail/PUT mutation only; no create declared | K02 POST /mutaties with CreateMutatieDto; GET/PUT/DELETE also declared; H2 only narrow updates | Required create fields, supplier/ledger/VAT/date choices and update semantics distinct; F01 |
| BK-002 Receipts and payments | POST /v1/mutation types3/4/5/6 D; no source-worklist-ID input | Mutation update/read; no new payment create declared | K02 POST /mutaties with soort and row factuur/relatieId; source-bank-row candidate separate | Enum numbers alone do not prove all UI kind meanings or settlement; F01/F02 |
| BK-003 Memorial/general journal | POST /v1/mutation type7 D | Mutation read/update candidate, no create contract | K02 generic create/update with kind enum and rows A | General-journal validation and attachment binding not runtime-proved; F01 |
| BK-004 Import worklist | NF for pending imported rows, rules/reprocess/delete/export | GET /afschriftregels and /{id} | K03 read/comment/delete; K02 source-bound create candidate | No automatic rule editor/reprocess-all or worklist export; consumption not proved; F02/F03 |
| BK-005 Balance report | GET /v1/ledger/balances and individual balance are raw-balance reads, not full report | NF balance report | K04 POST /balans with endDate/showGroups | Native layout/group parity and Excel/PDF/CSV export not established; F04 |
| BK-006 Profit-and-loss | Raw ledger balance reads only; no native report endpoint | POST /winstverlies/overzicht/ | K04 same POST, periods/groups/comparison DTO | Report query A/C, no export proof; F04 |
| BK-007 Ledger transactions | GET /v1/ledger, /{id}/balance and /v1/mutation filters; partial data only | Ledger picker, not ledger transaction report | K04 POST /grootboek/overzicht; GET ledger/{id}/saldo | Single-ledger/period/paging present; UI range/zero-account/cumulative options not all mapped; F04 |
| BK-008 Mutation search/detail/change | GET list/detail; POST new mutation. No mutation PATCH/PUT/DELETE | POST filter, GET internal detail, PUT mutaties; prefixless search not working proof | K02 adds create/delete/nextdata and richer MutatieFilterRequestDto | Copy/print independent actions; no general paid-edit/row-text guarantee. H1/H2 narrow; F01 |
| BK-009 Open items/follow-up | GET /v1/mutation/invoice/outstanding, C/D/invoice/paging; no write-off/reminder endpoint | POST /openposten/debiteuren and /crediteuren | K13 lists with includePaid/peildate/search, GET details, POST reminder/write-off | Full payment graph, credit workflow/comment mutation/incasso-agency/grouping remain partial/U; F05 |
| BK-010 Fixed assets/depreciation | NF asset register/schedule/posting/report | NF | NF in inspected client/endpoint/DTO groups | Do not replace with inferred journal logic. Exact web/backend asset contract needed; F06 |
| BK-011 Other financial reports/dashboard | Raw balances only, no report/export parity | Dashboard balances/open items/P&L reads | K04 dashboard/ledger/P&L/balance candidates | Column balance/liquidity/top-lists/full current-state parity and exports partial/NF; F04 |
| BK-012 VAT return preparation/submission | NF; VAT codes/mutations are not filing operations | NF | NF filing client | Tax-return calculation/view/submit/pay are separate unknowns; F06 |
| BK-013 ICP listing/submission | NF | NF | NF | Exact listing and submission contract needed; F06 |
| BK-014 Submitted returns/payment history | NF | NF | NF | History/acceptance/payment actions not inferred from generic payment creation; F06 |
| BK-015 Archive files/folders | NF upload/archive/link API | Browse/detail/download/upload/link/unlink/folder-create/move/delete observed | K05 adds POST search, folder PUT/delete, batch-delete, scan, attachment query; H3 selected only | Restore/undo absent from inspected methods; namespace/graph/move semantics U; F07 |
| BK-016 Preview features | NF | NF | NF | No concrete function contract identified; establish a named feature first; F08 |
| BK-017 Automatic bank-import rules | NF | NF | NF rule CRUD/reprocessing | Comment/delete bank row is not rule editing. Obtain rule schema/operation; F03 |
| BK-018 Bank-file upload/import | NF uploaded-statement wizard | NF | NF file-format/deduplicate import contract | Archive upload is not statement import. Exact preview/commit/duplicate semantics needed; F03 |
| BK-019 Automatic recognition/entry feature | NF activation/reporting | NF activation | K05 per-file scan flag/scan call only, not activation/invoer-report | Feature configuration/interlocks/processing contract unknown; F08 |
| BK-020 Archive capacity/credits/recognition inbox | NF | Directory metadata only | K05 isMailEnHerkenInbox/setAsMenHInbox; K14 GET /credits/saldo | Credit read not storage quota, purchase or active automatic recognition proof; F07/F08 |

### Sales, quotes and products — FA crosswalk

| ID / generic function | Official REST v1 | Community App-v4 | APK extended static evidence | Remaining boundary / follow-up |
| --- | --- | --- | --- | --- |
| FA-001 Sales invoice entry/detail/edit | GET /v1/invoice list/detail, POST create D; no existing-invoice edit/delete | NF | K06 filter/detail/create/PUT/delete, row-change lists | Create versus edit/processed-document restrictions and string-number identity require validation; F09 |
| FA-002 Print/email queue and sending | New-invoice print=true prepares printing; email object sends immediately D. Not existing queue control | NF | K06 GET download/maildata/emailencount; POST bulk/setmail, mail, bulk/email | Queue removal semantics U; read mail data, queue and send are separate. H: none; F09 |
| FA-003 Electronic invoicing/Peppol candidate | No declared Peppol operation; generic errors not proof | NF | NF named client | Functional target itself unconfirmed; no need/coverage claim; F08 |
| FA-004 Direct-debit file/output | New-invoice directDebit metadata D; does not generate file | NF | IncassobestandClient GET /incassobestand/formdata, GET /incassobestand/hasincassokoppeling; POST /incassobestand/send A (concrete async bodies) | Generation/download versus transmission/connection effects U. No runtime or mail/bank authority; F10 |
| FA-005 Quotes/search/status | NF quote CRUD | NF | K07 quote CRUD/filter; K10 status/progress-type CRUD; typed filters | Search selectors largely represented; exact sort/permissions/transition validation U; F11 |
| FA-006 Standard invoice definitions | Invoice templates D are layout metadata, not this function | NF | K08 POST filter, GET detail, POST/PUT/DELETE /standaardfacturen | Definition CRUD not separate generate/schedule proof; F09 |
| FA-007 Subscription list/create/edit/bill | NF | NF | K08 CRUD/filter/nextdata/formdata/bulk factureer/delete | Cadence/selection/hold/scheduling/auto-send behavior needs validation; F12 |
| FA-008 Products/services | GET/POST/PATCH/DELETE /v1/product D | NF | K09 article filter/detail/create/update/delete | Monetary defaults/cost-center/stock field semantics and used-product delete constraints U; F13 |
| FA-009 Units and product groups | GET /v1/unit and /v1/product/groups D; no unit/group CRUD | NF | K10 GET/POST/PUT/DELETE /eenheden and /artikelgroepen | CRUD declarations, no current runtime proof; F13 |
| FA-010 Quote dashboard operations | NF quote copy/mail/convert/download | NF | K07 duplicate, mail/maildata/download, createfactuur, row CRUD | Quote-to-invoice choice and outward effects explicit; no UI tab parity implied; F11 |
| FA-011 Process/delete existing invoices | POST create mutation option makes a NEW mutation; not existing invoice processing | NF | K06 POST /facturen/bulk/verwerk, /bulk/delete; DELETE detail | Already-processed/double-processing/delete consequences U; F09 |
| FA-012 Quote progress/files/invoice links | NF | Generic file links without quote-kind semantics | K07 progress CRUD; K05 generic attachments; quote invoice creation/IDs A | Quote file kind and reverse invoice-list parity U; F07/F11 |
| FA-013 Product spreadsheet import | NF standalone CSV/XLS/XLSX wizard | NF | NF import contract | Product CRUD is not duplicate/overwrite-import semantics; F03 |
| FA-014 Product changes cascading into subscriptions | PATCH /v1/product updateSubscriptions:0 none/1 price/2 all D | NF | K09 ArtikelUpdateDto(artikel,cascade,cascadePriceOnly) A | Two different wire contracts; prove actual affected fields/atomicity, never auto-select; F13 |
| FA-015 Subscription cadence/hold/auto effects | NF | NF | K08 per/start/end/expiration/geenFactuur/mail/autoVerwerk and row-change fields; bulk billing directVerwerken | Exact cadence enum/automatic scheduling and generate-versus-send/processing effects U; F12 |

### Relations and hours — RE/UR crosswalk

| ID / generic function | Official REST v1 | Community App-v4 | APK extended static evidence | Remaining boundary / follow-up |
| --- | --- | --- | --- | --- |
| RE-001 Relations/contact/defaults | GET/POST/PATCH /v1/relation D; H1 selected reads/create; no DELETE | NF relation CRUD | K11 filter/detail/POST/PUT/DELETE/bulk-delete, full contact/default/tax/mandate/custom fields A | Company/private versus free soort distinct; alias choice and field precedence not inferred; F13 |
| RE-002 Newsletters/groups | Email-template list useMailing flag D; not send/group CRUD | NF | K11 GET/POST relation mailing membership; mailing picker E | Membership is not newsletter send or group administration; F14 |
| RE-003 Relation spreadsheet import | NF CSV/XLS/XLSX import | NF | NF import contract | Relation create/patch not wizard duplication/overwrite policy; F03 |
| RE-004 Mail-archive/recognition permission | No menHAllowMail/menHAllowHerken fields in relation schema | NF | K11 RelatieDetailsDto permissions + create/update A | Permission fields do not establish mailbox delivery/recognition pipeline; F07/F08 |
| UR-001 Hours/km entry/read/edit | NF hours API | NF in capture | K12 GET/filter/POST/PUT/DELETE /uren; H4 narrow | Null/zero/date/ownership/invoiced restrictions preserved; general delete not verified; F15 |
| UR-002 Generate invoices from hours | NF | NF | K12 POST /uren/factureren with FactureerUrenRequestDto.uurIds | Selection and billing settings are separate; exact outputs/book/mail side effects U; F15 |
| UR-003 Hours reports by period/project/activity/year | NF | NF | K12 registration filter supports period/employee/project/activity/search/nietGefactureerd | Data query is not exact native report grouping/tariff aggregation/export proof; F04/F15 |
| UR-004 Projects/activities/rates | NF | NF | K12 project/activity filter/detail/CRUD and projectafwijkendetarieven CRUD | User/project/activity IDs and tariff rules/permissions need fixtures, not guessed defaults; F15 |
| UR-005 Hours-billing configuration | NF | NF | K12 GET and POST /factuurinstellingen with unit/template/line text/term/post/mail/incasso/process flags | Setter is POST, not PUT; actual mail/process consequences not tested; F15 |

### Administration — BE crosswalk

| ID / generic function | Official REST v1 | Community App-v4 | APK extended static evidence | Remaining boundary / follow-up |
| --- | --- | --- | --- | --- |
| BE-001 Chart of accounts/groups | Ledger GET/POST/PATCH D, balances; no ledger DELETE or account-group CRUD | Context ledger picker only | K10 ledger/group list/detail/POST/PUT/DELETE A | Preserve category/references and used-account restrictions; F13 |
| BE-002 Opening balances | No dedicated opening-balance operation; type7 not proven parity | NF | NF opening-balance client | Exact opening-year/debtor-creditor setup contract needed; F06 |
| BE-003 General settings | Administration lists are not settings; no general setter | userinfo only | K14 GET /settings/administratie and userinfo flags; specific settings elsewhere | See 23-feature crosswalk below; read flags are not setters; F16 |
| BE-004 Integrations/bank connections | No connection-management contract | NF | Incasso has connection-availability read; not bank-feed configuration | Provider activation/revocation/status, import success and credentials scope U; F10/F16 |
| BE-005 Mutation spreadsheet import | NF file-import contract | NF | NF spreadsheet-import client | POST mutation is an individual entry, not file import/deduplication; F03 |
| BE-006 Asset setup | NF asset model/schedule | NF | NF asset family | Same gap as BK-010, not an inferred journal substitute; F06 |
| BE-007 Dunning/invoice/quote/email templates | GET /v1/invoicetemplate(id/name/active/type), /emailtemplate(id/name/use flags) D; no content editor | NF | K10 email-template detail read; template picker constants E | Layout/content create/edit/copy not established; F14 |
| BE-008 Users/account/security | GET member is membership administration, not user/rights control | userinfo is current context only | K01 context/permissions; users picker constant E; K14 own business details read/update | No general user/MFA/SMTP/rights management proof; F16 |
| BE-009 Auditfile/software exports | NF export operations | NF | NF export client | Exact format/version/period/content/download contract needed; F04 |
| BE-010 Closed periods/budget scenarios | No declared management route; generic error codes not operations | NF | NF matching client | Actual list/create/change/close semantics unknown; F06/F16 |
| BE-011 Accountant/administrations | GET /v1/administration and /linked D have accountant/linked semantics, not general switch | GET /administraties C | K01 auth switch; K14 own/accountant lists and own-details read/PUT A | REST GUID/linked list and App admin IDs not equivalent; entitlement/switch contract U; F16 |
| BE-012 Custom field definitions | Relation freeText1..10 values D; not definition labels | NF | K11 GET /relaties/customfields(index,name) and relation index/value fields A | Label-definition create/update setter NF in client catalogue; F16 |
| BE-013 API credential administration | Session POST/DELETE authenticates, not token CRUD | NF | No token-management client; auth login/renew/logout is not token-list editing | Host/portal credential lifecycle requires separate evidence/authority; F16 |

### Configuration-feature crosswalk without private values

This table maps feature TYPES only. It intentionally publishes no observed account on/off values, provider choices, selected periods or template selections. D/C/A/E have the same bounded meanings as above.

| Feature ID | Generic feature | Read evidence | Change evidence / unresolved scope |
| --- | --- | --- | --- |
| CFG-001 | Document/bookstuk field | App GET auth/userinfo → UserSettingDto.useBoekstuk A | General flag setter NF; mutation boekstuk field is not setting change |
| CFG-002 | VAT total/per-row mode | App GET mutaties/btwperregel C/A; GET facturen/settings → calculateBtwPerRow A | No general mode setter; mutation versus invoice context may differ |
| CFG-003 | Extended foreign VAT codes | App GET btwcodes/inkoop/verkoop A; selection data only | Catalogue read does not prove activation flag read/write |
| CFG-004 | VAT-liability setting | Company tax identifiers exist, not this boolean | General read/set NF |
| CFG-005 | Prior-period VAT-correction checks | NF exact feature field | General read/set NF |
| CFG-006 | Invoice format | REST GET invoice urlPdfFile D; App invoice PDF download A | Output retrieval not global format-setting read/write |
| CFG-007 | Cost-centre enablement | App GET settings/administratie.useKostenplaatsen A | REST costcenter CRUD changes entities, not enable flag; setter NF |
| CFG-008 | Row-description enablement | App settings. exact field omschrijvingPerMutatieregel A | Read flag only; setting setter and independent stored-row behavior U |
| CFG-009 | RGS configuration | App settings.rgslevel and rgscodes read A | RGS lookup/export availability not level setter |
| CFG-010 | General sales payment-term preference | App settings.standaardBetalingsTermijn A, sales-specific semantics U | Per-invoice/relation term setters are not global preference |
| CFG-011 | UBL version/automatic attachment | REST new-invoice email.attachUbl/invoiceUbl D; App FactuurEmailRequestDto.factuurUbl A | Per-send options; global version/auto-attach setter NF |
| CFG-012 | Memorial enablement | App userinfo.useMemoriaal A | Mutation kind support not toggle setter |
| CFG-013 | Remember last relation | NF matching preference field | General read/set NF |
| CFG-014 | Remember last VAT selection | VAT lists exist, not preference | General read/set NF |
| CFG-015 | Remember last counteraccount | Ledger lookups exist, not preference | General read/set NF |
| CFG-016 | Inventory enablement | App userinfo.useVoorraad A; product inVoorraad is per-product | Product stock field is not global switch |
| CFG-017 | Automatic recognition activation | Per-file upload scan/scan request A | Activation/interlocks/invoer-report NF |
| CFG-018 | Hours-billing output/process flags | GET /factuurinstellingen A | POST same route A; consequences require validation |
| CFG-019 | Subscription bill-now processing | GET abonnementen/facturerenFormData A | AbonnementFacturerenDto.directVerwerken A; per-billing action, not universal default |
| CFG-020 | Per-subscription hold/automatic effects | AbonnementDetailsDto.geenFactuur/mailFactuur/autoVerwerk A | POST/PUT abonnementen A; scheduling semantics U |
| CFG-021 | Product→subscription cascade | REST PATCH updateSubscriptions D; App ArtikelUpdateDto flags A | Explicit per-update action, not an always-on global policy |
| CFG-022 | VAT return period preference | No return configuration contract | Read/set NF |
| CFG-023 | Fiscal-year start | No exact field/operation established | Date filters are not fiscal-year configuration; F16 |

No unchanged/empty setting is inferred to be false, and no absent API flag is filled from UI defaults. Specific form settings and general configuration remain separate capabilities.

### Concrete remaining evidence work

These are research follow-ups, not permission to execute operations. Prefer further static/public contracts first; any account-specific verification needs a new explicit scope. No missing financial report or tax operation is replaced with guessed local rules.

| Follow-up | Concrete missing evidence / acceptance target |
| --- | --- |
| F01 Mutation semantics | Trace mobile create/form mapper for all requested kinds; pin required header/row/payment fields and ID namespaces. Later authorized synthetic create/update readback must preserve protected fields; no general paid PUT inferred. |
| F02 Bank worklist consumption | Trace UI/service assignment of source row ID into CreateMutatieDto; determine source-bound create response, row removal, partial matching and atomic/retry semantics. A future controlled proof must read both mutation and source queue before/after; no blind trial now. |
| F03 Imports/rules | Find exact web backend/public client contracts for statement/product/relation/mutation file preview/commit, rule CRUD and reprocess actions, with overwrite/duplicate/error semantics. Existing CRUD/archive upload is insufficient. |
| F04 Reports/exports | Identify native report/export request/response/download contracts for the named report/format/period options; compare data/grouping without reimplementing bookkeeping calculations. |
| F05 Payment/open-item graph | Classify list/detail IDs and returned paid/open data, exact filters and all observed references; obtain explicit comment/credit/agency operations. No missing row becomes paid=0 or a complete graph. |
| F06 Tax/assets/periodic setup | Obtain separate fixed-asset/schedule/post, opening-balance, VAT/ICP preparation/submission/history/payment and period/budget contracts from vendor or authorized static web sources. REST+App mix currently does not close these gaps. |
| F07 Archive graph/restore | Trace link-kind mapping, association-reference namespace, move/delete/restore effects and folder/inbox flags. Verify existing-target retention and identical bytes only in a separately authorized narrow proof. |
| F08 Optional/unidentified features | Establish a named functional requirement and exact activation/status/report contract for recognition/preview/e-invoicing before choosing a route. UI text or generic validation error is insufficient. |
| F09 Invoice lifecycle | Trace queue-on/queue-off, print/download, immediate mail versus queued mail, existing invoice processing/delete and processed-state restrictions. Verify side-effect flags separately; never test by sending mail. |
| F10 Connection/incasso | Classify incassobestand/send response/effect (file versus transmission), connection-provider and mandate validation; obtain bank-feed management contract separately. |
| F11 Quotes | Pin conversion percentage/row selection, progress/status transitions, attachment-kind and reverse invoice links; no whole-dashboard parity from one route. |
| F12 Subscriptions | Decode cadence/scheduling/hold and generated-invoice/mail/process selection rules; distinguish per-subscription state from bill-now parameters. |
| F13 Master data/cascade | Pin exact identity/default/category/stock fields and used-entity restrictions, then cascade affected-field and failure semantics. No automatic alias/account/VAT selection. |
| F14 Templates/newsletters | Find layout/content editor/copy/group/send contracts. Picker, member list or useMailing flag is not that contract. |
| F15 Hours | Preserve exact nullable DTO/ID/date/precision/ownership semantics; trace invoiced-hour restrictions, billing settings and output effects; report aggregation/export needs its own evidence. |
| F16 Administration | Obtain feature-specific flag/setter, user/rights/security/credential lifecycle and fiscal-year contracts. Keep accountant/linked administration listing separate from authenticated current-context binding. |

The old interface policy and reviewed design can supply preservation lessons, but are not the current implementation basis. A later owner-approved strategy may select App-only for the evidenced core, deliberate REST+App composition, or additional backend research for uncovered functions. This document records evidence and trade-offs, not a new operational mandate.

## Related Documents

- [Research entrypoint](<research.md>)
- [Official/API documentation inventory](<api-catalog.md>)
- [Historical App assessment](<app-api-v4-assessment.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-01 | Imp | Complete operation-specific functional/configuration crosswalk using refreshed REST/community sources and expanded APK evidence. |
