# Twin Reasoning Wiki — Adaptation Specification for Opus 4.6

## 0. Mission

You are working on a local fork derived from the LLM-Wiki approach/repository.

Your goal is to adapt this repository into a **Twin Reasoning Wiki**: a global, human-readable, editable and evolutive knowledge system that acts as the **guardian of Twin reasoning rules**.

This project is intentionally separate from the **Twin Capability Registry**. Do not implement the capability registry here. The registry answers **“what Twin can do / what already exists”**. This repository must answer **“how Twin should reason”**.

Before modifying code:

1. Inspect the current repository structure, existing ingestion pipeline, storage model, prompts, indexing/search, update logic, tests and UI/API.
2. Reuse the existing LLM-Wiki mechanisms whenever they fit.
3. Avoid a rewrite unless technically necessary.
4. Identify the smallest architectural changes required to reach the target described below.
5. Preserve working functionality unless it conflicts with the target architecture.
6. Add tests for every new core behavior.

---

# 1. Product definition

## 1.1 What the Twin Reasoning Wiki is

The Twin Reasoning Wiki is a persistent repository of:

- reasoning rules;
- reasoning methods;
- decomposition patterns;
- design doctrines;
- decision frameworks;
- reusable reasoning structures;
- examples;
- counter-examples;
- anti-patterns;
- domain-specific reasoning;
- entity/scope-specific reasoning variants;
- rules that help transform an intention into functional steps;
- rules that help transform functional steps into implementation patterns.

Examples of knowledge that belongs here:

- how to understand a user intention;
- how to decompose a prompt into macro-intentions;
- how to perform functional decomposition;
- how to choose the right granularity of a functional step;
- how to decompose a slide/presentation need;
- how to reason about architecture;
- how to decide whether a reasoning step should become a Skill, a Subagent, a Tool, a Workflow, deterministic code, etc.;
- how a specific business entity should adapt a generic reasoning pattern;
- reusable architecture/design principles;
- known reasoning anti-patterns.

The Wiki is therefore a **reasoning knowledge network**, not a general enterprise document repository.

## 1.2 What it is not

Do NOT turn this project into:

- a capability registry;
- an inventory of existing Agents / Skills / MCP / APIs;
- an operational data store;
- an event/state database;
- a generic data lake;
- a GraphRAG project whose graph becomes the primary user-facing knowledge representation;
- a black-box vector database;
- a system that silently rewrites source documents.

Operational/current-state knowledge and capability inventory belong elsewhere.

---

# 2. Core architectural principle: two strata only

For the initial architecture, keep the model deliberately simple:

```text
RAW KNOWLEDGE
PDF / Word / Markdown / Excel / Confluence exports / mails / text / etc.
        |
        | knowledge compilation
        v
TWIN REASONING WIKI
structured / consolidated / linked / editable / human-readable
        |
        v
Twin Steps / Agents / Skill Builder / Harness
```

There is **no separate Knowledge Ledger** in this version.

## 2.1 Raw layer

The Raw layer contains the original knowledge sources.

Responsibilities:

- preserve original content;
- preserve source identity and provenance;
- preserve source version/date when available;
- preserve enough structure to retrieve an exact section later;
- remain accessible for high-fidelity verification.

Raw sources should not be silently modified by the LLM.

Think of Raw as:

> “What did the original source actually say?”

## 2.2 LLM-Wiki layer

The Wiki is the compiled, structured and navigable representation.

Responsibilities:

- consolidate dispersed knowledge;
- organize reasoning knowledge into coherent pages;
- create links between related reasoning concepts;
- remove unnecessary duplication;
- detect potential inconsistencies;
- support scope/entity-specific variants;
- be directly readable and editable by humans;
- provide the normal knowledge path used by Twin reasoning agents.

Think of the Wiki as:

> “What has Twin understood and capitalized about how it should reason?”

---

# 3. One global Wiki, not many independent Wikis

Build **one logical Twin Reasoning Wiki**.

