
# Agent Instructions Design

# Project Information

| Property      | Value                                              |
| ------------- | -------------------------------------------------- |
| Project       | P2-003 – NovaWorks Sales Lead Qualification Agent |
| Platform      | Microsoft Copilot Studio                           |
| Agent Type    | Autonomous AI Agent                                |
| AI Model      | GPT-5.5                                            |
| Orchestration | Generative Orchestration                           |

---

# Purpose

The agent instructions define the decision-making framework used by the autonomous agent. Rather than prescribing every individual action, the instructions establish business objectives, operational rules, tool boundaries, and workflow sequencing that enable Generative Orchestration to determine the appropriate actions during runtime.

The instructions are designed to ensure that the agent behaves consistently, follows business policies, and only uses the configured tools for their intended purposes.

No credentials, secrets, authentication tokens, or confidential business information are embedded within the instructions.

---

# Instruction Design Principles

The instructions were developed using the following principles:

- Business-rule driven processing
- Clear role definition
- Explicit workflow sequencing
- Deterministic tool usage
- Separation of business logic and implementation
- No hardcoded operational data
- Human escalation for uncertain cases
- No fabrication of information

---

# Agent Role

The agent acts as an autonomous Sales Lead Qualification Assistant responsible for processing inbound sales enquiries received through Outlook.

Its responsibilities include:

- Reading operational reference data.
- Extracting lead information.
- Validating business information.
- Detecting duplicate leads.
- Applying qualification logic.
- Assigning sales ownership.
- Generating qualification reports.
- Updating operational records.
- Sending business communications.
- Escalating exceptional cases.

The agent is instructed to perform these activities autonomously while adhering to organizational policies.

---

# Operational Workflow

The agent follows the business workflow below.

1. Receive a qualifying Outlook email.
2. Read operational reference data.
3. Extract structured lead information.
4. Validate mandatory fields.
5. Detect duplicate leads.
6. Apply qualification rules.
7. Calculate qualification score.
8. Determine lead classification.
9. Assign the appropriate sales owner.
10. Generate the Lead Qualification Report.
11. Create or update the operational workbook.
12. Send the required communication.
13. Escalate for manual review when necessary.

The workflow ensures that records are processed in a consistent and repeatable manner.

---

# Tool Invocation Strategy

The instructions define clear responsibilities for each configured tool.

| Tool                               | Intended Use                                                                                |
| ---------------------------------- | ------------------------------------------------------------------------------------------- |
| Read Lead Reference Data           | Retrieve operational and reference information before making business decisions.            |
| Create Lead Record                 | Insert a new lead into the operational workbook only after duplicate checks have completed. |
| Update Lead Record                 | Modify an existing lead when updates are required.                                          |
| Generate Lead Qualification Report | Produce the Lead Qualification Report after qualification is complete.                      |
| Send Email                         | Deliver customer acknowledgements, requests for information, and internal notifications.    |

The agent is instructed not to use tools outside their intended purpose.

---

# Business Rules

The instruction set requires the agent to:

- Always perform duplicate detection before creating a record.
- Read operational reference data before making decisions.
- Validate mandatory information.
- Never fabricate missing values.
- Apply qualification rules consistently.
- Generate reports only after qualification.
- Update existing records instead of creating duplicates.
- Escalate uncertain cases for manual review.

---

# Duplicate Detection Strategy

The instructions require the agent to check existing operational records before creating a new lead.

Duplicate evaluation is performed using available operational identifiers and lead information.

If a duplicate is identified, the existing record is updated rather than creating a new operational record.

---

# Data Validation

Before qualification begins, the agent validates that mandatory business information is available.

If required information is missing:

- Missing fields are identified.
- Missing values are not fabricated.
- Appropriate follow-up communication may be generated.
- Processing continues only where permitted by business rules.

---

# Qualification Process

The instructions require the agent to use operational reference data to evaluate:

- Product suitability
- Budget
- Purchase timeline
- Decision-maker involvement
- Territory
- Business need

The resulting evaluation determines:

- Qualification Score
- Lead Classification
- Priority
- Assigned Sales Owner

---

# Communication Strategy

The agent determines the appropriate communication based on the processing outcome.

Possible communications include:

- Customer acknowledgement
- Request for additional information
- Internal sales notification

Communications are generated using professional business language and organizational communication guidelines.

---

# Error Handling

The instructions require the agent to:

- Detect missing operational data.
- Prevent duplicate record creation.
- Handle incomplete information gracefully.
- Avoid unsupported assumptions.
- Escalate exceptional situations.

The objective is to maximize reliability while preventing incorrect business decisions.

---

# Security Considerations

The instruction design intentionally excludes:

- Passwords
- Secrets
- Authentication tokens
- API keys
- Personal credentials
- Confidential organizational information

Authentication and authorization are managed through Microsoft 365 connectors.

---

# Design Decisions

Several design decisions were adopted during implementation:

- Generative Orchestration is used instead of manually connected workflows.
- Business rules are separated from connector configuration.
- Operational data resides in Excel rather than being embedded within prompts.
- Reports are generated dynamically using Word Online (Business).
- Outlook is used for event triggering and communication.

These decisions improve maintainability, readability, and scalability.

---

# Limitations

The instructions depend on:

- Availability of configured connectors.
- Operational workbook accessibility.
- Outlook event trigger execution.
- AI interpretation of incoming email content.

Certain runtime behaviors remain dependent on Microsoft Copilot Studio orchestration and connector capabilities.

---

# Conclusion

The instruction design provides a structured, policy-driven framework that enables the NovaWorks Sales Lead Qualification Agent to autonomously process inbound sales enquiries while maintaining consistency, operational accuracy, and compliance with business requirements.

The design intentionally separates business logic from implementation details, enabling maintainability, transparency, and future extensibility without exposing sensitive information.
