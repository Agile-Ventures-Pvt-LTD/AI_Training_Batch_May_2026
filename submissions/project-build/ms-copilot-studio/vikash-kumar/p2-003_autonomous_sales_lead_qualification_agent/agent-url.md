# 🔗 Agent URL

## 🚀 Project Information

| Property | Details |
|----------|---------|
| **Project ID** | P2-003 – Autonomous Sales Lead Qualification Agent |
| **Participant** | Vikash Kumar |
| **Agent Name** | NovaWorks Autonomous Sales Lead Qualification Agent |
| **Platform** | Microsoft Copilot Studio |
| **Environment** | Agile Consulting Pvt. Ltd. |
| **Deployment Status** | 🟢 Published |

---

# 🌐 Published Agent

The autonomous sales lead qualification agent has been successfully developed, configured, tested, and published using Microsoft Copilot Studio.

### Agent URL

https://copilotstudio.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/d3af7856-a48c-f111-8077-000d3af21e08/overview

---

# 🔐 Authentication & Access

The agent is deployed within a Microsoft 365 tenant and is protected using Microsoft Entra ID authentication.

Access is controlled through:

- Microsoft Entra ID authentication
- Microsoft Copilot Studio environment permissions
- Microsoft 365 connector authentication
- Organization-level security policies

Only authorized users with appropriate permissions can access or execute the agent.

---

# 📥 Trigger Configuration

The published agent automatically starts processing when an Outlook email satisfies the configured trigger conditions.

**Trigger Type**

- Outlook – **When a new email arrives (V3)**

**Trigger Condition**

```text
Subject contains:
[P2-003 LEAD]
```

Emails that do not satisfy the trigger conditions are ignored automatically.

---

# ⚙️ Deployment Configuration

| Component | Status |
|-----------|--------|
| 🤖 Agent | 🟢 Published |
| 📥 Outlook Trigger | 🟢 Configured |
| 📊 Excel Online (Business) | 🟢 Connected |
| 📄 Word Online (Business) | 🟢 Connected |
| 📧 Outlook Connector | 🟢 Connected |
| 🧠 Generative AI Orchestration | 🟢 Enabled |

---

# 🧪 Deployment Verification

The published agent has been validated using both interactive testing and real Outlook-triggered execution.

The following capabilities were successfully verified:

- ✔️ Outlook email trigger execution
- ✔️ Lead information extraction
- ✔️ AI-driven orchestration
- ✔️ Operational Excel table lookup
- ✔️ New lead creation
- ✔️ Existing lead update
- ✔️ Qualification report generation
- ✔️ Customer acknowledgement email
- ✔️ Duplicate lead detection
- ✔️ End-to-end autonomous processing

---

# 📌 Notes

- The shared URL is the Microsoft Copilot Studio authoring link for the published agent.
- Runtime access depends on Microsoft Entra ID authentication and organizational permissions.
- All Microsoft 365 connectors used by the solution were authenticated and validated during implementation.
- No credentials, API keys, or confidential tenant information are included in this submission.

---

# 🎯 Submission Status

**Project:** P2-003 – Autonomous Sales Lead Qualification Agent

**Implementation:** 🟢 Complete

**Publishing:** 🚀 Successful

**End-to-End Testing:** ✔️ Completed

**Documentation:** 🟢 In Progress