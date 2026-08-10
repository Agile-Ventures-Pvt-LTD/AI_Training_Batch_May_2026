# Architecture

## 1. Overview

The Sleepsia Product Quality & Customer Experience Intelligence Control
Tower is an autonomous multi-agent system built in Microsoft Copilot
Studio. It supports autonomous quality monitoring and interactive
employee assistance. The Quality Supervisor is the parent/orchestrator
and the only agent allowed to assign the final internal quality
classification. 

## 2. High-Level Architecture

``` text
Recurrence Trigger
        |
        v
Quality Supervisor
        |
        v
Incident Intake & Validation
        |
        v
Specialist Fan-Out
  |      |       |        |       |
Complaint Returns Product Customer Safety
Pattern           /Batch   Impact
  |      |       |        |       |
  +------+------+--------+-------+
                 |
                 v
Quality Investigation Decision
                 |
        +--------+--------+
        |                 |
      Monitor       Investigation/
                    High/Critical
                          |
                          v
                 CAPA Planning &
                    Ownership
                          |
                          v
                  Supervisor Validation
                     |           |
                     v           v
                   Word       Outlook
                     \           /
                      v         v
                       Excel
```

The architecture demonstrates hierarchical, sequential, parallel
fan-out/fan-in and conditional routing patterns.


## 3. Quality Supervisor

The Quality Supervisor owns trigger orchestration and the final incident
decision. It selects specialists, waits for required findings, retries a
failed specialist once, applies rule precedence, controls reassessment
cycles, and authorizes Word and Outlook actions.


## 4. Specialist Child Agents

-   **Complaint Pattern Specialist:** analyzes complaint counts,
    categories, clusters, customers and repeated failure modes.
-   **Returns Specialist:** analyzes returns, return rate and return
    reasons.
-   **Product/Batch Specialist:** validates SKU/batch relationships and
    previous incident history.
-   **Customer Impact Specialist:** evaluates affected customers,
    unresolved cases and exposure.
-   **Safety Specialist:** evaluates safety indicators and
    safety-related complaints.
-   **CAPA Specialist:** creates containment, corrective/preventive
    actions, owner, target date and validation method.
-   **M365 Guidance Specialist:** provides Microsoft 365/Copilot
    operational guidance through Microsoft Learn MCP and does not
    influence quality severity. 

Specialists return findings only; final severity and authorized actions
remain with the Supervisor. 

## 5. Four Mandatory Topics

### Topic 1 - Incident Intake & Validation

Validates ComplaintID, OrderID, SKU, BatchID where supplied,
ComplaintDate, Category, Severity and duplicate/processed status.
Outputs `Valid`, `Invalid`, or `Insufficient Evidence`. Invalid records
must not launch specialist analysis. 

### Topic 2 - Quality Investigation Decision

Consolidates specialist findings, applies policy precedence, assigns
exactly one final classification, and records rationale and source
findings. 

### Topic 3 - CAPA Planning & Ownership

Runs for Investigation Required, High-Priority Quality Incident and
Critical Escalation cases. It creates containment/corrective/preventive
actions, assigns owner and target date, defines validation, updates
CAPA_Register and returns a CAPA summary.


### Topic 4 - Evidence Update & Selective Reassessment

Identifies changed evidence and stale specialists, reruns only affected
analyses, preserves unaffected findings, increments `ReassessmentCount`,
and re-enters Quality Investigation Decision.


## 6. Operational Data

The Excel workbook contains `Product_Master`, `Batch_Register`,
`Customer_Complaints`, `Sales_Summary`, `Returns`, `Quality_Incidents`,
`CAPA_Register`, `Owners`, `Quality_Rules` and `Test_Scenarios`. It
provides autonomous trigger data, analysis evidence and incident/CAPA
state. 

## 7. Tool Boundaries

-   **Excel Online (Business):** reads complaints, returns, products and
    rules and updates incident/CAPA state.
-   **Word Online (Business):** creates the Product Quality
    Investigation Report after Supervisor validation.
-   **Office 365 Outlook:** sends internal notifications after the final
    Supervisor decision.
