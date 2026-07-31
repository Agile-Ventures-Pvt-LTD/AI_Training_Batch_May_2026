# Supervisor Agent Design

# P2-004: Autonomous Multi-Agent BC/DR Readiness System

## 1. Supervisor Role & Responsibilities
The **BC/DR Supervisor Agent** is the central coordinator in the Copilot Studio 2026 Modern Experience. It governs the orchestration flow of a BC/DR readiness assessment.

Its core responsibilities include:
1. **OneDrive Trigger Action**: Responding to the workbook modification event trigger ("When a file is modified (OneDrive for Business)") on the Excel workbook to begin processing.
2. **Excel Pending Record Scrutiny**: Interacting with `P2-004_BCDR_Lab_Data.xlsx` to find records in the `Application_Inventory` sheet with `AssessmentStatus = "Pending"`.
3. **Assessment ID Generation**: Programmatically creating a unique assessment identifier (`BCDR-2026-XXXX` or `ASM-XXXX`).
4. **Context Passing**: Parsing variables from the target application record (such as `CurrentCriticality`, `CurrentRTOHours`, `RequiredRTOHours`, etc.) and passing them as JSON-like slot structures to connected specialist agents.
5. **Specialist Handoff Coordination**: Invoking connected specialist agents in sequence (Criticality $\rightarrow$ Recovery $\rightarrow$ Technical $\rightarrow$ Risk $\rightarrow$ Remediation $\rightarrow$ Reporting).
6. **Conflict Resolution**: Implementing the override logic when specialists diverge (e.g. override rule: "Always default to the highest risk classification").
7. **Readiness Determination**: Scoring gaps using the decision matrix and handling MCP lookup failures (intercepting `Technical evidence unavailable` and mapping to `Insufficient Evidence`).
8. **Audit Trail Logging**: Writing findings back to the `Assessment_Register` sheet, changing `AssessmentStatus` to `"Completed"`, and authorizing the Reporting agent to generate Word/Outlook notifications.

---

## 2. Trigger Mappings & Excel Integration
The Supervisor is wired to the consolidated workbook **`P2-004_BCDR_Lab_Data.xlsx`** stored in OneDrive for Business.

| Action | Target Sheet | Mapped Key | Key Columns / Variables |
| :--- | :--- | :--- | :--- |
| **List rows present** | `Application_Inventory` | `AssessmentStatus == "Pending"` | Reads all metadata context (RTO, RPO, platform, services, backup frequency, owners) |
| **Add a row** | `Assessment_Register` | `AssessmentID` | Records assessment outcomes, gap counts, and final readiness classification |
| **Update a row** | `Application_Inventory` | `ApplicationID` | Changes `AssessmentStatus` from `"Pending"` to `"Completed"` once finalized |

---

## 3. Delegation Logic & Process Flow

```text
  [OneDrive File Modified Trigger]
     (P2-004_BCDR_Lab_Data.xlsx)
                 │
                 ▼
     [BC/DR Supervisor Agent]
                 │
    [Read Application_Inventory]
 (Filter: AssessmentStatus = 'Pending')
                 │
                 ▼
     (Assessment ID Generated)
   (e.g., ASM-0001, ASM-0002)
                 │
                 ▼
┌──────────────────────────────────────┐
│ 1. Application Criticality Agent     │ -> Scopes Business Criticality
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│ 2. Recovery Requirements Agent       │ -> Audits RTO/RPO actuals vs goals
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│ 3. Technical Recovery Agent          │ -> Connects to MS Learn MCP
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│ 4. Risk & Recovery Gap Agent         │ -> Scores consolidated gap counts
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│ 5. Remediation Planning Agent        │ -> Groups fix tasks and deadlines
└──────────────────┬───────────────────┘
                   │
                   ▼
    [Supervisor Score Validation]  <──- Conflict Override / MCP Failure Checks
                   │
       ┌───────────┴───────────┐
       ▼ (Pass)                ▼ (Fail/Network Timeout)
  [Readiness Assigned]     [Status: Insufficient Evidence]
       │                       │
       └───────────┬───────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│ 6. Reporting & Communication Agent   │ -> Updates Excel, Word doc, Outlook
└──────────────────────────────────────┘
```

---

## 4. Supervisor Decision Matrix (Readiness Classification)

The Supervisor evaluates outputs from the connected specialist agents using the following rules to assign the overall readiness status:

| Business Criticality | Critical Gaps | High Gaps | Medium Gaps | MCP Lookup Status | Overall Readiness | Escalation Notification |
| :--- | :---: | :---: | :---: | :--- | :--- | :--- |
| **Mission Critical** | $\ge 1$ | Any | Any | Successful | **High Risk** | Urgent alert to Director & CIO |
| **Mission Critical** | 0 | 0 | 0 | Successful | **Ready** | Standard completion email |
| **Business Critical**| 0 | $\ge 1$ | Any | Successful | **Remediation Required** | Tasks sent to Technical Owner |
| **Important** | 0 | 0 | $\ge 1$ | Successful | **Ready with Minor Gaps** | Advisory notice to Tech Owner |
| **Standard** | 0 | 0 | 0 | Successful | **Ready** | Standard completion email |
| **Any** | Any | Any | Any | Unsuccessful / Fail | **Insufficient Evidence** | Owner notified; request missing info |

### 4.1 Scoring, Conflicts, and Failure Handling Rules
- **Conflict Resolution Rule**: When specialist classifications diverge (e.g. Criticality Specialist rates an app as `Standard` but Risk Specialist flags a regulatory SOX gap as `Critical`), the Supervisor overrides the conflict by applying the rule: **"Always default to the highest risk classification."**
- **MCP Failure Interception**: If the Technical Recovery Specialist returns `Technical evidence unavailable` due to an MCP connection failure, the Supervisor intercepts this string, bypasses standard matrix calculations, marks the final status as `Insufficient Evidence`, and alerts the cloud administrator.
