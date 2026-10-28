# Sleepsia product quality & customer experience intelligence control tower

An enterprise-grade autonomous multi-agent quality investigation system built with **Microsoft Copilot Studio**, **Excel Online (Business)**, **Word Online (Business)**, **Outlook**, and **Microsoft Learn MCP**.

The system autonomously validates customer complaints, analyzes complaint clusters, evaluates return trends, investigates manufacturing batches, measures customer impact, assesses safety risk, recommends quality classifications, creates CAPA plans, generates investigation reports, updates operational records, and manages selective reassessment.

---

## Project overview

Sleepsia receives customer complaints across multiple products and manufacturing batches. Manual quality investigations are slow, inconsistent, and difficult to scale.

This project implements a **hierarchical multi-agent orchestration system** where a **Quality Supervisor** coordinates specialized child agents that independently analyze different dimensions of quality evidence before a final enterprise-quality decision is made.

The system follows the PRD-defined workflow:

1. Complaint intake and validation
2. Parallel specialist analysis
3. Evidence consolidation
4. Quality decision recommendation
5. Supervisor final classification
6. CAPA planning
7. Report generation
8. Excel updates
9. Outlook notifications
10. Selective reassessment

---

# Architecture

## Parent agent

**Quality Supervisor**

Responsibilities:

* workflow orchestration,
* child-agent coordination,
* evidence consolidation,
* quality rule evaluation,
* final quality classification,
* CAPA authorization,
* report authorization,
* notification authorization,
* reassessment control.

The Quality Supervisor is the **only authority permitted to assign the final quality classification**.

---

## Child agents

### Incident Intake & Validation Specialist

Validates:

* ComplaintID,
* OrderID,
* SKU,
* BatchID,
* category,
* severity,
* duplicate processing,
* evidence completeness.

### Complaint Pattern Specialist

Analyzes:

* complaint clusters,
* repeated failure modes,
* complaint categories,
* time-window concentration,
* cluster confidence.

### Returns Specialist

Analyzes:

* return count,
* return rate,
* return reasons,
* refund exposure,
* threshold status.

### Product/Batch Specialist

Analyzes:

* manufacturing batches,
* supplier lots,
* previous incidents,
* quality holds,
* repeated batch patterns.

### Customer Impact Specialist

Analyzes:

* customers affected,
* unresolved cases,
* repeat customers,
* operational impact,
* exposure level.

### Safety Specialist

Evaluates:

* safety indicators,
* heat complaints,
* burning smell patterns,
* critical escalation conditions.

### Quality Investigation Decision Specialist

Applies deterministic quality rules and recommends a classification.

### CAPA Planning & Ownership Specialist

Creates:

* containment actions,
* corrective actions,
* preventive actions,
* owner assignments,
* target dates,
* validation methods.

### Evidence Update & Selective Reassessment Specialist

Controls:

* stale evidence detection,
* selective specialist reruns,
* reassessment counting,
* manual review escalation.

### M365 Guidance Specialist

Provides Microsoft operational guidance using **Microsoft Learn MCP**.

---

# Multi-agent orchestration

## Sequential flow

Trigger

↓

Incident Intake & Validation

↓

Validation Gate

↓

Parallel Specialist Execution

↓

Evidence Consolidation

↓

Quality Investigation Decision

↓

Supervisor Final Classification

↓

CAPA Planning

↓

Report Generation

↓

Excel Updates

↓

Outlook Notification

---

## Parallel fan-out / fan-in

After successful validation the supervisor launches:

* Complaint Pattern Specialist,
* Returns Specialist,
* Product/Batch Specialist,
* Customer Impact Specialist,
* Safety Specialist.

All specialists execute independently.

The supervisor waits for all required findings before making the final decision.

---

# Quality rule precedence

Rules are evaluated in this order:

1. Safety override.
2. Complaint threshold.
3. Return-rate threshold.
4. Previous incident recurrence.
5. Missing evidence.
6. Overdue CAPA.

The highest-priority applicable rule always wins.

---

# Final quality classifications

The supervisor may assign:

* Informational
* Monitoring
* Investigation Required
* High-Priority Quality Incident
* Critical Escalation
* Insufficient Evidence
* Manual Review

---

# Technology stack

* Microsoft Copilot Studio
* Excel Online (Business)
* Word Online (Business)
* Office 365 Outlook
* Microsoft Learn MCP
* OneDrive for Business

No Power Automate is required.

---

# Excel data model

The system reads:

* Product_Master
* Batch_Register
* Customer_Complaints
* Sales_Summary
* Returns
* Owners
* Quality_Rules

The system writes:

* Quality_Incidents
* CAPA_Register
* Customer_Complaints (Processed status)

---

# Autonomous trigger

The recurrence trigger retrieves the **oldest unprocessed complaint cluster**.

If no unprocessed complaints exist, the workflow exits.

Only one complaint cluster is processed per execution.

---

# Safety handling

Any complaint with:

**SafetyIndicator = Yes**

immediately triggers:

**Critical Escalation**

Safety evidence overrides all other quality rules.

---

# Reassessment

When new evidence arrives:

* identify stale specialists,
* rerun only affected specialists,
* preserve unaffected findings,
* increment ReassessmentCount,
* re-enter the decision stage.

After **two unresolved automated reassessment cycles**, the incident is assigned **Manual Review**.

---

# Outputs

The system generates:

* Product Quality Investigation Report
* Quality Incident record
* CAPA record
* Complaint processing update
* Outlook notification
* Supervisor decision rationale

---

# Microsoft Learn MCP

The M365 Guidance Specialist uses:

https://learn.microsoft.com/api/mcp

to retrieve Microsoft documentation and Copilot Studio guidance.

MCP failures do not block the quality investigation workflow.

---

# Key enterprise capabilities

* hierarchical multi-agent orchestration,
* parallel evidence collection,
* deterministic rule evaluation,
* safety-first escalation,
* structured CAPA generation,
* auditable supervisor decisions,
* selective reassessment,
* Microsoft 365 integration,
* enterprise-quality governance.
