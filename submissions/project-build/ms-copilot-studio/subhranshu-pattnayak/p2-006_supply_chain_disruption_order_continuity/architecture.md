# Solution Architecture

## Architecture Overview

The Supply Chain Disruption Order Continuity System follows a Supervisor-Orchestrated Multi-Agent Architecture implemented in Microsoft Copilot Studio.

The architecture separates orchestration, specialist analysis, governance decisions, and reporting responsibilities into distinct components.

This separation ensures:

- Clear responsibility boundaries
- Policy compliance
- Auditability
- Scalable assessment workflows
- Deterministic governance decisions

The solution combines autonomous agents, deterministic custom topics, and Microsoft productivity services to create an end-to-end disruption management workflow.

---

## High-Level Architecture

```text
                Autonomous Trigger
                        |
                        V
                Supply Continuity Supervisor
                        |
                        V
                Disruption Intake & Validation Topic
                        |
        +--------------------------------------+
        |                                      |
        V                                      V

Inventory Impact Specialist      Alternate Supplier Specialist
        |                                      |
        +------------------+-------------------+
                           |
                           V

    Customer & Order Impact Specialist

                           |
                           V

                Commercial Impact Specialist

                           |
                           V

            Supervisor Fan-In Consolidation

                           |
                           V

                Recovery Planning Specialist

                           |
                           V

            Recovery Strategy Resolution Topic

                           |
                           V

        Approval, Exception & Selective Reassessment Topic

                           |
                           V

                Final Supervisor Decision

                           |
                           V

            Reporting & Communication Specialist

                           |
              +------------+------------+
              |                         |
              V                         V

      Word Report            Outlook Notification

                           |
                           V

                   Status Update
```

---

## Architectural Components

### 1. Autonomous Trigger

The workflow begins with a scheduled autonomous trigger.

Responsibilities:

- Monitor disruption requests.
- Identify pending disruption records.
- Initiate assessment workflow.
- Pass disruption context to the Supervisor.

The trigger acts as the workflow entry point.

---

### 2. Supply Continuity Supervisor

The Supervisor is the central orchestration component.

Responsibilities include:

- Workflow coordination
- Specialist execution
- Parallel task orchestration
- Fan-in consolidation
- Policy enforcement
- Approval determination
- Escalation handling
- Final recommendation generation

The Supervisor does not perform specialist analysis directly.

---

### 3. Disruption Intake & Validation Topic

This deterministic topic validates disruption requests before specialist execution.

Validation includes:

- Required field checks
- Quantity validation
- Date validation
- Request completeness checks

Possible outcomes:

- PASS
- FAIL

Invalid requests stop further processing.

---

## Specialist Assessment Layer

The specialist layer performs domain-specific analysis.

Each specialist operates independently and returns structured findings to the Supervisor.

---

### Inventory Impact Specialist

Purpose:

Evaluate inventory availability and inventory risk.

Primary outputs:

- ATP assessment
- Inventory risk
- Shortage assessment
- Safety stock impact
- Inventory recommendation

---

### Alternate Supplier Specialist

Purpose:

Evaluate alternate sourcing options.

Primary outputs:

- Alternate supplier availability
- Supplier approval status
- Supplier capacity
- Supplier risk
- Supplier recommendation

---

### Customer & Order Impact Specialist

Purpose:

Evaluate customer exposure and fulfillment risk.

Primary outputs:

- Strategic orders at risk
- SLA orders at risk
- Customer impact classification
- Revenue exposure
- Customer recommendations

---

### Commercial Impact Specialist

Purpose:

Evaluate financial and approval implications.

Primary outputs:

- Cost premium percentage
- Expedite premium percentage
- Incremental cost
- Commercial risk
- Approval requirements

---

## Fan-Out Pattern

The Supervisor launches the following specialists in parallel:

- Inventory Impact Specialist
- Alternate Supplier Specialist
- Customer & Order Impact Specialist
- Commercial Impact Specialist

Benefits:

- Faster assessment completion
- Reduced workflow duration
- Independent domain analysis

---

## Fan-In Pattern

After specialist execution completes, the Supervisor performs fan-in consolidation.

Responsibilities:

- Collect findings
- Identify conflicts
- Evaluate dependencies
- Review approval requirements
- Prepare consolidated assessment package

The consolidated package becomes the input for recovery planning.

---

## Recovery Planning Layer

### Recovery Planning Specialist

