<!-- pgmcp:v1 id=reference pv=1.0.0 pf=Q4Tx8SxSHKiKF_yz sf=WI5iXHBKVOU91bYE -->

# APK 3.9.0 App-v4 contract catalogue

**Status:** RESEARCH EVIDENCE — STATIC CONTRACTS, NOT EXECUTION AUTHORITY  
**Version:** 1.0  
**Last Updated:** 2026-11-01

## Purpose

Record screened static method/path/DTO evidence across the mobile client's functional groups, without redistributing the package, decompiled implementation or private observations.

## Scope In

The owner-supplied Android 3.9.0 package, its four first-party managed assemblies and the complete Core Clients/Endpoints catalogue; static contract metadata and bounded negative evidence.

## Scope Out

No APK execution, installation, interception, credential access, account request or new runtime test. Static declarations do not prove current service support, permissions, side effects, retry safety or parity with every web function.

## Sources

- [Official mobile app description][src-1]
- [Official store release history][src-2]
- [Community App-v4 snapshot (separate evidence)][src-3]
- [Managed assembly-store format reference][src-4]

[src-1]: <https://www.e-boekhouden.nl/app>
[src-2]: <https://apps.apple.com/nl/app/e-boekhouden-nl/id1078225120>
[src-3]: <https://github.com/kozmoz/e-boekhouden-APP-API-v4/blob/6ca849003ed196ca10877d8854644e9c38cf3145/swagger.openapi.json>
[src-4]: <https://github.com/dotnet/android/blob/c92702619f5fabcff0ed88e09160baf9edd70f41/Documentation/project-docs/AssemblyStores.md>

## API Reference

### Source identity and evidence boundary

The supplied base package identifies Android package eboekhouden.nl, versionName 3.9.0, versionCode 3900001. Its SHA-256 is CEF93CB505479F68834054408E5140F06B388A69B656452272ABD9538F010216. Current bytes match the previously preserved manifest/extraction evidence. This is owner-supplied source identity, not full publisher-signature verification.

The package is Xamarin/.NET, not a Java Retrofit API client. Its assembly-store manifest names exactly four first-party EB assemblies: Android, Dto, Core and Core.Ui. Expanded source-scope counts are metadata inspection counts, not account records. Already extracted images were read as PE metadata/CIL, never loaded or executed. Core SHA-256: 1424CE466B78233A97D685D09369F096E3644AF360F2B6FF0827D8472192E046; Dto SHA-256: 0659B11C0C995A7F34BFF464137E905E88384EEEF6F3786F3744D4A012205518. Type catalogues of all four images were inspected; API client definitions are in Core, UI pages in Core.Ui and platform handler code in Android.

Private immutable evidence retains assembly identity, method RVA/file offset/CIL and DTO property signatures/Json.NET attributes. The expanded Core evidence contains 516 method records across 117 endpoint/client/helper types; the direct-client extraction selects 217 method records across 41 client types, and the DTO catalogue has 229 property-bearing types/1377 properties. These are not unique HTTP routes or calls: overloads, shared method bodies, async wrappers and generic pagination occur. For example relation/member GetItems share a method RVA. Empty routeAtoms or an interface declaration alone is not path evidence; concrete getters, caller and HTTP wrapper are followed per operation.

No vendor implementation, raw Swagger examples, APK/assembly/parser dependency, private filename/path, account identifier or record value is committed. Private evidence is available for authorized independent review. This catalogue publishes factual interface metadata and original analysis only.

### K01 — Production family and authentication

Complete static binding chain: EnvironmentConfigurations..cctor RVA 917040 loads https://appapi.e-boekhouden.nl/api/ at CIL offset 0x32, constructs EnvironmentConfiguration at 0x38 and assigns Production at 0x3d. That constructor stores the supplied BaseUrl. Endpoints..cctor RVA 914132 selects Production at 0xc and stores CurrentEnvironment at 0x11. Endpoints.get_BaseUrl RVA 914001 supplies v4/. ClientBase.CreateHttpClient's async body RVA 933292 obtains CurrentEnvironment.BaseUrl at 0x14d/0x152 and sets HttpClient.BaseAddress at 0x15c. Endpoint getters append resource paths to v4/.

Thus this APK's default configuration targets the same App-v4 origin/family as the community capture and historical App helpers. It is additional client evidence for that family, not a third independent API. It proves default compiled configuration, not a live host response or that every runtime environment is identical. Official REST v1 remains a separate family/authentication contract.

