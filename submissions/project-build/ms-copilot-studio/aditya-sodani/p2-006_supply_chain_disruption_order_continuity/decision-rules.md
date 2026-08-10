# P2-006 — Decision Rules

## Purpose

Defines the deterministic rules used to resolve supply-chain disruption recovery decisions.

## Mandatory Decision Precedence

When findings conflict, apply the following order:

1. Safety or quality restriction
2. Strategic/SLA-protected customer commitment
3. Supplier approval restriction
4. Inventory availability and timing
5. Commercial approval requirement
6. Cost optimisation
7. Lower-priority customer convenience

The system must never simply average conflicting specialist scores.

## Existing Inventory Sufficient

If ATP protects all affected demand until supplier recovery:

- Prefer existing supply.
- Avoid unnecessary premium sourcing.
- Confirm whether safety stock consumption is required.

## Partial Inventory

If ATP covers only part of demand:

- Rank customer orders.
- Protect highest-priority orders.
- Evaluate alternate sourcing.
- Evaluate partial fulfilment permissions.

## Approved Alternate Available

If an approved alternate can meet demand:

- Calculate cost impact.
- Determine approval requirement.
- Combine alternate supply with existing inventory where necessary.

## Unapproved Alternate Only

If only an unapproved alternate is available:

- Do not recommend autonomous sourcing.
- Do not treat the supplier as approved.
- Escalate for supplier qualification or manual review.

## No Viable Recovery Route

If no viable approved recovery route exists:

- Set risk to Critical where appropriate.
- Generate management escalation.
- Do not fabricate a recovery option.

## Quality-Held Inventory

Quality-held or otherwise restricted inbound quantity must not be treated as available supply when determining ATP or recovery capacity.

## Customer Priority

Strategic and SLA-protected customer commitments take precedence over lower-priority customer convenience.

When inventory is insufficient, affected orders must be ranked according to the applicable customer-priority rules.

## Partial Fulfilment

### If Allowed

Partial fulfilment may be recommended when permitted by policy.

The system should:

- Protect the highest-priority demand.
- Identify the quantity that can be fulfilled.
- Identify the remaining uncovered quantity.
- Evaluate additional recovery options.

### If Prohibited

The system must not recommend split fulfilment.

If no compliant recovery option exists, escalate the case.

## Commercial Approval

If a recovery option requires commercial or Finance approval:

- Identify the required approval.
- Identify the approver.
- Record the approval reason.
- Route the recommendation for human authorization.

The system must not represent an unapproved recommendation as approved.

## Premium Alternate Sourcing

Where premium sourcing exceeds the applicable approval threshold:

- Calculate the cost impact.
- Identify the required approval.
- Route the recommendation for approval.
- Do not autonomously authorize the purchase.

## Supplier Approval Restriction

Supplier approval restrictions take precedence over cost optimisation.

An unapproved supplier must not be selected autonomously even when the supplier appears to provide a faster or cheaper recovery.

## Specialist Failure

If a specialist fails:

1. Retry once.
2. If successful, use the returned result.
3. If the second attempt fails, mark the result as insufficient evidence.
4. Do not fabricate the missing result.
5. Route the case to the appropriate fallback or manual-review path.

## Selective Reassessment

When disruption data or specialist findings change:

1. Identify affected specialist results.
2. Mark affected results as stale.
3. Set reassessment as required.
4. Rerun affected specialists where possible.
5. Update the findings.
6. Increment the reassessment cycle.
7. Return to recovery strategy resolution.

## Reassessment Limit

If reassessment remains unresolved after the permitted cycle limit:

- Stop automatic reassessment.
- Set the case to Manual Review.
- Escalate where required.

## Management Escalation

Management escalation is required where:

- No viable approved recovery route exists.
- Critical risk is identified.
- Required approval cannot be obtained.
- Reassessment remains unresolved after the allowed limit.
- Required specialist evidence remains unavailable.
- The required business decision exceeds autonomous authority.

## Human Approval Boundary

The system may recommend, prepare, and route actions.

It must not autonomously perform or fabricate:

- Supplier approval
- Supplier qualification
- Purchase-order placement
- Commercial approval
- Finance approval
- Customer agreement
- Management authorization

## Decision Principle

Every final recovery decision must be:

- Deterministic
- Policy-aligned
- Evidence-based
- Traceable to specialist findings
- Consistent with mandatory precedence
- Explicit about approval requirements
- Explicit about unresolved risk
- Safe against unauthorized autonomous actions