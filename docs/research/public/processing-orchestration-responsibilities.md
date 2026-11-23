<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Processing coordination: capabilities and MyBrain responsibilities

**Status:** Research record — technology selection deferred; independent review requested

**Version:** 1.0

**Last Updated:** 2026-11-12

## Purpose

Record reusable processing-coordination capabilities and their boundaries around MyBrain intake, processing and evolution, without choosing a package or technology.

## Scope In

Technology-neutral responsibilities, documented orchestration examples, MyBrain integration/domain boundaries, synthetic illustrations, open options and possible evidence criteria.

## Scope Out

Technology adoption, accepted architecture, implementation planning, live source/data access, platform installation/runtime experiments, issue-9 probe expansion and workflow phase exit.

## Problem Statement

Scheduling, retries, waiting work and processing visibility can otherwise become repeated custom infrastructure. Research needs to identify what reusable machinery could provide and what must remain explicit MyBrain responsibility, without mistaking an engine for source authority or domain understanding.

## Goals

- Preserve the findings as screened cross-project research rather than an issue-specific technology decision.
- Separate documented engine capabilities, integration work and MyBrain/domain responsibilities.
- Keep evidence limits, candidate status, open questions and possible later evaluation criteria explicit.

## Background

The owner requested durable recording of these findings on 2026-11-12 while explicitly deferring package and technology selection. The accepted [foundational principles](../../architecture/decisions/0001-digital-brain-foundational-principles.md), revision 1.12 dated 2026-10-28, govern conceptual meaning. The [issue-6 research](../../development/issue6/research.md) is a dated consolidation; its [design](../../development/issue6/design.md), revision 1.3, and associated [operations](../../development/issue6/storage-operations.md) remain a design candidate with independent review requested, not an implemented storage service. Earlier platform/trial proposals retain their historical status.

## Findings

### Functional responsibility, without a deployment decision

Processing coordination arranges when authorized work is attempted, which inputs and dependencies are available, how resources are shared, and how incomplete or failed work becomes visible and recoverable. It can support intake, extraction, interpretation, computational representations and later re-evaluation as the reference frame evolves. These functions need not form one mandatory sequential pipeline (P05).

**Research inference:** reusable scheduling and execution machinery could reduce plumbing around MyBrain-specific processing. This is a functional responsibility, not a requirement for a separate service or orchestration platform in v1. A small in-process coordinator, a simple persistent queue or a reusable orchestrator remain possible.

### Capability and responsibility matrix

The engine column records documented Dagster examples consulted on 2026-11-12. The other columns are MyBrain research interpretations of the integration boundary, not implemented contracts or accepted requirements. A capability still requires appropriate deployment and configuration; another engine would need its own evidence.

