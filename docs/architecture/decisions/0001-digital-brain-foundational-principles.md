<!-- pgmcp:v1 id=adr pv=1.0.0 pf=oghRUmcCvPBl7mJ- sf=WI5iXHBKVOU91bYE -->

# Digital brain foundational principles

**Status:** accepted  
**Version:** 1.12  
**Last Updated:** 2026-10-28

## Purpose

Record the owner's accepted conceptual principles for MyBrain so that subsequent design can be assessed against them.

## Scope In

Conceptual requirements for information, meaning, history, exclusive personal ownership and owner control, preservation, destruction, connection, intake, identity, transfer packages, description contracts, validity, traceable retrieval, generated context and label origin, retrieval responses, access revocation, scoped completeness, usability, uncertainty of description applications, universal registrability, the storage/contract responsibility boundary, and enduring identity distinct from historical records and current views.

## Scope Out

Technical stack, storage or hosting selection, formal schemas, connector implementation, live imports and implementation readiness.

**ADR:** 0001

## Context

The owner chose a broad digital brain with an evolving wiki and traceable meaning, rather than organizing its foundation around a particular application or source format. These conceptual decisions were accepted in the design discussion and recorded on 2026-10-22. The status accepted applies to these principles; it does not approve a technical design or establish QA or product readiness.

Earlier email-trial Research, Design and Planning documents concern prior bounded issue work. They do not select the current architecture or authorize new capture. This ADR records the new conceptual direction without rewriting those earlier artifacts. Prior technical research supplies no implicit adoption of a standard, product or implementation.

## Decision Drivers

- Support information and the owner's own contributions across private and business domains without fixing the foundation to an application.
- Preserve admitted sources while distinguishing factual registration, explicit meaning and computational representations.
- Keep changes in definitions, interpretations, dependencies and user corrections understandable over time.
- Retain owner control over access, processing, sharing, preservation and explicit destruction.

## Options

### Start from a particular application or storage solution

Deferred. A concrete application or storage experiment can be useful later, but it does not define this domain-independent conceptual foundation.

**Pros:**

- Provides a bounded implementation starting point once the relevant design is agreed.

**Cons:**

- Starting there can fix technical or application assumptions before the shared principles are clear.

### Exclude uncertain or spam material at intake

Superseded as the preservation policy. Within an authorized source scope, immature relevance or spam assessments do not determine what is destroyed or excluded before preservation.

**Cons:**

- Current relevance can differ from future value; exclusion loses material and labels that could support later evaluation.

### Preserve a generic framework with distinct functions and versioned meaning

Chosen. Preserve admitted originals, distinguish the three functional domains, trace evolving meaning and dependencies, and keep owner control.

**Pros:**

- Allows information to be registered before its meaning is settled and keeps later interpretations accountable to sources and history.

**Cons:**

- Requires later design for versioning, uncertainty, dependency re-evaluation, access and recovery.

### Make actual destruction impossible

Considered and not chosen. Preservation is the default, but the owner must retain an explicit destruction choice.

**Pros:**

- Avoids losing history through actual destruction.

**Cons:**

- Removes the owner's ability to destroy information; retaining hidden content would not honor a destruction choice.

## Decision

### P01 A broad extensible foundation

MyBrain supports private and business information across domains. Its foundation does not depend on a fixed file type, application or use case, and must accommodate new kinds of content and relationships.

### P02 Origin and capture are distinct

An item's origin and history may precede its digital capture. Distinguish origin, receipt, observation and admission into MyBrain. Digitally captured thoughts and observations contributed by the owner remain recognizable as the owner's own contributions. Recording an item does not establish its complete external history.

### P03 Preserve the admitted original

Preserve an admitted original as received without silent loss. Extractions, conversions, summaries and other derivatives remain separate and do not replace it. An observed source is not necessarily the ultimate origin. Preservation is subject to the explicit destruction choice in P16.

### P04 Minimal registration independent of understanding

Minimal factual registration does not depend on semantic understanding. It supports identity, receipt, preservation and integrity. Distinguish the system's own observations from claims supplied by a source; unknown information remains unknown. A source naming an author is not independent verification of authorship. The precise registration fields remain open.

### P05 Source and three functional domains

Distinguish the source from three functional domains: (1) minimal registration; (2) explicit descriptions and statements identifiable by people, including properties, labels, relations, assessments and conditions, whether authored by people or machines; and (3) computational representations and comparisons. These are functions, not prescribed data types or a mandatory sequential pipeline. Their vocabularies, schemas and contracts are not fully specified here.

### P06 Attributable meaning and visible uncertainty

Descriptions, statements and interpretations retain attributable authorship, method and context, including meanings inherited from earlier statements or definitions. Source claims, user judgments and automated assertions remain distinguishable. Earlier AI labels do not automatically become truth. Missing support, uncertainty, conflicts and multiple interpretations remain visible.

### P07 Similarity and exact conditions serve different purposes

