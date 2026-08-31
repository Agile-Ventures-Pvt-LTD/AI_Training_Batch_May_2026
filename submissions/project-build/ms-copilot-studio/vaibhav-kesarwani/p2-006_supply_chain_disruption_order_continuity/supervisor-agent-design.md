# Supervisor agent design

## NovaSphere supply continuity autonomous multi-agent system

## Purpose

The Supervisor Agent is the central orchestration component of the NovaSphere Supply Continuity Autonomous Multi-Agent System.

The Supervisor coordinates the complete disruption lifecycle from autonomous detection through validation, specialist assessment, recovery planning, policy resolution, approval routing, reporting, and operational completion.

The Supervisor is responsible for orchestration, governance, sequencing, validation, and final decision authorization.

The Supervisor does not perform domain-specific operational analysis directly.

## Design objectives

The Supervisor Agent is designed to:

* autonomously process pending disruptions,
* coordinate specialist child agents,
* execute deterministic workflows,
* preserve approval governance,
* maintain decision traceability,
* prevent unsupported autonomous actions,
* ensure policy compliance,
* coordinate external execution through Power Automate.

## Architectural role

The Supervisor acts as the orchestration controller.

```text
Recurrence Trigger
        │
        ▼
Supply Continuity Supervisor
        │
        ├── Validation
        ├── Scope Identification
        ├── Inventory
        ├── Supplier
        ├── Customer
        ├── Commercial
        ├── Recovery Planning
        ├── Strategy Resolution
        ├── Approval & Reassessment
        └── Reporting
```

The Supervisor owns execution control.

Child agents own domain expertise.

## Core responsibilities

### Orchestration

The Supervisor is responsible for:

* trigger processing,
* disruption selection,
* context preparation,
* child-agent invocation,
* parallel coordination,
* fan-in consolidation,
* conflict detection,
* final sequencing.

### Governance

The Supervisor enforces:

* validation requirements,
* approval boundaries,
* state transitions,
* retry limits,
* reassessment limits,
* deterministic policy execution.

### Decision authority

The Supervisor authorizes:

* strategy progression,
* approval routing,
* report generation,
* Excel updates,
* Outlook notifications,
* workflow completion.

## Execution lifecycle

### Stage 1: Trigger activation

The Supervisor receives a recurrence trigger.

Actions:

* read Disruption_Requests,
* identify pending disruptions,
* select the oldest pending disruption,
* process only one disruption.

Output:

Selected disruption.

### Stage 2: Duplicate protection

Immediately update:

Pending

↓

In Assessment

Purpose:

Prevent concurrent processing.

### Stage 3: Validation

Invoke:

Disruption Intake & Validation Specialist

Input:

* DisruptionID
* SupplierID
* SKU
* AffectedPO
* AffectedQty
* dates

If validation fails:

* update state,
* stop execution,
* preserve evidence.

### Stage 4: Scope identification

Invoke:

Scope Identification & Order Discovery Specialist

Output:

* affected orders,
* total demand,
* strategic exposure,
* SLA exposure,
* earliest required date.

### Stage 5: Parallel specialist execution

Invoke simultaneously:

* Inventory Impact Specialist
* Alternate Supplier Specialist
* Customer & Order Impact Specialist
* Commercial Impact Specialist

The Supervisor waits for required specialist outputs.

### Stage 6: Fan-in consolidation

Collect:

* inventory assessment,
* supplier assessment,
* customer assessment,
* commercial assessment.

Retry failed specialists once.

Build the consolidated assessment package.

### Stage 7: Recovery planning

Invoke:

Recovery Planning Specialist

Receive:

* proposed strategy,
* strategy components,
* residual risk,
* required approvals.

### Stage 8: Strategy resolution

Invoke:

Recovery Strategy Resolution Specialist

Receive:

* final strategy,
* strategy status,
* final risk,
* approval requirements.

### Stage 9: Approval and reassessment

Invoke:

Approval, Exception & Selective Reassessment Specialist

Determine:

* approval routing,
* reassessment,
* manual review,
* workflow continuation.

### Stage 10: Reporting

Invoke:

Reporting & Communication Specialist

Authorize:

* Word report,
* Excel update,
* Outlook notification.

## Supervisor state model

### Valid states

* Pending
* In Assessment
* Recovery Plan Proposed
* Awaiting Approval
* Customer Action Required
* Management Escalation
* Insufficient Evidence
* Manual Review
* Completed

### State transition rules

Pending

↓

In Assessment

↓

Recovery Plan Proposed

↓

Awaiting Approval

↓

Completed

Alternative transitions:

* Customer Action Required
* Management Escalation
* Manual Review
* Insufficient Evidence

Invalid transitions are rejected.

## Supervisor variables

### Disruption context

* DisruptionID
* SupplierID
* SKU
* AffectedPO
* AffectedQty
* ReportedSeverity
* ExpectedRecoveryDate

### Scope context

* AffectedOrders
* TotalAffectedDemand
* EarliestRequiredDate
* StrategicOrderCount
* SLAOrderCount

