# Qualification Logic

## Project Information

| Item | Details |
|------|---------|
| Project ID | P2-003 |
| Project Name | Autonomous Sales Lead Qualification Agent |
| Platform | Microsoft Copilot Studio |
| Participant | Mohammad Anas |

---

# Purpose

This document explains the business rules and decision-making logic used by the Autonomous Sales Lead Qualification Agent to evaluate inbound sales enquiries.

The qualification logic ensures that every lead is assessed consistently using predefined business criteria before determining the appropriate processing outcome.

---

# Qualification Workflow

The lead qualification process follows a sequential evaluation model.

```
Incoming Email
       │
       ▼
Scope Validation
       │
       ▼
Extract Lead Information
       │
       ▼
Check Mandatory Information
       │
       ▼
Duplicate Detection
       │
       ▼
Read Qualification Rules
       │
       ▼
Business Evaluation
       │
       ▼
Calculate Qualification Score
       │
       ▼
Apply Override Rules
       │
       ▼
Determine Lead Classification
       │
       ▼
Assign Sales Owner
       │
       ▼
Execute Business Action
```

Each stage must complete successfully before the next stage begins.

---

# Step 1 – Scope Validation

The agent first determines whether the email represents a valid commercial sales enquiry.

The following enquiries are processed:

- Product enquiries
- Solution requests
- Enterprise implementation enquiries
- Demo requests
- Partnership enquiries
- Purchase discussions

The following are excluded:

- Technical support
- Recruitment
- Vendor communication
- Internal requests
- Spam
- Marketing newsletters
- Academic research

Excluded emails receive the classification:

```
Not a Sales Lead
```

No further qualification is performed.

---

# Step 2 – Information Extraction

The agent extracts structured information from the email.

Fields include:

- Contact Name
- Email Address
- Job Title
- Company Name
- Country
- Industry
- Company Size
- Product Interest
- Business Requirement
- Budget
- Purchase Timeline
- Decision Role
- Lead Source

If a value cannot be identified confidently, it is recorded as **Unknown** rather than inferred.

---

# Step 3 – Mandatory Data Validation

The extracted information is validated for completeness.

Examples of mandatory fields include:

- Company Name
- Contact Email
- Product Interest

If mandatory information is missing:

- Classification becomes **Additional Information Required**.
- A request for the missing information is generated.
- Qualification does not continue until sufficient information is available.

---

# Step 4 – Duplicate Detection

Before creating a new opportunity, the agent checks the existing Lead Register.

Comparison is performed using:

- Source Message ID
- Sender Email
- Company Name
- Product Interest

If a duplicate record is identified:

- Existing record is updated.
- New record creation is skipped.
- Duplicate acknowledgements are prevented.
- Processing status becomes **Duplicate**.

---

# Step 5 – Business Rule Evaluation

The agent evaluates the lead against predefined business rules.

Assessment considers:

- Product fit
- Budget viability
- Purchase timeline
- Decision authority
- Company size
- Territory
- Lead source
- Information completeness

Reference data is retrieved from operational Excel tables before evaluation.

---

# Step 6 – Qualification Scoring

Each evaluation criterion contributes to an overall qualification score.

Typical evaluation areas include:

| Criterion | Purpose |
|-----------|---------|
| Product Fit | Determines alignment between customer need and available products |
| Budget | Assesses purchasing capability |
| Timeline | Measures purchase urgency |
| Decision Role | Evaluates buying authority |
| Company Size | Determines commercial opportunity |
| Territory | Supports regional ownership assignment |
| Lead Source | Provides business context |
| Completeness | Measures confidence in available information |

The combined assessment produces the overall qualification score used during classification.

---

# Step 7 – Override Rules

Certain business conditions take priority over the calculated score.

Examples include:

- Duplicate opportunity detected
- Missing mandatory information
- Unknown product
- Unmapped territory
- Low confidence extraction
- Conflicting information
- Connector failure

When an override condition exists, the override outcome replaces the standard classification.

---

# Step 8 – Lead Classification

After evaluation, the agent assigns one of the approved business classifications.

| Classification | Description |
|---------------|-------------|
| Hot | High-value opportunity requiring immediate follow-up |
| Qualified | Meets qualification criteria and is ready for sales engagement |
| Nurture | Potential future opportunity requiring ongoing engagement |
| Low Priority | Limited commercial value at present |
| Additional Information Required | Essential information is missing |
| Human Review Required | Automated decision cannot be made confidently |
| Duplicate | Existing opportunity already recorded |
| Not a Sales Lead | Outside the project scope |

No additional classifications are generated.

---

# Step 9 – Sales Owner Assignment

After classification, the appropriate sales representative is assigned using operational reference data.

Assignment considers:

- Territory
- Product interest
- Business rules
- Ownership mappings

The assigned owner is recorded in the Lead Register.

---

# Step 10 – Business Actions

The final classification determines the next action.

| Classification | Action |
|---------------|--------|
| Hot | Update Lead Register, generate report, notify assigned sales owner |
| Qualified | Update Lead Register, generate report, send acknowledgement |
| Nurture | Update Lead Register, schedule follow-up action |
| Low Priority | Record lead for future reference |
| Additional Information Required | Send request for missing information |
| Human Review Required | Escalate to Sales Operations |
| Duplicate | Update existing record only |
| Not a Sales Lead | End workflow |

---

# Human Review Conditions

The agent routes the lead for manual review when:

- Business confidence is low.
- Product cannot be identified.
- Territory mapping is unavailable.
- Customer information conflicts.
- Qualification rules cannot be applied.
- Connector failures prevent completion.
- Business policy requires human judgement.

The agent records completed actions before escalation.

---

# Error Handling

If an error occurs during qualification:

1. Record the processing state.
2. Retry transient connector failures once.
3. Stop dependent actions if necessary.
4. Preserve completed work.
5. Escalate unresolved cases for manual review.

This prevents inconsistent or partial lead processing.

---

# Design Principles

The qualification logic follows these principles:

- Deterministic business decisions
- Sequential processing
- Policy-first evaluation
- Reference-data validation
- Controlled AI reasoning
- Human oversight for uncertainty
- Consistent classifications
- Full auditability

---

# Benefits

The implemented qualification logic provides:

- Consistent lead evaluation
- Reduced manual effort
- Faster response times
- Reliable duplicate detection
- Standardized qualification outcomes
- Improved operational governance
- Better reporting and traceability

---

# Summary

The Autonomous Sales Lead Qualification Agent uses a structured, rule-based qualification process that combines AI-assisted information extraction with predefined business policies and operational reference data.

By validating incoming enquiries, applying consistent qualification criteria, enforcing business overrides, and routing uncertain cases for human review, the solution delivers accurate, repeatable, and policy-compliant lead qualification while reducing manual effort and improving operational efficiency.