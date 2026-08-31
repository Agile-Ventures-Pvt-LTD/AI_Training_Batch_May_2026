# 🧩 Custom Topics
---

# 📖 Overview

The Campaign Readiness Governance solution implements **three mandatory reusable custom topics** that coordinate the end-to-end campaign governance workflow.

Each topic represents a distinct phase of the campaign lifecycle and is orchestrated by the **Campaign Readiness Supervisor**.

Rather than embedding all workflow logic inside a single conversation, the solution separates business processes into modular, reusable topics.

---

# 🎯 Topic Architecture

```text
Campaign Readiness Supervisor
              │
              ▼
┌────────────────────────────────────────────┐
│ Campaign Intake & Validation               │
└────────────────────────────────────────────┘
              │
              ▼
      Specialist Assessments
              │
              ▼
┌────────────────────────────────────────────┐
│ Remediation & Selective Reassessment       │
└────────────────────────────────────────────┘
              │
              ▼
┌────────────────────────────────────────────┐
│ Approval & Finalisation                    │
└────────────────────────────────────────────┘
              │
              ▼
        Campaign Completed
```

---

# 📌 Topic 1 — Campaign Intake & Validation

## 🎯 Purpose

This topic acts as the **entry point** for every campaign readiness assessment.

It retrieves campaign information, prepares the assessment context, and initiates specialist evaluations under the control of the Campaign Readiness Supervisor.

---

## Responsibilities

The topic is responsible for:

- 📥 Starting a campaign assessment
- 📊 Retrieving campaign data from Excel
- 📋 Preparing campaign information
- 🤖 Invoking specialist agents
- 🔄 Returning execution control to the Supervisor

---

## Connected Components

### Tool

📊 Excel Online (Business)

- CampaignRequestsTable

---

### Invoked Specialist Agents

- 💰 Budget & Commercial Specialist
- 🛡 Brand & Content Compliance Specialist
- 📣 Channel Readiness Specialist
- 🖼 Asset Readiness Specialist
- 🚀 Launch Risk & Decision Specialist
- 📄 Reporting & Communication Specialist

---

## Workflow

```text
Trigger

↓

Retrieve Campaign

↓

Prepare Campaign Context

↓

Invoke Budget Specialist

↓

Invoke Brand Specialist

↓

Invoke Channel Specialist

↓

Invoke Asset Specialist

↓

Invoke Launch Risk Specialist

↓

Invoke Reporting Specialist

↓

Return Control to Supervisor
```

---

## Expected Outcome

- Campaign information prepared
- Specialist assessments initiated
- Workflow progresses to the next stage

---

## Screenshot

![Campaign Intake & Validation Topic](/screenshots/intake_topics.png)

---

# 🔄 Topic 2 — Remediation & Selective Reassessment

## 🎯 Purpose

This topic coordinates corrective actions when campaign issues require remediation before approval.

It enables the Supervisor to initiate reassessment after campaign updates have been made.

---

## Responsibilities

- ⚠ Inform users that remediation is required
- 🔄 Coordinate reassessment
- 🤖 Reinvoke specialist agents
- 📋 Return updated findings to the Supervisor

---

## Workflow

```text
Campaign Requires Remediation

↓

Launch Risk Specialist

↓

Budget Specialist

↓

Brand Specialist

↓

Channel Specialist

↓

Asset Specialist

↓

Reporting Specialist

↓

Return to Supervisor
```

---

## Expected Outcome

- Updated specialist assessments
- Revised campaign findings
- Workflow continues toward approval

---

## Screenshot

![Remediation Workflow (Demonstrated in Final Assessment)](/screenshots/final_assesment.png)

---

# ✅ Topic 3 — Approval & Finalisation

## 🎯 Purpose

This topic represents the final stage of the campaign governance lifecycle.

It consolidates assessment outcomes, generates reporting artifacts, and prepares stakeholder communication.

---

## Responsibilities

- 📄 Generate readiness report
- 🚀 Coordinate final launch recommendation
- 📊 Update campaign status
- 📧 Notify stakeholders
- ✅ Complete workflow

---

## Invoked Specialist Agents

- 🚀 Launch Risk & Decision Specialist
- 📄 Reporting & Communication Specialist

---

## Workflow

```text
Prepare Final Assessment

↓

Launch Risk Specialist

↓

Reporting Specialist

↓

Generate Report

↓

Update Excel

↓

Send Outlook Notification

↓

Workflow Completed
```

---

## Expected Outcome

- Final readiness recommendation
- Campaign report generated
- Campaign tracker updated
- Stakeholders notified

---

## Screenshot

![Approval & Finalisation Workflow (Demonstrated in Final Assessment)](/screenshots/final_assesment.png)

---

# 🔄 Topic Interaction

The three topics work together as a complete governance workflow.

```text
Campaign Intake

↓

Specialist Assessment

↓

Remediation (if required)

↓

Approval

↓

Campaign Completed
```

---

# 🎛 Topic Responsibilities

| Topic | Primary Responsibility | Output |
|--------|------------------------|--------|
| 📌 Campaign Intake & Validation | Start assessment and invoke specialists | Assessment initiated |
| 🔄 Remediation & Selective Reassessment | Coordinate reassessment | Updated findings |
| ✅ Approval & Finalisation | Produce final decision | Campaign completed |

---

# 📊 Topic-to-Agent Mapping

| Topic | Specialist Agents |
|--------|------------------|
| Campaign Intake & Validation | All six specialists |
| Remediation & Selective Reassessment | Launch Risk, Budget, Brand, Channel, Asset, Reporting |
| Approval & Finalisation | Launch Risk, Reporting |

---

# 🔗 Integration

Each topic integrates with Microsoft 365 services through specialist agents.

| Service | Usage |
|----------|-------|
| 📊 Excel Online | Campaign data retrieval and update |
| 📄 Microsoft Word | Readiness report generation |
| 📧 Outlook | Stakeholder communication |

---

# 📈 Benefits

The modular topic design provides:

- 🧩 Reusable workflow components
- 🎯 Clear separation of responsibilities
- 🔄 Easier maintenance
- ⚡ Simplified orchestration
- 📊 Better readability
- 📈 Scalable architecture

---

# 📸 Implementation Evidence

The implementation is supported by the following screenshots.

- **Intake Topic**: ![Campaign Intake & Validation](/screenshots/intake_topics.png)
- **Remediation & Approval Flows**: ![Final Assessment](/screenshots/final_assesment.png)

---

# ✅ Conclusion

The Campaign Readiness Governance solution implements all **three mandatory reusable custom topics** required by the project specification.

The topics divide the campaign lifecycle into logical stages, enabling the Campaign Readiness Supervisor to coordinate specialist agents, remediation workflows, and final approval through a structured and maintainable orchestration model.

This modular approach improves readability, reusability, and long-term scalability while supporting enterprise campaign governance.