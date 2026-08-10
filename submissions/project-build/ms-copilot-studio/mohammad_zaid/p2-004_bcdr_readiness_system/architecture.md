
# System Architecture

## Overview

The Business Continuity & Disaster Recovery (BCDR) Readiness Assessment solution is implemented as a Hub-and-Spoke multi-agent architecture using Microsoft Copilot Studio.

The architecture consists of a single Supervisor Agent responsible for orchestrating the complete assessment lifecycle and multiple specialist child agents responsible for performing domain-specific analysis.

This design ensures clear separation of responsibilities, modularity, scalability, and maintainability while keeping orchestration centralized.

---

# Architecture Pattern

The solution follows the **Hub-and-Spoke Architecture**.

```

                          Assessment Request
                                  │
                                  ▼
                     BCDR Supervisor Agent
                                  │
        ┌───────────────┬──────────────┬───────────────┐
        │               │              │               │
        ▼               ▼              ▼               ▼
 Application      Recovery        Technical        Risk &
 Criticality     Requirements      Recovery        Recovery Gap
 Specialist       Specialist       Specialist      Specialist
                                         │
                                         ▼
                              Microsoft Learn MCP
                                  │
                                  ▼
                    Remediation Planning Specialist
                                  │
                                  ▼
             Reporting & Communication Specialist
                                  │
                                  ▼
                  Report Generation & Email Delivery

```

---

# Why Hub-and-Spoke?

The PRD requires:

- Centralized orchestration
- Sequential assessment execution
- Shared assessment context
- Consolidated decision making
- Single final assessment report

A Hub-and-Spoke model naturally supports these requirements by allowing one agent to coordinate all specialist agents while maintaining a single source of control.

---

# Components

## 1. Supervisor Agent

**Agent Name**

BCDR Supervisor Agent

### Responsibilities

- Receive assessment requests
- Retrieve application details
- Coordinate specialist agents
- Maintain assessment context
- Consolidate specialist findings
- Determine overall BC/DR readiness
- Update the Assessment Register
- Initiate report generation
- Trigger stakeholder notifications

The Supervisor Agent performs orchestration only and does not execute specialist assessments directly.

---

## 2. Specialist Agents

### Application Criticality Specialist

Evaluates:

- Business criticality
- Customer impact
- Regulatory impact
- Revenue impact
- Data classification
- Overall application criticality

Output:

Business Criticality Assessment

---

### Recovery Requirements Specialist

Evaluates:

- Recovery Time Objective (RTO)
- Recovery Point Objective (RPO)
- Maximum Tolerable Downtime
- Recovery priorities

Output:

Recovery Requirements Assessment

---

### Technical Recovery Specialist

Evaluates:

- Backup configuration
- Backup frequency
- Disaster Recovery configuration
- Recovery infrastructure
- Technical resilience

Uses Microsoft Learn MCP to validate Microsoft best practices where applicable.

Output:

Technical Recovery Assessment

---

### Risk & Recovery Gap Specialist

Evaluates:

- Recovery gaps
- Business risks
- Technical risks
- Compliance gaps
- Missing recovery capabilities

Output:

Risk Assessment

---

### Remediation Planning Specialist

Produces:

- Recommended remediation actions
- Priority improvements
- Recovery roadmap
- Readiness enhancement recommendations

Output:

Remediation Plan

---

### Reporting & Communication Specialist

Responsible for:

- Generating the BC/DR Readiness Assessment Report
- Sending assessment notification emails
- Formatting assessment output
- Communicating final results

Output:

Final Assessment Report

---

# Data Sources

The solution consumes data from the following sources.

## Assessment Requests

Assessment_Requests.csv

Purpose:

Initiates new BC/DR assessments.

---

## Application Inventory

ApplicationInventoryTable

Purpose:

Stores application metadata used throughout the assessment.

---

## Assessment Register

AssessmentRegisterTable

Purpose:

Stores completed assessment results.

---

# Knowledge Sources

The following organizational documents are configured as knowledge sources.

## NovaSphere BCDR Policy

Purpose:

Provides organizational BC/DR policies and governance guidelines used by specialist agents.

---

## BCDR Readiness Assessment Report Template

Purpose:

Provides the structure, formatting, and layout reference for generating the final assessment report.

---

# External Integrations

## Excel Online (Business)

Used by the Supervisor Agent to:

- Retrieve application details
- Update assessment records

---

## Microsoft Learn MCP

Used by the Technical Recovery Specialist.

Purpose:

Retrieve Microsoft best practices for:

- Backup
- Disaster Recovery
- Azure Availability
- Business Continuity
- Recovery Planning

---

## Outlook

Used by the Reporting & Communication Specialist.

Purpose:

Send assessment completion notifications to stakeholders.

---

# Assessment Workflow

The Supervisor Agent coordinates the following execution sequence.

```

Assessment Request

↓

Retrieve Application Details

↓

Application Criticality Assessment

↓

Recovery Requirements Assessment

↓

Technical Recovery Assessment

↓

Risk & Recovery Gap Assessment

↓

Remediation Planning

↓

Assessment Consolidation

↓

Update Assessment Register

↓

Generate Assessment Report

↓

Send Notification Email

↓

Assessment Complete

```

---

# Data Flow

```

Assessment Request

↓

Supervisor Agent

↓

Get Application Details (Excel)

↓

Child Agents

↓

Assessment Results

↓

Supervisor Agent

↓

Update Assessment Register (Excel)

↓

Reporting & Communication Specialist

↓

Assessment Report

↓

Outlook Email

↓

Stakeholders

```

---

# Design Principles

The architecture follows these principles.

### Single Responsibility

Each specialist agent is responsible for one assessment domain only.

---

### Centralized Orchestration

The Supervisor Agent controls the complete workflow and sequencing.

---

### Reusability

Specialist agents are modular and can be reused independently if required.

---

### Extensibility

Additional specialist agents can be incorporated into the workflow without redesigning the orchestration model.

---

### Maintainability

Changes to assessment logic remain isolated within the corresponding specialist agent.

---

# Technology Stack

- Microsoft Copilot Studio
- Microsoft 365
- Excel Online (Business)
- Outlook
- OneDrive for Business
- Microsoft Learn MCP

---

# Architecture Summary

The implemented Hub-and-Spoke architecture provides a structured and scalable approach to BC/DR readiness assessment. By separating orchestration from domain-specific analysis, the solution achieves modularity, maintainability, and consistent execution while remaining aligned with the project requirements defined in the PRD.
