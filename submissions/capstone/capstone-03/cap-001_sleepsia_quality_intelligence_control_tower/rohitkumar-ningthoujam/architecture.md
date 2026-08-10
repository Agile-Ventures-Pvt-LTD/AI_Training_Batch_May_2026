# Architecture

## 1. Solution Overview

The **Sleepsia Quality Intelligence Control Tower** is an autonomous multi-agent quality investigation solution built using **Microsoft Copilot Studio**.

The solution uses a central **Quality Supervisor** parent/orchestrator agent that receives quality investigation requests, validates the incident and complaint information, coordinates specialist child agents, consolidates their findings, determines the appropriate quality outcome, plans CAPA actions when required, and generates the final investigation report and notification.

The architecture follows a hierarchical multi-agent model where the Quality Supervisor controls the overall investigation while specialist agents perform focused analysis.

### Platform

- Microsoft Copilot Studio
- Excel Online (Business)
- Microsoft Word
- Microsoft Outlook
- Microsoft Learn MCP Server

### Solution Type

Autonomous Multi-Agent Quality Investigation and CAPA Management System.

---

## 2. High-Level Architecture

The overall architecture is:

User / Autonomous Trigger
        |
        v
Quality Supervisor
        |
        v
Incident Intake & Validation
        |
        v
Complaint / Incident Scope Identification
        |
        +----------------------+----------------------+----------------------+
        |                      |                      |                      |
        v                      v                      v                      v
Product/Batch Specialist  Complaint Pattern      Customer Impact       Safety Specialist
                          Specialist              Specialist
        |                      |                      |                      |
        +----------------------+----------------------+----------------------+
                               |
                               v
                       Quality Decision
                               |
                +--------------+--------------+
                |                             |
                v                             v
          CAPA Required                 No CAPA Required
                |
                v
          CAPA Specialist
                |
                v
        CAPA Register Update
                |
                +-----------------------------+
                                              |
                         +--------------------+--------------------+
                         |                                         |
                         v                                         v
                Word Report Tool                           Outlook Tool
                         |                                         |
                         +--------------------+--------------------+
                                              |
                                              v
                                      Final Outcome

---

## 3. Parent Agent Architecture

### Quality Supervisor

The **Quality Supervisor** is the central parent/orchestrator agent.

It is responsible for:

- Receiving quality investigation requests.
- Starting incident intake and validation.
- Checking whether the requested incident or complaint can be processed.
- Coordinating specialist child agents.
- Invoking specialist agents for independent analysis.
- Waiting for and consolidating specialist findings.
- Applying quality decision logic.
- Determining whether CAPA is required.
- Routing CAPA planning to the CAPA Specialist.
- Requesting report generation.
- Sending conditional quality investigation notifications.
- Returning the final investigation outcome to the requester.

The Quality Supervisor does not perform every specialist analysis itself. Instead, it delegates focused analysis to child agents and uses their outputs for the final decision.

---

## 4. Specialist Child Agent Architecture

The Quality Supervisor coordinates the following specialist agents.

### 4.1 Product/Batch Specialist

Purpose:

- Validate product information.
- Validate SKU against Product Master.
- Validate batch information.
- Review batch status.
- Identify relevant batch quality information.
- Identify previous incidents associated with the product or batch.

Primary data sources:

- Product Master table.
- Batch Register table.
- Quality Incidents table.

Primary tools:

- Get Product Master
- Get Batch Register
- Get Quality Incidents

---

### 4.2 Complaint Pattern Specialist

Purpose:

- Retrieve complaints related to the affected SKU and batch.
- Identify repeated complaint categories.
- Identify repeated failure modes.
- Count complaints.
- Identify affected orders/customers.
- Determine complaint clustering.
- Identify missing evidence.

Primary data source:

- Customer Complaints table.

Primary tool:

- Get Customer Complaints

The specialist returns structured complaint-pattern findings to the Quality Supervisor.

---

### 4.3 Customer Impact Specialist

Purpose:

- Assess customer impact from complaints and returns.
- Identify affected orders.
- Identify unique customers.
- Analyze return information.
- Determine return volume and impact.
- Identify customer-impact severity.

Primary data sources:

- Customer Complaints table.
- Returns table.

Primary tools:

- Get Customer Complaints - Customer Impact
- Get Returns - Customer Impact

---

### 4.4 Returns Specialist

Purpose:

- Analyze product returns associated with the quality investigation.
- Determine return count.
- Review return reasons.
- Calculate or report return-rate information where available.
- Identify financial/customer exposure from returns.

Primary data source:

- Returns table.

Primary tool:

- Get Returns

---

### 4.5 Safety Specialist

Purpose:

- Assess whether safety-related concerns exist.
- Review safety indicators in complaint information.
- Identify potential safety escalation.
- Determine whether safety evidence requires escalation.

Primary data source:

- Customer Complaints table.

Primary tool:

- Get Customer Complaints - Safety

