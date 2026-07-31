# Specialist agents

## BC/DR specialist child agents

Microsoft Copilot Studio | Multi-agent architecture | Structured assessment workflow

## Overview

The BC/DR Readiness System uses **six specialist child agents** coordinated by the **BC/DR Supervisor Agent**.

Each specialist is responsible for a **single bounded assessment domain** and returns structured outputs to the Supervisor Agent.

The specialists do not generate final readiness classifications, final reports, or stakeholder communications independently.

The Supervisor Agent remains responsible for consolidation, validation, decision making, and assessment completion.

## Specialist architecture

```text
BC/DR Supervisor Agent
        |
        +--------------------------------------+
        |                                      |
        +--> Application Criticality Specialist
        |
        +--> Recovery Requirements Specialist
        |
        +--> Technical Recovery Specialist
        |       |
        |       +--> Microsoft Learn MCP Server
        |
        +--> Risk & Recovery Gap Specialist
        |
        +--> Remediation Planning Specialist
        |
        +--> Reporting & Communication Specialist
```

## Agent 1: Application Criticality Specialist

### Purpose

Determine the business importance of an application and classify its operational criticality.

### Responsibilities

Evaluate:

* business function,
* customer impact,
* financial impact,
* regulatory impact,
* data sensitivity,
* operational dependency,
* outage tolerance,
* recovery urgency.

### Tool access

Excel Online (Business)

Used for retrieving application information from the application inventory workbook.

### Input

* Application ID
* Application Name
* Business profile
* Ownership information
* Dependency information
* Recovery objective information

### Output

* Criticality classification
* Criticality rationale
* Business impact assessment
* Maximum acceptable outage
* Dependency risk
* Recovery urgency
* Confidence level

### Classification levels

* Mission Critical
* Business Critical
* Important
* Standard

The specialist does not perform technical recovery analysis.

## Agent 2: Recovery Requirements Specialist

### Purpose

Evaluate whether recovery objectives are appropriate for the application’s business criticality.

### Responsibilities

Assess:

* RTO,
* RPO,
* maximum tolerable downtime,
* manual workaround,
* dependency recovery order,
* recovery requirement completeness,
* recovery requirement consistency.

### Tool access

Excel Online (Business)

Used for retrieving recovery-related application information.

### Input

* Criticality classification
* Current RTO
* Current RPO
* Maximum tolerable downtime
* Operating hours
* Dependency information
* Manual workaround information

### Output

* RTO assessment
* RPO assessment
* Recovery gaps
* Recovery inconsistencies
* Dependency recovery risk
* Recovery requirement recommendation
* Confidence level

### Gap detection

The specialist identifies:

* missing RTO,
* missing RPO,
* RTO exceeding MTD,
* excessive RPO,
* dependency conflicts,
* missing manual workaround.

The specialist does not evaluate Azure technologies.

## Agent 3: Technical Recovery Specialist

### Purpose

Evaluate technical recovery capability and Azure resiliency using **Microsoft Learn MCP**.

### Responsibilities

Assess:

* backup configuration,
* disaster recovery configuration,
* recovery testing,
* Azure resiliency,
* recovery architecture,
* Microsoft recovery guidance.

### Tool access

Excel Online (Business)

Retrieves technical application information.

Microsoft Learn MCP Server

Retrieves current Microsoft documentation.

### MCP configuration

Endpoint:

https://learn.microsoft.com/api/mcp

Transport:

Streamable HTTP

Authentication:

Public endpoint

### Input

* Hosting platform
* Azure service
* Backup configuration
* DR configuration
* Recovery testing information

### Output

* Backup status
* DR status
* Recovery test status
* Microsoft guidance summary
* Technical recovery gaps
* Recovery architecture assessment
* MCP evidence status
* Confidence level

### MCP evidence rule

All Microsoft technical guidance must come from MCP retrieval.

If MCP is unavailable, the specialist returns:

* technical evidence unavailable,
* MCP lookup unsuccessful,
* manual technical review required.

No Microsoft guidance is fabricated.

## Agent 4: Risk & Recovery Gap Specialist

### Purpose

Consolidate business, recovery, and technical findings into a structured BC/DR risk assessment.

### Responsibilities

Evaluate:

