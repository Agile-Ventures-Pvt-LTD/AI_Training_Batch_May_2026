# Test Report

## Project

Supply Continuity Disruption Response Agent
Microsoft Copilot Studio Multi-Agent Workflow

---

## Objective

Validate the end-to-end execution of the Supply Continuity Supervisor workflow, including:

- Disruption intake and validation
- Specialist assessment orchestration
- Recovery strategy selection
- Approval routing
- Escalation handling
- Manual review governance
- Report generation
- Stakeholder notification
- End-to-end workflow execution

---

## Test Environment

| Component | Status |
|---|---|
| Microsoft Copilot Studio | Configured |
| Supervisor Agent | Configured |
| Custom Topics | Configured |
| Knowledge Base | Configured |
| Excel Data Source | Connected |
| Power Automate Actions | Configured |
| Outlook Integration | Configured |
| Reporting Workflow | Configured |

---

## Test Methodology

Testing was performed using Copilot Studio Evaluation.

Each test case was evaluated against:

- General Quality
- Tool Usage

The objective was to verify that the Supervisor correctly:

- Retrieves disruption data
- Executes workflow logic
- Invokes appropriate topics and specialists
- Applies governance rules
- Produces expected workflow outcomes

---

## Test Cases

### TC-01 � Existing Inventory Recovery

#### Scenario

A disruption request exists with valid data, sufficient inventory available, and no approval requirements.

#### Expected Result

- Validation passes
- Inventory assessment recommends existing inventory
- Recovery Strategy Resolution selects Branch A
- Approval Topic returns Approved Route
- Report generated
- Notification sent

#### Actual Result

Evaluation scenario executed.

No automated result recorded by evaluation.

#### Status

> **Not Evaluated**

---

### TC-02 � Partial Fulfillment Recovery

#### Scenario

A disruption request exists with medium inventory risk requiring partial fulfillment.

#### Expected Result

- Validation passes
- Inventory specialist identifies partial inventory availability
- Recovery Strategy Resolution selects Branch B
- Approval Topic returns Approved Route
- Report generated
- Notification sent

#### Actual Result

Agent requested additional disruption information:

> *"Please provide the date when the disruption was reported."*

#### Evaluation Results

| Check | Result |
|---|---|
| General Quality | Pass |
| Tool Usage | Fail |

#### Tool Usage Observation

**Used:**
- Get oldest pending row present in table

**Not Used:**
- Disruption Intake & Validation Topic

#### Status

> **Fail**

#### Root Cause

Required disruption data was not available to continue workflow execution, causing the Supervisor to request additional information instead of continuing autonomously.

---

### TC-03 � Approved Alternate Supplier

#### Scenario

An approved alternate supplier exists and is eligible for recovery.

#### Expected Result

- Validation passes
- Supplier specialist identifies approved supplier
- Recovery Strategy Resolution selects Branch C
- Approval routing determined appropriately
- Workflow continues

#### Actual Result

Evaluation scenario executed.

No automated result recorded by evaluation.

#### Status

> **Not Evaluated**

---

### TC-04 � Unapproved Alternate Supplier

#### Scenario

Only an unapproved alternate supplier is available.

#### Expected Result

- Validation passes
- Supplier specialist identifies unapproved supplier
- Recovery Strategy Resolution selects Branch D
- EscalationRequired = True
- Approval or escalation path triggered

#### Actual Result

Evaluation scenario executed.

No automated result recorded by evaluation.

#### Status

> **Not Evaluated**

---

### TC-05 � Management Escalation

#### Scenario

Critical inventory risk exists and no alternate supplier is available.

#### Expected Result

- Validation passes
- No viable recovery path available
- Recovery Strategy Resolution selects Branch E
- EscalationRequired = True
- Management escalation recommended

#### Actual Result

Agent requested additional disruption information:

> *"What is the expected recovery date for the disruption?"*

#### Evaluation Results

| Check | Result |
|---|---|
| General Quality | Pass |
| Tool Usage | Fail |

#### Tool Usage Observation

**Used:**
- Get oldest pending row present in table

**Not Used:**
- Disruption Intake & Validation Topic

#### Status

> **Fail**

#### Root Cause

Missing disruption information prevented downstream workflow execution.

---

### TC-06 � Validation Failure

#### Scenario

Required disruption fields are missing.

#### Expected Result

- Validation topic returns FAIL
- Supervisor terminates workflow
- No specialist execution
- No report generation

#### Actual Result

Agent requested additional disruption information:

> *"What is the date when the disruption was reported?"*

#### Evaluation Results

| Check | Result |
|---|---|
| General Quality | Pass |
| Tool Usage | Fail |

#### Tool Usage Observation

**Used:**
- Get oldest pending row present in table

**Not Used:**
- Disruption Intake & Validation Topic

#### Status

> **Fail**

#### Root Cause

The evaluation dataset did not provide sufficient information for validation execution. The Supervisor requested missing data instead of executing the Validation Topic.

---

## Summary

| Metric | Value |
|---|---|
| Total Test Cases | 6 |
| General Quality Passes | 3 |
| General Quality Fails | 0 |
| Tool Usage Passes | 0 |
| Tool Usage Fails | 3 |
| Fully Successful End-to-End Executions | 0 |
| Incomplete Due to Missing Data | 3 |
| Not Evaluated by Framework | 3 |

---

## Findings

### Positive Findings

- Supervisor correctly attempted to retrieve disruption records.
- Responses remained relevant to workflow context.
- General Quality evaluation passed for all executed conversations.
- Governance prompts behaved as expected when required information was unavailable.

### Issues Identified

- Disruption Intake & Validation Topic was not invoked during evaluated runs.
- Several scenarios lacked required disruption attributes.
- Missing dates prevented workflow progression.
- End-to-end orchestration could not be fully validated through the evaluation dataset alone.

---

## Recommendations

1. Populate the Disruption Request table with complete test records.
2. Re-run evaluation using real disruption data instead of scenario descriptions.
3. Verify automatic invocation of the Validation Topic.
4. Execute end-to-end tests through the Power Automate trigger path.
5. Validate recovery strategy branch selection against actual workbook records.
6. Validate approval and reassessment routing with realistic approval scenarios.

---

## Conclusion

The evaluation confirms that the Supervisor can retrieve disruption records and maintain contextual workflow behavior. However, complete end-to-end validation was not achieved because multiple scenarios lacked the required disruption data needed to execute validation and specialist workflows. Additional testing using populated workbook records and trigger-based execution is recommended before production deployment.

---