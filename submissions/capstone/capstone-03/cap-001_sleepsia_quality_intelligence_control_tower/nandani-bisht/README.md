# CAP-001 — Sleepsia Product Quality & Customer Experience Intelligence Control Tower

## Project Overview

CAP-001 is an autonomous Product Quality and Customer Experience Intelligence Control Tower built using Microsoft Copilot Studio.

The agent monitors new customer complaint and quality signals, validates incoming records, coordinates specialist analysis, consolidates findings, applies deterministic quality-decision rules, plans Corrective and Preventive Actions (CAPA), supports selective reassessment when evidence changes, and updates operational records.

The system is designed for **training use with synthetic operational data**.

---

## Project Information

| Field | Details |
|---|---|
| Project ID | CAP-001 |
| Project Name | Sleepsia Product Quality & Customer Experience Intelligence Control Tower |
| Agent Name | `Sleepsia Quality Supervisor` |
| Participant Name | `[Nandani Bisht]` |
| Published Agent URL | `https://copilotstudio.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/76dac50e-8194-f111-b8dc-000d3af21e08/overview` |
| Submission Date | `[10-08-2026]` |
| Agent Platform | Microsoft Copilot Studio |
| Operating Mode | Autonomous + Interactive |
| Primary Orchestrator | Quality Supervisor |
| Autonomous Trigger | Recurrence Event Trigger |

---

## Business Objective

The objective is to create an autonomous quality-intelligence workflow that can:

1. Detect new complaint and quality records.
2. Validate complaint data before specialist analysis.
3. Identify product and batch information.
4. Perform independent specialist analyses.
5. Consolidate specialist findings.
6. Apply explicit quality decision rules.
7. Create and manage CAPA actions.
8. Reassess incidents when new evidence is received.
9. Preserve unaffected findings during reassessment.
10. Escalate unresolved cases to Manual Review.
11. Generate quality reports.
12. Send internal notifications after Supervisor validation.
13. Support interactive employee questions without unnecessarily starting autonomous assessments.

---

# Architecture

The mandatory high-level architecture is:

```text
Recurrence Trigger
        |
        v
Quality Supervisor
        |
        v
Incident Intake & Validation
        |
        v
Product / Batch Identified
        |
        +-------------------------------+
        |               |               |
        v               v               v
Complaint          Returns          Product/Batch
Pattern            Specialist       Specialist
Specialist
        |               |               |
        +---------------+---------------+
                        |
                        v
                 Customer Impact
                   Specialist
                        |
                        v
                  Safety Specialist
                        |
                        v
                 Supervisor Fan-In
                        |
                        v
             Quality Investigation
                   Decision
                        |
             +----------+----------+
             |          |          |
             v          v          v
          Monitor  Investigation  Critical
                                  Escalation
                        |
                        v
                CAPA / Closure Path
                        |
                        v
               Supervisor Validation
                    /          \
                   v            v
                Word         Outlook
                Report      Notification
                   \            /
                    \          /
                       v      v
                         Excel