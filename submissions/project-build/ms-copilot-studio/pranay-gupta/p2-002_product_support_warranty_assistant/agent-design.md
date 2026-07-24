# Agent Design

## Agent Overview

| Field | Details |
|--------|---------|
| Chatbot Name | NovaRetail Product Support & Warranty Assistant |
| Platform | Microsoft Copilot Studio |
| Project ID | P2-002 |
| Participant | Pranay Gupta |

---

# Agent Purpose

The chatbot provides first-line customer support for supported Lenovo laptops and HP printers by combining Retrieval-Augmented Generation (RAG), structured Copilot Studio topics, and NovaRetail policies. It assists customers with troubleshooting, preliminary warranty guidance, safety assessment, and service route recommendations.

---

# Supported Products

| Category | Products |
|----------|----------|
| Lenovo Laptop | ThinkPad E14 Gen 5 |
| Lenovo Laptop | ThinkPad E16 Gen 1 |
| HP Printer | LaserJet Pro MFP M428 Series |
| HP Printer | LaserJet Pro MFP M429 Series |

---

# Agent Capabilities

The chatbot can:

- Identify supported products.
- Guide customers through troubleshooting.
- Perform product safety assessment.
- Provide preliminary warranty guidance.
- Recommend the appropriate service route.
- Generate structured support summaries.
- Escalate safety-critical or unresolved cases.

The chatbot cannot:

- Approve warranty claims.
- Book repairs.
- Track repair status.
- Access customer accounts.
- Access live warranty databases.
- Support products outside the configured scope.

---

# Agent Instructions Summary

The agent follows these design principles:

- Use only configured knowledge sources.
- Prioritise customer safety.
- Validate supported products before troubleshooting.
- Stop troubleshooting when safety risks are detected.
- Never fabricate product or warranty information.
- Provide preliminary assessments only.
- Escalate when human intervention is required.

---

# Conversation Design

The chatbot follows a structured workflow:

1. Identify product family.
2. Validate supported model.
3. Perform safety assessment.
4. Guide troubleshooting or warranty assessment.
5. Recommend next steps.
6. Generate support summary when required.

---

# Custom Topics

| Topic | Purpose |
|--------|---------|
| Guided Product Troubleshooting & Safety Triage | Product diagnosis and safe troubleshooting |
| Warranty Eligibility & Service Route Assessment | Preliminary warranty assessment |

---

# Reusable Subtopics

| Subtopic | Purpose |
|-----------|---------|
| Product Safety Assessment | Detect safety-critical conditions before troubleshooting |
| Support Case Summary | Generate structured summaries for escalation |

---

# Variables

The chatbot maintains variables for:

- Product information
- Issue information
- Safety assessment
- Warranty assessment
- Troubleshooting progress
- Escalation level
- Customer confirmation

Detailed variable definitions are documented in **custom-topic-design.md**.

---

# Agent Workflow

```text
Customer Query
      │
      ▼
Product Identification
      │
      ▼
Safety Assessment
      │
      ▼
Topic Selection
      │
      ├── Troubleshooting
      └── Warranty Assessment
             │
             ▼
     Support Summary / Escalation
```

---

# Design Principles

The chatbot implementation follows:

- Retrieval-Augmented Generation (RAG)
- Structured topic routing
- Knowledge-source grounding
- Product validation
- Controlled troubleshooting loops
- Responsible AI
- Safety-first design
- Human escalation when appropriate

---

# Related Documents

- knowledge-sources.md
- custom-topic-design.md
- solution-summary.md
- known-limitations.md