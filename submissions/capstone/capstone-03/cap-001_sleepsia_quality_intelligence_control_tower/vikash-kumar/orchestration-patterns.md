# 🔀 Orchestration Patterns
## Overview
The solution uses several orchestration patterns.
These patterns are implemented across the four mandatory topics.
The patterns describe how work moves through the agentic workflow.

## Sequential Pattern
The main lifecycle follows a sequential structure.
Topic 1 executes before Topic 2.
Topic 2 executes before Topic 3.
Topic 3 precedes Topic 4 when new evidence requires reassessment.
The sequence creates a controlled business process.
Validation happens before specialist investigation.
Investigation happens before CAPA planning.
CAPA planning happens before final operational outputs.
Reassessment happens when new evidence becomes available.

## Topic 1 Sequence
The first stage retrieves complaint information.
The complaint record is validated.
Required information is checked.
A valid record can proceed.
An invalid or insufficient record follows a fallback.
Product and batch analysis can then occur.
The topic prevents incomplete data from immediately entering downstream investigation.

## Conditional Pattern
Conditional routing determines whether the workflow proceeds.
A required field may be missing.
A validation condition may fail.
The workflow then follows the insufficient-evidence branch.
A valid condition follows the investigation path.
The same principle can be used after specialist findings.
Decision routing remains controlled by the Supervisor.

## Hierarchical Pattern
The Supervisor is the parent orchestration layer.
Specialist agents are child investigation capabilities.
The Supervisor delegates domain analysis.
The specialists return findings.
The Supervisor combines findings.
The Supervisor owns the final decision.
This creates clear responsibility separation.

## Multi-Specialist Pattern
Topic 2 requires multiple quality perspectives.
Complaint Pattern analysis is one perspective.
Returns analysis is another perspective.
Customer Impact analysis is another perspective.
Safety analysis is another perspective.
Product and Batch analysis provides another evidence dimension.
The Supervisor receives the relevant findings.
The combined evidence supports the quality decision.

## Fan-Out Concept
The investigation can be viewed as fan-out from the Supervisor.
The Supervisor delegates independent analysis.
Each specialist investigates its own domain.
Specialists do not need to duplicate other specialists' responsibilities.
The model reduces monolithic reasoning.
The model makes domain boundaries explicit.

## Fan-In Concept
After specialist investigation, findings return to the Supervisor.
The Supervisor receives the evidence.
The Supervisor evaluates the combined evidence.
The Supervisor applies the configured decision rules.
The Supervisor selects the next operational action.
This creates a fan-in decision stage.

## CAPA Orchestration
After investigation, the workflow moves to CAPA planning.
The CAPA Specialist prepares action information.
The Supervisor coordinates operational execution.
Excel can be updated.
Word documentation can be created.
Outlook communication can be triggered.
The outputs are connected to the investigation result.

## Reassessment Pattern
Topic 4 introduces a reassessment loop.
New evidence enters the workflow.
The affected investigation dimension is identified.
The relevant specialist is selected.
The specialist performs reassessment.
The updated finding returns to the Supervisor.
The Supervisor evaluates whether the decision changes.
Final operational outputs can then be updated.

## Selective Reassessment
Selective reassessment is intentionally narrower than full rerun.
New safety evidence can trigger safety reassessment.
New complaint evidence can trigger complaint pattern reassessment.
New return evidence can trigger returns reassessment.
New customer evidence can trigger customer impact reassessment.
Product or batch evidence can trigger Product / Batch reassessment.
Unrelated areas should not be rerun without a reason.

## Fallback Pattern
Insufficient evidence is a controlled fallback.
The workflow does not invent missing information.
The workflow can stop or request additional evidence.
The Supervisor remains aware of the incomplete state.
The fallback protects evidence quality.

## Pattern Summary
Sequential orchestration controls the lifecycle.
Conditional orchestration controls routing.
Hierarchical orchestration controls delegation.
Multi-specialist orchestration controls investigation.
Fan-out distributes independent analysis.
Fan-in consolidates findings.
Reassessment handles new evidence.
Fallback handles missing evidence.
Together these patterns form the Control Tower workflow.