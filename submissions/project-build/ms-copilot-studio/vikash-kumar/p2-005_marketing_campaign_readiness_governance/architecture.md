# 🏗️ System Architecture

> **Project:** P2-005 – Marketing Campaign Readiness Governance
>
> **Platform:** Microsoft Copilot Studio
>
> **Architecture Pattern:** Supervisor–Specialist Multi-Agent System

---

# 🎯 Architecture Overview

The Campaign Readiness Governance solution is built using a **hierarchical multi-agent architecture** where a central **Supervisor Agent** coordinates multiple specialized AI agents responsible for evaluating different aspects of a marketing campaign.

Rather than embedding all business logic inside a single agent, responsibilities are divided into independent specialists, improving scalability, maintainability, and governance.

The Supervisor orchestrates the complete workflow while specialist agents focus only on their domain expertise.

---

# 🧠 High-Level Architecture

```text
                           User
                             │
                             ▼
                 Campaign Readiness Supervisor
                             │
     ┌───────────────────────┼────────────────────────┐
     │                       │                        │
     ▼                       ▼                        ▼
Campaign Intake        Validation Logic         Workflow Control
                             │
                             ▼
                  Specialist Agent Orchestration
                             │
 ┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
 ▼              ▼              ▼              ▼              ▼
Budget      Brand &        Channel        Asset         Launch Risk
Agent       Compliance     Readiness      Readiness     Specialist
                             │
                             ▼
          Reporting & Communication Specialist
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
   Excel Update         Word Report         Outlook Email
                             │
                             ▼
                    Final Campaign Decision
```

---

# 🏛️ Architectural Layers

The solution is divided into five logical layers.

---

## 👤 Presentation Layer

This is the user interaction layer.

Components include:

- Microsoft Copilot Studio Chat Interface
- Campaign Readiness Supervisor
- Test Console

Responsibilities:

- Accept campaign requests
- Display assessment progress
- Present final recommendations

---

## 🧠 Orchestration Layer

The orchestration layer contains the Supervisor Agent.

Responsibilities include:

- Workflow coordination
- Topic execution
- Child agent invocation
- Response consolidation
- Decision routing

The Supervisor never performs specialist analysis directly.

Instead, it delegates work to dedicated specialist agents.

---

## 👥 Specialist Layer

Each specialist agent owns a single business capability.

| Agent | Responsibility |
|---------|----------------|
| 💰 Budget & Commercial Specialist | Budget feasibility and commercial review |
| 🛡 Brand & Content Compliance Specialist | Branding and compliance validation |
| 📢 Channel Readiness Specialist | Marketing channel assessment |
| 🖼 Asset Readiness Specialist | Creative asset verification |
| 🚀 Launch Risk & Decision Specialist | Launch risk evaluation |
| 📄 Reporting & Communication Specialist | Reporting and stakeholder communication |

This separation ensures high cohesion and low coupling.

---

## 🔗 Integration Layer

The solution integrates with Microsoft 365 services.

### 📊 Excel Online

Purpose

- Campaign repository
- Campaign status updates
- Final assessment storage

---

### 📄 Microsoft Word

Purpose

- Generate Campaign Readiness Report

---

### 📧 Microsoft Outlook

Purpose

- Notify stakeholders
- Send assessment reports
- Communicate approval decisions

---

## 💾 Data Layer

Campaign data is stored in an Excel table.

Example fields include:

- Campaign ID
- Campaign Name
- Product
- Budget
- Target CPL
- Geography
- Channels
- Owner
- Campaign Status
- Assessment Status

This dataset acts as the primary data source for all specialist assessments.

---

# 🔄 End-to-End Workflow

The architecture follows the lifecycle below.

```text
User

↓

Campaign Intake

↓

Validation

↓

Budget Assessment

↓

Brand Assessment

↓

Channel Assessment

↓

Asset Assessment

↓

Launch Risk Assessment

↓

Reporting

↓

Approval

↓

Campaign Ready
```

---

# 📌 Supervisor Responsibilities

