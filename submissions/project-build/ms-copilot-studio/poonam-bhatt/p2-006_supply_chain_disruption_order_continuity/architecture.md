# Architecture

## 1. Purpose

The P2-006 Supply Chain Disruption & Order Continuity solution uses a supervisor-led multi-agent architecture to automate the assessment of supply disruptions and determine an appropriate order-continuity response.

The architecture separates orchestration responsibilities from specialist business assessments.

The Supervisor Agent coordinates the workflow, while specialist agents perform specific assessment activities.

---

## 2. Architecture Overview

The solution consists of the following major components:

1. Supervisor Agent
2. Specialist Agents
3. Custom Topics
4. Excel-based business data
5. Microsoft Word document generation
6. Outlook stakeholder notification
7. Autonomous/recurrence trigger

The high-level architecture is:

```text
                         +----------------------+
                         | Autonomous Trigger   |
                         | / User Request       |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |  Supervisor Agent    |
                         |                      |
                         | Orchestration        |
                         | Validation           |
                         | Fan-Out              |
                         | Fan-In               |
                         | Final Decision       |
                         +----------+-----------+
                                    |
              +---------------------+---------------------+
              |                     |                     |
              v                     v                     v
     +----------------+   +------------------+   +----------------------+
     | Inventory      |   | Alternate       |   | Customer & Order     |
     | Impact         |   | Supplier        |   | Impact               |
     | Specialist     |   | Specialist      |   | Specialist            |
     +-------+--------+   +--------+---------+   +----------+-----------+
             |                     |                        |
             +---------------------+------------------------+
                                   |
                                   v
                         +----------------------+
                         | Commercial Impact    |
                         | Specialist           |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         | Consolidation /      |
                         | Recovery Strategy    |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         | Approval &            |
                         | Reassessment Topic   |
                         +----------+-----------+
                                    |
                     +--------------+--------------+
                     |                             |
                     v                             v
            +------------------+          +----------------------+
            | Final Response   |          | Human Approval /     |
            | Report           |          | Manual Review        |
            +--------+---------+          +----------------------+
                     |
                     v
            +----------------------+
            | Authorized           |
            | Stakeholder Notice   |
            +----------------------+
````

---

## 3. Supervisor Layer

The Supervisor Agent is the central control point of the architecture.

It is responsible for coordinating the complete disruption assessment workflow.

The Supervisor Agent does not replace the specialist agents. Instead, it determines when each specialist assessment is required and uses their outputs to progress the workflow.

### Supervisor responsibilities

The Supervisor Agent is responsible for:

* Identifying the disruption to assess.
* Retrieving the appropriate disruption record.
* Ensuring the disruption is eligible for assessment.
* Invoking the disruption intake validation topic.
* Updating the disruption status after successful validation.
* Calling the required specialist agents.
* Collecting specialist outputs.
* Coordinating the recovery-strategy decision.
* Coordinating approval and reassessment checks.
* Initiating final response generation.
* Initiating authorized stakeholder notification.

The Supervisor therefore acts as the orchestration layer rather than the primary source of specialist business calculations.

---

## 4. Specialist Agent Layer

The specialist layer divides the assessment into domain-specific responsibilities.

The implemented specialist areas are:

```text
Inventory Impact Specialist
Alternate Supplier Specialist
Customer & Order Impact Specialist
Commercial Impact Specialist
```

Each specialist receives the information relevant to its assessment and returns structured findings that can be consumed by the Supervisor Agent.

This architecture avoids putting all supply-chain decision logic into one large agent.

---

## 5. Inventory Impact Specialist

The Inventory Impact Specialist is responsible for evaluating inventory consequences.

Its assessment uses the configured business data sources to determine whether sufficient inventory evidence is available.

Relevant information can include:

* SKU information.
* Inventory position.
* On-hand quantity.
* Reserved quantity.
* Quality-hold quantity.
* Inbound quantity.
* Demand until recovery.
* Safety stock.
* Available-to-Promise.

The specialist can identify evidence conflicts across source records.

For example, if the disruption references a SKU that cannot be found in the required inventory or master-data sources, the specialist should report insufficient evidence.

The specialist should not fabricate missing inventory values.

---

## 6. Alternate Supplier Specialist

The Alternate Supplier Specialist evaluates supplier recovery options.

The assessment determines whether an alternate supplier is available and whether the alternate supplier is approved.

The information returned by this specialist supports the recovery strategy decision.

The relevant outcomes include:

```text
No alternate supplier
Alternate supplier available but unapproved
Alternate supplier available and approved
```

The recovery strategy topic uses this information when selecting an appropriate recovery path.

---

## 7. Customer & Order Impact Specialist

The Customer & Order Impact Specialist evaluates the impact of the disruption on customer commitments and orders.

The specialist provides information needed to determine whether customer commitments may be affected and whether customer action or prioritization is required.

The output can contribute to the recovery strategy when inventory is insufficient to satisfy all affected demand.

This allows the supervisor to distinguish between a situation where existing stock is sufficient and a situation where customer commitments may require prioritization or negotiation.

---

## 8. Commercial Impact Specialist

The Commercial Impact Specialist evaluates commercial considerations associated with the disruption and proposed recovery action.

Commercial information can include the configured premium-related information used by the approval topic.

The specialist output supports decisions such as whether the recovery action may require additional business approval.

The Commercial Impact Specialist therefore contributes evidence to the approval and recovery decision rather than independently approving a recovery action.

---

## 9. Custom Topic Layer

Three important custom topics are implemented in the Supervisor workflow.

### 9.1 Disruption Intake Topic

The Disruption Intake topic performs initial validation.

It checks required disruption information and verifies that the disruption is in the expected Pending state.

The topic also includes duplicate detection.

Successful validation results in:

```text
ValidationStatus = Passed
Status = In Assessment
```

Failed validation results in:

```text
Status = Insufficient Evidence
```

This topic prevents invalid disruption records from immediately entering the specialist assessment stage.

---

### 9.2 Strategy Resolution Topic

The Strategy Resolution topic determines the proposed recovery strategy using the configured decision precedence.

The implemented branches include:

```text
No viable recovery route
        ↓
