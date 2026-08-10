# Architecture

## 1. Introduction

The **Sleepsia Product Quality & Customer Experience Intelligence Control Tower** is implemented using a **Supervisor–Specialist Multi-Agent Architecture** in Microsoft Copilot Studio.

The architecture separates orchestration from domain-specific analysis to ensure scalability, maintainability, deterministic decision-making, and clear ownership of business responsibilities.

The solution follows a governed workflow where the **Quality Supervisor** coordinates every investigation while specialist agents independently analyze specific operational domains.

---

# 2. Architecture Objectives

The architecture was designed to achieve the following objectives:

- Centralized orchestration
- Parallel specialist execution
- Deterministic decision making
- Separation of responsibilities
- Clear tool ownership
- Controlled knowledge access
- Microsoft 365 integration
- Reusable specialist agents
- Scalable workflow execution
- End-to-end investigation traceability

---

# 3. High-Level Architecture

```text
                    Quality Investigation Scheduler
                              OR
                      Authorized Employee
                               │
                               ▼
                    ┌──────────────────────────┐
                    │    Quality Supervisor     │
                    └──────────────────────────┘
                               │
                 Incident Intake & Validation
                               │
                 Validation Successful?
                     │                 │
                     ▼                 ▼
                 Stop Workflow      Fan-Out
                                      │
        ┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼              ▼
 Complaint        Returns       Product/Batch   Customer      Safety
 Pattern          Specialist     Specialist      Impact        Specialist
 Specialist                                        Specialist
        └──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
                               │
                             Fan-In
                               │
                               ▼
                 Quality Investigation Decision
                               │
                    Investigation Required?
                     │                    │
                     ▼                    ▼
           No Investigation         CAPA Planning
                 │                       │
                 ▼                       ▼
          Report Generation     Evidence Reassessment
                 │                       │
                 └──────────────┬────────┘
                                ▼
                       Excel Record Updates
                                │
                                ▼
                     Outlook Email Notification
                                │
                                ▼
                           Investigation Closed
```

---

# 4. Supervisor Architecture

## Quality Supervisor

The Quality Supervisor is the central orchestration agent.

The Supervisor is responsible for:

- Starting investigations
- Executing mandatory topics
- Coordinating specialist agents
- Managing workflow execution
- Consolidating specialist findings
- Applying investigation policies
- Coordinating CAPA generation
- Updating operational records
- Generating reports
- Sending notifications

The Supervisor never performs specialist analysis directly.

---

# 5. Specialist Architecture

Each specialist owns a single business domain.

## Complaint Pattern Specialist

### Responsibilities

- Complaint frequency analysis
- Complaint clustering
- Trend identification
- Failure mode detection

### Tools

- Complaint Pattern Specialist – Read Customer Complaints

---

## Returns Specialist

### Responsibilities

- Return rate analysis
- Refund analysis
- Return trends

### Tools

- Returns Specialist – Read Returns Register

---

## Product/Batch Specialist

### Responsibilities

- SKU validation
- Batch validation
- Supplier lot analysis
- Historical batch incidents

### Tools

- Product/Batch Specialist – Read Product Master
- Product/Batch Specialist – Read Batch Register

---

## Customer Impact Specialist

### Responsibilities

- Customer impact assessment
- Customer segmentation
- Affected customer estimation

### Tools

- Customer Impact Specialist – Read Customer Complaints

---

## Safety Specialist

### Responsibilities

- Safety evaluation
- Safety escalation
- Critical incident detection

### Tools

- Safety Specialist – Read Customer Complaints

---

## CAPA Specialist

### Responsibilities

- CAPA generation
- Corrective actions
- Preventive actions
- Ownership assignment

### Tools

- CAPA Specialist – Read CAPA Register
- CAPA Specialist – Add CAPA Register

---

## M365 Guidance Specialist

### Responsibilities

- Microsoft Learn guidance
- Copilot Studio support
- Teams support
- Connector guidance
- MCP documentation

### Tools

- Microsoft Learn MCP Server

---

# 6. Tool Ownership

Only the owning agent can use its assigned tools.

| Agent | Tool Ownership |
|---------|----------------|
| Quality Supervisor | Customer Complaints, Quality Rules, Quality Incidents, CAPA Register, Word, Outlook |
| Complaint Pattern Specialist | Customer Complaints |
| Returns Specialist | Returns Register |
| Product/Batch Specialist | Product Master, Batch Register |
| Customer Impact Specialist | Customer Complaints |
| Safety Specialist | Customer Complaints |
| CAPA Specialist | CAPA Register |
| M365 Guidance Specialist | Microsoft Learn MCP |

This separation prevents cross-agent responsibility overlap.

---

# 7. Knowledge Boundaries

The solution enforces strict knowledge boundaries.

| Agent | Knowledge Source |
|---------|----------------|
| Supervisor | Sleepsia Knowledge Base |
| Complaint Pattern Specialist | Customer Complaints |
| Returns Specialist | Returns Register |
| Product/Batch Specialist | Product Master, Batch Register |
| Customer Impact Specialist | Customer Complaints |
| Safety Specialist | Customer Complaints |
| CAPA Specialist | CAPA Register |
| M365 Guidance Specialist | Microsoft Learn MCP |

Each agent accesses only the information required for its responsibility.

---

# 8. Orchestration Model

The solution implements multiple orchestration strategies.

## Sequential

Mandatory workflow execution.

Example:

Incident Intake

↓

Decision

↓

CAPA

↓

Reporting

---

## Parallel

Specialist investigations execute simultaneously.

Complaint Pattern

||

Returns

||

Product/Batch

||

Customer Impact

||

Safety

---

## Fan-In

The Quality Supervisor waits until every specialist returns before continuing.

---

## Conditional

Workflow branches depending on:

- Validation status
- Investigation classification
- CAPA requirement
- Evidence availability

---

## Selective Reassessment

When new evidence is submitted:

Only the affected specialist is re-executed.

The remaining investigation remains unchanged.

---

# 9. Microsoft 365 Integration

The solution integrates Microsoft services.

## Excel Online

Operational data management.

## Word Online

Investigation report generation.

## Outlook

Stakeholder notifications.

## Microsoft Learn MCP

Official Microsoft implementation guidance.

---

# 10. Architectural Principles

The architecture follows these principles:

- Single orchestration authority
- Clear separation of concerns
- Parallel specialist processing
- Deterministic business rules
- Reusable specialist agents
- Controlled data ownership
- Evidence-based decision making
- Scalable workflow execution
- Complete investigation traceability

---

# 11. Benefits

The implemented architecture provides:

- Faster investigations
- Reduced manual effort
- Consistent decision making
- Controlled governance
- Better scalability
- Easier maintenance
- Improved reporting
- Strong auditability
- Reliable Microsoft integration

---

# 12. Conclusion

The Supervisor–Specialist architecture provides a structured, governed, and scalable framework for automating Sleepsia's product quality investigations. By separating orchestration from specialist analysis and enforcing clear tool and knowledge ownership, the solution delivers reliable, traceable, and repeatable quality investigation workflows within Microsoft Copilot Studio.