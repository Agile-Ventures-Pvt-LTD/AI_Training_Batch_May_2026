# Supervisor Agent Design

## Agent Name

**BC/DR Readiness Assessment Supervisor**

---

# Purpose

The Supervisor Agent acts as the central orchestrator of the BC/DR Readiness Assessment System. It coordinates the complete assessment workflow by receiving assessment requests, delegating tasks to specialist agents, consolidating their findings, determining the final readiness classification, and initiating reporting and stakeholder communication.

The Supervisor ensures that every assessment follows a standardized process while maintaining consistency across all specialist evaluations.

---

# Responsibilities

- Receive BC/DR assessment requests.
- Retrieve assessment and application details from Excel.
- Delegate assessment tasks to specialist agents.
- Coordinate the execution of all assessment activities.
- Consolidate specialist outputs.
- Validate completeness of assessment results.
- Determine the overall BC/DR readiness classification.
- Trigger report generation.
- Update the Assessment Register.
- Notify stakeholders of the final assessment outcome.

---

# Child Agents

The Supervisor coordinates the following specialist agents:

1. Application Criticality Specialist
2. Recovery Requirements Specialist
3. Technical Recovery Specialist
4. Risk & Recovery Gap Specialist
5. Remediation Planning Specialist
6. Reporting & Communication Specialist

---

# Connected Tools

## Excel Online (Business)

Purpose:

- Read Application Inventory
- Read Assessment Requests
- Update Assessment Register

---

## Word Online (Business)

Purpose:

- Generate BC/DR Readiness Assessment Report

---

## Office 365 Outlook

Purpose:

- Send assessment completion notifications
- Send remediation notifications
- Send management escalation emails

---

# Assessment Workflow

```text
Receive Assessment Request
            │
            ▼
Read Assessment Request
            │
            ▼
Read Application Inventory
            │
            ▼
Invoke Application Criticality Specialist
            │
            ▼
Invoke Recovery Requirements Specialist
            │
            ▼
Invoke Technical Recovery Specialist
            │
            ▼
Invoke Risk & Recovery Gap Specialist
            │
            ▼
Invoke Remediation Planning Specialist
            │
            ▼
Invoke Reporting & Communication Specialist
            │
            ▼
Consolidate Specialist Results
            │
            ▼
Determine Final Readiness Classification
            │
            ▼
Update Assessment Register
            │
            ▼
Generate Assessment Report
            │
            ▼
Send Stakeholder Notification
```

---

# Inputs

The Supervisor receives:

- Assessment Request
- Application ID
- Application metadata
- Recovery requirements
- Technical assessment results
- Specialist responses

---

# Outputs

The Supervisor produces:

- Overall BC/DR Readiness Classification
- Consolidated Assessment Summary
- Risk Assessment
- Recovery Gap Summary
- Remediation Recommendations
- Assessment Report
- Updated Assessment Register
- Stakeholder Notification

---

# Decision Logic

The Supervisor:

- Verifies that all required specialist responses are received.
- Identifies missing or incomplete assessments.
- Consolidates business and technical findings.
- Resolves assessment outcomes.
- Determines the final readiness classification based on the combined specialist recommendations.
- Initiates reporting and notification activities.

---

# Error Handling

The Supervisor handles situations such as:

- Missing assessment information
- Incomplete specialist responses
- Missing dependency information
- Insufficient assessment evidence
- Technical guidance unavailable from external services
- Duplicate assessment requests

When required information is unavailable, the Supervisor requests additional evidence or escalates the assessment for manual review.

---

# Benefits

- Centralized orchestration
- Standardized assessment workflow
- Consistent decision-making
- Modular specialist coordination
- Automated reporting
- Seamless Microsoft 365 integration
- Improved assessment accuracy and efficiency