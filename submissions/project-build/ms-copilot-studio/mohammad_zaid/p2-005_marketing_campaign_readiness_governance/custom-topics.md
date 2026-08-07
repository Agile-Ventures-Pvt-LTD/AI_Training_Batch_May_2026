
# Custom Topics Design

# 1. Overview

The Autonomous Marketing Campaign Launch Readiness & Governance System implements three custom Topics within Microsoft Copilot Studio to support deterministic workflow execution outside the responsibilities of the specialist agents.

These Topics coordinate campaign validation, remediation, reassessment, and approval workflows while remaining under the control of the Campaign Readiness Supervisor.

Unlike specialist agents, Topics execute structured workflow logic and manage campaign lifecycle transitions. They do not perform domain-specific assessments or assign the final campaign readiness outcome.

---

# 2. Topic Architecture

```text
                   Campaign Readiness Supervisor
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
Campaign Intake &      Remediation &          Approval &
Validation             Selective              Finalisation
                        Reassessment
```

The Supervisor invokes Topics only when their execution is required by the campaign workflow.

---

# 3. Campaign Intake & Validation

## Purpose

The Campaign Intake & Validation Topic performs deterministic validation before specialist assessment begins.

Its objective is to ensure that only complete and eligible campaigns enter the assessment workflow.

---

## Responsibilities

- Retrieve the selected campaign.
- Validate mandatory campaign information.
- Verify campaign eligibility.
- Prevent duplicate assessments.
- Ensure the campaign status is Pending.
- Update the campaign status to **In Assessment**.
- Return the validation result to the Campaign Readiness Supervisor.

---

## Mandatory Validation Rules

The Topic validates:

- Campaign ID exists.
- Campaign Name exists.
- Campaign Owner exists.
- Product exists.
- Launch Date exists.
- Launch Date is valid.
- Geography exists.
- Proposed Budget exists.
- Approved Budget exists.
- At least one campaign channel exists.
- Campaign Status equals **Pending**.

If any mandatory validation fails, the campaign is prevented from entering specialist assessment.

---

## Workflow

```text
Trigger
    │
    ▼
Retrieve Campaign
    │
    ▼
Validate Mandatory Fields
    │
    ▼
Campaign Eligible?
    │
 ┌──┴──┐
 │     │
No    Yes
 │      │
Exit   Update Status
        │
        ▼
In Assessment
        │
        ▼
Return to Supervisor
```

---

## Inputs

- Campaign ID
- Campaign data
- Campaign status

---

## Outputs

- Validation status
- Validation findings
- Updated campaign status
- Failure reason (if applicable)

---

# 4. Remediation & Selective Reassessment

## Purpose

The Remediation & Selective Reassessment Topic manages campaigns requiring corrective action before launch readiness can be achieved.

It coordinates remediation activities and ensures that only the affected assessment domains are reassessed.

---

## Responsibilities

- Receive remediation requests from the Supervisor.
- Record remediation status.
- Identify affected specialist domains.
- Trigger selective reassessment.
- Preserve previously successful specialist results.
- Return updated findings to the Campaign Readiness Supervisor.

---

## Workflow

```text
Trigger
    │
    ▼
Retrieve Campaign
    │
    ▼
Record Remediation
    │
    ▼
Identify Affected Domains
    │
    ▼
Selective Specialist Reassessment
    │
    ▼
Return Updated Results
```

---

## Selective Reassessment Strategy

Only specialists affected by the remediation are executed again.

Examples include:

| Issue                 | Specialists Reassessed                |
| --------------------- | ------------------------------------- |
| Budget change         | Budget & Commercial Specialist        |
| Brand correction      | Brand & Content Compliance Specialist |
| Missing assets        | Asset Readiness Specialist            |
| Channel configuration | Channel Readiness Specialist          |

Previously successful assessments remain valid and are not unnecessarily repeated.

---

## Inputs

- Campaign information
- Remediation actions
- Previous specialist findings

---

## Outputs

- Updated specialist findings
- Remediation completion status
- Reassessment status

---

# 5. Approval & Finalisation

## Purpose

The Approval & Finalisation Topic manages campaigns requiring mandatory human approval before launch.

The Topic coordinates approval processing without modifying campaign readiness decisions.

---

## Responsibilities

- Identify required approvers.
- Record approval requests.
- Update campaign status.
- Record approval outcomes.
- Return approval status to the Campaign Readiness Supervisor.

---

## Approval Scenarios

Examples include:

- Budget exceeds approved threshold.
- Cost per Lead exceeds governance threshold.
- High regulatory sensitivity.
- Multi-market campaigns.
- Executive approval requirements.

---

## Workflow

```text
Trigger
    │
    ▼
Retrieve Campaign
    │
    ▼
Record Approval Requirement
    │
    ▼
Await Approval
    │
    ▼
Return Approval Status
```

---

## Inputs

- Campaign information
- Approval requirement
- Governance rules

---

## Outputs

- Approval status
- Required approver
- Approval outcome
- Updated campaign status

---

# 6. Topic Invocation

Topics are not triggered independently.

The Campaign Readiness Supervisor invokes Topics according to workflow requirements.

| Topic                                | Invoked When                     |
| ------------------------------------ | -------------------------------- |
| Campaign Intake & Validation         | Beginning of campaign assessment |
| Remediation & Selective Reassessment | Corrective action is required    |
| Approval & Finalisation              | Human approval is required       |

---

# 7. Topic Interaction

```text
Supervisor
     │
     ▼
Campaign Intake & Validation
     │
     ▼
Specialist Agents
     │
     ▼
Supervisor
     │
     ├────────► Approval & Finalisation
     │
     └────────► Remediation & Selective Reassessment
                    │
                    ▼
                 Supervisor
```

Topics never invoke one another directly.

All workflow transitions remain under the control of the Campaign Readiness Supervisor.

---

# 8. Design Principles

The custom Topics follow these principles:

- Deterministic workflow execution.
- Single workflow responsibility.
- Supervisor-controlled invocation.
- No independent campaign decisions.
- No domain-specific assessments.
- Clear campaign lifecycle management.
- Minimal business logic duplication.
- Explainable workflow execution.

---

# 9. Summary

The three custom Topics provide the workflow foundation of the Autonomous Marketing Campaign Launch Readiness & Governance System. They ensure deterministic campaign validation, controlled remediation, selective reassessment, and structured approval processing while allowing the Campaign Readiness Supervisor to remain the single orchestration authority throughout the campaign lifecycle.
