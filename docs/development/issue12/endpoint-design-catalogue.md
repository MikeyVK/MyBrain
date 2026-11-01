<!-- pgmcp:v1 id=reference pv=1.0.0 pf=Q4Tx8SxSHKiKF_yz sf=WI5iXHBKVOU91bYE -->

# App-v4 endpoint registry and functional admission contract

**Status:** APP-ONLY ENDPOINT DESIGN — NOT IMPLEMENTED  
**Version:** 1.0  
**Last Updated:** 2026-11-01

## Purpose

Define the single source-backed registration boundary for the chosen endpoint-oriented server. Registry entries describe technical provider operations, not bookkeeping workflows or authority to execute them.

## Sources

- [APK contract evidence K01–K14][src-1]
- [Function/configuration evidence matrix][src-2]
- [Canonical technical contracts][src-3]

[src-1]: <apk-api-contracts.md>
[src-2]: <api-functional-coverage.md>
[src-3]: <design-contracts.md>

## API Reference

### Registry authority and admission

One immutable registry is loaded once at startup. Each concrete entry has operation_id, stable MCP name, effect, HTTP method, fixed /api/v4 path template, typed path/query/body schemas, response schema, body serializer profile, pagination metadata, possible side effects, admission/evidence status and inventory IDs. Named endpoint entries are expanded from the finite rows below, not from caller URLs or reflection over every APK method. Method/URL/headers/schema IDs cannot be supplied by an MCP caller.

The tables are the authoritative operation design. Schema names refer to the exact APK DTO definitions and their inherited properties/JsonProperty metadata, pinned by the source identity in the APK catalogue; representative full field seams and the deterministic schema-construction rule are in the contract appendix. This Design does not duplicate all 229 property-bearing DTOs. Implementation must provide the complete field registry/fixtures for each enabled operation; a missing schema/parameter mapping makes that operation unavailable, never a permissive JSON placeholder. A registration change adds a source-backed entry/model/fixture; handlers, auth, transport and audit do not acquire per-operation branches.

Legend: Q = provider query (including filter/calculation POST); C = provider state-changing command; L = local technical artifact command; AUTH = internal authentication/context effect. A = compiled contract, HV = bounded historical execution evidence, GAP = no admitted route. A is not a runtime guarantee. Initial implementation can register the backed operation set once complete schema admission is proven; writes remain disabled in distributed config. GAP/E-only rows are capability metadata and have no callable placeholder. Side-effect metadata is conservative and never execution permission.

Stable names below use app_<resource>_<action>. A slash-separated action list means a finite set of separate registrations, with the listed verbs/paths aligned in order. It does not create an arbitrary action argument. All inputs have the common profile alias; commands additionally require dispatch_id. Auth secrets are never public body schemas.

### Mutation, bank-row and archive registrations

