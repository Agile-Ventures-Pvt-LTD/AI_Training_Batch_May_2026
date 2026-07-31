# 🧠 Agent Instructions Design

## 🚀 Project Information

| Property | Details |
|----------|---------|
| **Project ID** | P2-003 – Autonomous Sales Lead Qualification Agent |
| **Participant** | Vikash Kumar |
| **Platform** | Microsoft Copilot Studio |
| **AI Capability** | Generative AI Orchestration |

---

# 🎯 Design Objective

The primary objective of the agent instructions is to enable the Microsoft Copilot Studio agent to autonomously qualify incoming sales enquiries while following NovaWorks operational policies and business rules.

Rather than responding conversationally, the agent is designed to behave as an autonomous business process executor capable of reasoning about incoming emails, invoking Microsoft 365 connector tools, and completing the qualification lifecycle without manual intervention.

The instructions guide the Large Language Model (LLM) to make consistent operational decisions while ensuring compliance with organizational policies.

---

# 🧩 Instruction Design Strategy

The instructions were designed using a modular structure instead of a single long prompt. Each section focuses on one responsibility, allowing the model to reason more effectively.

The major sections include:

- Trigger validation
- Lead identification
- Information extraction
- Data normalization
- Operational tool usage
- Duplicate detection
- Qualification logic
- Territory assignment
- Sales owner assignment
- Operational action selection
- Word report generation
- Customer communication
- Human review
- Failure handling
- Process execution order

This structure improves readability, maintainability, and orchestration accuracy.

---

# 📥 Trigger Behaviour

The instructions explicitly restrict processing to emails whose subject contains:

```text
[P2-003 LEAD]
```

This prevents the agent from processing unrelated emails and ensures only intended sales enquiries enter the qualification workflow.

---

# 🔍 Lead Identification

The instructions define what constitutes a valid sales lead.

The agent evaluates whether the email represents genuine commercial intent before performing any operational actions.

The following enquiries are explicitly excluded:

- Technical support
- Recruitment
- Job applications
- Academic research
- Vendor solicitations
- Competitor research
- Spam
- General information requests

By defining exclusions explicitly, the model avoids unnecessary processing and improves classification accuracy.

---

# 📑 Information Extraction

The instructions require the model to extract structured information from every valid enquiry.

The extracted information includes:

### Contact Information

- Contact Name
- Sender Email
- Job Title
- Decision Role

### Organization Information

- Company Name
- Country
- Territory
- Industry
- Company Size

### Opportunity Information

- Product Interest
- Business Need
- Budget
- Purchase Timeline
- Lead Source

### Operational Assessment

- Qualification Score
- Confidence
- Product Fit
- Missing Information
- Risk Flags

The agent is instructed to extract only information explicitly available within the email.

No assumptions or fabricated values are permitted.

---

# 🔄 Data Normalization

To improve operational consistency, the instructions require normalization of commonly varying business values.

Normalization includes:

- Country names
- Product names
- Industry values
- Decision roles
- Company size

Missing information is represented as **Unknown** rather than default values such as zero.

This prevents incorrect downstream qualification.

---

# 🛠️ Tool Orchestration

The instructions explicitly direct the model to use Microsoft 365 connector tools instead of relying solely on reasoning.

The following tools are available:

| Tool | Purpose |
|------|---------|
| 📊 Read Operational Excel Tables | Retrieve operational reference data |
| ➕ Create New Lead Record | Create operational lead records |
| 🔄 Update Existing Lead Record | Update existing leads |
| 📄 Generate Lead Qualification Report | Produce Word reports |
| 📧 Send Qualification Result Email | Send acknowledgement emails |

The instructions emphasize that operational decisions must be based on tool outputs rather than assumptions.

---

# 📊 Operational Reference Tables

The instructions define the exact operational tables available within the Excel workbook.

These include:

- LeadsRegisterTable
- QualificationRulesTable
- TerritoryOwnersTable
- ProductCatalogTable
- SalesOwnersTable
- ActionMatrixTable

The model is instructed to use only these table names when invoking the Excel connector.

This minimizes tool invocation errors and improves orchestration reliability.

---

# 🔁 Duplicate Detection Strategy

Duplicate detection is performed before any new operational record is created.

The instructions define the following comparison hierarchy:

1. Source Message ID
2. Sender Email
3. Company Name
4. Product Interest

When a duplicate is detected, the model updates the existing record rather than creating a new one.

This prevents duplicate operational records.

---

# 📈 Qualification Logic

The instructions require the model to retrieve operational qualification rules before determining the final lead classification.

Possible outcomes include:

- Hot
- Qualified
- Nurture
- Low Priority
- Additional Information Required
- Human Review Required
- Duplicate
- Not a Sales Lead

The model is explicitly instructed not to invent qualification scores.

---

# 👤 Sales Owner Assignment

Sales ownership is determined using the operational reference tables.

The instructions require the model to retrieve territory mappings and assign the appropriate sales representative before completing the workflow.

---

# 📄 Report Generation

The instructions define deterministic rules for Word report generation.

Reports are generated for valid sales leads while duplicate and non-sales enquiries do not produce additional reports.

This avoids unnecessary document generation.

---

# 📧 Customer Communication

Customer acknowledgement emails are generated only after successful processing.

The instructions prohibit disclosure of:

- Internal qualification scores
- Operational reasoning
- Confidence values
- Business rules
- Internal operational data

The agent therefore communicates only customer-appropriate information.

---

# 👨‍💼 Human Review

The instructions define several situations requiring escalation.

Examples include:

- Unknown products
- Unknown territories
- Low confidence
- Missing operational data
- Conflicting information
- Tool failures

This prevents unreliable autonomous decisions.

---

# ⚠️ Failure Handling

Connector failures are handled using a retry strategy.

The model is instructed to:

1. Retry once.
2. Stop processing if the retry fails.
3. Record the failure.
4. Escalate for human review.
5. Never claim successful completion.

This improves operational reliability.

---

# 🔄 Execution Order

The instructions define a deterministic execution sequence:

1. Validate trigger.
2. Validate sales lead.
3. Extract information.
4. Normalize data.
5. Read operational tables.
6. Detect duplicates.
7. Calculate qualification.
8. Assign territory.
9. Assign sales owner.
10. Determine operational action.
11. Create or update lead.
12. Generate qualification report.
13. Send acknowledgement email.
14. Escalate if necessary.

Providing an explicit execution order significantly improved AI orchestration during testing.

---

# 🎯 Design Outcomes

The final instruction set successfully enabled the agent to:

- Autonomously process Outlook-triggered sales enquiries.
- Invoke Microsoft 365 connector tools.
- Read operational reference data.
- Create and update lead records.
- Generate qualification reports.
- Send customer emails.
- Detect duplicate enquiries.
- Escalate uncertain cases.

The modular instruction design also simplified maintenance and future enhancements while improving the reliability of tool invocation through Generative AI Orchestration.