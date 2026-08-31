# Custom topics

## Overview

The **Autonomous Marketing Campaign Launch Readiness & Governance System** uses three custom topics to implement deterministic workflow control in Microsoft Copilot Studio.

These topics provide the orchestration layer that connects the **Campaign Readiness Supervisor** with the specialist child agents and operational data stored in Excel Online (Business).

The implemented custom topics are:

1. **Campaign Intake & Validation**
2. **Remediation & Selective Reassessment**
3. **Approval & Finalization**

These topics collectively implement the mandatory orchestration patterns required by the project:

* Sequential execution
* Conditional routing
* Selective reassessment
* Loop control
* Governance validation

---

# Topic 1: Campaign Intake & Validation

## Purpose

This topic performs deterministic pre-assessment validation before any specialist child agent is invoked.

Its objective is to ensure that only valid campaigns enter the autonomous assessment workflow.

## Invocation

**Invoked by:** Campaign Readiness Supervisor

**Trigger:** Internal topic invocation only

## Inputs

* CampaignID

## Outputs

* ValidationStatus
* DuplicateDetected
* Campaign
* DaysToLaunch
* ValidationErrors

## Validation checks

The topic validates:

* Campaign ID exists
* Campaign ID is unique
* Campaign status is Pending
* Campaign name exists
* Product exists
* Launch date exists
* Launch date is not in the past
* Proposed budget exists
* Approved budget exists
* Geography exists
* At least one channel exists
* Campaign owner exists

## Duplicate handling

The topic prevents duplicate assessment when the campaign is already in:

* In Assessment
* Awaiting Remediation
* Awaiting Approval
* Completed

Duplicate campaigns are returned to the Supervisor without creating a new assessment.

## Workflow

```text
Receive CampaignID
        |
        v
Retrieve Campaign
        |
        v
Campaign Exists?
        |
        v
Duplicate Check
        |
        v
Mandatory Field Validation
        |
        v
Launch Date Validation
        |
        v
Budget Validation
        |
        v
Validation Result
```

## Failure behavior

If validation fails:

* ValidationStatus = Invalid
* CampaignStatus = Not Ready
* FinalReadiness = Not Ready
* ValidationErrors populated
* Specialist execution prevented

## Success behavior

If validation succeeds:

* ValidationStatus = Valid
* DuplicateDetected = false
* DaysToLaunch calculated
* Validated campaign object returned
* Supervisor proceeds to specialist assessment

---

# Topic 2: Remediation & Selective Reassessment

## Purpose

Coordinate remediation for campaigns with correctable governance failures.

The topic preserves successful specialist assessments and reruns only the specialist domains affected by corrected data.

## Invocation

**Invoked by:** Campaign Readiness Supervisor

**Trigger:** Internal topic invocation only

## Inputs

* CampaignID
* BudgetResult
* BrandResult
* ChannelResult
* AssetResult
* ReassessmentCount

## Outputs

* UpdatedBudgetResult
* UpdatedBrandResult
* UpdatedChannelResult
* UpdatedAssetResult
* ReassessmentCompleted
* ManualReviewRequired

## Core responsibilities

The topic:

* Identifies failed specialist domains
* Creates remediation actions
* Identifies responsible owners
* Updates campaign status
* Increments reassessment count
* Detects corrected data
* Selectively reruns affected specialists
* Returns updated specialist results

## Remediation actions

### Budget

* Reduce budget
* Obtain approval
* Update approved budget

### Brand

* Correct disclaimers
* Remove unsupported claims
* Update product naming

### Channel

* Configure tracking
* Add required channel assets
* Resolve lead-time issues

### Asset

* Create missing assets
* Complete QA
* Obtain approvals
* Update asset status

## Selective reassessment logic

The topic intentionally avoids rerunning every specialist.

### Example 1: Landing page corrected

Rerun:

* Asset Specialist
* Channel Specialist

Do not rerun:

* Budget Specialist
* Brand Specialist

### Example 2: Budget approval obtained

Rerun:

* Budget Specialist only

### Example 3: Brand disclaimer corrected

Rerun:

* Brand Specialist only

### Example 4: Tracking configured

Rerun:

* Channel Specialist only

## Workflow

```text
Remediation Required
        |
        v
Create Remediation Actions
        |
        v
Update Awaiting Remediation
        |
        v
Detect Corrected Data
        |
        v
Selective Specialist Invocation
        |
        v
Return Updated Results
```

## Loop control

Maximum automated reassessment cycles:

**2**

After two unsuccessful cycles:

* CampaignStatus = Manual Review
* FinalReadiness = Manual Review
* ManualReviewRequired = true
* Automated reassessment stops

---

# Topic 3: Approval & Finalization

## Purpose

Handle campaigns requiring mandatory human approval before launch readiness can be assigned.

