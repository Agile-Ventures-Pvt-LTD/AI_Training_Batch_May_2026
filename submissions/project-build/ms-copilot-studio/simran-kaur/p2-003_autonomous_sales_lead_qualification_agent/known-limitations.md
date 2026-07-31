# Known Limitations

## Agent Name
**NovaWorks Sales Lead Qualification Agent**

---

# Functional Limitations

- The agent processes only emails containing `[P2-003 LEAD]` in the subject.
- Attachment content extraction is not implemented.
- Decisions depend on the accuracy of extracted email information.
- Unknown or ambiguous information may require human review.

---

# Connector Limitations

- Outlook, Excel Online (Business), and Word Online (Business) require active Microsoft 365 connections.
- Connector failures can interrupt autonomous execution.
- Access depends on tenant permissions and configuration.

---

# Data Limitations

- Only synthetic project data is supported.
- Qualification accuracy depends on the provided reference tables.
- Missing reference data may result in Human Review Required classification.

---

# AI Limitations

- The agent does not replace final sales decisions.
- Human review is required for uncertain, conflicting, or unsupported cases.
- AI-generated outputs must be validated before business use.

---

# Current Status

| Area | Status |
|---|---|
| Core Qualification Workflow | Completed |
| Exception Handling | Completed |
| Connector Integration | Completed |
| Known Constraints Documented | Completed |