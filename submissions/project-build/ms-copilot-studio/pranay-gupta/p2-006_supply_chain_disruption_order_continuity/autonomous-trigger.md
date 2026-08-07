# Autonomous Trigger

## Trigger
Microsoft Copilot Studio Recurrence event trigger.

## Required Behaviour
1. Read `Disruption_Requests`.
2. Find records where `Status = Pending`.
3. Select the oldest Pending disruption.
4. Process one disruption per trigger run.
5. Immediately update the selected record to `In Assessment`.
6. Continue validation and assessment.

## No Pending Disruption
Exit safely without invoking specialists.

## State Model
| State | Meaning |
|---|---|
| Pending | Awaiting assessment |
| In Assessment | Multi-agent assessment active |
| Awaiting Approval | Human approval required |
| Recovery Plan Proposed | Valid strategy identified |
| Customer Action Required | Customer-date or fulfilment decision required |
| Management Escalation | No safe/approved autonomous resolution |
| Insufficient Evidence | Required data or specialist result missing |
| Manual Review | Automated reassessment exhausted |
| Completed | Reporting and notification complete |

Invalid transitions must be prevented.

No separate Power Automate workflow is required by the PRD.
