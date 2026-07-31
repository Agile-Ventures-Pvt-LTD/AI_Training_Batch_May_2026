# Supervisor Agent Design

## Overview

The BC/DR Supervisor Agent is the central orchestrator of the Autonomous Multi-Agent BC/DR Readiness Assessment System. It manages the complete assessment workflow by retrieving assessment requests, coordinating specialist agents, consolidating their outputs, and producing the final BC/DR readiness assessment.

The Supervisor Agent does not perform detailed business or technical analysis itself. Instead, it delegates specific tasks to the appropriate specialist agents and combines their results into a single assessment.

---

# Purpose

The primary purpose of the Supervisor Agent is to:

- Initiate the BC/DR assessment workflow.
- Coordinate all specialist agents.
- Manage assessment execution.
- Validate collected information.
- Consolidate assessment findings.
- Produce the final readiness decision.

---

# Responsibilities

The Supervisor Agent is responsible for:

- Monitoring incoming assessment requests through the configured trigger.
- Reading application details from the Excel workbook.
- Delegating assessment tasks to specialist agents.
- Collecting responses from each specialist.
- Validating the completeness of assessment results.
- Determining the overall BC/DR readiness classification.
- Initiating report generation.
- Updating the Assessment Register.
- Triggering stakeholder notifications.

---

# Inputs

The Supervisor Agent receives information from:

- Assessment Requests worksheet
- Application Inventory worksheet
- Organizational BC/DR policy
- Specialist agent responses
- Microsoft Learn MCP findings (via the Technical Recovery Specialist)

---

# Outputs

The Supervisor Agent produces:

- Overall BC/DR readiness classification
- Consolidated assessment findings
- Assessment summary
- Instructions for report generation
- Assessment Register updates
- Notification request for stakeholders

---

# Child Agents

The Supervisor Agent delegates work to the following specialist agents:

1. Application Criticality Specialist
2. Recovery Requirements Specialist
3. Technical Recovery Specialist
4. Risk & Recovery Gap Specialist
5. Remediation Planning Specialist
6. Reporting & Communication Specialist

---

# Workflow

1. Receive trigger activation.
2. Read pending assessment requests.
3. Retrieve application details.
4. Invoke the Application Criticality Specialist.
5. Invoke the Recovery Requirements Specialist.
6. Invoke the Technical Recovery Specialist.
7. Receive Microsoft Learn MCP findings.
8. Invoke the Risk & Recovery Gap Specialist.
9. Invoke the Remediation Planning Specialist.
10. Validate all specialist responses.
11. Determine the overall BC/DR readiness status.
12. Instruct the Reporting & Communication Specialist to generate the assessment report.
13. Update the Assessment Register.
14. Complete the workflow.

---

# Decision Logic

The Supervisor Agent:

- Ensures all required specialist assessments are completed.
- Checks for missing or conflicting information.
- Consolidates findings into a single readiness assessment.
- Returns **Insufficient Evidence** when mandatory information is unavailable instead of making unsupported assumptions.

---

# Tools Used

- Excel Online
  - Read Assessment Requests
  - Read Application Inventory
  - Update Assessment Register

The Supervisor Agent does not directly access the Microsoft Learn MCP Server. Technical validation is performed by the Technical Recovery Specialist.

---

# Benefits

- Centralized workflow orchestration.
- Clear separation of responsibilities.
- Consistent assessment execution.
- Improved scalability through modular agent design.
- Reliable coordination between specialist agents.
- Standardized and repeatable BC/DR readiness assessments.