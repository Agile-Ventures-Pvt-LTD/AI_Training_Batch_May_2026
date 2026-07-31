# Specialist Agents

## Overview

The BCDR Readiness Assessment System uses six specialist agents, each responsible for a specific stage of the BC/DR readiness assessment. The Supervisor Agent delegates assessment activities to these specialists and consolidates their outputs into the final assessment.

---

# 1. Application Criticality Specialist

## Responsibility

Determines the business criticality of the application based on its business impact and operational importance.

### Input

* Application profile
* Business information
* Customer impact
* Revenue impact
* Regulatory impact
* Business dependencies

### Output

* Criticality Classification
* Supporting Rationale

---

# 2. Recovery Requirements Specialist

## Responsibility

Evaluates whether the application's recovery objectives align with business requirements.

### Input

* Current RTO
* Current RPO
* Maximum Tolerable Downtime
* Manual Workaround
* Recovery Procedure
* Criticality Classification

### Output

* RTO Assessment
* RPO Assessment
* Recovery Requirement Assessment
* Recovery Gaps
* Confidence Indicator

---

# 3. Technical Recovery Specialist

## Responsibility

Assesses the application's technical recovery capabilities using Microsoft Learn MCP guidance.

### Input

* Hosting Platform
* Azure Service
* Backup Status
* Disaster Recovery Status
* Application Name

### Output

* Microsoft Technology Evaluated
* Technical Capability Assessment
* Recovery Gap
* Recommendation
* Evidence Status

---

# 4. Risk and Recovery Gap Specialist

## Responsibility

Identifies recovery risks, classifies assessment gaps, and determines the overall readiness recommendation.

### Input

* Criticality Assessment
* Recovery Requirements Assessment
* Technical Recovery Assessment

### Output

* Identified Gaps
* Gap Severity
* Overall Risk
* Readiness Recommendation

---

# 5. Remediation Planning Specialist

## Responsibility

Creates remediation actions for the identified BC/DR gaps.

### Input

* Identified Gaps
* Overall Risk

### Output

* Recommended Actions
* Priority
* Suggested Owner
* Validation Requirements
* Expected Outcome

---

# 6. Reporting and Communication Specialist

## Responsibility

Generates the BC/DR Readiness Assessment Report and prepares stakeholder communication after Supervisor approval.

### Input

* Final validated assessment
* Overall Readiness
* Remediation Plan
* Supervisor Decision

### Output

* BC/DR Readiness Assessment Report
* Stakeholder Notification
* Report Status
* Notification Status

---

# Specialist Agent Collaboration

```text
BCDR Supervisor Agent
        │
        ├── Application Criticality Specialist
        ├── Recovery Requirements Specialist
        ├── Technical Recovery Specialist
        ├── Risk and Recovery Gap Specialist
        ├── Remediation Planning Specialist
        └── Reporting and Communication Specialist
```

Each specialist focuses on a single responsibility and returns structured assessment results to the Supervisor Agent, ensuring a modular and consistent BC/DR readiness assessment process.
