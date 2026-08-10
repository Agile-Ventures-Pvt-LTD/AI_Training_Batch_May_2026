# Custom Topics

## Project
P2-005 — Marketing Campaign Readiness & Governance

## Overview

Custom topics are used in the Campaign Readiness Supervisor to implement deterministic workflow logic such as campaign validation, approval handling, remediation, reassessment, and finalisation.

## Campaign Intake & Validation

The Campaign Intake & Validation topic validates a campaign before specialist assessment begins.

### Input

- CampaignID

### Responsibilities

- Retrieve the campaign using CampaignID.
- Populate campaign information from the campaign dataset.
- Validate required campaign fields.
- Validate campaign eligibility.
- Check the current CampaignStatus.
- Prevent duplicate assessment.
- Validate the campaign LaunchDate.
- Calculate DaysToLaunch.
- Return a structured validation result to the Supervisor.

### Launch Date Validation

LaunchDate is stored as a string in YYYY-MM-DD format.

DaysToLaunch is calculated using Power Fx:

DateDiff(
    Today(),
    Date(
        Value(Left(Topic.LaunchDate, 4)),
        Value(Mid(Topic.LaunchDate, 6, 2)),
        Value(Right(Topic.LaunchDate, 2))
    ),
    TimeUnit.Days
)

The campaign passes launch-date validation when:

DaysToLaunch >= 0

If DaysToLaunch is negative, the launch date is in the past and the campaign is marked invalid.

### Validation Outputs

The topic returns the required campaign information together with:

- ValidationStatus
- ValidationMessage
- CampaignID
- CampaignName
- CampaignOwner
- Product
- Geography
- LaunchDate
- DaysToLaunch
- CampaignStatus
- ProposedBudget
- ApprovedBudget
- TargetCPL
- Channels
- RegulatorySensitivity

A successful validation returns:

ValidationStatus = Valid

A failed validation returns:

ValidationStatus = Invalid

The ValidationMessage explains the reason for failure.

## Approval & Finalisation

The Approval & Finalisation process is used when governance rules require mandatory human approval.

The process ensures that:

- Required approvals are identified.
- Approval is routed to the appropriate human approver.
- Human approval is never fabricated.
- The Supervisor waits for the actual approval result.
- The approval result is considered during final readiness validation.

## Remediation and Reassessment

Correctable blocking issues may be routed through remediation.

After remediation:

- Only affected specialist domains should be reassessed where possible.
- Existing valid findings from unaffected domains should be preserved.
- The Supervisor recomputes the readiness outcome.
- A maximum of two automated reassessment cycles is permitted.

If the issue remains unresolved after the allowed reassessment cycles, the campaign is routed according to the applicable governance rule.

## Topic Integration

The main topic interaction is:

Campaign Readiness Supervisor
        |
        v
Campaign Intake & Validation
        |
        v
ValidationStatus
        |
   +----+----+
   |         |
 Valid     Invalid
   |         |
   v         v
Continue    Stop
   |
   v
Mark Campaign In Assessment
   |
   v
Specialist Assessment

## Design Principles

The custom topics follow these principles:

- Deterministic validation is separated from generative reasoning.
- Structured inputs and outputs are used between topics and agents.
- Invalid campaigns are stopped before specialist assessment.
- Missing mandatory information is not inferred.
- Human approvals are never fabricated.
- Remediation requires reassessment.
- Automated reassessment is limited.
- Final readiness authority remains with the Campaign Readiness Supervisor.
- The system assesses campaign readiness only and never launches a campaign.