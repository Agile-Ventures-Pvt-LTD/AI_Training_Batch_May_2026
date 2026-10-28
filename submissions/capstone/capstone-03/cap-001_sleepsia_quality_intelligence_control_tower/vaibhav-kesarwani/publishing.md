# Publishing

## Overview

The **Sleepsia Product Quality & Customer Experience Intelligence Control Tower** has been successfully published as a **Microsoft Copilot Studio agent**. The **Quality Supervisor** serves as the primary user-facing agent and is accessible through both **Microsoft 365 Copilot** and **Microsoft Teams**.

All specialist agents are configured as **child agents** and are invoked through hierarchical orchestration.

## Deployment architecture

```text
Users
   |
   v
Quality Supervisor
   |
   +-- Incident Intake & Validation Specialist
   +-- Complaint Pattern Specialist
   +-- Returns Specialist
   +-- Product/Batch Specialist
   +-- Customer Impact Specialist
   +-- Safety Specialist
   +-- Quality Investigation Decision Specialist
   +-- CAPA Planning & Ownership Specialist
   +-- Evidence Update & Selective Reassessment Specialist
   +-- M365 Guidance Specialist
```

## Published channels

The agent has been deployed to:

* **Microsoft 365 Copilot**
* **Microsoft Teams**

Authorized users can interact directly with the Quality Supervisor, which automatically invokes the appropriate child agents during investigations.

## Enabled capabilities

The published solution supports:

* autonomous complaint validation,
* parallel specialist analysis,
* quality classification,
* CAPA planning,
* investigation report generation,
* Excel record updates,
* Outlook notifications,
* selective reassessment,
* Microsoft Learn MCP guidance.

## Microsoft 365 integration

The deployment is integrated with:

* Excel Online (Business)
* Word Online (Business)
* Office 365 Outlook
* OneDrive for Business
* Microsoft Learn MCP

## Production readiness

The published agent is designed for enterprise use with:

* hierarchical child-agent orchestration,
* centralized supervisor control,
* deterministic quality rules,
* auditable decision logging,
* Microsoft 365 native integration,
* controlled operational updates.

This deployment represents a **production-ready Microsoft Copilot Studio implementation** of the Sleepsia Product Quality & Customer Experience Intelligence Control Tower.
