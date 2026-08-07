# System Architecture

## P2-005 — Autonomous Marketing Campaign Launch Readiness & Governance System

---

## 1. Architecture Overview

The solution implements a **hierarchical multi-agent architecture** within Microsoft Copilot Studio. A central **Supervisor Agent** orchestrates six **specialist child agents** through a defined set of sequential stages, parallel fan-out/fan-in patterns, conditional routing, bounded reassessment loops, and fallback mechanisms.

### Logical Architecture Diagram

```
                    ┌─────────────────────┐
                    │  Recurrence Trigger  │
                    │  (Event - Scheduled) │
                    └──────────┬──────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │  CAMPAIGN READINESS SUPERVISOR │
                │  (Main Orchestrator Agent)     │
                │                                │
                │  • Owns final decisions        │
                │  • Resolves conflicts          │
                │  • Controls state transitions  │
                │  • Authorises reporting         │
                └──────────────┬────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  TOPIC 1: Campaign   │
                    │  Intake & Validation │
                    └──────────┬──────────┘
                               │
                          Validated?
                         /          \
                       No            Yes
                       │              │
                    [Exit]    [Mark "In Assessment"]
                                      │
              ┌───────────┬───────────┼───────────┬───────────┐
              ▼           ▼           ▼           ▼           │
        ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
        │ BUDGET & │ │ BRAND &  │ │ CHANNEL  │ │  ASSET   │  │
        │COMMERCIAL│ │ CONTENT  │ │READINESS │ │READINESS │  │
        │SPECIALIST│ │COMPLIANCE│ │SPECIALIST│ │SPECIALIST│  │
        │          │ │SPECIALIST│ │          │ │          │  │
        │ Excel:   │ │ Excel:   │ │ Excel:   │ │ Excel:   │  │
        │ Budget   │ │ Assets   │ │ Channels │ │ Assets   │  │
        │ Rules    │ │          │ │ Assets   │ │          │  │
        │ Approval │ │ Knowledge│ │          │ │          │  │
        │ Matrix   │ │ Brand    │ │          │ │          │  │
        │          │ │ Guidelines│ │         │ │          │  │
        └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘  │
             │            │            │             │        │
             └────────────┴─────┬──────┴─────────────┘        │
                                │                              │
                    ┌───────────▼───────────┐                  │
                    │  SUPERVISOR FAN-IN    │                  │
                    │  Consolidation        │                  │
                    └───────────┬───────────┘                  │
                                │                              │
                    ┌───────────▼───────────┐                  │
                    │  LAUNCH RISK &        │                  │
                    │  DECISION SPECIALIST  │                  │
                    │  (Sequential - Post   │                  │
                    │   Fan-In)             │                  │
                    └───────────┬───────────┘                  │
                                │                              │
                    ┌───────────▼───────────┐                  │
                    │  SUPERVISOR DECISION  │                  │
                    │  (Precedence Rules)   │                  │
                    └───┬───────┬───────┬───┘                  │
                        │       │       │                      │
              ┌─────────▼──┐ ┌─▼──────┐ ┌▼─────────────┐      │
              │   Ready /   │ │TOPIC 2 │ │   TOPIC 3    │      │
              │ Ready w/    │ │Remediat│ │  Approval &  │      │
              │ Conditions  │ │& Reasse│ │ Finalisation │      │
              │             │ │ssment  │ │              │      │
              │  Not Ready  │ │(Max 2  │ │  Awaiting    │      │
              │  Manual Rev.│ │cycles) │ │  Approval    │      │
              └──────┬──────┘ └───┬────┘ └──────┬───────┘      │
                     │            │             │              │
                     └────────────┴──────┬──────┘              │
                                         │                     │
                    ┌────────────────────▼────────────────┐    │
                    │  SUPERVISOR VALIDATION              │    │
                    │  (Verify outcome before reporting)  │    │
                    └────────────────────┬────────────────┘    │
                                         │                     │
                    ┌────────────────────▼────────────────┐    │
                    │  REPORTING & COMMUNICATION          │    │
                    │  SPECIALIST                         │    │
                    │                                     │    │
                    │  ┌─────────────┐  ┌──────────────┐  │    │
                    │  │ Word Online  │  │   Outlook    │  │    │
                    │  │ (Business)  │  │ (Office 365) │  │    │
                    │  │             │  │              │  │    │
                    │  │ Campaign    │  │ Stakeholder  │  │    │
                    │  │ Readiness   │  │ Notification │  │    │
                    │  │ Report      │  │              │  │    │
                    │  └─────────────┘  └──────────────┘  │    │
                    └────────────────────┬────────────────┘    │
                                         │                     │
                    ┌────────────────────▼────────────────┐    │
                    │  EXCEL REGISTER UPDATE              │◄───┘
                    │  (Update CampaignStatus + outcome)  │
                    └─────────────────────────────────────┘
```

---

## 2. Agent Inventory

