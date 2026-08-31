# Custom topics

## NovaSphere supply continuity autonomous multi-agent system

## Purpose

This document defines the deterministic custom topics used by the NovaSphere Supply Continuity Autonomous Multi-Agent System.

Custom topics are used for **workflow control, deterministic branching, approval routing, reassessment management, and execution governance**.

Unlike specialist child agents, custom topics do not perform domain-specific analysis.

They provide deterministic orchestration logic that supports the Supervisor Agent.

## Topic architecture

```text
Supervisor Agent
       │
       ├── Recovery Strategy Resolution
       ├── Approval Routing
       ├── Selective Reassessment
       ├── Manual Review Escalation
       ├── Execution Completion
       └── Error Recovery
```

Topics are invoked only by the Supervisor Agent.

They do not execute independently.

## Design principles

### Deterministic execution

Topics use explicit conditional branching.

### No business analysis

Topics do not calculate inventory, supplier feasibility, customer risk, or commercial impact.

### Workflow governance

Topics manage execution flow and state transitions.

### Explicit outputs

Each topic returns structured outputs.

### Supervisor authority

The Supervisor remains the orchestration authority.

# Topic 1: Recovery strategy resolution

## Purpose

Resolve competing specialist recommendations using deterministic policy precedence.

## Invocation point

After:

* Inventory Specialist
* Alternate Supplier Specialist
* Customer Specialist
* Commercial Specialist
* Recovery Planning Specialist

## Inputs

* InventoryAssessment
* SupplierAssessment
* CustomerAssessment
* CommercialAssessment
* ProposedStrategy
* ReportedSeverity

## Decision branches

### Branch A

Existing inventory sufficient

Output:

* Resolved with Existing Supply

### Branch B

Partial inventory protection

Output:

* Combined Recovery Strategy

### Branch C

Approved alternate supplier available

Output:

* Approved Alternate Strategy

### Branch D

Unapproved alternate supplier

Output:

* Management Escalation

### Branch E

No viable recovery route

Output:

* Management Escalation

## Policy precedence

Apply:

1. Quality restrictions
2. Strategic and SLA commitments
3. Supplier approval restrictions
4. Inventory timing
5. Commercial approvals
6. Cost optimization

## Outputs

* FinalStrategy
* StrategyStatus
* FinalRisk
* ApprovalRequired
* RequiredApprover
* ResolutionRationale

# Topic 2: Approval routing

## Purpose

Route approval-required recovery strategies to the appropriate approver.

## Invocation point

After Recovery Strategy Resolution.

## Inputs

* ApprovalRequired
* RequiredApprover
* FinalStrategy
* FinalRisk

## Routing logic

### Finance approval

Condition:

Cost premium >15%

Route:

Finance Business Partner

### Director approval

Condition:

Expedite premium >10%

Route:

Supply Chain Director

### Executive escalation

Condition:

Management Escalation

Route:

Executive Operations

### Customer approval

Condition:

Customer Action Required

Route:

Customer Operations Lead

## Outputs

* ApprovalStatus
* ApprovalRoute
* WorkflowState
* NotificationRequired

# Topic 3: Selective reassessment

## Purpose

Determine which specialist assessments must be rerun when operational conditions change.

## Invocation point

When data changes after strategy validation.

## Inputs

* DataChangeEvents
* InventoryAssessment
* SupplierAssessment
* CustomerAssessment
* CommercialAssessment
* ReassessmentCycleCount

## Change-event evaluation

### Inventory change

Rerun:

* Inventory Impact Specialist

### Supplier capacity change

Rerun:

* Alternate Supplier Specialist

### Supplier cost change

Rerun:

* Alternate Supplier Specialist
* Commercial Impact Specialist

### Customer order change

Rerun:

* Customer & Order Impact Specialist

### Recovery-date change

Rerun:

* Inventory Impact Specialist
* Alternate Supplier Specialist

## Multiple changes

Return only affected specialists.

## Outputs

* ReassessmentRequired
* SpecialistsToReassess
* ReassessmentReason
* UpdatedWorkflowState

