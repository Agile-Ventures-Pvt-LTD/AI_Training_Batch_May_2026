# Orchestration Patterns

## 1. Sequential
Required sequence:

`Trigger -> Intake Validation -> Specialist Assessments -> Fan-In -> Risk Decision -> Remediation/Approval -> Final Validation -> Reporting -> Notification`

Later stages must not execute before required earlier stages.

## 2. Parallel fan-out/fan-in
After validation, the Supervisor invokes:
- Budget & Commercial
- Brand & Content Compliance
- Channel Readiness
- Asset Readiness

The Supervisor waits for the mandatory specialist results before consolidation.

## 3. Hierarchical
`Supervisor -> Specialist Child Agents`

The Supervisor controls orchestration and owns the final decision. Specialists return findings and must not independently announce the final readiness state.

## 4. Conditional routing
Examples:
- Budget above approved amount -> approval path
- Budget above INR 1,000,000 -> VP Marketing approval
- CPL above INR 4,000 -> VP Marketing approval
- Multi-market -> Regional Marketing Lead approval
- High sensitivity -> additional review
- Missing mandatory asset -> remediation
- Specialist failure -> retry/fallback
- No blocking findings -> final readiness

## 5. Reassessment loop
`Failure -> Remediation -> Data Correction -> Selective Specialist Reassessment -> Supervisor Recalculation`

Only affected/stale domains are reassessed. The project bounds automated reassessment to two cycles.

## 6. Fallback
If a specialist fails, returns unusable information, cannot access required data, or produces insufficient evidence:
1. Retry once.
2. If unsuccessful, mark the domain as insufficient evidence.
3. Prevent unsupported Ready.
4. Route to Manual Review.

## Evidence screenshots
Reference `screenshots/parallel-specialists.png`, `fan-in-consolidation.png`, and `remediation-topic.png` after replacing the placeholders with actual build evidence.
