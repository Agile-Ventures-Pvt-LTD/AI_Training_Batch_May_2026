# qualification-logic.md — Qualification Logic
## P2-003 Autonomous Sales Lead Qualification Agent

---

## Overview

Lead qualification runs across 8 weighted dimensions producing a score from 0 to 100. The score is then mapped to a classification. Override rules can change the classification independently of the score. Duplicate detection and confidence assessment run before and after scoring.

---

## Scoring Model

### Dimension 1 — Product Fit (Max 20 points)

| Band | Points | Rule |
|---|---|---|
| Strategic | 20 | Direct match to a NovaWorks strategic product (Custom Agentic AI Platform, Enterprise RAG, Autonomous Sales Ops, Multi-Agent Service Ops, AI Governance) |
| Standard | 12 | Valid NovaWorks product but non-strategic or smaller engagement (AI Agent Enablement Workshop) |
| Limited | 5 | Partial product match requiring discovery |
| Unsupported | -20 | No supported NovaWorks offering or non-sales inquiry type |

### Dimension 2 — Budget vs Product Minimum (Max 20 points)

| Band | Points | Rule |
|---|---|---|
| At or above recommended minimum | 20 | Budget meets or exceeds the product minimum price |
| 75% to below minimum | 15 | Potentially viable with scope adjustment |
| 50% to below 75% of minimum | 10 | Material budget gap |
| Below 50% of minimum | 4 | Low commercial viability |
| Unknown | 0 | Budget not provided — record as Unknown, do not treat as zero |

**Product Minimum Prices:**
| Product | Minimum Budget |
|---|---|
| AI Agent Enablement Workshop | $15,000 |
| Enterprise RAG Knowledge Assistant | $60,000 |
| Autonomous Sales Operations Agent | $90,000 |
| Multi-Agent Service Operations System | $140,000 |
| AI Governance and Evaluation Accelerator | $75,000 |
| Custom Agentic AI Platform Implementation | $250,000 |

### Dimension 3 — Purchase Timeline (Max 15 points)

| Band | Points | Rule |
|---|---|---|
| 0–30 days | 15 | Immediate purchase window |
| 31–90 days | 10 | Near-term purchase window |
| 91–180 days | 5 | Medium-term purchase window |
| Over 180 days or unknown | 0 | Long-term or missing timeline — record as Unknown, do not treat as zero |

### Dimension 4 — Decision Role (Max 15 points)

| Value | Points | Rule |
|---|---|---|
| Decision Maker | 15 | Budget holder or final approver |
| Strong Influencer | 8 | Can shape the decision but cannot approve alone |
| Researcher/User | 3 | Early-stage evaluator or end user |
| Unknown | 0 | Role is missing or unclear |

### Dimension 5 — Company Size (Max 10 points)

| Value | Points | Employee Range |
|---|---|---|
| Enterprise | 10 | 1,000 or more employees |
| Mid-Market | 7 | 200–999 employees |
| SMB | 4 | 20–199 employees |
| Startup/Micro | 2 | Fewer than 20 employees |

### Dimension 6 — Territory (Max 10 points)

| Value | Points | Rule |
|---|---|---|
| Supported | 10 | Country maps to a named sales owner in TerritoryOwnersTable |
| Management Review | 5 | Country exists but requires sales operations review |
| Unmapped | 0 | Country not found in TerritoryOwnersTable — triggers Human Review override |

### Dimension 7 — Lead Source (Max 5 points)

| Value | Points |
|---|---|
| Executive or Partner Referral | 5 |
| Customer Referral or Industry Event | 4 |
| Website or Inbound | 3 |
| Cold or Unknown | 1 |

### Dimension 8 — Completeness (Max 5 points)

| Value | Points | Rule |
|---|---|---|
| All mandatory fields present | 5 | No missing information |
| One or two fields missing | 3 | Follow-up can resolve gaps |
| Three or more fields missing | 0 | Insufficient for autonomous qualification — triggers override |

---

## Classification Thresholds

| Score Range | Classification |
|---|---|
| 85 – 100 | Hot |
| 70 – 84 | Qualified |
| 50 – 69 | Nurture |
| 0 – 49 | Low Priority |

---

## Override Rules

Override rules are evaluated after the score is calculated. Overrides change the classification independently of the score. Both the score and the override reason are recorded in the Excel row.

### Override 1 — Startup/Micro Low Priority Override
**Condition:** Company Size is Startup/Micro AND Budget is below 50% of the product minimum price
**Result:** Classification forced to Low Priority regardless of calculated score
**Rationale:** Eliminates commercially non-viable leads from Hot and Qualified pipelines

### Override 2 — Unmapped Territory Human Review
**Condition:** Country does not appear in TerritoryOwnersTable
**Result:** Classification forced to Human Review Required. Autonomous owner assignment is not permitted.
**External communication:** Suppressed — no qualification result sent to the sender

### Override 3 — Missing Fields Human Review
**Condition:** Three or more mandatory fields are missing (Completeness score = 0)
**Result:** Classification forced to Human Review Required
**External communication:** Suppressed — no qualification result sent to the sender

### Override 4 — Additional Information Required
**Condition:** One or two specific fields are missing that prevent a reliable score
**Result:** Classification set to Additional Information Required
**External communication:** A missing fields request is sent to the sender listing exactly which fields are needed

### Override 5 — Low Confidence Human Review
**Condition:** The agent cannot determine a reliable classification from the available information
**Result:** Classification forced to Human Review Required
**External communication:** Suppressed

---

## Duplicate Detection

Duplicate detection runs at Step 3, before any scoring takes place.

**Method:** Excel Get Rows — search LeadsRegisterTable for records matching the same Company Name and Contact Name within the last 90 days.

**On duplicate found:**
- Update the existing Excel row (Last_Action timestamp)
- Do not create a new row
- Do not create a new Word report
- Do not send a new acknowledgement

**Idempotency:** The agent also checks Source_Message_ID if available to detect repeated Outlook trigger deliveries of the same email.

---

## Normalisation Rules

These normalisation rules run at Step 4 before scoring:

| Field | Allowed Values | Normalisation |
|---|---|---|
| Country | Must match TerritoryOwnersTable | If not found, flag as unmapped |
| Product Interest | Must match ProductCatalogTable | If not found, flag as unknown product |
| Company Size | Enterprise, Mid-Market, SMB, Startup/Micro | Map non-standard values to nearest category |
| Decision Role | Decision Maker, Strong Influencer, Researcher/User, Unknown | Map non-standard values (e.g. Final Approver → Decision Maker) |
| Budget | Numeric USD value | If absent, record as Unknown — do not score as zero |
| Timeline | Integer days | If absent, record as Unknown — do not score as zero |

---

## Confidence Levels

| Level | Condition | Autonomous Action Permitted |
|---|---|---|
| High | All mandatory fields present, territory mapped, no exceptions | Full autonomous action including external communications |
| Medium | One or two fields missing, scoreable | Nurture or Low Priority actions only |
| Low | Three or more fields missing, territory unmapped, or ambiguous | Human Review only — no external qualification result |