Safety findings have higher decision priority than ordinary customer inconvenience or commercial considerations.

---

### 4.6 CAPA Specialist

Purpose:

- Receive the incident ID and final classification.
- Determine whether CAPA planning is required.
- Create containment actions for active investigations and High/Critical cases.
- Create corrective recommendations.
- Create preventive recommendations.
- Assign the appropriate owner role.
- Determine the CAPA target date.
- Define the validation method.
- Create/update the CAPA Register.
- Return the CAPA summary to the Quality Supervisor.

Primary data source:

- Owners table.
- CAPA Register table.

Primary tools:

- Get Owners - CAPA
- Get CAPA Register
- Create CAPA Record

---

### 4.7 M365 Guidance Specialist

Purpose:

- Provide Microsoft 365 and Copilot Studio guidance where required.
- Support implementation or configuration questions.
- Use Microsoft Learn information through MCP.

Primary tool:

- Microsoft Learn MCP Server - M

---

## 5. Data Layer

The solution uses Excel Online (Business) tables as the primary operational data source.

The key tables are:

### ProductMasterTable

Contains product/SKU master information.

Used for:

- SKU validation.
- Product existence validation.
- Product information retrieval.

---

### BatchRegisterTable

Contains batch information.

Used for:

- Batch validation.
- Batch status validation.
- Quality-hold identification.
- Batch-level investigation.

---

### CustomerComplaintsTable

Contains customer complaint records.

Used for:

- Complaint validation.
- Complaint pattern analysis.
- Safety assessment.
- Customer impact analysis.

Typical fields include:

- ComplaintID
- OrderID
- SKU
- BatchID
- ComplaintDate
- Category
- Severity
- SafetyIndicator
- Processed

---

### ReturnsTable

Contains return records.

Used for:

- Return analysis.
- Customer impact assessment.
- Return-rate analysis.
- Financial/customer exposure analysis.

---

### QualityIncidentsTable

Contains quality incident records.

Used for:

- Incident identification.
- Previous incident checks.
- Incident status analysis.
- Quality investigation context.

---

### OwnersTable

Contains ownership information for CAPA actions.

Used for:

- Owner-role resolution.
- CAPA ownership assignment.

---

### CAPA_Register

Contains CAPA records.

Used for:

- CAPA creation.
- CAPA tracking.
- Corrective/preventive action ownership.
- Target dates.
- Validation methods.
- CAPA status.

---

## 6. Tool Architecture

Tools are separated according to the agent responsible for using them.

### Quality Supervisor Tools

- Get Customer Complaints-supervisor
- get capa owner -supervisor
- Send Quality Investigation Notification
- Generate Quality Investigation Report

### Product/Batch Specialist Tools

- Get Product Master
- Get Batch Register
- Get Quality Incidents

### Complaint Pattern Specialist Tools

- Get Customer Complaints

### Customer Impact Specialist Tools

- Get Customer Complaints - Customer Impact
- Get Returns - Customer Impact

### Safety Specialist Tools

- Get Customer Complaints - Safety

### Returns Specialist Tools

- Get Returns

### CAPA Specialist Tools

- Get CAPA Register
- Get Owners - CAPA
- Create CAPA Record

### M365 Guidance Specialist Tools

- Microsoft Learn MCP Server - M

---

## 7. Topic Architecture

The Quality Supervisor contains mandatory custom topics that control deterministic parts of the workflow.

### Topic 1 - Incident Intake & Validation

Purpose:

Perform deterministic validation before specialist analysis begins.

The topic validates:

- Incident/Complaint ID.
- Duplicate or processed status.
- Order ID.
- SKU.
- Batch ID where supplied.
- Complaint date.
- Category.
- Severity.
- Safety indicator.
- Product existence.
- Batch existence where applicable.

The topic produces a validation result such as:

- Valid
- Invalid
- Insufficient Evidence

Invalid records must not proceed to specialist analysis.

---

### Topic 2 - Quality Investigation Decision

Purpose:

Consolidate specialist findings and determine the quality classification.

The decision considers:

- Safety findings.
- Complaint patterns.
- Complaint volume.
- Return information.
- Customer impact.
- Product/batch findings.
- Previous incidents.
- CAPA status.
- Evidence availability.

The final classification determines whether the investigation requires:

- No further CAPA action.
- Quality monitoring.
- Investigation/CAPA.
- High-priority quality escalation.
- Critical escalation/safety action.

---

### Topic 3 - CAPA Planning & Ownership

Purpose:

Create and assign CAPA actions when required.

The topic:

1. Receives incident ID and classification.
2. Checks whether CAPA is required.
3. Creates containment actions for active Investigation/High/Critical cases.
4. Creates corrective recommendations.
5. Creates preventive recommendations.
6. Resolves the appropriate owner role.
7. Assigns a target date.
8. Defines a validation method.
9. Writes/updates the CAPA Register.
10. Returns a CAPA summary to the Quality Supervisor.

---

### Topic 4 - Reporting & Notification

