# Orchestration Patterns

## Sequential
Trigger → Validation → In Assessment → Specialist assessment → Fan-In → Recovery Planning → Strategy Resolution → Supervisor validation → Approval/Exception → Reporting → Excel/notification.

## Parallel
Four independent assessments:
- Inventory Impact
- Alternate Supplier
- Customer & Order Impact
- Commercial Impact

Logical independent fan-out/fan-in is required; literal simultaneous infrastructure execution is not required.

## Fan-In
The Supervisor waits for the four required findings and consolidates them before Recovery Planning.

## Hierarchical
Supply Continuity Supervisor → specialist child agents. Specialists provide domain findings; the Supervisor owns the final decision.

## Conditional
Examples: quality hold exclusion, approved/unapproved alternate route, Strategic/SLA protection, commercial approval thresholds, partial fulfilment restriction, no viable route escalation, specialist retry.

## Selective Reassessment
Data change → identify stale findings → rerun only impacted specialists → fan-in updated results → recalculate strategy.

## Retry/Fallback
Retry a missing specialist once. Maximum two attempts per domain. If both fail, mark Insufficient Evidence and prevent an unsupported execution-ready recommendation.

## Conflict Resolution
Precedence:
1. Safety or quality restriction
2. Strategic/SLA-protected customer commitment
3. Supplier approval restriction
4. Inventory availability and timing
5. Commercial approval requirement
6. Cost optimisation
7. Lower-priority customer convenience
