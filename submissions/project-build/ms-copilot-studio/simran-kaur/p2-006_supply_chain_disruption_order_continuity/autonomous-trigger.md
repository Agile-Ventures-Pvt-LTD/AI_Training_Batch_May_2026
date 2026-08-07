# Autonomous Trigger Design

This document details the configuration, logic flow, and execution parameters of the Recurrence event trigger that drives the autonomous behavior of the multi-agent system.

---

## 1. Recurrence Trigger Configuration
The Supply Continuity Supervisor Agent is configured to start autonomously using a **Recurrence event trigger** within Microsoft Copilot Studio. This allows the system to monitor and process disruptions without requiring a conversational user message.

* **Interval**: Configured to run every **5 minutes** (in production, this can be set hourly or daily depending on disruption volume).
* **Target Data Table**: `DisruptionRequestsTable` in Excel Online.
* **Orchestration Setting**: **Generative Orchestration** must be enabled on the Copilot Studio agent to allow the supervisor to coordinate custom topics, variables, and child agents dynamically.

---

## 2. Trigger Logic Flow

The trigger executes the following sequence to ingest and process a single disruption request:

```
[Trigger Fires]
       │
       ▼
[Query DisruptionRequestsTable] ➔ (Filter where Status = 'Pending')
       │
       ├──(If No Records Found) ➔ [Exit Safely (TC-24)]
       │
       └──(If Records Found)
             │
             ▼
      [Select Oldest Row] ➔ (Based on ReportedDate / Timestamp)
             │
             ▼
   [Immediate Database Update] ➔ (Write Status = 'In Assessment')
             │
             ▼
  [Pass DisruptionID to Supervisor] ➔ [Invoke Intake & Validation Topic]
```

### Key Logic Steps:
1. **Query**: The trigger queries the `DisruptionRequestsTable` using the Excel Online connector.
2. **Filter**: It filters the rows where `Status` is exactly equal to `Pending`.
3. **Queue Prioritization**: To ensure fairness and traceability, the system selects the **oldest single record** based on the reported timestamp.
4. **Single-Record Locking**: The trigger processes **only one record per run**. This prevents race conditions, database locks, or API rate-limiting issues.
5. **Immediate State Transition**: The selected record's status is immediately updated to `In Assessment` in the Excel sheet before executing downstream logic. This prevents duplicate trigger runs from grabbing the same record.
6. **Supervisor Hand-off**: The `DisruptionID` is mapped to a global variable, and the validation stage is initiated.

---

## 3. Trigger Variable Mapping

The following variables are initialized by the trigger action and passed to the main orchestration flow:

| Variable Name | Type | Source Column (Excel) | Description |
|---|---|---|---|
| `TriggerDisruptionID` | String | `DisruptionID` | The unique ID of the selected row. |
| `TriggerStatus` | String | `Status` | Initial value must be `Pending`. Updated immediately to `In Assessment`. |
| `TriggerTimestamp` | DateTime | `ReportedDate` | Used for prioritizing the oldest record in the queue. |
