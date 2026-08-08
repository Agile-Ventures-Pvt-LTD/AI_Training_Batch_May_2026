# P2-006 — Architecture

## Overview

The solution uses an autonomous multi-agent architecture implemented in Microsoft Copilot Studio. The Supply Continuity Supervisor acts as the central orchestration agent and coordinates disruption validation, scope identification, specialist analysis, recovery planning, deterministic recovery resolution, approval and exception handling, selective reassessment, final validation, reporting, and stakeholder notification.

The architecture combines hierarchical Supervisor-to-specialist orchestration with sequential processing, logical parallel fan-out/fan-in, conditional routing, conflict resolution, retry/fallback, and selective reassessment.

## Architecture Flow

Autonomous Recurrence Trigger  
↓  
Supply Continuity Supervisor  
↓  
Disruption Intake & Validation  
↓  
Scope Identification  
↓  
Parallel Specialist Fan-Out  
↓  
┌──────────────────┬──────────────────┬──────────────────────┬──────────────────┐  
│ Inventory Impact │ Alternate        │ Customer & Order     │ Commercial       │  
│ Specialist       │ Supplier         │ Impact Specialist    │ Impact Specialist│  
│                  │ Specialist       │                      │                  │  
└──────────────────┴──────────────────┴──────────────────────┴──────────────────┘  
↓  
Specialist Fan-In  
↓  
Recovery Planning Specialist  
↓  
Recovery Strategy Resolution  
↓  
Approval / Exception / Selective Reassessment  
↓  
Final Supervisor Validation  
↓  
Reporting & Communication  
├── Word Report  
├── Excel Status Update  
└── Outlook Notification

## Supervisor

The Supply Continuity Supervisor is responsible for coordinating the complete disruption-response lifecycle.

The Supervisor is responsible for:

- Detecting and coordinating disruption processing through the autonomous trigger.
- Calling the required custom topics.
- Validating disruption information before specialist processing.
- Identifying the affected disruption scope.
- Delegating independent analysis to specialist child agents.
- Collecting and consolidating specialist outputs.
- Coordinating recovery planning.
- Applying decision precedence through the Recovery Strategy Resolution process.
- Resolving conflicting specialist findings.
- Routing approval and exception conditions.
- Coordinating specialist retry and fallback.
- Coordinating selective reassessment when relevant information changes.
- Enforcing the maximum reassessment boundary.
- Validating the final recovery outcome.
- Determining the final risk classification and disruption status.
- Authorizing reporting and stakeholder communication.
- Preventing unsupported autonomous execution of human-approval actions.

The Supervisor retains ownership of the final recovery decision. Specialist agents provide domain-specific findings and recommendations but do not independently determine the final recovery strategy.

## Specialist Layer

Specialist agents provide focused and independent domain assessments before the Supervisor performs final coordination and recovery resolution.

The specialist layer consists of:

### Inventory Impact Specialist

Responsible for analysing:

- On-hand inventory
- Reserved inventory
- Inbound supply
- Quality-held inventory
- Available-to-promise
- Demand until supplier recovery
- Shortage quantity
- Safety-stock impact

### Alternate Supplier Specialist

Responsible for analysing:

- Available alternate suppliers
- Supplier approval status
- Available capacity
- Standard lead time
- Expedite lead time
- Unit cost
- Supplier risk
- Recovery feasibility

Only approved alternate suppliers can be autonomously recommended as recovery sources.

### Customer & Order Impact Specialist

Responsible for analysing:

- Affected customer orders
- Customer tier
- Strategic customer commitments
- SLA-protected orders
- Required dates
- Required quantities
- Partial-fulfilment permissions
- Revenue exposure
- Orders protected
- Orders remaining at risk

### Commercial Impact Specialist

Responsible for analysing:

- Recovery cost
- Alternate supplier cost premium
- Expedite premium
- Commercial impact
- Finance approval requirements
- Supply Chain Director approval requirements

### Recovery Planning Specialist

Receives the consolidated specialist findings and prepares a proposed recovery strategy.

Potential strategies include:

- Existing inventory
- Inventory reallocation
- Approved alternate supplier
- Expedite existing supply
- Expedite alternate supply
- Partial fulfilment
- Customer-date negotiation
- Combined recovery strategy
- Management escalation
- Manual review

The Recovery Planning Specialist provides a proposed strategy. Final strategy validation remains with the Supervisor and deterministic decision logic.

### Reporting & Communication Specialist

Handles downstream reporting and communication after final Supervisor validation.

Responsibilities include:

- Preparing the final Word recovery report.
- Preparing stakeholder communication.
- Using the configured Word integration.
- Using the configured Outlook integration.
- Ensuring that recommendations and actually executed actions are clearly distinguished.

Independent specialist outputs are consolidated during the Supervisor fan-in stage.

## Custom Topic Layer

### Topic 1 — Disruption Intake & Validation

Validates the disruption before specialist processing.

The topic verifies required disruption information and confirms that the disruption is eligible for processing.

Validation includes:

- Disruption ID existence
- Duplicate detection
- Pending processing status
- Supplier existence
- SKU existence
- Disruption type
- Reported date
- Expected recovery date
- Affected purchase order
- Supplier/SKU/PO relationship
- Positive affected quantity

If validation fails, specialist processing must not begin. The case is routed to the appropriate insufficient-evidence or manual-review path.

### Topic 2 — Recovery Strategy Resolution

Resolves competing specialist recommendations after fan-in and applies the mandatory deterministic decision precedence.

Mandatory precedence:

1. Safety or quality restriction
2. Strategic/SLA-protected customer commitment
3. Supplier approval restriction
4. Inventory availability and timing
5. Commercial approval requirement
6. Cost optimisation
7. Lower-priority customer convenience

The topic supports recovery evaluation for:

- Existing inventory sufficient
- Partial inventory availability
- Approved alternate supplier available
- Unapproved alternate supplier
- Expedite options
- Customer-date negotiation
- Partial fulfilment
- No viable approved recovery route
- Management escalation

The topic does not autonomously approve unqualified suppliers, place purchase orders, cancel customer orders, promise customer delivery dates, or authorize commercial expenditure.

### Topic 3 — Approval, Exception & Selective Reassessment

Controls:

- Human approval requirements
- Commercial approval requirements
- Specialist retry
- Specialist failure and fallback
- Stale specialist results
- Selective reassessment
- Reassessment cycles
- Insufficient evidence
- Manual review
- Management escalation

Specialist failures are retried once. A second unsuccessful attempt results in insufficient evidence and may require manual review.

Automated reassessment is limited to two cycles per disruption.

## Orchestration Patterns

### Sequential

Sequential orchestration is used when a downstream stage depends on the successful completion of a previous stage.

```text
Validation
    ↓
Scope Identification
    ↓
Specialist Assessment
    ↓
Fan-In
    ↓
Recovery Planning
    ↓
Recovery Strategy Resolution
    ↓
Final Validation