# CAP-001 — Generative Topics

## 1. Overview

CAP-001 uses topic-based orchestration in Microsoft Copilot Studio. Generative topics interpret natural-language requests, identify intent, extract relevant entities, and route requests to the appropriate deterministic workflow.

The core principle is:

```text
User / Autonomous Event
        |
        v
Generative Understanding
        |
        v
Topic Selection
        |
        v
Input Collection
        |
        v
Deterministic Validation
        |
        v
Specialist Analysis
        |
        v
Quality Supervisor Decision
        |
        v
CAPA / Report / Notification
```

---

## 2. Purpose

Generative topics allow users to express requests naturally, for example:

- "Process this customer complaint."
- "Check whether this complaint needs investigation."
- "Analyze returns for this product."
- "Check whether this batch has previous incidents."
- "Reassess this incident using new evidence."
- "Create the investigation report."
- "This complaint may indicate a safety issue. What should happen?"

The generative layer provides understanding and routing. It must not replace deterministic quality rules.

---

## 3. Generative vs Deterministic Responsibilities

### Generative Responsibilities

- Understand natural-language requests.
- Identify user intent.
- Extract entities such as ComplaintID, SKU and BatchID.
- Identify the appropriate topic.
- Ask for missing information.
- Summarize validated tool results.
- Present results naturally.

### Deterministic Responsibilities

- Required-field validation.
- SKU validation.
- Batch validation.
- Duplicate/Processed checks.
- Threshold calculations.
- Safety precedence.
- Quality classification.
- CAPA state.
- Incident state.
- Reassessment.
- Manual Review routing.
- Tool failure handling.

The generative model must never override deterministic quality rules.

---

## 4. Main Generative Entry Topic

### Incident Intake & Validation

This is the primary entry topic for complaint and incident processing.

It recognizes requests such as:

```text
"Process complaint CMP001."
"Please investigate this customer complaint."
"Can you assess this quality incident?"
"Check this complaint against product and batch data."
```

The topic collects or extracts:

- ComplaintID
- SKU
- BatchID
- OrderID where applicable
- Complaint description
- Complaint category where available
- Complaint date where available

---

## 5. Input Extraction vs Validation

Extraction does not prove that data is valid.

Example:

```text
User:
"Process complaint CMP001 for SKU SKU123 from batch BATCH45."

Generative Extraction:
ComplaintID = CMP001
SKU = SKU123
BatchID = BATCH45

Then:

Product_Master lookup
        |
        v
Actual validation
```

The agent must not invent values when they are missing.

---

## 6. Missing SKU

If SKU is required and missing:

```text
SKU missing
    |
    v
Invalid
    |
    v
"SKU is required."
```

The workflow must stop before specialist analysis.

---

## 7. Product Validation

```text
SKU
 |
 v
Product Master Tool
 |
 +---- Found ------> Continue
 |
 +---- Not Found --> Invalid
```

Expected invalid result:

```text
Invalid: The provided SKU does not exist in the Product Master.
```

---

## 8. Batch Validation

```text
BatchID
   |
   v
Batch Register
   |
   v
Batch Record
   |
   v
Compare Batch SKU
   |
   v
Complaint SKU
```

If the BatchID does not correspond to the complaint SKU, the workflow must reject the relationship.

---

## 9. Duplicate Processing Protection

The workflow checks the `Processed` value.

```text
Processed = Yes
       |
       v
Already Processed
       |
       v
Stop duplicate processing
```

Expected response:

```text
Invalid: This complaint has already been processed.
```

If:

```text
Processed = No
```

the complaint can continue.

---

## 10. Specialist Routing

After validation, the Quality Supervisor routes work to the appropriate specialist topics.

Possible specialists include:

- Customer Complaint Specialist
- Returns Specialist
- Product/Batch Specialist
- Safety Specialist
- CAPA Specialist

The generative layer must not bypass the Supervisor orchestration layer.

