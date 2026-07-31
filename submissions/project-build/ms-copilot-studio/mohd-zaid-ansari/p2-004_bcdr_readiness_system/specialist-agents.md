# Specialist Agents

## Overview

The Autonomous BC/DR Readiness Assessment solution uses six specialist agents. Each agent is responsible for a specific domain of the assessment, enabling the Supervisor Agent to coordinate a modular, scalable, and evidence-based workflow.

Each specialist performs only its assigned responsibility and returns structured findings to the Supervisor Agent. Specialists do not communicate directly with each other; all communication is coordinated by the Supervisor.

---

# 1. Application Criticality Specialist

## Purpose

Evaluates the business importance of the application and determines its criticality based on business impact.

## Responsibilities

- Assess business criticality
- Evaluate business impact
- Evaluate customer impact
- Evaluate regulatory impact
- Evaluate operational importance
- Identify business dependencies
- Return a structured criticality assessment

## Input

- Application details
- Business information
- Assessment context

## Output

- Business Criticality
- Business Impact Summary
- Operational Impact
- Regulatory Impact
- Customer Impact
- Criticality Rating

---

# 2. Recovery Requirements Specialist

## Purpose

Evaluates the application's recovery objectives and business continuity requirements.

## Responsibilities

- Assess Recovery Time Objective (RTO)
- Assess Recovery Point Objective (RPO)
- Evaluate downtime tolerance
- Identify recovery dependencies
- Assess continuity requirements
- Identify recovery gaps

## Input

- Application details
- Criticality assessment
- Recovery configuration

## Output

- Current RTO
- Current RPO
- Recovery Requirement Assessment
- Recovery Gaps
- Dependency Findings

---

# 3. Technical Recovery Specialist

## Purpose

Evaluates the application's technical recovery capabilities and validates them against Microsoft best practices.

## Responsibilities

- Assess technical recovery architecture
- Evaluate resilience
- Review disaster recovery configuration
- Retrieve Microsoft guidance using the configured MCP tool
- Identify technical recovery gaps

## Tools

- Microsoft Learn MCP Server

## Input

- Application infrastructure
- Azure services
- Hosting platform

## Output

- Technical Assessment
- Microsoft Guidance Summary
- Recovery Architecture Findings
- Technical Recovery Gaps

---

# 4. Risk & Recovery Gap Specialist

## Purpose

Consolidates specialist findings to identify BC/DR risks and readiness gaps.

## Responsibilities

- Review specialist outputs
- Identify recovery gaps
- Classify risk severity
- Consolidate assessment findings
- Recommend readiness status

## Input

- Criticality Assessment
- Recovery Requirements Assessment
- Technical Recovery Assessment

## Output

- Consolidated Risk Assessment
- Risk Severity
- Recovery Gap Summary
- Recommended Readiness Status

---

# 5. Remediation Planning Specialist

## Purpose

Generates practical remediation recommendations to address identified BC/DR gaps.

## Responsibilities

- Recommend corrective actions
- Prioritize remediation activities
- Identify suggested owners
- Recommend validation activities
- Produce implementation recommendations

## Input

- Consolidated Risk Assessment
- Recovery Gaps

## Output

- Remediation Plan
- Recommended Actions
- Priority Levels
- Suggested Owners
- Validation Recommendations

---

# 6. Reporting & Communication Specialist

## Purpose

Generates assessment deliverables and stakeholder communications.

## Responsibilities

- Generate the BC/DR Readiness Assessment Report
- Prepare stakeholder notifications
- Create communication drafts
- Summarize assessment outcomes

## Tools

- Microsoft Word
- Microsoft Outlook

## Input

- Final Assessment
- Readiness Classification
- Risk Assessment
- Remediation Plan

## Output

- BC/DR Readiness Assessment Report
- Stakeholder Email Draft
- Report Status
- Notification Status

---

# Agent Collaboration

The specialist agents execute in the following sequence under the control of the Supervisor Agent:

```text
BC/DR Supervisor Agent
        │
        ▼
Application Criticality Specialist
        │
        ▼
Recovery Requirements Specialist
        │
        ▼
Technical Recovery Specialist
        │
        ▼
Risk & Recovery Gap Specialist
        │
        ▼
Remediation Planning Specialist
        │
        ▼
Reporting & Communication Specialist
        │
        ▼
Supervisor Validates and Finalizes Assessment
```

---

# Design Principles

- Single responsibility for each specialist
- No direct communication between specialist agents
- Supervisor-controlled orchestration
- Evidence-based assessments
- Policy-driven decision making
- Structured inputs and outputs
- No assumptions or fabricated information
- Modular and scalable architecture
- Human escalation when required

---

# Benefits

- Clear separation of responsibilities
- Reusable specialist agents
- Improved assessment consistency
- Easier maintenance and extensibility
- Faster and more reliable BC/DR readiness assessments
- Standardized reporting and communication
```