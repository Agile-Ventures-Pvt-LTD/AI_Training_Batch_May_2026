# Autonomous trigger

## NovaSphere supply continuity autonomous multi-agent system

## Purpose

This document defines the autonomous trigger architecture used by the NovaSphere Supply Continuity Autonomous Multi-Agent System.

The trigger layer is responsible for continuously monitoring pending supply disruptions and autonomously initiating the Supervisor Agent without requiring manual user interaction.

The trigger is designed to provide reliable, deterministic, and idempotent disruption processing.

## Trigger architecture

The system uses a **Power Automate recurrence trigger** as the autonomous execution mechanism.

```text
Power Automate Recurrence Trigger
               │
               ▼
Read Disruption_Requests
               │
               ▼
Filter Pending Disruptions
               │
               ▼
Select Oldest Pending Disruption
               │
               ▼
Update Status to In Assessment
               │
               ▼
Invoke Supervisor Agent
```

The trigger is the entry point for every autonomous execution cycle.

## Design objectives

The trigger layer is designed to:

* operate autonomously,
* process disruptions continuously,
* prevent duplicate processing,
* process one disruption at a time,
* preserve execution traceability,
* support reliable recovery,
* integrate cleanly with the Supervisor Agent.

## Trigger type

### Power Automate recurrence

Recommended schedule:

* Every 5 minutes

Alternative schedules:

* Every 1 minute for high-volume environments
* Every 15 minutes for low-volume environments
* Every hour for testing environments

The trigger frequency should balance responsiveness and execution cost.

## Data source

The trigger reads:

**Excel Online (Business)**

Workbook:

`P2-006_Supply_Chain_Continuity_Lab_Data.xlsx`

Table:

`Disruption_Requests`

## Trigger query

The recurrence flow retrieves disruptions where:

* Status = Pending

The flow sorts by:

* ReportedDate ascending

The oldest pending disruption is selected for processing.

## Single-disruption processing

Each execution cycle processes **exactly one disruption**.

Example:

| DisruptionID | Status  |
| ------------ | ------- |
| DSP-001      | Pending |
| DSP-002      | Pending |
| DSP-003      | Pending |

Execution cycle:

* DSP-001 selected
* DSP-002 remains pending
* DSP-003 remains pending

The next recurrence cycle processes DSP-002.

Benefits:

* simpler orchestration,
* easier recovery,
* deterministic execution,
* reduced concurrency risk,
* cleaner auditability.

## Duplicate-processing protection

Immediately after selecting a disruption, the flow updates:

Pending

↓

In Assessment

This occurs **before invoking the Supervisor Agent**.

Example:

| DisruptionID | Status  |
| ------------ | ------- |
| DSP-001      | Pending |

After lock:

| DisruptionID | Status        |
| ------------ | ------------- |
| DSP-001      | In Assessment |

Subsequent trigger executions ignore the record.

This provides idempotent processing.

## Trigger flow design

### Step 1: Recurrence

Power Automate starts automatically.

### Step 2: Read disruptions

Use:

**List rows present in a table**

Table:

`Disruption_Requests`

### Step 3: Filter pending

Condition:

`Status = Pending`

### Step 4: Check availability

If no pending disruptions exist:

* terminate the flow,
* wait for the next recurrence.

### Step 5: Select oldest disruption

Sort by:

`ReportedDate ascending`

Select the first row.

### Step 6: Lock the disruption

Update:

* Status = In Assessment
* LastUpdated = utcNow()

### Step 7: Invoke the Supervisor

Pass:

* DisruptionID
* SupplierID
* SKU
* AffectedPO
* AffectedQty
* ReportedSeverity
* ExpectedRecoveryDate
* DisruptionType

## Trigger payload

The Supervisor receives a structured disruption payload.

Example:

```json
{
  "DisruptionID": "DSP-001",
  "SupplierID": "SUP-001",
  "SKU": "SKU-1001",
  "AffectedPO": "PO-45821",
  "AffectedQty": 1200,
  "ReportedSeverity": "High",
  "ExpectedRecoveryDate": "2026-08-12",
  "DisruptionType": "Supplier Delay"
}
```