Similarity can assist retrieval and discovery of relationships. Explicit properties and conditions enable exact tests. An exact calculation does not establish the semantic truth of its inputs. No representation model, search technology or ontology is selected by this principle.

### P08 Stable identity and versioned change

Keep stable identity distinct from versions for sources, descriptions, definitions, numerical representations and contracts. New states preserve history, subject to explicit destruction. Renaming and changing a definition are different changes; neither may silently reinterpret earlier claims.

### P09 An evolving reference frame

Definitions, rules, contracts and relevant supporting knowledge form an evolving reference frame whose changes remain traceable. An unchanged source can acquire new meaning as that frame changes. Earlier and current interpretations remain distinguishable without inventing historical reasons that were never recorded. The aim is traceability of historical meaning, not a claim of ultimate truth.

### P10 Trace dependencies and preserve corrections

Trace dependencies on source versions, statements, processing and contracts. A change flags possible re-evaluation rather than automatically making dependent results false. Preserve user corrections and their history. This does not promise replay of opaque AI internals or complete knowledge of every cause behind a result.

### P11 Generic versioned contracts

Use a domain-independent framework with explicit, versioned and extensible contracts. Add content-specific meanings and base sets separately. Contract evolution must leave earlier results understandable. Concrete contract structures, formal schemas and implementation technologies remain undecided.

### P12 Durable and usable information

Provide durable storage with checkable integrity and distinguish successful, incomplete and failed operations. Recovery must be possible within limits to be defined explicitly. Functional capabilities include retrieving, importing, labeling, finding, connecting, processing, exporting, presenting and using information. A clean, accessible interface across mobile, web and desktop is a requirement; no platform is selected.

### P13 Owner control and distinct durations

MyBrain is exclusively personally owned and controlled; the owner is the sole user in its internal authorization model. Internal sources, metadata, descriptions and derived context are private by default. Tools act on the owner's behalf within authorized scope, not as independent holders of rights over individual entities. P39 defines the staged access direction and refines the earlier general access discussion.

The owner controls reading, processing, changing, disclosing and destroying information and the duration of delegated access. Retention duration, access duration and substantive validity remain separate concepts. Disclosure restrictions must also cover derivatives so that summaries or computational representations cannot bypass owner control. Enforcement mechanisms and duration rules remain open.

### P14 Autonomous upkeep within owner control

Autonomous upkeep of the wiki and its meanings is intended product behavior within authorized source access and processing scope. Sources remain accessible within that scope, doubt and conflicts visible, and user corrections and history available; automated upkeep must not silently undo corrections. Remember user assessments as understandable, editable and versioned rules with bounded scope. This principle does not authorize a live import or unrestricted account access.

### P15 Preserve before assessing relevance

Future value differs from current relevance. Within a configured, authorized source scope, preserve incoming mail first and classify or assess it afterward. Spam and its labels can be useful for later testing and improvement. This supersedes the earlier conversational proposal to exclude spam or uncertain mail before storage. It does not authorize fetching accounts now or revise earlier published issue artifacts.

### P16 Preservation by default and explicit destruction

Preservation is the default. Actual destruction requires an explicit choice by the owner; classification alone has no autonomous destructive effect. Classification, withdrawal and hiding from an active view are distinct from destruction. Later design must define the chosen destruction scope across versions, derivatives and backups, the irreversible point and any minimal residual record. Hidden residual content within that scope would defeat destruction. Destruction knowingly reduces historical traceability; an audit marker cannot restore the destroyed source.

### P17 Connection is distinct from intake and authorization

Connection describes the medium, channel or digital sense through which MyBrain can exchange information with the outside world. It may support inbound, outbound or both directions; not every connection must support both. Connection capability is distinct from owner authorization in P13 and does not itself authorize reading, capture or outward action. Connection and intake behavior can evolve independently. Outbound behavior and its conditions remain to be discussed separately.

### P18 Explicit intake behavior and observable completeness

Intake arrangements describe how information is brought in through connections: initiative through push or pull, timing on request, periodically or in response to events, scope, and progress such as completed, pending or requiring retry. Keep origin, observation, receipt and successful complete storage distinguishable. Within an agreed, authorized intake scope, capture is a responsibility; a provisional relevance judgment must not become a hidden additional exclusion. Make incompleteness, failure and uncertainty about coverage visible. Completeness is assessed against the recorded intake scope, not against all external information or reality. Operational mechanisms remain open.

### P19 Selectivity defines intake scope rather than value

Selectivity determines whether information belongs within a particular intake's explicit scope. Scope can use sources, collections, periods or other stated characteristics, including content-based characteristics. The distinction from assessment is the purpose of the criterion, not whether content is read. Scope membership and judgments about meaning, importance or reliability remain separate.

Distinguish within scope, outside scope and undetermined membership. Outside scope means outside this intake only, not irrelevant or unreliable, and does not authorize deletion at the source. Undetermined membership must not silently become exclusion; its handling remains open.

Scope definitions and their changes are versioned and historically traceable. Widening scope requires a separate decision about future intake only or historical backfill. Narrowing scope never automatically destroys already preserved information. Scope selection has no destructive effect and does not replace the owner's explicit choice under P16.

