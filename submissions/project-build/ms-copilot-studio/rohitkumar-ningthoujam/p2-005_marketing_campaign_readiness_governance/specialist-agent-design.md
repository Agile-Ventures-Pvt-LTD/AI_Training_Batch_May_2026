# Specialist Agent Design

## Overview

The Campaign Readiness Supervisor delegates domain-specific assessments to six specialist child agents. Each specialist evaluates a specific governance area and returns structured outputs to the supervisor for final consolidation and readiness determination.

---

# Child Specialist Agents

## 1. Budget & Commercial Specialist

### Purpose
Evaluates campaign budgets against organisational governance policies.

### Responsibilities

- Validate approved budget
- Calculate budget variance
- Determine approval requirements
- Evaluate commercial compliance

### Outputs

- BudgetStatus
- BudgetVariance
- ApprovalRequired

---

## 2. Brand & Content Compliance Specialist

### Purpose
Validates campaign content against brand and regulatory standards.

### Responsibilities

- Brand compliance review
- Regulatory validation
- High-sensitivity content detection
- Required review identification

### Outputs

- BrandStatus
- ComplianceIssues
- ReviewRequired

---

## 3. Channel Readiness Specialist

### Purpose

Validates readiness of all selected campaign channels.

### Responsibilities

- Assess every selected channel
- Verify channel-specific requirements
- Detect missing channel configurations

### Outputs

- ChannelStatus
- ChannelIssues

---

## 4. Asset Readiness Specialist

### Purpose

Ensures all mandatory campaign assets are available before launch.

### Responsibilities

- Verify mandatory assets
- Detect missing deliverables
- Assess launch dependencies

### Outputs

- AssetStatus
- MissingAssets

---

## 5. Launch Risk & Decision Specialist

### Purpose

Consolidates specialist assessment results and determines overall campaign readiness.

### Responsibilities

- Aggregate assessment outputs
- Evaluate launch risk
- Apply decision logic
- Produce Final Readiness

### Outputs

- FinalReadiness
- RiskLevel
- RecommendedAction

Possible values:

- Ready
- Ready with Conditions
- Remediation Required
- Not Ready

---

## 6. Reporting & Communication Specialist

### Purpose

Generates final deliverables after readiness is determined.

### Responsibilities

- Generate Microsoft Word readiness report
- Prepare stakeholder communication
- Support Outlook notification

### Outputs

- Word report
- Notification content

---

# Orchestration Model

The Campaign Readiness Supervisor coordinates all specialist agents while custom topics manage the overall workflow.

```
Campaign Readiness Supervisor
│
├── Topic 1 – Campaign Intake & Validation
│
├── Budget & Commercial Specialist
├── Brand & Content Compliance Specialist
├── Channel Readiness Specialist
├── Asset Readiness Specialist
├── Launch Risk & Decision Specialist
├── Topic 2 – Remediation & Selective Reassessment
├── Reporting & Communication Specialist
└── Topic 3 – Approval & Finalisation
```

Each specialist performs an independent assessment and returns structured outputs. The supervisor consolidates these results, applies governance rules, manages remediation when necessary, and determines the final campaign readiness decision.