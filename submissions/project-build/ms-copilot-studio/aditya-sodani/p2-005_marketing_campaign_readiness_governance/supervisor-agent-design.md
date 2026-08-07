# Supervisor Agent Design

## Project
**P2-005 — Marketing Campaign Readiness & Governance**

## Agent Name
**Campaign Readiness Supervisor**

## Role
The Campaign Readiness Supervisor is the central orchestration agent responsible for coordinating the complete campaign readiness assessment.

It is the **only agent authorized to assign the final campaign readiness outcome**.

## Core Responsibilities

- Process only campaigns eligible for assessment.
- Invoke Campaign Intake & Validation before specialist analysis.
- Prevent duplicate assessments.
- Change eligible campaigns from `Pending` to `In Assessment`.
- Invoke mandatory specialist agents.
- Wait for all mandatory specialist results.
- Retry a failed specialist once.
- Handle missing evidence as `Insufficient Evidence`.
- Consolidate specialist findings.
- Invoke the Launch Risk & Decision Specialist.
- Validate the proposed readiness outcome.
- Apply mandatory governance precedence.
- Route correctable blockers to remediation.
- Perform selective reassessment.
- Limit automated reassessment to two cycles.
- Route mandatory human approvals.
- Assign the final readiness outcome.
- Update the final campaign status.
- Authorize reporting and stakeholder communication.

## Mandatory Specialist Agents

The Supervisor coordinates:

1. Budget & Commercial Specialist
2. Brand & Content Compliance Specialist
3. Channel Readiness Specialist
4. Asset Readiness Specialist

All mandatory specialist results must be available before final decision analysis.

## Assessment Flow

```text
Campaign Request
      |
      v
Campaign Intake & Validation
      |
      v
ValidationStatus = Valid?
   /        \
 No         Yes
 |           |
Stop         v
       Mark In Assessment
             |
             v
       Invoke Specialists
             |
             v
       Collect Findings
             |
             v
   Launch Risk & Decision
             |
             v
     Supervisor Validation
             |
      +------+------+
      |             |
 Remediation     Approval
      |             |
      +------+------+
             |
             v
       Final Outcome
             |
             v
 Update Campaign Status
             |
             v
Reporting & Communication