### P20 Identity, state and exemplar are distinct

Distinguish an item's continuing identity, its recorded states or versions, and the exemplars or representations through which a state is encountered. Specify what equality means: identical received material, the same source item, the same version and the same meaning are different claims. Equal content does not prove shared identity or origin; changed content does not disprove continuity of identity.

| Distinction | Meaning |
| --- | --- |
| Same item | Recognized continuity of identity despite movement, redescription or change. |
| Copy | A separate exemplar reproducing a state, with its own receipt and preservation history. |
| New version | A changed state recognized as a continuation of the same item, with the earlier state retained. |
| Alternate representation or derivative | Information derived from or presenting an item differently, without automatically becoming its next source version. |
| Independent item with equal content | Content agrees, while shared identity or lineage has not been established. |

Identity, copy, version and derivation relationships retain their basis: supplied source claims, the system's own verification, inference or uncertainty. Repeated receipt remains a distinct event whose relevant provenance must not disappear through copy recognition. Changes belong to the component that changes: a new label or recalculated representation does not automatically create a new source version. Version histories may branch without silently selecting a sole successor. Identity assertions can be corrected, including mistaken merging or separation, while retaining earlier observations, judgments and correction history.

### P21 Transfer package, source item and version are distinct

A transfer package carries transfer context alongside content or a reference to content. It is distinct from the source item, its version, and the transfer or receipt occurrence. A package can carry one or several items or references; a source version can recur through different packages. Do not assume a one-to-one correspondence.

Sources differ in the context they supply. An identifier might identify a package, occurrence, source item, version or collection. A fresh package identifier does not establish a fresh source item. Preserve the distinction between supplied claims and our observations under P04. This is a generic transfer concept, not adoption of a particular messaging or transport standard.

### P22 Explicit contracts justify recognition

Concepts define what must be distinguished; explicit, versioned recognition contracts define what evidence justifies those distinctions. Identifiers, timestamps and change signals have no universally self-evident meaning. Contracts must address the following questions, with missing guarantees exposed rather than invented.

| Contract question | Required distinction |
| --- | --- |
| What is identified, and by whom? | The identified object, identifier issuer or source, and scope of uniqueness. |
| For how long is recognition justified? | Stability, validity, lifetime, and the meaning of resets or identifier reuse. |
| What does a change signal establish? | Source-content change, provider-side state change, changed accompanying registration, or uncertainty. |
| What does each timestamp describe? | Origin, change, offering, receipt and storage are separate events; a date alone does not generally prove identity or newness. |
| What supports repetition and completion claims? | Evidence for matching, expected coverage, completed capture and resumption of incomplete capture. |
| Which conclusions remain uncertain? | Missing or conflicting evidence and limits on recognition remain visible. |

Known identity, unchanged state and fully completed capture are separate findings. When sufficiently supported by the applicable contract, recognize repeated delivery without creating a second independent source merely because it arrived again. Retain relevant receipt history under P20. Unknown identifier meaning or validity must not cause silent skipping or an unjustified identity match. These requirements do not promise exactly-once delivery or reliable duplicate recognition where the source supplies insufficient guarantees.

The following daily inbox refresh is a conceptual illustration, not a chosen integration or permission to access a source.

| What is encountered | Required distinction |
| --- | --- |
| Known, unchanged and fully captured message | Recognize repetition rather than inventing a second independent source. |
| Previously encountered message with incomplete capture | Known does not mean complete; distinguish the outstanding work needed to resume or finish capture. |
| Message not previously captured | New to our memory even if it originated earlier. |
| Known message with changed characteristics | Distinguish changed source content from provider-side state or accompanying registration. |
| Identifier with uncertain meaning or validity | Expose uncertainty rather than silently skipping or claiming a reliable match. |

### P23 Description contracts span the three functional domains

Descriptions are distinguished by function and interpreted through explicit, versioned contracts across all three domains in P05. This defines how kinds of description work, not a catalog of individual labels, named properties or content-specific meanings.

| Domain | Function of its description contracts |
| --- | --- |
| Minimal registration | Distinguish what is observed during receipt and preservation from claims supplied with the source. |
| Explicit descriptions and statements | Identify what is asserted, what it concerns and the conditions for interpretation, without thereby establishing its truth. |
| Computational representations and comparisons | Explain what a representation or result stands for, which operations are justified and under what conditions results are comparable. |

A contract distinguishes the description's function, target item, version or part, admissible form, justified interpretation and its limits, conditions for use and processing, dependencies, and consequences of revision. These are general questions, not prescribed fields, schemas or an exhaustive vocabulary. Domain membership follows function rather than author or data type: an automated statement can belong to the second domain and a number to the first.

Keep a description linked to the governing contract version so it remains interpretable under the agreements used to create it. Reassessment under a new contract produces a separately recognizable result instead of silently rewriting the earlier description. The source need not have changed. Concrete description types, comparability requirements and contract definitions remain open.

