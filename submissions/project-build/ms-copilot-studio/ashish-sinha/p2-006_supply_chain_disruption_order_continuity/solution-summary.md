# Solution Summary

## Business problem
NovaSphere supply planners manually review multiple operational sources when a supplier disruption occurs. A disruption can affect inventory, open purchase orders, customer delivery commitments, strategic/SLA orders, production schedules, procurement cost, and alternate supplier requirements.

## Solution
The solution uses Microsoft Copilot Studio generative orchestration with one Supervisor Agent and six specialized child agents. The Supervisor controls the lifecycle and delegates domain-specific work.

## Core workflow
1. Autonomous trigger identifies a Pending disruption.
2. Supervisor validates the disruption through Topic 1.
3. Valid disruptions move to `In Assessment`.
4. Supervisor identifies affected SKU, PO, supplier, and customer orders.
5. Four specialists independently assess inventory, alternate suppliers, customer/order impact, and commercial impact.
6. Supervisor performs fan-in.
7. Recovery Planning Specialist creates a recovery proposal from consolidated evidence and policy.
8. Topic 2 deterministically resolves competing recovery recommendations.
9. Topic 3 handles approvals, exceptions, retries, and selective reassessment.
10. Supervisor validates the final strategy and risk.
11. Reporting & Communication Specialist creates the Word report.
12. Excel disruption status is updated.
13. Outlook notification is sent only after Supervisor authorization.

## Key controls
- Quality-held stock is excluded from usable supply.
- Unapproved suppliers cannot be autonomously selected.
- Strategic/SLA customer commitments receive priority.
- Cost premium above 15% requires Finance Business Partner approval.
- Expedite premium above 10% requires Supply Chain Director approval.
- Reassessment is limited to two automated cycles.
- Failed specialist calls are retried once before fallback.
- Missing material evidence results in `Insufficient Evidence`.
- Unresolved reassessment after two cycles results in `Manual Review`.
- `Completed` is not used while approvals remain outstanding.

## Expected outcomes
The solution demonstrates autonomous triggering, structured validation, hierarchical delegation, logical fan-out/fan-in, deterministic decision boundaries, approval routing, selective reassessment, retry/fallback, state management, Excel integration, Word reporting, and conditional Outlook communication.
