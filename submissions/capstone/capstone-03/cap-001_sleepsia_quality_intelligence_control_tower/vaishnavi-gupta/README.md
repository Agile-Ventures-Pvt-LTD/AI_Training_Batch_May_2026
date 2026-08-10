# Sleepsia Product Quality & Customer Experience Intelligence Control Tower

## 1. Project Overview

The **Sleepsia Product Quality & Customer Experience Intelligence
Control Tower (CAP-001)** is an autonomous multi-agent solution built
using **Microsoft Copilot Studio**. Its purpose is to identify emerging
product-quality signals, coordinate specialist analysis, apply approved
quality rules, manage investigations and CAPA actions, maintain
operational records, generate internal reports, and support employees
with approved quality information.

The solution supports two operating modes:

-   **Autonomous Mode:** A recurrence trigger identifies unprocessed
    complaints and starts the quality assessment workflow.
-   **Interactive Mode:** Employees can ask questions about incidents,
    CAPA, product care, internal quality policy, approved product facts,
    and Microsoft 365/Copilot usage.

The system demonstrates the required Copilot Studio capabilities:
instructions, knowledge, custom topics, autonomous triggers, child
agents, tools, MCP, orchestration patterns, testing, and Teams/Microsoft
365 publishing. 

## 2. Business Objective

The control tower is designed to help Sleepsia quality teams:

-   Detect complaint clusters and emerging quality signals.
-   Analyze returns and return-rate signals.
-   Correlate complaints with products and batches.
-   Identify customer impact.
-   Detect safety indicators.
-   Determine whether a quality investigation is required.
-   Create and track CAPA actions.
-   Generate internal quality investigation reports.
-   Send authorized internal notifications.
-   Reassess an existing incident when new evidence becomes available.
-   Provide employees with controlled quality and product information.

The system is an internal quality-control solution. It does not replace
approved business decisions such as recalls, customer compensation, or
public safety communications.

## 3. Key Architecture

The solution uses a **hierarchical multi-agent architecture**.

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
   |       |        |        |       |
Complaint Returns Product  Customer Safety
Pattern           /Batch    Impact
   |       |        |        |       |
   +-------+--------+--------+-------+
                    |
                    v
          Quality Investigation Decision
                    |
          +---------+---------+
          |                   |
       Monitoring       Investigation /
                        High / Critical
                              |
                              v
                    CAPA Planning & Ownership
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

The architecture implements hierarchical, sequential, parallel
fan-out/fan-in, conditional routing, selective reassessment, and
retry/fallback patterns.

## 4. Parent Agent

### Quality Supervisor

The **Quality Supervisor** is the parent/orchestrator and the sole owner
of the final internal quality classification.

Responsibilities:

-   Coordinate the autonomous workflow.
-   Select required specialist agents.
-   Wait for required specialist findings.
-   Consolidate evidence.
-   Apply approved quality decision precedence.
-   Assign exactly one final classification.
-   Control reassessment cycles.
-   Invoke CAPA when required.
-   Authorize Word report generation.
-   Authorize Outlook notification.
-   Handle specialist/tool failures.
-   Ensure complaints are not marked processed until the required
    assessment record is successfully created or updated.
-   Never invent missing evidence or claim failed actions succeeded.

The PRD explicitly requires the Quality Supervisor to remain the final
decision owner. 

## 5. Child Specialist Agents

The project uses separate specialist agents with non-overlapping
responsibilities.

### 5.1 Complaint Pattern Specialist

Uses `Customer_Complaints`.

Responsibilities:

-   Count complaints by SKU, batch, and category.
-   Identify complaint clusters.
-   Identify unique affected customers.
-   Determine first/latest complaint dates.
-   Detect repeated failure modes.
-   Return complaint count, dominant categories, cluster evidence, and
    confidence.

It does not calculate return rate or assign final severity.


### 5.2 Returns Specialist

Uses `Returns` and `Sales_Summary`.

Responsibilities:

-   Calculate return count.
-   Calculate SKU return rate.
-   Identify return reasons.
-   Identify refund exposure.
-   Return return-threshold evidence.

