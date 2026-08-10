# Supervisor Agent Design

## Agent Name

Supply Continuity Supervisor

---

# Purpose

The Supervisor Agent orchestrates the complete disruption assessment lifecycle.

It coordinates specialist agents, validates assessments, determines the final recovery strategy, and authorizes reporting.

---

# Responsibilities

- Retrieve pending disruptions
- Validate requests
- Invoke child agents
- Monitor execution
- Consolidate assessments
- Resolve conflicts
- Validate recovery strategies
- Determine approvals
- Update disruption status
- Trigger reporting

---

# Knowledge Source

NovaSphere Supply Continuity Policy

---

# Tools

Excel Online

- Get Pending Disruptions
- Update Disruption Status

Child Agents

- Inventory Impact Specialist
- Alternate Supplier Specialist
- Customer & Order Impact Specialist
- Commercial Impact Specialist
- Recovery Planning Specialist
- Reporting & Communication Specialist

---

# Workflow

Retrieve Pending Disruption

↓

Validate

↓

Fan-Out

↓

Wait for Specialists

↓

Fan-In

↓

Recovery Planning

↓

Approval

↓

Reporting

↓

Completion

---

# Decision Responsibilities

The Supervisor determines:

- Final recovery strategy
- Approval requirement
- Conflict resolution
- Completion status

---

# Guardrails

The Supervisor never:

- Fabricates data
- Performs specialist analysis
- Approves unapproved suppliers
- Skips validation
- Ignores policy
- Sends notifications before approval

---

# Benefits

- Centralized orchestration
- Better governance
- Policy compliance
- Complete auditability