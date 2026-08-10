# Orchestration Patterns

## 1. Purpose

The CAP-001 solution uses multiple orchestration patterns to coordinate
the Quality Supervisor, specialist child agents, custom topics, tools,
reassessment, and failure handling.

The PRD requires demonstration of:

-   Sequential orchestration
-   Parallel fan-out/fan-in
-   Hierarchical orchestration
-   Conditional routing
-   Selective reassessment
-   Retry/fallback

Generative orchestration must be enabled.
fileciteturn14file1L112-L130

## 2. Overall Orchestration Architecture

``` text
Recurrence Trigger
        |
        v
Quality Supervisor
        |
        v
Topic 1: Incident Intake & Validation
        |
        v
Validated SKU / Batch Cluster
        |
        +-------------------+-------------------+-------------------+
        |                   |                   |                   |
        v                   v                   v                   v
 Complaint Pattern      Returns          Product/Batch       Customer Impact
 Specialist             Specialist        Specialist          Specialist
        |                   |                   |                   |
        +-------------------+-------------------+-------------------+
                            |
                            v
                     Safety Specialist
                            |
                            v
                       Supervisor
                         Fan-In
                            |
                            v
             Topic 2: Quality Investigation
                            |
                 +----------+----------+
                 |                     |
                 v                     v
          Monitoring /              Investigation /
          closure path              High / Critical
                                         |
                                         v
                              Topic 3: CAPA Planning
                                         |
                                         v
                                Supervisor Validation
                                   /                                              v              v
                              Word Report     Outlook
                                  \              /
                                   +------v------+
                                          |
                                          v
                                   Excel Update

New Evidence
     |
     v
Topic 4: Evidence Update & Selective Reassessment
     |
     v
Rerun only stale specialists
     |
     v
Quality Investigation Decision
```

This architecture follows the PRD's mandatory Supervisor hierarchy,
specialist fan-out/fan-in, decision topic, CAPA path, validation,
reporting, notification, and Excel update flow.
fileciteturn14file0L28-L65

## 3. Hierarchical Orchestration

### Pattern

The **Quality Supervisor is the parent/orchestrator** and all domain
specialists are child agents.

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

The Supervisor:

-   Selects required specialists.
-   Controls execution.
-   Waits for required findings.
-   Consolidates findings.
-   Applies quality policy.
-   Assigns the final classification.
-   Authorizes final report and notification actions.

Specialists provide findings only and do not own the final incident
decision. fileciteturn14file0L75-L77

### Important Boundary

The M365 Guidance Specialist is a child agent but is **not part of the
product-quality severity decision**. It is used for Microsoft
operational guidance. fileciteturn14file7L654-L664

## 4. Sequential Orchestration

The core autonomous workflow follows a controlled sequence:

``` text
Trigger
  ↓
Incident Intake & Validation
  ↓
Specialist Analysis
  ↓
Fan-In
  ↓
Quality Decision
  ↓
CAPA / Closure Path
  ↓
Supervisor Validation
  ↓
Word Report
  ↓
Excel Update
  ↓
Outlook Notification
```

The PRD explicitly defines this mandatory sequence.
fileciteturn14file0L66-L70

### Why Sequential Control Is Used

Certain actions must not occur before earlier stages are complete.

Examples:

-   Specialists must not run before validation.
-   Final classification must not occur before required specialist
    findings are collected.
-   CAPA must not run before an eligible quality classification exists.
-   Word generation must occur after Supervisor validation.
-   Outlook notification must occur after the final Supervisor decision.
-   Complaint records must not be marked processed before the assessment
    record is successfully created or updated.

The trigger specifically validates records before specialist invocation
and marks consumed records only after successful assessment state
creation/update. fileciteturn14file5L470-L477

## 5. Parallel Fan-Out / Fan-In

After successful validation, independent specialist analyses are
performed as a logical parallel group.

### Fan-Out

``` text
                  Supervisor
                      |
          +-----------+-----------+-----------+
          |           |           |           |
          v           v           v           v
     Complaint     Returns    Product/Batch  Customer
      Pattern                              Impact
```

The required independent analyses are:

-   Complaint Pattern
-   Returns
-   Product/Batch
-   Customer Impact

