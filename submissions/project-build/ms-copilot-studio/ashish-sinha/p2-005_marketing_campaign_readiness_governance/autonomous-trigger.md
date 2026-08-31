# ⏱️ Autonomous Trigger Configuration

---

## 📖 Overview

The P2-005 Marketing Campaign Launch Readiness & Governance System is designed to operate fully autonomously without manual intervention. This autonomy is achieved by configuring a **Recurrence Event Trigger** directly within Microsoft Copilot Studio. 

The trigger acts as the initiator for the orchestration flow, scheduling periodic checks to identify and process new campaign requests.

---

## ⚙️ Trigger Configuration Details

| Parameter | Value | Description |
|-----------|-------|-------------|
| **Trigger Type** | Recurrence (Event-based) | Executes the supervisor flow on a scheduled interval. |
| **Development Interval** | Every 5 Minutes | Configured for rapid testing and validation of campaign states. |
| **Production Interval** | Every 30 Minutes | Standard operational cadence to assess campaign batches. |
| **Orchestration Mode** | Generative Orchestration | Required for event triggers to invoke corresponding topics dynamically. |

---

## 🛠️ Campaign Selection & Processing Logic

On every trigger execution, the Campaign Readiness Supervisor executes the following logic:

1. **Excel Query**: Retrieves rows from the `Campaign_Requests` table in Excel Online (Business).
2. **Status Filtering**: Identifies campaign requests where `CampaignStatus = "Pending"`.
3. **Queue Sorting**: Sorts the eligible pending campaigns by `SubmissionDate` in ascending order to process the oldest request first.
4. **Single campaign limit**: Processes exactly one campaign per trigger execution to optimize resource usage and prevent race conditions.
5. **State Transition**: Immediately updates the status of the selected campaign to `In Assessment` in the Excel spreadsheet before launching parallel specialist assessments. This prevents duplicate processing on subsequent trigger runs.

---

## 📸 Recurrence Trigger Screenshot

Below is the configuration screenshot demonstrating the event recurrence trigger inside Microsoft Copilot Studio:

![Recurrence Trigger Configuration](/screenshots/recurrence-trigger.png)

---

## 🔗 Integration with Intake Topic

Once triggered and the target campaign is selected, the flow hands off execution to the **Campaign Intake & Validation** topic. The supervisor passes the campaign variables down to begin verification.
