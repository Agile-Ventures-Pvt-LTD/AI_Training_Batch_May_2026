# Supervisor Agent Design

## Agent Name

Supply Continuity Supervisor

---

## Purpose

The Supply Continuity Supervisor serves as the central orchestration and governance agent for the Supply Chain Disruption Order Continuity System.

The Supervisor coordinates the complete disruption assessment lifecycle, manages specialist execution, consolidates findings, applies policy rules, determines approval requirements, and produces the final disruption recommendation.

The Supervisor acts as the workflow controller and decision authority but does not perform specialist analysis directly.

---

## Design Philosophy

The solution follows a Supervisor-Orchestrated Multi-Agent architecture.

The Supervisor is responsible for:

- Workflow control
- Specialist coordination
- Policy enforcement
- Conflict resolution
- Approval governance
- Escalation decisions
- Final recommendation generation

Domain analysis is delegated to specialist agents.

This separation ensures that business decisions are based on specialist evidence rather than unsupported assumptions.

---

## Responsibilities

The Supervisor is responsible for:

### Workflow Orchestration

- Initiating disruption assessments
- Managing workflow progression
- Coordinating specialist execution
- Managing topic execution

---

### Specialist Coordination

- Launching specialist agents
- Monitoring execution
- Collecting specialist outputs
- Managing assessment dependencies

---

### Fan-In Consolidation

- Consolidating specialist findings
- Identifying conflicts
- Identifying dependencies
- Reviewing approval requirements
- Building a unified assessment package

---

### Policy Enforcement

- Applying business policies
- Applying recovery rules
- Applying escalation rules
- Applying customer prioritization rules

---

### Approval Governance

- Determining approval requirements
- Routing approval decisions
- Preventing unauthorized execution

---

### Escalation Management

- Escalating unsupported recommendations
- Escalating insufficient evidence situations
- Escalating policy violations
- Escalating unresolved reassessment cycles

---

### Final Recommendation

- Producing final workflow outcomes
- Selecting approval paths
- Determining manual review requirements
- Initiating reporting and communication

---

## Responsibilities Not Allowed

The Supervisor must not perform specialist analysis.

The Supervisor must not independently perform:

### Inventory Analysis

The Supervisor must not:

- Calculate ATP
- Assess inventory sufficiency
- Determine inventory shortages
- Assess inventory risk

These activities belong exclusively to the Inventory Impact Specialist.

---

### Supplier Analysis

The Supervisor must not:

- Evaluate supplier capacity
- Determine supplier lead times
- Assess supplier approval status
- Evaluate alternate sourcing feasibility

These activities belong exclusively to the Alternate Supplier Specialist.

---

### Customer Impact Analysis

The Supervisor must not:

- Prioritize customer orders
- Assess SLA exposure
- Determine customer impact classification

These activities belong exclusively to the Customer & Order Impact Specialist.

---

### Commercial Analysis

The Supervisor must not:

- Calculate cost premiums
- Calculate revenue exposure
- Determine commercial risk

These activities belong exclusively to the Commercial Impact Specialist.

---

### Recovery Planning Analysis

The Supervisor must not:

- Independently evaluate recovery options
- Invent recovery strategies
- Override recovery recommendations

These activities belong exclusively to the Recovery Planning Specialist.

---

## Policy Knowledge Base

The Supervisor uses a policy knowledge base as the authoritative source of governance rules.

The policy knowledge base contains:

### Recovery Policies

- Approved recovery methods
- Recovery restrictions
- Escalation conditions

---

### Supplier Policies

- Supplier approval requirements
- Qualification restrictions

---

### Customer Policies

- Strategic customer rules
- SLA protection rules
- Customer prioritization rules

---

### Commercial Policies

- Cost approval thresholds
- Expedite approval thresholds

---

### Escalation Policies

- Manual review conditions
- Approval routing rules

---

## Decision Precedence Framework

The Supervisor applies policy decisions using the following precedence order.

### Priority 1

Safety or Quality Restriction

Examples:

- Quality hold inventory
- Regulatory restrictions

---

### Priority 2

Strategic or SLA-Protected Customer Commitments

Examples:

- Strategic customers
- SLA-protected orders

---

### Priority 3

Supplier Approval Restrictions

Examples:

- Unapproved alternate suppliers
- Qualification restrictions

---

### Priority 4

Inventory Availability and Timing

Examples:

- Inventory shortages
- ATP limitations
- Recovery timing constraints

---

### Priority 5

