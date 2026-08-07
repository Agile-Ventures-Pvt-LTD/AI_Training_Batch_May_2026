# Custom Topics

## Topic 1 — Campaign Intake & Validation
Purpose: deterministic pre-assessment validation.

Required checks:
- Campaign ID exists and is unique.
- Campaign status is Pending.
- Campaign name exists.
- Product exists.
- Launch date exists and is not in the past.
- Budget values exist.
- Geography exists.
- At least one channel exists.
- Campaign owner exists.

Duplicate campaigns already in In Assessment, Awaiting Remediation, Awaiting Approval, or Completed must not receive a fresh assessment.

Required state before specialists: `In Assessment`.

## Topic 2 — Remediation & Selective Reassessment
Purpose: coordinate correction and selective reassessment.

Required behavior:
- Receive failed specialist domains.
- Create remediation actions.
- Identify responsible owner.
- Set `Awaiting Remediation`.
- Preserve passed results.
- Detect corrected underlying data.
- Identify stale specialist results.
- Rerun only affected specialists.
- Return updated results to Supervisor.
- Limit automated reassessment to two cycles.
- After two unsuccessful cycles, assign Manual Review.

Example: correcting only a landing-page issue must not cause an unrelated Budget reassessment.

## Topic 3 — Approval & Finalisation
Purpose: handle mandatory human approval.

Approval conditions:
- Proposed budget > approved budget.
- Proposed budget > INR 1,000,000.
- Target CPL > INR 4,000.
- High regulatory sensitivity.
- Multi-market geography.
- Restricted/quantified claims.
- Urgent launch with unresolved approval.

Required behavior:
- Determine required approver.
- Prevent Ready while approval is outstanding.
- Record approval reason.
- Set `Awaiting Approval`.
- Reassess if approval data changes.
- Return to Supervisor.
- Never fabricate human approval.

## Topic interaction
```text
Supervisor
   |
   +--> Intake
   |
   +--> Specialists
   |
   +--> Risk Decision
          |
          +--> Remediation --> Selective Reassessment --> Supervisor
          |
          +--> Approval --> Human Decision --> Supervisor
```