AuthClient maps POST /api/v4/auth/login, /logintwofactor, /renew, /switch/{argument}, /logout and GET /api/v4/auth/userinfo. Login/renew/switch DTOs and success-handling exist statically; no newly tested 2FA, refresh, logout or switching claim follows. Earlier statements that logout completion was unestablished remain valid as historical runtime limits; the route is now statically identified. The switch argument namespace and safe renewal/replay behavior still need contract validation. Do not copy client automatic refresh/retry behavior into a financial connector without an explicit uncertainty contract.

### K02 — Mutations, source bank rows and identity

All paths below are relative to /api/v4. MutatiesClient: POST /mutaties/filter; GET /mutaties/{id}; POST /mutaties; PUT /mutaties; DELETE /mutaties/{id}; GET /mutaties/nextmutatiedata/{argument}; GET /mutaties/nextmutatiedata/{argument}/afschriftregel/{id}; GET /mutaties/GetOmschrijvingEnRekening?factuurnummer={value}&relatieId={id}; GET /mutaties/btwperregel. The overridden PaginationEndpoint getter supplies the filter route for inherited/shared GetItems.

Create (RVA 927368) invokes ClientBase.Post<CreateMutatieDto,MutatieDetailsDto>. GetNewMutatieDataFromAfschriftRegel (RVA 927452) invokes ClientBase.Get<NextMutatieDataDto> and composes the afschriftregel suffix. CreateMutatieDto explicitly has afschriftRegelId and bestanden in addition to id(Int64), mutatieNummer(Int32), factuurNummer, datum, soort, relatieId, grootboekRekeningId/code, bedrag, boekstuk, omschrijving, isInclusiefBtw, termijnInDagen and mutatieRegels. UpdateMutatieDto has the common header/row fields, but no corresponding declared source-bank-row field. CreateMutatieRegelDto has index, tegenRekeningId, btwCode, kostenplaatsId, bedrag, btw, factuur, relatieId and omschrijving.

The compiled MutatieSoort enum contains numeric members 0–7 with generated names; their business meanings are not established by those names alone. Visible number and Int64 internal/version ID remain distinct. Historical read/narrow-update evidence shows that an App update can replace the internal ID and normalize invoice-number whitespace. It does not validate arbitrary mutation kinds, paid updates, computed fields or independent row text.

A bank-source create contract is now a concrete static candidate, stronger than the earlier incomplete community catalogue. Consumption/removal of the pending bank row, matching, atomicity, duplicate prevention and retry behavior have NOT been executed or proved. Creating an unrelated payment remains different from source-row-bound processing.

### K03 — Pending bank rows

AfschriftRegelClient declares GET /afschriftregels, GET /afschriftregels/{id}, PUT /afschriftregels/opmerking and DELETE /afschriftregels/{id}. DTOs: AfschriftRegelsResponseDto.afschriftRegels, AfschriftRegelDto(id, importDatum, boekDatum, rekeningNummer, bedrag, omschrijving, opmerking), UpdateAfschriftRegelOpmerkingDto(id, opmerking). A list/detail/comment/delete contract is not an automatic import-rule editor or an uploaded bank-statement wizard. Processing candidate linkage is K02, not DELETE. No matching/consumption/restore semantics inferred from successful HTTP status.

### K04 — Financial reports and ledger views

BalansClient.GetOverzicht: POST /balans, BalansRequestDto(endDate, showGroups) → BalansOverzichtDto with groups/totals. WinstEnVerliesClient.GetOverzicht: POST /winstverlies/overzicht/ with startDate/endDate/showGroups and optional comparison dates → WinstEnVerliesOverzichtResponseDto.

GrootboekOverzichtClient: POST /grootboek/overzicht with page/startPage/pageSize/grootboekId/period → PagedGrootboekOverzichtDto including items/total/saldo/openingsSaldoRegel/period; GET /grootboekrekeningen/{id} and /{id}/saldo. DashboardClient GET /dashboard/saldo/betalingsmiddelen, /dashboard/saldo/openposten, /dashboard/winstverlies; SaldoClient GET /saldo/betalingsmiddelendetails.

These are provider-calculated report/read contracts, not a proposal to reproduce financial reports locally. No Excel/PDF/CSV report-export route, full liquidity forecast, complete column-balance parity or report permission guarantee is established by these methods. Client paging responses expose currentStartPage/currentPage/pageSize/hasMoreRows/items; those fields are contract metadata, not proof of complete runtime coverage.

### K05 — Archive content, folders, search and linking

BestandenClient method/path metadata:

