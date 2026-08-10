# Sleepsia Quality Intelligence Control Tower

## Overview

The Sleepsia Quality Intelligence Control Tower is a Microsoft Copilot Studio solution designed to automate quality-investigation workflows for customer complaints.

The solution follows a supervisor-specialist architecture where a central Quality Supervisor orchestrates complaint validation, specialist investigations, incident management, CAPA processing, reassessment activities, report generation, and stakeholder notifications.

The objective is to provide a structured, policy-driven approach to complaint handling while maintaining auditability and consistency across quality investigations.

---

## Key Features

- Autonomous complaint processing
- Complaint intake validation
- Specialist-based investigation workflow
- Policy-driven incident classification
- Incident lifecycle management
- CAPA initiation and ownership assignment
- Selective reassessment processing
- Investigation report generation
- Stakeholder notification workflow
- Interactive quality and product guidance

---

## Solution Architecture

The solution is built using a supervisor-specialist orchestration model.

### Supervisor

- Quality Supervisor

### Specialist Agents

- Complaint Pattern Specialist
- Returns Specialist
- Product/Batch Specialist
- Customer Impact Specialist
- CAPA Specialist
- M365 Guidance Specialist

### Decision Topics

- Incident Intake & Validation
- Quality Investigation Decision
- CAPA Planning & Ownership
- Evidence Update & Selective Reassessment

---

## Knowledge Sources

The solution uses the following knowledge sources:

- Sleepsia Product Quality Policy
- Sleepsia Product Care and Usage Guide
- Sleepsia Customer Resolution Policy
- Approved Product Information Sources

---

## Data Sources

The solution uses workbook tables including:

- Customer Complaints
- Quality Incidents
- CAPA Register
- Product Master
- Batch Register
- Returns
- Sales Summary
- Owners

---

## Autonomous Workflow Mode

1. Retrieve unprocessed complaint.
2. Validate complaint evidence.
3. Execute specialist investigations.
4. Build investigation metrics.
5. Execute quality investigation decision.
6. Create or update incident records.
7. Execute CAPA processing when required.
8. Execute reassessment processing when required.
9. Generate investigation report.
10. Send notifications.
11. Mark complaint as processed.

---

## Interactive Mode

Interactive mode supports:

- Product guidance
- Policy guidance
- Quality guidance
- Customer-resolution guidance
- Product-information retrieval

Interactive mode is read-only and does not modify records.

---

## Repository Contents

- README.md
- ai-usage-declaration.md
- architecture.md
- custom-topics.md
- knowledge-sources.md
- known-limitations.md
- mcp-implementation.md
- orchestration-patterns.md
- publishing.md
- screenshots/
- test-report.md
- tool-implementation.md

---

## Agent Access

### Copilot Studio Agent

**Agent Name:** Sleepsia Quality Intelligence Control Tower

**Editor Access Link:**

```
https://copilotstudio.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/bf323b02-8494-f111-b8dc-000d3af21e08/overview
```

---

## Author

**Subhranshu Pattnayak**

Project developed as part of the MCP + Agentic AI implementation assignment using Microsoft Copilot Studio.