| Stable operation names | Method/path; effect | Request → response contract | Inventory/evidence |
| --- | --- | --- | --- |
| app_mutations_list | POST /mutaties/filter; Q | MutatieFilterRequestDto → MutatieDtoPagedResponse | BK001–003/008; K02 A |
| app_mutations_get | GET /mutaties/{internal_id}; Q | AppMutationVersionId64 path → MutatieDetailsDto | BK001–003/008; K02 A/HV |
| app_mutations_create | POST /mutaties; C | CreateMutatieDto → MutatieDetailsDto | BK001–004/008; K02 A; no server booking choices |
| app_mutations_update | PUT /mutaties; C | UpdateMutatieDto → MutatieDetailsDto | BK001–003/008; K02 A/HV narrow only |
| app_mutations_delete | DELETE /mutaties/{internal_id}; C | AppMutationVersionId64 → MutatieDto | BK008; K02 A; deletion semantics/permissions not execution-proven |
| app_mutations_vat_mode | GET /mutaties/btwperregel; Q | EmptyBody → GenericBoolDto | BE003/CFG002; K02 A/C |
| app_bank_rows_list / get | GET /afschriftregels; GET /afschriftregels/{id}; Q | EmptyBody / BankRowId32 → AfschriftRegelsResponseDto / AfschriftRegelDto | BK004; K03 A/C |
| app_bank_rows_comment | PUT /afschriftregels/opmerking; C | UpdateAfschriftRegelOpmerkingDto → same DTO/HTTP acknowledgement | BK004; K03 A |
| app_bank_rows_delete | DELETE /afschriftregels/{id}; C | BankRowId32 → AfschriftRegelDto | BK004; K03 A; not processing |
| app_archive_list / get | GET /bestanden or /bestanden/{directory_id}; GET /bestanden/bestand/{id}; Q | Optional DirectoryId32 / FileId32 → DirectoryDto / FileDto | BK015/020; K05 A/HV |
| app_archive_search | POST /bestanden/search; Q | BestandenSearchRequestDto → BestandenSearchResultDto | BK015; K05 A |
| app_archive_download | GET /bestanden/download/{id}; provider Q plus L | FileId32 → BinaryArtifactReceipt | BK015; K05 A/HV; explicit private binary capture |
| app_archive_upload | POST /bestanden/upload; C | UploadToolRequest → UploadFileResponse | BK015; K05 A/HV; base64 translation only |
| app_archive_update | PUT /bestanden; C | UpdateFileDto → FileDto | BK015; K05 A/HV name-only; directory change is explicitly broader |
| app_archive_file_delete | DELETE /bestanden/bestand/{id}; C | FileId32 → FileDto/HTTP acknowledgement | BK015; K05 A |
| app_archive_directory_create / update / delete | POST /bestanden/directory; PUT same; DELETE /bestanden/{id}; C | CreateUpdateDirectoryDto / DirectoryId32 → DirectoryDto / acknowledgement | BK015/020; K05 A |
| app_archive_links_list | POST /bestanden/gekoppeld; Q | GekoppeldRequestDto → GekoppeldResponseDto (source shape acceptance required) | BK008/015/FA012; K05 A/HV one domain |
| app_archive_link_create / delete | POST /bestanden/koppel; DELETE /bestanden/koppel/{association_id}; C | CreateFileKoppelDto / AssociationId32 → source link response | BK008/015/FA012; K05 A/HV create one domain |
| app_archive_move_bulk / delete_bulk | POST /bestanden/bulkMove; POST /bestanden/bulkDelete; C | BulkMoveFolderDto / BulkActieRequestDto → source bulk response | BK015; K05 A |
| app_archive_scan | POST /bestanden/scan/{id}; C | FileId32 → provider Boolean/result envelope | BK019/020 partial; K05 async A; recognition can have further provider effects |

Source-exact response names not present in the compact evidence are resolved from the pinned method generic argument before enabling that registration; the runtime never substitutes Any. The linked-file names above are the actual GekoppeldRequestDto/GekoppeldResponseDto pair (client RVA923300); no alternate guessed schema names are admitted. Other incomplete response mappings remain schema admission obligations, not provider guesses.

Ancillary candidate GET /mutaties/nextmutatiedata/{argument} and its /afschriftregel/{id} suffix are source-backed, but their complete kind/query mapping must be pinned before registering app_mutations_next_data or app_bank_rows_entry_data. They remain non-callable until then. CreateMutatieDto.afschriftRegelId is forwarded only when caller supplies it; the server neither chooses a pending row nor interprets queue consumption, matches invoices, creates a payment, or deletes the row automatically. Archive link kind/target values are caller-supplied typed provider fields, not inferred by the server from bookkeeping type.

### Sales, quotes and subscription registrations