It does not decide customer refunds or final quality severity.


### 5.3 Product/Batch Specialist

Uses `Product_Master`, `Batch_Register`, and `Quality_Incidents`.

Responsibilities:

-   Confirm SKU/batch relationships.
-   Identify manufacture date and supplier lot.
-   Identify quality-hold information.
-   Review previous incident count/history.
-   Detect repeated incident history.
-   Identify missing product/batch evidence.


### 5.4 Customer Impact Specialist

Uses `Customer_Complaints` and `Returns`.

Responsibilities:

-   Calculate affected customers.
-   Identify unresolved cases.
-   Identify repeated customer impact.
-   Evaluate exposure.
-   Separate fulfilment errors from systemic product-quality evidence.

It does not determine internal severity.

### 5.5 Safety Specialist

Reviews complaint descriptions and safety indicators.

Responsibilities:

-   Evaluate `SafetyIndicator`.
-   Identify potential safety complaint patterns.
-   Trigger the safety path when required.
-   Stop routine troubleshooting for confirmed safety concerns.
-   Never provide medical advice.

A confirmed `SafetyIndicator = Yes` requires `Critical Escalation`. Two
or more potential safety complaints for the same SKU/batch require a
High-Priority Quality Incident unless a confirmed indicator overrides
the rule. 

### 5.6 CAPA Specialist

Runs after an `Investigation Required`,
`High-Priority Quality Incident`, or `Critical Escalation`
classification.

Responsibilities:

-   Create containment recommendations.
-   Create corrective/preventive recommendations.
-   Assign owner role.
-   Set target date.
-   Define validation method.
-   Write/update CAPA records.
-   Return a CAPA summary to the Supervisor.

It must not claim root cause without explicit evidence and cannot
independently close Critical incidents. fileciteturn10file8L803-L809

### 5.7 M365 Guidance Specialist

The M365 Guidance Specialist provides operational Microsoft guidance and
is separate from the product-quality decision process.

It uses the **Microsoft Learn MCP Server** for current Microsoft Copilot
Studio, Teams, Microsoft 365, and connector guidance.

It must never influence Sleepsia quality severity.

If MCP is unavailable, the response is:

`Microsoft guidance unavailable - manual review`

The core quality workflow must continue.

## 6. Mandatory Custom Topics

The project contains four mandatory custom topics.

### Topic 1 - Incident Intake & Validation

Purpose: deterministic validation before specialist analysis.

Validates:

-   ComplaintID
-   OrderID
-   SKU
-   BatchID where supplied
-   Batch/SKU mapping
-   ComplaintDate
-   Category
-   Severity
-   Duplicate/processed status

Outputs:

-   `Valid`
-   `Invalid`
-   `Insufficient Evidence`

Invalid complaints must not launch specialist analysis.

### Topic 2 - Quality Investigation Decision

Purpose: consolidate specialist findings and apply explicit
quality-policy precedence.

It:

-   Applies the safety override.
-   Evaluates complaint-cluster threshold.
-   Evaluates return-rate threshold.
-   Evaluates previous incident history.
-   Evaluates missing evidence.
-   Evaluates overdue CAPA.
-   Assigns exactly one classification.
-   Records rationale and source findings.


### Topic 3 - CAPA Planning & Ownership

It:

-   Receives incident ID and classification.
-   Creates containment actions.
-   Creates corrective/preventive recommendations.
-   Assigns `OwnerRole`.
-   Sets target date.
-   Defines validation method.
-   Writes/updates `CAPA_Register`.
-   Returns a CAPA summary.


### Topic 4 - Evidence Update & Selective Reassessment

It:

-   Identifies changed evidence.
-   Determines stale specialist findings.
-   Reruns only stale analyses.
-   Preserves unaffected findings.
-   Increments `ReassessmentCount`.
-   Re-enters Quality Investigation Decision.
-   Assigns Manual Review after the second unresolved automated cycle.


## 7. Autonomous Workflow

The autonomous workflow follows this sequence:

