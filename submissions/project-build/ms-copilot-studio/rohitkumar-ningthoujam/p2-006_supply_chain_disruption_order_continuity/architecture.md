# P2-006 — Architecture

## Overview

The solution uses a multi-agent architecture in Microsoft Copilot Studio. The Supply Continuity Supervisor coordinates validation, specialist analysis, recovery resolution, approval handling, reassessment, and final reporting.

## Architecture Flow

Autonomous Trigger
        ↓
Supply Continuity Supervisor
        ↓
Disruption Intake & Validation
        ↓
Scope Identification
        ↓
Parallel Specialist Fan-Out
        ↓
┌──────────────────┬──────────────────┬──────────────────┬──────────────────┐
│ Inventory        │ Alternate        │ Customer &       │ Commercial       │
│ Specialist       │ Supplier         │ Order Specialist │ Specialist       │
└──────────────────┴──────────────────┴──────────────────┴──────────────────┘
        ↓
Specialist Fan-In
        ↓
Recovery Planning
        ↓
Recovery Strategy Resolution
        ↓
Approval / Exception / Selective Reassessment
        ↓
Final Validation
        ↓
Reporting & Communication
        ├── Word Report
        ├── Excel Update
        └── Outlook Notification

## Supervisor

The Supply Continuity Supervisor is responsible for:

- Detecting and coordinating disruption processing.
- Calling the required custom topics.
- Delegating independent analysis to specialist agents.
- Collecting specialist outputs.
- Coordinating recovery planning.
- Applying decision precedence through the Recovery Strategy Resolution topic.
- Routing approval and exception handling.
- Coordinating selective reassessment.
- Validating the final recovery outcome.
- Coordinating reporting and notification.

## Specialist Layer

Specialist agents provide independent assessments before the Supervisor performs final coordination.

The specialist layer supports independent analysis of:

- Inventory availability
- Alternate supplier options
- Customer and order impact
- Commercial impact
- Recovery planning

Independent specialist outputs are consolidated during fan-in.

## Custom Topic Layer

### Topic 1 — Disruption Intake & Validation

Validates the disruption before specialist processing.

The topic verifies required disruption information and confirms that the disruption is eligible for processing.

### Topic 2 — Recovery Strategy Resolution

Resolves competing specialist recommendations after fan-in.

Mandatory precedence:

1. Safety or quality restriction
2. Strategic/SLA-protected customer commitment
3. Supplier approval restriction
4. Inventory availability and timing
5. Commercial approval requirement
6. Cost optimisation
7. Lower-priority customer convenience

The topic supports:

- Existing inventory sufficient
- Partial inventory
- Approved alternate available
- Unapproved alternate only
- No viable recovery route

### Topic 3 — Approval, Exception & Selective Reassessment

Controls:

- Human approval
- Specialist retry
- Stale specialist results
- Selective reassessment
- Reassessment cycles
- Manual review

## Orchestration Patterns

### Sequential

Used when a downstream stage depends on a previous stage.

Validation → Scope → Recovery Planning → Final Validation

### Parallel Fan-Out / Fan-In

Independent specialist analyses are executed separately and then consolidated.

Supervisor
    ↓
Fan-Out
 ┌──┼──┬──┐
 ↓  ↓  ↓  ↓
Inv Alt Cust Comm
 └──┼──┴──┘
    ↓
  Fan-In

### Hierarchical

The Supervisor coordinates specialist child agents and controls the overall workflow.

### Conditional

Recovery branches are selected according to inventory, supplier approval, customer priority, commercial requirements, and recovery feasibility.

### Conflict Resolution

Conflicting specialist recommendations are resolved using the mandatory decision precedence rather than averaging scores.

### Retry / Fallback

A failed specialist is retried once. A second failure results in insufficient evidence and may require manual review.

### Selective Reassessment

When relevant disruption or specialist information changes, only affected analysis is reassessed where possible.

## Data Flow

Input disruption data is validated first.

Validated data is then used to identify affected supply and demand.

Specialists independently analyse the relevant dimensions and return findings to the Supervisor.

The Supervisor sends consolidated findings to the Recovery Strategy Resolution topic.

The resulting recovery strategy is then evaluated for approval, exception handling, reassessment, and final validation.

## Human Approval Boundary

The architecture prevents autonomous execution of actions requiring human authorization.

These include:

- Supplier approval
- Supplier qualification
- Purchase-order placement
- Commercial approval
- Finance approval
- Customer agreement
- Management authorization

The system may recommend, route, and escalate these actions.

## External Systems

### Excel Online

Used for operational disruption and supply-chain data and status updates.

### Word

Used to generate the final recovery report.

### Outlook

Used for conditional recovery notifications after required authorization checks.

## Governance

The architecture follows separation of responsibilities.

The Supervisor coordinates the workflow.

Specialist agents provide focused analysis.

Custom topics implement deterministic business rules.

Human approval remains the boundary for actions requiring authorization.

The system must not fabricate specialist findings, approval decisions, customer agreements, or execution results.