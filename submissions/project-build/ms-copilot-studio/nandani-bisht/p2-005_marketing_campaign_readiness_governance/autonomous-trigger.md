# Autonomous Trigger

## Project

**Marketing Campaign Readiness Governance**

---

# Overview

The Marketing Campaign Readiness Governance solution includes an **Autonomous Scheduled Trigger** that automatically monitors the campaign data source and initiates the readiness assessment workflow without requiring manual user interaction.

The trigger enables continuous campaign governance by periodically checking for new or pending campaign requests and invoking the Campaign Readiness Supervisor whenever a campaign requires assessment.

---

# Purpose

The autonomous trigger eliminates the need for users to manually start the campaign readiness process.

Its responsibilities include:

- Periodically checking campaign records.
- Detecting campaigns that require assessment.
- Automatically invoking the Campaign Readiness Supervisor.
- Preventing unnecessary execution.
- Supporting continuous campaign governance.

---

# Trigger Type

The implementation uses:

**Scheduled Trigger**

within Microsoft Copilot Studio.

The trigger executes automatically at predefined intervals.

Example:

- Every Hour
- Every Day
- Every Morning

The schedule can be adjusted according to business requirements.

---

# Trigger Workflow

```
Scheduled Trigger
        │
        ▼
Read CampaignRequestsTable
        │
        ▼
Find Pending Campaigns
        │
        ▼
Campaign Found?
   ┌──────────────┐
   │              │
  No             Yes
   │              │
   ▼              ▼
Stop        Invoke Supervisor
                    │
                    ▼
      Campaign Intake & Validation
                    │
                    ▼
          Specialist Assessments
                    │
                    ▼
      Remediation / Approval
                    │
                    ▼
        Final Readiness Decision
                    │
                    ▼
        Update Campaign Status
```

---

# Trigger Conditions

The scheduled trigger identifies campaigns that satisfy the following conditions:

- Campaign Status = Pending
- Campaign has not been processed
- Campaign contains required identifiers
- Campaign is available for assessment

Only campaigns matching these conditions are passed to the Campaign Readiness Supervisor.

---

# Trigger Inputs

The trigger retrieves campaign information from the Excel data source.

Typical fields include:

- Campaign ID
- Campaign Name
- Campaign Status
- Product
- Budget
- Geography
- Campaign Owner

---

# Trigger Output

The trigger passes the Campaign ID to the Campaign Readiness Supervisor.

The Supervisor then performs:

- Validation
- Specialist Assessment
- Approval Evaluation
- Remediation (if required)
- Final Readiness Decision

---

# Campaign Processing Sequence

```
Trigger Fires

↓

Read Excel

↓

Pending Campaign?

↓

Yes

↓

Campaign Readiness Supervisor

↓

Topic 1

↓

Specialist Agents

↓

Topic 2 (If Needed)

↓

Topic 3 (If Needed)

↓

Final Status

↓

Update Excel

↓

Finish
```

---

# Status Updates

During processing, the campaign status transitions through different workflow stages.

```
Pending

↓

In Assessment

↓

Awaiting Remediation

OR

Awaiting Approval

↓

Manual Review

↓

Ready
```

Each transition is written back to the Excel table to maintain a complete audit trail.

---

# Duplicate Prevention

Before invoking the Supervisor, the trigger ensures that duplicate assessments are not started.

Campaigns already in one of the following states are skipped:

- In Assessment
- Awaiting Remediation
- Awaiting Approval
- Completed

This prevents multiple assessment workflows from running simultaneously for the same campaign.

---

# Error Handling

The trigger handles common processing issues.

Examples include:

## Campaign Not Found

The workflow stops without invoking the Supervisor.

---

## Missing Campaign ID

The campaign is ignored and logged for review.

---

## Invalid Campaign Status

Only campaigns in the **Pending** state are processed.

---

## Data Source Unavailable

The trigger retries during the next scheduled execution.

---

# Advantages

The autonomous trigger provides:

- Fully automated campaign processing
- Continuous governance
- Reduced manual intervention
- Faster readiness assessment
- Consistent execution
- Better operational efficiency

---

# Current Implementation

The current implementation includes:

- Scheduled Trigger in Microsoft Copilot Studio
- Excel Online (Business) integration
- Campaign Readiness Supervisor invocation
- Automatic campaign status updates
- Integration with all three custom topics
- Integration with six specialist agents

---

# Future Enhancements

The trigger can be extended to support:

- Dataverse as the primary data source
- SharePoint Lists
- SQL Database
- Power Automate event triggers
- Microsoft Forms submissions
- Teams notifications
- Email notifications
- Event-driven execution instead of polling

---

# Conclusion

The Autonomous Scheduled Trigger acts as the entry point of the Marketing Campaign Readiness Governance solution. By automatically detecting pending campaigns and invoking the Campaign Readiness Supervisor, it enables continuous, scalable, and reliable campaign governance while minimizing manual effort and ensuring timely readiness assessments.