``` text
Recurrence Trigger
    |
    v
Read Customer_Complaints
    |
    v
Find Processed = No
    |
    v
Select logical SKU/batch cluster
    |
    v
Incident Intake & Validation
    |
    +---- Invalid ----> Stop
    |
    +---- Insufficient Evidence ----> Evidence handling
    |
    +---- Valid
             |
             v
      Specialist Fan-Out
             |
             v
       Specialist Fan-In
             |
             v
   Quality Investigation Decision
             |
             v
        Final Classification
             |
             v
     CAPA when required
             |
             v
     Supervisor Validation
             |
       +-----+------+
       |            |
       v            v
      Word       Outlook
       \            /
        +----------+
             |
             v
       Excel Update
             |
             v
      Processed = Yes
```

The trigger exits without creating an incident if no unprocessed
complaints exist. A complaint is marked `Processed = Yes` only after the
assessment record has been successfully created or updated.

## 8. Interactive Workflow

Interactive requests do not automatically start an autonomous quality
assessment unless appropriate.

Employees can ask about:

-   Open quality incidents.
-   Incidents by SKU/batch.
-   CAPA status and ownership.
-   Internal quality policy.
-   Product care/use information.
-   Approved public product facts.
-   Microsoft 365/Copilot usage guidance.

The same published agent supports these employee interactions.


## 9. Quality Decision Rules

The system evaluates quality rules in this order:

  -------------------------------------------------------------------------
  Priority                Condition                 Classification
  ----------------------- ------------------------- -----------------------
  1                       Any                       Critical Escalation
                          `SafetyIndicator = Yes`   

  2                       Two or more potential     High-Priority Quality
                          safety complaints for     Incident
                          same SKU/batch            

  3                       Five or more similar      Investigation Required
                          complaints for same       
                          SKU/batch within 7 days   

  4                       Return rate \>= 2% for    Investigation Required
                          SKU                       

  5                       Previous incident +       High-Priority Quality
                          repeated failure mode     Incident

  6                       Missing batch for         Insufficient Evidence
                          repeated cluster          

  7                       Overdue CAPA              High-Priority Quality
                                                    Incident

  8                       Single isolated           Informational
                          low-severity complaint    
  -------------------------------------------------------------------------

When multiple rules apply, the highest-priority rule wins. The
Supervisor must not average classifications.


## 10. Allowed Final Classifications

The system can assign exactly one of:

-   `Informational`
-   `Monitoring`
-   `Investigation Required`
-   `High-Priority Quality Incident`
-   `Critical Escalation`
-   `Insufficient Evidence`
-   `Manual Review`

Specialist agents do not assign the final classification.

## 11. Operational Data

The PRD specifies one compact Excel workbook containing:

  Sheet                   Purpose
  ----------------------- ---------------------------------------------
  `Product_Master`        Supported products and public product links
  `Batch_Register`        Batch, supplier lot, and previous incidents
  `Customer_Complaints`   Autonomous trigger/input data
  `Sales_Summary`         Return-rate denominator
  `Returns`               Return analysis
  `Quality_Incidents`     Existing incident history/state
  `CAPA_Register`         Corrective actions and due dates
  `Owners`                Owner/approver roles
  `Quality_Rules`         Explicit decision rules
  `Test_Scenarios`        Implementation testing

The workbook should be stored in OneDrive for Business or SharePoint so
Excel Online (Business) can access the tables.


## 12. Knowledge Sources

### Primary Internal Policy

`Sleepsia_Product_Quality_Policy.docx`

Authority:

-   Quality thresholds.
-   Classification.
-   Investigation rules.
-   CAPA.
-   Escalation.

This is the highest authority for internal quality decisions.

### Product Care Guide

`Sleepsia_Product_Care_and_Usage_Guide.docx`

Used for:

-   Product care.
-   Product usage.
-   Product-safety escalation boundary.

### Customer Resolution Policy

`Sleepsia_Customer_Resolution_Policy.docx`

Used for:

-   Customer-resolution boundaries.
-   Separation between customer resolution and quality ownership.