| Stable operation names | Method/path; effect | Request → response contract | Inventory/evidence |
| --- | --- | --- | --- |
| app_sales_invoices_list / get | POST /facturen/filter; GET /facturen/{id}; Q | FactuurFilterRequestDto / InvoiceId32 → FactuurDtoPagedResponse / FactuurDetailsDto | FA001; K06 A |
| app_sales_invoices_create / update / delete | POST /facturen; PUT /facturen; DELETE /facturen/{id}; C | CreateFactuurDto → CreateFactuurResponseDto; UpdateFactuurDto → PutWithBoolResult wrapper; InvoiceId32 → source delete response | FA001/011; K06 A |
| app_sales_invoices_download | GET /facturen/{id}/download; Q+L | InvoiceId32 → BinaryArtifactReceipt | FA002; K06 A |
| app_sales_invoices_mail_data / email_count | GET /facturen/{id}/maildata; GET /facturen/emailencount; Q | InvoiceId32 / EmptyBody → EmailDataDto / GenericCountDto | FA002; K06 A |
| app_sales_invoices_mail / email_bulk | POST /facturen/mail; POST /facturen/bulk/email; C | FactuurEmailRequestDto → EmailResponseDto | FA002; K06 A; external mail |
| app_sales_invoices_queue_mail / queue_debit / process_bulk / delete_bulk | POST /facturen/bulk/setmail; /facturen/bulk/setincasseren; /facturen/bulk/verwerk; /facturen/bulk/delete; C | BulkActieRequestDto → FactuurBulkResponseDto / BulkDeleteResponseDto | FA002/004/011; K06 A |
| app_sales_invoices_calculate_totals / price_exclusive / price_inclusive | POST /facturen/calculatetotals; /facturen/calculateprijsexcl; /facturen/calculateprijsincl; Q | CalculateFactuurTotalsRequestDto / CalculatePrijsRequestDto → matching response DTO | FA001/008; K06 A; provider calculation, no local calculation |
| app_sales_invoices_settings | GET /facturen/settings; Q | EmptyBody → FactuurSettingsDto | CFG002 partial; K06 A |
| app_quotes_list / get | POST /offertes/filter; GET /offertes/{id}; Q | OffertesFilterRequestDto / QuoteId32 → OfferteDtoPagedResponse / OfferteDetailsDto | FA005/010; K07 A |
| app_quotes_create / update / delete | POST /offertes; PUT /offertes; DELETE /offertes/{id}; C | CreateOfferteDto / UpdateOfferteDto / QuoteId32 → quote DTO/acknowledgement | FA005/010; K07 A |
| app_quotes_duplicate / invoice_create | POST /offertes/duplicate; POST /offertes/createfactuur; C | GenericIdDto / CreateFactuurFromOfferteRequestDto → GenericIdDto / FactuurDetailsDto | FA010/012; K07 A |
| app_quotes_mail_data / download | GET /offertes/{id}/maildata; GET /offertes/{id}/download; Q / Q+L | QuoteId32 → EmailDataDto / BinaryArtifactReceipt | FA010; K07 A |
| app_quotes_mail | POST /offertes/mail; C | OfferteEmailRequestDto → EmailResponseDto | FA010; K07 A; external mail |
| app_quote_rows_create / update / delete / update_bulk | POST /offerteregels; PUT same; DELETE /offerteregels/{id}; PUT /offerteregels/bulk; C | CreateUpdateOfferteRegelDto / QuoteRowId32 / UpdateMultipleOfferteregelsDto → row/quote DTO | FA010; K07 A |
| app_quote_progress_list / get | GET /offertes/{quote_id}/voortgang; GET same/{progress_id}; Q | typed IDs → OfferteVoortgangResponseDto / OfferteVoortgangDetailsDto | FA012; K07 A |
| app_quote_progress_create / update / delete | POST /offertes/{quote_id}/voortgang; PUT same; DELETE same/{progress_id}; C | typed IDs + CreateUpdateOfferteVoortgangDto → progress DTO | FA012; K07 A |
| app_quote_appointments_list / create / update / delete | GET/POST/PUT /offertes/{quote_id}/afspraken; DELETE same/{appointment_id}; Q/C | typed IDs + CreateUpdateOfferteAfspraakDto where applicable → source appointment DTO | FA012 extension; K07 A |
| app_subscriptions_list / get | POST /abonnementen/filter; GET /abonnementen/{id}; Q | AbonnementFilterRequestDto / SubscriptionId32 → paged/detail DTO | FA007/015; K08 A |
| app_subscriptions_create / update / delete | POST /abonnementen; PUT same; DELETE same/{id}; C | AbonnementDetailsDto → CreateFactuurResponseDto; UpdateAbonnementDto → PutWithBoolResult wrapper; SubscriptionId32 → source delete response | FA007/015; K08 A |
| app_subscriptions_billing_data | GET /abonnementen/facturerenFormData; Q | EmptyBody → AbonnementenFacturerenFormDataDto | FA007/015; K08 A |
| app_subscriptions_invoice_bulk / delete_bulk | POST /abonnementen/bulk/factureer; POST /abonnementen/bulk/delete; C | AbonnementFacturerenDto / BulkActieRequestDto → BulkCreateResponseDto / BulkDeleteResponseDto | FA007/015; K08 A |
| app_standard_invoices_list / get / create / update / delete | POST /standaardfacturen/filter; GET /standaardfacturen/{id}; POST/PUT root; DELETE detail; Q/C | list filter / StandardInvoiceId32 → source paged/detail; StandaardFactuurDetailsDto → CreateFactuurResponseDto; UpdateStandaardFactuurDto → PutWithBoolResult wrapper | FA006; K08 A |

