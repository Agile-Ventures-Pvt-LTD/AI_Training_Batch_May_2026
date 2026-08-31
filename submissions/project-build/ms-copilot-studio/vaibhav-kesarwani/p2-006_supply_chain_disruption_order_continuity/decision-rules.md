# Decision rules

## NovaSphere supply continuity autonomous multi-agent system

## Purpose

This document defines the deterministic decision rules used by the NovaSphere Supply Continuity Autonomous Multi-Agent System.

The system does not rely on unrestricted generative reasoning for operational decisions.

Instead, all recovery recommendations are validated through explicit policy rules, precedence rules, approval thresholds, and deterministic branching logic.

These rules ensure:

* predictable execution,
* policy compliance,
* approval governance,
* customer protection,
* operational traceability,
* auditability.

## Decision framework

The decision engine evaluates disruptions through a structured sequence.

Validation

↓

Scope Identification

↓

Inventory Assessment

↓

Supplier Assessment

↓

Customer Assessment

↓

Commercial Assessment

↓

Recovery Planning

↓

Strategy Resolution

↓

Approval Evaluation

↓

Reporting

Only one validated recovery strategy may be produced.

## Rule hierarchy

When rules conflict, the following hierarchy applies.

1. Quality and safety restrictions
2. Strategic and SLA-protected customer commitments
3. Supplier approval restrictions
4. Inventory availability and timing
5. Commercial approval requirements
6. Cost optimization
7. Lower-priority customer convenience

Higher-priority rules always override lower-priority optimization.

## Validation rules

### Rule V1: Supplier must exist

Condition:

SupplierID not found

Result:

Validation Failed

### Rule V2: SKU must exist

Condition:

SKU not found

Result:

Validation Failed

### Rule V3: Purchase order must exist

Condition:

AffectedPO not found

Result:

Validation Failed

### Rule V4: Supplier and PO relationship

Condition:

PO does not belong to SupplierID

Result:

Validation Failed

### Rule V5: Duplicate disruption

Condition:

Disruption already In Assessment or Completed

Result:

DuplicateDetected = Yes

### Rule V6: Mandatory fields

Required:

* SupplierID
* SKU
* AffectedPO
* AffectedQty
* ReportedSeverity

Missing required fields:

Result:

Insufficient Evidence

## Inventory rules

### ATP calculation

ATP = On Hand - Reserved + Inbound Within 7 Days - Quality Hold

Quality-held inventory is never treated as available supply.

### Rule I1: Sufficient inventory

Condition:

ATP ≥ DemandUntilRecovery

Result:

InventoryAssessment = Sufficient

### Rule I2: Partial inventory

Condition:

0 < ATP < DemandUntilRecovery

Result:

InventoryAssessment = Partial

### Rule I3: No inventory protection

Condition:

ATP ≤ 0

Result:

InventoryAssessment = Insufficient

### Rule I4: Quality-hold restriction

Condition:

Recovery depends on quality-held inventory

Result:

Quality restriction overrides inventory availability.

## Supplier rules

### Rule S1: Approved supplier required

Condition:

ApprovedStatus = No

Result:

Autonomous alternate sourcing prohibited.

### Rule S2: Capacity sufficient

Condition:

AvailableCapacity ≥ RequiredAlternateQty

Result:

Capacity feasible

### Rule S3: Timing feasible

Condition:

CanMeetRequiredDate = Yes

Result:

Timing feasible

### Rule S4: No approved alternate

Condition:

AlternateAvailable = No

Result:

Escalate to recovery planning.

## Customer rules

### Customer priority order

1. Strategic + SLA
2. Strategic
3. Priority
4. Standard

### Rule C1: Strategic protection

Condition:

StrategicOrdersAtRisk > 0

Result:

Strategic protection required.

### Rule C2: SLA protection

Condition:

SLAOrdersAtRisk > 0

Result:

SLA protection mandatory.

### Rule C3: Partial fulfillment restriction

Condition:

PartialFulfillmentAllowed = No

Result:

Partial fulfillment cannot be proposed.

### Rule C4: Revenue exposure

Condition:

RevenueAtRisk exceeds internal threshold

Result:

Increase customer impact classification.

## Commercial rules

### Cost premium calculation

CostPremiumPct = (AlternateUnitCost - PrimaryUnitCost) / PrimaryUnitCost × 100

### Rule M1: Finance approval

Condition:

CostPremiumPct > 15%

Result:

ApprovalRequired = Yes

RequiredApprover = Finance Business Partner

### Expedite premium calculation

ExpeditePremiumPct = ExpeditePremium / PrimaryUnitCost × 100

### Rule M2: Director approval

Condition:

ExpeditePremiumPct > 10%

Result:

ApprovalRequired = Yes

RequiredApprover = Supply Chain Director

### Rule M3: Combined approval

Condition:

Both thresholds exceeded

Result:

Finance Business Partner and Supply Chain Director

### Rule M4: No approval

Condition:

Thresholds not exceeded

Result:

ApprovalRequired = No

## Recovery planning rules

### Rule R1: Existing inventory preferred

Condition:

InventoryAssessment = Sufficient

Result:

Use existing inventory

### Rule R2: Combined recovery

Condition:

InventoryAssessment = Partial

Result:

Combined recovery strategy

### Rule R3: Approved alternate

Condition:

ApprovedStatus = Yes

and

CanMeetRequiredDate = Yes

