# Autonomous Trigger

## Project
P2-005 — Marketing Campaign Readiness & Governance

## Overview

The autonomous trigger enables the Campaign Readiness Supervisor to identify campaigns that are eligible for readiness assessment and begin the assessment workflow without requiring a manual user request.

The autonomous process is restricted by the same governance rules as manually initiated assessments.

## Trigger Purpose

The autonomous trigger is responsible for:

- Checking campaign records for campaigns awaiting assessment.
- Identifying campaigns with CampaignStatus = Pending.
- Starting the readiness assessment for eligible campaigns.
- Preventing already processed campaigns from being reassessed automatically.
- Safely exiting when no eligible campaigns are available.

## Trigger Condition

A campaign is eligible for autonomous assessment when:

CampaignStatus = Pending

Campaigns with other statuses, such as In Assessment or Completed, must not be treated as new autonomous assessments.

## Autonomous Processing Flow

Autonomous Trigger
        |
        v
Check Campaign Records
        |
        v
Pending Campaign Available?
        |
   +----+----+
   |         |
  Yes        No
   |         |
   v         v
Select      Exit
Campaign    Safely
   |
   v
Campaign Readiness Supervisor
   |
   v
Campaign Intake & Validation
   |
   v
ValidationStatus = Valid?
   |
 +---+---+
 |       |
Yes      No
 |       |
 v       v
Mark     Stop
Campaign Assessment
In Assessment
 |
 v
Invoke Mandatory Specialists
 |
 v
Continue Readiness Workflow

## Campaign Intake Validation

The autonomous trigger does not bypass the Campaign Intake & Validation topic.

Before specialist processing begins, the Supervisor validates:

- CampaignID
- Required campaign fields
- Campaign eligibility
- Campaign status
- Duplicate-processing conditions
- Launch date
- Other mandatory intake requirements

Only campaigns returning:

ValidationStatus = Valid

may proceed.

## Status Transition

After successful validation, the Supervisor invokes the Mark Campaign In Assessment tool.

The campaign status is changed from:

Pending

to:

In Assessment

Specialist agents must not be invoked before this status update succeeds.

If the update fails:

- Stop further autonomous processing for the campaign.
- Do not invoke specialist agents.
- Route the campaign to Manual Review.

## Specialist Invocation

After the campaign successfully enters the In Assessment state, the Supervisor invokes the mandatory specialist agents:

- Budget & Commercial Specialist
- Brand & Content Compliance Specialist
- Channel Readiness Specialist
- Asset Readiness Specialist

The Supervisor waits for the mandatory specialist results before continuing to final decision analysis.

## Duplicate Prevention

The autonomous trigger must not repeatedly assess the same campaign.

Campaigns already marked as:

- In Assessment
- Completed
- Or another non-Pending state

must not be treated as new Pending assessments.

This prevents duplicate specialist execution and duplicate readiness decisions.

## No Pending Campaign Scenario

If no campaign has:

CampaignStatus = Pending

the autonomous workflow exits safely.

No specialist agents are invoked and no campaign records are modified.

## Failure Handling

Autonomous processing follows the same failure-handling rules as manually initiated assessments.

If a specialist fails or returns unusable evidence:

1. Retry the affected specialist once.
2. If the retry succeeds, continue processing.
3. If the retry fails, classify the domain as Insufficient Evidence.
4. Prevent a Ready outcome.
5. Route the campaign to Manual Review.

Missing specialist findings must never be inferred.

## Remediation and Reassessment

If the autonomous assessment identifies a correctable blocking issue:

- Route the issue to remediation.
- Reassess only the affected specialist domain where possible.
- Preserve valid findings from unaffected domains.
- Permit a maximum of two automated reassessment cycles.

The autonomous process must not enter an unlimited remediation loop.

## Human Approval

Autonomous processing does not replace mandatory human approval.

If governance rules require approval, the campaign must be routed through the Approval & Finalisation process.

The system must never fabricate or assume human approval.

## Finalisation

After specialist assessment, governance validation, remediation, reassessment, and required approvals are complete, the Campaign Readiness Supervisor determines the final readiness outcome.

Only the Supervisor may assign the final readiness result.

The final CampaignStatus is then persisted using the configured final status update process.

## Reporting and Communication

The Reporting & Communication Specialist may be invoked only after the Campaign Readiness Supervisor has validated the final outcome.

Autonomous processing must not send final stakeholder communication before Supervisor validation.

## Autonomous Trigger Guardrails

- Process only eligible Pending campaigns.
- Always perform Campaign Intake & Validation.
- Prevent duplicate assessment.
- Mark the campaign In Assessment before specialist invocation.
- Stop processing if the status update fails.
- Wait for mandatory specialist evidence.
- Never infer missing specialist findings.
- Retry a failed specialist only once.
- Route repeated specialist failures to Manual Review.
- Respect mandatory outcome precedence.
- Limit automated reassessment to two cycles.
- Never fabricate human approval.
- Allow only the Supervisor to assign the final outcome.
- Invoke reporting only after final Supervisor validation.
- Exit safely when no Pending campaigns exist.
- Never launch a marketing campaign.

## Scope Boundary

The autonomous trigger initiates and coordinates campaign readiness assessment only.

It does not:

- Activate marketing channels.
- Publish campaign content.
- Start advertisements.
- Launch campaigns.

The solution assesses whether a campaign is ready for launch; it does not perform the launch itself.