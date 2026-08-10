
# Business Continuity & Disaster Recovery (BCDR) Readiness Assessment – Multi-Agent System

## Overview

This project implements an AI-powered Business Continuity and Disaster Recovery (BCDR) Readiness Assessment solution using Microsoft Copilot Studio.

The solution follows a Hub-and-Spoke (Supervisor–Specialist) architecture where a central Supervisor Agent orchestrates multiple specialist child agents to evaluate an application's BC/DR readiness, consolidate findings, generate an assessment report, and notify stakeholders.

The implementation is based on the provided Product Requirements Document (PRD) and is designed to demonstrate autonomous multi-agent orchestration using Microsoft Copilot Studio.

---

# Solution Architecture

The solution consists of one Supervisor Agent and six specialist child agents.

```
                    New Assessment Request
                              │
                              ▼
                 BCDR Supervisor Agent
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
Application           Recovery Requirements   Technical Recovery
Criticality             Specialist              Specialist
Specialist                                        │
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
                              │
                              ▼
                Report Generation & Email
```

---

# Implemented Agents

## Supervisor Agent

- BCDR Supervisor Agent

## Child Agents

- Application Criticality Specialist
- Recovery Requirements Specialist
- Technical Recovery Specialist
- Risk & Recovery Gap Specialist
- Remediation Planning Specialist
- Reporting & Communication Specialist

---

# Implemented Tools

## Supervisor Agent

- Get Application Details (Excel Online)
- Update Assessment Register (Excel Online)

## Technical Recovery Specialist

- Microsoft Learn Documentation MCP

## Reporting & Communication Specialist

- Generate BCDR Assessment Report
- Send BCDR Assessment Email (Outlook)

---

# Knowledge Sources

The following knowledge sources are used within the solution.

- NovaSphere BCDR Policy
- BCDR Readiness Assessment Report Template

---

# Data Sources

The implementation uses the following datasets.

- Assessment_Requests.csv
- P2-004_BCDR_Lab_Data.xlsx

The Excel workbook contains:

- ApplicationInventoryTable
- AssessmentRegisterTable

---

# Trigger

The assessment process starts using an Autonomous Trigger.

Trigger Name:

**New BC/DR Assessment Request**

The trigger monitors incoming assessment requests and starts the Supervisor Agent workflow.

---

# Assessment Workflow

1. Receive Assessment Request
2. Retrieve Application Details
3. Assess Business Criticality
4. Assess Recovery Requirements
5. Perform Technical Recovery Assessment
6. Identify Recovery Risks and Gaps
7. Generate Remediation Plan
8. Update Assessment Register
9. Generate Assessment Report
10. Notify Stakeholders

---

# Repository Structure

```
README.md
solution-summary.md
architecture.md
supervisor-agent-design.md
specialist-agents.md
mcp-implementation.md
autonomous-trigger.md
test-report.md
known-limitations.md
ai-usage-declaration.md
```

---

# Technology Stack

- Microsoft Copilot Studio
- Microsoft 365
- Excel Online (Business)
- Outlook
- Microsoft Learn MCP
- OneDrive for Business

---

# Project Objective

Develop an autonomous multi-agent system capable of assessing Business Continuity and Disaster Recovery readiness by coordinating specialized AI agents, producing a structured assessment report, and supporting organizational decision-making through Microsoft Copilot Studio.

---

# Current Status

✔ Architecture Designed

✔ Supervisor Agent Implemented

✔ Specialist Agents Implemented

✔ Excel Tool Configuration Completed

✔ Microsoft Learn MCP Integrated

✔ Report Generation Configured

✔ Email Notification Configured

✔ Autonomous Trigger Configured

⏳ End-to-End Testing Pending

---

# Documentation

Refer to the accompanying documentation for detailed implementation information.

- solution-summary.md
- architecture.md
- supervisor-agent-design.md
- specialist-agents.md
- mcp-implementation.md
- autonomous-trigger.md
- test-report.md
- known-limitations.md
- ai-usage-declaration.md
