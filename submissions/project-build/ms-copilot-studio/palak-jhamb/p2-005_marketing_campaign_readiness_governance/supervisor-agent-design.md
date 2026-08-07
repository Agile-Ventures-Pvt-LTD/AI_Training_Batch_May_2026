# Supervisor Agent Design

## Overview

The **Campaign Readiness Supervisor** is the central orchestration agent of the Campaign Readiness Assessment solution. It is responsible for coordinating the complete campaign assessment lifecycle by invoking workflow topics, delegating domain-specific evaluations to specialist agents, consolidating assessment results, and determining the final campaign readiness outcome.

The Supervisor does not perform business-specific analysis itself. Instead, it orchestrates the execution of specialist agents and workflow topics while ensuring that the overall assessment follows the defined governance process.

---

# Primary Responsibilities

The Supervisor Agent is responsible for:

- Initiating the campaign readiness workflow.
- Invoking the Campaign Intake & Validation topic.
- Validating workflow progression.
- Coordinating specialist agent execution.
- Passing required inputs to specialist agents.
- Waiting for specialist assessments to complete.
- Consolidating assessment results.
- Invoking the Launch Risk & Decision Specialist.
- Determining the overall workflow outcome.
- Triggering remediation or approval workflows when required.
- Invoking the Reporting & Communication Specialist.
- Completing the campaign assessment lifecycle.

---

# Architectural Role

```
Power Automate Trigger
        │
        ▼
Campaign Readiness Supervisor
        │
        ▼
Campaign Intake & Validation
        │
        ▼
Parallel Specialist Agents
        │
        ▼
Launch Risk & Decision
        │
        ▼
Workflow Decision
        │
        ▼
Reporting & Communication
```

The Supervisor serves as the single coordination point between all workflow components.

---

# Workflow Responsibilities

## Step 1 – Start Workflow

The Supervisor receives the trigger from Power Automate and starts a new campaign readiness assessment.

---

## Step 2 – Campaign Validation

The Supervisor invokes the **Campaign Intake & Validation** topic.

If validation fails:

- Stop workflow.
- Return validation errors.

If validation succeeds:

- Continue with specialist assessments.

---

## Step 3 – Parallel Specialist Assessment

The Supervisor invokes the following specialist agents in parallel:

- Budget & Commercial Specialist
- Brand & Content Compliance Specialist
- Channel Readiness Specialist
- Asset Readiness Specialist

The Supervisor waits until every specialist returns its assessment before continuing.

---

## Step 4 – Launch Risk Evaluation

After all specialist assessments are available, the Supervisor invokes the **Launch Risk & Decision Specialist**.

The Supervisor provides:

- Budget assessment
- Brand assessment
- Channel assessment
- Asset assessment
- Days Until Launch
- Geography
- Campaign Sensitivity
- Pending Approvals

The Launch Risk Specialist returns:

- Risk Level
- Readiness Recommendation
- Blocking Issues
- Conditions
- Supporting Evidence

---

## Step 5 – Workflow Decision

Based on the consolidated findings, the Supervisor determines the next workflow step.

Possible outcomes include:

- Ready
- Ready with Conditions
- Approval Required
- Remediation Required
- Not Ready

---

## Step 6 – Remediation

If remediation is required, the Supervisor invokes the **Remediation & Selective Reassessment** topic.

The topic returns updated specialist assessments after remediation.

---

## Step 7 – Approval

If management approval is required, the Supervisor invokes the **Approval & Finalization** topic.

The Supervisor waits for the approval outcome before continuing.

---

## Step 8 – Reporting

After the final readiness decision has been reached, the Supervisor invokes the **Reporting & Communication Specialist**.

The specialist generates:

- Campaign readiness report
- Executive summary
- Stakeholder notification

---

## Step 9 – Workflow Completion

The Supervisor completes the assessment by:

- Updating campaign status.
- Recording assessment completion.
- Returning the final readiness result.

---

# Delegation Strategy

The Supervisor delegates responsibilities according to business domains.

| Activity | Delegated To |
|-----------|--------------|
| Campaign Validation | Campaign Intake & Validation |
| Budget Assessment | Budget & Commercial Specialist |
| Brand Compliance | Brand & Content Compliance Specialist |
| Channel Assessment | Channel Readiness Specialist |
| Asset Assessment | Asset Readiness Specialist |
| Risk Evaluation | Launch Risk & Decision Specialist |
| Reporting | Reporting & Communication Specialist |

---

# Information Passed to Specialists

The Supervisor passes only the information required by each specialist.

### Budget & Commercial

- Campaign ID

---

### Brand & Content Compliance

- Campaign ID

---

### Channel Readiness

- Campaign ID

---

### Asset Readiness

- Campaign ID

---

### Launch Risk & Decision

- Budget Assessment
- Brand Assessment
- Channel Assessment
- Asset Assessment
- Days Until Launch
- Geography
- Campaign Sensitivity
- Pending Approvals

---

### Reporting & Communication

- Final Readiness Decision
- Specialist Assessments
- Campaign Information
- Risk Assessment

---

# Decision Logic

The Supervisor evaluates workflow progression using specialist outputs.

```
Campaign Validation
        │
        ▼
Specialist Assessments
        │
        ▼
Launch Risk Evaluation
        │
        ▼
Supervisor Decision
        │
        ├── Ready
        ├── Ready with Conditions
        ├── Approval Required
        ├── Remediation Required
        └── Not Ready
```

---

# Orchestration Pattern

The Supervisor combines sequential and parallel orchestration.

### Sequential Stages

1. Campaign Intake & Validation
2. Launch Risk & Decision
3. Reporting & Communication

### Parallel Stage

The following specialists execute simultaneously:

- Budget & Commercial
- Brand & Content Compliance
- Channel Readiness
- Asset Readiness

The Supervisor synchronizes all specialist outputs before continuing.

---

# Design Rules

The Supervisor follows these operational rules:

- Never perform specialist evaluations directly.
- Always invoke Campaign Intake & Validation before assessment.
- Execute independent specialist agents in parallel.
- Wait for all required specialist outputs before invoking Launch Risk.
- Invoke remediation only when required.
- Invoke approval only when required.
- Generate reports only after the final readiness decision.
- Base every workflow decision on specialist evidence.

---

# Benefits

The Supervisor-centric architecture provides:

- Centralized workflow management.
- Consistent decision-making.
- Modular specialist integration.
- Parallel assessment execution.
- Reduced coupling between business domains.
- Simplified maintenance.
- Improved scalability.
- Enterprise-ready orchestration.

---

# Current Implementation

The Supervisor Agent currently supports:

- Autonomous workflow initiation.
- Campaign validation orchestration.
- Specialist agent coordination.
- Parallel execution management.
- Launch risk evaluation.
- Reporting orchestration.
- Power Automate integration.
- Microsoft Copilot Studio Generative Orchestration.

---

# Conclusion

The Campaign Readiness Supervisor acts as the orchestration layer of the solution, coordinating every stage of the campaign readiness assessment lifecycle. By separating workflow management from domain-specific evaluation, the Supervisor enables scalable, maintainable, and autonomous execution of complex marketing campaign assessments while ensuring that every readiness decision is supported by structured evidence from the specialist agents.