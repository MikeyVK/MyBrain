<!-- pgmcp:v1 id=reference pv=1.0.0 pf=Q4Tx8SxSHKiKF_yz sf=WI5iXHBKVOU91bYE -->

# e-Boekhouden API documentation and capability catalogue

**Status:** REFERENCE FINDINGS — official documents inspected; no live integration proof  
**Version:** 1.1
**Last Updated:** 2026-10-30

## Purpose

Index the discovered official public API contracts and identify the boundary around the owner's mutation and imported-bank-row workflow.

## Scope In

REST v1 resource groups, historical SOAP 5.7 reference and WSDL, official user-workflow evidence, authentication, limits and documented gaps, inspected on 2026-10-30.

## Scope Out

No credentials, live administration access, bookkeeping writes, tax filing, implementation or claim that undocumented endpoints cannot exist.

## Sources

- [Official API landing page][src-1]
- [REST interactive documentation][src-2]
- [REST raw OpenAPI v1][src-3]
- [SOAP 5.7 manual — Dutch][src-4]
- [SOAP 5.7 manual — English][src-5]
- [SOAP WSDL and inline XSD][src-6]
- [SOAP service and operation-help index][src-7]
- [Official FAQ with SOAP manual links][src-8]
- [Official bookkeeping user manual][src-9]
- [Official explanation of reconciliation][src-10]

[src-1]: <https://www.e-boekhouden.nl/koppelingen/api>
[src-2]: <https://api.e-boekhouden.nl/scalar/>
[src-3]: <https://api.e-boekhouden.nl/openapi/v1.json>
[src-4]: <https://cdn.e-boekhouden.nl/handleiding/Documentatie_soap.pdf>
[src-5]: <https://cdn.e-boekhouden.nl/handleiding/Documentation_soap_english.pdf>
[src-6]: <https://soap.e-boekhouden.nl/soap.asmx?wsdl>
[src-7]: <https://soap.e-boekhouden.nl/soap.asmx>
[src-8]: <https://www.e-boekhouden.nl/veelgestelde-vragen>
[src-9]: <https://cdn.e-boekhouden.nl/handleiding/Handleiding_boekhoudpakket.pdf>
[src-10]: <https://www.e-boekhouden.nl/boekhoudtermen/afletteren>

## API Reference

### Complete REST v1 operation inventory

Inspected on 2026-10-30. The public REST v1 OpenAPI 3.1.1 document contains 24 business paths and 39 operations across 12 business groups. Two additional GET routes serve Swagger documentation. This is the complete path/method inventory of that retrieved specification, not a claim about private or undocumented APIs.

| Group | Documented methods and paths | Operations |
| --- | --- | --- |
| Session | POST, DELETE `/v1/session` | 2 |
| Administration | GET `/v1/administration`; GET `/v1/administration/linked` | 2 |
| CostCenter | GET, POST `/v1/costcenter`; GET, PATCH, DELETE `/v1/costcenter/{id}` | 5 |
| EmailTemplate | GET `/v1/emailtemplate` | 1 |
| Invoice | GET, POST `/v1/invoice`; GET `/v1/invoice/{id}` | 3 |
| InvoiceTemplate | GET `/v1/invoicetemplate` | 1 |
| Ledger | GET, POST `/v1/ledger`; GET, PATCH `/v1/ledger/{id}`; GET `/v1/ledger/{id}/balance`; GET `/v1/ledger/balances` | 6 |
| Member | GET, POST `/v1/member`; GET, PATCH `/v1/member/{id}` | 4 |
| Mutation | GET, POST `/v1/mutation`; GET `/v1/mutation/{id}`; GET `/v1/mutation/invoice/outstanding` | 4 |
| Product | GET, POST `/v1/product`; GET `/v1/product/groups`; GET, PATCH, DELETE `/v1/product/{id}` | 6 |
| Relation | GET, POST `/v1/relation`; GET, PATCH `/v1/relation/{id}` | 4 |
| Unit | GET `/v1/unit` | 1 |

`GET /swagger` and `GET /swagger/{catchAll}` are the two documentation routes. No PUT operation is present. PATCH is confined to cost centers, ledgers, members, products and relations; entity DELETE is confined to cost centers and products. No mutation or invoice update/delete route is declared.