### P24 Validity is explicit and distinct from chronology

Distinguish when a description was recorded, its governing contract version, its applicability scope, conditions and time, and its relationships to other descriptions. A newer timestamp, description or contract revision does not automatically invalidate an earlier description. There is no implicit latest-wins rule.

Descriptions under different contract versions may coexist, address different contexts, supplement each other or conflict. Conflict alone does not establish which description is invalid. Replacement, restriction or withdrawal requires an explicit basis, such as a contract rule, supporting evidence or an identifiable correction. Keep that basis, reason, scope and effective conditions traceable.

Conformance to a contract, applicability in a context and assessed semantic truth are separate judgments. Preferring a description for a particular use does not automatically invalidate alternatives. Earlier descriptions and changes to their status remain historically recognizable, subject to the owner's explicit destruction choice in P16. Concrete validity and replacement rules remain to be defined; this principle does not require a new owner approval for every rule-governed judgment.

### P25 Controlled joint retrieval and traceable results

The three domains in P05 and P23 are also described as metadata, labels, and mathematical or computational relationships. Metadata serves minimal registration with observations distinct from supplied claims; labels provide explicit, identifiable descriptions; computational relationships serve representation and comparison. These functional names introduce neither a fourth domain nor a fixed vocabulary.

Support retrieving a source or version by a described method and bringing together items with shared describable characteristics under explicit, versioned retrieval and comparison contracts. Joint selection does not itself establish contextual meaning or independent truth. Contextualization is a separate processing responsibility.

Keep each retrieval traceable to the participating source versions and descriptive identities and versions, governing contracts, labels and applicability conditions used, method and scope, and actual result. Distinguish the recorded result at moment A from a later execution at moment B: the same request may produce different results after sources, descriptions, validity or methods change. Historical reconstruction must not silently substitute current descriptions for those actually used. This requires no reconstruction of opaque reasoning or unrelated external information. Concrete retrieval guarantees remain open.

### P26 Produced context becomes a stored source

Produced context is itself a digital creation and is stored in MyBrain, regardless of its form. It receives its own identity, descriptions and version history and can serve as a source for subsequent processing. Being derived from earlier information and becoming a source for later work are compatible roles; preserve derived origin rather than treating storage as independent confirmation.

Context can receive descriptions in the same three domains as other sources. Contextualization is processing; its produced artifact belongs to memory. Neither a contextual format nor a requirement to perform that processing inside storage is selected here.

Contextual analysis can yield candidates for existing labels or new labels. Candidate assessment and acceptance follow contracts still to be defined; automatic processing within owner-authorized rules remains possible. Do not assume independent confirmation or manual approval is required for every label.

### P27 Label origin is distinct from assignment

A label is a reusable item with identity, meaning and origin. A newly stored label, including a candidate retained as an item, carries its origin when recorded. When it originates from produced context, refer to the originating context version rather than a moving current version. Reusing an existing label does not replace its origin. Meaning revisions follow the definition history in P08 and P09; missing origin remains visibly unknown under P04.

| Component | Responsibility |
| --- | --- |
| Label | Retain its identity, meaning and origin, including the originating context version where applicable. |
| Assignment | Connect a label to the source or context it describes, retaining applicability and history. The assignment is not additional metadata of the label itself. |
| Context | Remain an independently stored item that can carry the same labels as related sources. |

Sources and context carrying the same label can be selected together within a retrieval's scope. The label's origin can be consulted at label level without repeating it on each assignment. Label origin and the reason for every subsequent use are different questions: joint membership establishes neither a unique rationale for each assignment nor independent truth.

There is no universal requirement for a separate rationale document, an exact passage reference or a complete inference chain on every assignment. Further relationships may be expressed where their contracts require them, without duplicating the context in the original source registration.

### P28 Label applicability changes without erasing history

Keep label definition and origin distinct from assignment, assessment and recorded use. Later analysis may establish that an assignment was previously applicable but no longer is, was mistaken, applies more narrowly or remains contested. Contracts must express the relevant distinctions without imposing a fixed status vocabulary here.

Withdrawal, restriction or correction changes applicability or assessment; it does not erase the connection to the source or the label's contribution to earlier analysis. Preserve the assignment and assessment actually used, so that current-applicability retrieval differs from historical-use retrieval. Later changes may prompt dependent analyses to be reconsidered without automatically invalidating them all. Derived origin alone does not establish lesser validity.

Historical retention remains subject to the owner's explicit destruction choice in P16. Removing an assignment from current use is not destruction or permission to destroy it.

### P29 Retrieval method and response contract are distinct

Distinguish identifying the desired source, version or source set from defining what its retrieval returns. A described retrieval method can address an identified item, select items meeting explicit conditions, or compare items under stated criteria. These are starting distinctions, not an exhaustive prescribed query vocabulary.

A corresponding response contract defines which content and which recorded descriptions are returned. Do not assume that all metadata, labels and computational descriptions always accompany source content. Concrete response contracts remain open. This distinction preserves the historical retrieval basis in P25 without requiring that every description used for selection also be disclosed in every response. Retrieval is not a complete specification of export or exchange.