### Specialist context

* InventoryAssessment
* SupplierAssessment
* CustomerAssessment
* CommercialAssessment

### Decision context

* ProposedStrategy
* FinalStrategy
* StrategyStatus
* FinalRisk
* ApprovalRequired
* RequiredApprover

### Reporting context

* ExecutiveSummary
* NotificationRecipients
* RecommendedFinalStatus
* ReportPath

## Child-agent coordination

### Invocation pattern

The Supervisor invokes specialists through explicit orchestration.

The Supervisor passes:

* validated context,
* scope context,
* required operational variables.

Specialists return structured outputs.

### Synchronization

The Supervisor waits for:

Inventory

Supplier

Customer

Commercial

before recovery planning.

Partial completion is handled through retry and fallback logic.

## Fan-out and fan-in

### Fan-out

Independent specialist execution.

Benefits:

* reduced latency,
* independent evidence,
* fault isolation.

### Fan-in

Supervisor consolidation.

Responsibilities:

* collect evidence,
* validate completeness,
* identify conflicts,
* prepare recovery planning inputs.

## Context management

The Supervisor progressively enriches context.

### Initial

* disruption identifiers

### Validated

* validated operational identifiers

### Scoped

* operational impact package

### Assessed

* specialist evidence package

### Resolved

* validated strategy package

Context is never discarded.

Evidence remains traceable.

## Conflict detection

The Supervisor identifies conflicts before strategy resolution.

### Inventory vs customer

Inventory sufficient.

Strategic customer at risk.

### Supplier vs commercial

Approved alternate available.

Approval required.

### Supplier approval

Unapproved supplier proposed.

### Quality hold

Recovery depends on held inventory.

Conflicts are passed to Strategy Resolution.

The Supervisor does not resolve them directly.

## Retry strategy

Retry limit:

1

Pattern:

Failure

↓

Retry

↓

Success

or

Insufficient Evidence

Repeated failures do not generate fabricated conclusions.

## Fallback behavior

When retries fail:

* preserve successful evidence,
* mark failed domains,
* continue only if safe,
* otherwise route to Manual Review.

## Approval governance

The Supervisor enforces approval boundaries.

Approval-required cases cannot be completed autonomously.

The Supervisor:

* identifies approvers,
* updates workflow state,
* pauses execution,
* resumes only after data changes.

## Selective reassessment

When operational data changes:

* inventory,
* supplier,
* customer,
* commercial,
* recovery timing.

The Supervisor identifies stale specialist domains.

Only affected specialists are rerun.

Maximum reassessment cycles:

2

After the second unresolved cycle:

Manual Review

## Deterministic execution

The Supervisor always follows this order.

Validation

↓

Scope

↓

Parallel assessment

↓

Consolidation

↓

Recovery planning

↓

Strategy resolution

↓

Approval

↓

Reporting

↓

External execution

Execution order cannot be bypassed.

## Power Automate integration

### Generate report

Input:

Validated reporting package

Output:

Executive Word document

### Update Excel

Input:

Final strategy status

Output:

Updated disruption record

### Send notification

Input:

Notification package

Output:

Stakeholder email

The Supervisor authorizes.

Power Automate executes.

## Safety boundaries

The Supervisor must never fabricate:

* supplier approval,
* customer agreement,
* inventory availability,
* commercial approval,
* executive approval,
* purchase-order execution,
* delivery commitments.

Unsupported autonomous execution is prohibited.

## Logging and traceability

The Supervisor should record:

* selected disruption,
* validation result,
* scope result,
* specialist outputs,
* consolidation result,
* proposed strategy,
* final strategy,
* approval decisions,
* reassessment events,
* reporting outputs,
* completion status.

This provides complete auditability.

## Performance considerations

### Single-unit processing

One disruption per execution.

Benefits:

* isolation,
* predictable execution,
* simpler recovery,
* easier monitoring.

### Parallel assessment

Independent specialist execution reduces total assessment time.

### Selective reassessment

Preserving unchanged evidence minimizes unnecessary recomputation.

## Error handling

The Supervisor handles:

* missing disruption data,
* Excel read failures,
* specialist failures,
* Power Automate failures,
* notification failures,
* approval routing failures.

Material failures result in:

* Manual Review,
* Insufficient Evidence,
* Management Escalation.

## Success criteria

A successful Supervisor execution:

* processes one pending disruption,
* validates operational integrity,
* identifies operational scope,
* completes specialist assessments,
* consolidates evidence,
* resolves conflicts deterministically,
* respects approval boundaries,
* produces one validated strategy,
* generates the executive report,
* updates operational records,
* notifies stakeholders,
* preserves complete decision traceability.

## Conclusion

The Supervisor Agent is the central orchestration authority of the NovaSphere Supply Continuity Autonomous Multi-Agent System.

Its design emphasizes deterministic orchestration, modular specialist coordination, approval governance, selective reassessment, and complete operational traceability.

This architecture enables autonomous disruption response while preserving enterprise control, auditability, and policy compliance.
