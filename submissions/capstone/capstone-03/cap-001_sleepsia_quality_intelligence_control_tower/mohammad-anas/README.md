# CAP-001 — Sleepsia Product Quality & Customer Experience Intelligence Control Tower

## Participant
- Name: Mohammad Anas
- Date completed: 10/08/2026

## Project summary
An autonomous multi-agent system built in Microsoft Copilot Studio that detects unprocessed customer complaints for Sleepsia sleep-support products, validates them, runs independent specialist analysis (complaint pattern, returns, product/batch, customer impact, safety), consolidates findings under a single Quality Supervisor, applies deterministic quality-classification rules, creates Corrective and Preventive Action (CAPA) recommendations where warranted, and reports/notifies through Word and Outlook — with a bounded selective-reassessment loop for new evidence on existing incidents. The same agent also supports interactive employee queries in Teams/Microsoft 365 Copilot without triggering a new autonomous assessment per question.

## Agent / channel status
| Item | Status |
|---|---|
| Quality Supervisor agent | Built |
| Recurrence trigger | Built and tested |
| Specialist child agents (6) | Built |
| Custom topics (4) | Built |
| Word tool | Built |
| Excel tool | Built |
| Outlook tool | Built |
| Microsoft Learn MCP (M365 Guidance Specialist) | Built |
| Teams channel | Cannot Published because of Billing Issue |
| Microsoft 365 Copilot channel | Cannot Published because of Billing Issue |
| Published agent URL | Cannot Published because of Billing Issue |

## Completion status
Core autonomous pipeline complete and tested. Publishing pending tenant approval - see known-limitations.md.

## Repository structure
```
cap-001_sleepsia_quality_intelligence_control_tower/
├── README.md
├── architecture.md
├── orchestration-patterns.md
├── custom-topics.md
├── knowledge-sources.md
├── mcp-implementation.md
├── tool-implementation.md
├── publishing.md
├── test-report.md
├── ai-usage-declaration.md
├── known-limitations.md
└── screenshots/
```