**Sources:**

- [Raw OpenAPI v1][api-1-src-1]

[api-1-src-1]: <https://api.e-boekhouden.nl/openapi/v1.json>

### Mutation creation and retrieval

The bookkeeping contract is `POST /v1/mutation` (`CreateMutation`), not merely a file upload or an invoice-generation call. Its schema requires `type`, `date` and `ledgerId`; validation descriptions impose additional conditional obligations. It returns HTTP 201 with the created mutation ID. Its declared error responses are 400 and 401.

| Mutation type | Meaning |
| --- | --- |
| `1` | Invoice received — purchase invoice |
| `2` | Invoice sent |
| `3` | Invoice payment received |
| `4` | Invoice payment sent — supplier payment |
| `5` | Money received |
| `6` | Money sent |
| `7` | General journal entry |

These values are strings in the shared `MutationType` enum; the vendor's example shows a number. A synthetic contract test and later authorized proof must settle client serialization rather than assuming examples override schema.

| Area | Relevant documented fields / restrictions |
| --- | --- |
| Header | `date`, `ledgerId`, `relationId`, `invoiceNumber`, `entryNumber`, `description`, `termOfPayment`, `inExVat`, `paymentReference`, `checkPaymentReference` |
| Detail rows | Up to 500; row schema requires `vatCode` and `amount`. Additional row fields include `ledgerId`, `relationId`, `invoiceNumber`, `costCenterId`, `description` and conditional `vatAmount` |
| Ledger identity | `ledgerId` is the API ID; it is not the ledger `code`. Resolve through GET ledgers. Row ledgers for types 1, 2, 5 and 6 cannot be FIN, CRED or DEB; type 7 differs |
| Payment association | Row `invoiceNumber` is required for types 3 and 4; row `relationId` is available. These fields associate a newly created invoice-payment mutation with an invoice |
| Duplicate checks | `checkPaymentReference=true` requests uniqueness validation for `paymentReference`. Duplicate invoice and relation/invoice errors are also documented. These are not a general idempotency-key contract |
| Unsupported inference | Request has no documented existing-mutation ID, bank-import-row ID, archive-file ID or attachment upload. Example `Id:null` is not a documented update/upsert mechanism |

`GET /v1/mutation` filters by type, ID, description, invoice number and date and has limit/offset pagination. Its list gives summary fields; GET by ID supplies rows and VAT totals. This does not establish visibility into unprocessed imported bank rows.

**Sources:**

- [OpenAPI mutation contracts][api-2-src-1]

[api-2-src-1]: <https://api.e-boekhouden.nl/openapi/v1.json>

### Open items, payments and invoice-module distinction

`GET /v1/mutation/invoice/outstanding` requires `credDeb=C` for creditors or `D` for debtors. It accepts invoice-number and pagination filters and returns mutation ID, relation ID, total, paid and outstanding amounts.

The response deprecates `invoiceNumber` in favor of `mutationId` and `relationCode` in favor of `relationId`. However, the current payment-row request still names `invoiceNumber` and has no `mutationId` input. Keep both observed contracts distinct; do not invent a replacement field.

`POST /v1/invoice` creates an invoice with a template, items and optional print/email/direct-debit/bookkeeping options. It is not a documented received-supplier-PDF import endpoint. GET invoice results expose a shareable `urlPdfFile` for generated invoices. Optional outbound UBL/email attachments do not establish a general incoming-archive upload API. Providing the optional email object can send mail immediately; that side effect must not be an accidental part of research or a bookkeeping proof.

**Sources:**

- [OpenAPI invoice and outstanding contracts][api-3-src-1]

[api-3-src-1]: <https://api.e-boekhouden.nl/openapi/v1.json>

### Authentication, filtering and operational constraints

The REST quick start exchanges the secret API token through POST session with `accessToken` and a mandatory source identifier (maximum ten characters). The result contains `token` and `expiresIn`; DELETE session revokes the session token. Business operations declare the session security requirement and 401 responses.