Purpose:

Complete the investigation after the final decision.

The topic can:

- Prepare the final investigation content.
- Generate the Word quality investigation report.
- Determine whether notification is required.
- Send the notification through Outlook.
- Return the completed investigation status.

---

## 8. End-to-End Processing Flow

The expected execution sequence is:

### Step 1 - Request Intake

A quality investigation request is received by the Quality Supervisor.

The request contains the relevant incident or complaint identifier.

---

### Step 2 - Deterministic Validation

The Quality Supervisor invokes the intake/validation topic.

The record is checked against the required Excel tables.

If validation fails:

- Specialist agents are not invoked.
- The validation result is returned.
- The investigation stops or waits for correction.

---

### Step 3 - Specialist Fan-Out

For a valid investigation, the Quality Supervisor invokes the relevant specialist agents.

The independent assessments cover:

- Product and batch.
- Complaint patterns.
- Customer impact.
- Returns.
- Safety.

---

### Step 4 - Specialist Fan-In

The Quality Supervisor receives the specialist outputs.

The findings are consolidated into one investigation context.

The Supervisor evaluates the findings instead of relying on a single specialist result.

---

### Step 5 - Quality Decision

The Supervisor determines the final quality classification.

Safety-related findings receive priority.

Repeated quality failures, customer impact, returns, previous incidents and evidence gaps are considered when determining the outcome.

---

### Step 6 - CAPA Decision

If the classification requires CAPA:

- CAPA Planning & Ownership is invoked.
- CAPA actions are generated.
- Owner information is retrieved.
- A target date is assigned.
- Validation method is defined.
- CAPA Register is updated.

If CAPA is not required, the process proceeds to reporting/notification.

---

### Step 7 - Report Generation

The Generate Quality Investigation Report tool is used to create the final Word report containing the investigation findings and final decision.

---

### Step 8 - Notification

Where required, the Send Quality Investigation Notification tool sends the investigation result to the appropriate recipient.

The recipient can be resolved from owner information available through the configured data source.

---

### Step 9 - Final Outcome

The Quality Supervisor returns the final investigation result, including:

- Investigation ID.
- Classification.
- Key findings.
- Safety assessment.
- Customer impact.
- CAPA status.
- Owner.
- Target date.
- Report status.
- Notification status.

---

## 9. Decision and Control Boundaries

The architecture separates responsibilities between deterministic topics, specialist agents and the Supervisor.

### Deterministic Topics

Used for:

- Validation.
- Mandatory field checks.
- Status checks.
- Routing.
- CAPA conditions.
- Final process control.

### Specialist Agents

Used for:

- Focused data retrieval.
- Domain-specific analysis.
- Independent findings.

### Quality Supervisor

Used for:

- Orchestration.
- Coordination.
- Consolidation.
- Final classification.
- Escalation.
- Report and notification coordination.

### Tools

Used for:

- Reading Excel data.
- Writing CAPA records.
- Generating Word reports.
- Sending Outlook notifications.
- Accessing Microsoft Learn through MCP.

---

## 10. Error and Guardrail Handling

The architecture includes validation and guardrails to prevent invalid processing.

Examples include:

- Missing complaint/incident ID.
- Duplicate or already processed record.
- Invalid SKU.
- Invalid batch.
- Invalid complaint date.
- Invalid severity.
- Missing evidence.
- Safety escalation.
- CAPA ownership resolution failure.
- Report-generation failure.
- Notification failure.

Invalid records should not trigger specialist analysis.

Safety-related findings should not be overridden by lower-priority business considerations.

CAPA ownership should be resolved from the configured Owners table rather than being invented by the agent.

---

## 11. External Integrations

### Excel Online (Business)

Used as the operational data layer for:

- Product Master.
- Batch Register.
- Customer Complaints.
- Returns.
- Quality Incidents.
- Owners.
- CAPA Register.

---

### Microsoft Word

Used to generate the final Quality Investigation Report.

Tool:

**Generate Quality Investigation Report**

---

### Microsoft Outlook

Used for conditional investigation notifications.

Tool:

**Send Quality Investigation Notification**

---

### Microsoft Learn MCP

Used by the M365 Guidance Specialist to retrieve Microsoft 365/Copilot-related guidance.

Tool:

**Microsoft Learn MCP Server - M**

---

## 12. Architecture Summary

The solution follows a hierarchical autonomous multi-agent architecture.

The **Quality Supervisor** acts as the central orchestrator. It performs deterministic validation through topics, delegates domain-specific investigation to specialist agents, consolidates the independent findings, applies the quality decision logic, initiates CAPA planning when required, and coordinates final reporting and notification.

The architecture provides separation of concerns between:

- Data retrieval.
- Domain analysis.
- Deterministic validation.
- Decision logic.
- CAPA management.
- Reporting.
- Notification.

This structure enables the Quality Intelligence Control Tower to process quality investigations consistently while maintaining clear agent, topic, tool and data responsibilities.
