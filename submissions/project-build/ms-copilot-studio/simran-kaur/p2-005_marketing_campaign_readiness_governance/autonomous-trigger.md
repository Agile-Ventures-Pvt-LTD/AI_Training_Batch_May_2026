# Autonomous Trigger

## Trigger
Use a Microsoft Copilot Studio **Recurrence** event trigger.

## Processing rules
On each trigger:
1. Retrieve campaign requests from Excel.
2. Identify campaigns where `CampaignStatus = Pending`.
3. Select the oldest eligible Pending campaign.
4. Process only one campaign per trigger execution.
5. Update its status before specialist analysis begins.
6. Continue through the Supervisor orchestration.

## Duplicate prevention
Changing the selected campaign to `In Assessment` before specialist analysis prevents duplicate concurrent assessment of the same Pending campaign.

## No Pending campaign
If no eligible Pending campaign exists, exit safely without processing a campaign.

## Implementation constraint
No separate Power Automate workflow is required for the recurrence mechanism.

## Evidence
Replace `screenshots/recurrence-trigger.png` with the actual Copilot Studio trigger configuration.
