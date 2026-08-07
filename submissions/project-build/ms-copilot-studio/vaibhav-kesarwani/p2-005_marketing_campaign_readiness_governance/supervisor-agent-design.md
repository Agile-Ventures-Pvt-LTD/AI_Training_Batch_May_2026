# Supervisor agent design

## Overview

The **Campaign Readiness Supervisor** is the central orchestration component of the Autonomous Marketing Campaign Launch Readiness & Governance System. It functions as the **parent agent** in the hierarchical multi-agent architecture and is responsible for coordinating the complete campaign assessment lifecycle.

The Supervisor controls workflow execution, campaign state management, specialist delegation, governance decision making, remediation coordination, and final stakeholder communication authorization.

The Supervisor is the **only component authorized to assign the final campaign readiness classification**.

## Design objectives

The Supervisor was designed to achieve the following objectives:

* autonomous event-driven execution,
* deterministic governance decisions,
* controlled multi-agent orchestration,
* prevention of duplicate processing,
* structured specialist coordination,
* selective reassessment,
* safe failure handling,
* auditable decision making.

## Core responsibilities

The Supervisor performs the following functions.

### Campaign orchestration

* Select pending campaigns.
* Initiate assessment.
* Coordinate execution stages.
* Control workflow progression.

### Campaign state management

The Supervisor owns all campaign state transitions.

Supported states:

* Pending
* In Assessment
* Awaiting Remediation
* Awaiting Approval
* Ready with Conditions
* Ready
* Not Ready
* Manual Review
* Completed

### Specialist management

The Supervisor:

* invokes child agents,
* waits for mandatory specialist completion,
* consolidates results,
* resolves conflicts,
* determines reassessment requirements.

### Governance decision making

The Supervisor applies deterministic governance policy to determine the final readiness outcome.

### Reporting authorization

Only the Supervisor can authorize:

* Word report generation,
* Outlook notification,
* campaign completion.

## High-level architecture

```text
Recurrence Trigger
        |
        v
Campaign Readiness Supervisor
        |
        v
Campaign Intake & Validation
        |
        v
Parallel Specialist Invocation
        |
        v
Fan-In Consolidation
        |
        v
Launch Risk & Decision
        |
        v
Supervisor Validation
        |
        v
Approval / Remediation
        |
        v
Reporting & Communication
```

## Execution lifecycle

### Stage 1: Autonomous trigger

The Supervisor receives control through a **Copilot Studio Recurrence Trigger**.

Actions:

* retrieve pending campaigns,
* select the oldest pending campaign,
* mark campaign In Assessment.

### Stage 2: Intake validation

The Supervisor invokes the **Campaign Intake & Validation** topic.

Validation includes:

* campaign identity,
* duplicate processing,
* campaign status,
* mandatory fields,
* launch timing,
* budget data,
* geography,
* channels,
* ownership.

Invalid campaigns terminate before specialist assessment.

### Stage 3: Parallel specialist assessment

After validation, the Supervisor invokes four independent child agents:

* Budget & Commercial Specialist
* Brand & Content Compliance Specialist
* Channel Readiness Specialist
* Asset Readiness Specialist

Each specialist evaluates the same campaign independently.

### Stage 4: Fan-in consolidation

The Supervisor waits for all mandatory specialist results.

Consolidated information includes:

* blocking issues,
* conditions,
* required actions,
* required approvals,
* evidence.

### Stage 5: Risk evaluation

The Supervisor invokes the **Launch Risk & Decision Specialist**.

The Risk Specialist provides:

* risk level,
* timing assessment,
* governance exposure,
* proposed readiness.

### Stage 6: Final validation

The Supervisor validates the recommendation using deterministic governance rules.

Possible outcomes:

* Ready
* Ready with Conditions
* Management Approval Required
* Remediation Required
* Not Ready
* Manual Review

### Stage 7: Reporting

After validation, the Supervisor authorizes the Reporting & Communication Specialist.

## Child-agent relationships

### Budget & Commercial Specialist

Purpose:

