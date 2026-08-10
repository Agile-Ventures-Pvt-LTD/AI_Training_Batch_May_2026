# Autonomous Trigger Design

## Overview

The solution uses a **Microsoft Copilot Studio Recurrence Event Trigger** to start the Supply Continuity workflow autonomously without requiring a user conversation.

The trigger activates the **Mohd Zaid Supply Continuity Supervisor**, which manages the complete disruption assessment process.

---

# Trigger Type

**Event Trigger: Recurrence**

Platform:

* Microsoft Copilot Studio

Purpose:

* Monitor disruption requests automatically.
* Start disruption assessment workflow.
* Process one pending disruption per execution.

---

# Trigger Flow

```text
Recurrence Trigger
        |
        ▼
Supply Continuity Supervisor
        |
        ▼
Retrieve Pending Disruption
        |
        ▼
Validate Request
        |
        ▼
Run Specialist Assessment
        |
        ▼
Generate Recovery Decision
```

---

# Execution Logic

On every trigger execution:

1. Retrieve records from **DisruptionRequestsTable**.
2. Find records where:

```
Status = Pending
```

3. Select the oldest pending disruption.
4. Update status:

```
Pending → In Assessment
```

5. Start validation workflow.
6. Continue orchestration through the Supervisor.

---

# Processing Rules

The trigger must:

* Process only one disruption per execution.
* Prevent duplicate processing.
* Ignore already processed records.
* Stop safely when no pending disruption exists.

---

# No Pending Disruption Handling

If no pending disruption is found:

* Do not start specialist analysis.
* End workflow successfully.
* Record that no action was required.

---

# Duplicate Prevention

Before processing:

Check:

* Disruption ID uniqueness.
* Existing processing status.

If duplicate detected:

```
Status = Manual Review
```

No specialist agents are invoked.

---

# Supervisor Interaction

The trigger only starts execution.

The Supervisor controls:

* Validation
* Specialist delegation
* Recovery planning
* Approval routing
* Reporting
* Final status update

---

# Data Source

The trigger workflow reads:

**Excel Online (Business)**

Table:

```
DisruptionRequestsTable
```

Required fields:

* DisruptionID
* SupplierID
* SKU
* Status
* ReportedDate
* AffectedPO
* AffectedQty

---

# Failure Handling

## Excel Read Failure

Action:

* Stop execution.
* Record failure.
* Mark case for Manual Review if required.

---

## Excel Update Failure

Action:

* Do not claim completion.
* Retry update.
* Escalate if retry fails.

---

# Design Principles

* Autonomous execution without user input.
* Controlled single-record processing.
* Supervisor-driven orchestration.
* Deterministic state transitions.
* No unsupported business actions.
* Full traceability of workflow execution.

---

# Outcome

The recurrence trigger enables continuous autonomous monitoring of supply disruptions while maintaining business controls, approval boundaries, and reliable multi-agent execution.
