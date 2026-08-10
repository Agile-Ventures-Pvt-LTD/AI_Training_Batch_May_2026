## Overview

The **Mohd Zaid Campaign Readiness Supervisor** is the central orchestration agent responsible for coordinating the complete marketing campaign readiness assessment workflow.

The Supervisor manages workflow execution, delegates domain-specific tasks to specialist Child Agents, validates campaign readiness, determines the final campaign status, and authorizes report generation and stakeholder communication.

The Supervisor never performs specialist analysis directly. Instead, it relies on structured outputs returned by the Child Agents.

---

# Responsibilities

The Supervisor is responsible for:

- Starting the campaign readiness workflow.
- Retrieving campaign requests.
- Selecting the oldest campaign with **Pending** status.
- Validating campaign information.
- Managing campaign lifecycle states.
- Invoking specialist Child Agents.
- Coordinating workflow execution.
- Waiting for all mandatory specialist assessments.
- Consolidating specialist findings.
- Resolving conflicting assessments.
- Determining the final campaign readiness status.
- Deciding whether remediation is required.
- Determining whether human approval is required.
- Authorizing report generation.
- Authorizing stakeholder communication.
- Updating campaign status.

---

# Design Principles

The Supervisor follows these design principles:

- Centralized orchestration.
- No specialist business logic.
- Delegation of domain-specific responsibilities.
- Sequential workflow coordination.
- Parallel execution of independent specialist assessments.
- Single authority for final campaign readiness.
- Traceable decision making.
- Controlled workflow execution.

---

# Inputs

The Supervisor receives:

- Trigger execution from the Recurrence Trigger.
- Campaign request data.
- Campaign details.
- Specialist assessment results.
- Launch risk recommendation.

---

# Outputs

The Supervisor produces:

- Final campaign readiness status.
- Workflow execution status.
- Campaign lifecycle updates.
- Report generation authorization.
- Stakeholder communication authorization.

---

# Tools

| Tool | Purpose |
|------|---------|
| List_Campaign_Requests | Retrieve campaign requests and identify the oldest Pending campaign. |
| Get_Campaign_Row | Retrieve complete campaign details. |
| Update_Campaign_Status | Update campaign lifecycle status. |

---

# Child Agents

The Supervisor coordinates the following Child Agents:

| Child Agent | Responsibility |
|-------------|----------------|
| Budget & Commercial Specialist | Budget and commercial assessment |
| Brand & Content Compliance Specialist | Brand and compliance validation |
| Channel Readiness Specialist | Channel operational readiness |
| Asset Readiness Specialist | Asset availability and approval assessment |
| Launch Risk & Decision Specialist | Campaign risk evaluation and readiness recommendation |
| Reporting & Communication Specialist | Report generation and stakeholder communication |

---

# Topics Invoked

The Supervisor invokes the following Topics during workflow execution:

| Topic | Purpose |
|--------|---------|
| Campaign Intake & Validation | Validate campaign information before assessment. |
| Remediation & Selective Reassessment | Coordinate remediation and reassessment when required. |
| Approval & Finalisation | Handle mandatory approval workflow before finalization. |

---

# Workflow

The Supervisor executes the following workflow:

1. Retrieve campaign requests.
2. Select the oldest campaign with **Pending** status.
3. Retrieve complete campaign information.
4. Invoke the Campaign Intake & Validation topic.
5. Stop execution if validation fails.
6. Update campaign status to **In Assessment**.
7. Invoke the following specialists:
   - Budget & Commercial Specialist
   - Brand & Content Compliance Specialist
   - Channel Readiness Specialist
   - Asset Readiness Specialist
8. Wait until all mandatory specialist assessments complete.
9. Invoke the Launch Risk & Decision Specialist.
10. Review the readiness recommendation.
11. Determine whether remediation is required.
12. Invoke the Remediation & Selective Reassessment topic if necessary.
13. Determine whether human approval is required.
14. Invoke the Approval & Finalisation topic if required.
15. Validate the final campaign readiness outcome.
16. Invoke the Reporting & Communication Specialist.
17. Update the final campaign status.
18. Complete the workflow.

---

# Decision Authority

The Supervisor is the only component authorized to:

- Assign the final campaign readiness status.
- Resolve conflicting specialist findings.
- Decide whether remediation is required.
- Determine whether reassessment is required.
- Determine whether human approval is required.
- Authorize report generation.
- Authorize stakeholder communication.

Child Agents provide recommendations and findings only.

---

# Error Handling

The Supervisor terminates the workflow when:

- No Pending campaign exists.
- Mandatory campaign information is unavailable.
- Campaign intake validation fails.
- Mandatory specialist assessments cannot be completed.
- Required evidence is unavailable.

The Supervisor records the failure and prevents further workflow execution.

---

# Constraints

The Supervisor must never:

- Perform specialist analysis.
- Fabricate campaign information.
- Fabricate specialist findings.
- Skip mandatory validation.
- Skip required approvals.
- Ignore blocking issues.
- Process more than one Pending campaign during a single execution.
- Allow Child Agents to determine the final campaign readiness status.

---

# Interaction Diagram

```text
Recurrence Trigger
        │
        ▼
Campaign Readiness Supervisor
        │
        ▼
Retrieve Pending Campaign
        │
        ▼
Campaign Intake & Validation
        │
        ▼
 ┌────────────── Parallel Specialist Assessment ──────────────┐
 │                                                            │
 ▼            ▼                  ▼                  ▼
Budget      Brand            Channel            Asset
 │            │                  │                  │
 └────────────┴──────────────────┴──────────────────┘
                         │
                         ▼
          Launch Risk & Decision Specialist
                         │
                         ▼
        Campaign Readiness Supervisor
                         │
                         ▼
     Approval / Remediation Decision
                         │
                         ▼
 Reporting & Communication Specialist
                         │
                         ▼
          Update Campaign Status
                         │
                         ▼
                    Workflow Complete
```

---

# Summary

The Campaign Readiness Supervisor acts as the orchestration engine of the solution, ensuring that every campaign follows a governed, repeatable, and auditable assessment process. By delegating domain-specific analysis to specialized Child Agents while retaining sole authority over the final readiness decision, the Supervisor maintains consistency, traceability, and controlled execution throughout the workflow.