The Supervisor Agent performs orchestration only.

Its responsibilities include:

✅ Receive campaign request

✅ Validate campaign information

✅ Invoke specialist agents

✅ Coordinate workflow

✅ Handle remediation

✅ Consolidate assessments

✅ Produce final recommendation

The Supervisor never performs business-specific evaluations itself.

---

# 👥 Specialist Responsibilities

Each specialist focuses on one business capability.

Benefits include:

- Independent development
- Easy maintenance
- Clear ownership
- Modular expansion
- Reusability

Each specialist returns a structured assessment rather than free-form responses.

---

# 📂 Custom Topics

Three mandatory reusable topics implement the workflow.

---

## 1️⃣ Campaign Intake & Validation

Purpose

- Retrieve campaign
- Validate campaign data
- Prepare workflow

Invokes:

- Budget Specialist
- Brand Specialist
- Channel Specialist
- Asset Specialist
- Launch Risk Specialist
- Reporting Specialist

---

## 2️⃣ Remediation & Selective Reassessment

Purpose

Handle failed assessments.

Activities include:

- Review issues
- Trigger reassessment
- Update findings
- Return revised assessment

---

## 3️⃣ Approval & Finalisation

Purpose

Generate the final decision.

Activities include:

- Consolidate specialist outputs
- Generate report
- Update Excel
- Notify stakeholders

---

# 🔄 Data Flow

```text
Excel Dataset

↓

Supervisor

↓

Specialist Agents

↓

Assessment Results

↓

Reporting Specialist

↓

Excel Update

↓

Word Report

↓

Outlook Notification

↓

Final Response
```

---

# 🧩 Tool Integration

The following Microsoft tools are integrated into the solution.

| Tool | Purpose |
|------|---------|
| 📊 Excel Online | Read and update campaign records |
| 📄 Word | Generate readiness report |
| 📧 Outlook | Notify stakeholders |

These integrations automate administrative work and reduce manual effort.

---

# 🛡 Error Handling Strategy

The architecture includes basic resilience mechanisms.

Examples:

- Missing campaign records return validation errors.
- Specialist failures halt approval.
- Invalid campaign status prevents workflow progression.
- Failed reassessments return the campaign to remediation.
- Missing mandatory fields stop execution before assessments begin.

---

# 📈 Scalability

The architecture is designed to support future expansion.

Possible enhancements include:

- Additional specialist agents
- Dataverse integration
- SharePoint repositories
- Power BI dashboards
- Microsoft Teams notifications
- Approval workflows
- AI-generated executive summaries

No architectural redesign is required to introduce additional specialist agents.

---

# 🔒 Security Considerations

The solution follows Microsoft 365 security boundaries.

Security principles include:

- Least privilege access
- Secure Microsoft connectors
- Controlled Excel access
- Organization-level authentication
- No external public data exposure

---

# 📸 Architecture Evidence

The following screenshots support this architecture.

- 📷 supervisor-agent.png
- 📷 child-agents.png
- 📷 intake-topic.png
- 📷 parallel-specialists.png
- 📷 remediation-topic.png
- 📷 approval-topic.png
- 📷 excel-tools.png
- 📷 word-tool.png
- 📷 outlook-tool.png
- 📷 final-assessment.png

---

# ✅ Architectural Benefits

The implemented architecture provides several enterprise advantages.

✔ Modular design

✔ Reusable specialist agents

✔ Clear separation of responsibilities

✔ Centralized orchestration

✔ Easy extensibility

✔ Automated reporting

✔ Simplified maintenance

✔ Microsoft 365 integration

✔ Enterprise-ready governance

✔ Consistent campaign assessment workflow

---

# 🏁 Conclusion

The Campaign Readiness Governance solution adopts a Supervisor–Specialist multi-agent architecture that enables centralized orchestration while delegating domain-specific decisions to dedicated AI specialists.

This design improves maintainability, scalability, transparency, and governance while satisfying the mandatory project requirements for Microsoft Copilot Studio.