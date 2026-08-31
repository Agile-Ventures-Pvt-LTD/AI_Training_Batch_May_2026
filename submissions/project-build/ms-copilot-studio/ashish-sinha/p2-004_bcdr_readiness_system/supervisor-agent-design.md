# Supervisor Agent Design

## Overview

The **BC/DR Supervisor Agent** is the central orchestrator of the BC/DR Readiness Assessment System. It coordinates the assessment workflow by retrieving application information, invoking specialized child agents, validating their outputs, determining the final readiness classification, and initiating reporting activities.

The Supervisor Agent does **not** perform business or technical analysis itself. Instead, it delegates specialized tasks to child agents and consolidates their results into a final assessment.

---

# Objectives

The Supervisor Agent is responsible for:

- Receiving assessment requests
- Building the assessment context
- Coordinating specialist agents
- Passing context between agents
- Validating assessment results
- Handling execution failures
- Determining the overall readiness classification
- Triggering report generation
- Completing the assessment workflow

---

# Architecture

```text
                 Assessment Request
                        │
                        ▼
              BC/DR Supervisor Agent
                        │
      ┌─────────────────┼─────────────────┐
      │                 │                 │
      ▼                 ▼                 ▼
Application      Recovery Requirements   Technical
Criticality          Specialist          Recovery
 Specialist                              Specialist
                                             │
                                             ▼
                                  Microsoft Learn MCP
                        │
                        ▼
             Risk & Recovery Gap Specialist
                        │
                        ▼
            Remediation Planning Specialist
                        │
                        ▼
     Reporting & Communication Specialist
```

---

# Responsibilities

The Supervisor Agent performs the following tasks:

1. Receive assessment requests.
2. Retrieve application information.
3. Create the assessment context.
4. Invoke child agents.
5. Collect specialist outputs.
6. Validate findings.
7. Determine overall readiness.
8. Trigger reporting.
9. Return the final assessment.

---

# Assessment Workflow

## Step 1 – Receive Assessment Request

The workflow begins when an autonomous trigger or user request provides:

- Assessment ID
- Application ID

Example:

```json
{
  "AssessmentID": "BCDR-001",
  "ApplicationID": "APP-001"
}
```

---

## Step 2 – Retrieve Application Information

The Supervisor retrieves application information from the Application Inventory.

Typical information includes:

- Application Name
- Business Owner
- Technical Owner
- Business Criticality
- RTO
- RPO
- Recovery Information
- Technical Configuration

This information becomes the **Assessment Context**.

---

## Step 3 – Invoke Child Agents

The Supervisor invokes the child agents in the following sequence.

### 1. Application Criticality Specialist

Purpose:

Determine business criticality.

Output:

- Criticality Classification
- Business Impact Summary

---

### 2. Recovery Requirements Specialist

Purpose:

Evaluate recovery objectives.

Output:

- RTO Assessment
- RPO Assessment
- Recovery Requirement Findings

---

### 3. Technical Recovery Specialist

Purpose:

Evaluate technical recovery capabilities.

Responsibilities include:

- Backup assessment
- Disaster Recovery assessment
- Recovery testing validation
- Microsoft Learn MCP integration

Output:

- Technical Findings
- Evidence Status
- Recovery Gaps

---

### 4. Risk & Recovery Gap Specialist

Purpose:

Combine specialist findings.

Output:

- Gap Summary
- Severity Classification
- Recommended Readiness

---

### 5. Remediation Planning Specialist

Purpose:

Generate remediation recommendations.

Output:

- Recommended Actions
- Suggested Owners
- Validation Requirements

---

### 6. Reporting & Communication Specialist

Purpose:

Generate assessment artifacts.

Responsibilities:

- Generate Word report
- Update Excel register
- Send Outlook notification

---

# Assessment Context

The Supervisor maintains a shared assessment context throughout execution.

Example fields include:

| Field | Description |
|---------|-------------|
| AssessmentID | Unique assessment identifier |
| ApplicationID | Application identifier |
| ApplicationName | Application name |
| BusinessOwner | Business owner |
| TechnicalOwner | Technical owner |
| BusinessCriticality | Current classification |
| CurrentRTO | Recovery Time Objective |
| CurrentRPO | Recovery Point Objective |
| Specialist Results | Outputs from child agents |

The Supervisor passes the relevant context to each child agent.

---

# Child Agent Orchestration

```text
Assessment Context
        │
        ▼
Application Criticality
        │
        ▼
Recovery Requirements
        │
        ▼
Technical Recovery
        │
        ▼
Risk Assessment
        │
        ▼
Remediation Planning
        │
        ▼
Reporting
```

Each child agent receives:

- Assessment Context
- Previous specialist outputs (where required)

---

# Validation Logic

After all specialists complete, the Supervisor validates:

- All mandatory agents executed successfully.
- Required outputs are available.
- Technical evidence is available or documented as unavailable.
- No conflicting specialist findings exist.
- The assessment can be completed.

If mandatory information is missing, the final status is:

```
Insufficient Evidence
```

---

# Readiness Decision

The Supervisor assigns exactly one readiness classification.

Possible outcomes are:

| Status | Description |
|----------|-------------|
| Ready | No significant BC/DR gaps identified |
| Ready with Minor Gaps | Minor issues identified with low operational risk |
| Remediation Required | Medium or high-priority remediation actions required |
| High Risk | Critical recovery gaps identified |
| Insufficient Evidence | Required assessment evidence is unavailable |

The Supervisor is the only component authorized to assign the final readiness status.

---

# Error Handling

The Supervisor supports graceful failure handling.

## Child Agent Failure

Action:

- Retry once.
- Record the failure.
- Continue where possible.
- Do not fabricate results.

---

## Microsoft Learn MCP Failure

Action:

- Record the MCP failure.
- Mark technical evidence as unavailable.
- Continue the assessment.
- Do not generate unsupported technical recommendations.

---

## Reporting Failure

If report generation fails:

- Record the failure.
- Return the assessment.
- Report the tool error.

---

## Notification Failure

If email delivery fails:

- Record the failure.
- Do not repeat report generation.
- Return the notification status.

---

# Inputs

The Supervisor receives:

| Input | Description |
|---------|-------------|
| AssessmentID | Assessment identifier |
| ApplicationID | Target application |
| TriggerType | Scheduled or event-driven trigger |
| RequestedBy | User or system |

---

# Outputs

The Supervisor returns:

| Output | Description |
|---------|-------------|
| AssessmentID | Assessment identifier |
| ApplicationID | Target application |
| Overall Readiness | Final readiness classification |
| Criticality Classification | Business criticality result |
| Gap Summary | Consolidated gaps |
| Remediation Summary | Recommended actions |
| Report Status | Word generation result |
| Notification Status | Outlook notification result |
| Assessment Status | Final execution status |

---

# Design Principles

The Supervisor Agent follows these principles:

- Orchestrate rather than analyze
- Delegate specialist tasks
- Preserve assessment context
- Validate specialist outputs
- Support evidence-based decisions
- Handle failures gracefully
- Ensure end-to-end workflow completion

---

# Summary

The Supervisor Agent serves as the orchestration layer of the BC/DR Readiness Assessment System. By coordinating specialized child agents, managing shared assessment context, validating results, and initiating reporting, it enables a scalable, maintainable, and autonomous assessment workflow while ensuring that business and technical evaluations remain evidence-based and traceable.