Commercial Approval Requirements

Examples:

- Cost premium approvals
- Expedite premium approvals

---

### Priority 6

Cost Optimization

Examples:

- Lower-cost sourcing options
- Cost reduction opportunities

---

### Priority 7

Lower-Priority Customer Convenience

Examples:

- Standard customer requests
- Non-critical fulfillment preferences

---

## Execution Workflow

### Step 1 – Retrieve Disruption Request

The Supervisor retrieves the oldest disruption request with:

```text
Status = Pending
```

The disruption becomes the active case.

---

### Step 2 – Validation

Invoke:

```text
Disruption Intake & Validation Topic
```

Possible outcomes:

- PASS
- FAIL

If validation fails:

- Stop execution
- Record failure
- Do not continue

---

### Step 3 – Fan-Out Specialist Assessments

Launch the following specialists in parallel:

- Inventory Impact Specialist
- Alternate Supplier Specialist
- Customer & Order Impact Specialist
- Commercial Impact Specialist

This minimizes assessment time.

---

### Step 4 – Consolidate Findings

Collect specialist outputs.

Review:

- Risks
- Recommendations
- Constraints
- Approval requirements
- Evidence sufficiency

---

### Step 5 – Resolve Missing Evidence

If any specialist returns:

```text
AssessmentStatus = Insufficient Evidence
```

The Supervisor:

- Records the issue
- Determines reassessment need
- Escalates when required

The Supervisor must not invent missing information.

---

### Step 6 – Recovery Planning

Invoke:

```text
Recovery Planning Specialist
```

Inputs:

- Inventory findings
- Supplier findings
- Customer findings
- Commercial findings

Outputs:

- ProposedStrategy
- ResidualRisk
- RequiredApprovals
- RequiredActions

---

### Step 7 – Recovery Strategy Resolution

Invoke:

```text
Recovery Strategy Resolution Topic
```

Possible outcomes:

- Branch A
- Branch B
- Branch C
- Branch D
- Branch E

The topic determines the approved recovery path.

---

### Step 8 – Approval Determination

Invoke:

```text
Approval, Exception & Selective Reassessment Topic
```

Possible outcomes:

- Approved Route
- Awaiting Approval
- Manual Review

---

### Step 9 – Final Recommendation

Generate final recommendation.

Possible statuses:

- Approved Route
- Awaiting Approval
- Escalated
- Manual Review

---

### Step 10 – Reporting & Communication

Invoke:

```text
Reporting & Communication Specialist
```

The specialist:

- Generates report
- Sends notifications
- Returns execution status

---

### Step 11 – Update Final Status

Update disruption case status.

Examples:

```text
Approved Route
Awaiting Approval
Escalated
Manual Review
Closed
```

---

## Failure Handling Strategy

### Validation Failure

Action:

- Stop workflow

---

### Specialist Failure

Action:

- Record failure
- Request reassessment when allowed
- Escalate when required

---

### Missing Evidence

Action:

- Do not invent findings
- Record insufficient evidence
- Escalate if necessary

---

### Policy Conflict

Action:

- Apply precedence framework
- Escalate unresolved conflicts

---

### Reassessment Limit Reached

Condition:

```text
ReassessmentCycleCount >= 2
```

Action:

```text
Manual Review
```

---

## Governance Principles

The Supervisor follows the following governance principles:

### Evidence First

All decisions must be supported by specialist findings or workbook data.

### No Assumptions

Missing information must never be fabricated.

### Policy Before Optimization

Policy compliance takes precedence over cost optimization.

### Escalate When Required

The Supervisor must escalate whenever policy requirements cannot be satisfied.

### Recommendations Are Not Actions

The Supervisor may recommend actions but must never execute governed business decisions.

---

## Inputs

Primary inputs received by the Supervisor include:

- Disruption Requests
- Specialist Assessments
- Policy Knowledge Base
- Topic Outputs
- Approval Status Information

---

## Outputs

The Supervisor produces:

- Final Recommendation
- Recovery Strategy
- Approval Path
- Escalation Decision
- Manual Review Decision
- Reporting Request
- Final Disruption Status

---

## Key Design Benefits

The Supervisor design provides:

- Clear separation of responsibilities
- Controlled governance
- Policy-driven decisions
- Explainable recommendations
- Auditability
- Scalable orchestration
- Consistent disruption management

The Supervisor acts as the central decision-governance layer while ensuring all domain expertise remains within the appropriate specialist agents.

---