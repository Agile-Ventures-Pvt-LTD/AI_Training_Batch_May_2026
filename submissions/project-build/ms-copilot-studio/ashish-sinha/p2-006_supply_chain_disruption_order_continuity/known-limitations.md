# Known Limitations

## 1. Logical parallelism
The architecture demonstrates independent logical fan-out/fan-in. It does not require proof of literal simultaneous infrastructure execution.

## 2. Copilot Studio orchestration variability
Generative orchestration may choose tools/topics/agents differently if instructions are ambiguous. Deterministic business rules should therefore remain explicit in custom topics and Supervisor instructions.

## 3. Approval execution
Human approvals are boundaries. The solution can identify and route required approval but must not fabricate or silently approve it.

## 4. External connector failures
Excel, Word, or Outlook operations may fail due to connector permissions, workbook location, authentication, throttling, or service availability. Failure handling should record the failure and avoid false success.

## 5. Data quality
Missing, inconsistent, duplicate, or stale operational data can prevent a safe decision. The system must prefer `Insufficient Evidence` or `Manual Review` over invented values.

## 6. Reassessment
Automated reassessment is intentionally bounded to two cycles. Unresolved cases after the limit go to Manual Review.

## 7. Reporting
A generated Word report is only considered successful when the actual Word operation returns a successful result/reference.

## 8. Notification
Outlook notification is conditional on final Supervisor authorization. A notification must never be represented as sent without actual connector evidence.

## 9. Evidence
Screenshots, emails, test outcomes, and execution results must be captured from the actual Copilot Studio environment. They must not be fabricated.

## 10. Tool scope
Not every child agent receives every operational connector. This improves responsibility separation but means cross-domain information must be passed through structured handoffs/fan-in.

## 11. Policy authority
The supplied NovaSphere Supply Continuity Policy is authoritative for policy-defined thresholds, precedence, status, risk, approval, and reassessment rules.
