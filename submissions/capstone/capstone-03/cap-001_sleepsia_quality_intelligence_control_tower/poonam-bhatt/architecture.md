# Architecture

## 1. Purpose

The CAP-001 Sleepsia Product Quality & Customer Experience Intelligence Control Tower uses a hierarchical multi-agent architecture in Microsoft Copilot Studio.

The Quality Supervisor is the parent orchestrator and sole owner of the final internal quality classification and downstream business actions. Child agents provide domain-specific evidence and findings only. :contentReference[oaicite:0]{index=0}

## 2. High-Level Architecture

```text
                    Recurrence Trigger
                           |
                           v
                 +---------------------+
                 | Quality Supervisor  |
                 | Parent Orchestrator |
                 +----------+----------+
                            |
                            v
              Incident Intake & Validation
                            |
                    Valid Investigation
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
      Complaint        Returns       Product/Batch
      Specialist       Specialist      Specialist
             |              |              |
             +--------------+--------------+
                            |
             +--------------+--------------+
             |                             |
             v                             v
      Customer Impact                 Safety Specialist
       Specialist
             |                             |
             +--------------+--------------+
                            |
                            v
                    Supervisor Fan-In
                            |
                            v
              Quality Investigation Decision
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
          Monitor       Investigation    Critical
                           / High        Escalation
                            |
                            v
                     CAPA Planning
                            |
                            v
                  Supervisor Validation
                            |
                 +----------+----------+
                 |          |          |
                 v          v          v
               Word       Excel     Outlook
````

The architecture follows the PRD sequence:

`Trigger -> Validation -> Specialist Analysis -> Fan-In -> Quality Decision -> CAPA/Closure -> Supervisor Validation -> Word -> Excel -> Outlook`. 

## 3. Supervisor

### Quality Supervisor

The Quality Supervisor:

* Receives autonomous and interactive requests.
* Selects the appropriate topic.
* Validates workflow state.
* Determines which child specialists are required.
* Controls sequential and conditional execution.
* Coordinates parallel fan-out/fan-in.
* Consolidates specialist findings.
* Calls the final Quality Investigation Decision topic.
* Routes qualifying incidents to CAPA.
* Controls reassessment and retry behavior.
* Validates the final result.
* Authorizes Word, Excel and Outlook actions.

The Supervisor is the only component permitted to own the final internal quality classification. 

## 4. Child Specialist Agents

### Complaint Pattern Specialist

Owns complaint counts, clusters, categories, repeated failure modes and complaint trends.

### Returns Specialist

Owns return counts, return reasons, sales quantity and return-rate calculations.

### Product/Batch Specialist

Owns SKU, product, batch, manufacturing and previous-incident evidence.

### Customer Impact Specialist

Owns affected customers, unresolved cases and customer exposure.

### Safety Specialist

Owns safety indicators and potential safety evidence. A confirmed safety indicator routes the investigation to Critical Escalation.

### CAPA Specialist

Runs only after the Supervisor's final classification requires Investigation, High-Priority or Critical handling. It provides containment and corrective/preventive action recommendations but does not own final severity or independently close critical incidents. 

### M365 Guidance Specialist

Provides Microsoft 365, Copilot Studio, Teams and connector guidance. It is isolated from quality-severity decisions and uses Microsoft Learn MCP. MCP failure is non-blocking to the core quality workflow. 

## 5. Orchestration Patterns

### Hierarchical

```text
Quality Supervisor
    |
    +-- Complaint Pattern Specialist
    +-- Returns Specialist
    +-- Product/Batch Specialist
    +-- Customer Impact Specialist
    +-- Safety Specialist
    +-- CAPA Specialist
    +-- M365 Guidance Specialist
```

The Supervisor controls all child execution and final decisions.

### Sequential

Used where downstream processing depends on a previous result:

```text
Trigger
  -> Intake Validation
  -> Specialist Analysis
  -> Fan-In
  -> Quality Decision
  -> CAPA/Closure
  -> Supervisor Validation
  -> Word
  -> Excel
  -> Outlook
```

### Parallel Fan-Out / Fan-In

After successful intake validation, independent evidence domains are analyzed through the required specialists. The Supervisor waits for the required findings and then consolidates them before the final decision.

Literal simultaneous execution is not required; logical parallel fan-out/fan-in is the required pattern. 

### Conditional Routing

Examples:

* Safety indicator -> Critical path.
* Complaint threshold -> Investigation path.
* Return rate >= 2% -> Investigation path.
* Previous incident + repeated failure -> High-Priority path.
* Missing evidence -> Insufficient Evidence.
* Overdue CAPA -> Escalation.
* MCP unavailable -> Continue quality assessment. 

### Selective Reassessment

When new evidence arrives, only specialists whose input became stale are rerun. Unaffected findings are preserved.

Maximum automated reassessment cycles per incident: 2. After the limit, the investigation moves to Manual Review. 

### Retry / Fallback

A failed specialist or required tool operation may be retried once.

If the second attempt fails:

* Record the failure.
* Do not fabricate the missing result.
* Continue only where the workflow can safely continue.
* Mark affected analysis as unavailable/insufficient where appropriate. 

## 6. Tool Boundaries

### Excel Online (Business)

Used for operational quality data, evidence retrieval and authorized investigation/CAPA state updates.

The Supervisor controls when updates are permitted.

### Word Online (Business)

Used to generate the final quality investigation report after final classification and Supervisor validation.

### Office 365 Outlook

Used for conditional internal notification after final validation.

A successful action must never be claimed unless the configured tool confirms success.

### Microsoft Learn MCP

Connected only to the M365 Guidance Specialist.

MCP is not part of the product-quality decision path. If unavailable, the core quality assessment continues and Microsoft guidance is reported as unavailable/manual review. 

## 7. Decision Ownership

| Component                  |           Evidence | Analysis | Final Classification | Downstream Actions |
| -------------------------- | -----------------: | -------: | -------------------: | -----------------: |
| Quality Supervisor         |                Yes |      Yes |              **Yes** |            **Yes** |
| Complaint Specialist       |                Yes |      Yes |                   No |                 No |
| Returns Specialist         |                Yes |      Yes |                   No |                 No |
| Product/Batch Specialist   |                Yes |      Yes |                   No |                 No |
| Customer Impact Specialist |                Yes |      Yes |                   No |                 No |
| Safety Specialist          |                Yes |      Yes |                   No |                 No |
| CAPA Specialist            |                Yes |      Yes |                   No |                 No |
| M365 Guidance Specialist   | Microsoft guidance |      Yes |                   No |                 No |

This separation prevents child agents from independently changing severity or executing final business actions.

## 8. Core Design Principle

The system follows:

**Validate first -> analyze independently -> fan-in -> decide centrally -> conditionally remediate -> validate -> persist -> notify.**

This architecture satisfies the PRD requirements for hierarchical orchestration, sequential processing, parallel fan-out/fan-in, conditional routing, selective reassessment and retry/fallback. 

```

This is the **second GitHub submission file: `architecture.md`**.
```
