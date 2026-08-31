# Specialist Agent Design

## Standard Output Contract

Every specialist must return equivalent semantic information:

| Field | Meaning |
|---|---|
| SpecialistName | Specialist identity |
| AssessmentStatus | Pass / Condition / Block / Insufficient Evidence |
| EvidenceSummary | Evidence used |
| BlockingIssues | Blocking findings |
| Conditions | Non-blocking findings |
| RequiredActions | Remediation required |
| RequiredApprover | Human approver where applicable |
| Confidence | High / Medium / Low |
| Completed | Yes / No |

Different internal variable names are acceptable, but the semantic structure must remain consistent.

---

## 1. Budget & Commercial Specialist

### Description

Evaluates campaign budget and commercial controls.

### Responsibilities

- Proposed budget
- Approved budget
- Budget variance
- Target CPL
- Expected leads
- Required financial approval
- Budget-related blocking conditions

### Knowledge / Data

- Campaign_Requests
- Budget_Rules
- Approval_Matrix
- Governance Policy

### Output

Return the standard output contract plus:

- Proposed budget
- Approved budget
- Variance
- CPL assessment
- Approval required
- Required approver
- Recommended action
- Evidence used

---

## 2. Brand & Content Compliance Specialist

### Description

Evaluates brand and content compliance.

### Responsibilities

- Product naming
- Campaign claims
- Regulatory sensitivity
- Required disclaimers
- Brand approval
- Restricted or unsupported claims
- CTA consistency
- External agency implications

### Knowledge

Mandatory:

`NovaSphere Brand & Content Guidelines`

### Data

- Campaign Requests
- Asset Status

### Boundary

Must not perform budget analysis or channel-operational analysis.

---

## 3. Channel Readiness Specialist

### Description

Evaluates every channel listed for the campaign.

### Responsibilities

- Mandatory channel assets
- Minimum lead time
- Tracking requirement
- Channel owner
- Brand approval requirement
- Missing channel prerequisite
- Channel-specific blocker

### Data

- Campaign Requests
- Channel Requirements
- Asset Status

### Important Rule

Evaluate **all** campaign channels, not only the first channel.

---

## 4. Asset Readiness Specialist

### Description

Evaluates campaign asset readiness.

### Responsibilities

- Mandatory assets
- Asset availability
- Asset approval status
- Missing assets
- Pending QA
- Pending approval
- Needs Changes
- Responsible owner

### Classification

Each asset should be classified as:

- Ready
- Condition
- Blocking
- Missing

The specialist returns aggregate counts to the Supervisor.

---

## 5. Launch Risk & Decision Specialist

### Execution Order

Runs after Budget, Brand, Channel, and Asset assessments.

### Inputs

- Budget result
- Brand result
- Channel result
- Asset result
- Days to launch
- Geography
- Sensitivity
- Pending approvals

### Responsibilities

Identify:

- Blocking issues
- Non-blocking conditions
- Approval requirements
- Timing risk
- Unresolved evidence
- Campaign risk level

### Risk Levels

- Low
- Medium
- High
- Critical

### Boundary

This specialist may propose a readiness outcome, but the Supervisor must validate it.

---

## 6. Reporting & Communication Specialist

### Execution Order

Runs only after Supervisor validation.

### Word Report

The Campaign Launch Readiness Report should contain:

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

### Outlook

After Supervisor approval, send the correct stakeholder notification.

The notification should differ according to the final outcome.

### Boundary

Do not send final launch communication before Supervisor validation.