### P30 Access accompanies stored information and is revocable

Access control protects the owner's exclusive internal domain and is enforced on retrieval, alongside the stored information. A connection's capabilities do not confer authorization. Initially access is global for the owner; later bounded disclosure or access routes may exercise expressly delegated authority under P39. This does not establish independent third-party entitlements over individual sources, descriptions or other entities, nor prescribe a physical layout or database-row policy.

Revocation of granted authority must be atomic within its declared scope: the change takes effect as one whole without a partial access state. From its effective point, no further information may be disclosed under that authority. This includes a running retrieval for information not yet released; having started a request does not preserve its authority after revocation.

Revocation changes access, not retention of the source or history. It cannot recall information already delivered. Exact effective and release boundaries and controls over delegated routes, selected content and derivatives remain to be defined. Enforcement must be assessed against these guarantees, not inferred from a technology's name. The broader rights wording in earlier revisions is refined by P39; it is not a planned multi-party or per-entity rights model.

### P31 Completeness is relative to scope and operation

Exactness and completeness are separate properties. A result can accurately represent the available information while omitting information outside what was captured, processed or retrieved. Completeness is always assessed against an explicitly described scope and operation, not against global knowledge.

| Operation | Completeness question |
| --- | --- |
| Intake | Has everything within the agreed intake scope been received and stored? |
| Processing | Has the intended operation been performed on all involved inputs? |
| Retrieval | Does the result include everything deliverable under the retrieval method, conditions and access rights? |

Distinguish established completeness, established incompleteness and unknown completeness. These are separate judgments, not a prescribed status schema. If scope or coverage cannot be established or verified, completeness remains unknown. A successful operation proves only the scope actually checked; intact captured items do not establish complete intake.

An empty retrieval alone does not establish nonexistence. Information may be absent from a source, not captured, not processed or outside retrieval scope. Coverage reports must respect P30 rather than disclose inaccessible existence. Concrete methods for establishing coverage remain open.

### P32 Partial results and usability are distinct from completeness

Partial results may be supplied while making actual execution, assessed completeness, known limits and unknowns recognizable within the recipient's access rights. Do not silently present a partial result as complete or promise to enumerate missing items whose existence cannot be established.

The applicable contract or the recipient, within their authority, may assess whether a partial result suffices for its intended use. A contract may set prior requirements; a recipient may decide within the permitted scope. Neither usability judgment overrides access restrictions or mandatory applicable constraints. This creates no universal requirement for manual approval.

Incomplete does not necessarily mean unusable, and a result deemed usable does not thereby become complete. Concrete thresholds, stop or continuation rules, recovery and presentation remain open; this principle does not prescribe a per-request audit mechanism.

### P33 Application uncertainty is distinct from definition

Keep the reusable label or description's registration and definition, including identity, origin and versioned meaning, distinct from its coupling or application to a particular source or source version. For this concern, uncertainty or dispute about whether a description fits a source belongs to that application, not to the reusable definition. A clearly defined label can have an uncertain application.

Keep what a source states distinct from assessments of it. Contradictions are recognized between concrete applications or statements about sources; conflicting applications do not themselves make the shared definition contradictory or invalid. Preserve uncertain, disputed and conflicting applications rather than silently resolving them by treating one as truth. A reasoned selection for a particular use does not erase alternatives or automatically invalidate them.

A dispute about an application does not automatically propagate into a definition change. If the definition itself needs revision, make that a separate, explicit versioned change under P08, P09 and P24. This does not claim that definitions can never be ambiguous or revised. Retain historical applications, assessments and uses under P27 and P28.

Concrete conflict-recognition, review and use contracts remain open. No fixed status vocabulary, confidence score or additional rationale requirement for every assignment is introduced.

### P34 Universal registrability without prior understanding

Everything capable of digital recording must be able to have a place in the storage framework, directly or through a referencing registration. Function, meaning and intended use are not prerequisites for registrability. Registration must not depend on semantic understanding or a predetermined source class. This applies to sources, descriptions, produced context, contracts and other digitally recordable items without selecting a format, schema, ontology or platform.

Assess the general source-registration framework against that breadth, including whether a contract can receive identity, origin, versions and the other applicable registration properties. Registrability is a capability, not blanket authorization to access or ingest information; the existing scope and owner-control principles remain in force.

Keep preserved content distinct from a preserved reference. Recording a reference alone does not establish preservation, integrity or continued availability of its target. Concrete reference guarantees and treatment remain open. This neither requires copying every referenced target nor weakens the preservation requirements for an admitted original under P03.

### P35 Storage and operational contract responsibilities are distinct

Storage registers and preserves items, descriptions, identities, history and relevant properties or results. Stored source properties can provide inputs for deciding whether a computational comparison may take place. Whether such a property is a label or another description remains open.

