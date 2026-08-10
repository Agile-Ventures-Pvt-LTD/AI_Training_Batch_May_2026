# P2-006 — Specialist Agent Design

## Purpose

Specialist child agents provide focused, independent analysis for different dimensions of a supply-chain disruption.

The Supply Continuity Supervisor coordinates the specialists and consolidates their findings. Specialists do not make the final enterprise recovery decision.

## Specialist Architecture

Supply Continuity Supervisor ↓ Parallel Fan-Out ↓ ┌───────────┬───────────┬──────────────┬──────────────┐ │ Inventory │ Alternate │ Customer & │ Commercial │ │ Specialist│ Supplier │ Order │ Specialist │ │ │ Specialist│ Specialist │ │ └───────────┴───────────┴──────────────┴──────────────┘ ↓ Fan-In ↓ Recovery Planning ↓ Strategy Resolution

## 1. Inventory Specialist

### Purpose

Assess inventory availability and determine whether available supply can protect affected demand.

### Responsibilities

Evaluate available inventory.  
Assess ATP.  
Identify inventory constraints.  
Exclude quality-held quantities where applicable.  
Determine whether existing inventory can protect affected demand.  
Identify partial inventory coverage.  
Identify potential safety-stock consumption.

### Output

Inventory availability  
ATP  
Protected demand quantity  
Unprotected demand quantity  
Timing  
Safety-stock impact  
Inventory constraints  
Recommendation

## 2. Alternate Supplier Specialist

### Purpose

Assess alternate supplier options for recovering affected demand.

### Responsibilities

Identify alternate suppliers.  
Determine supplier approval status.  
Assess alternate capacity.  
Assess recovery timing.  
Determine whether the alternate can meet demand.  
Identify unapproved suppliers.  
Provide alternate sourcing recommendations.

### Output

Alternate supplier  
Approval status  
Available capacity  
Expected recovery date  
Quantity supported  
Cost information where available  
Supplier restrictions  
Recommendation

## 3. Customer & Order Specialist

### Purpose

Assess customer and order impact and determine demand priority.

### Responsibilities

Identify affected customer orders.  
Assess customer priority.  
Identify strategic/SLA-protected commitments.  
Rank affected orders.  
Determine customer impact.  
Assess partial fulfilment considerations.  
Identify orders requiring protection.

### Output

Affected orders  
Customer priority  
SLA/strategic status  
Required quantities  
Order ranking  
Customer impact  
Partial fulfilment status  
Recommendation

## 4. Commercial Specialist

### Purpose

Assess commercial and financial implications of recovery options.

### Responsibilities

Evaluate cost impact.  
Assess premium sourcing.  
Identify commercial approval requirements.  
Identify Finance approval requirements where applicable.  
Compare recovery alternatives.  
Provide commercial constraints.

### Output

Recovery option cost  
Premium impact  
Commercial approval requirement  
Finance approval requirement  
Commercial constraints  
Recommendation

## 5. Recovery Planning Specialist

### Purpose

Develop recovery options from the available specialist findings.

### Responsibilities

Review consolidated specialist findings.  
Identify feasible recovery options.  
Compare inventory and alternate sourcing.  
Consider customer priority.  
Consider commercial constraints.  
Identify approval requirements.  
Prepare recovery recommendations for the Resolution topic.

### Output

Recovery options  
Supporting evidence  
Constraints  
Required approvals  
Risks  
Recommended recovery approach

## Independent Analysis

Specialists perform independent analysis within their assigned responsibility.

They must not:

Override another specialist's findings without evidence.  
Grant human approval.  
Perform unauthorized supplier qualification.  
Place purchase orders.  
Make customer commitments.  
Bypass policy restrictions.

## Fan-In

After parallel analysis, the Supervisor consolidates the specialist outputs.

Inventory Findings + Alternate Supplier Findings + Customer & Order Findings + Commercial Findings + Recovery Planning Findings ↓ Supervisor Fan-In ↓ Recovery Strategy Resolution

## Conflict Handling

Specialists may return conflicting recommendations.

Conflicts are resolved by the Recovery Strategy Resolution topic using the mandatory precedence:

Safety or quality restriction  
Strategic/SLA-protected customer commitment  
Supplier approval restriction  
Inventory availability and timing  
Commercial approval requirement  
Cost optimisation  
Lower-priority customer convenience

Specialists must not average or fabricate conflicting results.

## Failure Handling

If a specialist fails:

Retry once.  
If successful, use the returned result.  
If the second attempt fails, mark the result as insufficient evidence.  
Do not fabricate the missing analysis.  
Route the case to the appropriate fallback or manual review path.

## Selective Reassessment

When relevant data changes, the Supervisor identifies affected specialists.

Examples:

Inventory quantity changes → reassess Inventory Specialist.  
Alternate capacity changes → reassess Alternate Supplier Specialist.  
Customer priority changes → reassess Customer & Order Specialist.  
Commercial conditions change → reassess Commercial Specialist.

Only affected analysis should be rerun where possible.

## Human Approval Boundary

Specialists can recommend actions but cannot autonomously approve or execute human-controlled actions.

Human approval remains required for applicable:

Supplier approval  
Supplier qualification  
Purchase-order placement  
Commercial approval  
Finance approval  
Customer agreement  
Management escalation

## Specialist Output Principle

Every specialist result should be:

Relevant to its assigned responsibility.  
Based on available data.  
Explicit about constraints.  
Explicit about uncertainty.  
Suitable for Supervisor fan-in.  
Free from fabricated approvals or unsupported conclusions.