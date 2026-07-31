# Agent URL

## P2-003 Autonomous Sales Lead Qualification Agent
## Published URL

The autonomous Copilot Studio agent has been successfully published.

[**Published URL**](https://teams.microsoft.com/l/app/?titleId=T_9ced1082-8fd0-f917-570b-b9ffae694fd5)

The agent is accessible to authenticated Microsoft 365 users with the appropriate permissions.

---

## Authentication requirement

The published agent requires Microsoft organizational authentication before access is granted.

| Setting                          | Configuration |
| -------------------------------- | ------------- |
| Sign-in required                 | Yes           |
| Microsoft organizational account | Required      |
| External public access           | Disabled      |

---

## Access scope

The published agent has access only to the configured Microsoft 365 resources.

### Connected services

* Office 365 Outlook
* Excel Online (Business)
* Word Online (Business)
* OneDrive (Business)

### Accessible resources

* P2-003 Outlook mailbox
* Operational Excel workbook
* Generated Word qualification reports
* Configured Microsoft 365 document library

---

## Trigger verification

The autonomous event trigger has been configured and validated.

| Trigger configuration         | Status   |
| ----------------------------- | -------- |
| When a new email arrives (V3) | Verified |
| Subject filter: [P2-003 LEAD] | Verified |
| Trigger folder configured     | Verified |
| Autonomous execution          | Verified |

The agent processes only emails whose subject contains:

```text
[P2-003 LEAD]
```

This prevents unrelated mailbox traffic from being processed.

---

## Tool connection verification

The published agent has verified connector access to the required Microsoft 365 tools.

### Outlook

| Tool                             | Status   |
| -------------------------------- | -------- |
| Send acknowledgement             | Verified |
| Send missing-information request | Verified |
| Send owner notification          | Verified |
| Send Sales Operations alert      | Verified |

### Excel Online (Business)

| Tool                     | Status   |
| ------------------------ | -------- |
| Read lead register       | Verified |
| Read qualification rules | Verified |
| Read territory owners    | Verified |
| Add lead record          | Verified |
| Update lead record       | Verified |

### Word Online (Business)

| Tool                        | Status   |
| --------------------------- | -------- |
| Create qualification report | Verified |
| Dynamic report filename     | Verified |
| Report storage location     | Verified |

---

## Access limitations

The published agent is restricted to the P2-003 autonomous sales qualification scenario.

The agent does not:

* process real customer production data
* approve pricing
* approve discounts
* generate contracts
* guarantee delivery dates
* bypass human-review requirements
* modify qualification policies

---

## Verification results

The published deployment has been verified against the PRD acceptance requirements.

| Verification test                  | Result |
| ---------------------------------- | ------ |
| Agent URL accessible               | Passed |
| Authentication successful          | Passed |
| Trigger executed autonomously      | Passed |
| Excel reference tables accessible  | Passed |
| Duplicate detection executed       | Passed |
| Lead record creation verified      | Passed |
| Word report generation verified    | Passed |
| Outlook communication verified     | Passed |
| Human-review routing verified      | Passed |
| Autonomous run monitoring verified | Passed |

---

## Publication evidence

The following evidence has been captured for submission:

* Agent overview
* Published status
* Trigger configuration
* Tool configuration
* Excel table connection
* Word connector configuration
* Outlook connector configuration
* Successful autonomous run
* Duplicate prevention evidence
* Generated Word qualification report
* Published agent confirmation

---

## Security and privacy

This deployment uses Microsoft 365 authentication and connector permissions.

No API keys, secrets, access tokens, or production customer data are included in this repository.

All testing was performed using synthetic project data in accordance with the P2-003 PRD.

---

## Final deployment status

The NovaWorks Autonomous Sales Lead Qualification Agent has been successfully published in Microsoft Copilot Studio and is available through the published Copilot Studio URL for authenticated Microsoft 365 users.

This document satisfies the P2-003 requirement for documenting the published agent URL, authentication configuration, access limitations, and deployment verification evidence.
