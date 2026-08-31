# Specialist agent design

## Overview

The Autonomous Marketing Campaign Launch Readiness & Governance System uses **six specialist child agents** operating under the control of the **Campaign Readiness Supervisor**.

Each specialist has:

* a clearly defined responsibility,
* scoped tools,
* scoped knowledge,
* structured outputs,
* no authority to assign final readiness.

The Supervisor invokes specialists, consolidates their findings, resolves conflicts, and determines the final campaign readiness classification.

## Multi-agent architecture

```text
Campaign Readiness Supervisor
        |
---------------------------------------------------------
|          |            |            |         |         |
v          v            v            v         v         v
Budget   Brand      Channel      Asset     Risk     Reporting
```

The design intentionally separates domain expertise from governance decision making.

## Standard specialist output contract

Every specialist returns a structured assessment object.

```json
{
  "SpecialistName": "...",
  "AssessmentStatus": "Pass|Condition|Block|Insufficient Evidence",
  "EvidenceSummary": "...",
  "BlockingIssues": [],
  "Conditions": [],
  "RequiredActions": [],
  "RequiredApprover": null,
  "Confidence": "High|Medium|Low",
  "Completed": true
}
```

This common structure enables deterministic fan-in consolidation.

---

# Budget & Commercial Specialist

## Purpose

Evaluate financial and commercial readiness.

## Responsibilities

Assess:

* proposed budget,
* approved budget,
* budget variance,
* target CPL,
* approval thresholds,
* financial blockers.

## Data sources

Excel:

* Campaign_Requests
* Budget_Rules
* Approval_Matrix

## Business rules

Apply:

* budget above approved budget,
* budget above INR 1,000,000,
* CPL above INR 4,000.

## Outputs

Return:

* assessment status,
* variance,
* approval requirement,
* blocking issues,
* required approver,
* financial evidence.

## Tool scope

* Excel Online (Business)

## Authority limitations

Cannot:

* assign final readiness,
* update campaign state,
* generate reports,
* send notifications.

---

# Brand & Content Compliance Specialist

## Purpose

Evaluate brand governance and content compliance.

## Responsibilities

Assess:

* product naming,
* campaign claims,
* regulatory sensitivity,
* disclaimers,
* brand approvals,
* CTA consistency,
* unsupported claims.

## Data sources

Excel:

* Campaign_Requests
* Asset_Status

Knowledge:

* NovaSphere Brand & Content Guidelines

## Outputs

Return:

* compliance status,
* blocking findings,
* content conditions,
* required actions,
* evidence.

## Tool scope

* Excel Online (Business)

## Knowledge scope

* Brand Guidelines only

## Authority limitations

Cannot:

* evaluate budget,
* evaluate channel operations,
* assign final readiness.

---

# Channel Readiness Specialist

## Purpose

Evaluate operational channel readiness.

## Responsibilities

Assess every campaign channel for:

* mandatory assets,
* lead times,
* tracking readiness,
* ownership,
* channel blockers.

## Data sources

Excel:

* Campaign_Requests
* Channel_Requirements
* Asset_Status

## Evaluation rule

Every channel listed in the campaign must be evaluated.

## Outputs

Return:

* channel readiness,
* missing prerequisites,
* timing constraints,
* blocking issues,
* required actions.

## Tool scope

* Excel Online (Business)

## Authority limitations

Cannot:

* evaluate budget,
* evaluate brand compliance,
* assign final readiness.

---

# Asset Readiness Specialist

## Purpose

Evaluate campaign asset readiness.

## Responsibilities

Assess:

* mandatory assets,
* asset availability,
* approval status,
* QA status,
* missing assets,
* ownership.

## Data sources

Excel:

* Asset_Status

## Asset classification

Each asset is classified as:

* Ready
* Condition
* Blocking
* Missing

## Outputs

Return:

* aggregate asset readiness,
* blocking assets,
* missing assets,
* required actions,
* responsible owners.

## Tool scope