The trigger performs no business analysis.

## Trigger responsibilities

The trigger is responsible only for:

* polling,
* filtering,
* ordering,
* locking,
* payload creation,
* Supervisor invocation.

The trigger does not:

* validate suppliers,
* evaluate inventory,
* evaluate customers,
* evaluate suppliers,
* calculate commercial impact,
* propose recovery strategies.

## Supervisor handoff

The trigger hands control to the Supervisor immediately after locking the disruption.

The Supervisor owns the complete execution lifecycle.

```text
Trigger
   │
Lock
   │
   ▼
Supervisor
   │
Validation
   │
Scope
   │
Specialists
   │
Recovery
   │
Reporting
```

## Idempotency model

The trigger guarantees that a disruption is processed only once.

State transitions:

Pending

↓

In Assessment

↓

Final Status

A disruption already in:

* In Assessment
* Awaiting Approval
* Manual Review
* Completed

cannot be selected again.

## Concurrency control

Recommended Power Automate setting:

**Concurrency Control = 1**

This ensures:

* one trigger execution at a time,
* no duplicate Supervisor invocations,
* no competing Excel updates.

## Failure handling

### Trigger failure

If the recurrence flow fails before locking:

* the disruption remains Pending,
* the next recurrence retries automatically.

### Supervisor invocation failure

If the disruption was locked but the Supervisor failed to start:

* the record remains In Assessment,
* a monitoring process should detect stale assessments.

## Stale-assessment recovery

Recommended monitoring rule:

If:

* Status = In Assessment

and

* LastUpdated older than 30 minutes

then:

* route to Manual Review,
* notify the process owner.

This prevents permanently locked disruptions.

## Monitoring metrics

Recommended metrics:

### Trigger metrics

* recurrence executions,
* pending disruptions,
* disruptions selected,
* trigger failures.

### Processing metrics

* average processing time,
* successful completions,
* approval-required cases,
* manual-review cases.

### Queue metrics

* oldest pending disruption,
* queue length,
* average queue age.

## Trigger frequency recommendations

| Environment            | Frequency  |
| ---------------------- | ---------- |
| Development            | 15 minutes |
| Testing                | 10 minutes |
| Production             | 5 minutes  |
| High-volume production | 1 minute   |

## Power Automate implementation

### Trigger

Recurrence

### Actions

1. List rows from Excel
2. Filter Status = Pending
3. Sort by ReportedDate
4. Condition: rows exist
5. Update selected row
6. Invoke Copilot Studio
7. Log execution

## Example flow

```text
Recurrence
      │
List Rows
      │
Filter Pending
      │
Rows Exist?
      │
 ┌────┴────┐
 │         │
No        Yes
 │         │
End    Sort Oldest
           │
           ▼
      Update Status
           │
           ▼
      Invoke Supervisor
           │
           ▼
      End
```

## Logging

Each trigger execution should record:

* execution time,
* selected disruption,
* previous status,
* updated status,
* Supervisor invocation result.

This supports operational monitoring and auditability.

## Security considerations

The trigger should use a dedicated service account with access to:

* Excel Online (Business)
* Copilot Studio
* OneDrive for Business

The trigger should not use personal credentials.

## Future enhancements

The trigger architecture can later support:

* event-driven triggers,
* SharePoint triggers,
* Dataverse triggers,
* SAP events,
* Azure Event Grid,
* supplier portal integration,
* IoT disruption events,
* transportation disruption events.

The Supervisor architecture remains unchanged.

## Success criteria

The autonomous trigger is successful when it:

* runs without manual intervention,
* detects pending disruptions,
* selects exactly one disruption,
* prevents duplicate processing,
* locks the disruption immediately,
* invokes the Supervisor reliably,
* preserves execution traceability,
* supports safe recovery from failures.

## Conclusion

The autonomous trigger provides the continuous monitoring and execution foundation of the NovaSphere Supply Continuity Autonomous Multi-Agent System.

By combining recurrence scheduling, deterministic disruption selection, duplicate prevention, and controlled Supervisor invocation, the trigger enables reliable autonomous disruption response while preserving enterprise governance and operational traceability.
