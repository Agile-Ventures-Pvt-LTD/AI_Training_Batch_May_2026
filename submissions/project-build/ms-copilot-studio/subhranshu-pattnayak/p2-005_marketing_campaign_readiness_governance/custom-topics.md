# Custom Topics

## Overview

The Campaign Readiness Review Agent uses custom topics to handle deterministic workflow operations that require structured validation, approval routing, and reassessment control.

These topics are orchestrated by the Campaign Readiness Supervisor and provide controlled outputs used during readiness evaluation.

---

# 1. Campaign Intake & Validation

## Purpose

The Campaign Intake & Validation topic acts as the entry point of the readiness workflow.

Its responsibility is to identify a pending campaign, validate mandatory campaign information, and ensure the campaign is eligible for specialist assessment.

---

## Data Source

Campaign Requests dataset

---

## Processing Logic

The topic:

1. Retrieves pending campaign records.
2. Selects the next campaign for assessment.
3. Validates mandatory campaign fields.
4. Calculates:
   - Days To Launch
   - Budget Variance
5. Confirms readiness assessment can proceed.

---

## Validation Rules

Mandatory fields:

- Campaign ID
- Campaign Name
- Product
- Launch Date
- Geography
- Channels
- Campaign Owner

Additional checks:

- Launch Date must not be in the past.
- Proposed Budget must be greater than zero.

---

## Outputs

| Output | Description |
|----------|-------------|
| ValidationStatus | Passed / Failed |
| CampaignID | Campaign identifier |
| CampaignName | Campaign name |
| DaysToLaunch | Days remaining until launch |
| BudgetVariance | Proposed Budget - Approved Budget |
| CampaignStatus | Assessment state |

---

## Failure Handling

If validation fails:

- Assessment stops immediately.
- Specialist agents are not invoked.
- Validation findings are returned to the Supervisor.

---

# 2. Approval & Finalization

## Purpose

Determine whether governance policies require additional approval before launch.

The topic evaluates approval conditions and returns approval requirements to the Supervisor.

The Supervisor remains responsible for assigning the final readiness status.

---

## Inputs

- CampaignID
- ProposedBudget
- ApprovedBudget
- TargetCPL
- Sensitivity
- Geography
- BrandFindings
- DaysToLaunch
- RequiredApprovals

---

## Approval Conditions

Approval is required when:

### Budget Escalation

Proposed Budget > Approved Budget

Required Approver:

- Marketing Director

---

### Governance Escalation

Any of the following:

- Proposed Budget > 1,000,000 INR
- Target CPL > 4,000 INR
- High Regulatory Sensitivity
- Specialist approval requirement exists

Required Approver:

- Management Approval

---

## Outputs

| Output | Description |
|----------|-------------|
| ApprovalRequired | True / False |
| RequiredApprover | Required approver |
| ApprovalReason | Approval justification |
| FinalisationStatus | Approval outcome |

---

## Possible Outcomes

- No Approval Required
- Awaiting Approval

---

# 3. Remediation & Selective Reassessment

## Purpose

Control reassessment execution and prevent infinite remediation loops.

The topic determines whether additional automated reassessment cycles are permitted.

---

## Inputs

- CampaignID
- BlockingIssues
- AffectedDomain
- ReassessmentCycle

---

## Processing Logic

The topic evaluates:

```text
ReassessmentCycle < 2
```

If true:

```text
ReassessmentAllowed = true
RemediationStatus = Reassessment Required
```

If false:

```text
ReassessmentAllowed = false
RemediationStatus = Manual Review Required
```

---

## Outputs

| Output | Description |
|----------|-------------|
| DomainsToReassess | Specialist domain requiring reassessment |
| ReassessmentAllowed | True / False |
| RemediationStatus | Reassessment result |

---

## Reassessment Policy

Maximum automated reassessment cycles:

```text
2
```

After two unsuccessful cycles:

```text
Manual Review Required
```

The Supervisor is responsible for rerunning the appropriate specialist agent and incrementing the reassessment cycle counter.

---

# Topic Orchestration Flow

```text
Campaign Intake & Validation
            │
            ▼
Specialist Assessments
            │
            ▼
Launch Risk & Decision Specialist
            │
            ▼
Approval & Finalization
            │
            ▼
Remediation & Selective Reassessment
            │
            ▼
Supervisor Final Readiness Determination
            │
            ▼
Reporting & Communication Specialist
```

The Supervisor coordinates all topic execution and remains the sole authority for assigning the final campaign readiness status.