# Specialist Agent Design

## Specialist 1 — Budget & Commercial
### Responsibilities
Evaluate proposed budget, approved budget, budget variance, Target CPL, expected leads, financial approval, and budget blocking conditions.

### Data
- Campaign_Requests
- Budget_Rules
- Approval_Matrix

### Output
Assessment status, budget values, variance, CPL assessment, approval requirement, required approver, blocking issues, recommended action, and evidence.

## Specialist 2 — Brand & Content Compliance
### Responsibilities
Evaluate product naming, campaign claims, regulatory sensitivity, disclaimers, brand approval, restricted/unsupported claims, CTA consistency, and external agency implications.

### Knowledge
NovaSphere Brand & Content Guidelines.

### Data
Campaign_Requests and applicable Asset_Status data.

## Specialist 3 — Channel Readiness
### Responsibilities
Evaluate every campaign channel for mandatory assets, lead time, tracking, owner, brand approval, prerequisites, and channel-specific launch blockers.

### Data
Campaign_Requests, Channel_Requirements, Asset_Status.

## Specialist 4 — Asset Readiness
### Responsibilities
Evaluate mandatory assets, availability, approval status, missing assets, pending QA, pending approval, changes required, and responsible owner.

### Classification
Each asset is classified as Ready, Condition, Blocking, or Missing.

## Sequential specialist — Launch Risk & Decision
Runs after the first four specialists and receives their findings plus launch timing, geography, sensitivity, and pending approvals. It identifies blocking/non-blocking issues, approvals, timing risk, evidence gaps, and campaign risk. It proposes an outcome but does not own the final decision.

## Sequential specialist — Reporting & Communication
Runs only after Supervisor validation. It supports Word report generation and conditional Outlook communication.

## Scope discipline
Specialists must not duplicate responsibilities. Tools and knowledge should be narrowly scoped to the domain.