Do not create isolated Wikis per use case.

Instead, support slices / namespaces / tags that allow an agent to retrieve only the relevant subset.

Example logical organization:

```text
Twin Reasoning Wiki
|
+-- Intent Understanding
+-- Prompt Decomposition
+-- Functional Decomposition
+-- Architecture Reasoning
+-- Implementation Pattern Selection
+-- Agent Design
+-- Subagent Design
+-- Skill Design
+-- Tool / Workflow Design
+-- Slide / Presentation Decomposition
+-- Data / Analysis Reasoning
+-- Business-domain Reasoning
+-- Entity-specific Overlays
+-- Examples
+-- Anti-patterns
```

A single piece of reasoning knowledge may participate in several slices.

Example:

```text
"Separate functional decomposition from technical implementation"
```

may be tagged as relevant to:

- functional decomposition;
- architecture;
- agent design;
- skill design.

This avoids duplicated truths across independent Wikis.

---

# 4. Metadata and slicing model

Every Wiki page or knowledge unit should support lightweight structured metadata.

Keep the taxonomy small and controlled.

Recommended initial fields:

```yaml
id: stable-id
title: Human readable title

domain:
  - functional-analysis

reasoning_type:
  - decomposition

scope:
  - global

entity:
  - all

knowledge_type:
  - principle

tags:
  - functional-decomposition
  - granularity

status: active

source_refs:
  - raw://source-id#section-id

related_pages:
  - wiki://another-page-id

last_updated: ISO_DATE
```

Suggested controlled dimensions:

- `domain`
- `reasoning_type`
- `knowledge_type`
- `scope`
- `entity`
- `tags`
- `status`
- `source_refs`
- `related_pages`

Do not create hundreds of mandatory tags.

The purpose of metadata is to let a Knowledge Resolver ask:

> “Give me reasoning knowledge for functional decomposition, for this domain/entity/scope.”

---

# 5. Canonical knowledge + contextual overlays

Reasoning can vary by entity, scope or context.

Do not duplicate complete pages whenever possible.

Use a model similar to:

```text
Canonical reasoning
        +
Contextual overlay
        =
Applicable reasoning
```

Example:

```markdown
# Functional Decomposition

## Global principles
1. Understand intent first.
2. Decompose by functional outcome.
3. Do not mix functional decomposition and implementation.
4. Identify dependencies.
5. Keep coherent granularity.

## Entity overlays

### CIB
- consider legal entity boundaries;
- consider booking location;
- consider specific criticality constraints.

### Retail
- consider customer journey;
- consider channel/country.
```

Or store overlays as separate linked pages if that matches the current repository architecture better.

The resolver must be capable of building the effective reasoning context from:

```text
GLOBAL + DOMAIN + ENTITY/SCOPE OVERLAY
```

---

# 6. Knowledge ingestion / compilation

The project must support knowledge that does **not already exist as a clean document**.

This is fundamental.

The source knowledge may be scattered across:

- Confluence;
- Word;
- PDFs;
- PowerPoint/text exports;
- emails;
- existing Markdown;
- architecture documents;
- meeting notes;
- human expert input;
- previously generated reasoning documents.

The ingestion/compiler pipeline should conceptually support:

```text
Raw sources
    |
    v
Extract / normalize
    |
    v
Identify reusable reasoning knowledge
    |
    v
Compare with existing Wiki
    |
    +--> new knowledge
    +--> enrichment
    +--> duplicate
    +--> contextual variant
    +--> possible contradiction
    |
    v
Propose Wiki change
    |
    v
Validate / apply
```

Do not treat ingestion as simple summarization.

The goal is to extract:

- principles;
- decision rules;
- sequences of reasoning;
- patterns;
- exceptions;
- contextual variants;
- anti-patterns;
- definitions needed to reason correctly;
- examples that teach the reasoning.

---

# 7. Human editability is a first-class requirement

One of the reasons for choosing the Wiki model is to avoid a black-box knowledge representation.

A human expert must be able to:

