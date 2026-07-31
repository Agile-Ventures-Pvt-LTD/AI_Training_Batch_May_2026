# System Architecture

# P2-004: Autonomous Multi-Agent BC/DR Readiness System

## 1. Multi-Agent System Overview
The **P2-004 Autonomous BC/DR Readiness System** is built on a **Supervisor-Specialist** design pattern within Microsoft Copilot Studio (2026 Modern Experience), utilizing connected agents (skills) and generative orchestration.

The architecture is split into two branches:
- **Left Branch (Data & Control Flow)**: Responsible for the autonomous OneDrive file modification trigger, reading pending items from the consolidated workbook `P2-004_BCDR_Lab_Data.xlsx`, writing completed audits back to the register, and generating report files.
- **Right Branch (MCP Grounding & Communication)**: Responsible for connecting to the external Microsoft Learn MCP Server under the Technical Recovery Specialist, and managing Outlook stakeholder notifications.

---

## 2. System Architecture Diagram

Below is the sequence diagram showing how the OneDrive file modification trigger initiates the assessment and how the Supervisor coordinates the connected specialist agents:

```mermaid
sequenceDiagram
    autonumber
    participant Trigger as OneDrive File Trigger
    participant Super as BC/DR Supervisor Agent
    participant Excel as Excel Inventory (Lab Data)
    participant CriticalityAgent as Application Criticality Specialist
    participant RecoveryAgent as Recovery Requirements Specialist
    participant TechAgent as Technical Recovery Specialist
    participant MCPServer as Microsoft Learn MCP Server
    participant RiskAgent as Risk & Recovery Gap Specialist
    participant PlanAgent as Remediation Planning Specialist
    participant ReportAgent as Reporting & Comm Specialist
    participant Outlook as Outlook (Notification)

    Trigger->>Super: 1. Workbook Modified Trigger
    Super->>Excel: 2. Read Application_Inventory (Filter: AssessmentStatus = 'Pending')
    Excel-->>Super: 3. Return Pending Application Row(s)
    
    Note over Super: Generate Assessment ID & Initialize Register State

    Super->>CriticalityAgent: 4. Delegate Criticality Scoping (App Metadata)
    CriticalityAgent-->>Super: 5. Return Business Criticality & Rationale

    Super->>RecoveryAgent: 6. Delegate Recovery Audit (RTO/RPO actuals vs goals)
    RecoveryAgent-->>Super: 7. Return RTO/RPO gaps & manual workaround status

    Super->>TechAgent: 8. Delegate Technical Review (Azure/M365 services used)
    activate TechAgent
    TechAgent->>MCPServer: 9. Search/Fetch Microsoft Learn (HTTP, Anonymous Connection)
    MCPServer-->>TechAgent: 10. Return Microsoft Docs (ASR, SQL Georeplication, etc.)
    TechAgent->>TechAgent: Compare configuration with retrieved guidance
    TechAgent-->>Super: 11. Return Structured Findings (Gaps, Docs, Confidence)
    deactivate TechAgent

    Super->>RiskAgent: 12. Delegate Risk Scoring (Consolidated outputs 5, 7, 11)
    RiskAgent-->>Super: 13. Return Gap Classifications & Overall Readiness

    Super->>PlanAgent: 14. Delegate Action Planning (Classified Gaps list)
    PlanAgent-->>Super: 15. Return Remediation Tasks (Owners, Priority, expected outcomes)

    Note over Super: Supervisor performs final validation of readiness scoring

    Super->>Excel: 16. Update Application_Inventory (Set AssessmentStatus = 'Completed')
    Super->>Excel: 17. Add Row to Assessment_Register

    Super->>ReportAgent: 18. Authorize Report & Notifications
    activate ReportAgent
    ReportAgent->>ReportAgent: 19. Generate Word BC/DR Report
    ReportAgent->>Outlook: 20. Send Conditional Stakeholder Email
    deactivate ReportAgent
```

---

## 3. Component Details & Responsibilities

### 3.1 Orchestration Path (BC/DR Supervisor Agent)
- **Trigger Check**: Executed automatically by the **When a file is modified (OneDrive for Business)** trigger. It reads the inventory table and processes only rows marked `Pending`.
- **Delegation**: Instead of performing calculations, the Supervisor routes structured JSON payloads containing relevant context variables to connected specialist agents.
- **Conflict Resolution**: Applies overrides (e.g. defaulting to the highest risk classification when specialists diverge).
- **Validation**: Checks for missing specialist results, network failures (handling `Technical evidence unavailable`), and assigns readiness.
- **Register Update**: Updates the inventory row status to `Completed` and appends a row to the register.

### 3.2 Specialist Branch (Connected Agents)
- **Application Criticality Specialist**: Uses business parameters (user count, customer-facing, regulatory impact, etc.) to scope business importance.
- **Recovery Requirements Specialist**: Detects logical contradictions like critical workloads missing RTO/RPO goals or slow recovery targets in parent dependencies.
- **Technical Recovery Specialist**: Invokes the Microsoft Learn MCP Server and compares hosting configurations (e.g. Azure SQL, Azure VM) against live guidance. It returns a strict, structured layout (Technology Evaluated, Gaps, Recommendations, Evidence Status, and Confidence Level).
- **Risk & Recovery Gap Specialist**: Categorizes risks from Critical to Low and calculates the final readiness level.
- **Remediation Planning Specialist**: Creates distinct remediation cards mapping directly to identified gaps.
- **Reporting & Communication Specialist**: Uses Word integration to format the executive report, and executes email logic based on readiness (e.g. Routine completion notification vs. Management escalation).
