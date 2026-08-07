# Custom Topics Design - P2-005

## Custom Topic 1: Campaign Intake & Validation
- **Trigger:** Topic Intent
- **Purpose:** Deterministic pre-assessment validation before child agent fan-out. (Triggered only for Pending campaigns)
- **Validations:** ID uniqueness, Pending status, mandatory field presence, non-past launch date.
- **Action:** Updates Excel status to `In Assessment`.

## Custom Topic 2: Remediation & Selective Reassessment
- **Trigger:** Supervisor invocation upon specialist block.
- **Purpose:** Coordinates selective re-testing of failed domains.
- **Loop Limit:** Maximum 2 cycles. Escalates to `Manual Review` if exceeded.
- **Action:** Sets Excel status to `Awaiting Remediation`.

## Custom Topic 3: Approval & Finalisation
- **Trigger:** Supervisor invocation upon approval requirement.
- **Purpose:** Evaluates budget thresholds, CPL limits, APAC geography, and high sensitivity.
- **Action:** Sets Excel status to `Awaiting Approval` and logs `RequiredApprover`.
