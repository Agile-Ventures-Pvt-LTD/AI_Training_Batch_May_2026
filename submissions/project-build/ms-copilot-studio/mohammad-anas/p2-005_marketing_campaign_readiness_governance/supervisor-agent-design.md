# Supervisor Agent Design

## Agent Name

Anas_Market_Campaign Readiness Governance


---

# Purpose

The Campaign Readiness Supervisor is the central orchestration agent responsible for managing the complete Marketing Campaign Readiness Assessment workflow.

Rather than performing business analysis itself, the Supervisor coordinates workflow execution, invokes workflow topics, delegates specialist assessments, validates governance requirements, consolidates findings, determines the final campaign readiness decision, and authorizes reporting and stakeholder communication.

The Supervisor acts as the single source of orchestration and governance throughout the assessment lifecycle.

---

# Design Philosophy

The implementation follows the Supervisor–Specialist architecture.

Business intelligence is distributed among specialist child agents while orchestration responsibilities remain centralized within the Supervisor.

This separation provides:

- Clear responsibility boundaries
- Modular workflow execution
- Better maintainability
- Reusable specialist agents
- Enterprise governance
- Consistent decision making

The Supervisor never replaces specialist agents and never performs domain-specific analysis directly.

---

# Responsibilities

The Supervisor is responsible for:

- Initiating the campaign readiness workflow
- Managing campaign lifecycle state
- Coordinating workflow topics
- Delegating specialist assessments
- Waiting for specialist completion
- Consolidating specialist findings
- Validating governance requirements
- Resolving conflicting specialist assessments
- Determining the final campaign readiness decision
- Authorizing report generation
- Authorizing stakeholder notification
- Updating campaign lifecycle status
- Returning the completed assessment

---

# Workflow Orchestration

The Supervisor executes the following workflow.

```
Recurrence Trigger
        │
        ▼
Campaign Intake & Validation
        │
        ▼
Update Campaign Status
        │
        ▼
Specialist Assessment
        │
        ▼
Launch Risk & Decision
        │
        ▼
Remediation (Conditional)
        │
        ▼
Approval Finalisation (Conditional)
        │
        ▼
Reporting & Communication
        │
        ▼
Update Final Campaign Status
        │
        ▼
Workflow Complete
```

---

# Topic Coordination

The Supervisor coordinates the following workflow topics.

## Campaign Intake & Validation

Purpose

- Retrieve campaign requests
- Select oldest pending campaign
- Validate campaign information

---

## Specialist Assessment

Purpose

- Coordinate specialist execution
- Collect specialist findings
- Validate completion

---

## Launch Risk & Decision

Purpose

- Consolidate specialist findings
- Validate proposed readiness
- Determine whether remediation or approval is required

---

## Remediation & Selective Reassessment

Purpose

- Coordinate reassessment activities
- Execute only required reassessments

---

## Approval Finalisation

Purpose

- Manage mandatory approval workflow
- Record approval outcome

---

## Reporting & Communication

Purpose

- Coordinate report generation
- Coordinate stakeholder notification
- Finalize campaign lifecycle

---

# Child Agent Coordination

The Supervisor delegates responsibilities to six specialist agents.

## Budget & Commercial Specialist

Evaluates:

- Budget
- Budget Variance
- CPL
- Financial Approval
- Commercial Readiness

---

## Brand & Content Compliance Specialist

Evaluates:

- Brand Compliance
- Product Naming
- Claims
- Regulatory Sensitivity
- CTA
- Disclaimers

---

## Channel Readiness Specialist

Evaluates:

- Channel Readiness
- Operational Dependencies
- Tracking
- Lead Time
- Channel Risks

---

## Asset Readiness Specialist

Evaluates:

- Asset Availability
- QA Status
- Approval Status
- Missing Assets
- Production Readiness

---

## Launch Risk & Decision Specialist

Responsible for:

- Risk Classification
- Proposed Readiness
- Consolidated Risk Assessment

---

## Reporting & Communication Specialist

Responsible for:

- Report Generation
- Email Draft Creation
- Stakeholder Notification

---

# Microsoft 365 Tools

The Supervisor uses the following tools.

## List Campaign Requests

Purpose

Retrieve campaign records from the CampaignRequestsTable and identify the oldest campaign whose CampaignStatus is **Pending**.

---

## Get Campaign Row

Purpose

Retrieve the complete campaign record for the selected CampaignID.

---

## Update Campaign Status

Purpose

Update campaign lifecycle information after Supervisor authorization.

Typical updates include:

- In Assessment
- Ready
- Ready with Conditions
- Remediation Required
- Management Approval Required
- Not Ready
- Manual Review

---

# Decision Authority

Only the Supervisor is authorized to:

- Determine the final campaign readiness outcome
- Resolve conflicting specialist findings
- Require reassessment
- Require management approval
- Approve report generation
- Approve stakeholder communication
- Update campaign lifecycle status

No child agent is permitted to perform these actions.

---

# Failure Handling

The Supervisor validates every workflow stage before continuing.

If any mandatory workflow stage fails, the Supervisor terminates execution and returns the appropriate outcome.

Examples include:

- Campaign retrieval failure
- Campaign validation failure
- Missing specialist assessment
- Missing evidence
- Approval failure
- Reporting failure

The Supervisor never fabricates missing information and always preserves workflow traceability.

---

# Governance Rules

The Supervisor follows the NovaSphere Marketing Governance Policy.

Core governance principles include:

- One campaign processed per execution
- Mandatory validation before assessment
- Mandatory specialist execution
- Mandatory governance review
- Mandatory reporting authorization
- Complete traceability between specialist findings and final readiness decision

---

# Benefits

The Supervisor architecture provides:

- Centralized orchestration
- Controlled workflow execution
- Policy-driven governance
- Reusable specialist agents
- Clear separation of responsibilities
- Enterprise scalability
- Consistent decision making
- End-to-end auditability
- Modular workflow management