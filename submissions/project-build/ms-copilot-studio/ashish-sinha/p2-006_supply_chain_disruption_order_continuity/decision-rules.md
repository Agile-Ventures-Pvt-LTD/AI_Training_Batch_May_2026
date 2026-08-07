# Decision Rules

## Authority
The supplied **NovaSphere Supply Continuity Policy** is authoritative. Where explicit policy/Excel rules exist, deterministic business rules override general language-model judgment.

## Precedence
1. Policy constraints
2. Quality holds and hard operational constraints
3. Customer priority and SLA requirements
4. Supplier feasibility and recovery date
5. Commercial approval requirements
6. Cost optimization

## Inventory
- Quality-held stock is not usable supply.
- Existing inventory should be preferred when it can protect affected demand without violating constraints.
- Safety-stock consumption may require approval for strategic/SLA demand.

## Customer priority
- Strategic/SLA commitments take priority over lower-priority demand.
- If inventory is partial, rank affected orders and protect highest-priority orders.
- Do not recommend partial fulfilment when policy/constraints prohibit it.

## Alternate supplier
- An unapproved/unqualified supplier cannot be autonomously selected.
- Approved alternate suppliers may be evaluated for capacity, lead time, required-date feasibility, and cost.
- Unapproved supplier routes require qualification/manual review.

## Commercial
- Alternate supplier premium >15% → Finance Business Partner approval.
- Expedite premium >10% → Supply Chain Director approval.

## Recovery strategies
Permitted proposal categories:
- existing stock
- inventory reallocation
- approved alternate
- expedited existing supply
- expedited alternate supply
- partial fulfilment
- customer-date negotiation
- combined recovery
- management escalation
- manual review

## Approval
When approval is required:
- status = Awaiting Approval
- required approver is recorded
- reason is recorded
- system does not fabricate approval
- execution requiring approval remains blocked

## No viable route
If no safe/approved recovery protects critical demand:
- escalate to management
- final risk may be Critical
- do not autonomously execute an unapproved alternative

## Risk
Final risk must be exactly one:
- Low
- Medium
- High
- Critical

## Final strategy status
Exactly one primary status:
- Resolved with Existing Supply
- Recovery Plan Proposed
- Awaiting Approval
- Customer Action Required
- Management Escalation
- Insufficient Evidence
- Manual Review
- Completed

`Completed` must not be used while approvals are outstanding.

## Conflict examples
1. Inventory adequate for five days but Strategic SLA order due in two days → prioritize customer commitment.
2. Alternate supplier meets date but has 18% premium → technically feasible but Finance approval required.
3. Alternate supplier has capacity but is not approved → qualification/manual route.
4. Inbound PO quantity is on quality hold → exclude from usable supply.
