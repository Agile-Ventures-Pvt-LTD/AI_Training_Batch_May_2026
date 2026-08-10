# architecture.md

# CAP-001 — Architecture

## 1. Architecture Overview

The Sleepsia Product Quality & Customer Experience Intelligence Control Tower follows a hierarchical multi-agent architecture implemented in Microsoft Copilot Studio.

The architecture is centered on the **Quality Supervisor**, which owns orchestration, consolidation, final decision-making, reassessment control, and authorization of downstream actions.

Specialist agents perform independent domain analysis and return structured findings to the Supervisor.

```text
                         ┌──────────────────────┐
                         │   Recurrence Trigger │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Quality Supervisor  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │ Incident Intake & Validation │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                         ┌──────────────────────┐
                         │ Valid Incident Data? │
                         └───────┬───────┬──────┘
                                 │       │
                                No      Yes
                                 │       │
                                 ▼       ▼
                              Reject   Fan-Out
                                        │
                ┌───────────────────────┼───────────────────────┐
                │           │           │           │           │
                ▼           ▼           ▼           ▼           ▼
          Complaint      Returns    Product/Batch Customer    Safety
           Pattern       Specialist  Specialist   Impact    Specialist
          Specialist                               Specialist
                │           │           │           │           │
                └───────────────────────┼───────────────────────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │ Supervisor      │
                               │ Fan-In          │
                               └────────┬────────┘
                                        │
                                        ▼
                            ┌────────────────────────┐
                            │ Quality Investigation  │
                            │ Decision               │
                            └───────────┬────────────┘
                                        │
                         ┌──────────────┼──────────────┐
                         │              │              │
                         ▼              ▼              ▼
                      Critical     Investigation   High-Priority
                      Escalation      / CAPA
                                        │
                                        ▼
                               ┌─────────────────┐
                               │ CAPA Specialist │
                               └────────┬────────┘
                                        │
                                        ▼
                              Reassessment / Review
                                        │
                                        ▼
                              Supervisor Validation
                                        │
                         ┌──────────────┼──────────────┐
                         ▼              ▼              ▼
                    Excel Update   Word Report     Outlook
                                                     Notification
```

---

## 2. Quality Supervisor

The Quality Supervisor is the central orchestration and governance component.

### Responsibilities

* Initiate and coordinate the quality assessment workflow.
* Validate incoming complaint information.
* Prevent duplicate processing.
* Select and invoke the appropriate specialist agents.
* Coordinate parallel specialist execution.
* Consolidate specialist outputs.
* Apply deterministic decision precedence.
* Resolve conflicting specialist findings.
* Determine the final quality classification.
* Coordinate CAPA and evidence workflows.
* Control selective reassessment.
* Enforce the reassessment limit.
* Validate the final outcome.
* Authorize report generation.
* Authorize stakeholder notification.

The Supervisor is the **sole final decision owner**.

Specialist agents provide evidence and recommendations but do not independently determine the final quality decision.

---

## 3. Specialist Architecture

### 3.1 Complaint Pattern Specialist

Responsible for identifying complaint patterns and clustering complaints by relevant product and batch information.

It provides pattern evidence to the Quality Supervisor.

### 3.2 Returns Specialist

Responsible for evaluating return-related evidence, including return counts and return-rate calculations using the applicable sales information.

It provides return-risk findings to the Quality Supervisor.

### 3.3 Product-Batch Specialist

Responsible for evaluating product and batch-related information and identifying previous incidents or repeat quality concerns.

It provides product/batch evidence to the Quality Supervisor.

### 3.4 Customer Impact Specialist

Responsible for evaluating customer-impact information and determining the potential impact associated with the quality issue.

It provides customer-impact findings to the Quality Supervisor.

### 3.5 Safety Specialist

Responsible for identifying safety-related indicators and determining whether a safety concern requires Critical escalation.

Safety findings have the highest decision precedence.

### 3.6 CAPA Specialist

Runs for Investigation Required, High-Priority, or Critical classifications.

Responsibilities include:

* Containment recommendations.
* Corrective-action recommendations.
* Preventive-action recommendations.
* Owner-role assignment.
* Target-date assignment.
* Validation-method definition.
* CAPA register management.

The CAPA Specialist does not claim that root cause is confirmed without explicit evidence and does not independently close Critical incidents.

### 3.7 M365 Guidance Specialist

Provides Microsoft 365 guidance using the Microsoft Learn MCP integration.

The MCP integration is non-blocking to the core product-quality decision workflow.

---

## 4. Tool Boundaries

Operational data access is separated by specialist responsibility.

| Tool Category | Primary Responsibility |
|--------------|------------------------|
| Customer Complaints Data | Complaint Pattern Specialist |
| Returns and Sales Data | Returns Specialist |
| Product and Batch Data | Product-Batch Specialist |
| Customer Complaint Impact Data | Customer Impact Specialist |
| Safety Complaint Data | Safety Specialist |
| CAPA Register | CAPA Specialist |
| Quality Rules | Quality Supervisor |
| Quality Incident Register | Quality Supervisor / relevant workflow |
| Owners | CAPA workflow |
| Word Report | Quality Supervisor |
| Outlook Notification | Quality Supervisor |
| Microsoft Learn MCP | M365 Guidance Specialist |

Tools are scoped to the agents that require them. Specialists should not receive unnecessary access to unrelated operational data.

---

## 5. Data and Integration Layer

### Excel Online (Business)