The contract layer evaluates applicability, suitability and permission for comparison and governs and enforces the corresponding processing operations. Do not silently make comparison eligibility or contextual interpretation inherent storage work. Computational representations and results can themselves be stored, while calculation and assessment remain separate responsibilities.

A contract is digital information and can be stored with identity, origin, versions and applicable registration properties. Registering that artifact does not activate it, establish its authority or execute or enforce it. Distinguish the stored contract from the layer that consumes and enforces it.

These are conceptual responsibilities, not a prescribed physical topology. This boundary does not remove P30's access-control requirement at stored information or permit bypass: retrieval authorization remains distinct from comparison eligibility. Concrete contract activation, applicability and enforcement arrangements remain open.

### P36 Enduring identity, historical records and current views are distinct

Keep an item's enduring identity distinct from versioned descriptions of it, a historical record of what was known or used, and a current view assembled under an applicable contract. A link to an identity does not by itself freeze that identity's entire description. Where a historical statement, result or action depends on particular descriptions or values, retain the versions or values actually used rather than silently substituting their current successors.

Later changes do not automatically retarget historical references, rewrite earlier source content or invalidate earlier descriptions. Corrections and supplements remain separately recognizable with their history. A current view may incorporate newer knowledge without changing those historical records. Keep when information was recorded or known distinct from when it applies; uncertainty or conflicting applicability remains visible under P24 and P33.

For a new action, the operational contract determines which available descriptions apply to its purpose and effective circumstances; the newest registration alone is not sufficient. Record the actual selected or used information in the new action's contribution, result or source where relevant. This describes the required traceability, not permission to execute an action or a selection mechanism in storage.

In a synthetic example, person P remains the shared identity across a recorded shipment using address A and a later shipment using address B. The relocation changes the person's recorded descriptions, not the earlier shipment. A current view can show B as applicable while preserving the earlier use of A.

A recorded combined state must distinguish its participating source-content and description versions from an evolving current view. Independently versioned, unchanged components can be reused; traceability does not require a full copy of the whole composition or cascading revisions of every linked item. Concrete version boundaries, selection and correction rules, reconstruction mechanisms and storage techniques remain open.

### P37 Version history supports metadata sets and narrative context

Version history is the foundation for retaining change without losing earlier recorded meaning. Validity, receipt and registration moments are examples of descriptive metadata that can be versioned together as a coherent set. Grouping does not collapse their distinct meanings: receipt, recording or knowledge, and substantive applicability remain different questions under P24 and P36. A revised set retains its preceding values and their interpretation, observations remain distinct from supplied claims, and enduring identity is preserved. This selects neither a mandatory grouping for all metadata nor a separate history engine for every field.

Unknown, conditional or disputed validity must not be forced into two artificial timestamps. Complex temporal relationships and wider meaning can also be described in narrative wiki contexts; not every nuance needs a compact label or exact property. Such context is itself a versioned stored source under P26, with attributable basis and retained corrections. Narrative description does not itself enforce operational conditions or reconstruct evidence that was never recorded. Later interpretation may yield label candidates under P27 and P28 without treating derived repetition as independent support.

Labels provide explicit associations for retrieval and contract-defined tests, while narrative contexts connect sources, events and knowledge in richer descriptions. If confidence or association strength is recorded, it concerns the particular assignment or assessment under P33 rather than a universal property of the label definition. A score does not by itself establish a probability or truth; no mandatory scoring method, threshold or representation is selected.

The brain analogy explains these complementary functions, not a choice of neural implementation. Metadata grouping, version boundaries, contextual extraction and scoring contracts remain open. These requirements adopt no event-sourcing, bitemporal-storage or other particular database mechanism.

### P38 Lifecycle metadata stays with the source registration

A candidate for intake is an ordinary source registration with lifecycle metadata, not a separate kind of source authority. Admission does not require creating a second registration or assigning a new source identity solely because its lifecycle position changes. Registration itself neither authorizes further capture nor proves complete preservation or present availability.

Lifecycle metadata remains attached to that same registration during intake and throughout its subsequent existence. Its changes follow the general version-history framework in P37, preserving earlier observations and states without a new semantic domain or special versioning engine. Keep operational lifecycle descriptions distinct from content labels, substantive applicability and source-content versions. Independent lifecycle concerns need not be compressed into one status or a fixed state catalog.

A staging area is a working view of those registrations needing preparation, processing or attention. It is not a second authoritative source repository or identity. Leaving that view does not delete the source or its history; a registration can reappear when new work arises. This defines the view's responsibility without prescribing storage layout or interface behavior.

The applicable lifecycle contract defines the meaning of these descriptions and the admissible transitions and conditions for the same registered object. Under P35, storing that contract remains distinct from its operational execution, enforcement and authorization. A recorded lifecycle description alone does not prove that the described operation succeeded; completeness and unknowns remain subject to P31 and P32.

Expired access, ended applicability and retention duration remain distinct under P13. Requested deletion and confirmed actual destruction are different facts. Neither lifecycle classification nor leaving a working view authorizes destruction: the owner's explicit choice and scoped consequences under P16 remain required. Concrete metadata, transition conditions and evidence remain open.