Mail queue removal, print-queue toggling, Peppol and a general print/export operation lack a complete admitted contract. No invented inverse flag or fallback is registered. Form-data/next-data and quote-rest-amount getters can be added only with their exact source parameter schema. Provider invoice/billing/bulk/calculation operations are legitimate endpoint functions: the server forwards supplied fields and returned results, never chooses rows, discounts, cadence, prices, VAT or whether to send/process. Possible output/processing effects are recorded on each operation and on known payload flags.

### Master data, hours, reports and administration registrations

| Stable operation family | Fixed methods/paths; effect | Schemas / functional trace |
| --- | --- | --- |
| app_products_list/get/create/update/delete/delete_bulk | POST /artikelen/filter; GET /artikelen/{id}; POST/PUT root; DELETE detail; POST /artikelen/bulk/delete; Q/C | ArtikelFilterRequestDto, ArtikelDto, ArtikelUpdateDto(artikel,cascade,cascadePriceOnly), BulkActieRequestDto; FA008/013(partial)/014, K09 |
| app_product_groups_list/get/create/update/delete | GET /artikelgroepen, GET /{id}, POST/PUT root, DELETE detail; Q/C | ArtikelGroepenResponseDto/ArtikelGroepDto; FA009, K10 |
| app_units_list/get/create/update/delete | GET /eenheden, GET /{id}, POST/PUT root, DELETE detail; Q/C | source unit response/detail DTO; FA009, K10 |
| app_ledgers_list/get/create/update/delete | GET /grootboekrekeningen, GET /{id}, POST/PUT root, DELETE detail; Q/C | source Grootboek request/response DTOs; BE001, K10 |
| app_ledger_groups_list/get/create/update/delete | GET /rekeninggroepen, GET /{id}, POST/PUT root, DELETE detail; Q/C | source RekeningGroep DTOs; BE001, K10 |
| app_quote_statuses_list/create/update/delete | GET/POST/PUT /offertestatussen, DELETE /{id}; Q/C | source OfferteStatus DTOs; FA005, K10 |
| app_progress_types_list/create/update/delete | GET/POST/PUT /voortgangsoorten, DELETE /{id}; Q/C | VoortgangSoortDto/source response; FA005/012, K10 |
| app_relations_list/get/create/update/delete/delete_bulk | POST /relaties/filter; GET /relaties/{id}; POST/PUT root; DELETE detail; POST /relaties/bulk/delete; Q/C | source specific filter; RelatieCreateDto → RelatieDetailsDto; RelatieUpdateDto → PutWithBoolResult wrapper; bulk source response; RE001/003(partial)/004, K11 |
| app_relation_fields_get | GET /relaties/customfields; Q | CustomRelatieFieldsResponseDto; BE012, K11 |
| app_relation_mailing_get/update | GET/POST /relaties/{id}/mailinglijst; Q/C | source relation membership DTOs; RE002 partial, K11 |
| app_hours_list/get/create/update/delete | POST /uren/filter; GET /uren/{id}; POST/PUT root; DELETE detail; Q/C | UrenFilterRequestDto/UurDto and source paged response; UR001/003 partial, K12 |
| app_hours_invoice | POST /uren/factureren; C | FactureerUrenRequestDto(uurIds) → source Boolean/result; UR002, K12 |
| app_hours_invoice_settings_get/update | GET/POST /factuurinstellingen; Q/C | FactuurInstellingenDto; UR005/CFG018, K12; update is POST |
| app_projects_list/get/create/update/delete | POST /projecten/filter; GET /projecten/{id}; POST/PUT root; DELETE detail; Q/C | ProjectFilterRequestDto/source ProjectDto; UR004, K12 |
| app_activities_list/get/create/update/delete | POST /activiteiten/filter; GET /activiteiten/{id}; POST/PUT root; DELETE detail; Q/C | ActiviteitFilterRequestDto/source ActiviteitDto; UR004, K12 |
| app_project_rates_list/get/create/update/delete | GET /projectafwijkendetarieven?ProjectId={id}; GET /{id}; POST/PUT root; DELETE detail; Q/C | source tariff DTOs; UR004, K12 |
| app_reports_balance / profit_loss / ledger | POST /balans; POST /winstverlies/overzicht/; POST /grootboek/overzicht; Q | BalansRequestDto/WinstEnVerliesRequestDto/GrootboekOverzichtListRequestDto → source report DTO; BK005/006/007/011 partial, K04 |
| app_ledgers_balance_get | GET /grootboekrekeningen/{id}/saldo; Q | source SaldoDetailsDto; BK007, K04 |
| app_dashboard_payment_balances/open_items/profit_loss | GET /dashboard/saldo/betalingsmiddelen; /dashboard/saldo/openposten; /dashboard/winstverlies; Q | exact source dashboard DTOs; BK011 partial, K04 |
| app_payment_balances_details | GET /saldo/betalingsmiddelendetails; Q | source balance DTO; BK011 partial, K04 |
| app_open_items_creditors/debtors | POST /openposten/crediteuren; POST /openposten/debiteuren; Q | OpenPostenListRequestDto → OpenPostenPagedResponseDto; BK009, K13 |
| app_open_items_details | GET /openposten/details/{relation_id}/{invoice_number}; Q | RelationId32 + literal invoice string → OpenPostDetailsDto; BK009, K13 |
| app_open_items_reminder/write_off | POST /openposten/aanmaning; POST /openposten/wegboeken; C | source reminder DTO / OpenPostWegboekingDto → source response; BK009, K13 |
| app_vat_codes_purchase/sales | GET /btwcodes/inkoop; GET /btwcodes/verkoop; Q | source code-list DTO; master-data selection only, CFG003 partial, K10 |
| app_cost_centres_list / rgs_get | GET /kostenplaatsen; GET /rgscodes/{id}; Q | source DTOs; CFG007/009 partial, K10 |
| app_email_templates_get | GET /emailsjablonen/{id}; Q | EmailSjabloonDto including subject/body; BE007 partial, K10 |
| app_administrations_list/accountant_list/details_get/details_update | GET /administraties; GET /administraties/accountant; GET/PUT /administraties/uwgegevens; Q/C | source administration DTOs; BE011/008 partial, K14; no generic settings editing |
| app_administration_settings_get | GET /settings/administratie; Q | AdministratieSettingsDto four declared flags; BE003/CFG007/008/009/010 partial, K14 |
| app_credits_balance | GET /credits/saldo; Q | source balance DTO; BK020 partial, K14; no purchase operation |