### Approved Public URLs

-   https://www.sleepsia.in/products/travel-pillow
-   https://www.sleepsia.in/products/kids-alpha-pillow

Public pages provide product facts only. They cannot override internal
quality policy. fileciteturn10file6L580-L598

## 13. Knowledge Precedence

Use the following precedence:

1.  `Sleepsia_Product_Quality_Policy.docx`
2.  Other approved internal policy documents
3.  Operational Excel data
4.  Approved Sleepsia public product URLs

Synthetic internal policy controls severity, escalation, and CAPA
decisions. Public marketing claims must never override internal quality
rules. fileciteturn10file6L596-L598

## 14. Tools

### Excel Online (Business)

Used to:

-   Read complaints.
-   Read returns.
-   Read products and batches.
-   Read quality rules.
-   Read incident/CAPA state.
-   Create/update incident records.
-   Create/update CAPA records.

Boundary: source evidence must not be silently overwritten.

### Word Online (Business)

Used to:

-   Generate the Product Quality Investigation Report.

It can be invoked only after Supervisor validation.

If generation fails, the system must not claim a report exists.

### Office 365 Outlook

Used to:

-   Send authorized internal quality notifications.

It is invoked after the final Supervisor decision.

If the send operation fails, the system must not claim an email was
sent.

### Microsoft Learn MCP

Used only by the M365 Guidance Specialist.

It provides current Microsoft guidance and is non-blocking to the
product-quality decision. fileciteturn10file2L184-L198

## 15. Orchestration Patterns

### Sequential

``` text
Trigger
-> Validation
-> Specialist Analysis
-> Fan-In
-> Quality Decision
-> CAPA/Closure Path
-> Supervisor Validation
-> Word Report
-> Excel Update
-> Outlook Notification
```

### Parallel Fan-Out/Fan-In

After validation, the independent specialists analyze the same logical
incident from their own domain.

The Supervisor waits for all required findings before final
consolidation.

### Hierarchical

