# 🛠️ Tool Design

## 🚀 Project Information

| Property | Details |
|----------|---------|
| **Project ID** | P2-003 – Autonomous Sales Lead Qualification Agent |
| **Participant** | Vikash Kumar |
| **Platform** | Microsoft Copilot Studio |
| **AI Capability** | Generative AI Orchestration |
| **Integration Method** | Microsoft 365 Connectors |

---

# 🎯 Design Objective

The NovaWorks Autonomous Sales Lead Qualification Agent relies on Microsoft 365 connector tools to perform business operations beyond natural language understanding.

Rather than embedding business data directly within the prompt, the agent retrieves operational information from Microsoft 365 services whenever required.

This design keeps operational data separate from the AI model, improves maintainability, and enables real-time interaction with business systems.

---

# 🧠 Tool Orchestration Strategy

The agent uses **Generative AI Orchestration**, meaning the Large Language Model (LLM) determines:

- Which tool should be invoked.
- When a tool should be executed.
- Whether multiple tools are required.
- The sequence of tool execution.

The orchestration is driven entirely by the agent instructions and the context of the incoming sales enquiry.

The tools themselves perform business operations, while the AI agent decides **when** those operations are necessary.

---

# 📊 Tool 1 – Read Operational Excel Tables

## 🎯 Purpose

This tool retrieves operational reference data stored within the Excel workbook.

The retrieved information supports decision-making throughout the qualification process.

## 📌 Operational Tables

The tool can access the following Excel tables:

- LeadsRegisterTable
- QualificationRulesTable
- TerritoryOwnersTable
- ProductCatalogTable
- SalesOwnersTable
- ActionMatrixTable

## 🔍 Business Usage

The agent invokes this tool to:

- Check existing lead records.
- Retrieve qualification rules.
- Validate products.
- Determine territory.
- Identify the assigned sales owner.
- Retrieve operational actions.

The agent may invoke this tool multiple times during a single execution depending on the information required.

---

# ➕ Tool 2 – Create New Lead Record

## 🎯 Purpose

Creates a new record within the operational lead register after a sales enquiry has been successfully qualified.

## 📋 Business Rules

The tool is used only when:

- The enquiry is identified as a valid sales lead.
- No duplicate record exists.
- Required operational validation has completed.

The tool inserts the newly qualified lead into the Leads Register for future sales activities.

---

# 🔄 Tool 3 – Update Existing Lead Record

## 🎯 Purpose

Updates an existing lead record when the incoming enquiry matches an existing opportunity.

## 📋 Business Rules

The tool is invoked only after duplicate detection confirms that the lead already exists.

Typical update scenarios include:

- Additional customer information.
- Updated budget.
- Revised purchase timeline.
- New communication from an existing prospect.

Using updates instead of creating new records prevents duplicate operational data.

---

# 📄 Tool 4 – Generate Lead Qualification Report

## 🎯 Purpose

Creates a Microsoft Word qualification report summarizing the evaluation performed by the agent.

## 📋 Report Contents

The report includes:

- Contact information
- Organization details
- Opportunity summary
- Qualification outcome
- Assigned sales owner
- Confidence assessment
- Recommended next actions

## 📌 Business Rules

Reports are generated only for qualified operational scenarios.

Reports are not generated for:

- Duplicate enquiries
- Non-sales enquiries

This reduces unnecessary document creation.

---

# 📧 Tool 5 – Send Qualification Result Email

## 🎯 Purpose

Sends the final acknowledgement email after successful lead processing.

## 📋 Email Contents

The acknowledgement typically includes:

- Thank-you message
- Confirmation of receipt
- Next processing steps
- Appropriate sales contact information

## 📌 Business Rules

The agent does not send acknowledgement emails when:

- The enquiry is classified as Duplicate.
- The enquiry is not considered a sales lead.

This prevents unnecessary customer communication.

---

# 🔄 Tool Execution Sequence

Although the LLM determines tool usage dynamically, the expected operational sequence is:

```text
Receive Outlook Email
        │
        ▼
Read Operational Excel Tables
        │
        ▼
Duplicate Detection
        │
 ┌──────┴──────┐
 │             │
 ▼             ▼
Update      Create
Existing    New Lead
Lead         Record
        │
        ▼
Generate Qualification Report
        │
        ▼
Send Qualification Result Email
```

This sequence reflects the intended business process while allowing the AI agent to adapt based on context.

---

# 🤖 AI Decision-Making

The agent does not invoke tools arbitrarily.

Instead, it reasons about:

- Whether operational data is required.
- Whether duplicate detection is necessary.
- Whether a report should be generated.
- Whether customer communication is appropriate.

Only then does it invoke the relevant connector tool.

This reduces unnecessary connector calls and improves execution efficiency.

---

# ⚠️ Failure Handling

Connector failures are managed through controlled retry logic.

The agent follows these steps:

1. Attempt the connector operation.
2. Retry once if the operation fails.
3. Stop further processing if the retry also fails.
4. Record the failure.
5. Escalate for human review.
6. Never report a successful operation when execution has failed.

This behavior improves reliability while maintaining data integrity.

---

# 🔒 Security Considerations

The configured tools operate only within the authenticated Microsoft 365 environment.

The agent:

- Does not expose operational reference tables.
- Does not reveal internal qualification logic.
- Does not disclose confidence scores.
- Does not expose connector configuration.
- Does not reveal organizational business rules.

All connector access is governed by Microsoft Entra ID authentication and Microsoft 365 permissions.

---

# 🧪 Validation

Each tool was individually configured and validated during implementation.

Successful validation confirmed:

- ✔️ Operational Excel data retrieval
- ✔️ New lead creation
- ✔️ Existing lead updates
- ✔️ Word report generation
- ✔️ Outlook acknowledgement emails

The complete toolset was subsequently verified through end-to-end execution using both Copilot Studio testing and real Outlook-triggered email processing.

---

# 🎉 Outcome

The tool design separates business operations from AI reasoning, allowing the NovaWorks Autonomous Sales Lead Qualification Agent to dynamically orchestrate Microsoft 365 connector actions based on the context of each incoming sales enquiry.

This modular architecture improves scalability, maintainability, and reliability while supporting fully autonomous lead qualification.