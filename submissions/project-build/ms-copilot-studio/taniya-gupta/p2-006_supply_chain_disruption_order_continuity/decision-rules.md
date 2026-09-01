# Deterministic Business Rules & Guardrails — P2-006

## Summary of Authoritative Policy Guardrails

| Rule ID | Domain | Policy Rule Description | Enforcement Component |
|---|---|---|---|
| **R-01** | Inventory | Quality-held stock (`QualityHold = Yes`) MUST be subtracted from Available to Promise (ATP). | `Inventory Impact Specialist` |
| **R-02** | Inventory | Safety stock may only be drawn down to protect Strategic or SLA-protected customer orders. | `Inventory Impact Specialist` |
| **R-03** | Supplier | Any alternate supplier with `Approved = No` MUST NEVER be autonomously selected as the final recovery source. | `Alternate Supplier Specialist` & Topic 2 |
| **R-04** | Customer | Customer order priority hierarchy: 1. Strategic + SLA Protected, 2. Priority, 3. Standard. | `Customer Impact Specialist` |
| **R-05** | Customer | `PartialFulfillmentAllowed = No` constraints must be strictly respected. Split fulfillment is prohibited. | `Customer Impact Specialist` |
| **R-06** | Commercial | Alternate supplier cost premium > 15% requires Finance Business Partner approval. | `Commercial Impact Specialist` & Topic 3 |
| **R-07** | Commercial | Expedite cost premium > 10% requires Supply Chain Director approval. | `Commercial Impact Specialist` & Topic 3 |
| **R-08** | Reassessment | Automated reassessment loop maximum limit is 2 cycles. Exceeding 2 cycles forces `Manual Review`. | Topic 3 |
| **R-09** | Escalation | If no viable approved recovery route protects critical demand, state must be set to `Management Escalation`. | Topic 2 & Topic 3 |
| **R-10** | Safety | System must never autonomously place POs, approve unapproved suppliers, cancel customer orders, or promise delivery dates. | All Specialist Agents |

## Permitted Disruption States (PRD Section 8)
- `Pending`: Awaiting assessment.
- `In Assessment`: Multi-agent assessment active.
- `Awaiting Approval`: Human approval required.
- `Recovery Plan Proposed`: Valid strategy identified.
- `Customer Action Required`: Customer fulfillment decision required.
- `Management Escalation`: No safe/approved autonomous resolution.
- `Insufficient Evidence`: Required data or specialist result missing.
- `Manual Review`: Automated reassessment exhausted (2 cycles).
- `Completed`: Reporting and notification complete.