Excel Online provides the operational data layer.

The solution uses Excel for:

* Customer complaints.
* Returns.
* Sales summary.
* Product master.
* Batch register.
* Safety complaints.
* Quality incidents.
* CAPA register.
* Owners.
* Quality rules.

Excel is also used for state updates after the Supervisor has reached an appropriate decision.

The system must not silently overwrite source evidence.

### Word Online (Business)

Word Online is used to create the Product Quality Investigation Report after the appropriate Supervisor validation.

The report is generated only after the required decision and validation steps have completed.

### Office 365 Outlook

Outlook is used to send internal quality notifications after the Supervisor has validated the final decision.

The system must not claim that an email was sent if the sending operation fails.

### Microsoft Learn MCP

Microsoft Learn MCP is connected to the M365 Guidance Specialist only.

Its failure must not block the product-quality decision workflow.

---

## 6. Orchestration Architecture

### Sequential Flow

The principal workflow follows this sequence:

```text
Trigger
   ↓
Incident Intake & Validation
   ↓
Specialist Analysis
   ↓
Supervisor Fan-In
   ↓
Quality Investigation Decision
   ↓
CAPA / Evidence / Closure Path
   ↓
Supervisor Validation
   ↓
Word Report
   ↓
Excel Update
   ↓
Outlook Notification
```

### Parallel Fan-Out

After successful intake validation, independent specialist assessments can run in parallel.

```text
                 Quality Supervisor
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     Complaint         Returns      Product-Batch
      Pattern          Specialist    Specialist
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                    Fan-In
```

Customer Impact and Safety analysis are also incorporated according to the applicable incident path.

### Fan-In

The Supervisor waits for the relevant specialist findings and consolidates them into a unified decision context.

No specialist result alone constitutes the final quality decision.

---

## 7. Decision Architecture

The Supervisor applies explicit precedence when multiple conditions are present.

```text
Safety Indicator
      ↓
Complaint Cluster Threshold
      ↓
Return-Rate Threshold
      ↓
Previous Incident History
      ↓
Missing Evidence
      ↓
Overdue CAPA
      ↓
Final Classification
```

The system uses deterministic governance rules rather than averaging specialist outputs.

The highest-precedence applicable condition controls the final classification.

---

## 8. Reassessment Architecture

When new evidence is supplied, the Supervisor determines which specialist results are stale.

Only affected analyses are rerun.

```text
New Evidence
     │
     ▼
Identify Affected Domain
     │
     ▼
Mark Related Result Stale
     │
     ▼
Re-run Required Specialist
     │
     ▼
Supervisor Fan-In
     │
     ▼
Recalculate Decision
```

Automated reassessment is bounded to **two cycles per incident**.

If the issue remains unresolved after the permitted reassessment cycles, the incident is routed to Manual Review.

---

## 9. Failure and Fallback Architecture

Specialist failures are handled without fabricating successful results.

```text
Specialist Failure
       │
       ▼
     Retry
       │
   ┌───┴────┐
 Success   Failure
   │          │
   ▼          ▼
Continue   Insufficient
            Evidence
               │
               ▼
          Manual Review
```

For operational tools:

* Failed Excel reads prevent unsupported conclusions.
* Failed Excel updates do not result in a false processed state.
* Failed Word generation preserves the quality decision but records report failure.
* Failed Outlook sending preserves the quality decision but records notification failure.
* MCP failure does not block the core quality workflow.

---

## 10. State Management

The quality workflow maintains explicit incident states.

```text
New Incident
     ↓
In Assessment
     ↓
┌────┴───────────────────────────┐
│                                │
▼                                ▼
Monitoring                Investigation Open
                                │
                                ▼
                           CAPA Open
                                │
                                ▼
                       Awaiting Evidence
                                │
                                ▼
                          Reassessment
                                │
                                ▼
                         Supervisor Review
                                │
                 ┌──────────────┼──────────────┐
                 ▼              ▼              ▼
             Critical        Manual         Closed
            Escalation       Review
```

State transitions are controlled by the Supervisor and applicable governance rules.

---

## 11. Governance and Safety Boundaries

The architecture enforces the following boundaries:

* The Quality Supervisor owns final decisions.
* Specialist agents cannot independently close Critical incidents.
* Root cause is not treated as confirmed without explicit evidence.
* Missing evidence cannot be silently replaced with assumptions.
* Tool failures cannot be represented as successful actions.
* Critical safety findings take precedence over lower-priority findings.
* Human review remains available for unresolved or high-risk cases.
* Autonomous reassessment is bounded.
* The system evaluates and governs quality incidents; it does not fabricate operational completion.

---

## 12. Architecture Principles

The solution follows these principles:

1. **Centralized governance** — final decisions remain with the Quality Supervisor.
2. **Specialization** — each specialist has a defined domain responsibility.
3. **Least-privilege tool access** — agents receive only the tools required for their responsibilities.
4. **Deterministic decision-making** — explicit governance precedence controls outcomes.
5. **Evidence-based assessment** — unsupported conclusions are not permitted.
6. **Traceability** — specialist findings are retained as decision evidence.
7. **Bounded automation** — reassessment and retry loops have explicit limits.
8. **Safe failure handling** — failures result in evidence gaps or escalation rather than fabricated success.
9. **Human oversight** — unresolved and critical scenarios can require human review.
10. **Separation of analysis and decision authority** — specialists analyze; the Supervisor decides.