---

## 11. Complaint Analysis Topic

Purpose:

- Analyze complaint patterns.
- Identify complaint clusters.
- Return structured findings.

Example:

> "Check whether recent complaints for this SKU form a quality cluster."

The specialist provides evidence and findings. The Quality Supervisor owns the final classification.

---

## 12. Returns Analysis Topic

The Returns Specialist uses:

- Returns
- Sales_Summary

Conceptually:

```text
Return Rate = Returns / Sales
```

The configured project threshold is:

```text
Return Rate >= 2%
```

This supports:

```text
Investigation Required
```

unless a higher-priority rule applies.

---

## 13. Product / Batch Analysis Topic

The Product/Batch workflow validates:

- Product identity.
- SKU.
- BatchID.
- Batch/SKU relationship.
- Relevant historical information.

It must rely on operational data and must not create unsupported product or batch facts.

---

## 14. Safety Analysis Topic

A safety-related request is routed to the Safety Specialist.

```text
Safety Indicator
       |
       v
Safety Specialist
       |
       v
Quality Supervisor
       |
       v
Critical Escalation
       |
       v
Supervisor Validation
```

The system must not autonomously:

- Announce a public recall.
- Issue a public safety statement.
- Stop marketplace sales.
- Promise customer compensation.

---

## 15. Quality Decision Topic

The Quality Supervisor combines validated specialist findings.

Possible classifications:

```text
Informational
Complaint Cluster
Investigation Required
High-Priority Quality Incident
Critical Escalation
Manual Review
```

The final decision is rule-driven.

---

## 16. Decision Precedence

Safety-related rules have priority over lower-level classifications.

Example:

```text
Complaint Cluster
+
Safety Indicator
        |
        v
Critical Escalation
```

Generative reasoning must not downgrade a safety case.

---

## 17. Missing Evidence

If required evidence is unavailable:

```text
Missing Evidence
       |
       v
Insufficient Evidence
       |
       v
Manual Review
```

The model must not fabricate missing evidence.

---

## 18. CAPA Topic

When CAPA is required:

```text
Quality Decision
      |
      v
CAPA Topic
      |
      v
Owners Lookup
      |
      v
CAPA_Register
```

Possible CAPA fields include:

- IncidentID
- Classification
- ContainmentAction
- CorrectiveAction
- PreventiveAction
- OwnerRole
- TargetDate
- ValidationMethod
- Status

---

## 19. Report Generation Topic

After Supervisor validation:

```text
Validated Decision
       |
       v
Report Topic
       |
       v
Word Online
       |
       v
Product Quality Investigation Report
```

The report must reflect validated information and must not change the quality classification.

---

## 20. Notification Topic

After validation:

```text
Validated Action
      |
      v
Notification Topic
      |
      v
Office 365 Outlook
      |
      v
Internal Notification
```

Notification information may include:

- IncidentID
- SKU
- BatchID
- Final Classification
- Decision Rationale
- Required Action
- OwnerRole
- TargetDate

Only approved internal recipients should be used.

---

## 21. Reassessment Topic

Reassessment is used when new evidence becomes available.

Example:

> "Reassess incident INC001 because new batch evidence has arrived."

Flow:

```text
Existing Incident
       |
       v
New Evidence
       |
       v
Reassessment
       |
       v
Specialist Analysis
       |
       v
Quality Supervisor
       |
       v
New / Confirmed Classification
```

The workflow must not create a duplicate incident unnecessarily.

---

## 22. Manual Review Topic

Manual Review is used when:

- Evidence is insufficient.
- Required data cannot be retrieved.
- A specialist fails.
- A required tool fails.
- The quality decision cannot be safely automated.
- A policy exception requires human review.

```text
Automation Boundary
       |
       v
Manual Review
       |
       v
Human / Supervisor Action
```

The agent must explain why Manual Review is required.

---

