# Custom Topics

## 1. Overview

The P2-005 solution requires **three mandatory custom topics** in Microsoft Copilot Studio:

1. **Campaign Intake & Validation**
2. **Remediation & Selective Reassessment**
3. **Approval & Finalisation**

These topics support deterministic validation, remediation and reassessment, and mandatory human-approval handling. The PRD explicitly requires these three topics. fileciteturn10file1L205-L314

---

# 2. Custom Topic 1 — Campaign Intake & Validation

## 2.1 Purpose

Perform deterministic pre-assessment validation **before child agents are invoked**. fileciteturn10file1L205-L209

## 2.2 Required Validations

The topic must validate:

- Campaign ID exists.
- Campaign ID is unique.
- Campaign status is `Pending`.
- Campaign name exists.
- Product exists.
- Launch date exists.
- Launch date is not in the past.
- Budget values exist.
- Geography exists.
- At least one channel exists.
- Campaign owner exists.

fileciteturn10file1L210-L221

## 2.3 Required Variables

Equivalent variables must include:

```text
CampaignID
CampaignName
Product
LaunchDate
DaysToLaunch
ProposedBudget
ApprovedBudget
BudgetVariance
TargetCPL
Geography
Channels
Sensitivity
CampaignOwner
ValidationStatus
DuplicateDetected
```

fileciteturn10file1L222-L238

## 2.4 Duplicate Handling

If the same campaign is already:

- `In Assessment`
- `Awaiting Remediation`
- `Awaiting Approval`
- `Completed`

the topic must not create a fresh assessment. fileciteturn10file1L265-L271

## 2.5 Expected Flow

```text
Campaign Received
      ↓
Retrieve Campaign Data
      ↓
Validate Required Fields
      ↓
Check Campaign Status
      ↓
Check Duplicate State
      ↓
Calculate DaysToLaunch / BudgetVariance
      ↓
Validation Passed?
   /           No            Yes
 ↓              ↓
Reject/Hold   Mark In Assessment
                 ↓
          Continue to Specialists
```

The topic must complete before specialist analysis begins. The PRD requires specialist analysis only after campaign validation. fileciteturn10file5L793-L800

---

# 3. Custom Topic 2 — Remediation & Selective Reassessment

## 3.1 Purpose

Coordinate remediation when one or more specialist assessments fail.

The PRD explicitly states that this must be a **complex topic**. fileciteturn10file1L272-L276

## 3.2 Required Logic

The topic must:

1. Receive all failed specialist domains.
2. Create remediation actions.
3. Identify the responsible owner.
4. Set `CampaignStatus` to `Awaiting Remediation`.
5. Preserve already-passed specialist results.
6. Detect when underlying data has been corrected.
7. Identify which specialist results are stale.
8. Rerun only affected specialists.
9. Re-enter Supervisor consolidation.
10. Recalculate final readiness.

fileciteturn10file1L277-L288

## 3.3 Selective Reassessment Example

If only a missing landing page is corrected:

```text
Missing Landing Page
        ↓
Remediation
        ↓
Landing Page Corrected
        ↓
Identify affected domain
        ↓
Rerun relevant Channel / Asset assessment
        ↓
Preserve unrelated Budget result
        ↓
Supervisor Consolidation
        ↓
Recalculate Readiness
```

The system must not automatically rerun every specialist when only one domain changed. fileciteturn10file1L289-L291

## 3.4 Loop Control

A campaign may undergo a maximum of **two automated reassessment cycles**.

After two unsuccessful cycles:

```text
Manual Review
```

must be assigned. fileciteturn10file1L292-L310

## 3.5 Expected Flow

```text
Blocking Specialist Finding
          ↓
Create Remediation Actions
          ↓
Identify Owner
          ↓
Awaiting Remediation
          ↓
Data Corrected?
      /              No            Yes
    ↓              ↓
Remain Waiting   Identify Stale Results
                     ↓
              Rerun Affected Specialists
                     ↓
              Supervisor Consolidation
                     ↓
              Recalculate Readiness
```

---

# 4. Custom Topic 3 — Approval & Finalisation

## 4.1 Purpose

Handle campaigns requiring mandatory human approval. fileciteturn10file1L311-L314

## 4.2 Required Approval Conditions

The topic must evaluate:

- Proposed budget > approved budget
- Proposed budget > INR 1,000,000
- Target CPL > INR 4,000
- High regulatory sensitivity
- Multi-market geography
- Restricted/quantified claims
- Urgent launch with unresolved approval

