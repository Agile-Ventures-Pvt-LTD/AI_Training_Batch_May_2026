# Specialist Agent Design

## 1. Overview

The P2-005 solution uses six specialist child agents under the **Campaign Readiness Supervisor**.

The specialist agents have non-overlapping responsibilities. The first four specialists perform independent assessments in the parallel fan-out stage. The **Launch Risk & Decision Specialist** runs after fan-in, and the **Reporting & Communication Specialist** runs only after Supervisor validation.

The Supervisor remains the only component permitted to assign the final readiness classification, resolve specialist conflicts, decide reassessment, authorize Word generation, and authorize Outlook communication. fileciteturn8file2L364-L371

---

## 2. Specialist Architecture

```text
                         Supervisor
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
           Budget           Brand          Channel
         Specialist       Specialist      Specialist
              |               |               |
              +---------------+---------------+
                              |
                              v
                       Asset Specialist
                              |
                              v
                         FAN-IN
                              |
                              v
                 Launch Risk & Decision
                       Specialist
                              |
                              v
                    Supervisor Validation
                              |
                              v
                Reporting & Communication
                       Specialist
```

The first four specialists form the independent parallel assessment stage. The Launch Risk & Decision Specialist is explicitly part of the sequential stage after parallel fan-in. fileciteturn8file0L140-L184

---

# 3. Specialist Agent 1 — Budget & Commercial Specialist

## Purpose

Evaluate the financial and commercial readiness of the campaign.

## Responsibilities

The specialist evaluates:

- Proposed budget
- Approved budget
- Budget variance
- Target CPL
- Expected leads
- Required financial approval
- Budget-related blocking conditions

These responsibilities are defined by the PRD. fileciteturn8file0L11-L29

## Data Sources

Use:

- `Campaign_Requests`
- `Budget_Rules`
- `Approval_Matrix`

fileciteturn8file0L30-L34

## Required Output

Return:

- Assessment status
- Proposed budget
- Approved budget
- Variance
- CPL assessment
- Approval required
- Required approver
- Blocking issues
- Recommended action
- Evidence used

fileciteturn8file0L35-L46

## Scope Restriction

This agent should remain focused on budget and commercial assessment and should not take over the responsibilities of the Brand, Channel, or Asset specialists.

---

# 4. Specialist Agent 2 — Brand & Content Compliance Specialist

## Purpose

Evaluate brand, content, claims, and compliance readiness.

## Responsibilities

The specialist evaluates:

- Product naming
- Campaign claims
- Regulatory sensitivity
- Required disclaimers
- Brand approval
- Restricted or unsupported claims
- CTA consistency
- External agency implications

fileciteturn8file0L47-L58

## Knowledge Source

Mandatory knowledge source:

- **NovaSphere Brand & Content Guidelines**

fileciteturn8file0L84-L86

## Data Sources

Use applicable rows from:

- `Campaign Requests`
- `Asset Status`

fileciteturn8file0L87-L90

## Scope Restriction

The PRD explicitly states that this specialist **must not perform budget or channel-operational analysis**. fileciteturn8file0L91-L91

---

# 5. Specialist Agent 3 — Channel Readiness Specialist

## Purpose

Evaluate the readiness of every channel included in the campaign.

## Responsibilities

For every campaign channel, determine:

- Mandatory channel assets
- Minimum lead time
- Tracking requirement
- Channel owner
- Brand approval requirement
- Missing channel prerequisite
- Channel-specific launch blocker

fileciteturn8file0L92-L103

## Data Sources

Use:

- `Campaign Requests`
- `Channel Requirements`
- `Asset Status`

fileciteturn8file0L104-L108

## Important Requirement

The specialist must evaluate **all channels included in the campaign**, not only the first channel. fileciteturn8file0L109-L109

## Scope Restriction

The agent should remain focused on channel readiness and should not duplicate the detailed financial, brand-content, or asset-readiness assessment assigned to other specialists.

---

# 6. Specialist Agent 4 — Asset Readiness Specialist

## Purpose

Evaluate whether the required campaign assets are ready for launch.

## Responsibilities

Evaluate:

- Mandatory assets
- Asset availability
- Asset approval status
- Missing assets
- Pending QA
- Pending approval
- Assets requiring changes
- Responsible owner

fileciteturn8file0L122-L132

## Asset Classification

Each asset must be classified as one of:

- `Ready`
- `Condition`
- `Blocking`
- `Missing`

fileciteturn8file0L133-L138

## Required Output

The specialist must return **aggregate counts** to the Supervisor. fileciteturn8file0L139-L139

---

# 7. Standard Output Contract

To simplify fan-in consolidation, each specialist should return equivalent structured information containing:

| Output | Requirement |
|---|---|
| `SpecialistName` | Name of specialist |
| `AssessmentStatus` | Pass / Condition / Block / Insufficient Evidence |
| `EvidenceSummary` | Information used |
| `BlockingIssues` | Blocking findings |
| `Conditions` | Non-blocking findings |
| `RequiredActions` | Required remediation |
| `RequiredApprover` | Human approver where applicable |
| `Confidence` | High / Medium / Low |
| `Completed` | Yes / No |

The PRD allows different variable names, but the semantic structure must remain consistent. fileciteturn8file7L1195-L1207

---

# 8. Parallel Fan-Out

The first four specialists are independent domain assessors:

```text
                    Supervisor
                        |
       +----------------+----------------+
       |                |                |
       v                v                v
    Budget            Brand           Channel
       |                |                |
       +----------------+----------------+
                        |
                        v
                      Asset
                        |
                        v
                       Fan-In
```

