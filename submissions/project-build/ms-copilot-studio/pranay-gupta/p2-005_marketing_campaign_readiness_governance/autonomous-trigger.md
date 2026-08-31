# Autonomous Trigger

## 1. Trigger Type

The PRD requires a **Recurrence event trigger directly in Microsoft Copilot Studio**.

No separate Power Automate workflow is required for this trigger.

## 2. Trigger Flow

On each trigger:

1. Retrieve Campaign Requests from Excel.
2. Identify campaigns where `CampaignStatus = Pending`.
3. Select the oldest eligible Pending campaign.
4. Process only one campaign per trigger execution.
5. Update its status before specialist analysis begins.

## 3. Purpose of State Update

Moving the selected campaign out of Pending before specialist analysis prevents duplicate concurrent assessment.

## 4. Eligible States

Only:

```text
Pending
```

is eligible for a new autonomous assessment.

The system must not restart campaigns already in:

- In Assessment
- Awaiting Remediation
- Awaiting Approval
- Completed

## 5. Campaign State Model

| State | Meaning |
|---|---|
| Pending | Awaiting assessment |
| In Assessment | Autonomous assessment active |
| Awaiting Remediation | Blocking issues require correction |
| Awaiting Approval | Mandatory human approval outstanding |
| Ready with Conditions | Only permitted non-blocking conditions remain |
| Ready | All mandatory requirements satisfied |
| Not Ready | Launch cannot proceed |
| Manual Review | Insufficient evidence or unresolved system failure |
| Completed | Final assessment and communication completed |

