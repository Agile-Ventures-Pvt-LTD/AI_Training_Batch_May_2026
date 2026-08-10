# Custom Topics

## Overview

The supervisor agent implements three custom orchestration topics to manage the complete campaign readiness lifecycle.

---

## Topic 1 – Campaign Intake & Validation

### Purpose
Starts the assessment process by validating that a campaign is eligible for evaluation.

### Responsibilities
- Retrieve pending campaign from Excel.
- Validate campaign status.
- Prevent duplicate assessments.
- Update campaign status to **In Assessment**.
- Trigger all specialist child agents.

### Orchestration Pattern
- Sequential
- Parallel Fan-out

---

## Topic 2 – Remediation & Selective Reassessment

### Purpose
Handles campaigns that fail one or more specialist assessments.

### Responsibilities
- Receive FinalReadiness from Launch Risk & Decision Specialist.
- If remediation is required:
  - Execute remediation workflow.
  - Re-run only the affected specialist assessments.
  - Recalculate FinalReadiness.
- Stop after the configured retry limit and escalate for manual review if still not ready.

### Orchestration Pattern
- Conditional
- Selective Loop
- Decision

---

## Topic 3 – Approval & Finalisation

### Purpose
Completes governance, reporting, and communication after readiness is determined.

### Responsibilities
- Check FinalReadiness.
- If Ready:
  - Execute Reporting & Communication Specialist.
  - Generate Word readiness report.
  - Update Excel dataset.
  - Send Outlook notification.
- If not Ready:
  - End workflow without approval.

### Orchestration Pattern
- Conditional
- Sequential
- Hierarchical

---

## Summary

| Topic | Purpose | Pattern |
|--------|---------|---------|
| Campaign Intake & Validation | Validate campaign and start assessments | Sequential + Parallel |
| Remediation & Selective Reassessment | Correct issues and selectively rerun assessments | Conditional + Loop |
| Approval & Finalisation | Produce reports and notify stakeholders | Conditional + Sequential |

