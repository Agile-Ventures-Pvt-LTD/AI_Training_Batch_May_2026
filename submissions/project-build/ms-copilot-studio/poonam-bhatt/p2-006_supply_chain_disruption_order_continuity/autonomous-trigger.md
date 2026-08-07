# Autonomous Trigger Design

## Trigger Mechanism
To achieve fully autonomous operation without conversational messages, the system uses a **Recurrence event trigger** inside Microsoft Copilot Studio. During production execution, this runs on a scheduled interval (e.g., every 15 minutes). During testing, a shorter interval (e.g., 1 minute) is configured.

```
       [Recurrence Event Trigger] (Every N minutes)
                   │
                   ▼
       [Query DisruptionRequestsTable] (Filter: Status = 'Pending')
                   │
                   ▼
       [Select Oldest Record] (Process exactly one)
                   │
                   ▼
    [Lock Status to 'In Assessment'] (Write back to Excel)
                   │
                   ▼
    [Invoke Intake & Validation Topic]
```

## Row Selection & Locking
On each trigger execution, the Supervisor agent performs the following steps:
1. **Query**: Calls the Excel Online (Business) connector to list rows from the `DisruptionRequestsTable` in OneDrive or SharePoint.
2. **Filter**: Applies a OData filter query: `Status eq 'Pending'`.
3. **Sort/Select**: Sorts the returned array by `ReportedDate` ascending and selects the first (oldest) record:
   ```text
   Record = First(Sort(Filter(DisruptionRequestsTable, Status = "Pending"), ReportedDate, Ascending))
   ```
4. **Locking**: Immediately calls the Excel Online (Business) connector to update the status of the selected `DisruptionID` from `Pending` to `In Assessment`. This state lock prevents subsequent triggers from picking up the same record while the multi-agent assessment is running, guaranteeing that exactly one disruption is processed per run and avoiding duplicate processing.
5. **Topic Transition**: Once the record is locked, the Supervisor transfers control and the record variables to the **Disruption Intake & Validation** topic.
