# Orchestration patterns

## Overview

This project implements all mandatory orchestration patterns required for the **Autonomous Marketing Campaign Launch Readiness & Governance System** using Microsoft Copilot Studio.

The solution combines **sequential execution**, **parallel fan-out/fan-in**, **hierarchical Supervisor control**, **conditional routing**, **selective reassessment**, and **fallback/error handling**.

The **Campaign Readiness Supervisor** is the central orchestration component and controls all execution stages.

---

## Sequential orchestration

### Purpose

Sequential orchestration ensures that later stages cannot execute before required earlier stages complete successfully.

### Implemented sequence

```text
Recurrence Trigger
        |
        v
Campaign Selection
        |
        v
Campaign Intake & Validation
        |
        v
Parallel Specialist Assessments
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
        |
        v
Excel Update
        |
        v
Outlook Notification
```

### Implementation

The Supervisor invokes each stage only after the previous stage returns a successful result.

Examples:

* Specialist agents are not invoked before intake validation.
* Risk evaluation does not execute before fan-in consolidation.
* Word report generation occurs only after final readiness is determined.
* Outlook notification occurs only after Supervisor authorization.

This prevents premature reporting and unsupported readiness classifications.

---

## Parallel fan-out / fan-in orchestration

### Purpose

Parallel orchestration allows independent specialist assessment of the same campaign across multiple governance domains.

### Fan-out implementation

After successful intake validation, the Supervisor invokes four child agents independently:

* Budget & Commercial Specialist
* Brand & Content Compliance Specialist
* Channel Readiness Specialist
* Asset Readiness Specialist

Each specialist receives the same validated campaign object.

### Specialist independence

Each specialist has:

* separate instructions,
* separate tools,
* separate knowledge,
* non-overlapping responsibilities.

No specialist depends on another specialist’s output.

### Fan-in implementation

The Supervisor waits for all mandatory specialist responses before continuing.

Results are stored in:

* BudgetResult
* BrandResult
* ChannelResult
* AssetResult

The Supervisor then performs structured consolidation of:

* blocking issues,
* conditions,
* required actions,
* approvals,
* evidence.

This demonstrates the required fan-out/fan-in pattern.

---

## Hierarchical orchestration

### Purpose

The architecture uses a **parent Supervisor with specialist child agents**.

### Parent responsibilities

The Campaign Readiness Supervisor controls:

* campaign selection,
* campaign state,
* specialist invocation,
* consolidation,
* risk evaluation,
* final readiness,
* remediation,
* reporting authorization,
* notification authorization.

### Child-agent responsibilities

Budget Specialist

* financial assessment,
* budget rules,
* approval thresholds.

Brand Specialist

* brand compliance,
* content governance,
* claims,
* disclaimers.

Channel Specialist

* operational readiness,
* lead times,
* tracking,
* channel blockers.

Asset Specialist

* asset availability,
* approval status,
* QA,
* missing assets.

Risk Specialist

* governance analysis,
* risk classification,
* readiness recommendation.

Reporting Specialist

* Word report,
* Outlook notification.

### Authority separation

Child agents cannot:

* assign final readiness,
* update campaign state,
* generate final governance decisions,
* authorize communication.

All final authority remains with the Supervisor.

---

## Conditional routing

### Purpose

Conditional routing enables different execution paths based on campaign characteristics and specialist findings.

### Implemented conditions

#### Intake validation

* Missing campaign
* Duplicate processing
* Invalid campaign status
* Missing mandatory fields
* Past launch date

Invalid campaigns terminate immediately.

#### Budget routing

* Budget above approved budget
* Budget above INR 1,000,000
* CPL above INR 4,000

Routes to approval workflow.

#### Brand routing

* High-sensitivity content
* Restricted claims
* Missing disclaimers
* Brand approval required

Routes to additional review.

#### Geography routing

* Multi-market campaigns

Routes to regional approval.

#### Asset routing

* Missing mandatory assets
* Pending approvals
* Needs changes

Routes to remediation.

#### Final readiness routing

The Supervisor routes campaigns to:

* Ready
* Ready with Conditions
* Awaiting Approval
* Awaiting Remediation
* Not Ready
* Manual Review

based on deterministic governance rules.

---

## Selective reassessment loop

### Purpose

Reassessment reruns only specialist domains whose underlying data changed.

### Workflow

```text
Remediation Required
        |
        v
Create Remediation Actions
        |
        v
Update Campaign Status
        |
        v
Detect Corrected Data
        |
        v
Selective Specialist Reassessment
        |
        v
Supervisor Recalculation
```

### Preserved results

Successful specialist assessments are preserved.

Examples:

* Budget Pass remains valid.
* Brand Pass remains valid.
* Channel Pass remains valid.
* Asset Pass remains valid.

unless their underlying data changes.

### Selective invocation

Landing page corrected:

* Asset Specialist
* Channel Specialist

Budget approval obtained:

* Budget Specialist only

Brand disclaimer corrected:

* Brand Specialist only

Tracking configured:

* Channel Specialist only

This avoids unnecessary reassessment.

### Loop limit

Automated reassessment is limited to **two cycles**.

After two unsuccessful reassessments:

* CampaignStatus = Manual Review
* FinalReadiness = Manual Review

This prevents infinite reassessment loops.

---

## Fallback and failure handling

### Purpose

Failure handling prevents unsupported readiness decisions.

### Specialist failure

Supervisor behavior:

1. Retry specialist once.
2. Mark Insufficient Evidence.
3. Prevent Ready classification.
4. Route to Manual Review.

### Missing evidence

If a critical domain lacks sufficient evidence:

* Ready is prohibited.
* Manual Review is assigned.

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

Campaigns already in:

* In Assessment
* Awaiting Remediation
* Awaiting Approval
* Completed

are rejected before reassessment begins.

---

## Orchestration state management

The Supervisor controls all state transitions.

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

Invalid transitions are prevented.

Example:

Pending → Ready

is not permitted without assessment.

---

## Supervisor decision precedence

The Supervisor applies deterministic governance precedence.

Priority order:

1. Not Ready
2. Management Approval Required
3. Remediation Required
4. Ready with Conditions
5. Ready

A single blocking finding overrides lower-priority outcomes.

Specialist results are never averaged.

---

## Pattern summary

| Pattern      | Implementation                                                                  |
| ------------ | ------------------------------------------------------------------------------- |
| Sequential   | Trigger → Validation → Specialists → Risk → Validation → Reporting              |
| Parallel     | Four independent specialist child agents                                        |
| Fan-In       | Supervisor waits for all mandatory specialist outputs                           |
| Hierarchical | Supervisor controls all child-agent orchestration                               |
| Conditional  | Approval, remediation, sensitivity, geography, and failure routing              |
| Reassessment | Selective specialist rerun based on changed domains                             |
| Fallback     | Retry, insufficient evidence, manual review, and communication failure handling |

## Evidence

The implementation is demonstrated through the following Copilot Studio components:

* Campaign Readiness Supervisor
* Campaign Intake & Validation topic
* Budget Specialist
* Brand Specialist
* Channel Specialist
* Asset Specialist
* Launch Risk & Decision Specialist
* Remediation & Selective Reassessment topic
* Approval & Finalization topic
* Reporting & Communication Specialist
* Recurrence event trigger

These components collectively implement the required multi-agent orchestration architecture and governance workflow.
