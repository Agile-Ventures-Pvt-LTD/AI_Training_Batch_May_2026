# Specialist Agent Design

## Project
**P2-005 — Marketing Campaign Readiness & Governance**

## Overview

The solution uses four mandatory specialist agents to independently assess specific campaign-readiness domains.

The specialist agents provide findings and evidence to the Campaign Readiness Supervisor. They do **not** assign the final campaign readiness outcome.

---

## 1. Budget & Commercial Specialist

### Purpose
Assess the financial and commercial readiness of the campaign.

### Responsibilities
- Compare proposed and approved budget.
- Evaluate Target CPL.
- Apply applicable budget rules.
- Identify commercial risks.
- Identify required management approvals.
- Return evidence-based findings.

### Output
Provides:
- Assessment status
- Findings
- Evidence
- Blocking issues
- Approval requirements
- Recommended actions

---

## 2. Brand & Content Compliance Specialist

### Purpose
Assess campaign content against brand and content governance requirements.

### Responsibilities
- Validate brand compliance.
- Validate product naming.
- Review campaign claims.
- Check disclaimers.
- Evaluate content approval status.
- Consider regulatory sensitivity.
- Identify required Brand & Content review.

### Guardrails
- Do not fabricate supporting evidence.
- Do not fabricate approval.
- Report missing evidence explicitly.

---

## 3. Channel Readiness Specialist

### Purpose
Determine whether all selected marketing channels are operationally ready.

### Responsibilities
Evaluate applicable channels such as:

- Email
- LinkedIn
- Paid Search
- Web
- Webinar/Event

For each configured channel, the specialist evaluates its required readiness controls and reports unresolved gaps.

### Output
Provides:
- Channel readiness status
- Channel-specific findings
- Blocking issues
- Outstanding actions
- Supporting evidence

---

## 4. Asset Readiness Specialist

### Purpose
Assess whether mandatory campaign assets are available and ready.

### Responsibilities
- Identify required campaign assets.
- Check asset status.
- Identify missing assets.
- Detect assets pending approval.
- Detect assets requiring changes.
- Evaluate Pending QA conditions.
- Identify blocking asset gaps.

### Example Asset States
- Approved
- Pending QA
- Pending Approval
- Needs Changes
- Missing / Not Started

Missing mandatory assets are treated as blocking findings.

---

## Specialist Invocation

Specialists are invoked only after:

```text
Campaign Intake & Validation = Valid
              |
              v
CampaignStatus = In Assessment
              |
              v
Invoke Specialists