# 🏗️ Architecture
## Architecture Objective
The architecture defines how the Sleepsia Quality Intelligence Control Tower is organized.
The architecture is centered on a Quality Supervisor.
The Supervisor coordinates specialist child agents.
The Supervisor coordinates operational tools.
The architecture separates domain analysis from final decision ownership.
The design supports a controlled quality investigation lifecycle.

## High-Level Components
The first component is the Quality Supervisor.
The second component is the Product / Batch Specialist.
The third component is the Complaint Pattern Specialist.
The fourth component is the Returns Specialist.
The fifth component is the Customer Impact Specialist.
The sixth component is the Safety Specialist.
The seventh component is the CAPA Specialist.
The eighth component is the Excel operational layer.
The ninth component is the Word documentation layer.
The tenth component is the Outlook communication layer.
The mandatory custom topics connect these components.

## Supervisor
The Supervisor is the top-level orchestration component.
It receives the user request or workflow trigger.
It determines the appropriate topic.
It invokes specialist agents when required.
It evaluates specialist findings.
It applies conditional routing.
It coordinates CAPA activities.
It coordinates operational tool actions.
It manages evidence updates.
It owns the final quality decision.
It should not delegate final ownership blindly.
It should maintain clear responsibility boundaries.

## Product / Batch Specialist
The Product / Batch Specialist analyzes product evidence.
It analyzes SKU information.
It analyzes BatchID information.
It checks relevant product and batch relationships.
It provides findings to the Supervisor.
It does not independently make the final quality classification.
It should identify missing product or batch evidence.
It should avoid unsupported assumptions.
It should return concise evidence-based findings.

## Complaint Pattern Specialist
The Complaint Pattern Specialist analyzes complaint patterns.
It analyzes complaint counts.
It analyzes complaint categories.
It analyzes severity distribution.
It analyzes repeated failure modes.
It analyzes similar complaint clusters.
It analyzes SKU-level patterns.
It analyzes batch-level patterns.
It analyzes complaint dates.
It analyzes seven-day windows.
It identifies potential repeated complaints.
It identifies affected customers where available.
It identifies safety indicators present in complaint data.
The specialist should not count one ComplaintID twice.
The specialist should not assume duplicates solely from SKU similarity.
The specialist should report the evidence used.
The specialist should report missing information.
The specialist does not own final classification.

## Returns Specialist
The Returns Specialist analyzes return evidence.
It retrieves relevant return records.
It identifies return counts.
It identifies return reasons.
It checks SKU relationships.
It checks BatchID relationships.
It identifies return patterns.
It reports supporting evidence.
It identifies missing return information.
It does not own the final classification.

## Customer Impact Specialist
The Customer Impact Specialist analyzes customer impact.
It identifies affected customers where data supports it.
It analyzes customer exposure.
It analyzes complaint distribution.
It identifies repeated customer impact.
It identifies broader impact evidence.
It identifies missing customer impact information.
It reports findings to the Supervisor.
It does not own the final quality decision.

## Safety Specialist
The Safety Specialist analyzes safety indicators.
It identifies safety-related evidence.
It identifies missing safety information.
It reports safety findings to the Supervisor.
It does not provide medical diagnosis.
It does not provide treatment advice.
It does not independently classify the entire incident.
It does not independently own critical escalation.
The Supervisor retains final decision ownership.

## CAPA Specialist
The CAPA Specialist supports corrective action planning.
It supports preventive action planning.
It supports ownership identification.
It supports follow-up action planning.
It provides CAPA rationale.
It supports monitoring requirements.
The Supervisor controls final CAPA workflow execution.

## Data Layer
Excel provides structured operational information.
Complaint data can include ComplaintID.
Complaint data can include ComplaintDate.
Complaint data can include SKU.
Complaint data can include BatchID.
Complaint data can include OrderID.
Complaint data can include Category.
Complaint data can include Description.
Complaint data can include Severity.
Complaint data can include SafetyIndicator.
Complaint data can include Processed.
Complaint data can include Status.

## Topic Layer
Topic 1 handles intake and validation.
Topic 2 handles quality investigation.
Topic 3 handles CAPA planning and ownership.
Topic 4 handles evidence update and selective reassessment.
The topics form the business workflow.
Each topic has a defined responsibility.
The Supervisor connects the topic stages.
The architecture can stop processing when evidence is insufficient.

## Tool Layer
Excel supports retrieval and operational updates.
Word supports formal documentation.
Outlook supports communication.
Tools execute actions requested by the workflow.
Tools do not replace the Supervisor decision layer.

## Architecture Principle
The architecture is evidence first.
The architecture is supervisor controlled.
The architecture is specialist driven.
The architecture is operationally connected.
The architecture supports targeted reassessment.