The shorthand root/detail in this table refers only to the literal root in that row. At implementation the canonical registry stores fully expanded paths; a caller cannot substitute a resource. Each separate action has its own generated input/output JSON schema and effect metadata. Ancillary picker constants, source-map ambiguities and incomplete response schemas remain unavailable until source admission is complete, rather than acquiring a generic proxy tool. Do not add feedback, push registration, in-app purchases or membership administration merely because clients exist in the APK.

### Technical-only registrations and internal authentication

Local technical tools: app_capabilities (frozen registry/admission list, no login); app_receipt_get (dispatch ID → private typed provider-result receipt); app_session_status (nonsecret local state/confirmed context); app_source_import (explicit configured-inbox basename → immutable artifact receipt). app_archive_download and app_sales_invoices_download/app_quotes_download explicitly persist bounded binary artifacts; byte capture is a command followed by a receipt query, even though provider GET is a query.

Host staging copies a chosen file into a protected configured inbox and supplies its actual basename. Import itself computes bytes/hash and optional expected-hash comparison; no manual hash requirement or arbitrary path/ACL argument. Upload consumes the selected immutable artifact, not an automatically chosen source. No filename shortening, OCR/classification, bookkeeping interpretation or automatic scan is performed.

Login/two-factor/renew/userinfo are internal named auth registrations. Credentials and secret-bearing responses belong exclusively to the process session manager; they never enter ordinary receipts, logging or MCP results. Current-context read is projected through a nonsecret session-state model. Explicit context selection may target only configured allowed administration aliases and waits for existing leases to drain; it is never an implicit query action. Logout is an explicit host-auth action with a source-backed route, but its provider-wide revocation scope is unproved: default shutdown closes local resources and drops secrets, without claiming provider logout or automatically revoking other processes.

No technical tool is a prepare/approve/book/repair/source-selection workflow. It does not compute balances/VAT, choose suppliers/accounts, decide payment completeness, or call several business endpoints to complete an invoice lifecycle. Explicit provider bulk/billing/calculation commands are forwarded as one declared operation.

### Coverage admission for every function and configuration type

The evidence matrix remains the detailed 57-group/23-feature crosswalk. This table binds every ID to the new server admission boundary; no actual account values are reproduced.

