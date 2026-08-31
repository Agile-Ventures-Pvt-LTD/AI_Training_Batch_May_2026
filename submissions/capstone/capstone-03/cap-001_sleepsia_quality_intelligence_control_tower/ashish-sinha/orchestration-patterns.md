# Orchestration Patterns

## Sequential
Trigger -> Topic 1 -> Specialist Analysis -> Fan-In -> Topic 2 -> Topic 3 when applicable -> Supervisor Validation -> Word/Excel/Outlook.

## Fan-Out / Fan-In
After validation, independent specialist domains are assessed and their findings are consolidated by the Supervisor. Logical fan-out/fan-in is sufficient; literal simultaneous execution is not required.

## Hierarchical
Supervisor -> child agent -> tool/knowledge source. Final severity remains with Supervisor.

## Conditional Routing
- Confirmed safety -> Critical Escalation.
- >=2 potential safety complaints -> High-Priority Quality Incident.
- >=5 similar complaints within 7 days -> Investigation Required.
- Return rate >=2% -> Investigation Required.
- Previous incident + repeated failure -> High-Priority Quality Incident.
- Missing required evidence -> Insufficient Evidence.
- Overdue CAPA -> escalation.
- Reassessment limit exceeded -> Manual Review.

## Selective Reassessment
New evidence -> identify changed input -> rerun only stale specialist -> preserve unaffected findings -> increment ReassessmentCount -> Topic 2.

Maximum automated reassessment cycles: 2.

## Retry/Fallback
Retry once. On second failure explicitly record failure and use the appropriate evidence/review path. Never claim success without execution evidence.