## 23. Tool Failure Handling

### Excel Failure

```text
Excel Failure
    |
    v
Do not invent data
    |
    v
Record failure
    |
    v
Manual Review / Safe Stop
```

### Word Failure

```text
Word Failure
    |
    v
Decision preserved
    |
    v
ReportGeneration = Failed
```

### Outlook Failure

```text
Outlook Failure
    |
    v
Decision preserved
    |
    v
Notification = Failed
```

The agent must never claim a failed tool operation succeeded.

---

## 24. Generative Topic Guardrails

The generative layer must:

1. Never invent operational data.
2. Never invent SKU information.
3. Never invent BatchID information.
4. Never invent complaint records.
5. Never invent quality evidence.
6. Never override deterministic thresholds.
7. Never override safety precedence.
8. Never claim a failed tool succeeded.
9. Never claim an email was sent unless Outlook succeeded.
10. Never claim a report was generated unless Word succeeded.
11. Never expose secrets or credentials.
12. Never issue unauthorized public safety communications.
13. Never make unsupported customer compensation commitments.
14. Route uncertain cases to Manual Review.

---

## 25. Recommended Generative Instructions

```text
You are the Quality Supervisor for the CAP-001 quality-control workflow.

Interpret the user's request and route it to the appropriate quality workflow.

Use operational tools for factual information.

Do not invent SKU, batch, complaint, incident, or quality data.

Follow deterministic quality rules and safety precedence.

If required evidence is unavailable, route the case to Manual Review.

Do not claim a tool operation succeeded unless the tool returned success.

Do not perform unauthorized public safety or customer actions.
```

---

## 26. Natural-Language Variations

The same intent may be expressed differently:

```text
"Check this complaint."
"Investigate this complaint."
"Analyze this customer issue."
"Assess this quality incident."
"Can you review complaint CMP001?"
```

These should map to the relevant incident-processing workflow.

The underlying deterministic workflow remains unchanged.

---

## 27. Topic Variables

Important variables may include:

```text
ComplaintID
SKU
BatchID
OrderID
Category
ComplaintDate
Description
IncidentID
Processed
SafetyIndicator
Status
Classification
```

Global variables can be used where information must be shared across Supervisor workflows.

---

## 28. Specialist Output Contract

Specialists should return structured findings rather than independently overriding the Supervisor.

Example:

```text
Specialist: Returns

Finding:
Return rate = 2.5%

Evidence:
Sales and return records

Recommendation:
Investigation Required
```

The Quality Supervisor applies the final classification.

---

## 29. Generative Orchestration

```text
                    USER / EVENT
                         |
                         v
                Generative Understanding
                         |
                         v
                    Topic Routing
                         |
                         v
              Incident Intake & Validation
                         |
                         v
                  Quality Supervisor
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
      Complaint       Returns       Product/Batch
      Specialist      Specialist     Specialist
          |              |              |
          +--------------+--------------+
                         |
                         v
                    Safety Check
                         |
                         v
                  Quality Decision
                         |
             +-----------+-----------+
             |           |           |
             v           v           v
            CAPA       Report     Notification
```

---

## 30. Autonomous Generative Trigger

For autonomous processing:

```text
New / Eligible Record
        |
        v
Autonomous Trigger
        |
        v
Generative Interpretation
        |
        v
Incident Intake Topic
        |
        v
Deterministic Validation
        |
        v
Quality Supervisor
```

Autonomous execution must use the same validation and safety controls as interactive execution.

---

## 31. Interactive vs Autonomous

| Capability | Interactive | Autonomous |
|---|---:|---:|
| Natural-language input | Yes | Not required |
| Complaint validation | Yes | Yes |
| Product validation | Yes | Yes |
| Batch validation | Yes | Yes |
| Specialist routing | Yes | Yes |
| Quality decision | Yes | Yes |
| CAPA | Yes | Yes |
| Report | Yes | Yes |
| Notification | Yes | Yes |
| Manual Review | Yes | Yes |

