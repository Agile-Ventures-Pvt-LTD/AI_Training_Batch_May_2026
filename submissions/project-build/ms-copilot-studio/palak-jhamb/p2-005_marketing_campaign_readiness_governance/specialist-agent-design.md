# Specialist Agent Design

## Overview

The Campaign Readiness Assessment Supervisor follows a **Supervisor–Specialist Agent** architecture. Rather than performing every assessment itself, the Supervisor delegates domain-specific responsibilities to independent specialist agents.

Each specialist is designed around the **Single Responsibility Principle**, ensuring that it evaluates only one business domain. Specialists perform their assessment independently, return a standardized response, and never determine the final campaign readiness status. The Supervisor consolidates all specialist outputs to make the final decision.

---

# Design Principles

All specialist agents follow the same architectural principles.

- Single business responsibility.
- Independent decision making.
- Evidence-based assessment.
- Standardized output structure.
- Read-only access to campaign data.
- No direct communication with other specialists.
- No authority to determine final campaign readiness.
- All findings returned to the Supervisor Agent.

---

# Standard Specialist Workflow

```
Supervisor
      │
      ▼
Receive Assessment Request
      │
      ▼
Retrieve Required Data
      │
      ▼
Evaluate Assigned Domain
      │
      ▼
Generate Findings
      │
      ▼
Return Standardized Assessment
      │
      ▼
Supervisor Consolidation
```

---

# Standard Output Structure

Every specialist returns a consistent output to simplify orchestration.

| Field | Description |
|--------|-------------|
| Assessment Status | Pass, Condition, Fail |
| Summary | Overall assessment summary |
| Findings | Key observations |
| Blocking Issues | Issues preventing campaign launch |
| Conditions | Non-blocking observations |
| Recommended Action | Suggested next steps |
| Supporting Evidence | Data used during assessment |

---

# Specialist 1 – Budget & Commercial

## Purpose

The Budget & Commercial Specialist evaluates the financial readiness of the campaign and determines whether the proposed campaign budget satisfies organizational budget policies.

---

## Responsibilities

The specialist evaluates:

- Proposed Budget
- Approved Budget
- Budget Variance
- Target CPL
- Expected Leads
- Required Financial Approval
- Budget Blocking Conditions

---

## Data Sources

- Campaign Requests
- Budget Rules
- Approval Matrix

---

## Tools

- Get Campaign Request
- Get Budget Rules
- Get Approval Matrix

---

## Output

Returns:

- Assessment Status
- Proposed Budget
- Approved Budget
- Budget Variance
- CPL Assessment
- Approval Required
- Required Approver
- Blocking Issues
- Recommended Action
- Supporting Evidence

---

# Specialist 2 – Brand & Content Compliance

## Purpose

The Brand & Content Compliance Specialist verifies that campaign content complies with organizational branding standards and regulatory requirements.

---

## Responsibilities

The specialist evaluates:

- Brand guideline compliance
- Mandatory disclaimers
- Required approvals
- Content review status
- Regulatory compliance
- Missing mandatory content
- Brand launch blockers

---

## Data Sources

- Campaign Requests
- Brand Guidelines
- Content Review

---

## Tools

- Get Brand Guidelines
- Get Content Review

---

## Output

Returns:

- Assessment Status
- Brand Compliance
- Content Review Status
- Missing Requirements
- Approval Required
- Blocking Issues
- Recommended Action
- Supporting Evidence

---

# Specialist 3 – Channel Readiness

## Purpose

The Channel Readiness Specialist determines whether every marketing channel included in the campaign satisfies its launch requirements.

---

## Responsibilities

The specialist evaluates:

- Mandatory channel assets
- Lead time requirements
- Tracking requirements
- Channel ownership
- Brand approval requirements
- Missing prerequisites
- Channel launch blockers

Every channel included in the campaign is evaluated independently.

---

## Data Sources