* Excel Online (Business)

## Authority limitations

Cannot:

* evaluate budget,
* evaluate channels,
* evaluate brand,
* assign final readiness.

---

# Launch Risk & Decision Specialist

## Purpose

Evaluate consolidated campaign governance risk.

## Responsibilities

Analyze:

* budget result,
* brand result,
* channel result,
* asset result,
* launch timing,
* geography,
* sensitivity,
* pending approvals.

## Risk classification

Assign:

* Low
* Medium
* High
* Critical

## Evaluate

* blocking issues,
* conditions,
* approval exposure,
* timing risk,
* unresolved evidence,
* governance impact.

## Proposed outcomes

Recommend:

* Ready
* Ready with Conditions
* Remediation Required
* Management Approval Required
* Not Ready
* Manual Review

## Tool scope

No direct operational authority.

Uses consolidated specialist outputs.

## Authority limitations

Cannot:

* assign final readiness,
* update campaign state,
* authorize communication.

---

# Reporting & Communication Specialist

## Purpose

Generate reports and execute stakeholder communication.

## Responsibilities

Generate:

* Microsoft Word Campaign Launch Readiness Report.

Execute:

* Outlook stakeholder notifications.

Update:

* report location in Excel.

## Data sources

Excel:

* Campaign_Requests
* Stakeholders

Inputs:

* final readiness,
* risk level,
* specialist summaries,
* remediation actions,
* approvals.

## Word report content

Includes:

* campaign details,
* specialist assessments,
* blocking issues,
* conditions,
* approvals,
* risk classification,
* final readiness,
* next steps.

## Notification routing

Supports:

* Ready
* Ready with Conditions
* Awaiting Approval
* Awaiting Remediation
* Not Ready
* Manual Review

## Tool scope

* Word Online (Business)
* Outlook
* Excel Online (Business)

## Authority limitations

May execute communication only after Supervisor authorization.

---

# Tool and knowledge ownership

| Specialist | Excel | Knowledge | Word | Outlook |
| ---------- | ----- | --------- | ---- | ------- |
| Budget     | Yes   | No        | No   | No      |
| Brand      | Yes   | Yes       | No   | No      |
| Channel    | Yes   | No        | No   | No      |
| Asset      | Yes   | No        | No   | No      |
| Risk       | No    | No        | No   | No      |
| Reporting  | Yes   | No        | Yes  | Yes     |

This narrow scoping reduces orchestration ambiguity and prevents unnecessary tool exposure.

---

# Responsibility separation

The design follows strict separation of concerns.

## Specialists own

* analysis,
* evidence,
* domain expertise,
* recommendations.

## Supervisor owns

* orchestration,
* state management,
* governance precedence,
* conflict resolution,
* reassessment,
* final readiness,
* reporting authorization,
* communication authorization.

This separation ensures deterministic governance and prevents child agents from issuing unsupported launch decisions.

---

# Interaction model

## Initial assessment

```text
Supervisor
     |
     +---- Budget
     |
     +---- Brand
     |
     +---- Channel
     |
     +---- Asset
```

## Fan-in

```text
Budget
Brand
Channel
Asset
     |
     v
Supervisor
```

## Reassessment

```text
Corrected Data
      |
      v
Affected Specialist Only
      |
      v
Supervisor
```

This interaction model enables efficient specialist reuse and selective reassessment.

---

# Failure handling

Specialists must return **Insufficient Evidence** when:

* required data is unavailable,
* Excel access fails,
* evidence is incomplete,
* analysis cannot be completed.

The Supervisor performs retry and escalation.

Specialists never fabricate successful assessments.

---

# Design rationale

The specialist-agent architecture provides:

* domain isolation,
* explainable assessments,
* reusable expertise,
* scalable orchestration,
* deterministic governance,
* maintainable Copilot Studio implementation.

The resulting multi-agent design aligns with enterprise governance principles while preserving centralized control through the Campaign Readiness Supervisor.
