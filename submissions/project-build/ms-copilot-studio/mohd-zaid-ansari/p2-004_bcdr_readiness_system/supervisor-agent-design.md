# Supervisor Agent Design

## Agent Name

**Mohd Zaid Autonomous Multi-Agent**

---

# Purpose

The BC/DR Supervisor Agent orchestrates the complete Business Continuity and Disaster Recovery (BC/DR) readiness assessment. It coordinates specialist agents, validates their outputs, determines the final readiness classification, and manages report generation, stakeholder communication, and assessment record updates.

The Supervisor does **not** perform domain-specific analysis itself. Instead, it delegates each responsibility to the appropriate specialist agent and consolidates the results into a single assessment outcome.

---

# Responsibilities

The Supervisor Agent is responsible for:

- Receiving assessment requests from the configured trigger.
- Retrieving assessment and application information using configured tools.
- Applying organizational BC/DR policy.
- Determining the assessment scope.
- Invoking specialist agents.
- Passing assessment context between specialists.
- Validating specialist outputs.
- Detecting missing or conflicting findings.
- Coordinating reassessment when required.
- Determining the final readiness classification.
- Authorizing report generation.
- Authorizing stakeholder communication.
- Updating the assessment register.
- Returning the final structured assessment result.

---

# Workflow

```text
Assessment Trigger
        │
        ▼
Retrieve Assessment Data
        │
        ▼
Retrieve Application Data
        │
        ▼
Apply BC/DR Policy
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
Validate Results
        │
        ▼
Determine Final Readiness
        │
        ▼
Invoke Reporting & Communication Specialist
        │
        ▼
Update Assessment Register
        │
        ▼
Complete Assessment
```

---

# Child Agents

The Supervisor coordinates the following specialist agents:

| Specialist Agent | Responsibility |
|------------------|---------------|
| Application Criticality Specialist | Evaluates business criticality and business impact. |
| Recovery Requirements Specialist | Assesses RTO, RPO, downtime tolerance, and recovery requirements. |
| Technical Recovery Specialist | Evaluates technical recovery architecture and retrieves Microsoft guidance. |
| Risk & Recovery Gap Specialist | Consolidates findings, identifies risks, and recommends readiness status. |
| Remediation Planning Specialist | Generates prioritized remediation actions. |
| Reporting & Communication Specialist | Generates reports and prepares stakeholder communications. |

---

# Decision Logic

The Supervisor validates all specialist outputs before making a decision.

Validation includes:

- Missing specialist responses
- Conflicting recommendations
- Missing evidence
- Policy compliance
- Technical evidence availability

If required information cannot be validated, the assessment is escalated for manual review.

---

# Final Readiness Classification

The Supervisor determines exactly one of the following:

- Ready
- Ready with Minor Gaps
- Remediation Required
- High Risk
- Insufficient Evidence

---

# Escalation Conditions

Escalation is required when:

- Assessment information cannot be retrieved.
- Application information is unavailable.
- Mandatory evidence is missing.
- Specialist findings conflict and cannot be reconciled.
- Microsoft technical guidance is unavailable.
- Manual approval is required.

---

# Tools Used

The Supervisor uses configured tools to:

- Retrieve assessment requests
- Retrieve application information
- Update assessment records

The Supervisor delegates report generation and stakeholder communication to the Reporting & Communication Specialist.

---

# Inputs

The Supervisor receives:

- Assessment Request
- Application Information
- BC/DR Policy
- Specialist Assessment Results

---

# Outputs

The Supervisor produces:

- Final Readiness Classification
- Consolidated Risk Summary
- Remediation Priority
- Assessment Status
- Report Status
- Notification Status
- Escalation Decision

---

# Design Principles

- Single orchestration point
- Delegation to specialist agents
- Policy-driven decision making
- Evidence-based assessment
- No assumption of missing information
- Human escalation for unresolved issues
- Structured and auditable workflow
- Modular and scalable architecture

---

# Benefits

- Automates BC/DR readiness assessments
- Ensures consistent decision making
- Reduces manual effort
- Standardizes recovery evaluations
- Improves governance and compliance
- Produces structured reports and stakeholder notifications
- Supports scalable multi-agent orchestration
```