- Campaign Requests
- Channel Requirements
- Asset Status

---

## Tools

- Get Channel Requirements
- Get Asset Status

---

## Output

Returns:

- Assessment Status
- Channel Evaluations
- Missing Prerequisites
- Tracking Status
- Blocking Issues
- Recommended Action
- Supporting Evidence

---

# Specialist 4 – Asset Readiness

## Purpose

The Asset Readiness Specialist verifies that every mandatory campaign asset is available, approved, and ready for launch.

---

## Responsibilities

The specialist evaluates:

- Asset Availability
- Approval Status
- QA Status
- Missing Assets
- Pending Approvals
- Assets Requiring Changes
- Responsible Owners

---

## Asset Classification

Each asset is classified as:

- Ready
- Conditional
- Blocking
- Missing

---

## Data Sources

- Campaign Requests
- Asset Status
- Approval Records

---

## Tools

- Get Asset Status
- Get Asset Approvals

---

## Output

Returns:

- Assessment Status
- Asset Summary
- Ready Assets
- Conditional Assets
- Blocking Assets
- Missing Assets
- Responsible Owners
- Aggregate Counts
- Recommended Action
- Supporting Evidence

---

# Specialist 5 – Launch Risk & Decision

## Purpose

The Launch Risk & Decision Specialist consolidates specialist findings and evaluates the overall launch risk of the campaign.

This specialist executes only after the Budget, Brand, Channel, and Asset specialists complete their assessments.

---

## Inputs

Receives:

- Budget Assessment
- Brand Assessment
- Channel Assessment
- Asset Assessment
- Days Until Launch
- Geography
- Campaign Sensitivity
- Pending Approvals

---

## Responsibilities

The specialist evaluates:

- Blocking Issues
- Non-blocking Conditions
- Approval Requirements
- Timing Risks
- Unresolved Evidence
- Campaign Risk Level

---

## Risk Levels

The campaign is classified as:

- Low
- Medium
- High
- Critical

---

## Output

Returns:

- Assessment Status
- Risk Level
- Readiness Recommendation
- Blocking Issues
- Conditions
- Approval Requirements
- Supporting Evidence

---

# Specialist 6 – Reporting & Communication

## Purpose

The Reporting & Communication Specialist prepares the final campaign readiness report and communicates the outcome to stakeholders.

---

## Responsibilities

The specialist:

- Consolidates assessment findings.
- Generates campaign readiness reports.
- Produces executive summaries.
- Prepares stakeholder communications.
- Updates workflow completion status.

---

## Data Sources

- Supervisor Assessment
- Specialist Results
- Campaign Information

---

## Tools

- Generate Word Report
- Send Outlook Notification

---

## Output

Returns:

- Report Status
- Report Location
- Notification Status
- Communication Summary

---

# Interaction Model

Specialists never communicate directly with one another.

```
                    Supervisor
                         │
      ┌──────────────────┼──────────────────┐
      ▼                  ▼                  ▼
 Budget           Brand Compliance      Channel
      │
      ▼
 Asset
      │
      ▼
 Launch Risk
      │
      ▼
 Reporting
```

The Supervisor acts as the single coordination point for all specialist interactions.

---

# Benefits of the Design

The specialist-agent architecture provides:

- Clear separation of responsibilities.
- Independent business evaluations.
- Simplified maintenance.
- Reusable specialist agents.
- Parallel execution of independent assessments.
- Consistent assessment outputs.
- Improved scalability.
- Reduced coupling between workflow components.

---

# Conclusion

The Campaign Readiness Assessment Supervisor employs six dedicated specialist agents, each responsible for a distinct aspect of campaign readiness. By separating domain-specific evaluation from workflow orchestration, the solution achieves a modular, scalable, and maintainable architecture. Standardized outputs and centralized coordination by the Supervisor ensure consistent decision-making while enabling efficient execution of complex marketing campaign assessments.