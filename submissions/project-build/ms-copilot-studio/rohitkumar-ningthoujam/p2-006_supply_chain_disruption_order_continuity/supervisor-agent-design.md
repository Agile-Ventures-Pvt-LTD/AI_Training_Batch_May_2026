# P2-006 — Supervisor Agent Design

## Purpose

The Supply Continuity Supervisor is the central orchestration agent for the autonomous supply-chain disruption response process.

It coordinates disruption validation, scope identification, specialist execution, fan-in, recovery strategy resolution, approval handling, reassessment, final validation, reporting, and notification.

## Responsibilities

The Supervisor is responsible for:

- Detecting eligible disruption cases.
- Validating disruption information.
- Identifying affected scope.
- Calling specialist child agents.
- Coordinating parallel specialist analysis.
- Collecting and consolidating specialist outputs.
- Invoking Recovery Strategy Resolution.
- Applying mandatory decision precedence.
- Routing approval requirements.
- Handling specialist failures and retry.
- Coordinating selective reassessment.
- Enforcing reassessment limits.
- Escalating cases requiring manual intervention.
- Validating the final recovery plan.
- Coordinating reporting and notification.

## Orchestration Flow

Autonomous Trigger
        ↓
Supervisor
        ↓
Topic 1 — Disruption Intake & Validation
        ↓
Scope Identification
        ↓
Specialist Fan-Out
        ↓
Specialist Fan-In
        ↓
Recovery Planning
        ↓
Topic 2 — Recovery Strategy Resolution
        ↓
Topic 3 — Approval / Exception / Reassessment
        ↓
Final Validation
        ↓
Word Report
        ↓
Excel Update
        ↓
Conditional Outlook Notification

## Child-Agent Coordination

The Supervisor coordinates specialist agents for independent analysis.

Specialist responsibilities include:

- Inventory assessment
- Alternate supplier assessment
- Customer and order impact
- Commercial impact
- Recovery planning

Specialists return findings to the Supervisor rather than making the final enterprise recovery decision.

## Decision Control

The Supervisor ensures that conflicting recommendations are resolved using the required precedence:

1. Safety or quality restriction
2. Strategic/SLA-protected customer commitment
3. Supplier approval restriction
4. Inventory availability and timing
5. Commercial approval requirement
6. Cost optimisation
7. Lower-priority customer convenience

The Supervisor must not average conflicting specialist scores.

## Recovery Routing

The Supervisor coordinates the following recovery outcomes:

### Existing Inventory Sufficient

Prefer existing supply and avoid unnecessary premium sourcing.

### Partial Inventory

Protect the highest-priority customer orders and evaluate alternate sourcing and partial fulfilment.

### Approved Alternate

Evaluate capacity, timing, cost impact, and approval requirements.

### Unapproved Alternate

Do not autonomously select the supplier. Route for supplier qualification or manual review.

### No Viable Recovery

Escalate the case and set Critical risk where appropriate.

## Approval Boundary

The Supervisor may identify and route approval requirements but must not fabricate or autonomously grant human approvals.

Examples:

- Supplier approval
- Supplier qualification
- Finance approval
- Commercial approval
- Customer agreement
- Management authorization

## Failure Handling

If a specialist fails:

1. Retry the specialist once.
2. If successful, continue processing.
3. If the second attempt fails, mark the evidence as insufficient.
4. Do not fabricate the missing result.
5. Route for manual review or appropriate fallback.

## Selective Reassessment

When disruption data or specialist findings change, the Supervisor determines which specialist analyses are affected.

Only affected specialists should be reassessed where possible.

Reassessment is bounded by a cycle limit.

If the reassessment limit is reached without resolution, the case is routed to manual review.

## Key State Variables

The Supervisor may coordinate state such as:

- Disruption status
- Approval required
- Required approver
- Approval reason
- Specialist result status
- Specialist result stale indicator
- Reassessment required
- Reassessment cycle
- Final recovery status
- Escalation status

## Final Validation

Before completion, the Supervisor verifies that:

- The disruption was validated.
- Required specialist findings are available or appropriately handled.
- Recovery precedence was applied.
- Required approvals are identified.
- Reassessment requirements are resolved or escalated.
- The final recovery plan is internally consistent.
- Reporting requirements are satisfied.
- Notification conditions are satisfied.

## Human-in-the-Loop Principle

The Supervisor is autonomous for coordination and recommendation but remains bounded by human approval requirements.

It must never represent a recommendation as an approved business action when authorization has not occurred.

## Expected Output

The Supervisor should produce or coordinate a final outcome containing:

- Disruption status
- Affected scope
- Specialist findings
- Selected recovery strategy
- Recovery rationale
- Approval requirement
- Escalation requirement
- Reassessment status
- Final decision
- Reporting status
- Notification status