Management escalation

Unapproved alternate supplier
        ↓
Manual supplier qualification

Existing inventory sufficient
        ↓
Use existing stock

Approved alternate supplier
        ↓
Use approved alternate supplier

Partial inventory
        ↓
Reallocate inventory & negotiate customer dates
```

The topic also assigns the configured risk classification and rationale for the selected branch.

---

### 9.3 Approval / Reassessment Topic

The Approval/Reassessment topic evaluates whether the proposed recovery action requires approval.

Configured approval triggers include:

* Cost premium above the configured threshold.
* Expedite premium above the configured threshold.
* Unapproved alternate supplier.
* Strategic SLA risk combined with safety-stock consumption.

When approval is required:

```text
Status = Awaiting Approval
```

The topic also identifies the required approver.

If reassessment is required because relevant information has changed, the topic can initiate the configured selective reassessment behavior.

A maximum automated reassessment cycle count is enforced.

When the configured limit is exceeded:

```text
Status = Manual Review
```

---

## 10. Data Layer

The solution uses structured business data stored in the configured Excel source.

The data is used by the workflow and specialist agents to retrieve disruption and supporting business information.

The architecture follows a data-driven assessment model:

```text
Excel Business Data
        |
        v
Data Retrieval
        |
        v
Specialist Assessment
        |
        v
Structured Specialist Output
        |
        v
Supervisor Consolidation
```

The specialist agents are expected to use the configured source data rather than inventing unavailable information.

---

## 11. Status-Based Workflow

The disruption status is used as a control mechanism throughout the architecture.

Important statuses include:

```text
Pending
   |
   v
In Assessment
   |
   +------------------------------+
   |              |               |
   v              v               v
Recovery Plan   Customer       Management
Proposed        Action         Escalation
                Required
   |
   v
Awaiting Approval
   |
   v
Completed
```

Other controlled outcomes include:

```text
Insufficient Evidence
Manual Review
```

The exact status depends on the assessment results and decision rules.

---

## 12. Fan-Out Pattern

After successful intake validation, the Supervisor uses a fan-out pattern.

The supervisor invokes the required specialist assessments rather than performing every assessment sequentially inside one topic.

Conceptually:

```text
                    Supervisor
                        |
        +---------------+---------------+
        |               |               |
        v               v               v
    Inventory       Alternate       Customer &
     Impact         Supplier         Order Impact
        |               |               |
        +---------------+---------------+
                        |
                        v
                 Commercial Impact
```

The purpose of this pattern is to separate business responsibilities and allow each specialist to focus on its domain.

---

## 13. Fan-In Pattern

After specialist assessments are completed, their outputs are consolidated by the Supervisor.

The fan-in stage combines the relevant specialist findings and makes them available to the downstream recovery strategy and approval logic.

Conceptually:

```text
Inventory Assessment
        |
Alternate Supplier Assessment
        |
Customer & Order Assessment
        |
Commercial Assessment
        |
        v
+-------------------------+
| Supervisor Consolidation|
+------------+------------+
             |
             v
     Recovery Strategy