| Operation | Static method/path | DTO/qualification |
| --- | --- | --- |
| Browse | GET /bestanden; GET /bestanden/{directoryId} | DirectoryDto with nested directories/files, parent, childCount, isMailEnHerkenInbox |
| File metadata/content | GET /bestanden/bestand/{id}; GET /bestanden/download/{id} | FileDto; GetFile wrapper for binary download |
| Upload | POST /bestanden/upload | UploadFileRequest(fileName,data,directoryId,scan); response originalFileName/saved/scanned/errorMessage/file |
| Rename/move metadata | PUT /bestanden | UpdateFileDto(id,naam,directoryId); name-only historical proof does not prove safe directory changes |
| Folder create/update | POST, PUT /bestanden/directory | CreateUpdateDirectoryDto(id,parentDirectoryId,naam,setAsMenHInbox) |
| File/folder deletion | DELETE /bestanden/bestand/{id}; DELETE /bestanden/{id} | Different targets; no undo/restore contract established |
| Search | POST /bestanden/search | BestandenSearchRequestDto.searchTerm → directories/files; differs from prefixless community GET |
| Linked items | POST /bestanden/gekoppeld | Request target domain and returned association reference remain separate |
| Link/unlink | POST /bestanden/koppel; DELETE /bestanden/koppel/{id} | CreateFileKoppelDto(fileId,soort,koppelId); runtime proof only for the historically selected target domain |
| Move/delete batch | POST /bestanden/bulkMove; POST /bestanden/bulkDelete | BulkMoveFolderDto(moveToFolderId,itemsToMove), bulk action IDs |
| Scan | POST /bestanden/scan/{id} | Async ScanFile body calls HttpClient.PostAsync; success/Boolean interpretation is client behavior |
| Mutation attachments | GET /bestanden/bijlagen/{argument} | Parameter namespace and full reverse graph need separate validation |

FileDto contains id/naam/datum/directoryId/scanStatus, not a proven restore operation. KoppelSoortDto's generated enum values 0–3 alone do not establish their target meanings. Source metadata supports a Mail & Herken inbox flag, not proof that recognition is active or that Autopilot can be enabled. Historical selected list/download/upload/link/rename and shared-target retention outcomes remain bounded historical runtime evidence, not general deletion/move/scan permissions or retry safety.

### K06 — Sales invoices and separate output effects

FacturenClient: POST /facturen/filter; GET /facturen/{id}; POST /facturen; PUT /facturen; DELETE /facturen/{id}; GET /facturen/nextfactuurdata, /facturen/settings, /facturen/{id}/download and /facturen/{id}/maildata. Provider calculations are POST /facturen/calculatetotals, /facturen/calculateprijsexcl and /facturen/calculateprijsincl.

Output/queue/processing methods are separate: POST /facturen/mail; POST /facturen/bulk/email; POST /facturen/bulk/setmail; POST /facturen/bulk/setincasseren; POST /facturen/bulk/verwerk; POST /facturen/bulk/delete; GET /facturen/emailencount. The queue setter's inverse/unqueue semantics are not established merely by its name or an IDs-only DTO.

CreateFactuurDto/UpdateFactuurDto carry relation, string number, date, terms, template IDs, isInclusiefBtw, kenmerk/factuurTekst, printFactuur/mailFactuur/incasseren/verwerkenInBoekhouding, invoice rows and optional incassoGegevens/boekhoudGegevens. Update includes rowsToAdd/Update/Delete using the actual Dutch JSON property names regelsToAdd/regelsToUpdate/regelsToDelete. FactuurRegelDto includes product/unit/code/description/account/cost-center/quantity/prices/VAT and korting/kortingIsPerc. FactuurEmailRequestDto includes target ID, factuurUbl, sender/recipient/CC/BCC/subject/body and attachments.

GetMailData is a read, BulkSetMail is a queue-intent command, Mail/BulkEmail are outbound-mail-intent commands; do not merge them into a single generic send/read flag. None was executed in this research. Exact timing, idempotency, queue reversal and processed-document restrictions require provider validation, not guessed client semantics.

### K07 — Quotes, progress and quote-to-invoice

OffertesClient: POST /offertes/filter; GET /offertes/{id}; POST /offertes; PUT /offertes; DELETE /offertes/{id}; POST /offertes/duplicate; GET /offertes/nextdata, /offertes/{id}/download, /offertes/{id}/maildata, /offertes/{id}/restbedrag; POST /offertes/mail and /offertes/createfactuur.

Quote rows: POST/PUT /offerteregels; DELETE /offerteregels/{id}; PUT /offerteregels/bulk. Progress: GET/POST/PUT /offertes/{quoteId}/voortgang and GET/DELETE its /{progressId} detail. Appointments: GET/POST/PUT /offertes/{quoteId}/afspraken and DELETE its /{appointmentId}.

