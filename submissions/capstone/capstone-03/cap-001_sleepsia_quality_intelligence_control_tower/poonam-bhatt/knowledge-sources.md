# Knowledge Sources

## 1. Purpose

The Quality Intelligence Control Tower uses approved internal quality knowledge and approved public product information to support quality investigations, product questions, and operational guidance.

Knowledge retrieval is evidence-driven. The supervisor and child agents must use the appropriate knowledge source only when the requested analysis requires it.

Knowledge sources must not override configured quality policy, investigation rules, specialist findings, or authoritative internal data.

---

## 2. Approved Knowledge Sources

The solution uses three approved knowledge documents as the primary knowledge sources for the Sleepsia quality workflow.

### Knowledge Source 1 — Product / Quality Knowledge

Purpose:
- Product information
- Product characteristics
- Approved product descriptions
- Product-related quality context
- Product care and use information

Used by:
- Supervisor Agent
- Product/Batch Specialist
- Customer Impact Specialist
- Product-care related interactive queries

---

### Knowledge Source 2 — Quality Investigation / Policy Knowledge

Purpose:
- Quality investigation procedures
- Investigation requirements
- Quality escalation guidance
- Evidence handling
- Investigation and decision-process guidance

Used by:
- Quality Supervisor
- Incident Intake & Validation topic
- Quality Investigation Decision topic
- CAPA Planning & Ownership topic
- Evidence Update & Selective Reassessment topic

The configured decision rules remain authoritative for final quality classification.

---

### Knowledge Source 3 — Product Care / Customer Support Knowledge

Purpose:
- Approved product-use guidance
- Product-care information
- Customer-support guidance
- Approved responses to general product questions

Used by:
- Quality Supervisor
- Product/Batch Specialist when relevant
- Interactive customer/product questions

This source must not be used to determine internal quality severity.

---

## 3. Approved Sleepsia URLs

Public product questions must use approved Sleepsia public sources.

Approved source pattern:

- Official Sleepsia website
- Approved Sleepsia product pages
- Approved Sleepsia support/product-care pages

Public sources are used only for public product information.

Public product information must not override internal quality records or quality policy.

If an approved Sleepsia URL is unavailable, the agent must not invent product information. It should report that the requested information is unavailable or direct the user to the approved support channel.

---

## 4. Source Precedence

When multiple sources provide information, use the following precedence:

1. Configured internal quality policy and decision rules
2. Authoritative internal operational data
3. Approved internal knowledge documents
4. Approved Sleepsia public product information
5. Microsoft/M365 guidance when specifically required

Public product information must never override internal quality evidence.

Microsoft guidance must not influence Sleepsia quality severity.

Specialist findings must be based on current validated evidence.

The Quality Investigation Decision topic is the authoritative source for final classification.

---

## 5. Knowledge Retrieval Rules

The supervisor must determine whether knowledge retrieval is required before calling a knowledge source.

Use knowledge when:

- The user asks a product-care or product-use question.
- A specialist requires documented product information.
- The investigation requires approved quality-policy guidance.
- Microsoft/M365 operational guidance is specifically requested.
- A response must be grounded in approved documentation.

Do not retrieve knowledge unnecessarily when the required information is already available in the current investigation context or authoritative data source.

Never fabricate a knowledge-source result.

---

## 6. Investigation vs Public Product Questions

### Internal Quality Investigation

For an internal quality investigation:

- Internal quality records are authoritative.
- Complaint, return, product, batch, customer, safety, and CAPA evidence must come from configured internal sources.
- Knowledge documents provide supporting policy/context.
- Public product information must not be used to change classification.

Example:

> "Investigate the quality issue for SKU SLP-1002."

The supervisor should use the configured investigation workflow and internal evidence sources.

---

### Public Product Question

For a public product question:

- Use approved Sleepsia public information.
- Do not apply internal incident-classification rules.
- Do not expose internal investigation records.
- Do not present internal quality findings as public product facts.

Example:

> "How should I care for this Sleepsia pillow?"

The agent should retrieve approved product-care guidance rather than starting a quality investigation.

---

## 7. Safety and Quality Evidence

Safety-related evidence must be handled using the configured quality workflow.

Examples include:

- Burning smell
- Heat
- Potential injury
- Safety complaint
- Potential safety cluster

The Safety Specialist and configured decision topic determine how safety evidence affects the investigation.

If confirmed:

`SafetyIndicator = Yes`

the configured decision policy takes precedence and results in:

`Critical Escalation`

Public product information must not be used to downgrade or dismiss an internal safety finding.

---

## 8. Missing or Unavailable Knowledge

If a required knowledge source cannot be retrieved:

- Do not invent the missing information.
- Record the knowledge retrieval failure.
- Continue the core quality workflow when the missing source is not required for the quality decision.
- If the missing source is essential, mark the affected analysis as unavailable or Insufficient Evidence.
- Identify the missing source in the final result.

For Microsoft/M365 guidance specifically:

- Use the M365 Guidance Specialist when required.
- If Microsoft guidance is unavailable, the core Sleepsia quality workflow should continue when possible.
- The unavailable guidance must be explicitly reported.

---

## 9. Retrieval Test Coverage

Knowledge retrieval should be tested for the following scenarios:

| Test | Expected Behaviour |
|---|---|
| Approved product question | Retrieve approved Sleepsia product information |
| Product-care question | Retrieve approved product-care guidance |
| Internal quality investigation | Use internal quality evidence and configured policy |
| Quality policy question | Retrieve applicable approved policy knowledge |
| Public product question | Use approved Sleepsia public source |
| Public source unavailable | Do not fabricate product information |
| Internal policy conflicts with public information | Internal configured policy takes precedence |
| M365 guidance request | Use M365 Guidance Specialist |
| M365 guidance unavailable | Core quality workflow continues where possible |
| Safety investigation | Internal safety evidence and configured policy take precedence |

---

## 10. Knowledge Boundaries

Knowledge sources are supporting evidence and guidance.

They must not be used to:

- Invent complaint records
- Invent return records
- Invent SKU or batch information
- Invent customer impact
- Invent CAPA status
- Override specialist findings without new evidence
- Override configured decision rules
- Create a quality classification independently of Topic 2
- Approve recalls
- Approve refunds
- Issue public safety statements

The supervisor remains responsible for orchestration and final workflow control.

---

## 11. Evidence Integrity

Every knowledge-derived conclusion must remain distinguishable from operational data.

The agent must preserve:

- Source used
- Relevant finding
- Evidence status
- Any retrieval failure
- Any unresolved evidence gap

The agent must never claim that a document, URL, or knowledge source was successfully retrieved unless the configured retrieval mechanism confirms the result.

---

## 12. Summary

The knowledge architecture separates:

**Internal quality evidence**
→ Investigation and classification

**Approved internal knowledge**
→ Policy, procedures, product and quality context

**Approved Sleepsia public information**
→ Public product and care questions

**Microsoft guidance**
→ M365/Copilot/Teams operational guidance

The Quality Supervisor controls source selection and ensures that knowledge retrieval supports, rather than overrides, the configured quality investigation workflow.