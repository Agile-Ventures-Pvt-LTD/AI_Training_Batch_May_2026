# 📚 Knowledge Sources
## Purpose
Knowledge sources provide information needed for grounded responses.
Operational records provide structured evidence.
Quality documentation provides policy and process context.
The agent should use the appropriate source for the question.

## Operational Excel
Excel is an important operational data source.
Complaint records provide incident evidence.
Product records provide product evidence.
Batch records provide batch evidence.
Returns records provide return evidence.
Operational fields support validation.
Operational fields support specialist investigation.
Operational fields support CAPA updates.
Operational fields support status tracking.

## Complaint Evidence
ComplaintID identifies a complaint.
ComplaintDate identifies the complaint date.
SKU identifies the product.
BatchID identifies the batch.
OrderID identifies the related order.
Category identifies the complaint category.
Description provides complaint detail.
Severity provides severity information.
SafetyIndicator provides safety-related information.
Processed can indicate processing state.
Status can indicate workflow state.

## Quality Documentation
Quality documentation can provide process definitions.
Quality documentation can provide policy context.
Quality documentation can provide decision criteria.
Quality documentation should be used according to configured source precedence.
The Supervisor should not treat unsupported generated content as source evidence.

## Evidence Precedence
Operational records should be used when the question concerns a specific incident.
Approved quality documentation should be used for policy or process definitions.
Specialist calculations should be derived from retrieved records.
The Supervisor should distinguish source evidence from generated interpretation.

## Grounding Rules
Agents should retrieve relevant information.
Agents should identify the source information used.
Agents should distinguish observed data from calculated findings.
Agents should identify missing information.
Agents should avoid unsupported assumptions.
Agents should return Insufficient Evidence when evidence is inadequate.

## Safety Information
Safety evidence should come from available complaint or approved quality records.
The Safety Specialist should not invent safety indicators.
The Safety Specialist should not provide medical diagnosis.
The Safety Specialist should not provide treatment advice.
Safety findings should be returned to the Supervisor.

## Retrieval Behavior
The system should retrieve only relevant information.
The system should avoid unsupported extrapolation.
The system should preserve identifiers such as ComplaintID.
The system should avoid duplicate counting.
The system should maintain date boundaries for seven-day analysis.

## Knowledge Governance
Knowledge sources support investigation.
They do not replace decision ownership.
The Supervisor remains responsible for final quality decisions.
Source availability can affect the quality of findings.
Missing sources should result in controlled fallback behavior.