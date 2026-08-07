# Supervisor Agent Design

## Overview

The Campaign Readiness Supervisor serves as the central orchestration agent for the Campaign Readiness Review solution.

The Supervisor coordinates all readiness activities, invokes specialist agents and supporting topics, applies governance policies, manages approvals and remediation, and determines the final readiness status.

The Supervisor is the only component authorized to assign a final campaign readiness outcome.

---

# Responsibilities

The Supervisor is responsible for:

- Campaign intake orchestration
- Validation execution
- Specialist coordination
- Specialist output consolidation
- Risk assessment orchestration
- Governance policy enforcement
- Approval routing
- Remediation management
- Reassessment orchestration
- Final readiness determination
- Report generation initiation
- Request Table Status updation

---

# Information Sources

The Supervisor uses:

## Knowledge Sources

- Governance Policy

## Topics

- Campaign Intake & Validation
- Approval & Finalization
- Remediation & Selective Reassessment

## Specialist Outputs

- Budget Assessment
- Brand Assessment
- Channel Assessment
- Asset Assessment
- Launch Risk Assessment

---

# Inputs

The Supervisor receives:

- Campaign information
- Validation results
- Specialist findings
- Risk assessments
- Approval outcomes
- Remediation outcomes
- Governance policies

---

# Outputs

The Supervisor produces:

- Final Readiness Status
- Approval Requirements
- Escalation Requirements
- Remediation Decisions
- Recommended Actions
- Final Campaign Summary

---

# Decision Authority

Only the Supervisor may:

- Determine final readiness
- Apply readiness precedence
- Escalate approvals
- Initiate reassessment
- Initiate reporting

Specialists may recommend outcomes but cannot assign final readiness.

---

# Execution Flow

## Step 1

Invoke:

Campaign Intake & Validation

---

## Step 2

If validation succeeds:

Invoke in parallel:

- Budget & Commercial Specialist
- Brand & Content Compliance Specialist
- Channel Readiness Specialist
- Asset Readiness Specialist

---

## Step 3

Wait for all specialist assessments.

---

## Step 4

Consolidate findings.

Review:

- Blocking Issues
- Conditions
- Required Actions
- Required Approvers
- Evidence
- Confidence

---

## Step 5

Invoke:

Launch Risk & Decision Specialist

---

## Step 6

Invoke:

Approval & Finalization Topic

When approvals are required.

---

## Step 7

Invoke:

Remediation & Selective Reassessment Topic

When blocking issues require correction.

---

## Step 8

Apply Governance Policy.

Determine:

- Final Readiness Status
- Escalations
- Next Actions

---

## Step 9

Invoke:

Reporting & Communication Specialist

---

## Step 10

Invoke:

Update a row Tool

Update:

    - Campaign Status of the selected campaign.

---

# Readiness Precedence Rules

The Supervisor applies the following precedence order:

1. Not Ready
2. Management Approval Required
3. Remediation Required
4. Ready With Conditions
5. Ready

The highest-precedence outcome always wins.

---

# Approval Handling

The Supervisor evaluates approval outcomes returned from the Approval & Finalization Topic.

Approval requirements may originate from:

- Budget conditions
- Governance requirements
- Specialist findings
- Risk findings

---

# Remediation Handling

The Supervisor manages reassessment cycles.

Maximum automated reassessment cycles:

2

After two unsuccessful reassessments:

Manual Review Required

---

# Final Readiness Determination

The final readiness outcome is determined after considering:

- Governance Policy
- Specialist findings
- Risk assessment
- Approval status
- Remediation status

Only the Supervisor may assign:

- Ready
- Ready With Conditions
- Remediation Required
- Management Approval Required
- Not Ready