* financial governance,
* budget compliance,
* approval thresholds.

Authority:

Analysis only.

### Brand & Content Compliance Specialist

Purpose:

* content governance,
* brand compliance,
* claims validation.

Authority:

Analysis only.

### Channel Readiness Specialist

Purpose:

* operational readiness,
* channel prerequisites,
* tracking.

Authority:

Analysis only.

### Asset Readiness Specialist

Purpose:

* asset availability,
* approvals,
* QA.

Authority:

Analysis only.

### Launch Risk & Decision Specialist

Purpose:

* governance risk,
* readiness recommendation.

Authority:

Recommendation only.

### Reporting & Communication Specialist

Purpose:

* report generation,
* notification execution.

Authority:

Execution only after Supervisor authorization.

## Supervisor variables

### Campaign variables

* CurrentCampaignID
* CurrentCampaign
* ValidationStatus
* DaysToLaunch

### Specialist result variables

* BudgetResult
* BrandResult
* ChannelResult
* AssetResult
* RiskResult

### Decision variables

* FinalReadiness
* RiskLevel
* ApprovalRequired
* ReassessmentRequired
* ManualReviewRequired

### Reporting variables

* ReportURL
* NotificationStatus

## Tool ownership

The Supervisor has access to operational Excel data required for orchestration.

Primary tools:

* List Campaign Requests
* Get Campaign
* Update Campaign
* Retrieve Rules
* Retrieve Stakeholders

Word and Outlook execution are delegated to the Reporting Specialist.

## Knowledge ownership

The Supervisor uses the **NovaSphere Marketing Governance Policy** as the authoritative governance source.

The Brand Guidelines are intentionally scoped to the Brand Specialist.

## Decision framework

The Supervisor applies deterministic precedence.

### Priority order

1. Not Ready
2. Management Approval Required
3. Remediation Required
4. Ready with Conditions
5. Ready

### Blocking override

Any blocking finding prevents Ready.

Examples:

* Brand Block
* Missing mandatory asset
* Critical timing risk
* Unresolved approval
* Insufficient evidence

### Approval routing

Mandatory approval results in:

* Awaiting Approval
* Management Approval Required

### Remediation routing

Correctable governance failures result in:

* Awaiting Remediation
* Remediation Required

## Campaign state control

### Initial transition

Pending

↓

In Assessment

### Approval transition

In Assessment

↓

Awaiting Approval

↓

In Assessment

### Remediation transition

In Assessment

↓

Awaiting Remediation

↓

In Assessment

### Completion transition

In Assessment

↓

Ready / Not Ready / Manual Review

↓

Completed

Invalid transitions are rejected.

## Failure handling

### Specialist failure

Supervisor behavior:

1. Retry once.
2. Mark Insufficient Evidence.
3. Prevent Ready.
4. Route to Manual Review.

### Word failure

Behavior:

* preserve readiness,
* update Excel,
* record report failure.

### Outlook failure

Behavior:

* preserve readiness,
* preserve report,
* record notification failure.

### Duplicate processing

Campaigns already being processed are rejected before specialist invocation.

## Reassessment strategy

The Supervisor coordinates selective reassessment.

Preserved results:

* successful specialist assessments.

Reassessed domains:

* only specialists affected by corrected data.

Examples:

* Landing page corrected → Asset and Channel.
* Budget approval obtained → Budget.
* Disclaimer corrected → Brand.

Maximum automated reassessment cycles:

**2**

After two unsuccessful cycles:

* Manual Review

## Supervisor constraints

The Supervisor must never:

* fabricate specialist results,
* fabricate approvals,
* fabricate reports,
* fabricate notifications,
* bypass governance precedence,
* ignore blocking findings.

## Design rationale

The Supervisor architecture intentionally separates **orchestration** from **analysis**.

This provides:

* explainability,
* deterministic governance,
* auditability,
* maintainability,
* scalable multi-agent coordination,
* safe autonomous operation.

The resulting design ensures that all specialist expertise contributes to the assessment while preserving centralized governance control through the Campaign Readiness Supervisor.
