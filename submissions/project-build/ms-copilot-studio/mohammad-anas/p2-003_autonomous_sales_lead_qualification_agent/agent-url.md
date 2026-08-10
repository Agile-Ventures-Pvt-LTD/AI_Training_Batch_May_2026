# Published Agent URL

## Project Information

| Item | Value |
|------|-------|
| Project ID | P2-003 |
| Project Name | Autonomous Sales Lead Qualification Agent |
| Platform | Microsoft Copilot Studio |
| Participant | Mohammad Anas |

---

# Agent Details

| Property | Value |
|----------|-------|
| Agent Name | Anas_NovaWorks Sales Lead Qualification Agent |
| Environment | Agile Consulting Pvt. Ltd. |
| Status | Published *(Update after successful publication)* |
| Version | 1.0 |

---

# Published URL

**Agent URL**

```
https://copilotstudio.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/50584f25-a38c-f111-8077-000d3af21e08/overview
```

---

# Authentication

Current Authentication Method

```
Microsoft Entra ID (Organizational Account)
```

The agent is accessible only to authenticated users who have permission within the Microsoft 365 tenant.

---

# Access Limitations

The published agent is subject to the following restrictions:

- Microsoft 365 authentication is required.
- Users must belong to the authorized tenant.
- Connector permissions must be granted for Outlook, Excel Online (Business), and Word Online (Business).
- Access depends on organizational security policies and Copilot Studio environment permissions.

---

# Publishing Verification

| Check | Status |
|-------|--------|
| Agent Published | Completed *(Update after publishing)* |
| URL Verified | Verified |
| Authentication Verified | Verified |
| Outlook Trigger Enabled | Verified |
| Generative Orchestration Enabled | Verified |
| Connector Configuration Verified | Verified |

---

# Environment Configuration

| Component | Status |
|-----------|--------|
| Microsoft Copilot Studio | Configured |
| Office 365 Outlook Connector | Configured |
| Excel Online (Business) Connector | Configured |
| Word Online (Business) Connector | Configured |

---

# Deployment Notes

The agent is configured as an autonomous event-driven solution.

Execution begins automatically when an Outlook email matching the required subject filter is received.

The trigger processes only emails whose subject contains:

```
[P2-003 LEAD]
```

This prevents unrelated mailbox messages from being processed.

---

# Verification Procedure

After publication, verify the following:

1. The published URL opens successfully.
2. Authentication completes without errors.
3. The Outlook event trigger activates for valid project emails.
4. The agent processes the lead according to business rules.
5. Excel records are created or updated successfully.
6. Word reports are generated for eligible classifications.
7. Outlook communications are sent according to policy.
8. Activity history records a successful execution.

---

# Known Access Constraints

The published agent may not function correctly if:

- Outlook connector authentication expires.
- Excel workbook permissions are removed.
- Word Online connector becomes unavailable.
- Required Microsoft 365 licenses are missing.
- The agent is unpublished or disabled.
- Organizational policies block connector execution.

---

# Notes

This document intentionally excludes authentication secrets, access tokens, tenant identifiers, or confidential configuration values.

All sensitive information must remain protected and must not be committed to GitHub.
