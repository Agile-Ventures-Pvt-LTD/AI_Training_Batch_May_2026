# Agent URL

## Agent Information

| Property          | Value                                                                                                                                                                                                                                                                                                                                                              |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Project           | P2-003 – NovaWorks Sales Lead Qualification Agent                                                                                                                                                                                                                                                                                                                 |
| Platform          | Microsoft Copilot Studio                                                                                                                                                                                                                                                                                                                                           |
| Agent Type        | Autonomous AI Agent                                                                                                                                                                                                                                                                                                                                                |
| Deployment Status | Published                                                                                                                                                                                                                                                                                                                                                          |
| Environment       | Microsoft Copilot Studio                                                                                                                                                                                                                                                                                                                                           |
| Published URL     | **[copilotstudio.preview.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/bd2ba825-ac8c-f111-8077-000d3af21e08/overview](https://copilotstudio.preview.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/bd2ba825-ac8c-f111-8077-000d3af21e08/overview)<PASTE YOUR PUBLISHED AGENT URL HERE></paste>** |

---

# Authentication

The published agent is protected using Microsoft authentication provided by the configured Microsoft 365 tenant.

Authentication method:

- Microsoft Entra ID (Azure Active Directory)
- Organization account required
- User permissions controlled by the Microsoft 365 tenant

No anonymous access is enabled.

---

# Access Limitations

The following limitations apply to the published agent.

## Tenant Restrictions

- Accessible only from the configured Microsoft 365 tenant.
- Users outside the tenant cannot access the agent unless explicitly granted permission.

## Connector Restrictions

The agent requires authenticated access to:

- Office 365 Outlook
- Excel Online (Business)
- Word Online (Business)
- OneDrive for Business

If any connector connection expires or is removed, the affected functionality will not execute successfully.

## Data Restrictions

The agent processes only synthetic project data supplied as part of Project P2-003.

No production customer information is used.

---

# Verification

The published agent was verified using the following checks:

- Agent successfully published.
- Agent accessible through the published URL.
- Outlook trigger configured.
- Excel tools available.
- Word report generation configured.
- Outlook communication tool configured.
- Generative orchestration enabled.

---

Published Version

| Property     | Value     |
| ------------ | --------- |
| Version      | 1.0       |
| Status       | Published |
| Verification | Completed |

---

# Notes

- The published URL is environment-specific and therefore is intentionally not included in this document.
- Authentication and permissions are managed by the Microsoft 365 tenant administrator.
- No credentials, secrets, access tokens, or confidential information are stored within the documentation.

---

# Submission Checklist

- [X] Agent published successfully
- [X] Published URL copied into this document
- [X] Authentication verified
- [X] Outlook trigger verified
- [X] Excel connectivity verified
- [X] Word report generation verified
- [X] Email communication verified