1. open a Wiki page;
2. understand what Twin believes;
3. inspect the sources;
4. modify the reasoning text directly;
5. add/remove a rule;
6. add an example;
7. add an entity-specific overlay;
8. resolve a conflict;
9. save the change;
10. make the updated knowledge immediately retrievable.

Prefer Markdown or another plain-text representation as the canonical editable Wiki format.

If vector indexing/search is used internally, treat it as a derived index, not the authoritative representation.

```text
Wiki Markdown/text = knowledge representation
Index/vector/search = retrieval acceleration
```

A user should never need to understand or manually operate embeddings or a graph database to maintain reasoning knowledge.

---

# 8. Provenance

Every significant Wiki rule should remain traceable to its origin when an origin exists.

Support source references such as:

```text
raw://document-id#section-id
raw://document-id?page=12
raw://email-id
raw://confluence-page-id#heading
```

The Wiki may synthesize multiple sources.

Example:

```yaml
source_refs:
  - raw://architecture-guidelines#agent-design
  - raw://meeting-notes-2026-07-12#decision-4
  - raw://existing-functional-decomposition-md#principles
```

A source reference must allow later retrieval of the exact original passage if possible.

---

# 9. Wiki vs Raw routing policy

The default reasoning path must be:

```text
QUESTION / KNOWLEDGE NEED
          |
          v
        WIKI
```

Do **not** query Wiki and Raw systematically in parallel.

The Raw layer is a **high-fidelity escalation path**.

Use Raw when one or more of the following is true:

1. **Precision required**
   - exact definition;
   - exact rule;
   - exact value;
   - exact wording matters.

2. **Exhaustiveness required**
   - all exceptions;
   - all conditions;
   - complete list;
   - omission could invalidate the answer.

3. **Decision impact is high**
   - missing information may change the functional or architectural decision.

4. **Exception sensitivity**
   - a hidden exception could materially change the reasoning.

5. **Ambiguity or conflict**
   - Wiki contains competing interpretations or insufficient confidence.

6. **Wiki insufficiency**
   - Wiki does not contain enough knowledge to answer safely.

Macro rule:

> Wiki for reasoning. Raw for fidelity.

Or more precisely:

> Use the Wiki as the normal reasoning knowledge source; descend to Raw only when fidelity, completeness, ambiguity resolution or decision criticality requires it.

---

# 10. Conflict detection without a separate Ledger

The Wiki must not silently erase real contradictions.

When new knowledge is ingested, compare it to relevant existing Wiki knowledge.

First distinguish:

## 10.1 Contextual difference

Not a real conflict.

Examples:

- different entity;
- different scope;
- different domain;
- different applicability;
- different time/version.

Store both as contextual variants/overlays.

## 10.2 Genuine conflict

A genuine conflict exists when two incompatible rules apply to:

- the same concept;
- the same scope/entity;
- the same effective context;
- with no clear precedence.

Example:

```text
Rule A:
For this decomposition, identify criticality before incidents.

Rule B:
For the same scope, identify incidents before criticality.
```

Do not automatically choose.

Represent it visibly:

```yaml
conflict_status: unresolved
conflicts_with:
  - wiki://rule-b
```

And expose a human-readable conflict section.

Provide a simple way to list unresolved conflicts:

```text
/conflicts
```

or equivalent API/UI/CLI depending on the existing repository.

When a human resolves a conflict:

- preserve both source references;
- record which reasoning became canonical;
- preserve the rejected/superseded alternative for audit;
- remove the unresolved status.

---

# 11. Suggested Wiki page structure

A reasoning page should be optimized for both humans and LLM consumption.

Recommended structure:

```markdown
---
metadata...
---

# Title

## Purpose
What reasoning problem this page addresses.

## Applicability
Where/when this reasoning applies.

## Core principles
The reusable reasoning rules.

## Reasoning sequence
If relevant, an ordered reasoning process.

## Decision rules
Conditions / choices / branching logic.

## Contextual variants
Domain/entity/scope-specific differences.

## Examples
Representative examples.

## Anti-patterns
What should not be done and why.

## Related reasoning
Links to other Wiki pages.

## Sources
Links to Raw evidence.

## Known conflicts
Only if relevant.
```

