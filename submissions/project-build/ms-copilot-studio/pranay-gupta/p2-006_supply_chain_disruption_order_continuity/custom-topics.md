# Custom Topics

## Topic 1 — Disruption Intake & Validation
Validates:
- Disruption ID exists and is unique
- Status is Pending
- Supplier ID, SKU, disruption type and reported date exist
- Reported date is valid
- Affected PO exists and matches supplier/SKU
- Affected quantity is positive
- Supplier exists
- SKU exists in SKU Master

Required variables:
DisruptionID, SupplierID, SKU, DisruptionType, ReportedDate, ExpectedRecoveryDate, AffectedPO, AffectedQty, ReportedSeverity, ValidationStatus, DuplicateDetected.

If validation fails, do not invoke specialists. Use Insufficient Evidence or Manual Review.

## Topic 2 — Recovery Strategy Resolution
Runs after fan-in and Recovery Planning. Receives the four specialist findings and relevant context.

Decision precedence:
1. Safety/quality
2. Strategic/SLA customer commitment
3. Supplier approval
4. Inventory availability/timing
5. Commercial approval
6. Cost optimisation
7. Lower-priority convenience

Branches:
- Existing inventory sufficient → prefer existing supply.
- Partial inventory → protect highest-priority demand and assess alternate/partial fulfilment.
- Approved alternate → evaluate cost/approval and combine with inventory if required.
- Unapproved alternate only → manual qualification; no autonomous sourcing.
- No viable route → Critical where appropriate and management escalation.

## Topic 3 — Approval, Exception & Selective Reassessment
Handles:
- alternate premium >15%;
- expedite premium >10%;
- Strategic/SLA safety-stock consumption;
- no approved alternate;
- prohibited partial fulfilment;
- no recovery route protecting critical demand;
- specialist retry/fallback;
- stale-result reassessment.

Maximum two specialist attempts and two automated reassessment cycles. Never invent approval.