This topic ensures that governance approvals are enforced and never fabricated.

## Invocation

**Invoked by:** Campaign Readiness Supervisor

**Trigger:** Internal topic invocation only

## Inputs

* CampaignID
* ProposedBudget
* ApprovedBudget
* TargetCPL
* Sensitivity
* Geography
* PendingApprovals

## Outputs

* ApprovalRequired
* RequiredApprover
* ApprovalReason
* ApprovalCompleted
* ReturnToSupervisor

## Approval conditions

The topic evaluates:

* Proposed budget greater than approved budget
* Proposed budget greater than INR 1,000,000
* CPL greater than INR 4,000
* High regulatory sensitivity
* Multi-market geography
* Restricted or quantified claims
* Urgent launch with unresolved approval

## Approval routing

Determine the appropriate approver:

* Marketing Director
* VP Marketing
* Regional Marketing Lead
* Executive approver

based on governance policy.

## Workflow

```text
Approval Evaluation
        |
        v
Approval Required?
      /   \
     /     \
   No       Yes
   |         |
   |         v
   |    Determine Approver
   |         |
   |         v
   |    Record Approval Reason
   |         |
   |         v
   |    Awaiting Approval
   |         |
   |         v
   +---- Supervisor
```

## Approval behavior

If approval is required:

* CampaignStatus = Awaiting Approval
* FinalReadiness cannot be Ready
* Approval reason recorded
* Supervisor notified

## Approval completion

When approval data changes:

* Approval is revalidated
* Budget Specialist may be rerun
* Risk Specialist is invoked
* Supervisor recalculates readiness

## Governance rule

The topic never fabricates:

* Approval decisions
* Approver responses
* Approval completion

Human approval must be explicitly available before the campaign can proceed.

---

# Topic interaction architecture

## Initial assessment

```text
Supervisor
      |
      v
Campaign Intake & Validation
      |
      v
Specialist Agents
```

## Remediation path

```text
Supervisor
      |
      v
Remediation & Selective Reassessment
      |
      v
Affected Specialists
      |
      v
Supervisor
```

## Approval path

```text
Supervisor
      |
      v
Approval & Finalization
      |
      v
Approval Status
      |
      v
Supervisor
```

---

# Shared variable management

## Campaign variables

* CampaignID
* CampaignStatus
* FinalReadiness
* DaysToLaunch
* Geography
* Sensitivity
* ReassessmentCount

## Specialist variables

* BudgetResult
* BrandResult
* ChannelResult
* AssetResult
* RiskResult

## Governance variables

* ApprovalRequired
* RequiredApprover
* RequiredActions
* BlockingIssues
* Conditions

---

# Excel integration

The topics interact with **CampaignRequestsTable** to manage operational state.

## Campaign Intake & Validation

Reads:

* Campaign_Requests

Updates:

* CampaignStatus
* FinalReadiness

## Remediation & Selective Reassessment

Reads:

* Campaign_Requests
* Asset_Status

Updates:

* CampaignStatus
* ReassessmentCount

## Approval & Finalization

Reads:

* Campaign_Requests
* Approval_Matrix

Updates:

* CampaignStatus
* ApprovalReason

---

# Error handling

## Campaign Intake & Validation

Handles:

* Missing campaign
* Duplicate processing
* Invalid campaign state
* Missing mandatory fields
* Invalid launch date

## Remediation & Selective Reassessment

Handles:

* Reassessment limit reached
* Missing corrected data
* Specialist reassessment failure
* Unresolved remediation

## Approval & Finalization

Handles:

* Missing approver
* Approval still pending
* Approval data unavailable
* Governance escalation

---

# Orchestration contribution

| Topic                                | Sequential | Conditional | Loop |
| ------------------------------------ | ---------- | ----------- | ---- |
| Campaign Intake & Validation         | Yes        | Yes         | No   |
| Remediation & Selective Reassessment | Yes        | Yes         | Yes  |
| Approval & Finalization              | Yes        | Yes         | No   |

---

# End-to-end topic flow

```text
Pending Campaign
        |
        v
Campaign Intake & Validation
        |
        v
Specialist Assessments
        |
        v
Supervisor Validation
        |
        +------------------+
        |                  |
        v                  v
Approval Topic       Remediation Topic
        |                  |
        +--------+---------+
                 |
                 v
Risk Recalculation
                 |
                 v
Final Readiness
                 |
                 v
Reporting & Communication
```

## Conclusion

The custom topics provide the deterministic workflow control required for autonomous campaign governance. They ensure that campaigns are validated before assessment, corrected efficiently through selective reassessment, routed through mandatory approval workflows, and returned to the Supervisor for centralized governance decisions.

The Supervisor remains the only component authorized to assign the final readiness classification, preserving hierarchical control, explainability, and enterprise governance integrity.