``` text
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

### Conditional Routing

Examples:

-   Safety indicator -\> Critical path.
-   Complaint threshold exceeded -\> Investigation path.
-   Return rate \>= 2% -\> Investigation path.
-   Previous incident + repeated failure -\> High-Priority path.
-   Missing evidence -\> Insufficient Evidence/evidence path.
-   Overdue CAPA -\> escalation.
-   MCP unavailable -\> continue quality workflow.

### Selective Reassessment

When new evidence arrives, only specialists whose inputs became stale
are rerun.

Maximum automated reassessment cycles per incident: **2**.

After the second unresolved cycle, the incident goes to `Manual Review`.

### Retry/Fallback

A failed specialist is retried once.

If the second attempt fails:

-   Record the failure.
-   Do not fabricate the result.
-   Treat the affected assessment as `Insufficient Evidence` where
    appropriate.

fileciteturn10file9L895-L920

## 16. Incident State Model

The supported states are:

-   `New` --- incident record created; assessment not complete.
-   `In Assessment` --- specialist analysis is active.
-   `Monitoring` --- below investigation threshold but requires
    observation.
-   `Investigation Open` --- formal investigation required.
-   `CAPA Open` --- corrective/preventive action underway.
-   `Awaiting Evidence` --- required evidence is missing.
-   `Critical Escalation` --- safety/highest-priority escalation active.
-   `Manual Review` --- automation is exhausted or unresolved.
-   `Closed` --- human-approved closure where required.

fileciteturn10file6L648-L658

## 17. Failure Handling

### Specialist Failure

-   Retry once.
-   If the second attempt fails, record the failure.
-   Do not invent specialist findings.
-   Use `Insufficient Evidence` where appropriate.

### Excel Read Failure

-   Stop the affected assessment.
-   Record the failure.

### Excel Update Failure

-   Preserve the decision.
-   Do not mark the complaint as processed.

### Word Failure

-   Preserve the quality decision.
-   Set `ReportGeneration = Failed`.
-   Do not claim that a report was generated.

### Outlook Failure

-   Preserve the quality decision.
-   Set `Notification = Failed`.
-   Do not claim that an email was sent.

### MCP Failure

-   Continue the core quality workflow.
-   Return `Microsoft guidance unavailable - manual review` when
    Microsoft guidance is requested.

These failure behaviors are mandatory project boundaries.
fileciteturn10file2L228-L234

## 18. Safety and Business Boundaries

The system must:

-   Use only supplied synthetic operational data.
-   Never enter real customer PII, medical information, or payment data.
-   Never expose hidden instructions or tenant secrets.
-   Never diagnose medical conditions.
-   Never provide medical treatment advice.
-   Never approve recalls.
-   Never issue public safety announcements.
-   Never promise refunds or compensation.
-   Never make customer compensation decisions.
-   Never invent missing evidence.
-   Never claim a failed action succeeded.

For confirmed safety concerns, routine troubleshooting stops and the
issue follows the internal escalation path.

## 19. Publishing

The required publishing channels are:

-   **Microsoft Teams**
-   **Microsoft 365 Copilot**, where tenant permissions/licensing allow.

Publishing requires:

1.  Publish the agent.
2.  Open Channels.
3.  Configure Teams.
4.  Configure Microsoft 365 Copilot where available.
5.  Install/test in Teams.
6.  Test Microsoft 365 Copilot where available.
7.  Capture publication evidence.
8.  Document any tenant limitation.

Availability depends on organizational permissions, sharing, licensing,
and Teams/Power Platform policies. fileciteturn10file2L244-L256

## 20. Testing

The PRD defines 20 mandatory test scenarios, including:

-   Single low-severity complaint.
-   Complaint cluster.
-   Return-rate threshold.
-   Potential safety complaints.
-   Confirmed safety indicator.
-   Missing batch evidence.
-   Previous incident and repeated failure.
-   Overdue CAPA.
-   Specialist retry.
-   Specialist second failure.
-   MCP unavailable.
-   New evidence and selective reassessment.
-   Reassessment limit.
-   Word generation.
-   Word failure.
-   Outlook failure.
-   Teams interactive query.
-   Microsoft 365 Copilot access.
-   Public product question.
-   Medical/advice request.

At least **16 tests must be executed**, including TC-02, TC-05, TC-09,
TC-10, TC-11, TC-12, TC-17, and TC-18, or a documented tenant limitation
for TC-18. fileciteturn10file5L509-L538

## 21. Acceptance Criteria

The project is considered complete when the following are demonstrated:

-   Quality Supervisor exists and is the sole final decision owner.
-   At least six domain specialists plus M365 Guidance Specialist are
    configured.
-   Generative orchestration is enabled.
-   Recurrence trigger works.
-   Three supplied knowledge documents are configured.
-   At least one approved Sleepsia public URL is configured.
-   Four mandatory custom topics are implemented.
-   Sequential, parallel fan-out/fan-in and hierarchical patterns are
    demonstrated.
-   Conditional routing, selective reassessment, and retry/fallback
    work.
-   Excel data can be read and incident/CAPA state updated.
-   Word report generation works.
-   Outlook notification is conditional on Supervisor validation.
-   Microsoft Learn MCP is configured for the M365 Guidance Specialist.
-   MCP failure does not block quality assessment.
-   Teams publishing is validated.
-   Microsoft 365 Copilot publishing is validated where tenant
    permissions allow.
-   At least 16 test cases are documented.
-   GitHub evidence is complete.

fileciteturn10file1L104-L123

## 22. Recommended Implementation Sequence

Follow this order when rebuilding or validating the project:

1.  Upload `Sleepsia_CAP001_Quality_Capstone_Data.xlsx` to OneDrive for
    Business or SharePoint.
2.  Create the Quality Supervisor.
3.  Enable generative orchestration.
4.  Add the three supplied knowledge documents.
5.  Add approved Sleepsia public product URLs.
6.  Create the specialist child agents with non-overlapping scopes.
7.  Configure the recurrence trigger.
8.  Configure Excel tools and validate table access.
9.  Build Incident Intake & Validation.
10. Build Quality Investigation Decision.
11. Build CAPA Planning & Ownership.
12. Build Evidence Update & Selective Reassessment.
13. Configure Word report generation.
14. Configure Outlook notification.
15. Configure Microsoft Learn MCP for the M365 Guidance Specialist.
16. Test autonomous complaint processing.
17. Test interactive employee queries.
18. Test failure and retry behavior.
19. Test reassessment.
20. Publish to Teams.
21. Validate Microsoft 365 Copilot access where available.
22. Execute the required test cases.
23. Capture screenshots/evidence.
24. Complete the GitHub documentation package.

The PRD specifically identifies this implementation sequence as the
recommended build order. fileciteturn10file1L164-L173

## 23. Repository Structure

The PRD requires the project under:

``` text
submissions/project-build/ms-copilot-studio/firstname-lastname/cap-001_sleepsia_quality_intelligence_control_tower
```

Recommended documentation structure:

``` text
cap-001_sleepsia_quality_intelligence_control_tower/
|
+-- README.md
+-- architecture.md
+-- orchestration-patterns.md
+-- custom-topics.md
+-- knowledge-sources.md
+-- mcp-implementation.md
+-- tool-implementation.md
+-- publishing.md
+-- test-report.md
+-- ai-usage-declaration.md
+-- known-limitations.md
```

The PRD defines the purpose of each required documentation artifact.


## 24. Project Completion Status

Update this section before final submission.


Agent Created: [Completed]
Generative Orchestration: [Completed]
Knowledge Sources: [Completed]
Specialist Child Agents: [Completed]
Autonomous Trigger: [Completed]
Four Custom Topics: [Completed]
Excel Tools: [Completed]
Word Tool: [Completed]
Outlook Tool: [Completed]
Microsoft Learn MCP: [Completed]
Autonomous Workflow Test: [Pending]
Interactive Workflow Test: [Completed]
Teams Publishing: [Pending]
Microsoft 365 Copilot Publishing: [Pending]
Test Cases Executed: [_20_/20]
GitHub Evidence: [Completed]


## 25. Important Design Principles

1.  **Supervisor owns the final decision.**
2.  **Specialists provide evidence, not final severity.**
3.  **Topics own their defined workflow logic.**
4.  **Do not duplicate specialist responsibilities.**
5.  **Use parallel analysis where specialist domains are independent.**
6.  **Wait for required findings before final consolidation.**
7.  **Apply quality rules in explicit priority order.**
8.  **Never fabricate missing evidence.**
9.  **Never claim failed tool actions succeeded.**
10. **Do not mark complaints processed before the required assessment
    update succeeds.**
11. **Reassess only stale specialist analyses.**
12. **Limit automated reassessment to two cycles.**
13. **Keep MCP non-blocking to the core quality workflow.**
14. **Keep customer-resolution decisions separate from quality
    decisions.**
15. **Use internal policy as the highest authority for quality
    decisions.**

## 26. Summary

The Sleepsia Quality Intelligence Control Tower is a controlled,
hierarchical multi-agent architecture in which the **Quality
Supervisor** coordinates validation, specialist analysis, quality
decision-making, CAPA, reporting, notifications, and reassessment.

The solution combines:

-   Autonomous recurrence-based processing.
-   Four deterministic custom topics.
-   Seven child specialist agents.
-   Parallel specialist fan-out/fan-in.
-   Explicit quality decision precedence.
-   CAPA planning and ownership.
-   Selective reassessment.
-   Retry and failure handling.
-   Excel operational data.
-   Word investigation reporting.
-   Outlook internal notifications.
-   Microsoft Learn MCP for M365 guidance.
-   Teams and Microsoft 365 Copilot publishing.
-   Controlled interactive employee assistance.

The final implementation must preserve the separation between **evidence
collection, specialist findings, final quality classification, CAPA
execution, reporting, and notification**, ensuring that no specialist or
external product information can override the Supervisor's approved
internal quality decision process.

## Participant information
Name - Vaishnavi Gupta
Branch name - vaishnavi-gupta
