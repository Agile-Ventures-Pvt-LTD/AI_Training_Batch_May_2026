# Orchestration Patterns

## P2-005 — Marketing Campaign Readiness & Governance System

This document details how each of the six mandatory orchestration patterns is implemented in the solution.

---

## 1. Sequential Pattern

### Definition
Stages execute in a strict order where later stages depend on earlier stages completing successfully.

### Implementation

The following stages execute in sequence — a later stage **never** executes before its required earlier stages complete:

```
Stage 1: Recurrence Trigger
    ↓
Stage 2: Campaign Intake & Validation
    ↓ (only if validation passes)
Stage 3: Parallel Specialist Assessments (fan-out)
    ↓ (only after ALL specialists return)
Stage 4: Supervisor Fan-In Consolidation
    ↓
Stage 5: Launch Risk & Decision Specialist
    ↓
Stage 6: Conditional Routing (Remediation / Approval / Final)
    ↓
Stage 7: Supervisor Validation
    ↓ (only after validation)
Stage 8: Reporting (Word)
    ↓ (only after Word succeeds or is handled)
Stage 9: Excel Update
    ↓
Stage 10: Communication (Outlook)
```

### Sequential Dependencies Enforced

| Stage | Cannot Execute Until |
|-------|---------------------|
| Specialist Assessments | Campaign validation passes AND status is "In Assessment" |
| Fan-In Consolidation | ALL four specialists have returned results |
| Risk Assessment | Fan-in consolidation is complete |
| Reporting (Word) | Supervisor has validated the final readiness classification |
| Outlook Notification | Supervisor has approved communication AND Word step is handled |
| Excel Status Update | Readiness has been determined |

### Evidence
- **Screenshot**: ![Campaign Intake Topic](/screenshots/intake_topics.png) — shows validation completing before specialist invocation
- **Screenshot**: ![Final Assessment Outcome](/screenshots/final_assesment.png) — shows sequential flow from risk assessment to reporting

---

## 2. Parallel Fan-Out/Fan-In Pattern

### Definition
Multiple independent agents process the same input simultaneously, and the orchestrator waits for all results before proceeding.

### Implementation

#### Fan-Out (Parallel Invocation)
After campaign validation, the Supervisor invokes **four specialist child agents** for the same campaign:

1. **Budget & Commercial Specialist** — evaluates financial viability
2. **Brand & Content Compliance Specialist** — evaluates brand/content compliance
3. **Channel Readiness Specialist** — evaluates channel readiness
4. **Asset Readiness Specialist** — evaluates asset availability

These specialists:
- Operate **independently** of each other
- Analyse the **same campaign** from **different domain perspectives**
- Have **non-overlapping responsibilities** (budget ≠ brand ≠ channel ≠ asset)
- Each return a structured output following the Standard Specialist Output Contract

#### Fan-In (Result Consolidation)
The Supervisor:
1. **Waits** until all four specialists have returned their results
2. **Collects** all AssessmentStatus values (Pass / Condition / Block / Insufficient Evidence)
3. **Aggregates** all BlockingIssues and Conditions
4. **Identifies** all RequiredApprovers
5. **Detects** conflicts between specialist results

> **Note**: "Parallel" means independent fan-out/fan-in orchestration. Whether Copilot Studio executes the child-agent calls simultaneously at the infrastructure level is a platform detail.

### Evidence
- **Screenshot**: ![Parallel Specialists Configuration](/screenshots/parlalel_specialist.png) — shows all four specialists configured
- **Screenshot**: ![Supervisor Consolidation / Final Assessment](/screenshots/final_assesment.png) — shows the Supervisor consolidation logic outcome

---

## 3. Hierarchical Pattern

### Definition
A parent agent controls child agents, owns decision authority, and delegates specific responsibilities.

### Implementation

#### Hierarchy Structure
```
Campaign Readiness Supervisor (Parent)
├── Budget & Commercial Specialist (Child)
├── Brand & Content Compliance Specialist (Child)
├── Channel Readiness Specialist (Child)
├── Asset Readiness Specialist (Child)
├── Launch Risk & Decision Specialist (Child)
└── Reporting & Communication Specialist (Child)
```

#### Supervisor Authority (Exclusive)
The Supervisor is the **only** component permitted to:
- Assign the **final readiness classification**
- **Resolve conflicts** between specialist assessments
- Decide whether **reassessment** is required
- **Authorise** Word report generation
- **Authorise** Outlook communication

#### Specialist Constraints
Child agents:
- Return **findings** to the Supervisor
- Do **not** independently announce final decisions
- Have **scoped tools and knowledge** relevant to their domain only
- Follow the **Standard Specialist Output Contract** for structured responses

### Evidence
- **Screenshot**: ![Supervisor Agent Configuration](/screenshots/supervisor_agent.png) — shows the Supervisor agent configuration
- **Screenshot**: ![Child Agents Under Supervisor](/screenshots/child_agent.png) — shows all child agents under the Supervisor

---

