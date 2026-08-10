
# Specialist Agents Design

## Overview

The Business Continuity & Disaster Recovery (BCDR) Readiness Assessment solution uses six specialist child agents coordinated by the BCDR Supervisor Agent.

Each specialist agent is responsible for a single assessment domain. They perform independent analysis using the information provided by the Supervisor Agent and return structured findings without making the final readiness decision.

The Supervisor Agent remains the only agent responsible for orchestration and final assessment consolidation.

---

# 1. Application Criticality Specialist

## Purpose

Evaluate the business importance of the application and determine its overall business criticality.

---

## Responsibilities

- Review application information.
- Assess business impact.
- Assess customer impact.
- Assess operational dependency.
- Assess regulatory impact.
- Determine application criticality.

---

## Input

Receives from Supervisor Agent:

- Application Details
- Business Owner
- Business Function
- Customer Facing Status
- Number of Users
- Business Criticality Information

---

## Output

Returns:

- Criticality Rating
- Business Impact Summary
- Customer Impact Assessment
- Operational Dependency Assessment
- Overall Criticality Findings

---

## Knowledge Source

NovaSphere BCDR Policy

---

## Tools

No external tools required.

---

# 2. Recovery Requirements Specialist

## Purpose

Determine the application's recovery objectives and continuity requirements.

---

## Responsibilities

- Evaluate Recovery Time Objective (RTO).
- Evaluate Recovery Point Objective (RPO).
- Assess business continuity requirements.
- Review recovery priorities.

---

## Input

Receives from Supervisor Agent:

- Application Details
- Business Criticality Assessment
- Existing Recovery Information

---

## Output

Returns:

- Recovery Time Objective
- Recovery Point Objective
- Recovery Requirements
- Business Continuity Findings

---

## Knowledge Source

NovaSphere BCDR Policy

---

## Tools

No external tools required.

---

# 3. Technical Recovery Specialist

## Purpose

Assess the application's technical recovery capabilities and validate recovery practices using Microsoft documentation.

---

## Responsibilities

- Review backup strategy.
- Review disaster recovery capability.
- Assess high availability.
- Evaluate technical resilience.
- Validate recommendations using Microsoft Learn.

---

## Input

Receives from Supervisor Agent:

- Application Details
- Recovery Requirements
- Infrastructure Information

---

## Output

Returns:

- Backup Assessment
- Disaster Recovery Assessment
- Technical Recovery Findings
- Azure Best Practice Validation
- Technical Recommendations

---

## Knowledge Sources

- NovaSphere BCDR Policy

---

## Tools

### Microsoft Learn Docs MCP

Purpose:

Retrieve Microsoft guidance related to:

- Disaster Recovery
- Backup
- High Availability
- Azure Resiliency
- Business Continuity

---

# 4. Risk & Recovery Gap Specialist

## Purpose

Identify risks, deficiencies and recovery gaps that may affect business continuity.

---

## Responsibilities

- Identify recovery risks.
- Evaluate compliance gaps.
- Identify missing recovery capabilities.
- Assess operational risks.

---

## Input

Receives from Supervisor Agent:

- Business Criticality Findings
- Recovery Requirements
- Technical Recovery Findings

---

## Output

Returns:

- Risk Assessment
- Recovery Gap Analysis
- Compliance Findings
- Overall Risk Summary

---

## Knowledge Source

NovaSphere BCDR Policy

---

## Tools

No external tools required.

---

# 5. Remediation Planning Specialist

## Purpose

Develop recommendations that improve the application's BC/DR readiness.

---

## Responsibilities

- Analyse identified gaps.
- Recommend corrective actions.
- Prioritize remediation activities.
- Improve recovery readiness.

---

## Input

Receives from Supervisor Agent:

- Risk Assessment
- Recovery Gap Analysis
- Technical Findings

---

## Output

Returns:

- Remediation Plan
- Priority Recommendations
- Recovery Improvement Roadmap

---

## Knowledge Source

NovaSphere BCDR Policy

---

## Tools

No external tools required.

---

# 6. Reporting & Communication Specialist

## Purpose

Generate the final BC/DR Readiness Assessment Report and communicate assessment results to stakeholders.

---

## Responsibilities

- Generate the assessment report.
- Follow the report structure defined in the report template.
- Summarize assessment findings.
- Send assessment notifications.
- Prepare stakeholder communication.

---

## Input

Receives from Supervisor Agent:

- Complete Assessment Results
- Overall Readiness
- Risk Assessment
- Remediation Plan
- Assessment Metadata

---

## Output

Returns:

- BC/DR Readiness Assessment Report
- Assessment Summary
- Email Notification Status

---

## Knowledge Sources

- BCDR_Readiness_Assessment_Report_Template.docx

---

## Tools

### Generate BCDR Assessment Report

Purpose:

Generate a new BC/DR Readiness Assessment Report using the provided report template as a structural reference.

---

### Send BCDR Assessment Email

Connector:

Office 365 Outlook

Purpose:

Notify stakeholders after successful assessment completion.

---

# Child Agent Communication

All specialist agents communicate only with the BCDR Supervisor Agent.

Child agents do not communicate directly with one another.

The Supervisor Agent is responsible for:

- Passing assessment context.
- Invoking specialist agents.
- Collecting assessment findings.
- Consolidating results.
- Initiating report generation.

---

# Execution Sequence

The child agents execute in the following order:

1. Application Criticality Specialist
2. Recovery Requirements Specialist
3. Technical Recovery Specialist
4. Risk & Recovery Gap Specialist
5. Remediation Planning Specialist
6. Reporting & Communication Specialist

Each specialist completes its assessment before the Supervisor Agent invokes the next specialist.

---

# Design Principles

The specialist agents follow these principles:

- Single Responsibility
- Independent Assessment
- No Cross-Agent Communication
- Stateless Execution
- Structured Outputs
- Supervisor-Controlled Orchestration

Each specialist focuses exclusively on its assigned assessment domain while the Supervisor Agent remains responsible for workflow coordination and final decision making.
