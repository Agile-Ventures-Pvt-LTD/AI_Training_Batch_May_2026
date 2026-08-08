# P2-006 — Custom Topics

## Overview

The solution contains three mandatory custom topics:

Disruption Intake & Validation  
Recovery Strategy Resolution  
Approval, Exception & Selective Reassessment

## 1. Disruption Intake & Validation

### Purpose

Validates an incoming supply disruption before downstream processing.

### Responsibilities

Validate required disruption information.  
Confirm the disruption is eligible for processing.  
Prevent duplicate processing.  
Confirm disruption status.  
Stop invalid or already-processed cases.

### Flow

Disruption Trigger ↓ Validate Required Data ↓ Check Duplicate / Existing Assessment ↓ Check Disruption Status ↓ Eligible? → Yes: Continue → No: Stop / Exception

### Expected Behaviour

A valid pending disruption proceeds to scope identification.

A disruption already under assessment must not be processed again.

An invalid or ineligible disruption must stop without creating a recovery decision.

## 2. Recovery Strategy Resolution

### Purpose

Resolves competing specialist recommendations after fan-in and produces a deterministic recovery strategy.

### Inputs

Inventory specialist output  
Alternate supplier specialist output  
Customer and order specialist output  
Commercial specialist output  
Recovery planning output  
Applicable policy rules

### Mandatory Decision Precedence

When findings conflict, apply the following precedence:

Safety or quality restriction  
Strategic/SLA-protected customer commitment  
Supplier approval restriction  
Inventory availability and timing  
Commercial approval requirement  
Cost optimisation  
Lower-priority customer convenience

The topic must never simply average conflicting scores.

### Branch A — Existing Inventory Sufficient

If ATP protects all affected demand until supplier recovery:

Prefer existing inventory.  
Avoid unnecessary premium sourcing.  
Confirm whether safety stock consumption is required.

### Branch B — Partial Inventory

If ATP covers only part of demand:

Rank affected customer orders.  
Protect highest-priority orders.  
Evaluate alternate sourcing.  
Evaluate partial fulfilment permissions.

### Branch C — Approved Alternate Available

If an approved alternate can meet demand:

Calculate cost impact.  
Determine approval requirements.  
Combine alternate supply with existing inventory where necessary.

### Branch D — Unapproved Alternate Only

Do not recommend autonomous sourcing.  
Do not treat the supplier as approved.  
Escalate for supplier qualification/manual review.

### Branch E — No Viable Recovery Route

Set risk to Critical where appropriate.  
Generate management escalation.  
Do not fabricate a recovery option.

## 3. Approval, Exception & Selective Reassessment

### Purpose

Controls human approvals, specialist retry, exceptions, and selective reassessment when disruption data or specialist findings change.

### Responsibilities

Identify approval requirements.  
Identify the required approver.  
Record approval reasons.  
Track disruption status.  
Detect stale specialist results.  
Determine when reassessment is required.  
Track reassessment cycles.  
Prevent uncontrolled reassessment loops.  
Route unresolved cases to manual review.

### Core Variables

Topic.ApprovalRequired  
Topic.RequiredApprover  
Topic.ApprovalReason  
Topic.DisruptionStatus  
Topic.SpecialistResultStale  
Topic.ReassessmentRequired  
Topic.ReassessmentCycle

### Initial Values

ApprovalRequired = false  
RequiredApprover = blank  
ApprovalReason = blank  
DisruptionStatus = Pending Approval / Assessment  
SpecialistResultStale = false  
ReassessmentRequired = false  
ReassessmentCycle = 0

### Approval Flow

Recovery Recommendation ↓ Approval Required? → No: Continue → Yes: Identify Approver ↓ Route for Approval ↓ Human Decision

The system must never fabricate an approval decision.

### Specialist Failure Flow

Specialist Failure ↓ Retry Once ↓ Success? → Yes: Continue → No: Insufficient Evidence ↓ Manual Review

### Selective Reassessment

When relevant data changes:

Identify affected specialist results.  
Mark affected results as stale.  
Set ReassessmentRequired to true.  
Rerun only affected specialists where possible.  
Update specialist findings.  
Increment ReassessmentCycle.  
Return to Recovery Strategy Resolution.

### Reassessment Limit

If the case remains unresolved after the allowed reassessment cycle:

Stop automatic reassessment.  
Set the case to Manual Review.  
Escalate where required.

### Topic Integration

Autonomous Trigger ↓ Disruption Intake & Validation ↓ Scope Identification ↓ Specialist Fan-Out ↓ Specialist Fan-In ↓ Recovery Strategy Resolution ↓ Approval / Exception / Selective Reassessment ↓ Final Validation ↓ Reporting & Notification

### Human Approval Boundary

The topics may recommend and route actions but must not autonomously perform or fabricate:

Supplier approval  
Supplier qualification  
Purchase-order placement  
Commercial approval  
Finance approval  
Customer agreement  
Management authorization

### Design Principle

The three custom topics provide deterministic control over the core workflow:

Topic 1 controls eligibility and duplicate protection.  
Topic 2 controls recovery decision logic and conflict resolution.  
Topic 3 controls approvals, exceptions, retry, and reassessment.