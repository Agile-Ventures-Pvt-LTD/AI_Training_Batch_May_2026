# Specialised Agents

## Overview

The Autonomous Multi-Agent BC/DR Readiness Assessment System follows a multi-agent architecture where each specialist agent is responsible for a specific stage of the assessment process. This separation of responsibilities improves modularity, maintainability, and assessment accuracy. All specialist agents operate under the coordination of the BC/DR Supervisor Agent.

---

## 1. Application Criticality Specialist

### Purpose
Evaluates the business importance of an application and determines its overall business criticality.

### Responsibilities
- Analyze business impact.
- Evaluate customer impact.
- Assess financial and operational impact.
- Determine regulatory importance.
- Classify application criticality.

### Output
- Business Criticality Classification
- Criticality rationale
- Confidence level

---

## 2. Recovery Requirements Specialist

### Purpose
Evaluates whether the application's recovery objectives meet business continuity requirements.

### Responsibilities
- Validate Recovery Time Objective (RTO).
- Validate Recovery Point Objective (RPO).
- Identify recovery objective gaps.
- Evaluate dependency recovery order.
- Review recovery documentation.

### Output
- Recovery requirements assessment
- RTO/RPO gap analysis
- Recovery recommendations

---

## 3. Technical Recovery Specialist

### Purpose
Validates the application's technical recovery architecture using the Microsoft Learn MCP Server.

### Responsibilities
- Retrieve official Microsoft Learn documentation.
- Review backup and disaster recovery configurations.
- Compare the existing architecture with Microsoft best practices.
- Identify technical recovery gaps.
- Recommend improvements.

### Tools Used
- Microsoft Learn MCP Server

### Output
- Technical recovery assessment
- Microsoft guidance summary
- Technical recommendations

---

## 4. Risk & Recovery Gap Specialist

### Purpose
Identifies business and technical risks affecting BC/DR readiness.

### Responsibilities
- Review findings from specialist agents.
- Identify recovery gaps.
- Assign risk severity.
- Determine overall readiness recommendation.

### Output
- Risk assessment
- Recovery gap analysis
- Readiness recommendation

---

## 5. Remediation Planning Specialist

### Purpose
Converts identified gaps into actionable remediation activities.

### Responsibilities
- Prioritize remediation actions.
- Recommend ownership.
- Define validation requirements.
- Organize corrective actions based on priority.

### Output
- Remediation plan
- Action items
- Priority levels

---

## 6. Reporting & Communication Specialist

### Purpose
Generates the final assessment report and communicates assessment results.

### Responsibilities
- Generate the BC/DR Readiness Assessment Report.
- Update the Assessment Register.
- Send Outlook notifications.
- Summarize assessment findings.

### Tools Used
- Microsoft Word
- Microsoft Outlook

### Output
- Final assessment report
- Updated assessment register
- Stakeholder notifications

---

## Agent Collaboration

The specialist agents do not work independently. Each agent performs a dedicated task and returns its findings to the BC/DR Supervisor Agent. The Supervisor validates, consolidates, and combines these outputs to determine the final BC/DR readiness status.

This collaborative architecture enables consistent assessments, clear separation of responsibilities, and easier future enhancements.