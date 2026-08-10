# CAP-001 — Sleepsia Product Quality Intelligence Control Tower

## Overview

A Microsoft Copilot Studio multi-agent solution for managing Sleepsia product-quality incidents from **intake to classification, CAPA, reassessment, reporting and notification**.

## Workflow

```text
Incident
   ↓
Topic 1 — Validate
   ↓
Specialist Analysis
   ↓
Topic 2 — Classify
   ↓
Topic 3 — CAPA
   ↓
Supervisor Validation
   ↓
Word Report + Excel Update + Outlook Notification
```

New evidence is handled through **Topic 4 — Selective Reassessment**.

## Main Components

- **Quality Supervisor** — orchestrates the workflow and makes the final classification.
- **Child Specialists** — Complaint Pattern, Returns, Product/Batch, Customer Impact, Safety and CAPA.
- **Excel Online** — operational data and incident/CAPA updates.
- **Knowledge Base** — quality policy, product care and customer-resolution guidance.
- **MCP Server** — Microsoft 365 guidance through the M365 Guidance Specialist.
- **Word Online** — investigation report generation.
- **Outlook** — internal quality notifications.
- **Custom Topics** — validation, classification, CAPA and reassessment.

## Decision Priority

The Supervisor applies deterministic rules, including:

1. Confirmed safety → **Critical Escalation**
2. Multiple potential safety complaints → **High-Priority**
3. Complaint cluster → **Investigation Required**
4. Return rate ≥ 2% → **Investigation Required**
5. Previous incident + repeated failure → **High-Priority**
6. Missing required batch evidence → **Insufficient Evidence**
7. Overdue CAPA → **High-Priority**
8. Isolated low-severity complaint → **Informational**

Specialists provide findings only. **The Supervisor is the final decision authority.**

## Test Status

Current Copilot Studio evaluation:

- **20 test cases**
- **14 Passed**
- **6 Failed**
- **70% Pass Rate**

Key failures are related to safety escalation, medical/advice handling, Word/Outlook failure handling and connector/runtime execution.

See [`test-report.md`](test-report.md) for details.

## Documentation

```text
README.md
architecture.md
orchestration-patterns.md
custom-topics.md
knowledge-sources.md
mcp-implementation.md
tool-implementation.md
publishing.md
test-report.md
ai-usage-declaration.md
known-limitations.md
```

## Screenshots

```text
screenshots/
├── supervisor_agent/
├── child_agent/
├── excel_tool/
├── knowledge_base/
├── mcp_server/
├── topics/
├── word_outlook_tool/
├── publishing/
└── tests/
```

Screenshot paths are referenced from the relevant documentation files.