fileciteturn10file3L537-L549

## 4.3 Required Logic

The topic must:

1. Determine the required approver.
2. Prevent `Ready` status while approval is outstanding.
3. Record the approval reason.
4. Set state to `Awaiting Approval`.
5. Allow reassessment when approval data changes.
6. Return to the Supervisor.
7. Never fabricate a human approval.

fileciteturn10file3L550-L558

## 4.4 Expected Flow

```text
Approval Condition Detected
          ↓
Determine Required Approver
          ↓
Record Approval Reason
          ↓
Awaiting Approval
          ↓
Approval Received?
       /               No            Yes
     ↓              ↓
Remain Waiting   Return to Supervisor
                     ↓
              Final Validation
```

The topic must not assign `Ready` while mandatory approval remains outstanding.

---

# 5. Topic Relationship with Supervisor

The three topics operate under Supervisor orchestration.

```text
                    Supervisor
                        |
        +---------------+----------------+
        |               |                |
        v               v                v
     Intake         Remediation       Approval
   & Validation    & Reassessment   & Finalisation
        |               |                |
        +---------------+----------------+
                        |
                        v
                 Supervisor Control
```

The Supervisor owns:

- Overall orchestration
- Final readiness classification
- Conflict resolution
- Reassessment decision
- Final stakeholder communication authorization

Specialists and topics must operate within their assigned responsibilities. fileciteturn10file5L812-L830

---

# 6. Topic Routing

## Intake

```text
Recurrence Trigger
       ↓
Campaign Intake & Validation
       ↓
Valid?
       ↓
Specialist Assessment
```

## Remediation

```text
Specialist Block / Correctable Failure
       ↓
Remediation & Selective Reassessment
       ↓
Affected Specialist(s)
       ↓
Supervisor Consolidation
```

## Approval

```text
Approval Condition
       ↓
Approval & Finalisation
       ↓
Awaiting Approval
       ↓
Approval Received
       ↓
Supervisor
```

These routes support the required sequential, conditional, and reassessment orchestration patterns. fileciteturn10file5L791-L844

---

# 7. Topic Design Rules

All three topics must:

- Operate within Microsoft Copilot Studio.
- Use the required variables and campaign state.
- Return control to the Supervisor when their assigned work is complete.
- Preserve evidence and status information.
- Avoid fabricating approvals or assessment results.
- Respect the campaign state model.
- Avoid bypassing required validation or approval stages.

The PRD requires Copilot Studio topics, child agents, tools/connectors, event triggers, and generative orchestration for the core solution. fileciteturn10file4L685-L695

---

# 8. Relationship to Final Readiness

The topics do not replace the Supervisor's final decision authority.

The mandatory readiness precedence is:

```text
1. Not Ready
2. Management Approval Required
3. Remediation Required
4. Ready with Conditions
5. Ready
```

If multiple conditions apply, the highest-precedence outcome wins. Specialist results must not be averaged. fileciteturn10file3L559-L588

For example:

```text
Budget  = Pass
Channel = Pass
Assets  = Pass
Brand   = Block
```

The final status cannot be `Ready`. fileciteturn10file3L581-L588

---

# 9. Topic Evidence

The required GitHub screenshot structure includes:

```text
screenshots/
├── intake-topic.png
├── remediation-topic.png
└── approval-topic.png
```

These screenshots should demonstrate the actual configured topics in Copilot Studio. fileciteturn10file0L85-L97

The implementation should also provide test evidence showing:

- Topic invoked
- Child agents invoked
- Pattern demonstrated
- Specialist outputs
- Expected result
- Actual result
- Final status
- Pass/Fail
- Failure reason
- Remediation
- Retest result
- Screenshot reference

fileciteturn10file6L906-L922

---

# 10. Summary

| Custom Topic | Primary Responsibility | Main Pattern |
|---|---|---|
| Campaign Intake & Validation | Deterministic pre-assessment validation and duplicate/state handling | Sequential |
| Remediation & Selective Reassessment | Correct failed domains and rerun only affected specialists | Loop / Reassessment |
| Approval & Finalisation | Manage mandatory human approval and return to Supervisor | Conditional / Sequential |

Together, these three topics provide the required control points around the multi-agent assessment workflow while keeping final readiness ownership with the Campaign Readiness Supervisor.