The Safety Specialist may also be invoked when safety evidence is
relevant.

### Fan-In

``` text
Complaint Pattern --+
Returns ------------+
Product/Batch ------+--> Supervisor --> Quality Decision
Customer Impact ----+
Safety -------------+
```

The Supervisor must wait for all required findings before final
consolidation.

The PRD requires logical fan-out/fan-in; literal simultaneous
infrastructure execution is not required. fileciteturn14file0L71-L74

### Specialist Boundaries

Complaint Pattern:

-   Complaint counts.
-   Categories.
-   Failure modes.
-   Cluster evidence.
-   No final severity.

Returns:

-   Return count.
-   Return rate.
-   Return reasons.
-   No final severity.

Product/Batch:

-   SKU/batch relationship.
-   Supplier/manufacturing information.
-   Previous incidents.
-   Missing-data status.

Customer Impact:

-   Customers affected.
-   Unresolved cases.
-   Exposure.
-   No final severity.

These boundaries prevent duplicate ownership.
fileciteturn14file7L614-L638

## 6. Conditional Routing

After specialist findings are consolidated, the Quality Supervisor
applies explicit policy precedence.

### Routing Logic

``` text
SafetyIndicator = Yes
        |
        v
Critical Escalation

Otherwise:
        |
        v
Two or more potential safety complaints
        |
        v
High-Priority Quality Incident

Otherwise:
        |
        v
Five or more similar complaints in 7 days
        |
        v
Investigation Required

Otherwise:
        |
        v
Return rate >= 2%
        |
        v
Investigation Required

Otherwise:
        |
        v
Previous incident + repeated failure
        |
        v
High-Priority Quality Incident

Otherwise:
        |
        v
Missing batch for repeated cluster
        |
        v
Insufficient Evidence

Otherwise:
        |
        v
Overdue CAPA
        |
        v
High-Priority Quality Incident

Otherwise:
        |
        v
Single isolated low-severity complaint
        |
        v
Informational
```

The PRD explicitly requires this priority ordering, with the
highest-priority rule winning when multiple rules apply.
fileciteturn14file0L78-L85

### Conditional Routing Principles

-   Safety takes precedence.
-   Threshold breaches route to investigation.
-   Repeated incidents can route to high priority.
-   Missing evidence prevents unsupported decisions.
-   Overdue CAPA triggers escalation.
-   MCP availability does not affect the core quality route.

## 7. CAPA Conditional Branch

CAPA is not executed for every complaint.

The CAPA Specialist runs after:

-   Investigation Required
-   High-Priority Quality Incident
-   Critical Escalation

The specialist prepares:

-   Containment action.
-   Corrective/preventive recommendations.
-   Owner role.
-   Target date.
-   Validation method.

It must not claim a root cause without explicit evidence and cannot
independently close a Critical incident.
fileciteturn14file7L647-L653

``` text
Final Classification
        |
        +--> Informational / Monitoring
        |          |
        |          v
        |       Observe / Close
        |
        +--> Investigation Required
        |
        +--> High-Priority Quality Incident
        |
        +--> Critical Escalation
                   |
                   v
              CAPA Planning
```

## 8. Selective Reassessment Loop

When new evidence arrives, the system must not rerun every specialist
automatically.

### Flow

``` text
New Evidence
     |
     v
Identify Changed Evidence
     |
     v
Determine Stale Findings
     |
     +---- Unaffected findings ----> Preserve
     |
     +---- Stale findings ---------> Rerun
                                      |
                                      v
                              Fan-In / Consolidation
                                      |
                                      v
                              Quality Decision
```

The PRD requires only analyses whose inputs became stale to be rerun,
while unaffected findings are preserved. Maximum automated reassessment
cycles per incident are **2**. After the second unresolved cycle, the
incident moves to **Manual Review**. fileciteturn14file5L455-L457

### Example

If new batch information arrives:

-   Product/Batch analysis may become stale.
-   Complaint Pattern may remain valid.
-   Returns may remain valid.
-   Customer Impact may remain valid.

Therefore, rerun Product/Batch rather than unnecessarily rerunning every
specialist.

## 9. Retry and Fallback

The system uses controlled retry behavior.