Purpose:

Evaluate recovery alternatives using specialist findings.

Inputs:

- Inventory findings
- Supplier findings
- Customer findings
- Commercial findings

Outputs:

- Proposed strategy
- Orders protected
- Orders remaining at risk
- Residual risk
- Required actions
- Required approvals

The Recovery Planning Specialist recommends a strategy but does not approve execution.

---

## Governance Layer

The Governance Layer consists of deterministic custom topics.

These topics enforce business rules that must not depend solely on generative reasoning.

---

### Recovery Strategy Resolution Topic

Purpose:

Resolve recovery recommendations into approved recovery branches.

Possible outcomes:

| Branch | Description |
|----------|-------------|
| A | Existing Inventory |
| B | Partial Fulfillment |
| C | Approved Alternate Supplier |
| D | Unapproved Alternate Supplier |
| E | Management Escalation |

Outputs:

- SelectedRecoveryBranch
- SelectedRecoveryStrategy
- EscalationRequired

---

### Approval, Exception & Selective Reassessment Topic

Purpose:

Manage approvals and reassessment governance.

Responsibilities:

- Approval routing
- Reassessment cycle tracking
- Manual review determination

Possible outcomes:

- Approved Route
- Awaiting Approval
- Manual Review

Outputs:

- CaseStatus
- ManualReviewRequired
- UpdatedReassessmentCycleCount

---

## Policy Knowledge Base

The Supervisor references a policy knowledge base to enforce organizational decision rules.

The knowledge base supports:

- Recovery strategy governance
- Approval policies
- Customer priority policies
- Supplier approval policies
- Escalation rules

The policy knowledge base is used during:

- Fan-in consolidation
- Conflict resolution
- Recovery evaluation
- Approval determination

---

## Decision Precedence Hierarchy

The Supervisor applies the following decision order:

1. Safety or Quality Restrictions
2. Strategic/SLA-Protected Commitments
3. Supplier Approval Restrictions
4. Inventory Availability and Timing
5. Commercial Approval Requirements
6. Cost Optimization
7. Lower-Priority Customer Convenience

Higher-priority rules always override lower-priority rules.

---

## Reporting & Communication Layer

### Reporting & Communication Specialist

Purpose:

Generate approved reports and stakeholder communications.

Responsibilities:

- Generate disruption response report
- Create Word document
- Prepare stakeholder notifications
- Send Outlook communications
- Return execution status

Outputs:

- ReportGenerated
- ReportLocation
- NotificationSent
- NotificationRecipients

---

## External Services

### Microsoft Excel

Used as the operational data source.

Provides:

- Disruption Requests
- SKU Master Data
- Inventory Data
- Supplier Data
- Alternate Supplier Data
- Customer Orders
- Recovery Rules

---

### Microsoft Word

Used to generate the final Supply Disruption Response Report.

---

### Microsoft Outlook

Used to distribute stakeholder notifications.

---

## End-to-End Processing Sequence

```text
         Trigger
            |
            V
        Supervisor
            |
            V
    Validation Topic
            |
            V
    Parallel Specialists
            |
            V
    Fan-In Consolidation
            |
            V
    Recovery Planning
            |
            V
    Recovery Strategy Topic
            |
            V
    Approval/Reassessment Topic
            |
            V
    Final Supervisor Decision
            |
            V
    Reporting & Communication
            |
            V
Word Report + Outlook Notification
            |
            V
        Status Update
```

---

## Architectural Benefits

The architecture provides:

### Separation of Concerns

Each component performs a specific responsibility.

### Scalability

Additional specialists can be added without redesigning orchestration.

### Governance

Critical decisions are enforced through deterministic topics.

### Explainability

All recommendations are traceable to specialist findings and policy rules.

### Auditability

Every decision can be linked to:

- Source data
- Specialist outputs
- Governance topics
- Policy rules

### Business Continuity

Provides a structured and repeatable response process for supply disruptions.

---

## Supporting Screenshots

The following screenshots are included in the project package:

- supervisor-agent.png
- child-agents.png
- recurrence-trigger.png
- intake-validation-topic.png
- fan-out-specialists.png
- fan-in-consolidation.png
- recovery-strategy-topic.png
- approval-reassessment-topic.png
- excel-tools.png
- word-tool.png
- outlook-tool.png
- final-response.png
- successful-trigger.png
- mail-sent.png
- word-generated.png

---