# Topic 4: Reassessment limit enforcement

## Purpose

Prevent infinite reassessment loops.

## Invocation point

After Selective Reassessment.

## Inputs

* ReassessmentCycleCount

## Logic

### Cycle count less than 2

Allow reassessment.

### Cycle count greater than or equal to 2

Route to:

Manual Review

Set:

* StrategyStatus = Manual Review
* FinalRisk = High

## Outputs

* ReassessmentAllowed
* ManualReviewRequired
* UpdatedStrategyStatus

# Topic 5: Manual review escalation

## Purpose

Escalate cases that cannot be safely resolved autonomously.

## Invocation point

When:

* validation fails,
* evidence is insufficient,
* approvals cannot be routed,
* reassessment limit reached,
* critical conflicts remain unresolved.

## Inputs

* FinalStrategy
* FinalRisk
* ResolutionRationale
* FailedSpecialists

## Actions

Prepare escalation package containing:

* disruption summary,
* failed assessments,
* unresolved conflicts,
* required decisions,
* current risk level.

## Outputs

* EscalationPackage
* EscalationRecipients
* RecommendedFinalStatus

# Topic 6: Execution completion

## Purpose

Finalize the disruption lifecycle.

## Invocation point

After:

* reporting,
* Excel update,
* notification authorization.

## Inputs

* RecommendedFinalStatus
* ReportGenerated
* NotificationsSent
* ExcelUpdated

## Validation

Verify:

* report generated,
* Excel updated,
* notifications completed,
* final strategy recorded.

## Completion logic

### Success

Set:

* Status = Completed

### Partial completion

Set:

* Recovery Plan Proposed

### Approval pending

Set:

* Awaiting Approval

## Outputs

* FinalWorkflowStatus
* ExecutionCompleted
* AuditRecord

# Topic 7: Error recovery

## Purpose

Provide deterministic recovery from orchestration failures.

## Invocation point

When:

* Excel read fails,
* Excel update fails,
* specialist invocation fails,
* report generation fails,
* notification fails.

## Inputs

* FailedComponent
* ErrorType
* RetryCount

## Recovery logic

### Excel read

Retry once.

### Excel update

Retry once.

### Specialist invocation

Retry once.

### Report generation

Retry once.

### Notification

Retry once.

## Failure escalation

After retry failure:

* preserve evidence,
* create execution log,
* route to Manual Review,
* notify process owner.

## Outputs

* RetryPerformed
* RecoverySucceeded
* EscalationRequired

# Topic interaction model

```text
Recovery Strategy Resolution
            │
            ▼
      Approval Routing
            │
      ┌─────┴─────┐
      │           │
Approval     No Approval
      │           │
      ▼           ▼
Await Approval  Reporting
      │
      ▼
Selective Reassessment
      │
      ▼
Reassessment Limit
      │
      ▼
Manual Review
```

## State transitions

Topics may update workflow state.

Allowed transitions:

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
* Insufficient Evidence
* Manual Review

Invalid transitions must be rejected.

## Topic contracts

### Inputs

Topics receive validated Supervisor context.

### Processing

Topics execute deterministic branching only.

### Outputs

Topics return structured workflow decisions.

### Side effects

Topics do not:

* modify inventory,
* create purchase orders,
* approve suppliers,
* approve spending,
* send notifications directly.

External actions are performed by Power Automate.

## Logging requirements

Each topic execution should record:

* topic name,
* invocation time,
* input summary,
* selected branch,
* output summary,
* workflow state,
* completion status.

This provides workflow traceability.

## Success criteria

A custom topic is successful when it:

* applies deterministic rules,
* produces predictable outputs,
* updates workflow state correctly,
* preserves governance boundaries,
* enables Supervisor orchestration,
* supports auditability.

## Conclusion

The custom-topic layer provides deterministic workflow control for the NovaSphere Supply Continuity Autonomous Multi-Agent System.

By separating workflow governance from specialist analysis, the architecture achieves predictable execution, policy compliance, approval governance, selective reassessment, and complete operational traceability.