* recovery gaps,
* technical gaps,
* dependency gaps,
* documentation gaps,
* ownership gaps,
* evidence sufficiency,
* operational recovery risk.

### Tool access

Excel Online (Business)

Used only when additional application evidence is required.

### Input

* Criticality findings
* Recovery findings
* Technical findings
* Backup assessment
* DR assessment
* Dependency assessment
* Evidence assessment

### Output

* Critical gaps
* High gaps
* Medium gaps
* Low gaps
* Gap counts
* Overall readiness assessment
* Risk assessment
* Evidence limitations
* Confidence level

### Readiness classifications

* Ready
* Ready with Minor Gaps
* Remediation Required
* High Risk
* Insufficient Evidence

The specialist does not generate remediation plans.

## Agent 5: Remediation Planning Specialist

### Purpose

Convert validated BC/DR gaps into actionable remediation plans.

### Responsibilities

Generate:

* remediation actions,
* ownership recommendations,
* implementation priorities,
* validation requirements,
* implementation sequencing.

### Tool access

Excel Online (Business)

Used when ownership or dependency information requires validation.

### Input

* Validated gap assessment
* Criticality classification
* Readiness classification
* Ownership information
* Dependency information

### Output

For each remediation action:

* Gap ID
* Gap description
* Recommended action
* Remediation category
* Priority
* Suggested owner
* Target timeline
* Dependency
* Validation requirement
* Expected outcome

### Remediation categories

* Configuration remediation
* Architecture review
* Documentation remediation
* Recovery testing
* Business decision
* Dependency review
* Missing evidence
* Management escalation

The specialist does not claim that remediation has been completed.

## Agent 6: Reporting & Communication Specialist

### Purpose

Generate the official BC/DR assessment report and send stakeholder communications after Supervisor approval.

### Responsibilities

Generate:

* Word assessment report,
* management-ready documentation,
* stakeholder notifications,
* escalation communications.

### Tool access

Word Online (Business)

Creates assessment reports from the Word template.

Outlook

Sends approved stakeholder notifications.

### Input

Approved assessment results including:

* assessment metadata,
* criticality findings,
* recovery findings,
* technical findings,
* risk assessment,
* remediation plan,
* Supervisor decision,
* evidence limitations.

### Output

* Report generation status
* Report file name
* Report validation status
* Notification status
* Communication completion status

### Notification rules

Ready

Routine completion notification.

Ready with Minor Gaps

Notify application and technical owners.

Remediation Required

Notify owners and remediation stakeholders.

High Risk

Escalate to management.

Insufficient Evidence

Request additional information.

Notifications are sent only after Supervisor approval.

## Tool access matrix

| Specialist                | Excel | Word | Outlook | MCP |
| ------------------------- | ----- | ---- | ------- | --- |
| Application Criticality   | Yes   | No   | No      | No  |
| Recovery Requirements     | Yes   | No   | No      | No  |
| Technical Recovery        | Yes   | No   | No      | Yes |
| Risk & Recovery Gap       | Yes   | No   | No      | No  |
| Remediation Planning      | Yes   | No   | No      | No  |
| Reporting & Communication | No    | Yes  | Yes     | No  |

## Context handoff

The Supervisor Agent provides a structured assessment context to each specialist.

Standard context includes:

* Assessment ID
* Application ID
* Application Name
* Application record
* Relevant specialist context
* Previous assessment outputs when required

Each specialist returns structured data only.

## Output contract

Every specialist returns:

* Assessment_ID
* Specialist_Name
* Structured findings
* Evidence status
* Missing information
* Confidence level

This enables reliable Supervisor validation and consolidation.

## Orchestration principles

The specialist architecture follows these principles.

### Bounded responsibility

Each agent performs one assessment function only.

### Structured outputs

All findings are returned in structured form.

### Evidence-first analysis

Technical conclusions require Microsoft MCP evidence.

### No autonomous completion

Specialists cannot complete assessments independently.

### Supervisor governance

The Supervisor validates all specialist outputs before any report generation or stakeholder communication.

This architecture ensures separation of responsibilities, evidence-grounded technical assessment, reliable multi-agent orchestration, and enterprise-grade BC/DR assessment governance within Microsoft Copilot Studio.