Result:

Approved alternate may be used.

### Rule R4: Unapproved alternate

Condition:

ApprovedStatus = No

Result:

Manual supplier qualification

### Rule R5: No viable recovery

Condition:

Inventory insufficient

No approved alternate

Strategic exposure remains

Result:

Management escalation

## Strategy resolution rules

### Branch A: Existing inventory

Conditions:

Inventory sufficient

No quality restriction

No strategic conflict

Output:

Resolved with Existing Supply

### Branch B: Partial inventory

Conditions:

Inventory partial

Output:

Combined Recovery Strategy

### Branch C: Approved alternate

Conditions:

Approved supplier available

Output:

Approved Alternate Strategy

### Branch D: Unapproved alternate

Conditions:

Only unapproved suppliers available

Output:

Management Escalation

### Branch E: No recovery

Conditions:

No inventory protection

No approved alternate

Critical customer exposure

Output:

Management Escalation

## Conflict resolution rules

### Rule X1: Quality overrides inventory

Condition:

QualityHoldImpact exists

Result:

Exclude held inventory from recovery.

### Rule X2: Customer overrides inventory convenience

Condition:

Inventory sufficient

Strategic/SLA exposure exists

Result:

Protect strategic commitments.

### Rule X3: Supplier approval overrides feasibility

Condition:

ApprovedStatus = No

Result:

Supplier cannot be autonomously selected.

### Rule X4: Approval overrides execution

Condition:

ApprovalRequired = Yes

Result:

StrategyStatus = Awaiting Approval

## Final risk rules

### Low

Conditions:

Inventory sufficient

No strategic exposure

No approval required

### Medium

Conditions:

Partial recovery required

### High

Conditions:

Approval required

Strategic exposure

Supplier limitations

### Critical

Conditions:

Strategic/SLA exposure

No approved recovery route

Management escalation

## Strategy status rules

Allowed values:

* Resolved with Existing Supply
* Recovery Plan Proposed
* Awaiting Approval
* Customer Action Required
* Management Escalation
* Insufficient Evidence
* Manual Review
* Completed

### Rule T1: Completed

Condition:

Recovery validated

No approvals outstanding

### Rule T2: Awaiting Approval

Condition:

ApprovalRequired = Yes

### Rule T3: Manual Review

Condition:

Reassessment limit reached

### Rule T4: Insufficient Evidence

Condition:

Material evidence missing

## Approval rules

The system may determine approval requirements.

The system may not grant approval.

### Finance Business Partner

* Cost premium >15%

### Supply Chain Director

* Expedite premium >10%
* Unapproved supplier escalation

### Executive Operations

* Critical recovery failure
* Management escalation

## Reassessment rules

### Inventory change

Rerun:

Inventory Impact Specialist

### Supplier capacity change

Rerun:

Alternate Supplier Specialist

### Supplier cost change

Rerun:

Alternate Supplier Specialist

Commercial Impact Specialist

### Customer order change

Rerun:

Customer & Order Impact Specialist

### Recovery-date change

Rerun:

Inventory Impact Specialist

Alternate Supplier Specialist

## Reassessment limit

Maximum automated reassessment cycles:

2

After cycle 2:

StrategyStatus = Manual Review

FinalRisk = High

Automation stops.

## Retry rules

Retry limit:

1

After retry failure:

Insufficient Evidence

No fabricated conclusions.

## Reporting rules

Generate reporting when:

* strategy validated,
* approval state determined,
* final status assigned.

Do not report Completed while approvals remain outstanding.

## Notification rules

### Completed

Operations

Supply Planning

### Recovery Plan Proposed

Operations

Procurement

Planning

### Awaiting Approval

Required approver

Operations

Planning

### Customer Action Required

Customer Operations

Account Management

### Management Escalation

Supply Chain Leadership

Executive Operations

## Prohibited decisions

The system must never:

* approve suppliers,
* approve spending,
* place purchase orders,
* cancel customer orders,
* promise delivery dates,
* consume quality-held inventory,
* fabricate inventory availability,
* fabricate customer agreements,
* fabricate approvals.

## Decision traceability

Every final strategy must be traceable to:

* validation evidence,
* scope evidence,
* inventory evidence,
* supplier evidence,
* customer evidence,
* commercial evidence,
* policy rules,
* approval rules.

## Decision matrix

| Condition              | Final Strategy           | Approval |
| ---------------------- | ------------------------ | -------- |
| Inventory sufficient   | Existing Supply          | No       |
| Partial inventory      | Combined Recovery        | Possible |
| Approved alternate     | Alternate Supplier       | Depends  |
| Unapproved alternate   | Escalation               | Yes      |
| No recovery route      | Escalation               | Yes      |
| Quality restriction    | Exclude held inventory   | Possible |
| Strategic SLA exposure | Protect strategic orders | Possible |

## Success criteria

A decision is considered valid when it:

* follows policy precedence,
* respects approval boundaries,
* protects strategic customers,
* excludes quality-held inventory,
* prevents unsupported supplier selection,
* produces one final strategy,
* produces one final status,
* produces one final risk classification,
* provides a traceable rationale.

## Conclusion

The NovaSphere Supply Continuity decision engine is intentionally deterministic.

All operational decisions are governed by explicit policy rules, approval thresholds, and conflict-resolution precedence.

This design ensures consistent disruption response, enterprise governance, customer protection, and complete operational traceability.