CreateFactuurFromOfferteRequestDto has offerteId, offerteRegelIds, totaalBedrag and percentage: partial/selected-row conversion is a static candidate, not only a whole-quote copy. CreateUpdateOfferteVoortgangDto has id, voortgangsoortId, onderwerp/body; details additionally carry date/user/quote references. Independent status/progress-type management is K10. Quote attachment support requires K05 target-domain mapping: do not assume a numeric link kind from the UI tab or enum ordinal. No quote/invoice/mail/progress operation was executed.

### K08 — Subscriptions and standard invoices

AbonnementenClient: POST /abonnementen/filter; GET /abonnementen/{id}; POST/PUT /abonnementen; DELETE /abonnementen/{id}; GET /abonnementen/nextdata and /abonnementen/facturerenFormData; GET /abonnementen/countwithincasso/{relationArgument}; POST /abonnementen/bulk/delete and /abonnementen/bulk/factureer.

AbonnementDetailsDto includes relation, start/end/expiration dates, per, terms, invoice rows/templates, printFactuur/mailFactuur/incasseren/autoVerwerk and geenFactuur; UpdateAbonnementDto has separate row-change lists. AbonnementFacturerenDto has directVerwerken, betalingsTermijn, factuurDatum, expirationPeriod, grootboekRekeningId and type. These expose billing cadence/hold/processing intent without establishing scheduling timing, actual sending or all web selection semantics.

StandaardFacturenClient: POST /standaardfacturen/filter, GET /standaardfacturen/{id}, POST/PUT /standaardfacturen, DELETE /standaardfacturen/{id}. StandaardFactuurDetailsDto carries name/templates/mode/rows/totals. It is not an invoice-layout template. Neither list CRUD nor a create response proves a separate generate-invoice or scheduled-mail operation.

### K09 — Products and subscription cascade

ArtikelenClient: POST /artikelen/filter; GET /artikelen/{id}; POST/PUT /artikelen; DELETE /artikelen/{id}; POST /artikelen/bulk/delete. ArtikelDto covers code/omschrijving/unit/VAT/ledger/cost-center/group, purchase/sales prices, inclPrijsIsLeading, actief and inVoorraad. ArtikelUpdateDto explicitly wraps artikel plus cascade and cascadePriceOnly. Those are two cascade choices, not an instruction to modify subscriptions automatically. No bulk CSV/XLS/XLSX product-import or its duplicate/overwrite workflow is found in the inspected client methods. CRUD is not import parity.

### K10 — Reference and configuration entities

Concrete client CRUD families: ArtikelGroepenClient GET /artikelgroepen and /{id}, POST/PUT /artikelgroepen, DELETE /{id}; EenhedenClient analogous /eenheden; GrootboekenClient analogous /grootboekrekeningen; RekeningGroepenClient analogous /rekeninggroepen. OfferteStatusClient GET/POST/PUT /offertestatussen and DELETE /{id}; VoortgangSoortClient GET/POST/PUT /voortgangsoorten and DELETE /{id}.

BtwCodesClient GET /btwcodes/verkoop and /btwcodes/inkoop. KostenplaatsenClient GET /kostenplaatsen; RgsCodeClient GET /rgscodes/{id}. Additional pickerlist paths occur in Endpoints constants and generic PickerItemClient. A constant alone is a candidate, not a proved caller/method mapping; no missing write/create operation is inferred from a picker.

No standalone invoice/quote/dunning-layout-template editor client is established. EmailSjablonenClient.GetDetails (RVA 924676) calls ClientBase.Get<EmailSjabloonDto> at GET /emailsjablonen/{id}; the parameter is Int32 id. EmailSjabloonDto declares id, naam, cc, bcc, subject and body. Endpoint constants also describe invoice/quote/dunning picker lists. Full template creation, layout editing and copy-base workflow need separate evidence.

### K11 — Relations and mailing membership

RelatiesClient POST /relaties/filter, GET /relaties/{id}, POST/PUT /relaties, DELETE /relaties/{id}, POST /relaties/bulk/delete; GET /relaties/customfields and /relaties/nextrelatiedata; GET/POST /relaties/{id}/mailinglijst. Validation/address lookup candidates include GET /relaties/kvk/{query}, /relaties/kvkvestiging/{id}/adres, /relaties/{argument}/{argument} and /iban/validate/{value}; their parameter/permission/provider semantics are not execution proof.

