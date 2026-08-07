## P2-005 — Autonomous Marketing Campaign Launch Readiness & Governance System

## Overview

The solution uses three custom topics in Microsoft Copilot Studio to manage critical workflow stages:

1. Campaign Intake & Validation  
2. Remediation & Selective Reassessment  
3. Approval & Finalisation  

The **Mohd Zaid Campaign Readiness Supervisor Agent** controls these topics and remains the only component authorized to determine the final campaign readiness status.

---

# 1. Campaign Intake & Validation Topic

## Purpose

Validates campaign information before specialist Child Agents start assessment.

## Flow

```
Recurrence Trigger
        ↓
Supervisor Agent
        ↓
Campaign Intake & Validation Topic
        ↓
Specialist Assessment
```

## Validation Checks

The topic validates:

- Campaign ID exists.
- Campaign ID is unique.
- Campaign status is Pending.
- Campaign name exists.
- Product exists.
- Launch date exists and is not in the past.
- Budget information exists.
- Geography exists.
- At least one channel exists.
- Campaign owner exists.

## Duplicate Handling

The topic checks whether the campaign is already:

- In Assessment
- Awaiting Remediation
- Awaiting Approval
- Completed

If duplicate is detected:

```
Stop processing
Prevent duplicate assessment
```

## Output

Success:

```
ValidationStatus = Passed
CampaignStatus = In Assessment
Continue workflow
```

Failure:

```
ValidationStatus = Failed
Stop workflow execution
```

---

# 2. Remediation & Selective Reassessment Topic

## Purpose

Handles campaigns with correctable blocking issues and reassesses only affected areas.

## Trigger

Executed when the Supervisor identifies remediation requirements.

## Responsibilities

The topic:

- Collects failed specialist domains.
- Creates remediation actions.
- Assigns responsible owners.
- Updates campaign status to Awaiting Remediation.
- Detects corrected data.
- Identifies stale specialist results.
- Re-runs only impacted specialists.
- Returns updated results to the Supervisor.

## Selective Reassessment Example

Initial Assessment:

| Specialist | Result |
|---|---|
| Budget | Pass |
| Brand | Pass |
| Channel | Block |
| Asset | Block |

Issue:

```
Missing Landing Page
```

After correction:

Re-run:

```
Channel Specialist
Asset Specialist
```

Skip:

```
Budget Specialist
Brand Specialist
```

## Reassessment Control

Maximum automated reassessment cycles:

```
2 cycles
```

After two unsuccessful attempts:

```
Campaign Status = Manual Review
```

---

# 3. Approval & Finalisation Topic

## Purpose

Handles campaigns requiring mandatory human approval before final readiness.

## Trigger

Executed when approval conditions are detected.

## Approval Conditions

The topic evaluates:

- Proposed budget exceeds approved budget.
- Proposed budget exceeds INR 1,000,000.
- Target CPL exceeds INR 4,000.
- High sensitivity campaign.
- Multi-market campaign.
- Restricted or quantified claims.
- Urgent launch with unresolved approval.

## Responsibilities

The topic:

- Identifies required approver.
- Records approval reason.
- Sets campaign status to Awaiting Approval.
- Returns approval information to the Supervisor.

## Rules

The topic must:

- Never fabricate human approval.
- Never mark campaign Ready while approval is pending.
- Allow reassessment after approval changes.

---

# Topic Responsibility Boundary

| Component | Responsibility |
|---|---|
| Supervisor Agent | Orchestration, conflict resolution, final readiness decision |
| Intake & Validation Topic | Campaign validation before assessment |
| Remediation Topic | Issue correction and selective reassessment |
| Approval Topic | Human approval workflow |
| Child Agents | Domain-specific campaign evaluation |

---

# Summary

The custom topics provide controlled workflow execution for the Campaign Readiness Governance System.

They ensure:

- Only valid campaigns enter assessment.
- Blocking issues follow remediation workflows.
- Only impacted domains are reassessed.
- Mandatory approvals are enforced.
- Final readiness decisions remain with the Supervisor Agent.