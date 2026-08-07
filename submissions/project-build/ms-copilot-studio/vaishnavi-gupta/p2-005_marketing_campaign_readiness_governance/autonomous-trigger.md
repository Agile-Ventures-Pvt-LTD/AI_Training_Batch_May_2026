# Autonomous Trigger

## 1. Purpose

The P2-005 solution must start autonomously using a **Recurrence event trigger configured directly in Microsoft Copilot Studio**.

The trigger is responsible for initiating the campaign-readiness workflow without requiring a separate Power Automate workflow. fileciteturn11file0L73-L85

---

## 2. Trigger Type

**Trigger:** Recurrence event trigger

**Platform:** Microsoft Copilot Studio

The recurrence interval may be configured to a short interval during development and testing. fileciteturn11file0L73-L76

The implementation must **not require a separate Power Automate recurrence workflow**. fileciteturn11file0L83-L85

---

## 3. Trigger Responsibilities

Every recurrence execution must:

1. Retrieve campaign requests from Excel.
2. Identify campaigns where `CampaignStatus = Pending`.
3. Select the oldest eligible Pending campaign.
4. Process only one campaign during that trigger execution.
5. Update the selected campaign's status before specialist analysis begins.

fileciteturn11file0L77-L84

---

## 4. Trigger Flow

```text
Recurrence Event
       ↓
Retrieve Campaign Requests
       ↓
Find CampaignStatus = Pending
       ↓
Select Oldest Eligible Campaign
       ↓
One Campaign Only
       ↓
Update Status
       ↓
Campaign Intake & Validation
       ↓
Specialist Assessment
```

The trigger must not directly skip the intake and validation stage.

---

## 5. Campaign Selection Logic

The trigger must identify all eligible campaigns with:

```text
CampaignStatus = Pending
```

From the eligible records, it must select the **oldest Pending campaign**. fileciteturn11file0L77-L82

Conceptually:

```text
Campaign Requests
       ↓
Filter:
CampaignStatus = Pending
       ↓
Sort by age / oldest eligible record
       ↓
Select first campaign
```

Only one campaign is processed per recurrence execution.

---

## 6. Duplicate Prevention

Processing only one Pending campaign per trigger execution and updating its status before specialist analysis begins prevents duplicate concurrent assessment. fileciteturn11file0L81-L84

The campaign state model must be respected.

Valid states include:

- `Pending`
- `In Assessment`
- `Awaiting Remediation`
- `Awaiting Approval`
- `Ready with Conditions`
- `Ready`
- `Not Ready`
- `Manual Review`
- `Completed`

fileciteturn11file0L86-L108

The system must prevent invalid progression such as:

```text
Pending → Ready
```

without completing the required assessment. fileciteturn11file0L109-L112

---

## 7. Excel Integration

The operational workbook must be accessible through **Excel Online (Business)**, with the workbook stored in OneDrive for Business or SharePoint. fileciteturn11file7L1025-L1027

The solution uses appropriate Excel actions to:

- List campaign rows
- Retrieve relevant rules
- Retrieve assets
- Retrieve channel requirements
- Retrieve stakeholders
- Update campaign status

fileciteturn11file7L1028-L1036

`CampaignID` should be used as the primary logical key where applicable. fileciteturn11file7L1035-L1037

---

## 8. Recommended Trigger Execution Sequence

```text
1. Recurrence Trigger
          ↓
2. List Campaign Requests
          ↓
3. Filter Pending Campaigns
          ↓
4. Select Oldest Eligible Campaign
          ↓
5. Update Campaign Status
          ↓
6. Campaign Intake & Validation
          ↓
7. Supervisor Orchestration
          ↓
8. Specialist Assessments
```

The trigger itself is the autonomous entry point; the Supervisor and topics control the subsequent assessment workflow.

---

## 9. No Pending Campaign Scenario

If no campaign has:

```text
CampaignStatus = Pending
```

the trigger must exit safely without processing a campaign.

This is a mandatory failure/edge scenario in the PRD:

**TC-22 — No Pending campaign exists → Trigger exits safely without processing.** fileciteturn11file5L773-L779

Expected behaviour:

```text
Recurrence
    ↓
List Campaign Requests
    ↓
No Pending Campaign
    ↓
Exit Safely
```