The Supervisor must consolidate their results before moving to the next decision stage.

The architecture specifically requires independent specialist assessments and fan-in consolidation. fileciteturn8file1L215-L229

---

# 9. Specialist Agent 5 — Launch Risk & Decision Specialist

## Purpose

Evaluate consolidated specialist results after the first four specialist assessments have completed.

## Execution Position

This specialist runs **after the first four specialists** and therefore forms part of the sequential stage following parallel fan-in. fileciteturn8file0L140-L143

## Inputs

The specialist receives:

- Budget result
- Brand result
- Channel result
- Asset result
- Days until launch
- Geography
- Sensitivity
- Pending approvals

fileciteturn8file0L144-L170

## Responsibilities

Identify:

- Blocking issues
- Non-blocking conditions
- Approval requirements
- Timing risk
- Unresolved evidence
- Campaign risk level

fileciteturn8file0L171-L178

## Risk Levels

The campaign risk level must use:

- `Low`
- `Medium`
- `High`
- `Critical`

fileciteturn8file0L179-L183

## Decision Authority

This specialist **proposes** a readiness outcome.

It does not own the final decision.

The Supervisor must validate the proposed outcome. fileciteturn8file0L184-L184

---

# 10. Specialist Agent 6 — Reporting & Communication Specialist

## Purpose

Generate the campaign readiness report and perform approved stakeholder communication.

## Execution Position

This specialist executes **only after Supervisor validation**. fileciteturn8file7L1145-L1147

## Word Report Responsibility

Create a **Campaign Launch Readiness Report** containing:

- Campaign ID
- Campaign name
- Objective
- Launch date
- Days to launch
- Budget assessment
- Brand assessment
- Channel assessment
- Asset assessment
- Blocking gaps
- Conditions
- Required approvals
- Risk classification
- Final readiness status
- Remediation actions
- Recommended next steps

fileciteturn8file7L1148-L1189

## Outlook Responsibility

After Supervisor approval, send the correct stakeholder notification.

The notification must differ based on the final outcome. fileciteturn8file7L1192-L1194

---

# 11. Tool and Knowledge Scoping

The PRD requires tools and knowledge to be scoped narrowly rather than exposing every capability to every child agent. fileciteturn8file3L622-L633

| Agent | Primary Capability |
|---|---|
| Budget Specialist | Excel financial/rule data |
| Brand Specialist | Brand knowledge + campaign/asset data |
| Channel Specialist | Excel channel requirements |
| Asset Specialist | Excel asset status |
| Risk Specialist | Consolidated specialist outputs |
| Reporting Specialist | Word + Outlook |

The Supervisor owns overall orchestration and campaign-state control. fileciteturn8file3L624-L632

---

# 12. Knowledge Source Allocation

## Marketing Governance Policy

Authoritative for:

- Readiness statuses
- Budget approval
- Timing
- Asset controls
- Geography
- Sensitivity
- Autonomous-processing rules
- Reassessment

## Brand & Content Guidelines

Authoritative for:

- Brand terminology
- Product naming
- Claims
- Evidence requirements
- Channel-content rules
- Brand review classification

fileciteturn8file3L585-L620

The Brand specialist specifically requires **NovaSphere Brand & Content Guidelines**. fileciteturn8file0L84-L86

---

# 13. Specialist Independence

Each specialist must remain within its assigned domain.

```text
Budget Specialist
    → Financial / commercial assessment

Brand Specialist
    → Brand / content / compliance assessment

Channel Specialist
    → Channel readiness assessment

Asset Specialist
    → Asset readiness assessment

Risk Specialist
    → Consolidated risk and proposed readiness

Reporting Specialist
    → Report generation and approved communication
```

Specialist responsibilities must remain non-overlapping, which is also an acceptance criterion for the project. fileciteturn8file4L644-L661

---

# 14. Failure Handling

Specialists must not fabricate successful results when evidence is unavailable.

The solution must handle:

- Specialist failure
- Incomplete evidence
- Conflicting specialist results
- Missing Excel rows
- Missing campaign information

A specialist failure must not result in an unsupported `Ready` classification. fileciteturn8file5L847-L868

The system must preserve traceability by identifying the specialist findings used in the final assessment. fileciteturn8file5L869-L875

---

# 15. Relationship with the Supervisor

The specialist lifecycle is:

```text
Supervisor
    |
    +--> Budget Specialist
    |
    +--> Brand Specialist
    |
    +--> Channel Specialist
    |
    +--> Asset Specialist
             |
             v
          Fan-In
             |
             v
    Launch Risk & Decision
             |
             v
        Supervisor
             |
             v
   Final Readiness Validation
             |
             v
 Reporting & Communication
```

Child agents return findings rather than independently announcing final decisions. fileciteturn8file2L364-L371

---

# 16. Key Design Rules

1. Keep specialist responsibilities non-overlapping.
2. Run the first four specialists as independent assessments.
3. Consolidate their outputs through the Supervisor.
4. Run Launch Risk & Decision after fan-in.
5. Run Reporting & Communication only after Supervisor validation.
6. Use narrowly scoped tools and knowledge.
7. Return structured specialist outputs.
8. Preserve evidence and blocking findings.
9. Do not fabricate missing evidence or approvals.
10. Do not allow child agents to make the final readiness decision.

These rules ensure that the specialist-agent layer follows the architecture and governance requirements defined in the P2-005 PRD.
