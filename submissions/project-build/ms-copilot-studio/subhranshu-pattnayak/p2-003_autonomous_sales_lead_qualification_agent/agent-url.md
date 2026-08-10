# Published Agent Information

## Purpose

This document provides the deployment information for the published Autonomous Sales Lead Qualification Agent, including its published URL, authentication method, access limitations, and verification details.

---

# Published Agent URL

**Published Agent URL**

```
https://copilotstudio.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/cca5bab1-a58c-f111-8077-000d3af21e08/overview
```

---

# Deployment Status

| Item | Status |
|------|--------|
| Agent Published | ✅ Yes |
| Environment | Production |
| Accessibility | Verified |
| Verification Status | Successful |

> **Screenshot – Published Agent**

![Published Agent](<Screenshot 2026-07-31 162121.png>)

---

# Authentication

The published agent uses Microsoft Entra ID (Microsoft 365 Organizational Account) authentication.

Only authenticated users with the required tenant permissions can access the agent.

| Setting | Value |
|---------|-------|
| Authentication Type | Microsoft Entra ID |
| Anonymous Access | Disabled |
| User Sign-in Required | Yes |
| Organization Restricted | Yes |

---

# Verification

The published agent was verified after deployment by executing a complete end-to-end autonomous workflow.

Verification included:

- Agent accessibility
- Outlook trigger execution
- AI instruction execution
- Excel Lead Register update
- Word report generation
- Outlook communication
- Successful completion of the autonomous workflow

---

# Verification Date

**31 July 2026**