RelatieDetailsDto includes company/private identity, code/name/contact/address and separate postal fields, invoice/reminder emails, bank/mandate/tax fields, standaardGrootboekRekeningId, betalingsTermijnDagen, inactief/geenEmail/notitie, customFieldValues and explicitly menHAllowMail/menHAllowHerken. These two permissions are absent from the inspected official REST relation schema. Custom field labels are read through CustomRelatieFieldsResponseDto(index,name); values through index/value. No label-definition setter, general relation spreadsheet import or newsletter-send client is established. Mailing-list membership is not newsletter delivery.

### K12 — Hours, billing, project/activity/rate management

UrenClient POST /uren/filter, GET /uren/{id}, POST/PUT /uren, DELETE /uren/{id}, GET /uren/nextdata and POST /uren/factureren. FactureerUrenRequestDto carries uurIds. FactuurInstellingenClient GET /factuurinstellingen and POST /factuurinstellingen through PostWithBoolResult: its update name does not imply HTTP PUT. DTO fields: uurEenheidId, kmEenheidId, factuurSjabloonId, regelTekst, betalingsTermijn, perPost/perEmail/incasseren/verwerken. Billing selection, generated outputs and mail/accounting side effects need independent checks.

ProjectenClient GET /projecten/{id}, POST /projecten/filter, POST/PUT /projecten, DELETE /projecten/{id}; ActiviteitenClient analogous /activiteiten; ProjectAfwijkendeTarievenClient GET /projectafwijkendetarieven/{id}, GET /projectafwijkendetarieven?ProjectId={id}, POST/PUT root and DELETE /{id}.

UurDto: id, datum, medewerkerId/projectId/activiteitId, nullable aantalUren/aantalKilometers/opmerkingen, reference display text and invoerDatum. Generated Json.NET null-omission and UTC settings are client serialization evidence, not arbitrary null-to-zero permission. Historical narrow create/edit and receipt-owned synthetic cleanup exist, not general delete authorization. Filtering uses period/employee/project/activity/search/filterType/nietGefactureerd plus paging. No separate annual/project/activity report export or guarantee of exact web aggregation is established by the registration filter.

### K13 — Open items and reminders

OpenPostenClient POST /openposten/crediteuren and /debiteuren with OpenPostenListRequestDto(per,relatieId,includePaid,searchTerm,sort/paging); GET /openposten/details/{relationId}/{invoiceNumber}; POST /openposten/aanmaning and /openposten/wegboeken.

OpenPostWegboekingDto carries date, Decimal amount, description, target ledger, openPosten IDs and openPostType; it is a write-off contract, not arbitrary payment matching. The compiled detail method parameters are relatieId(Int32), factuurNummer(String) and a cancellation token; the target is not a demonstrated visible-mutation-ID argument. OpenPostDetailsDto contains reminders and comments; it does not declare a complete reverse payment-mutation graph. MutatieRegelDetailsDto.openPostModel has invoice/relation/amount/paid fields, but their presence does not validate a complete editable paid-mutation contract. Native manual paid-edit evidence cannot be promoted into this API proof. Reminder email is an external effect; never call it to test availability.

### K14 — Administration, flags and residual surface

AdministratieClient GET /administraties, /administraties/accountant, /administraties/uwgegevens; PUT /administraties/uwgegevens. The latter DTO is business/contact/tax/bank/account identity data, not all bookkeeping settings or user permissions. SettingsClient GET /settings/administratie returns only useKostenplaatsen, omschrijvingPerMutatieregel, rgslevel, standaardBetalingsTermijn. UserInfoDto.userSettings exposes useMemoriaal/useBoekstuk/useVoorraad. Those reads are not setters. Invoice settings reads are K06; hours-billing settings have their own K12 GET/POST contract. CreditsClient GET /credits/saldo is not a storage-quota or purchase contract.

Other compiled clients include feedback, push-message subscription and in-app purchases. They are outside the functional accounting inventory; presence is not a proposed integration or purchase authority. The complete inspected Core Client/Endpoints list has no corresponding client family for VAT/ICP filing or submitted-return/payment history, fixed assets/depreciation, opening-balance administration, automatic bank-import rules, statement/product/relation spreadsheet import, auditfile/software-report export, closed periods, budget scenarios, Autopilot activation, full user/token/security administration or archive restore. This is bounded negative evidence over this package snapshot, not universal absence from the provider or its web backend.

For each gap the functional matrix records a concrete next evidence step. Web UI availability and store feature descriptions do not supply missing method/path/DTO contracts. No missing report is silently replaced with locally invented accounting logic.

## Related Documents

- [Earlier bounded App assessment](<app-api-v4-assessment.md>)
- [Historical runtime and retained tests](<toolkit-preservation.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-01 | Imp | Expand static inspection from hours to all mobile client and endpoint groups. |