| Inventory IDs | Design admission |
| --- | --- |
| BK001/BK002/BK003/BK008 | Named mutation endpoints; caller supplies provider kind/rows/IDs; no local booking workflow or mandatory REST check |
| BK004 | Bank-row read/comment/delete and source-bound mutation create fields; consumption semantics not inferred; rule/reprocess/export actions remain gaps |
| BK005/BK006/BK007/BK011 | Native App report/dashboard/ledger endpoints where declared; no locally recreated financial reports or export parity |
| BK009 | Open-item list/details/reminder/write-off endpoints; no local payment graph/completeness judgment |
| BK010/BE006 | GAP: asset/depreciation/register/schedule contracts missing, no tool placeholder |
| BK012/BK013/BK014 | GAP: VAT/ICP/filing/history/payment operations missing |
| BK015 | Named archive endpoints; restore/undo and unproved association namespaces remain gaps |
| BK016 | GAP: no named preview operation established |
| BK017/BK018/BE005/FA013/RE003 | GAP for automatic import rules/file-import workflows; individual entry/product/relation CRUD does not substitute |
| BK019 | Per-file scan endpoint only; GAP for automatic-feature activation/interlocks/reporting |
| BK020 | Credits read/folder-inbox metadata only; GAP for quota/purchase or automatic-processing guarantee |
| FA001/FA002/FA004/FA011 | Named invoice/output/incasso source-backed operations; queue reversal/transmission and incomplete schemas stay gated |
| FA003 | GAP: unconfirmed e-invoicing feature; no invented registration |
| FA005/FA010/FA012 | Quote/rows/progress/status/appointment/convert/mail endpoints; attachment target kinds must be proven before enabling that mapping |
| FA006 | Standard invoice definition CRUD, not layout templates or unspecified generation |
| FA007/FA015 | Subscription CRUD/provider bulk billing; scheduling effects described, not recreated locally |
| FA008/FA009/FA014 | Product/group/unit CRUD and explicit cascade flags, without price/discount choices |
| RE001/RE004 | Relation endpoint fields including archive/recognition permissions; no automatic identity/default choices |
| RE002 | Membership endpoints only; GAP for newsletter/group-send administration |
| UR001/UR002/UR004/UR005 | Hours/project/activity/tariff/billing/settings endpoints; no local invoice-generation logic |
| UR003 | Hours filter data only; GAP for exact native report aggregation/export |
| BE001 | Ledger/group endpoints; no bookkeeping category judgment |
| BE002 | GAP: dedicated opening-balance contract |
| BE003 | Specific read flags only; see configuration mapping |
| BE004 | Incasso connection-availability read only; GAP for bank-feed configuration |
| BE007 | Email-template detail read/picker evidence only; GAP for template layout/edit/copy |
| BE008 | Context/own-details read/update partial; GAP for user/security/MFA/SMTP administration |
| BE009 | GAP: auditfile/software exports |
| BE010 | GAP: closed-period/budget management |
| BE011 | Administration lists/own details and explicitly guarded context selection; no namespace equivalence |
| BE012 | Custom field labels read and relation values; GAP for definition setters |
| BE013 | GAP: API token management; auth session lifecycle is different |

Configuration admission: CFG001/012/016 are nonsecret projections from userinfo; CFG002 is source VAT-mode/settings reads only; CFG003 is code-list read, not activation; CFG007/008/009/010 have specific administration flags (sales-specific semantics of the last remain unproved). CFG004/005/006(global format)/013/014/015/017/022/023 have no admitted setting read/write route. CFG011 has explicit per-mail UBL fields only. CFG018 uses hours-billing GET/POST settings. CFG019 uses provider subscription bill-now directVerwerken; CFG020 per-subscription fields; CFG021 explicit product-cascade request. No missing setter is synthesized from a read flag, and per-action fields are not global configuration tools.

All gaps retain the matrix's concrete F01–F16 follow-ups. Registration expansion requires new source/schema/effect evidence and review; it does not silently use REST, native UI or a locally invented calculation.

## Explicit gated ancillary registrations

- app_incasso_form_data: GET /api/v4/incassobestand/formdata → IncassoBestandFormDataDto, query. app_incasso_connection_status: GET /api/v4/incassobestand/hasincassokoppeling → GenericBoolDto, query. app_incasso_send: POST /api/v4/incassobestand/send with IncassoBestandCreateDto → source response, command with possible external transmission. Concrete async CIL exists; send response/effect admission remains gated. These are not bank-feed configuration or invoice debit metadata.
- app_archive_mutation_attachments: GET /api/v4/bestanden/bijlagen/{argument}, source GetMutatieBijlagen. Candidate only until parameter namespace/response schema are fixed; method name alone does not register a tool.
## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-01 | Imp | Bind named endpoint families and schemas to the accepted App-v4 strategy and all inventoried functional/configuration groups. |
