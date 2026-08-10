# Decision Rules Design

## Overview

The Decision Rules define the deterministic business logic used by the Supply Continuity Supervisor and Recovery Strategy Resolution Topic.

These rules ensure recovery recommendations follow NovaSphere Supply Continuity Policy and prevent unsafe autonomous decisions.

---

# Decision Priority

When specialist recommendations conflict, apply the following precedence:

1. Safety and quality restrictions
2. Strategic and SLA customer commitments
3. Supplier approval restrictions
4. Inventory availability and timing
5. Commercial approval requirements
6. Cost optimization
7. Lower-priority customer convenience

The system must not average conflicting recommendations.

---

# Inventory Rules

## Available To Promise (ATP)

Calculation:

```
ATP =
On Hand
- Reserved
+ Inbound Within 7 Days
- Quality Hold
```

---

## Rule: Quality Hold

If inventory is under quality hold:

* Do not count as usable inventory.
* Reduce ATP accordingly.
* Escalate if customer demand is affected.

---

## Rule: Inventory Sufficient

Condition:

```
ATP >= Demand Until Recovery
```

Action:

* Prefer existing inventory.
* Avoid unnecessary alternate sourcing.
* Check safety stock consumption.

---

## Rule: Inventory Shortage

Condition:

```
ATP < Demand Until Recovery
```

Action:

* Calculate shortage quantity.
* Evaluate alternate supply options.
* Protect priority customer demand.

---

# Customer Priority Rules

Customer orders are ranked:

1. Strategic + SLA Protected
2. Priority
3. Standard

---

## Rule: Strategic/SLA Risk

If strategic or SLA orders are at risk:

Action:

* Prioritize those orders.
* Override lower-priority optimization.
* Escalate when required.

---

## Rule: Partial Fulfilment

If partial fulfilment is allowed:

* Allocate available supply based on priority.

If partial fulfilment is not allowed:

* Do not recommend split delivery.
* Evaluate alternate recovery options.

---

# Alternate Supplier Rules

## Approved Supplier Rule

Only suppliers where:

```
Approved = Yes
```

may be selected autonomously.

---

## Unapproved Supplier Rule

If:

```
Approved = No
```

Action:

* Do not select as recovery source.
* Route for manual supplier qualification.

---

## Approved Alternate Available

Condition:

* Supplier approved.
* Capacity available.
* Can meet required date.

Action:

* Evaluate cost.
* Check approval requirements.
* Recommend if feasible.

---

# Commercial Rules

## Alternate Supplier Premium

Condition:

```
Cost Premium > 15%
```

Action:

* Require Finance Business Partner approval.

---

## Expedite Premium

Condition:

```
Expedite Premium > 10%
```

Action:

* Require Supply Chain Director approval.

---

# Recovery Strategy Rules

Allowed strategies:

* Use existing stock
* Reallocate inventory
* Approved alternate supplier
* Expedite existing supply
* Expedite alternate supply
* Partial fulfilment
* Customer date negotiation
* Combined recovery strategy
* Management escalation
* Manual review

---

# Strategy Selection Rules

## Case 1: Existing Supply Protects Demand

If:

```
ATP covers all demand until recovery
```

Select:

```
Resolved with Existing Supply
```

---

## Case 2: Partial Inventory Coverage

If:

```
ATP covers only part of demand
```

Action:

* Protect highest priority orders.
* Evaluate alternate supply.
* Assess customer impact.

---

## Case 3: Approved Alternate Available

If:

```
Approved Alternate = Yes
AND
Can Meet Required Date = Yes
```

Action:

* Recommend alternate supply.
* Apply commercial approval rules.

---

## Case 4: Unapproved Alternate Only

Action:

```
Manual Review / Supplier Qualification
```

Never select automatically.

---

## Case 5: No Viable Recovery

Action:

```
Management Escalation
```

Risk:

```
Critical
```

---

# Risk Classification Rules

Final risk must be:

* Low
* Medium
* High
* Critical

---

## High/Critical Risk Requires Explanation

The Supervisor must provide:

* Evidence causing risk.
* Affected customers/orders.
* Supply constraints.
* Recovery limitations.

---

# Approval Rules

Approval is required when:

* Alternate cost premium exceeds 15%.
* Expedite premium exceeds 10%.
* Strategic SLA orders require safety stock use.
* No approved alternate exists.
* Partial fulfilment is prohibited.
* Critical demand cannot be protected.

---

# State Transition Rules

Valid transitions:

```
Pending
   ↓
In Assessment
   ↓
Recovery Plan Proposed
   ↓
Awaiting Approval
   ↓
Completed
```

Other valid outcomes:

```
Insufficient Evidence
Manual Review
Management Escalation
Customer Action Required
```

---

# Safety Boundaries

The system must never:

* Place purchase orders.
* Approve suppliers.
* Cancel customer orders.
* Commit customer delivery dates.
* Approve commercial expenditure.
* Ignore quality restrictions.

---

# Decision Rule Principles

* Business rules override generative judgement.
* Evidence-based recommendations only.
* Human approval boundaries are preserved.
* Every decision must be explainable and traceable.
