# Orchestration Patterns

## Overview

The Campaign Readiness Governance solution implements multiple orchestration patterns to automate campaign assessment while ensuring compliance with business governance policies. The Supervisor Agent coordinates specialist agents, applies decision rules, and manages remediation and approvals before determining the final campaign readiness.

---

# 1. Sequential Orchestration

## Purpose

Activities that depend on the successful completion of a previous step are executed sequentially.

## Implementation

```
Retrieve Pending Campaign
        ↓
Validate Campaign Intake
        ↓
Launch Specialist Assessments
        ↓
Aggregate Results
        ↓
Determine Final Readiness
        ↓
Generate Report
        ↓
Update Excel
        ↓
Send Notification
```

**Used For**

- Campaign intake validation
- Final report generation
- Excel status update
- Outlook notification

---

# 2. Parallel (Fan-Out / Fan-In)

## Purpose

Independent specialist assessments execute simultaneously to reduce processing time.

## Implementation

```
                Supervisor
                     │
     ┌───────────────┼───────────────┐
     │               │               │
 Budget        Brand & Content    Channel
 Specialist      Specialist      Specialist
     │               │               │
     └───────────────┼───────────────┘
                     │
             Asset Readiness
                     │
                     ▼
         Launch Risk & Decision
```

The supervisor waits until all required specialist assessments complete before continuing.

---

# 3. Conditional Routing

Business rules determine the next workflow based on assessment outcomes.

### Examples

- Budget exceeds approved budget → Budget approval required
- Budget > INR 1,000,000 → VP Marketing approval
- High regulatory sensitivity → Brand review
- Missing mandatory assets → Remediation
- Launch within five days with missing assets → Not Ready

---

# 4. Hierarchical Orchestration

The solution follows a Supervisor–Specialist architecture.

```
Campaign Readiness Supervisor
        │
        ├── Campaign Intake & Validation
        ├── Budget & Commercial Specialist
        ├── Brand & Content Compliance Specialist
        ├── Channel Readiness Specialist
        ├── Asset Readiness Specialist
        ├── Launch Risk & Decision Specialist
        └── Reporting & Communication Specialist
```

The supervisor delegates work, collects results, and makes the final decision.

---

# 5. Remediation & Selective Reassessment

When a campaign fails one or more assessments, only the affected specialists are re-executed.

```
Assessment Failed
        │
        ▼
Remediation Required
        │
Correct Deficiency
        │
Re-run Affected Specialist
        │
Updated Final Readiness
```

This avoids repeating the entire assessment workflow.

---

# 6. Approval Workflow

Certain governance conditions require additional approval before launch.

Examples include:

- Budget exceeding organisational thresholds
- Regional or multi-market approval
- High-risk campaigns

The supervisor routes these cases for approval before proceeding to finalisation.

---

# 7. Failure Handling

The solution includes fallback behaviour for exceptional scenarios.

Examples:

- Retry specialist assessment once if no result is returned.
- Escalate to manual review if retry fails.
- Record notification failures without interrupting assessment completion.
- Exit safely when no pending campaigns exist.

---

# Summary

The implemented orchestration combines sequential execution, parallel processing, hierarchical delegation, conditional routing, remediation loops, approval workflows, and failure handling to provide a scalable and autonomous campaign readiness assessment solution aligned with the project requirements.