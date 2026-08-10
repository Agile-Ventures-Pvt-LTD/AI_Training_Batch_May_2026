# 🧩 Custom Topics
## Topic Overview
The solution contains four mandatory custom topics.
Each topic represents a defined business stage.
The topics are coordinated by the Quality Supervisor.

## Topic 1 — Incident Intake & Validation
The purpose is deterministic validation before specialist analysis.
The topic retrieves the complaint from Excel.
The topic checks required complaint information.
ComplaintID is required.
OrderID is required.
SKU is required.
Category is required.
Severity is required.
ComplaintDate is required.
BatchID is checked when supplied.
The topic also supports duplicate processing validation where configured.
If required evidence is missing, the result is Insufficient Evidence.
If the record should not proceed, downstream analysis must not be launched.
A valid record can proceed to Product / Batch Specialist analysis.

## Topic 1 Output
A valid incident is allowed to proceed.
An insufficient record is stopped.
The validation outcome should be clear.
The reason for failure should be clear.
The workflow should preserve evidence state.
The Supervisor can use the result for downstream routing.

## Topic 2 — Quality Investigation Decision
The purpose is multi-dimensional quality investigation.
The topic receives a validated incident.
The Product / Batch Specialist can analyze product and batch evidence.
The Complaint Pattern Specialist analyzes complaint patterns.
The Returns Specialist analyzes return information.
The Customer Impact Specialist analyzes customer impact.
The Safety Specialist analyzes safety evidence.
The Supervisor receives the specialist findings.
The Supervisor applies the decision logic.
The Supervisor controls conditional routing.
The topic does not allow specialists to independently own final classification.

## Complaint Pattern Analysis
The Complaint Pattern Specialist analyzes complaint counts.
It analyzes complaint categories.
It analyzes severity distribution.
It analyzes repeated failure modes.
It analyzes similar complaint clusters.
It analyzes SKU-level patterns.
It analyzes batch-level patterns.
It analyzes complaint dates.
It analyzes seven-day windows.
It identifies affected customers where available.
It identifies safety indicators.
The configured threshold is five or more similar complaints for the same SKU or batch within seven days.
Duplicate ComplaintIDs should not be counted twice.
Missing evidence should be reported.

## Topic 3 — CAPA Planning & Ownership
The purpose is to translate investigation findings into action.
The CAPA Specialist supports corrective action.
The CAPA Specialist supports preventive action.
The CAPA Specialist supports ownership.
The CAPA Specialist supports follow-up planning.
The Supervisor controls final CAPA workflow.
Excel can be updated with CAPA information.
Word can document the investigation.
Outlook can notify stakeholders.
The outputs should reflect the validated investigation state.

## Topic 4 — Evidence Update & Selective Reassessment
The purpose is to process new evidence.
New evidence may affect one or more investigation dimensions.
The workflow identifies the affected dimension.
The relevant specialist is reassessed.
The updated finding returns to the Supervisor.
The Supervisor evaluates the updated evidence.
The final decision may remain unchanged.
The final decision may change.
Operational records can then be updated.
Word documentation can be updated.
Outlook communication can be triggered when required.

## Topic Design Principle
Topic 1 validates.
Topic 2 investigates.
Topic 3 executes CAPA.
Topic 4 reassesses.
The Supervisor coordinates all four.