There is an observed documentation inconsistency: quick-start and response prose show the session value directly in Authorization, while the security-scheme description shows `Bearer SESSION_TOKEN`. The scheme is typed `apiKey`, not OAuth2. Resolve the exact accepted header in a future owner-authorized, read-only proof; no credentials or session calls were used here. No token-level read-only scope, fine-grained bookkeeping permission model or fixed REST call ceiling was established from the inspected specification.

Most search endpoints use `limit` (default 100, range 1–2000) and `offset` (default 0, minimum 0). Dates use ISO spelling; supported filter syntax is documented in the specification introduction. The document lists structured error codes. No 429 response, webhook path, concurrency token or generic idempotency header is declared; absence is not an unlimited-service guarantee. Errors such as duplicate invoice, invalid ledger/VAT, expired session and closed-period invoice processing need distinct handling. The latter appears on the optional invoice-to-mutation path, not as a proven universal rule for every mutation type.

**Sources:**

- [OpenAPI introduction and security][api-4-src-1]

[api-4-src-1]: <https://api.e-boekhouden.nl/openapi/v1.json>

### Historical SOAP documentation and full operation inventory

The owner excludes SOAP from further integration work; it is not a fallback. The owner's report of a 2025 phase-out is not independently verified by a vendor announcement. The following inventory preserves what the retrieved historical documents declare, not a guarantee of present availability or support.

The public Dutch and English manuals identify SOAP version 5.7. The retrieved WSDL exposes 20 port-type operations and embeds its XSD; no imported XSD was declared.

| Area | Operations |
| --- | --- |
| Session / administration | `OpenSession`, `OpenSessionSub`, `CloseSession`, `AutoLogin`, `GetAdministraties` |
| Bookkeeping / invoices | `AddMutatie`, `GetMutaties`, `GetOpenPosten`, `AddFactuur`, `GetFacturen` |
| Ledgers / balances | `AddGrootboekrekening`, `UpdateGrootboekrekening`, `GetGrootboekrekeningen`, `GetSaldo`, `GetSaldi` |
| Relations / other lookups | `AddRelatie`, `UpdateRelatie`, `GetRelaties`, `GetKostenplaatsen`, `GetArtikelen` |

The manual distinguishes facturation-module `AddFactuur` from bookkeeping `AddMutatie` (physical PDF page 4). No `UpdateMutatie`, `DeleteMutatie`, archive upload or imported-bank-queue operation appears in either the 20-operation WSDL or the manual contents.

SOAP authentication uses a username and two security codes; a session ID and the second code accompany subsequent operations. The manual states that the manual takes precedence over WSDL optionality. Its GetMutaties section limits retrieval to the latest 500 and 5,000 calls per month (page 18); its error table states a general 10,000/day SOAP ceiling (page 43). Those SOAP limits are not asserted for REST. The FAQ says writes affect the administration directly and describes using a separate test account. It explicitly documents no webhooks and that changing the login password changes SecurityCode1.

**Sources:**

- [SOAP 5.7 Dutch][api-5-src-1]
- [SOAP 5.7 English][api-5-src-2]
- [WSDL][api-5-src-3]

[api-5-src-1]: <https://cdn.e-boekhouden.nl/handleiding/Documentatie_soap.pdf>
[api-5-src-2]: <https://cdn.e-boekhouden.nl/handleiding/Documentation_soap_english.pdf>
[api-5-src-3]: <https://soap.e-boekhouden.nl/soap.asmx?wsdl>

### Owner-priority capability boundary

The owner clarified that the target includes all imported bank rows, including supplier payments. Official REST v1 contracts and documented UI workflows cover different parts. The separate [App API v4 assessment](app-api-v4-assessment.md) records unofficial attachment and edit candidates; its evidence must not be conflated with the vendor contract:

| Owner task | Evidence | Boundary |
| --- | --- | --- |
| Register an incoming invoice | REST create mutation type 1 | Documented API creation, not executed |
| Associate a newly recorded supplier payment | REST type 4 with payment-row invoice number / relation | Not proof that an existing queued bank row is consumed or marked processed |
| Edit an existing bookkeeping mutation | Public user manual describes the pencil in ledger/mutation views | No corresponding official REST v1 operation; unofficial App v4 PUT is a candidate, not live proof |
| Process already imported bank rows | Manual PDF pages 8–11 describes automatic matching, the unprocessed-row list and manual processing | Queue API absent from official REST v1. App v4 describes GET list/detail; no processing contract established |
| Reprocess after invoices were entered later | Manual page 11, section 1.4.3: Boekhouden > Invoeren > Importeren > Alle regels opnieuw automatisch verwerken | A plausible minimal UI complement; current UI behavior still needs verification. The all-rows action can affect other pending rows and is not a scoped API preview |
| Attach a supplier PDF to a mutation | Manual page 27 describes files on new/existing mutations or from the digital archive | No official REST v1 upload/link endpoint; App v4 describes inferred upload/link routes |
| Prepare quarterly review | Date-filtered mutations, VAT totals, ledger balances and open creditor items are available | No documented VAT-return report or filing endpoint found; these data do not by themselves certify an accurate tax return |

A separately created payment mutation can duplicate an already booked bank payment or leave the imported row pending. Never create such a record merely to simulate the unproved queue-processing action. Creating counterentries to bypass missing update endpoints changes accounting meaning; no such policy is adopted here.

**Sources:**

- [REST contract][api-6-src-1]
- [Official bookkeeping manual][api-6-src-2]
- [Official explanation of reconciliation][api-6-src-3]

[api-6-src-1]: <https://api.e-boekhouden.nl/openapi/v1.json>
[api-6-src-2]: <https://cdn.e-boekhouden.nl/handleiding/Handleiding_boekhoudpakket.pdf>
[api-6-src-3]: <https://www.e-boekhouden.nl/boekhoudtermen/afletteren>

### Unofficial App API boundary

The [pinned App API v4 assessment](app-api-v4-assessment.md) examines a community reconstruction of iOS traffic. It describes file upload/link/unlink and PUT mutation operations missing from official REST v1, plus imported-bank-row GET routes. It does not establish bank processing. Its incomplete schemas, mixed search prefixes, uncertain ID mappings and absent repository license prevent treating it as a supported or automatically reusable open-source connector. No example financial data or account identifiers are copied. Archive-mail delivery is distinct from Scan & Herken and does not by itself establish attachment linkage.

### Coverage and limitations

The discovery covered the official API landing page; linked REST Scalar UI and its raw OpenAPI; the official FAQ's Dutch and English SOAP PDFs; the SOAP service/WSDL and inline schema; and the public bookkeeping manual for the owner's priority workflow. The web text extractor could not render Scalar or read raw JSON/WSDL, while direct unauthenticated public HTTP retrieval succeeded. The user manual was read as a public PDF with a local text extractor. No live bookkeeping API operation, account login or authorization token was used.

Retrieved public artifact identities:

| Artifact | Version / format | Bytes | SHA-256 |
| --- | --- | --- | --- |
| REST specification | API v1; OpenAPI 3.1.1 | 578380 | `0911fda0845873df8ebc6dfeaf2f1146dad2427737bcc7af1e94aaebf9b0bd98` |
| SOAP WSDL | 20 operations; inline XSD | 66001 | `2b17336ac539f3ad2587f153fd4c6db50523c253c1b1e6f3221b90b5632dde45` |
| Bookkeeping manual | Undated public PDF; 28 physical pages | 519432 | `1ca4ab066cef33edc2ac706380ab3031718b67dd30fb87570a30c9fac015ff7a` |

Full vendor documents remain outside tracked deliverables. This catalogue is a selective reference, not a redistribution of the specification or manuals. No separate public API changelog, official SDK or additional bank/attachment API contract was established by this bounded discovery. Authenticated knowledge-base articles, undocumented endpoints, account-specific entitlements and current UI layout are not certified.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.1 | 2026-10-30 | Codex (@imp researcher) | Scope capability gaps to official REST v1; link separate unofficial App assessment and exclude SOAP as a fallback. |
| 1.0 | 2026-10-30 | Codex (@imp researcher) | Catalogue the official REST and SOAP surfaces and the documented API/UI boundaries for invoices, mutations and imported bank rows. |
