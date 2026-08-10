# orchestration-patterns.md

# CAP-001 — Orchestration Patterns

## 1. Overview

The Sleepsia Product Quality & Customer Experience Intelligence Control Tower uses multiple orchestration patterns to coordinate autonomous quality assessment.

The required patterns are:

1. Sequential orchestration
2. Parallel fan-out/fan-in
3. Hierarchical orchestration
4. Conditional routing
5. Selective reassessment loop
6. Retry and fallback

These patterns are implemented under the control of the Quality Supervisor. The Supervisor remains responsible for final incident decisions, rule precedence, reassessment, and authorization of downstream actions.

---

## 2. Sequential Orchestration

The primary quality workflow follows a mandatory sequential progression.

```text
Recurrence Trigger
        ↓
Incident Intake & Validation
        ↓
Specialist Analysis
        ↓
Supervisor Fan-In
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

Each stage depends on the successful completion of the required preceding stage.

The recurrence trigger starts the autonomous workflow. Intake validation occurs before specialist analysis. Specialist findings are consolidated before the Quality Decision. Downstream reporting and notification occur only after Supervisor validation.

---

## 3. Parallel Fan-Out / Fan-In

After successful intake validation, independent specialist assessments are performed through a logical fan-out.

```text
                         Quality Supervisor
                                │
             ┌──────────────────┼──────────────────┐
             │                  │                  │
             ▼                  ▼                  ▼
      Complaint Pattern      Returns        Product/Batch
        Specialist          Specialist       Specialist
             │                  │                  │
             └──────────────────┬──────────────────┘
                                │
                                ▼
                     Customer Impact Specialist
                                │
                                ▼
                         Supervisor Fan-In
```

The required independent specialist analyses include:

* Complaint Pattern Specialist
* Returns Specialist
* Product-Batch Specialist
* Customer Impact Specialist

The Supervisor waits for all required findings before final consolidation.

The PRD requires logical fan-out/fan-in; literal simultaneous infrastructure execution is not required.

Safety analysis is incorporated into the quality assessment path where applicable.

---

## 4. Hierarchical Orchestration

The solution follows a parent-child agent architecture.

```text
                       Quality Supervisor
                              │
        ┌─────────────┬───────┼────────┬──────────────┐
        ▼             ▼       ▼        ▼              ▼
   Complaint       Returns  Product   Customer      Safety
    Pattern       Specialist /Batch   Impact      Specialist
   Specialist                 Specialist Specialist

                              │
                              ▼
                       CAPA Specialist

                              │
                              ▼
                    M365 Guidance Specialist
```

The Quality Supervisor is the parent orchestrator.

Specialist agents are child agents with clearly separated responsibilities.

Final severity and external/internal actions remain with the Supervisor.

---

## 5. Conditional Routing

The Supervisor applies explicit governance conditions to determine the appropriate quality path.

| Condition | Routing |
|------------|----------|
| Safety indicator present | Critical path |
| Quality threshold exceeded | Investigation path |
| Return rate ≥ 2% | Investigation path |
| Repeat incident | High-Priority path |
| Required evidence missing | Evidence Request / Insufficient Evidence |
| CAPA overdue | Escalation |
| Microsoft Learn MCP unavailable | Continue core quality workflow |

These conditions are evaluated according to the required governance precedence rather than by averaging specialist outputs.

### Conditional Flow

```text
                    Specialist Findings
                           │
                           ▼
                    Quality Decision
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
          Safety?      Threshold?    Repeat?
              │            │            │
              ▼            ▼            ▼
          Critical    Investigation High-Priority
              │
              └────────────┬────────────┘
                           ▼
                    Evidence / CAPA
                           │
                           ▼
                    Final Supervisor
                       Validation
```

---

## 6. Selective Reassessment Loop

The solution does not automatically rerun every specialist whenever new evidence becomes available.

Instead, the Supervisor identifies which specialist analyses depend on the changed evidence and reruns only those analyses whose inputs became stale.

```text
New Evidence
     │
     ▼
Identify Changed Evidence
     │
     ▼
Identify Stale Specialist Results
     │
     ▼