## 4. Conditional Routing Pattern

### Definition
Different execution paths are taken based on specific conditions evaluated at runtime.

### Implementation

#### Condition: Budget Thresholds
| Condition | Route |
|-----------|-------|
| ProposedBudget > ApprovedBudget | → Approval topic (Marketing Director) |
| ProposedBudget > INR 1,000,000 | → Approval topic (VP Marketing) |
| TargetCPL > INR 4,000 | → Approval topic (VP Marketing) |

#### Condition: Sensitivity
| Condition | Route |
|-----------|-------|
| RegulatorySensitivity = "High" | → Additional brand review + management approval |
| RegulatorySensitivity = "Medium" or "Low" | → Standard assessment |

#### Condition: Geography
| Condition | Route |
|-----------|-------|
| Geography ≠ "India" (multi-market) | → Regional Marketing Lead approval |
| Geography = "India" | → Standard assessment |

#### Condition: Assessment Outcome
| Condition | Route |
|-----------|-------|
| All specialists Pass, no conditions | → Ready → Reporting |
| Blocking issues, correctable | → Remediation & Reassessment topic |
| Budget/sensitivity/geography triggers | → Approval & Finalisation topic |
| Uncorrectable blocks OR launch < 5 days with missing assets | → Not Ready → Reporting |
| Specialist failure / insufficient evidence | → Manual Review → Reporting |

#### Condition: Reporting Outcome
| Condition | Route |
|-----------|-------|
| Word generation succeeds | → Update Excel → Send Outlook |
| Word generation fails | → Preserve in Excel → Mark report failed → Skip Outlook |
| Outlook fails | → Preserve assessment → Mark notification failed |

### Evidence
- **Screenshot**: ![Approval Topic Flow (Demonstrated in Final Assessment)](/screenshots/final_assesment.png) — shows conditional routing in the Approval topic
- **Screenshot**: ![Remediation Flow (Demonstrated in Final Assessment)](/screenshots/final_assesment.png) — shows conditional routing to remediation

---

## 5. Loop / Reassessment Pattern

### Definition
Failed conditions trigger a corrective cycle, after which the system selectively re-evaluates only the affected areas.

### Implementation

#### Reassessment Flow
```
Initial Assessment
    │
    ▼ (Blocking issues detected)
Remediation & Selective Reassessment Topic
    │
    ├── Identify failed specialist domains
    ├── Create remediation actions
    ├── Set status "Awaiting Remediation"
    ├── Detect data corrections
    ├── Identify stale results (only changed domains)
    ├── Rerun ONLY affected specialists ◄── KEY: Selective
    ├── Preserve already-passed results
    └── Return to Supervisor for re-consolidation
         │
         ├── If still blocking → Cycle 2 (repeat above)
         │                        │
         │                        ├── If still blocking after Cycle 2 → Manual Review
         │                        │
         │                        └── If resolved → Proceed to final readiness
         │
         └── If resolved → Proceed to final readiness
```

#### Selective Reassessment Rule
- **Only rerun** specialists whose underlying data has changed
- **Preserve** results from specialists that already passed and whose data hasn't changed
- **Example**: If a missing landing page is corrected, reassess Channel/Asset only — do NOT rerun Budget

#### Loop Control
- **Maximum 2 automated reassessment cycles**
- After 2 unsuccessful cycles → assign "Manual Review"
- This prevents infinite remediation loops

### Evidence
- **Screenshot**: ![Reassessment Loop (Demonstrated in Final Assessment)](/screenshots/final_assesment.png) — shows the reassessment loop with cycle counter

---

## 6. Fallback / Escalation Pattern

### Definition
When a specialist fails, times out, or returns unusable information, the system handles the failure gracefully rather than fabricating results.

### Implementation

#### Specialist Failure Handling

```
Specialist Invocation
    │
    ├── Success → Normal processing
    │
    └── Failure (no response / unusable data / access error / insufficient evidence)
         │
         ├── RETRY once
         │    │
         │    ├── Success → Normal processing
         │    │
         │    └── Still fails
         │         │
         │         ├── Mark domain as "Insufficient Evidence"
         │         ├── PREVENT unsupported "Ready" classification
         │         └── Route to "Manual Review"
```

#### Tool Failure Handling

| Tool | Failure | Response |
|------|---------|----------|
| Excel Online | Cannot read data | Mark assessment as incomplete, log error |
| Word Online | Cannot create report | Preserve readiness in Excel, mark report failed, do NOT claim report exists |
| Outlook | Cannot send email | Preserve assessment, mark notification failed, do NOT claim stakeholders were notified |
| Excel Online | Cannot update status | Log failure, preserve assessment data, alert for manual update |

#### Critical Rule
A specialist failure must **never** result in an unsupported "Ready" classification. The system always errs on the side of caution — routing to Manual Review rather than fabricating a positive outcome.

### Evidence
- **Screenshot**: ![Fallback/Escalation Handling](/screenshots/final_assesment.png) — shows fallback handling in the assessment flow