Not every page must contain every section.

---

# 12. Primary consumption patterns

The same Wiki must serve several Twin consumers.

## 12.1 Step 1 — Intent understanding

Typical Wiki slices:

- intent understanding;
- domain vocabulary;
- ambiguity resolution;
- macro-intent decomposition;
- scope interpretation.

Question answered:

> “How should I understand this request?”

## 12.2 Step 2 — Functional decomposition

Typical slices:

- functional decomposition;
- decomposition granularity;
- dependency identification;
- domain reasoning;
- functional patterns;
- anti-patterns.

Question answered:

> “How should this intention be decomposed into coherent functional steps?”

## 12.3 Step 3 — Implementation reasoning

Typical slices:

- architecture reasoning;
- agent design;
- skill design;
- subagent design;
- workflow/tool design;
- implementation-pattern selection.

Question answered:

> “How should this functional step be materialized architecturally?”

Important: this Wiki provides **reasoning doctrine**, not the list of existing capabilities.

The separate Twin Capability Registry will later answer whether a capability already exists.

---

# 13. Skill Builder integration

The Wiki must be usable as a knowledge source for the Skill Builder.

A Skill Builder should combine:

```text
User intent / user-authored reasoning
        +
Relevant Wiki reasoning knowledge
        =
Proposed executable Skill
```

Example:

User says:

> “For this analysis, first determine the perimeter, then criticality, then historical context.”

The Skill Builder may query Wiki slices such as:

- operational analysis pattern;
- skill design principles;
- decomposition rules;
- domain-specific reasoning.

The Wiki helps the Skill Builder:

- structure the reasoning;
- identify missing steps;
- avoid anti-patterns;
- apply domain rules;
- generate a consistent Skill.

Important distinction:

```text
Wiki = reusable reasoning knowledge
Skill = executable / procedural reasoning
```

A Skill is allowed to contain behavior specific to that Skill that does not belong in the global Wiki.

---

# 14. Learning loop from Skills and human feedback

When a user modifies a generated Skill, distinguish:

## Skill-specific preference

Example:

> “For this one Skill, return JSON instead of Markdown.”

Keep it local to the Skill.

## Generalizable reasoning knowledge

Example:

> “For all CIB application reviews, booking entity must be resolved before historical analysis.”

This may belong in the Wiki.

Support a mechanism where the Skill Builder or another agent can propose:

```text
Proposed Wiki Update
```

The proposal must not silently alter global reasoning knowledge.

Preferred flow:

```text
User feedback
     |
     v
Classify
     |
     +--> Skill-specific -> update Skill
     |
     +--> Generalizable -> propose Wiki update
                              |
                              v
                         Human validation
                              |
                              v
                            Wiki
```

---

# 15. Knowledge Resolver contract

Provide a simple API/service/function allowing agents to ask the Wiki for reasoning context.

Conceptual request:

```json
{
  "query": "How should I decompose a daily application-scope review?",
  "step": "functional_decomposition",
  "domain": ["application_operations"],
  "reasoning_type": ["decomposition"],
  "scope": ["global"],
  "entity": ["CIB"],
  "precision_required": "low",
  "exhaustiveness_required": "low",
  "decision_impact": "medium"
}
```

Conceptual response:

```json
{
  "wiki_context": [
    {
      "page_id": "functional-decomposition",
      "title": "Functional Decomposition",
      "content": "...",
      "applicability": "...",
      "source_refs": []
    }
  ],
  "raw_context": [],
  "conflicts": [],
  "retrieval_notes": {
    "raw_escalation": false
  }
}
```

When Raw escalation is required:

