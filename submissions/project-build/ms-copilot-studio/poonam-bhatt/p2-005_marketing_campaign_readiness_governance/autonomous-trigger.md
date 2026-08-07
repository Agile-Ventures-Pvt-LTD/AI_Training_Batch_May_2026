# Autonomous Trigger Configuration

The Campaign Readiness system operates autonomously without manual human input, driven by a native event-based schedule.

## 1. Recurrence Trigger Setup
The Supervisor is configured with a **Recurrence Trigger** directly inside Copilot Studio:
*   **Event Type:** Time-based Scheduled Event (Recurrence).
*   **Interval:** Every 1 hour (can be set to a short interval like 10 minutes during testing/development).
*   **Authentication:** Set to **App-Only / Maker Authentication** (using service credentials) to run in the background without requiring user sign-in.

## 2. Row Lock & Concurrency Control
To prevent concurrent trigger executions from picking up the same campaign request twice, the Supervisor immediately runs the following locking sequence:
1.  **Read oldest pending campaign:** Runs `Get Pending Campaign` to query the OneDrive Excel workbook and retrieves the oldest row where `CampaignStatus = "Pending"`.
2.  **Lock Campaign Status:** Before triggering specialist analysis, the Supervisor runs `Record Campaign Assessment` to update `CampaignStatus` to `"In Assessment"`.
3.  **Process Single Campaign:** The trigger processes exactly **one campaign per execution cycle**, preventing overlap.