| # | Agent Name | Type | Tools | Knowledge |
|---|-----------|------|-------|-----------|
| 1 | Campaign Readiness Supervisor | Main (Supervisor) | Excel Online (Business) - Campaign status updates | Governance Policy |
| 2 | Budget & Commercial Specialist | Child Agent | Excel: Campaign_Requests, Budget_Rules, Approval_Matrix | Governance Policy |
| 3 | Brand & Content Compliance Specialist | Child Agent | Excel: Campaign_Requests, Asset_Status | Brand & Content Guidelines |
| 4 | Channel Readiness Specialist | Child Agent | Excel: Campaign_Requests, Channel_Requirements, Asset_Status | Governance Policy |
| 5 | Asset Readiness Specialist | Child Agent | Excel: Campaign_Requests, Asset_Status | Governance Policy |
| 6 | Launch Risk & Decision Specialist | Child Agent | None (receives consolidated data) | Governance Policy |
| 7 | Reporting & Communication Specialist | Child Agent | Word Online (Business), Outlook | None |

---

## 3. Custom Topics

| # | Topic Name | Purpose | Invocation Context |
|---|-----------|---------|-------------------|
| 1 | Campaign Intake & Validation | Pre-assessment validation, duplicate prevention, field checks | After recurrence trigger fires |
| 2 | Remediation & Selective Reassessment | Correctable issue handling, bounded loops (max 2) | When specialist assessments identify correctable blockers |
| 3 | Approval & Finalisation | Mandatory human approval routing | When budget/sensitivity/geography triggers approval |

---

## 4. Connector Architecture

| Connector | Type | Used By | Purpose |
|-----------|------|---------|---------|
| Excel Online (Business) | Standard | Supervisor, Budget, Brand, Channel, Asset Specialists | Read campaign data, rules, assets; update status |
| Word Online (Business) | Premium | Reporting Specialist | Generate Campaign Readiness Report |
| Outlook (Office 365) | Standard | Reporting Specialist | Send stakeholder notifications |

---

## 5. Data Architecture

### Excel Workbook Tables

| Table | Records | Key Field | Used By |
|-------|---------|-----------|---------|
| Campaign_Requests | 6 | CampaignID | Supervisor, All Specialists |
| Budget_Rules | 6 | CampaignID | Budget Specialist |
| Channel_Requirements | 10 | Channel | Channel Specialist |
| Asset_Status | 24 | CampaignID + AssetName | Brand, Channel, Asset Specialists |
| Approval_Matrix | 7 | ApprovalType | Budget Specialist, Approval Topic |
| Stakeholders | 8 | Role | Reporting Specialist |

### Knowledge Documents

| Document | Scope | Authoritative For |
|----------|-------|------------------|
| NovaSphere Marketing Governance Policy | Supervisor, Budget, Channel, Asset, Risk | Readiness statuses, budget thresholds, timing rules, asset controls, geography, sensitivity, reassessment |
| NovaSphere Brand & Content Guidelines | Brand Specialist | Brand terminology, product naming, claims, evidence requirements, channel-content rules |

---

## 6. State Machine

```
                    ┌─────────┐
                    │ Pending │ (Initial state)
                    └────┬────┘
                         │ (Validation passes)
                    ┌────▼────────────┐
              ┌─────│ In Assessment   │─────┐
              │     └────┬────────────┘     │
              │          │                  │
    ┌─────────▼──────┐   │    ┌─────────────▼──────────┐
    │ Awaiting       │   │    │ Awaiting Approval      │
    │ Remediation    │   │    └────────────┬────────────┘
    └────┬───────────┘   │                 │
         │ (≤2 cycles)  │                 │
         └──────┬────────┘                 │
                │                          │
    ┌───────────▼───┐  ┌──────────────┐   │
    │ Ready with    │  │ Not Ready    │   │
    │ Conditions    │  └──────────────┘   │
    └───────┬───────┘                     │
            │         ┌──────────────┐    │
    ┌───────▼───┐     │ Manual       │    │
    │  Ready    │     │ Review       │    │
    └───────┬───┘     └──────────────┘    │
            │                             │
            └──────────┬──────────────────┘
                  ┌────▼─────┐
                  │Completed │ (After reporting)
                  └──────────┘
```

### Valid State Transitions

| From | To | Condition |
|------|----|-----------|
| Pending | In Assessment | Validation passes, status updated in Excel |
| In Assessment | Ready | All specialists pass, no conditions |
| In Assessment | Ready with Conditions | Only non-blocking conditions remain |
| In Assessment | Not Ready | Uncorrectable blockers |
| In Assessment | Awaiting Remediation | Correctable blocking issues |
| In Assessment | Awaiting Approval | Budget/sensitivity/geography triggers |
| In Assessment | Manual Review | Specialist failure or insufficient evidence |
| Awaiting Remediation | In Assessment | Data corrected, selective reassessment |
| Awaiting Remediation | Manual Review | 2 failed reassessment cycles |
| Any final state | Completed | After reporting and communication |

---

## 7. Supporting Screenshots

### Central Orchestrator (Supervisor)
![Supervisor Agent Configuration](/screenshots/supervisor_agent.png)

### Child Agent Architecture
![Child Agents Overview](/screenshots/child_agent.png)

### Intake Topic Configuration
![Intake Topic](/screenshots/intake_topics.png)

### Final Assessment & Execution Flow
![Final Assessment](/screenshots/final_assesment.png)