```json
{
  "wiki_context": [...],
  "raw_context": [
    {
      "source_id": "...",
      "section": "...",
      "content": "exact original passage"
    }
  ],
  "conflicts": [],
  "retrieval_notes": {
    "raw_escalation": true,
    "reason": "decision_critical_rule"
  }
}
```

Adapt names and schemas to the existing repository rather than forcing these exact structures.

---

# 16. Retrieval behavior

Do not build a retrieval system that only performs a single broad query.

Allow a reasoning agent / resolver to decompose a knowledge need.

Example:

```text
Functional decomposition of a daily application check
```

may trigger Wiki searches for:

1. application scope reasoning;
2. operational health reasoning;
3. historical analysis;
4. anomaly detection;
5. prioritization;
6. synthesis;
7. functional decomposition principles.

Support iterative:

```text
search -> read -> follow related page -> evaluate sufficiency
```

with a clear stop condition.

Avoid uncontrolled agent loops.

---

# 17. Minimal sufficiency / stop condition

The resolver should be able to stop when it has enough knowledge.

For a knowledge need, consider:

- applicable definition found?
- relevant reasoning principles found?
- necessary contextual overlay found?
- critical rules found?
- known exceptions found if needed?
- unresolved conflict present?
- enough evidence to proceed?

If sufficient:

```text
STOP RETRIEVAL
```

If not:

- follow related Wiki pages;
- broaden the Wiki search;
- or escalate selectively to Raw.

---

# 18. Source ingestion UX

The first useful product version should make it easy to feed knowledge into the Wiki.

Support, at minimum, whatever is already easiest in the fork, ideally:

- Markdown/text files;
- PDF;
- Word/docx if current dependencies allow;
- Excel/xlsx if current dependencies allow;
- structured pasted text;
- manually authored Wiki pages.

Later adapters can cover:

- Confluence;
- email;
- SharePoint;
- other enterprise sources.

Do not block the architecture on enterprise connectors.

Local-file ingestion is enough for the first milestone.

---

# 19. User-provided expert knowledge

Because important knowledge may exist only in people’s heads, support direct expert contribution.

Example input:

> “In our architecture, do not create a subagent solely to wrap one deterministic API call.”

The system should be able to classify this as:

```text
knowledge_type = anti_pattern
domain = agent_design
reasoning_type = implementation_pattern_selection
```

and propose a Wiki insertion/update.

Human expert knowledge is a first-class source.

---

# 20. Update strategy

When new source knowledge arrives, do not recreate the entire Wiki blindly.

Prefer incremental compilation:

```text
new source
   |
   v
identify impacted reasoning topics
   |
   v
retrieve relevant existing Wiki pages
   |
   v
compare
   |
   +--> no change
   +--> enrich
   +--> new contextual overlay
   +--> propose rewrite
   +--> conflict
   |
   v
apply validated update
```

Preserve stable page IDs when possible.

Preserve links between pages.

Preserve provenance.

---

# 21. No silent destructive updates

LLM-generated Wiki changes should preferably be staged as a proposal/diff before destructive replacement, especially when:

- an existing rule is removed;
- applicability changes;
- a contradiction is detected;
- a large section is rewritten;
- source evidence is weak.

For simple additive enrichment, automatic update may be configurable.

Design the code so approval policy can later be made stricter.

---

# 22. Search / indexing implementation guidance

The user-facing canonical knowledge must remain readable Wiki text.

You may use:

- lexical search;
- full-text search;
- embeddings;
- vector search;
- lightweight indexes;

if useful.

But:

> indexes are derived artifacts, not the knowledge source.

Do not require users to manually manage embeddings.

Do not make a graph database mandatory for the initial version.

If the current fork already uses embeddings/search, preserve them where useful.

---

# 23. Raw retrieval implementation guidance

Raw retrieval should support retrieving the original context around a source reference.

Prefer:

```text
small retrieval unit for search
+
larger parent section for reasoning
```

Example:

```text
match sentence/chunk
        |
        v
retrieve parent heading/section
        |
        v
send sufficient original context
```

