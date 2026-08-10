# Custom Topics

## Project

**Marketing Campaign Readiness Governance**

---

# Overview

The Marketing Campaign Readiness Governance solution implements three mandatory custom topics in Microsoft Copilot Studio. These topics provide deterministic workflow control for campaign validation, remediation, and approval while supporting the overall Supervisor–Specialist architecture.

Each topic is responsible for a specific stage of the campaign lifecycle and is invoked by the Campaign Readiness Supervisor when required.

---

# Topic Architecture

```
Campaign Readiness Supervisor
            │
            ▼
──────────────────────────────────
Topic 1
Campaign Intake & Validation
──────────────────────────────────
            │
            ▼
Specialist Agent Assessment
            │
            ▼
──────────────────────────────────
Topic 2
Remediation & Selective Reassessment
──────────────────────────────────
            │
            ▼
──────────────────────────────────
Topic 3
Approval & Finalisation
──────────────────────────────────
            │
            ▼
Final Readiness Decision
```

---

# Topic 1 – Campaign Intake & Validation

## Purpose

This topic performs deterministic validation before specialist agents are executed. It ensures that only valid campaigns enter the assessment workflow.

---

## Responsibilities

- Receive Campaign ID
- Retrieve campaign details from Excel
- Validate mandatory campaign fields
- Detect duplicate campaigns
- Update campaign status
- Return validation result to the Supervisor

---

## Validations Performed

The topic validates:

- Campaign ID exists
- Campaign ID is unique
- Campaign Status = Pending
- Campaign Name exists
- Product exists
- Launch Date exists
- Launch Date is not in the past
- Proposed Budget exists
- Approved Budget exists
- Geography exists
- At least one marketing channel exists
- Campaign Owner exists

---

## Variables Used

| Variable | Description |
|-----------|-------------|
| CampaignID | Campaign identifier |
| CampaignName | Campaign name |
| Product | Product name |
| LaunchDate | Campaign launch date |
| ProposedBudget | Proposed campaign budget |
| ApprovedBudget | Approved budget |
| Geography | Target geography |
| Channels | Marketing channels |
| CampaignOwner | Campaign owner |
| ValidationStatus | Validation result |
| DuplicateDetected | Duplicate campaign flag |

---

## Workflow

```
Start
   │
   ▼
Get Campaign
   │
   ▼
Validate Required Fields
   │
   ▼
Duplicate Check
   │
   ▼
Validation Passed?
   │
 ┌────┴────┐
 │         │
Yes        No
 │         │
 ▼         ▼
Update     Stop
Status
 │
 ▼
Return to Supervisor
```

---

## Output

Possible outcomes:

- Validation Passed
- Validation Failed
- Duplicate Campaign

---

# Topic 2 – Remediation & Selective Reassessment

## Purpose

Coordinate remediation activities when one or more specialist assessments fail.

---

## Responsibilities

- Receive failed specialist domains
- Create remediation actions
- Assign remediation owner
- Preserve successful assessments
- Detect corrected campaign data
- Rerun only affected specialist agents
- Return updated assessment to the Supervisor

---

## Business Rules

The topic:

- Updates Campaign Status to **Awaiting Remediation**
- Preserves previously successful assessments
- Executes selective reassessment
- Supports a maximum of two automated reassessment cycles
- Escalates to Manual Review after two unsuccessful cycles

---

## Variables Used

| Variable | Description |
|-----------|-------------|
| CampaignID | Campaign identifier |
| CampaignStatus | Current workflow state |
| FailedDomain | Failed specialist domain |
| ReassessmentCount | Number of reassessment attempts |
| ValidationStatus | Validation result |

---

## Workflow

```
Campaign Requires Remediation
            │
            ▼
Update Status
Awaiting Remediation
            │
            ▼
Assign Remediation Owner
            │
            ▼
Correct Campaign Data
            │
            ▼
Ready for Reassessment?
        │
   ┌────┴────┐
   │         │
Yes         No
 │           │
 ▼           ▼
Run Failed   End
Specialists
 │
 ▼
Increase
ReassessmentCount
 │
 ▼
Count >= 2 ?
 │
 ├─────────────┐
 │             │
Yes           No
 │             │
 ▼             ▼
Manual      Return to
Review      Supervisor
```

---

## Output

Possible outcomes:

- Awaiting Remediation
- Reassessment Complete
- Manual Review

---

# Topic 3 – Approval & Finalisation

## Purpose

Evaluate campaign approval rules and determine whether mandatory management approval is required before launch.

---

## Responsibilities

- Evaluate approval conditions
- Determine approval requirement
- Record approval reason
- Update campaign status
- Return final approval outcome

---

## Approval Conditions

The topic evaluates:

- Proposed Budget > Approved Budget
- Proposed Budget > ₹1,000,000
- Target CPL > ₹4,000
- High Regulatory Sensitivity
- Multi-Market Geography

*(Additional approval conditions such as Restricted Claims and Urgent Launch can be added if supported by the data source.)*

---

## Variables Used

| Variable | Description |
|-----------|-------------|
| ProposedBudget | Proposed budget |
| ApprovedBudget | Approved budget |
| TargetCPL | Target Cost Per Lead |
| RegulatorySensitivity | Regulatory classification |
| Geography | Campaign geography |
| CampaignStatus | Workflow status |

---

## Workflow

```
Start
   │
   ▼
Get Campaign
   │
   ▼
Budget Check
   │
   ▼
Budget Threshold Check
   │
   ▼
Target CPL Check
   │
   ▼
Regulatory Sensitivity Check
   │
   ▼
Geography Check
   │
   ▼
Approval Required?
   │
 ┌────┴────┐
 │         │
Yes        No
 │         │
 ▼         ▼
Awaiting   Ready
Approval
 │
 ▼
Return to Supervisor
```

---

## Output

Possible outcomes:

- Ready
- Awaiting Approval

---

# Topic Interaction

```
Supervisor
      │
      ▼
Topic 1
Validation
      │
      ▼
Specialist Agents
      │
      ▼
Topic 2
Remediation
      │
      ▼
Topic 3
Approval
      │
      ▼
Final Readiness
```

---

# Benefits

The custom topics provide:

- Deterministic validation
- Modular workflow design
- Reusable business logic
- Approval governance
- Selective reassessment
- Clear campaign state transitions
- Enterprise-ready orchestration

---

# Conclusion

The three custom topics form the governance layer of the Marketing Campaign Readiness Governance solution. Together, they ensure that campaigns are validated, remediated when necessary, approved according to business rules, and returned to the Campaign Readiness Supervisor for a consistent and controlled readiness decision.