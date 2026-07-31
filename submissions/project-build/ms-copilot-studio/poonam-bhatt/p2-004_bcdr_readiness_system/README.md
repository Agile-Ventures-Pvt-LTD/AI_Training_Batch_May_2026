# P2-004: Autonomous Multi-Agent Business Continuity & Disaster Recovery (BC/DR) Readiness System

## 1. Project Overview
This repository contains the implementation evidence, design documentation, and configuration templates for the **Autonomous Multi-Agent BC/DR Readiness System** built using **Microsoft Copilot Studio (2026 Modern Experience)**.

The system autonomously evaluates the disaster recovery readiness of business-critical applications within the enterprise **NovaSphere Technologies Pvt. Ltd.** It utilizes a **Supervisor Agent** to coordinate six specialized agents, retrieving live technical guidance from Microsoft documentation via a manually configured **Model Context Protocol (MCP) server**, and generates actionable management artifacts in Microsoft Word and Excel, with notifications sent via Outlook.

### 1.1 Core Objectives
- **Autonomous Event-Driven Triggering**: Initiate assessments without human chat interaction (e.g., when the consolidated workbook is modified in OneDrive).
- **Supervisor-Specialist Orchestration**: Separate concerns across 6 specialist connected agents coordinated by a central Supervisor.
- **MCP-Based Grounding**: Retrieve real-time, non-hallucinated Microsoft technical documentation.
- **Tool and Business Integration**: Automate recovery register updates (Excel), report generation (Word), and conditional escalation (Outlook).
- **Robust Risk Scoping**: Classify gaps (Critical, High, Medium, Low) and determine overall readiness (Ready, Ready with Minor Gaps, Remediation Required, High Risk, Insufficient Evidence).

---

## 2. Published Agent & Connection Status
- **Published URL**: `https://copilotstudio.preview.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/63612c18-cd8c-f111-8077-000d3af21e08/overview`
- **Agent ID**: `bcdr-readiness-supervisor-p2-004`
- **Active Connectors & Tools**:
  - **Microsoft Excel Online (Business)**: Connected to the consolidated workbook `P2-004_BCDR_Lab_Data.xlsx` (worksheets: `Application_Inventory`, `Assessment_Register`, `Risk_Scoring_Rules`).
  - **Microsoft Word Online (Business)**: Connected to the template for automated BC/DR report creation.
  - **Microsoft Office 365 Outlook**: Configured for conditional email notifications and management escalation.
  - **Model Context Protocol (MCP) Connector**: Streamable HTTP connection to the Microsoft Learn MCP server at `https://learn.microsoft.com/api/mcp` attached *only* to the `Technical Recovery Specialist`.

---

## 3. Directory Structure
The repository is organized according to the prescribed GitHub submission structure:

```
p2-004_bcdr_readiness_system/
├── README.md                    # This file (Project overview, URL, and status)
├── solution-summary.md          # Business problem, architecture, logic, and outcomes
├── architecture.md              # Sequence diagram and multi-agent data flow
├── supervisor-agent-design.md   # Supervisor decision logic, triggers, and state machine
├── specialist-agents.md         # Instructions and parameters for all 6 specialists
├── mcp-implementation.md        # Manually configured Microsoft Learn MCP details
├── autonomous-trigger.md        # Trigger payload, recurrence rules, and filters
├── test-report.md               # Detailed execution evidence for 25 test cases
├── known-limitations.md         # Tenant constraints, API thresholds, and failures
├── ai-usage-declaration.md      # Generative AI usage statement and verification
├── data/                        # Business data and configuration files
│   ├── application-inventory.xlsx
│   ├── assessment-register.xlsx
│   ├── risk-scoring-rules.xlsx
└── screenshots/                 # Captured implementation evidence
    ├── supervisor-agent.png
    ├── child-agents.png
    ├── autonomous-trigger.png
    ├── mcp-configuration.png
    ├── mcp-tools.png
    ├── mcp-successful-call.png
    ├── specialist-delegation.png
    ├── excel-tool.png
    ├── word-tool.png
    ├── outlook-tool.png
    └── final-assessment.png
```

---

## 4. Setup and Configuration Steps
1. **Model Context Protocol (MCP) Server Setup**:
   - Manually register the Microsoft Learn MCP server in Copilot Studio.
   - Set the server URL to: `https://learn.microsoft.com/api/mcp`
   - Select **Streamable HTTP** as the transport type.
   - Ground the **Technical Recovery Specialist** to use this connection.
   - Use the **Connection Manager** in Copilot Studio to authorize the HTTP connection (Create Connection $\rightarrow$ Allow, keeping auth as Anonymous/None).

2. **Trigger Activation**:
   - Set up the Copilot Studio trigger **When a file is modified (OneDrive for Business)** linked to the Supervisor Agent.
   - Configure it to monitor the folder and workbook `P2-004_BCDR_Lab_Data.xlsx` in OneDrive.
   - Modify any row in `Application_Inventory` (setting `AssessmentStatus` to `"Pending"`) and save the workbook to trigger the Supervisor autonomously.
   - Ensure **Generative Orchestration** is enabled in the Agent Builder UI.
3. **Publishing**:
   - Publish the Supervisor Agent to the Web Channel to activate the autonomous recurrence listeners and connection mapping.