### P39 Exclusive personal ownership precedes bounded disclosure

MyBrain's internal memory remains the owner's private domain, with no independent third-party entitlements to its individual sources, entities, rows, cells or fragments. Treating it as private thoughts expresses an intended confidentiality and design requirement, not evidence of absolute secrecy.

The first stage uses global owner access. Tools may perform authorized work on the owner's behalf without becoming additional internal users with their own content entitlements. Internal security boundaries and least privilege remain valid means of protecting that ownership; they do not imply a multi-party content-rights model.

A later stage may add bounded disclosure or access routes. The owner determines the permitted information selection, operations and revocable delegated authority for each route, without transferring ownership or automatically granting direct entitlements within internal memory. Exporting, sending or otherwise disclosing content remains subject to the owner's authorization. Sending content to an external model or service is a disclosure boundary even when that service is used as the owner's interface. This neither requires fresh manual confirmation for every routine operation within an existing authorization nor grants blanket autonomous publication authority.

Rights per entity are not a planned subsequent phase or target architecture. Adopting such a model would require explicit owner reconsideration. This refines the earlier P13/P30 access discussion and the historical row-level-security candidate without selecting or prohibiting a particular internal security mechanism. The revocation, retention and already-disclosed-information distinctions in P13 and P30 remain applicable. Concrete route boundaries and enforcement remain open.

## Rationale

Preservation keeps future interpretation possible even when current understanding is incomplete. Distinct sources, statements and computational functions prevent convenient representations from silently becoming originals or accepted truth. Stable identities and versioned reference frames make historical meaning understandable while allowing correction and change. Owner-controlled destruction remains possible because preservation by default does not remove the owner's authority over retained information.

## Consequences

### Design obligations

Subsequent design must keep originals, registration, explicit statements and computational representations distinguishable; support their provenance and evolution; preserve corrections; and expose uncertainty and incomplete operations. Autonomous upkeep remains subject to the owner's source scope and controls. Information must remain useful through accessible retrieval, processing, export and presentation. Connection capability, authorization, intake behavior and scope must remain distinguishable, with intake completeness judged against its recorded scope. Distinguish packages, source items, versions, exemplars and receipt occurrences; recognition must use explicit contracts and preserve the distinction between known identity, unchanged state and complete capture. Descriptions across all three domains retain their governing contract versions and explicit applicability; later descriptions or contracts do not silently invalidate earlier ones.

Produced context is stored as a reusable source, while contextualization remains a separate processing responsibility. Retrieval must retain its actual descriptive basis and results. Labels retain their origin separately from assignment; shared labels can bring sources and context together without requiring repeated assignment-level rationale. Changes in label applicability retain historical connections and uses.

Retrieval method and response content remain separate contract responsibilities. Protect exclusive personal ownership with global owner access first and possible bounded disclosure routes later; per-entity third-party rights are not a planned phase. Enforce atomic, directly effective revocation of delegated authority within its scope, including unreleased information in running retrievals. Retention remains independent, and already disclosed information cannot be recalled by changing authority.

Assess completeness separately for intake, processing and retrieval against their described scope. Partial results may be useful when their known limits and unknowns remain recognizable; the contract or authorized recipient assesses sufficiency without overriding mandatory constraints.

Assess uncertainty and dispute at the application of a reusable description to a source, separately from the description's definition. Keep conflicting applications and use-specific selections traceable without silently revising definitions or erasing alternatives.

The registration foundation must be general enough for any digitally recordable item, including contracts. Keep storage and reference guarantees explicit, and separate recording a contract or comparison result from activating, evaluating or enforcing processing contracts. Access control at stored information remains required.

Preservation and historical traceability carry storage, maintenance and interpretation costs. Explicit destruction can intentionally reduce the available history. Access control and destruction must account for derivatives rather than treating summaries or numerical representations as independent routes around the owner's choices.

### Open design details