``` text
Specialist / Required Tool
          |
       Failure
          |
          v
       Retry Once
          |
     +----+----+
     |         |
 Success     Failure
     |         |
     v         v
 Continue   Record Failure
               |
               v
       Insufficient Evidence
       / Manual Review where
          appropriate
```

A failed specialist or required tool operation may be retried once.

After the second failure:

-   Record the failure explicitly.
-   Do not fabricate the missing result.
-   Do not claim the action succeeded.
-   Use the appropriate evidence-gap/manual-review behavior.

The PRD explicitly requires retry once and no fabrication.
fileciteturn14file5L458-L460

## 10. Tool Failure Orchestration

### Excel Read Failure

``` text
Excel Read
   |
 Failure
   |
   v
Stop Affected Assessment
   |
   v
Record Failure
```

### Excel Update Failure

``` text
Excel Update
   |
 Failure
   |
   v
Do NOT mark Processed = Yes
```

### Word Failure

``` text
Supervisor Validation
       |
       v
Word Generation
       |
    Failure
       |
       v
Preserve Decision
ReportGeneration = Failed
```

### Outlook Failure

``` text
Final Decision
       |
       v
Outlook Notification
       |
    Failure
       |
       v
Preserve Decision
Notification = Failed
```

The PRD explicitly defines these failure behaviors.
fileciteturn14file5L458-L460

## 11. MCP Orchestration

Microsoft Learn MCP is isolated to the M365 Guidance Specialist.

``` text
Employee Microsoft Question
          |
          v
M365 Guidance Specialist
          |
          v
Microsoft Learn MCP
          |
          v
Microsoft Guidance
```

MCP does **not** participate in:

-   Complaint analysis.
-   Return-rate decisions.
-   Safety classification.
-   Quality severity.
-   CAPA decisions.

If MCP is unavailable:

``` text
MCP Failure
    |
    +--> Core quality workflow continues
    |
    +--> Microsoft guidance request:
         "Microsoft guidance unavailable - manual review"
```

The PRD explicitly defines MCP as non-blocking and prohibits it from
influencing Sleepsia quality severity. fileciteturn14file7L654-L673

## 12. Autonomous Orchestration

The autonomous workflow begins with a recurrence event trigger.

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
Select one logical SKU/batch cluster
       |
       v
Validate
       |
       +--> Invalid
       |      |
       |      v
       |   Stop; no specialists
       |
       +--> Valid
              |
              v
       Specialist Fan-Out
              |
              v
       Specialist Fan-In
              |
              v
       Quality Decision
              |
              v
       CAPA if required
              |
              v
       Supervisor Validation
              |
              v
       Report / Notification / Excel
```

The PRD specifies that one logical SKU/batch cluster is processed per
trigger execution and invalid records must not launch specialist
analysis. fileciteturn14file5L470-L477

## 13. Interactive Orchestration

Interactive employee questions use a different entry path.

``` text
Employee
   |
   v
Published Agent
   |
   v
Quality Supervisor
   |
   +--> Open Incident Query
   +--> CAPA Query
   +--> Policy Query
   +--> Product Care Query
   +--> Public Product Query
   +--> Microsoft Guidance Query
```

Interactive mode should not automatically start an autonomous quality
assessment unless appropriate.

The PRD defines Teams/Microsoft 365 Copilot as the interactive entry
point. fileciteturn14file5L461-L469

## 14. Complete End-to-End Pattern

``` text
                         AUTONOMOUS TRIGGER
                                |
                                v
                       QUALITY SUPERVISOR
                                |
                                v
                   INCIDENT INTAKE & VALIDATION
                                |
                    +-----------+-----------+
                    |                       |
                 Invalid                   Valid
                    |                       |
                    v                       v
                  Stop               SPECIALIST FAN-OUT
                                            |
                  +-------------------------+-------------------------+
                  |              |              |                    |
                  v              v              v                    v
             Complaint        Returns      Product/Batch       Customer Impact
             Pattern          Specialist     Specialist          Specialist
                  |              |              |                    |
                  +--------------+--------------+--------------------+
                                            |
                                      Safety if relevant
                                            |
                                            v
                                      SPECIALIST FAN-IN
                                            |
                                            v
                              QUALITY INVESTIGATION DECISION
                                            |
                      +---------------------+----------------------+
                      |                     |                      |
                 Monitoring          Investigation /          Critical /
                                      High Priority             Escalation
                                            |                      |
                                            +----------+-----------+
                                                       |
                                                       v
                                                CAPA SPECIALIST
                                                       |
                                                       v
                                             SUPERVISOR VALIDATION
                                                       |
                                          +------------+------------+
                                          |                         |
                                          v                         v
                                    WORD REPORT                OUTLOOK
                                          \                         /
                                           \                       /
                                            +--------+-------------+
                                                     |
                                                     v
                                                   EXCEL
                                                     |
                                                     v
                                            Processed = Yes