---

## 32. Generative Topic Test Cases

### Test 1 — Normal Request

```text
Process complaint CMP001 with SKU SKU001 and BatchID BATCH001.
```

Expected:

```text
Generative Understanding
        ↓
Incident Intake
        ↓
Validation
        ↓
Specialist Analysis
```

### Test 2 — Missing SKU

```text
Process complaint CMP002 with BatchID BATCH002.
```

Expected:

```text
SKU missing
   ↓
Invalid
```

### Test 3 — Invalid SKU

```text
Process CMP003 using SKU INVALID-SKU.
```

Expected:

```text
Product Master
     ↓
No Match
     ↓
Invalid SKU
```

### Test 4 — Duplicate

```text
Process CMP004.
```

If `Processed = Yes`:

```text
Already Processed
      ↓
Stop
```

### Test 5 — Complaint Cluster

```text
Analyze whether recent complaints for this product form a quality cluster.
```

Expected:

```text
Complaint Specialist
       ↓
Cluster Finding
       ↓
Quality Supervisor
```

### Test 6 — Return Threshold

```text
Check whether the product return rate requires an investigation.
```

Expected:

```text
Returns + Sales
       ↓
Return Rate
       ↓
Configured Threshold
       ↓
Decision
```

### Test 7 — Safety

```text
This complaint may indicate a product safety issue.
```

Expected:

```text
Safety Specialist
       ↓
Critical Escalation
       ↓
Supervisor Validation
```

### Test 8 — Missing Evidence

```text
Assess the incident but the required evidence is unavailable.
```

Expected:

```text
Insufficient Evidence
       ↓
Manual Review
```

### Test 9 — Reassessment

```text
Reassess incident INC001 because new evidence has arrived.
```

Expected:

```text
Existing Incident
       ↓
New Evidence
       ↓
Reassessment
```

---

## 33. Evaluation Criteria

Generative topics should be evaluated for:

### Intent Recognition

Can the agent identify the correct workflow?

### Entity Extraction

Can it identify ComplaintID, SKU and BatchID?

### Validation

Does it validate extracted values using operational tools?

### Routing

Does it select the correct specialist?

### Deterministic Compliance

Does it follow the configured quality rules?

### Safety

Does it preserve safety precedence?

### Hallucination Prevention

Does it avoid generating unsupported evidence?

### Tool Honesty

Does it accurately report tool success or failure?

### Human Escalation

Does it route uncertain cases to Manual Review?

---

## 34. Acceptance Checklist

- [ ] Incident Intake recognizes complaint requests.
- [ ] Missing SKU is handled.
- [ ] Invalid SKU is handled.
- [ ] Missing BatchID is handled.
- [ ] Invalid Batch/SKU relationship is handled.
- [ ] Duplicate processing is prevented.
- [ ] Complaint Specialist can be invoked.
- [ ] Returns Specialist can be invoked.
- [ ] Product/Batch Specialist can be invoked.
- [ ] Safety Specialist can be invoked.
- [ ] Quality Supervisor receives specialist findings.
- [ ] Quality rules determine final classification.
- [ ] Safety precedence is preserved.
- [ ] CAPA workflow is available.
- [ ] Report workflow is available.
- [ ] Outlook notification workflow is available.
- [ ] Reassessment workflow is available.
- [ ] Manual Review is available.
- [ ] Tool failures are handled.
- [ ] No unsupported data is generated.
- [ ] No unauthorized public action is performed.

---

## 35. Final Design Principle

> **Generative topics provide natural-language understanding and flexible routing, while deterministic Copilot Studio workflows and operational tools remain responsible for validation, quality rules, state changes, safety decisions, CAPA actions, reporting, and notifications.**

The generative layer improves usability without weakening the governance, traceability, safety, and auditability of the CAP-001 Quality Supervisor system.