Do not automatically send complete 100-page documents unless explicitly required.

---

# 24. Out-of-scope integration boundary: Twin Capability Registry

Do not implement the Capability Registry in this repository.

However, keep the architecture clean so a future orchestrator can combine:

```text
Twin Reasoning Wiki
= HOW SHOULD TWIN REASON?

Twin Capability Registry
= WHAT CAN TWIN ALREADY DO?
```

Expected future flow:

```text
User intention
    |
    v
Reasoning Wiki
    |
    v
Functional decomposition
    |
    v
Reasoning Wiki
    |
    v
Implementation pattern
    |
    v
Capability Registry
    |
    v
Reuse / extend / create decision
```

The Wiki should not contain dynamic capability inventory just to compensate for the absence of the registry.

---

# 25. Example end-to-end scenario

User request:

> “Help me check my application scope every morning.”

## Step 1 — Intent understanding

Query Wiki slice:

```text
intent_understanding
application_scope
operational_review
```

Expected output:

```text
Intent:
Recurring operational review of an application perimeter.

Goal:
Identify changes/anomalies requiring attention.
```

## Step 2 — Functional decomposition

Query Wiki slices:

```text
functional_decomposition
application_scope_reasoning
operational_health
historical_analysis
anomaly_detection
prioritization
daily_synthesis
```

Expected functional steps:

```text
1. Resolve application scope
2. Build current state
3. Retrieve historical context
4. Detect deviations/anomalies
5. Qualify and prioritize
6. Produce daily synthesis
```

## Step 3 — Implementation reasoning

Query Wiki slices:

```text
implementation_pattern_selection
skill_design
subagent_design
tool_design
workflow_design
```

Expected result:

For each functional step, recommend the architectural pattern based on the Wiki’s reasoning doctrine.

The separate registry may later verify whether a corresponding capability already exists.

---

# 26. Recommended initial repository capabilities

The adapted fork should target these first-class capabilities:

## A. Raw Source Store
- source ID;
- source metadata;
- normalized text;
- original file reference/path;
- section/chunk references.

## B. Wiki Page Store
- editable Markdown/text;
- front-matter metadata;
- stable page IDs;
- cross-links;
- source references.

## C. Knowledge Compiler
- ingest source;
- identify reasoning knowledge;
- find impacted pages;
- propose new/update/overlay/conflict;
- generate structured Wiki updates.

## D. Conflict Detector
- compare new claims/rules with applicable Wiki knowledge;
- distinguish context variant vs real contradiction;
- record unresolved conflicts.

## E. Wiki Search / Resolver
- metadata filtering;
- semantic/text search as appropriate;
- related-page navigation;
- contextual overlay resolution;
- Raw escalation.

## F. Human Editing
- direct Wiki modification;
- source visibility;
- conflict resolution;
- update/re-index after edit.

## G. API / Programmatic Interface
- search reasoning;
- resolve reasoning context;
- get Wiki page;
- get Raw source/section;
- list conflicts;
- propose Wiki update.

Use the existing UI/API patterns in the fork where possible.

---

# 27. Suggested development phases

## Phase 0 — Repository audit

Produce a short technical assessment:

- what already exists;
- what can be reused unchanged;
- what should be adapted;
- what is missing;
- proposed target module boundaries;
- migration risks.

Do this before major refactoring.

## Phase 1 — Global Wiki + metadata + Raw provenance

Deliver:

- one global Wiki;
- metadata/slices;
- Raw source references;
- direct editing;
- basic search/filtering.

## Phase 2 — Knowledge compiler

Deliver:

- ingest a document;
- detect relevant reasoning knowledge;
- create/update Wiki pages incrementally;
- preserve provenance.

## Phase 3 — Resolver + Raw escalation

Deliver:

- query by step/domain/reasoning type/scope/entity;
- contextual overlays;
- Wiki-first retrieval;
- selective Raw fallback.

## Phase 4 — Conflict management

Deliver:

- genuine conflict detection;
- contextual-difference detection;
- conflict list;
- human resolution;
- provenance preservation.

## Phase 5 — Skill Builder / agent consumption

Deliver:

- clean programmatic interface;
- sample Skill Builder integration;
- examples for Step 1 / Step 2 / Step 3.

---

# 28. Acceptance criteria

The architecture is successful when the following scenarios work.

## AC1 — Wiki is human-readable

An architect can open the Wiki and understand the reasoning rules without inspecting embeddings, graph structures or database internals.

## AC2 — Wiki is directly editable

A human changes a reasoning rule and agents can retrieve the updated rule without rebuilding the whole system manually.

## AC3 — Source traceability

A Wiki principle can link back to one or more original Raw sources.

## AC4 — Incremental enrichment

A new document enriches an existing Wiki page rather than blindly creating a duplicate.

## AC5 — Contextual variant

A CIB-specific rule can coexist with the global reasoning rule and be selected when `entity=CIB`.

## AC6 — Conflict visibility

Two incompatible rules for the same scope/context create an explicit unresolved conflict rather than silent arbitrary merging.

## AC7 — Wiki-first retrieval

A normal reasoning request is answered using Wiki knowledge without unnecessary Raw retrieval.

## AC8 — Raw escalation

A high-precision/critical/exhaustive question can retrieve the exact relevant Raw section.

## AC9 — Step-specific slices

Step 1, Step 2 and Step 3 can query different subsets of the same global Wiki.

## AC10 — Skill Builder consumption

A Skill Builder can combine user instructions with relevant Wiki reasoning rules to propose an executable Skill.

## AC11 — No capability-registry pollution

The Wiki does not become an inventory of current Twin capabilities.

## AC12 — No black-box dependency

The system remains useful and governable even if vector/graph indexes are rebuilt or replaced.

---

# 29. Engineering principles

Prefer:

- simple architecture first;
- explicit data models;
- stable IDs;
- plain-text/Markdown canonical Wiki pages;
- incremental updates;
- provenance everywhere;
- human-visible diffs;
- deterministic metadata filtering where possible;
- LLMs for semantic interpretation, synthesis and conflict detection;
- tests for LLM-independent logic;
- modular LLM provider abstraction.

Avoid:

- unnecessary microservices;
- mandatory graph databases;
- duplicating the same knowledge in multiple independent Wikis;
- silently overwriting expert knowledge;
- sending the full Raw corpus to every agent;
- treating vector search as the source of truth;
- coupling Wiki logic tightly to the Capability Registry;
- building enterprise connectors before the core reasoning model works.

---

# 30. What Opus 4.6 should do now

After reading this specification:

1. Inspect the current fork in detail.
2. Map existing components to this target architecture.
3. Produce a concise gap analysis.
4. Propose the minimal-change implementation plan.
5. Implement the plan incrementally.
6. Keep existing working features where compatible.
7. Add/update tests.
8. Add a small set of seed reasoning pages demonstrating:
   - intent understanding;
   - functional decomposition;
   - implementation pattern selection;
   - skill design;
   - subagent design.
9. Add one end-to-end demo using:
   - “Help me check my application scope every morning.”
10. Demonstrate:
   - Wiki-first retrieval;
   - entity/scope overlay;
   - Raw fallback;
   - conflict detection;
   - direct human Wiki edit;
   - programmatic consumption by a mock Skill Builder.

Do not over-engineer beyond these requirements until the above workflow is functional and testable.

---

# 31. Short architecture statement

Use this as the guiding principle when making implementation choices:

> **Twin Reasoning Wiki is the human-readable and evolutive guardian of Twin reasoning rules. Raw sources preserve fidelity; the Wiki consolidates, structures and contextualizes reasoning knowledge; Twin agents and Skill Builders consume targeted Wiki slices and fall back to Raw only when precision, completeness, ambiguity or decision criticality requires it.**

And keep the boundary clear:

> **Reasoning Wiki = how Twin should think. Capability Registry = what Twin can do.**