| Task | Documented engine capability: Dagster example | Integration/configuration we would provide | MyBrain/domain responsibility retained |
| --- | --- | --- | --- |
| Schedule and event observation | Schedules and [periodically evaluated sensors](https://dagster.io/docs/guides/automate/sensors) can request work; cursors track observation progress. | Source connectors, observation logic, trigger definitions, cursor meaning and intervals. A minimum interval is not an exact timing guarantee. | Authorized intake scope, freshness/coverage meaning and decisions about capture; an observation does not establish admission. |
| Dependency ordering and parallel work | [Assets, jobs and ops](https://dagster.io/docs/getting-started/concepts) describe execution dependencies; [automation conditions](https://dagster.io/docs/guides/automate/declarative-automation) can request dependent updates. | Map executable steps and dependencies; select an executor and define when inputs are usable. | Semantic dependencies, applicable contracts and whether re-evaluation is warranted. A processing-dependency graph is not the semantic relation graph. |
| Persistent waiting work and priority | [Instance storage and run coordination](https://dagster.io/docs/deployment/oss/oss-instance-configuration) support operational history, queued coordination and prioritization policies. | Durable instance configuration, queued coordinator/daemon where required, work-to-run mapping, priority tags and recovery/retention policy. | What outstanding work means, its authorized scope and result registration. A run queue is not the authoritative source registry. |
| Configured concurrency and resource pools | [Run, executor and cross-run pool limits](https://dagster.io/docs/guides/operate/managing-concurrency) limit simultaneous work. | Classify resource use, assign pools/tags and configure measured limits. Provider quotas may also need client-side pacing and shared quota accounting. | Work importance, permitted disclosure and acceptable contention. Concurrency limits alone do not enforce requests-per-minute, token or daily API quotas. |
| Bounded retries and backoff | [Ops](https://dagster.io/docs/guides/build/ops), [run retries](https://dagster.io/docs/deployment/execution/run-retries) and the vendor's [DataOps guide](https://dagster.io/blog/dataops-with-dagster-a-practical-guide-to-building-a-reliable-data-platform) describe retry policies, including op-level backoff. | Retryable error classification, attempt bounds, delay/backoff and coordination of step/run retries. | Idempotent effects, resolving uncertain publication and preserving failures; retry permission is not new capture or disclosure permission. |
| Selective re-execution | [Configured run retries](https://dagster.io/docs/deployment/execution/run-retries) can use a from-failure strategy; the [UI](https://dagster.io/docs/guides/operate/webserver) exposes re-execution. | Retain and locate successful prior outputs under durable, accessible storage and compatible execution definitions; map exact input/output references. | Validate historical inputs and method bindings; resolve already committed effects. This restarts selected work, not an arbitrary instruction pointer or opaque AI session. |
| Selective batches and historical backfill | [Backfills](https://dagster.io/docs/guides/build/partitions-and-backfills/backfilling-data) can select partitions and group their execution. | Define partition/batch meaning, bounded selection and code able to process the selected units. | Decide which admitted sources and versions qualify, whether historical intake is authorized, and how newer results coexist with earlier ones. |
| Run/step status, errors, logs and history | The [webserver/UI](https://dagster.io/docs/guides/operate/webserver) shows runs, step timing, errors, logs and backfill progress. Some documented enhancements are Dagster+ features. | Operate and protect the UI/history store, emit safe structured logs and link operational runs to domain results. | Explain source coverage, validity, authorization and actual registration outcomes. A green run alone is not evidence of meaningful or complete domain processing. |
| Shared resources and injection | [Resources](https://dagster.io/docs/guides/build/external-resources) share client implementations/configuration; [lifecycle hooks](https://dagster.io/docs/guides/build/external-resources/managing-resource-state) initialize and clean up per run and process. | Adapters, secret delivery, client lifetime, connection pools and cleanup appropriate to the executor. | Reusable domain authorization and durable writing remain in shared MyBrain components. No universal single connection across processes or runs is promised. |
| Execute quality checks and optionally block | [Asset checks](https://dagster.io/docs/guides/test/asset-checks) report outcomes; downstream blocking is explicitly configured and is not the default. | Implement checks, associate them with relevant outputs, choose blocking/severity behavior and handle failures. | Define correctness, sufficiency, uncertainty and permitted continuation under the applicable contract. Engine check status cannot decide semantic truth. |

The matrix describes potentially reusable machinery, not a claim that installing Dagster supplies MyBrain's connectors, processing functions, contracts or operating policy.

### Source authority remains with MyBrain

The following boundaries derive from the accepted principles and are consistent with the existing issue-6 design candidate; they do not accept that candidate or replace its precise contracts.

- **Identity and immutable basis:** distinguish source identity, source-content revisions, independently versioned descriptions and definitions, processor/model versions and processing-contract versions. Retain the actual selected inputs and method basis rather than later resolving everything to current heads (P08–P11, P20, P23–P24, P36–P37).
- **Validity and provenance:** when a result was produced or registered is different from when it applies. Newer computation does not automatically invalidate a prior meaningful result, reinterpret its definitions or undo an accepted correction. Preserve attributable claims, uncertainty, alternatives and actual used versions (P06, P10, P24, P33, P36).
- **Durable registration and publication:** MyBrain remains responsible for idempotent registration, atomic publication at its own boundary, integrity and explicit incomplete/uncertain outcomes. Scheduler run keys do not supply exactly-once business effects. Dagster deduplicates run requests by run key **within a given sensor**; a retried function or an external side effect still needs its own reliable effect protocol. See [sensor run keys](https://dagster.io/docs/guides/automate/sensors) and the [candidate publication contract](../../development/issue6/storage-operations.md#publication-and-idempotency).
- **Operational work is separate:** scheduler runs, queue entries, observation cursors and logs describe execution, not enduring source authority. Relevant lifecycle descriptions or results can be registered deliberately; a scheduler event is not automatically a durable MyBrain source registration.
- **Staging preserves one authority:** P38 makes staging a working view over existing source registrations needing attention. A registered candidate retains its identity through admission and later work. Pre-admission observations and synchronization inventory are not automatically such registrations; this report proposes no second source registry or fixed lifecycle vocabulary.
- **Authorization precedes execution:** a timer, retry, backfill or stored contract does not grant permission to read, transfer, disclose, activate a contract or destroy information. Capture, preservation and substantive assessment remain distinct (P13, P16–P19, P30–P35).
- **Graphs have different meanings:** semantic relations may include cycles and do not directly define a runnable dependency graph. The processing arrangement needs its own explicit dependencies and re-evaluation conditions; a change indicates possible work, not automatic falsity.

Dagster sensors observe on intervals and then request work. **Research inference:** this mechanism does not establish a native client's before-first-byte upload gate. It supplies no missing proof for the separate [OpenCloud admission investigation](../../development/issue9/opencloud-admission-extension-feasibility.md). Issue 9's scope and probe acceptance remain unchanged.

### Illustrative admitted-source processing

This synthetic example explains the boundary; its ordering, names and quantities select no workflow, defaults or requirements.

| Situation | Possible coordination task | Meaning retained in MyBrain |
| --- | --- | --- |
| Twelve already admitted synthetic documents await processing. | Select the authorized set and request suitable extraction steps; independent work may run in parallel within configured capacity. | Exact admitted source revisions and actual available bytes are the inputs. Registration does not depend on extraction succeeding. |
| Extraction succeeds; interpretation fails transiently. | Record failure and, under a bounded policy, re-execute the failed step using a durable available extraction result. | Preserve the successful derivative and its basis; resolve any uncertain prior writes before repeating effects. |
| A later model or contract becomes available. | Select a bounded subset for new processing rather than reread or regenerate everything. | New model/contract bindings produce distinguishable results. Earlier meaningful versions and user corrections remain available; current applicability is an explicit domain judgment. |
| The prior output is missing or incompatible. | Expose unavailable input or request explicitly authorized prerequisite work. | Do not pretend to resume from a saved program position or silently substitute a newer source/definition. |
| Work finishes. | Show actual run/step outcomes and remaining failures. | Publish traceable domain results through the registration boundary; completion covers the stated scope only. |

### Reusable processing and interfaces

**Research interpretation:** narrow functions could extract text, compute a representation or evaluate a stated check, while reusable API clients handle their external interfaces. Shared MyBrain components could own domain authorization and the durable registration/log-writing boundary. Orchestration adapters would call those components rather than duplicate their policy in every job.

Keep these components independent of any orchestration framework so they can also be invoked by a small coordinator, a command or another authorized consumer. Technical interfacing should not embed business judgments such as relevance, source identity, substantive validity or whether an uncertain result is acceptable. Operational logs and durable domain records have different purposes.

Dagster [I/O managers](https://dagster.io/docs/guides/build/io-managers) are optional; its documentation explicitly recognizes pipelines that already manage I/O. Reusing an orchestrator need not move MyBrain storage/publication into framework-managed outputs. How to preserve accessible intermediate outputs still needs explicit evidence.

### Options remain open

| Option | Potential benefit | Cost or uncertainty to investigate |
| --- | --- | --- |
| Build a small coordinator in the application. | Direct control and potentially little initial runtime overhead. | MyBrain would implement and maintain the needed waiting-work, retry, observability and recovery behavior. |
| Use a simple persistent queue with workers. | A bounded execution mechanism that may be enough for early work. | Dependency handling, selective reprocessing, administration and result semantics may need additional code. |
| Reuse an orchestration engine. | Reuse scheduling, execution tracking and operational tooling represented in the matrix. | Integration, operational metadata, resource overhead, upgrades and framework coupling remain to be assessed. Dagster is one sourced example, not a selection or complete market comparison. |

No processing platform, deployment, language, database/broker, topology, numeric settings or code contracts are chosen here. Existing storage-candidate choices are neither reopened nor adopted by this report. Runtime behavior, maintenance burden and NAS resource fit have not been tested.

### Proposed evidence criteria, not an execution plan

These questions could distinguish the options in later research. They are not approved acceptance requirements, a scheduled experiment or permission to install software.

| Boundary to assess | Useful evidence |
| --- | --- |
| Restart, partial failure and lost acknowledgment | Retained waiting work; bounded repeated attempts; deliberate resolution of uncertain writes; selective re-execution with demonstrably available prior outputs. |
| Historical meaning and selective evolution | Exact source/method/definition bindings; old and new results remain distinguishable; corrections survive reprocessing. |
| Resource and provider constraints | Measured CPU, memory and storage use; contention behavior; configured concurrency distinguished from time-window API quota control. |
| Operational use and privacy | Understandable pending/failed/completed states; protected/redacted logs; access and telemetry behavior verified for the selected deployment. |
| Maintainability and portability | Independent invocation of processing functions/clients; upgrade/recovery burden; costs and limitations visible for each option. |

### External evidence and its limits

Primary documentation and the vendor-authored retry explanation were consulted on 2026-11-12. The linked documentation is mutable: these are dated source observations, not a pinned release contract or results from an installed instance. MyBrain interpretations and proposed criteria above are not vendor guarantees. No Dagster runtime, integration, benchmark or NAS test was performed.

The [repository license](https://github.com/dagster-io/dagster/blob/master/LICENSE) identifies the Dagster open-source code as Apache-2.0. That does not make separately marked Dagster+ features part of the open-source edition. Exact edition/version capability and any dependency licenses would need later verification before adoption.

The [telemetry documentation](https://dagster.io/docs/about/telemetry) describes usage collection, an opt-out, and exclusion of pipeline data and identifiable definition names. This is the vendor's stated behavior, not an independent privacy/egress verification or an assurance about our own logs and integrations.

The [Help Net Security article](https://www.helpnetsecurity.com/2026/11/12/dagster-open-source-cloud-native-data-pipeline-orchestrator/) was a discovery pointer. Its contents could not be fetched during the original investigation; it is unread and is not evidence for the capability claims here.

### Change surface

This record changes public cross-project research and README navigation only. Existing issue-6 research/design/operations and ADR 0001 were reviewed as context and remain unchanged. No application code, tests, configuration, agent protocol, template package or enforcement rule is changed. Future research/design may use this report as an evidence index; it does not complete issue 9 Research or authorize a phase transition.

## Questions

- What is the smallest coordination mechanism adequate for the first authorized processing scope, and when would a reusable engine reduce total maintenance?
- What exact input/result references and available durable intermediates are needed for selective re-execution without coupling domain code to a framework?
- How should a later selected deployment reconcile its operational history with domain registration after crashes, restore, missing outputs or lost acknowledgments?
- What measured operating/resource costs and privacy behavior would distinguish the options, including a possible NAS deployment?
- Which domain changes warrant re-evaluation, and under which contracts can new results become current without erasing prior meaning or corrections?

## References

- [Accepted foundational principles (P05, P08–P11, P18–P24, P30–P38)](<../../architecture/decisions/0001-digital-brain-foundational-principles.md>)
- [Issue-6 research consolidation](<../../development/issue6/research.md>)
- [Issue-6 storage design candidate](<../../development/issue6/design.md>)
- [Candidate registration/publication operations](<../../development/issue6/storage-operations.md>)
- [Separate OpenCloud admission assessment](<../../development/issue9/opencloud-admission-extension-feasibility.md>)
- [Repository research and publication agreements](<../../../README.md#working-agreements>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-11-12 | Codex (@imp researcher) | Record technology-neutral processing-coordination capabilities, MyBrain boundaries, a sourced Dagster example and open evaluation criteria without adoption or runtime evidence. |