```

The supervisor should base downstream decisions on the available specialist evidence.

---

## 14. Reporting Layer

The reporting layer is responsible for producing the final response report.

The solution includes a Microsoft Word document-generation component.

The final report is intended to capture the outcome of the completed assessment in a structured format.

The report can include:

* Disruption identification.
* Validation result.
* Specialist assessment results.
* Recovery strategy.
* Risk.
* Rationale.
* Approval requirement.
* Final status.
* Relevant evidence or limitations.

The report generation step occurs after the required assessment and decision stages.

---

## 15. Notification Layer

The notification layer uses the configured Outlook capability to send the authorized stakeholder notification.

The notification is intended to communicate the final assessment outcome to the appropriate stakeholder.

The notification should be based on the final workflow state rather than being sent prematurely during intake or specialist assessment.

The architecture therefore follows:

```text
Assessment
    ↓
Decision
    ↓
Final Status
    ↓
Report Generation
    ↓
Authorized Notification
```

---

## 16. Autonomous Trigger

The solution includes an autonomous/recurrence trigger for initiating the assessment workflow.

The trigger is intended to allow the solution to periodically identify eligible disruption records and initiate processing without requiring a user to manually start every assessment.

The trigger feeds the Supervisor Agent, which then performs the normal validation and orchestration process.

The trigger does not replace the Supervisor's validation logic.

Instead:

```text
Recurrence Trigger
        ↓
Supervisor
        ↓
Retrieve Eligible Disruption
        ↓
Validate
        ↓
Assess
```

---

## 17. Human-in-the-Loop Control

The architecture deliberately retains human involvement where the configured business rules require approval.

For example, when an approval condition is triggered, the solution moves the disruption to:

```text
Awaiting Approval
```

The AI is not expected to fabricate human approval.

Similarly, when evidence is insufficient or automated reassessment reaches its configured limit, the workflow can route the disruption to a controlled state such as:

```text
Insufficient Evidence
```

or:

```text
Manual Review
```

This provides a controlled boundary between autonomous assessment and human decision-making.

---

## 18. Error and Evidence Handling

The architecture is designed to distinguish between successful assessment and insufficient evidence.

A specialist may complete its assessment while still reporting that the evidence is insufficient for a reliable business conclusion.

For example:

```text
Assessment Completed
        |
        v
Evidence Missing
        |
        v
AssessmentStatus =
Insufficient Evidence
```

The system should not replace unavailable business data with invented values.

Where a required source cannot be retrieved, the relevant assessment should identify the limitation and allow the supervisor to determine the appropriate downstream status.

---

## 19. End-to-End Architecture Flow

The complete architecture can be represented as:

```text
                    +----------------------+
                    | Recurrence / User    |
                    | Initiation            |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | SUPERVISOR AGENT     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Retrieve Disruption  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Intake Validation     |
                    +----------+-----------+
                               |
                    +----------+----------+
                    |                     |
              Validation Fail       Validation Pass
                    |                     |
                    v                     v
          Insufficient Evidence    In Assessment
                                          |
                                          v
                              +-----------------------+
                              | Specialist Fan-Out    |
                              +-----------+-----------+
                                          |
                 +------------------------+------------------------+
                 |             |              |                   |
                 v             v              v                   v
            Inventory     Alternate      Customer &          Commercial
             Impact        Supplier       Order Impact          Impact
                 |             |              |                   |
                 +-------------+--------------+-------------------+
                                          |
                                          v
                              +-----------------------+
                              | Result Consolidation  |
                              +-----------+-----------+
                                          |
                                          v
                              +-----------------------+
                              | Strategy Resolution   |
                              +-----------+-----------+
                                          |
                                          v
                              +-----------------------+
                              | Approval /            |
                              | Reassessment          |
                              +-----------+-----------+
                                          |
                              +-----------+-----------+
                              |                       |
                              v                       v
                         Approval Needed         Continue
                              |                       |
                              v                       |
                      Awaiting Approval              |
                                                      |
                              +-----------------------+
                              |
                              v
                    +----------------------+
                    | Final Response       |
                    | Report               |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Authorized           |
                    | Stakeholder Notice   |
                    +----------------------+
```

---

## 20. Architectural Principles

The solution follows these primary principles:

### Separation of Responsibilities

The Supervisor orchestrates the workflow while specialist agents perform domain-specific assessments.

### Evidence-Based Decisions

Business decisions should be based on available source evidence.

### Controlled Automation

Human approval and manual-review states are preserved where required.

### Status-Driven Processing

The disruption status provides a clear indication of the workflow stage and outcome.

### Reusable Specialist Assessments

Specialist agents are separated by business responsibility so that their outputs can be reused by the supervisor.

### Bounded Reassessment

Automated reassessment is limited to prevent uncontrolled loops.

### Finalized Reporting

The final report and notification are downstream activities and should occur after the assessment and decision stages have completed.

```
```
