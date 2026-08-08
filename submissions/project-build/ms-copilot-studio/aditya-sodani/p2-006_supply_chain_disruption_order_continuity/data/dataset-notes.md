# P2-006 — Dataset Notes

## Dataset Package

The P2-006 dataset package is intentionally small and synthetic.

All identities, emails, suppliers, customers, orders, and financial values are fictional.

## Participant Files

- `P2-006_Supply_Chain_Continuity_Lab_Data.xlsx` — primary operational workbook.
- `Disruption_Requests.csv` — optional lightweight copy of trigger/request data.
- `NovaSphere_Supply_Continuity_Policy.docx` — authoritative business policy and decision rules.
- `P2-006_Dataset_Manifest.md` — dataset package documentation.

The evaluator-only file is:

- `P2-006_Evaluator_Expected_Outcomes.csv` — expected primary strategy and risk classification for seeded disruptions. This file is trainer-only and must not be distributed to participants.

## Primary Workbook

`P2-006_Supply_Chain_Continuity_Lab_Data.xlsx`

The workbook contains the following sheets:

1. `README`
2. `Disruption_Requests`
3. `Suppliers`
4. `SKU_Master`
5. `Inventory`
6. `Purchase_Orders`
7. `Customer_Orders`
8. `Alternate_Suppliers`
9. `Recovery_Rules`
10. `Stakeholders`
11. `Test_Scenarios`

## Dataset Usage in the Solution

The dataset supports the required P2-006 workflow:

Disruption Request ↓ Disruption Validation ↓ Affected SKU / PO Identification ↓ Affected Customer Orders ↓ Inventory Assessment ↓ Alternate Supplier Assessment ↓ Customer / SLA Impact ↓ Commercial Impact ↓ Specialist Fan-Out / Fan-In ↓ Recovery Strategy Resolution ↓ Approval / Reassessment ↓ Final Recovery Decision ↓ Excel Update / Word Report / Outlook Notification

## Sheet Responsibilities

### Disruption_Requests

Provides the disruption/request information used to identify and validate an unprocessed disruption.

Used for:

- Trigger identification.
- Disruption validation.
- Duplicate-processing checks.
- Disruption status.
- Initial disruption context.

### Suppliers

Provides supplier information required for supplier-related analysis.

Used by the supplier assessment workflow to evaluate supplier context and restrictions.

### SKU_Master

Provides SKU/product information required to identify the affected product and support downstream inventory and order analysis.

### Inventory

Provides inventory information used to evaluate available supply and ATP protection.

Used for:

- Inventory availability.
- ATP assessment.
- Existing-stock recovery.
- Partial inventory scenarios.
- Supply timing.

Quality-held or restricted inventory must be handled according to the policy and must not be incorrectly treated as available recovery supply.

### Purchase_Orders

Provides open purchase-order information relevant to the disruption.

Used to identify affected POs and assess supplier recovery and timing.

### Customer_Orders

Provides affected customer-order information.

Used for:

- Customer impact analysis.
- Order ranking.
- Strategic customer identification.
- SLA-protected demand.
- Partial inventory decisions.
- Customer-priority recovery logic.

### Alternate_Suppliers

Provides alternate supplier information used to evaluate recovery options.

Used for:

- Alternate supplier availability.
- Approval status.
- Capacity.
- Timing.
- Alternate sourcing evaluation.

An unapproved alternate supplier must not be selected autonomously.

### Recovery_Rules

Provides the structured recovery rules used by the solution.

These rules support deterministic recovery decisions and must be applied according to the required decision precedence.

### Stakeholders

Provides stakeholder information required for approval and escalation routing.

Used when the solution identifies a required human approval or escalation.

### Test_Scenarios

Provides seeded scenarios for evaluation and validation of the P2-006 workflow.

These scenarios support testing of the required orchestration patterns and business branches.

## Policy Dataset

`NovaSphere_Supply_Continuity_Policy.docx` is the authoritative business-policy source.

The policy governs recovery decisions, approval requirements, supplier restrictions, customer commitments, inventory treatment, commercial constraints, and escalation behaviour.

The policy must take precedence over lower-priority optimisation logic.

## Decision Precedence

