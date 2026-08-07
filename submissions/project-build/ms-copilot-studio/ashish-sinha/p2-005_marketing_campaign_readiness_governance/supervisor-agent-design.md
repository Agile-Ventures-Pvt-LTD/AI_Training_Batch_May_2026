# Supervisor Agent Design

## P2-005 — Campaign Readiness Supervisor

---

## 1. Identity

| Property | Value |
|----------|-------|
| **Name** | Campaign Readiness Supervisor |
| **Type** | Main Agent (Supervisor) |
| **Platform** | Microsoft Copilot Studio |
| **Orchestration** | Generative Orchestration (required for event triggers) |

---

## 2. Core Responsibilities

The Supervisor is the **central orchestrator** of the entire campaign readiness system. It is the **only** component with authority to:

| Responsibility | Description |
|---------------|-------------|
| **Final Readiness Classification** | Assigns the definitive campaign readiness status |
| **Conflict Resolution** | Resolves conflicting specialist assessments (blocking prevails) |
| **Reassessment Decision** | Decides whether to trigger selective reassessment or assign Manual Review |
| **Word Report Authorisation** | Approves generation of the Campaign Readiness Report |
| **Outlook Communication Authorisation** | Approves sending stakeholder notifications |
| **State Management** | Controls campaign state transitions in Excel |
| **Orchestration Flow Control** | Enforces sequential stage order and conditional routing |

---

## 3. Orchestration Flow

### Stage Sequence
```
1. Recurrence Trigger fires
2. Campaign Intake & Validation topic
3. Parallel fan-out to 4 specialists
4. Wait for all 4 specialist results
5. Fan-in consolidation
6. Invoke Launch Risk & Decision Specialist
7. Validate proposed outcome against precedence rules
8. Conditional routing:
   a. Remediation → Topic 2
   b. Approval → Topic 3
   c. Ready / Not Ready → Continue
9. Supervisor validation (final check)
10. Invoke Reporting & Communication Specialist
11. Update Excel with final status
```

### Stage Dependencies
Each stage has strict prerequisites. The Supervisor enforces that no stage runs before its dependencies are met.

---

## 4. Decision Authority

### Final Readiness Precedence (Mandatory)

| Precedence | Outcome | Criteria |
|-----------|---------|----------|
| 1 (highest) | Not Ready | Any uncorrectable blocker OR launch < 5 days with missing mandatory assets |
| 2 | Management Approval Required | Budget/sensitivity/geography triggers human approval |
| 3 | Remediation Required | Correctable blocking issues identified |
| 4 | Ready with Conditions | Only permitted non-blocking conditions remain |
| 5 (lowest) | Ready | All mandatory requirements satisfied |

**Rule**: If multiple conditions apply, the highest-precedence outcome wins. The Supervisor NEVER averages specialist outcomes.

### Conflict Resolution Rules
- A **blocking** result from ANY specialist overrides pass results from all others
- **Insufficient Evidence** from any specialist prevents a "Ready" classification
- When in doubt, the Supervisor routes for human review

---

## 5. Tools and Knowledge

### Tools
| Tool | Connector | Actions Used |
|------|-----------|-------------|
| Excel Online (Business) | Standard | List rows present in a table, Get a row, Update a row |

### Knowledge Sources
| Document | Purpose |
|----------|---------|
| NovaSphere Marketing Governance Policy | Authoritative policy reference for all readiness rules |

---

## 6. State Management

### Valid States
| State | Meaning |
|-------|---------|
| Pending | Awaiting assessment |
| In Assessment | Currently being assessed |
| Awaiting Remediation | Blocking issues under correction |
| Awaiting Approval | Mandatory human approval outstanding |
| Ready | All requirements satisfied |
| Ready with Conditions | Non-blocking conditions remain |
| Not Ready | Cannot proceed |
| Manual Review | Requires human review |
| Completed | Assessment and communication finished |

### Transition Validation
The Supervisor prevents invalid transitions such as:
- `Pending → Ready` (skipping assessment)
- Any state → `Completed` (without full reporting cycle)
- `In Assessment → Ready` (when any specialist has a block)

---

## 7. Child Agent Management

### Invocation Model
The Supervisor follows Microsoft's recommended orchestration pattern:
```
Invoke specialists → Wait for results → Combine → Respond/Action
```

### Parallel Specialist Invocation
After validation, the Supervisor invokes all 4 domain specialists for the same campaign. It waits until ALL results are returned before proceeding.

### Sequential Specialist Invocation
The Risk Specialist and Reporting Specialist are invoked sequentially — they depend on earlier stages.

### Specialist Failure Protocol
1. Retry the specialist once
2. If still unsuccessful, mark domain as "Insufficient Evidence"
3. Prevent an unsupported "Ready" classification
4. Route for Manual Review

---

## 8. Duplicate Prevention

Before processing any campaign, the Supervisor checks:
- Is the CampaignID already in status: In Assessment / Awaiting Remediation / Awaiting Approval / Completed?
- If yes → skip this campaign, do not create a fresh assessment

---

## 9. Screenshots

### Supervisor Agent Configuration
![Supervisor Agent Configuration](/screenshots/supervisor_agent.png)

### Recurrence Trigger Setup
![Recurrence Trigger Setup](/screenshots/recurrence-trigger.png)

### Final Assessment Flow
![Final Assessment Flow](/screenshots/final_assesment.png)

