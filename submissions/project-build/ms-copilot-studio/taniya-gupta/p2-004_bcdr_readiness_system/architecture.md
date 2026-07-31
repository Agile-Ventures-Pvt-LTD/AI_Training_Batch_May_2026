# System Architecture (`architecture.md`)

## High-Level Architecture

The **P2-004 Autonomous Multi-Agent BC/DR Readiness System** is built on **Microsoft Copilot Studio**. A single **Supervisor Agent** coordinates a pipeline of **6 Child Specialist Agents**, external data stores and an external Model Context Protocol (MCP) server.

```mermaid
flowchart TD
    subgraph TriggerLayer [Trigger Layer]
        T1[OneDrive File Modified Trigger]
        T2[Copilot Studio Test Chat]
    end

    subgraph SupervisorLayer [Orchestration Layer]
        SUP[BC/DR Supervisor Agent]
    end

    subgraph DataLayer [Data Layer]
        EXCEL_INV[(P2-004_BCDR_Lab_Data.xlsx\nApplicationInventoryTable)]
        EXCEL_REG[(P2-004_BCDR_Lab_Data.xlsx\nAssessmentRegisterTable)]
        WORD_TMPL[BCDR Report Template.docx]
    end

    subgraph SpecialistLayer [Specialist Child Agents]
        SA1[1. Application Criticality Specialist]
        SA2[2. Recovery Requirements Specialist]
        SA3[3. Technical Recovery Specialist]
        SA4[4. Risk and Gap Specialist]
        SA5[5. Remediation Planning Specialist]
        SA6[6. Reporting & Communication Specialist]
    end

    subgraph MCPLayer [External Protocol Layer]
        MCP_SERVER[Microsoft Learn MCP Server\nhttps://learn.microsoft.com/api/mcp]
    end

    subgraph OutputLayer [Communication & Delivery Layer]
        WORD_OUT[OneDrive: BCDR_Assessment_Report_AppID.docx]
        MAIL_OUT[Outlook 365 Email Notification]
    end

    T1 --> SUP
    T2 --> SUP

    SUP -->|List Rows| EXCEL_INV
    SUP -->|Step 4: Handoff Context| SA1
    SA1 -->|Criticality Result| SUP
    SUP -->|Step 5: Handoff Context| SA2
    SA2 -->|RTO/RPO Gaps| SUP
    SUP -->|Step 6: Handoff Context| SA3
    SA3 <-->|Tool: microsoft_docs_search| MCP_SERVER
    SA3 -->|Technical Findings| SUP
    SUP -->|Step 7: Consolidate Outputs| SA4
    SA4 -->|Gap List & Readiness Rating| SUP
    SUP -->|Step 9: Handoff Gap List| SA5
    SA5 -->|Remediation Plan| SUP
    SUP -->|Step 10: Authorize Execution| SA6
    SA6 -->|Create File| WORD_OUT
    SA6 -->|Add Row| EXCEL_REG
    SA6 -->|Send Email V2| MAIL_OUT
```

---

## Error Handling & Resiliency Patterns

- **Dynamic Filter Pre-fill**: Prevents Copilot Studio from prompting the user for input during automated runs.
- **MCP Fallback**: If MCP is unreachable, Child Agent 3 sets `MCPEvidenceStatus = "Unavailable"` and continues assessment without breaking the pipeline.
- **Synthetic Email Resolver**: Maps synthetic `.example` domains in sample data to active Microsoft 365 user `Taniya.Gupta@agileventures.net` while retaining owner names in body.
- **Sequential Execution Lock**: Explicit instructions force single-pass execution of child agents to prevent generative retry loops.
