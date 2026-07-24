# Custom Topic Design

## Overview

The chatbot uses custom topics to guide customers through structured product support and preliminary warranty assessment while following NovaRetail policies and responsible AI practices.

---

# Custom Topics

| Topic | Purpose |
|--------|---------|
| Guided Product Troubleshooting & Safety Triage | Provides structured troubleshooting, performs safety assessment, and escalates unresolved or safety-critical issues. |
| Warranty Eligibility & Service Route Assessment | Performs a preliminary warranty assessment and recommends the appropriate service route based on NovaCare policy. |

---

# Reusable Subtopics

| Subtopic | Purpose |
|-----------|---------|
| Product Safety Assessment | Detects safety-critical conditions before troubleshooting and determines whether it is safe to continue. |
| Support Case Summary | Generates a structured summary for customer confirmation and human support escalation. |

---

# Topic Workflow

```text
Customer Query
      │
      ▼
Identify Product
      │
      ▼
Select Appropriate Topic
      │
      ├── Guided Product Troubleshooting
      └── Warranty Assessment
              │
              ▼
      Support Summary / Escalation
```

---

# Key Design Principles

- Validate supported products before providing guidance.
- Perform mandatory safety assessment before troubleshooting.
- Use official knowledge sources for all responses.
- Avoid repeated troubleshooting steps.
- Escalate unresolved or safety-critical cases.
- Provide preliminary warranty guidance only.

---

# Topic Outcomes

- Self-service resolution
- Technical support review
- Warranty assessment recommended
- Unsupported product escalation
- Safety-critical escalation
- Customer cancelled

---

# Related Documents

- README.md
- agent-design.md
- knowledge-sources.md
- solution-summary.md