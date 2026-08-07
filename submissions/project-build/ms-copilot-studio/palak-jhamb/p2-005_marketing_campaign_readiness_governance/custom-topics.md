# Custom Topics

## Overview

Custom Topics implement the workflow logic of the Campaign Readiness Assessment Supervisor. They represent discrete business processes that guide the Supervisor through campaign validation, remediation, approval, and workflow completion.

Topics are invoked autonomously by the Supervisor Agent based on the current workflow state and assessment outcomes. Each topic performs a specific responsibility and returns structured results to the Supervisor for further orchestration.

The solution currently contains three custom workflow topics.

---

# Topic Architecture

```text
Campaign Readiness Supervisor
        │
        ▼
Campaign Intake & Validation
        │
        ▼
Specialist Assessments
        │
        ▼
Launch Risk & Decision
        │
        ▼
──────── Workflow Decision ────────
        │                │
        ▼                ▼
Remediation      Approval & Finalization
        │                │
        └────────┬───────┘
                 ▼
Reporting & Communication
```

---

# Topic 1 – Campaign Intake & Validation

## Purpose

The Campaign Intake & Validation topic is the entry point of the assessment workflow. It validates campaign information before any specialist assessment begins and ensures that only eligible campaigns enter the readiness evaluation process.

---

## Trigger

This topic is invoked automatically by the Campaign Readiness Supervisor at the beginning of every campaign readiness assessment.

---

## Responsibilities

The topic is responsible for:

- Retrieving campaign records from the Campaign Requests dataset.
- Selecting the next campaign awaiting assessment.
- Validating mandatory campaign information.
- Ensuring campaign eligibility.
- Returning structured validation results to the Supervisor.

---

## Validation Rules

The topic validates the following information:

- Campaign ID exists.
- Campaign Name exists.
- Product exists.
- Campaign Status is **Pending**.
- Launch Date exists.
- Launch Date is not in the past.
- Proposed Budget exists.
- Geography exists.
- Marketing Channels exist.
- Campaign Owner exists.

---

## Tools Used

- Excel Online (Business) – List Rows
- AI Builder Prompt

---

## Workflow

```text
Supervisor
      │
      ▼
Retrieve Campaign Requests
      │
      ▼
Identify Pending Campaign
      │
      ▼
Validate Campaign Information
      │
      ├──────── Validation Passed
      │                 │
      │                 ▼
      │      Return Validated Campaign
      │
      └──────── Validation Failed
                        │
                        ▼
           Return Validation Errors
```

---

## Output

If validation succeeds, the topic returns:

- Validation Status
- Campaign Details
- Days Until Launch
- Validation Summary

If validation fails, the topic returns:

- Validation Status
- Validation Errors
- Failure Summary

---

# Topic 2 – Remediation & Selective Reassessment

## Purpose

The Remediation & Selective Reassessment topic manages campaigns that cannot proceed because one or more specialist assessments identified blocking issues or conditions requiring corrective action.

Rather than repeating the complete assessment, the topic determines which specialist domains require reassessment after remediation has been completed.

---

## Trigger

Invoked by the Campaign Readiness Supervisor whenever remediation is required following specialist assessment or launch risk evaluation.

---

## Responsibilities

- Review blocking findings.
- Identify specialist domains requiring reassessment.
- Preserve successful specialist results.
- Re-execute only affected specialist assessments.
- Return updated assessment results to the Supervisor.

---

## Workflow

```text
Supervisor
      │
      ▼
Blocking Issues Identified
      │
      ▼
Determine Required Remediation
      │
      ▼
Selective Specialist Reassessment
      │
      ▼
Return Updated Results
```

---

## Planned Outcome

The topic will:

- Reduce unnecessary reassessment.
- Improve workflow efficiency.
- Support iterative campaign improvement.

---

# Topic 3 – Approval & Finalization

## Purpose

The Approval & Finalization topic manages approval workflows whenever management authorization is required before campaign launch.

---

## Trigger

Invoked automatically by the Campaign Readiness Supervisor whenever the Launch Risk & Decision Specialist determines that management approval is required.

---

## Responsibilities

- Update campaign status.
- Identify required approver.
- Initiate approval workflow.
- Monitor approval outcome.
- Return approval status to the Supervisor.

---

## Tools Used

- Excel Online (Business)
- Microsoft Outlook
- Microsoft Word (planned for approval documentation)

---

## Workflow

```text
Supervisor
      │
      ▼
Approval Required
      │
      ▼
Update Campaign Status
      │
      ▼
Notify Approver
      │
      ▼
Receive Decision
      │
      ▼
Return Approval Status
```

---

## Possible Outcomes

- Approved
- Rejected
- Pending Approval

---

# Topic Interaction

The Supervisor Agent controls all topic execution.

```text
Campaign Readiness Supervisor
        │
        ▼
Campaign Intake & Validation
        │
        ▼
Specialist Assessment
        │
        ▼
Launch Risk Evaluation
        │
        ├──────── Remediation Required
        │                │
        │                ▼
        │     Remediation & Selective Reassessment
        │
        ├──────── Approval Required
        │                │
        │                ▼
        │      Approval & Finalization
        │
        ▼
Reporting & Communication
```

---

# Topic Design Principles

Each topic has been designed following the same architectural principles:

- Single business responsibility.
- Autonomous execution.
- Supervisor-controlled invocation.
- Structured outputs.
- Clear workflow boundaries.
- Reusable implementation.
- Minimal coupling with other topics.


