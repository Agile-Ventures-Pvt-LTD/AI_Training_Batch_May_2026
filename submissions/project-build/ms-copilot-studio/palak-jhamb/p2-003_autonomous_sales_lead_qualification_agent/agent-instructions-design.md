# Agent Instructions Design

## Purpose

The Autonomous Sales Lead Qualification Agent is designed to automatically process inbound sales enquiry emails, qualify potential leads, assign the appropriate sales owner, update operational records, generate qualification reports, and send required communications with minimal human intervention.

---

# Agent Role

The agent acts as an autonomous sales qualification assistant that:

- Monitors incoming sales emails.
- Extracts structured lead information.
- Validates data using operational reference tables.
- Detects duplicate opportunities.
- Qualifies leads.
- Assigns sales owners.
- Generates qualification reports.
- Sends customer and internal notifications.
- Escalates exceptional cases for human review.

---

# Instruction Design

The agent instructions are organized into logical execution phases instead of one large prompt.

1. Monitor incoming emails.
2. Extract structured information.
3. Validate and normalize data.
4. Read operational reference tables.
5. Detect duplicates.
6. Apply qualification rules.
7. Assign lead classification.
8. Assign the sales owner.
9. Update the Lead Register.
10. Generate the qualification report.
11. Send required communications.
12. Escalate Human Review cases.

---

# Knowledge Usage

The agent uses the following knowledge sources:

- **Sales Lead Qualification Policy** – qualification policy and processing rules.
- **Sales Communication Guidelines** – email writing standards.
- **Lead Qualification Report Structure** – report format and required sections.

Knowledge is used only for policy and documentation guidance.

---

# Tool Usage

The agent uses Outlook, Excel Online (Business), and Microsoft Word connector tools to retrieve emails, validate operational data, update records, generate reports, and send notifications.

Operational decisions always rely on Excel reference tables rather than static instructions.

---

# Decision Logic

Before qualifying a lead, the agent:

- Validates extracted information.
- Checks for duplicate opportunities.
- Reads qualification rules.
- Applies business logic.
- Determines the lead classification.
- Assigns the appropriate sales owner.
- Executes only the actions defined by the Action Matrix.

---

# Human Review

The agent routes a lead for manual review when:

- Information is incomplete.
- Qualification confidence is low.
- Territory or product cannot be determined.
- Business rules cannot be applied.
- Connector failures prevent successful processing.

---

# Design Principles

- Modular instruction design.
- Tool-first execution.
- Knowledge-driven responses.
- No hardcoded business rules.
- Deterministic workflow.
- Human-in-the-loop for exceptional scenarios.
- Consistent and explainable decision making.