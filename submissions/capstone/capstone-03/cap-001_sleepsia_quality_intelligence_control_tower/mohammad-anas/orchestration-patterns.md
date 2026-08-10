# Orchestration Patterns

## Sequential
Mandatory sequence implemented: Recurrence trigger → Incident Intake & Validation → specialist analysis → Supervisor fan-in → Quality Investigation Decision → CAPA Planning & Ownership (conditional) → Supervisor validation → Word report → Excel update → Outlook notification.

Each stage is gated on the prior stage's success:
- Specialist analysis never begins before Topic 1 returns Valid.
- Quality Investigation Decision never runs before all required specialist findings (or their retry/fallback outcomes) are collected.
- CAPA Planning only runs after a FinalClassification exists.
- Word generation never occurs before the Supervisor has a validated FinalClassification and (where applicable) CAPA output.
- Excel update never occurs before Word generation succeeds.
- Outlook notification never occurs before both Word generation and the Excel update have succeeded.

## Parallel Fan-Out/Fan-In
After Topic 1 validates a new (non-reassessment) incident, the Supervisor invokes five specialists — Safety, Complaint Pattern, Returns, Product/Batch, Customer Impact — each of which depends only on the original complaint's SKU/BatchID/OrderID, not on another specialist's output. This satisfies logical (not literal simultaneous) fan-out as permitted by the PRD.

Fan-in occurs at the point where all five specialist outputs are collected as topic variables, immediately before Quality Investigation Decision (Topic 2) is invoked.

## Hierarchical
Quality Supervisor → six domain specialists + M365 Guidance Specialist. The Supervisor owns specialist selection, fan-in consolidation, final classification (via Topic 2, which it invokes), reassessment control, and final report/notification authorisation. No specialist independently declares a final classification; each returns findings only, in the standard output contract described in custom-topics.md.

## Conditional Routing
Implemented via Condition nodes in Topic 1, Topic 2, and Topic 3:
- Existing open incident found for SKU/BatchID → route to Topic 4 (reassessment) instead of fresh fan-out.
- SafetyIndicator = Yes → Critical Escalation, bypassing all lower-priority rules.
- Two or more potential-safety complaints → High-Priority, without a confirmed indicator.
- Complaint cluster / return-rate thresholds → Investigation Required.
- FinalClassification in {Investigation Required, High-Priority, Critical Escalation} → CAPA Specialist invoked; otherwise skipped.


## Selective Reassessment
Topic 4 (Evidence Update & Selective Reassessment) determines which specialists are stale based on the nature of new evidence (e.g. a new complaint re-triggers Complaint Pattern and Safety Specialists; a new return re-triggers Returns Specialist) and re-invokes only those, preserving prior outputs from unaffected specialists. ReassessmentCount is incremented and persisted to Quality_Incidents each cycle; at ReassessmentCount > 2 the incident is set to Manual Review and no further automated reassessment occurs.

## Retry/Fallback
Each specialist topic/call is retried once on failure (self-referential topic call with an AttemptCount input variable, capped at 2 total attempts). A second failure sets AssessmentStatus = Insufficient Evidence and Completed = No for that domain rather than fabricating a value; the Supervisor does not produce an execution-ready recommendation when a material domain is Insufficient Evidence. Word, Excel, and Outlook failures at the reporting stage are recorded explicitly (ReportGeneration = Failed / Notification = Failed) and never reported as successful.

## Interactive Mode Boundary
The Supervisor's instructions explicitly separate autonomous mode (trigger-initiated) from interactive mode (Teams/Microsoft 365 Copilot chat). Interactive queries are answered from knowledge sources and read-only lookups; they never invoke Topic 1 or create/update an incident record, preventing an employee question from accidentally starting a new autonomous assessment.