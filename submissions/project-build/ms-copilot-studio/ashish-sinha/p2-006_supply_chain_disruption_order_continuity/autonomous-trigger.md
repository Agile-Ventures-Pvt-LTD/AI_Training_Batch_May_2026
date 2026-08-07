# Autonomous Trigger

![Recurring Copilot Trigger Configuration](screenshots/recurrence_agent.png)

## Objective
Start the supply disruption workflow autonomously without requiring a user to initiate a chat.

## Trigger behavior
The trigger should identify an eligible disruption request in the operational register, select a Pending record, and hand it to the Supply Continuity Supervisor.

## Required protections
- Select a Pending disruption.
- Prevent duplicate processing.
- Do not process a record already In Assessment, Awaiting Approval, Manual Review, or Completed.
- If no Pending disruption exists, exit safely.

## Expected sequence
```text
Recurrence/Event Trigger
→ Find eligible Pending disruption
→ Supervisor receives disruption context
→ Topic 1 validates record
→ Valid → In Assessment
→ Invalid → hold/stop
```

## Data
The operational workbook must be stored in OneDrive for Business or SharePoint and accessed through Excel Online (Business).

## No-pending behavior
If no Pending record exists:
- do not fabricate a disruption
- do not invoke specialists
- exit safely
- record/log the no-work condition where supported

## Duplicate protection
Before processing, verify the record state. A record must not be simultaneously processed as a new Pending disruption and as an active assessment.

## Trigger acceptance criteria
- recurrence/event trigger configured
- Pending record identified autonomously
- duplicate protection demonstrated
- validation invoked before specialist work