```

## 15. Pattern-to-Component Mapping

  -----------------------------------------------------------------------
  Orchestration Pattern   CAP-001 Component       Purpose
  ----------------------- ----------------------- -----------------------
  Sequential              Supervisor + 4 topics + Enforce correct
                          tools                   workflow order

  Hierarchical            Quality Supervisor +    Centralize ownership
                          child agents            and final decision

  Parallel Fan-Out        Complaint, Returns,     Independent specialist
                          Product/Batch, Customer analysis
                          Impact, Safety where    
                          required                

  Fan-In                  Quality Supervisor      Consolidate findings

  Conditional             Quality Investigation   Apply policy precedence
                          Decision Topic          

  Loop                    Evidence Update &       Reassess changed
                          Selective Reassessment  evidence
                          Topic                   

  Retry                   Supervisor              Retry failed
                                                  specialist/tool once

  Fallback                Supervisor + failure    Prevent false success
                          handling                and unsupported
                                                  decisions

  MCP Isolation           M365 Guidance           Provide Microsoft
                          Specialist              operational guidance
                                                  without affecting
                                                  quality severity
  -----------------------------------------------------------------------

The PRD explicitly requires these orchestration patterns as part of the
implementation and evaluation. fileciteturn14file1L120-L130

## 16. Orchestration Rules

The following rules must always be enforced:

1.  Validation happens before specialist analysis.
2.  Invalid records must not launch specialists.
3.  Specialists provide findings only.
4.  The Supervisor owns final classification.
5.  Required specialist findings must be collected before final
    consolidation.
6.  The Supervisor applies quality-policy precedence.
7.  CAPA runs only for eligible classifications.
8.  Word and Outlook actions require Supervisor
    validation/authorization.
9.  Failed tools must not produce false-success messages.
10. Missing evidence must never be fabricated.
11. New evidence triggers selective, not unnecessary full reassessment.
12. Maximum automated reassessment cycles are 2.
13. MCP failure must not stop quality assessment.
14. M365 Guidance Specialist must not influence Sleepsia quality
    severity.
15. Complaints are marked processed only after the assessment state is
    successfully created or updated.

## 17. Implementation Checklist

[ ] Generative orchestration enabled
[ ] Quality Supervisor configured as parent
[ ] Six quality specialists configured
[ ] M365 Guidance Specialist configured separately
[ ] Recurrence trigger configured
[ ] Topic 1 validation completed
[ ] Specialist fan-out implemented
[ ] Supervisor fan-in implemented
[ ] Topic 2 quality decision implemented
[ ] Conditional quality routing implemented
[ ] Topic 3 CAPA flow implemented
[ ] Supervisor validation implemented
[ ] Word report flow implemented
[ ] Outlook notification flow implemented
[ ] Excel state update implemented
[ ] Topic 4 selective reassessment implemented
[ ] Retry-once behavior implemented
[ ] Failure/fallback behavior implemented
[ ] MCP isolated from quality decisions
[ ] Autonomous mode tested
[ ] Interactive mode tested


## 18. Final Design Principle

The orchestration model is intentionally **Supervisor-controlled**:

> **Specialists analyze. The Supervisor consolidates, applies policy,
> decides, and authorizes final actions.**

The architecture therefore demonstrates hierarchical, sequential,
parallel fan-out/fan-in, conditional, reassessment, and retry/fallback
orchestration without allowing child agents or Microsoft guidance to
take ownership of the final Sleepsia quality decision.