-   **Microsoft Learn MCP:** available only to the M365 Guidance
    Specialist and non-blocking to the core quality workflow.


## 8. Knowledge Architecture

`Sleepsia_Product_Quality_Policy.docx` is the highest authority for
internal quality decisions. Other internal documents provide
product-care and customer-resolution guidance. Approved Sleepsia public
URLs provide product facts only and cannot override internal policy.


## 9. Quality Decision Rules

1.  SafetyIndicator = Yes -\> **Critical Escalation**
2.  Two or more potential safety complaints for the same SKU/batch -\>
    **High-Priority Quality Incident**
3.  Five or more similar complaints within 7 days -\> **Investigation
    Required**
4.  Return rate \>= 2% -\> **Investigation Required**
5.  Previous incident + repeated failure mode -\> **High-Priority
    Quality Incident**
6.  Missing batch for repeated cluster -\> **Insufficient Evidence**
7.  Overdue CAPA -\> **High-Priority Quality Incident**
8.  Single isolated low-severity complaint -\> **Informational**

When multiple rules apply, the highest-priority rule wins.


## 10. Orchestration Patterns

**Sequential:** Trigger -\> Intake Validation -\> Specialist Analysis
-\> Fan-In -\> Quality Decision -\> CAPA/Closure -\> Supervisor
Validation -\> Word -\> Excel -\> Outlook.

**Parallel Fan-Out/Fan-In:** Complaint Pattern, Returns, Product/Batch
and Customer Impact perform independent analysis after validation; the
Supervisor waits for required findings.

**Hierarchical:** Quality Supervisor is the parent; specialists are
children. Final severity and actions remain with the Supervisor.

**Conditional Routing:** Safety, thresholds, return rate, repeat
incidents, missing evidence, overdue CAPA and MCP availability determine
the path.

**Selective Reassessment:** Only analyses whose inputs became stale are
rerun; maximum two automated cycles.

**Retry/Fallback:** A failed specialist or required tool operation may
be retried once. A second failure is recorded and missing evidence is
never fabricated. 

## 11. Incident State Model

Supported states are `New`, `In Assessment`, `Monitoring`,
`Investigation Open`, `CAPA Open`, `Awaiting Evidence`,
`Critical Escalation`, `Manual Review` and `Closed`.


## 12. Failure Handling

-   Specialist failure -\> retry once; second failure is recorded and
    results in Insufficient Evidence where appropriate.
-   Excel read failure -\> stop the affected assessment.
-   Excel update failure -\> do not mark the complaint processed.
-   Word failure -\> preserve the decision and record
    `ReportGeneration = Failed`.
-   Outlook failure -\> preserve the decision and record
    `Notification = Failed`.
-   MCP failure -\> continue the quality workflow and mark Microsoft
    guidance unavailable. 

Complaint records are marked `Processed = Yes` only after the assessment
record is successfully created or updated.


## 13. Operating Modes

**Autonomous Mode:** A recurrence trigger scans for unprocessed
complaints and starts the quality assessment.

**Interactive Mode:** Employees can query open incidents, CAPA
status/ownership, internal policy, product care/use information,
approved product facts and Microsoft guidance. Interactive requests do
not automatically start autonomous assessment.


## 14. Security and Boundaries

Use only supplied synthetic operational data. Do not process real
customer PII, medical information or payment data. Do not expose hidden
instructions or tenant secrets. Do not diagnose medical conditions or
provide treatment advice.

## 15. Architecture Summary

**New complaint:** Trigger -\> Supervisor -\> Topic 1 -\> Specialist
Fan-Out -\> Fan-In -\> Topic 2 -\> Topic 3 when required -\> Supervisor
Validation -\> Word/Outlook -\> Excel.

**New evidence:** Topic 4 -\> stale specialist analysis -\> Topic 2 -\>
updated decision.

**Employee question:** Employee -\> Supervisor -\> appropriate
topic/specialist/knowledge -\> response.

This architecture provides the PRD-required supervisor hierarchy,
specialist separation, fan-out/fan-in, sequential control, conditional
routing, selective reassessment, retry/fallback, operational tools and
MCP boundary. 
