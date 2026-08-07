# Autonomous Recurrence Trigger — Configuration Specifications

## Purpose
The Supply Continuity System operates autonomously without requiring manual user initiation via chat. This is achieved using a **Recurrence Event Trigger** configured within Microsoft Copilot Studio.

## Trigger Configuration Details
- **Trigger Type:** Recurrence / Scheduled Copilot Event.
- **Interval:** Every 5 Minutes (or 15 Minutes for production deployment).
- **Target Copilot:** `Supply Continuity Supervisor`.
- **Generative Orchestration:** Enabled.

## Trigger Payload Instruction Prompt
```text
Check the DisruptionRequestsTable in Excel for the oldest record where Status is 'Pending'. If a Pending record is found, immediately update its Status to 'In Assessment' and begin the autonomous supply chain disruption assessment lifecycle. If no Pending record exists, exit safely without taking action.
```

## Autonomous Workflow Step-by-Step
1. **Timer Fires:** Every 5 minutes, Copilot Studio invokes the `Supply Continuity Supervisor`.
2. **Scan Excel:** Reads `DisruptionRequestsTable` in `P2-006_Supply_Chain_Continuity_Lab_Data.xlsx` stored in OneDrive.
3. **Filter Pending:** Selects oldest record where `Status = "Pending"`.
4. **Immediate Status Lock:** Updates `Status` to `"In Assessment"` to prevent duplicate processing during subsequent recurrence ticks.
5. **Execution:** Automatically triggers the 4 parallel specialists, fan-in consolidation, recovery planning, topic validation, Word report creation, and Outlook notification dispatch.
6. **No Pending Exit:** If zero `Pending` records exist, the trigger completes in <500ms without sending messages or modifying state.
