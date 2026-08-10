# knowledge-sources.md

# CAP-001 — Knowledge Sources

## 1. Overview

The Sleepsia Product Quality & Customer Experience Intelligence Control Tower uses approved knowledge sources to provide authoritative guidance for product quality, customer experience, escalation, CAPA, and product-related queries.

Knowledge sources are scoped to the agents that require them.

## 2. Knowledge Source Inventory

| # | Knowledge Source | Purpose | Primary Consumers |
|---|---|---|---|
| 1 | Sleepsia Quality & Governance Policy | Defines quality classification, escalation, evidence, investigation, CAPA, and closure requirements. | Quality Supervisor, Quality Specialists |
| 2 | Sleepsia Product & Customer Experience Knowledge | Provides product, customer-experience, usage, and product-related information. | Relevant Quality Specialists, M365 Guidance Specialist |
| 3 | Approved Sleepsia Public Product Information | Provides approved public-facing product facts and customer-facing information. | M365 Guidance Specialist / Interactive Queries |

## 3. Knowledge Precedence

When multiple knowledge sources provide information relevant to a decision, the following precedence applies:

```text
Internal Quality & Governance Policy
              ↓
Internal Product / Customer Experience Knowledge
              ↓
Approved Public Product Information
```

Internal quality policy takes precedence for:

* Quality classification.
* Safety escalation.
* Investigation requirements.
* CAPA decisions.
* Evidence requirements.
* Closure requirements.
* Governance decisions.

Public product information must not override internal quality governance.

## 4. Quality & Governance Policy

The internal quality and governance policy is the authoritative source for operational quality decisions.

It is used to determine:

* Quality severity.
* Critical escalation.
* Investigation requirements.
* Evidence requirements.
* CAPA requirements.
* Owner and target-date expectations.
* Reassessment requirements.
* Closure conditions.
* Escalation requirements.

The Quality Supervisor remains responsible for applying the policy to the available operational evidence.

## 5. Product & Customer Experience Knowledge

Internal product and customer-experience knowledge is used to support:

* Product-related analysis.
* Customer-impact assessment.
* Product and batch interpretation.
* Product usage information.
* Customer experience context.
* Quality investigation context.

The source provides supporting evidence and context but does not override quality-governance rules.

## 6. Approved Public Product Information

Approved Sleepsia public product information may be used for appropriate interactive product queries and customer-facing product facts.

Examples include:

* Product features.
* Product usage.
* Product care.
* Publicly stated product information.

Public information is not treated as authoritative evidence for internal quality severity or CAPA decisions.

## 7. Knowledge Scoping

Knowledge access follows the principle of least privilege.

```text
Quality Supervisor
       │
       ├── Quality & Governance Knowledge
       │
       ├── Product / Customer Experience Knowledge
       │
       └── Approved Public Product Information
```

Specialists receive only the knowledge sources relevant to their responsibilities.

The M365 Guidance Specialist is responsible for Microsoft 365 guidance and uses the Microsoft Learn MCP integration where required.

## 8. Knowledge Usage Rules

The solution follows these rules:

1. Use approved knowledge sources for quality-related guidance.
2. Internal governance policy takes precedence over public information.
3. Do not use public product information to override internal quality decisions.
4. Do not infer missing quality evidence from general knowledge.
5. Do not treat unsupported information as confirmed evidence.
6. Specialist agents use knowledge only within their assigned domain.
7. The Quality Supervisor applies final governance decisions.
8. Knowledge retrieval failures must not be represented as successful retrieval.
9. Missing or conflicting evidence is surfaced to the Supervisor.
10. Safety and quality decisions remain evidence-based.

## 9. Retrieval and Decision Flow

```text
Quality / Product Query
        |
        ▼
Identify Required Knowledge Domain
        |
        ▼
Retrieve Applicable Approved Source
        |
        ▼
Evaluate Evidence
        |
        ▼
Apply Internal Governance Policy
        |
        ▼
Supervisor Decision
```

## 10. Knowledge and Operational Data Separation

Knowledge sources provide policy and contextual information.

Operational Excel data provides incident-specific evidence.

```text
Knowledge Sources
      │
      ├── Policy
      ├── Product Knowledge
      └── Approved Public Information
      │
      ▼
Governance / Context
      │
      └──────────────┐
                     ▼
              Quality Supervisor
                     ▲
                     │
      ┌──────────────┘
      │
Operational Data
      │
      ├── Complaints
      ├── Returns
      ├── Sales
      ├── Products
      ├── Batches
      ├── Incidents
      └── CAPA
```

The Supervisor combines approved knowledge with operational evidence before applying the final quality decision.

## 11. Knowledge Governance

Knowledge sources must remain:

* Authoritative.
* Scoped.
* Traceable.
* Consistent with the current governance policy.
* Separate from unsupported assumptions.

If a required source is unavailable, the system must not fabricate the missing information.

Where the missing information affects a quality decision, the incident is routed to the appropriate evidence or manual-review path.