- Minimal registration fields and the boundary between receipt, observation and admission, including admission validation.
- Lifecycle metadata and conditions on the same registration before and after intake; staging-view membership, re-entry and evidence for transitions without a fixed state catalog or new identity.
- Assessing universal registrability across digitally recordable items, including contracts; concrete guarantees for direct content versus referencing registration.
- Stored contract artifacts versus activation, authority, applicability and enforcement roles; source properties used for operational contract judgments without fixing their descriptive form.
- Precise intake scope criteria, handling undetermined membership, timing and progress mechanisms, and determining observable coverage.
- Future-only intake versus historical backfill when scope widens; outbound behavior and its conditions.
- Vocabularies, content-specific base sets and their semantics.
- Coherent metadata grouping and version boundaries, confidence or association-strength representations and interpretation, and extracting compact descriptions from richer narrative context without forcing all meaning into fields.
- Concrete recognition contracts, evidence for identity and equality, package contents and capture completeness, identifier authority and reset behavior, and conflict or unknown handling. Contract purposes and questions are accepted; source-specific guarantees and mechanisms remain to be defined.
- Concrete description types and base sets across the three domains, admissible forms, comparability requirements, contract definitions, evolution rules and dependency re-evaluation.
- Evidence and rules for validity, contextual applicability, replacement, restriction and withdrawal, including scope and effective conditions. Their distinction from recording time, contract conformance and assessed truth is accepted.
- Concrete recognition of conflicts between source-related applications or statements, assessment and review of uncertain applications, and use-specific selection contracts. Application disputes and explicit definition revision remain distinct.
- Concrete retrieval and comparison guarantees, scope, historical-result reconstruction, and response contracts defining returned content and descriptive domains. No fixed response bundle is selected.
- Label origin and assignment contracts, candidate assessment and acceptance rules, and concrete applicability or review behavior. Label origin is required; a rationale for every assignment is not universally required.
- Context artifact forms and storage realization; contextualization methods and processing design remain outside the source-registration decisions.
- Criteria for copy, version and derivation relationships, branching history, and correction of mistaken identity merges or separations.
- Concrete reference and version boundaries for enduring identities, historical combined states and current views; applicable-description selection for new uses, correction rules and reconstruction. No event-sourcing, temporal-storage, hash scheme or full-copy mechanism is selected.
- Global owner-access protection and possible bounded disclosure/access routes: permitted information selection and operations, delegated-authority boundaries, derivative handling, concurrent retrieval enforcement and exact effective/release boundaries for revocation. Atomic and direct effect within granted scope is required. Per-entity multi-party entitlements are not a planned phase; any such change requires explicit owner reconsideration.
- Retention periods, access periods and substantive validity.
- Concrete completeness and coverage evidence for intake, processing and retrieval; handling unknown coverage without revealing inaccessible information.
- Partial-result usability requirements, recipient decision boundaries, thresholds, stop or continuation rules and presentation of known limits or unknowns.
- Recovery limits and mechanics.
- Destruction scope and mechanics across versions, derivatives and backups, its irreversible point and any minimal residual record.
- Platform, storage, search, AI processing and connectors.

No implementation or operational action follows automatically from this conceptual acceptance.

## Related Documents

- [Repository agreements for research and decisions](<../../../README.md#research-status-and-decisions>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-22 | Codex (recording owner decisions) | First record of the owner-agreed foundational principles; technical and operational design choices remain open. |
| 1.1 | 2026-10-22 | Codex (recording owner decisions) | Add P17–P19 to distinguish connection, authorization, intake behavior and scope selectivity; retain scope history, visible coverage limits and non-destructive scope changes. |
| 1.2 | 2026-10-22 | Codex (recording owner decisions) | Add P20–P22 for identity, state and exemplar distinctions, transfer packages, and versioned recognition contracts; illustrate repeated intake without selecting technical mechanisms. |
| 1.3 | 2026-10-22 | Codex (recording owner decisions) | Add P23–P24 for generic description contracts across the three domains and explicit validity independent of chronology; preserve earlier descriptions and contract interpretation. |
| 1.4 | 2026-10-23 | Codex (recording owner decisions) | Add P25–P28 for traceable joint retrieval, stored context as a reusable source, label origin distinct from assignment, and preserved label applicability history; retain open contract and processing details. |
| 1.5 | 2026-10-23 | Codex (recording owner decisions) | Add P29–P30 for retrieval method versus response contracts and access managed alongside stored information, with atomic and direct revocation; leave enforcement, scope and release-boundary details open. |
| 1.6 | 2026-10-23 | Codex (recording owner decisions) | Add P31–P32 for scoped completeness across intake, processing and retrieval, visible limits of partial results, and usability assessed by the contract or authorized recipient. |
| 1.7 | 2026-10-24 | Codex (recording owner decisions) | Add P33 to distinguish uncertainty and dispute about source applications from reusable definitions, preserve conflicting applications and keep definition revision explicit. |
| 1.8 | 2026-10-24 | Codex (recording owner decisions) | Add P34–P35 for universal registrability, direct/reference distinctions and the boundary between storage and operational contract responsibilities, including contracts as stored information. |
| 1.9 | 2026-10-26 | Codex (recording owner decisions) | Add P36 for enduring identity, historical records and current views; retain actual used descriptions, independent component histories and open version/selection mechanisms. |
| 1.10 | 2026-10-26 | Codex (recording owner decisions) | Add P37: version history as the foundation, coherent metadata sets with distinct meanings, richer narrative context and assignment-specific confidence without selecting a temporal or scoring mechanism. |
| 1.11 | 2026-10-26 | Codex (recording owner decisions) | Add P38: lifecycle metadata remains with the same registration beyond intake, and staging is a working view; preserve version history, operational boundaries and explicit destruction authority. |
| 1.12 | 2026-10-28 | Codex (recording owner decisions) | Add P39 and refine P13/P30: exclusive personal ownership, global owner access before optional bounded disclosure, with no planned per-entity multi-party rights phase; retain scoped revocation and internal security controls. |