The trigger must not invent a campaign or process a campaign in another state.

---

## 10. Missing Campaign Data

The overall implementation must handle missing campaign information and missing Excel rows. fileciteturn11file5L687-L700

If the selected campaign cannot provide the information required by the intake validation stage, the workflow must not proceed as if validation succeeded.

The agent must not fabricate successful completion. fileciteturn11file5L687-L700

---

## 11. Trigger and Intake Relationship

The recurrence trigger selects the campaign; the **Campaign Intake & Validation** topic performs deterministic validation.

```text
Recurrence Trigger
       ↓
Select Oldest Pending Campaign
       ↓
Campaign Intake & Validation
       ↓
Validation Passed?
     /          No         Yes
   ↓           ↓
Hold/Stop   In Assessment
               ↓
       Specialist Assessment
```

This separation keeps the autonomous trigger focused on campaign selection and the intake topic focused on validation.

---

## 12. Supervisor Relationship

After the trigger starts the workflow, the Supervisor controls the multi-agent process.

The Supervisor owns:

- Overall orchestration
- Final readiness classification
- Conflict resolution
- Reassessment decision
- Final Word generation authorization
- Outlook communication authorization

Child agents return findings rather than independently announcing final decisions. fileciteturn11file0L113-L120

---

## 13. Trigger-to-Specialist Architecture

```text
                 Recurrence Trigger
                         ↓
              Excel Campaign Requests
                         ↓
              Oldest Pending Campaign
                         ↓
              Campaign Intake & Validation
                         ↓
                     Supervisor
                         ↓
          +--------------+--------------+
          |              |              |
          ↓              ↓              ↓
       Budget          Brand         Channel
          |              |              |
          +--------------+--------------+
                         ↓
                       Asset
                         ↓
                       Fan-In
                         ↓
                Risk & Decision
                         ↓
                Supervisor Validation
```

The four domain specialists are independent assessments, followed by fan-in consolidation and the sequential Risk & Decision stage. fileciteturn11file6L964-L1008

---

## 14. Trigger Error Handling

The implementation must account for:

- No Pending campaigns
- Duplicate CampaignID
- Missing campaign information
- Missing Excel row
- Excel update delay/failure

fileciteturn11file5L687-L700

The trigger must never claim that processing succeeded if the required Excel operation failed.

---

## 15. Testing the Autonomous Trigger

The PRD includes the following trigger-related mandatory tests:

### TC-01 — Valid Pending Campaign

Expected:

```text
Recurrence
→ Select Pending Campaign
→ Validate
→ Proceed to Specialist Stage
```

### TC-02 — Campaign Already Completed

Expected:

```text
Recurrence
→ Completed campaign excluded
→ No duplicate assessment
```

### TC-22 — No Pending Campaign

Expected:

```text
Recurrence
→ No eligible campaign
→ Safe exit
```

fileciteturn11file5L742-L779

---

## 16. Evidence and Screenshot

The required GitHub structure includes:

```text
screenshots/
└── recurrence-trigger.png
```

fileciteturn11file1L203-L218

The screenshot should demonstrate the actual Recurrence event trigger configured in Microsoft Copilot Studio.

The test report should record the trigger execution along with:

- Test Case ID
- Campaign ID
- Trigger execution
- Topic invoked
- Child agents invoked
- Pattern demonstrated
- Expected result
- Actual result
- Final status
- Pass/Fail
- Failure reason
- Retest result
- Screenshot reference

fileciteturn11file5L780-L820

---

## 17. Key Implementation Rules

1. Use a **Recurrence event trigger directly in Microsoft Copilot Studio**.
2. Do not build a separate Power Automate recurrence workflow.
3. Retrieve campaigns from Excel.
4. Filter for `CampaignStatus = Pending`.
5. Select the oldest eligible Pending campaign.
6. Process only one campaign per trigger execution.
7. Update its status before specialist analysis.
8. Use `CampaignID` as the logical campaign identifier where applicable.
9. Exit safely when no Pending campaign exists.
10. Do not fabricate campaign data or successful execution.
11. Pass the selected campaign into the Intake & Validation stage.
12. Let the Supervisor control subsequent specialist orchestration.

These rules directly implement the autonomous-trigger requirements of the P2-005 PRD. fileciteturn11file0L73-L85