The solution must resolve conflicting specialist recommendations using:

1. Safety / Quality
2. Strategic / SLA Customer Commitment
3. Supplier Approval
4. Inventory Availability & Timing
5. Commercial Approval
6. Cost Optimisation
7. Customer Convenience

Conflicting scores must not simply be averaged.

## Dataset Support for Required Recovery Branches

### Existing Inventory Sufficient

Inventory and disruption data are used to determine whether ATP protects affected demand until supplier recovery.

Expected strategy:

- Prefer existing supply.
- Avoid unnecessary premium sourcing.
- Consider safety-stock consumption where applicable.

### Partial Inventory

Inventory and customer-order data are combined to:

- Determine protected demand.
- Rank affected orders.
- Protect higher-priority customers.
- Assess remaining uncovered demand.
- Evaluate alternate supply.

### Approved Alternate

Supplier and alternate-supplier data are used to evaluate:

- Availability.
- Approval status.
- Capacity.
- Timing.
- Cost impact.
- Approval requirements.

### Unapproved Alternate

The alternate supplier data must be checked for approval status.

An unapproved supplier must not be autonomously selected.

The case must be escalated for supplier qualification or manual review.

### No Viable Recovery Route

Where the available dataset and policy rules do not provide a viable approved recovery option:

- Appropriate critical risk must be assigned.
- Management escalation must be generated.
- The system must not fabricate a recovery option.

## Dataset Support for Specialist Agents

| Data Source | Primary Use |
|---|---|
| `Disruption_Requests` | Disruption intake and validation |
| `SKU_Master` | SKU/product identification |
| `Inventory` | Inventory and ATP analysis |
| `Purchase_Orders` | PO and supplier recovery analysis |
| `Suppliers` | Supplier assessment |
| `Alternate_Suppliers` | Alternate sourcing assessment |
| `Customer_Orders` | Customer, order and SLA impact |
| `Recovery_Rules` | Deterministic recovery rules |
| `Stakeholders` | Approval and escalation routing |
| `Test_Scenarios` | Evaluation and test execution |
| `NovaSphere_Supply_Continuity_Policy.docx` | Authoritative policy and decision rules |

## Data and Human Approval Boundary

Dataset information may be used to recommend and route actions.

It must not be used to fabricate or autonomously perform:

- Supplier approval.
- Supplier qualification.
- Purchase-order placement.
- Commercial approval.
- Finance approval.
- Customer agreement.
- Management authorization.

## Data Quality Principle

The system must use the supplied dataset as evidence.

It must not invent:

- Missing supplier approvals.
- Missing customer commitments.
- Missing inventory.
- Missing capacity.
- Missing commercial approvals.
- Specialist results.
- Recovery outcomes.

Where required evidence is unavailable, the system should identify insufficient evidence and follow the configured fallback or escalation path.

## Evaluator Data Boundary

`P2-006_Evaluator_Expected_Outcomes.csv` contains expected primary strategy and risk classification for seeded disruptions.

This file is trainer-only and is not part of the participant-facing dataset.

It should not be used as an autonomous decision source.

## Dataset-to-BRD Alignment

The dataset supports the BRD requirements to:

- Detect an unprocessed disruption.
- Validate the disruption record.
- Prevent duplicate processing.
- Identify affected SKU and PO.
- Identify affected customer orders.
- Evaluate available inventory.
- Evaluate alternate suppliers.
- Evaluate customer and SLA impact.
- Evaluate commercial impact.
- Run independent specialist assessments.
- Consolidate specialist findings.
- Resolve conflicting recommendations.
- Select or propose a continuity strategy.
- Identify required human approvals.
- Selectively reassess changed conditions.
- Update the disruption register.
- Generate the Word report.
- Support conditional Outlook notification.

## Data Governance

The dataset is synthetic and intended for controlled project evaluation.

The solution should preserve:

- Source-data traceability.
- Policy constraints.
- Approval boundaries.
- Customer-priority rules.
- Supplier-approval restrictions.
- Inventory restrictions.
- Deterministic recovery precedence.
- Evidence-based decision making.

## Reference

This document is based on the official P2-006 Dataset Manifest and the P2-006 Product Requirements Document.