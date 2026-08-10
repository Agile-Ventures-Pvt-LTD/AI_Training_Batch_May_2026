# MCP Implementation

## Overview

The Sleepsia Quality Intelligence Control Tower is implemented using Microsoft Copilot Studio agent orchestration. The solution follows a multi-agent architecture where the Quality Supervisor coordinates specialist agents responsible for specific investigation functions.

---

## MCP Usage

The solution uses the Model Context Protocol (MCP) pattern through structured agent-to-agent communication within Copilot Studio.

The Quality Supervisor acts as the central orchestrator and invokes specialist agents with scoped responsibilities:

- Complaint Pattern Specialist
- Returns Specialist
- Product/Batch Specialist
- Customer Impact Specialist
- CAPA Specialist
- M365 Guidance Specialist

Each specialist receives only the inputs required for its assigned investigation task and returns structured evidence to the Quality Supervisor.

---

## Context Exchange

Investigation context is passed between agents using defined input and output schemas.

Examples include:

- ComplaintID
- SKU
- BatchID
- IncidentID
- Complaint metrics
- Return metrics
- Incident history
- Customer impact findings

This structured exchange ensures evidence remains traceable throughout the investigation lifecycle.

---

## MCP Benefits

The MCP-based design provides:

- Separation of responsibilities
- Reusable specialist capabilities
- Consistent evidence collection
- Controlled decision authority
- Scalable investigation orchestration

Final decisions remain exclusively with the Quality Supervisor.

---

## Result

The MCP architecture enables coordinated quality investigations while maintaining clear responsibility boundaries, auditability, and structured evidence flow across all participating agents.