Re-run Affected Specialist(s)
     │
     ▼
Supervisor Fan-In
     │
     ▼
Recalculate Quality Decision
```

### Reassessment Limit

The maximum automated reassessment cycles per incident is **2**.

If the incident remains unresolved after the second automated reassessment cycle:

```text
Second Unresolved Reassessment
              │
              ▼
        Manual Review
```

This prevents uncontrolled automation loops.

---

## 7. Retry and Fallback

A failed specialist or required tool operation may be retried once.

```text
Specialist / Tool Failure
          │
          ▼
       Retry Once
          │
     ┌────┴────┐
     │         │
  Success    Failure
     │         │
     ▼         ▼
 Continue   Record Failure
               │
               ▼
      Insufficient Evidence /
          Manual Review
```

The second failure must be explicitly recorded.

The system must never:

* Fabricate a successful tool operation.
* Claim that a report was created when creation failed.
* Claim that an email was sent when sending failed.
* Treat missing evidence as confirmed evidence.

---

## 8. Autonomous Operating Mode

The autonomous workflow starts from a recurrence event trigger without requiring a user chat message.

```text
Recurrence Event Trigger
          ↓
Quality Supervisor
          ↓
Read Unprocessed Complaints
          ↓
Process One Logical SKU/Batch Cluster
          ↓
Validate Required Identifiers
          ↓
Specialist Assessment
```

The autonomous workflow reads complaint records where `Processed = No`.

One logical SKU/batch cluster is processed per trigger execution.

Complaint records are marked as processed only after the corresponding assessment record has been successfully created or updated.

If no unprocessed complaints exist, the workflow exits without creating an incident.

---

## 9. Interactive Operating Mode

The same published Quality Supervisor also supports interactive employee requests.

```text
Employee Request
       │
       ▼
Quality Supervisor
       │
       ├── Appropriate Topic
       ├── Appropriate Specialist
       └── Appropriate Knowledge Source
```

Interactive requests may cover:

* Product quality.
* Open incidents.
* CAPA information.
* Product care.
* Internal quality policy.

The interactive entry point is Teams / Microsoft 365 Copilot chat.

---

## 10. Combined Orchestration Flow

The complete orchestration pattern combines sequential, hierarchical, parallel, conditional, loop, and fallback behavior.

```text
                    Recurrence Trigger
                           │
                           ▼
                   Quality Supervisor
                           │
                           ▼
                Intake & Validation Topic
                           │
                    Valid Evidence?
                       │       │
                      No      Yes
                       │       │
                       ▼       ▼
                     Exit    Fan-Out
                               │
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
     Complaint             Returns             Product/Batch
      Pattern             Specialist            Specialist
     Specialist
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                               ▼
                     Customer Impact
                       Specialist
                               │
                               ▼
                         Safety Analysis
                               │
                               ▼
                         Supervisor Fan-In
                               │
                               ▼
                       Quality Decision
                               │
                ┌──────────────┼───────────────┐
                ▼              ▼               ▼
             Critical     Investigation    High-Priority
                │              │               │
                └──────────────┼───────────────┘
                               ▼
                         CAPA / Evidence
                               │
                               ▼
                        New Evidence?
                          │       │
                         Yes      No
                          │       │
                          ▼       ▼
                   Selective      Supervisor
                  Reassessment     Validation
                          │           │
                          └─────┬─────┘
                                ▼
                         Word / Excel /
                            Outlook
```

---

## 11. Orchestration Governance Principles

The implementation follows these principles:

1. The Quality Supervisor owns orchestration.
2. Specialists perform independent domain analysis.
3. Specialist responsibilities do not overlap.
4. Independent specialist findings are consolidated through Supervisor fan-in.
5. Explicit governance conditions control routing.
6. Safety findings receive Critical-path precedence.
7. New evidence triggers only the necessary reassessment.
8. Reassessment is limited to two automated cycles.
9. Failed specialists and required tool operations may be retried once.
10. Second failures are recorded explicitly.
11. Missing evidence is never silently replaced with assumptions.
12. Successful completion is never claimed when an underlying operation fails.
13. Final severity and internal/external actions remain under Supervisor control.