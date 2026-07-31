
# Trigger Design

## Agent Name
**NovaWorks Sales Lead Qualification Agent s**

---

## Trigger Overview

The agent uses an autonomous Outlook event trigger in Microsoft Copilot Studio.

**Trigger:**
```

When a new email arrives (V3)

```

The trigger automatically starts lead qualification when a new sales email is received.

---

## Trigger Configuration

| Field | Details |
|---|---|
| Connector | Office 365 Outlook |
| Trigger Type | Event Trigger |
| Execution | Autonomous |
| Source | Outlook Mailbox |
| Data | Synthetic Sales Emails |

---

## Trigger Filter

Only emails containing:

```

[P2-003 LEAD]

```

in the subject are processed.

Other emails are ignored.

---

## Trigger Inputs

The agent receives:

- Message ID
- Sender Name
- Sender Email
- Subject
- Email Body
- Received Date
- Attachment Metadata

---

## Trigger Flow

```

New Email Received
|
v
Subject Validation
|
v
[P2-003 LEAD] Present?
/        
Yes         No
|            |
Process      Ignore
Lead

```

---

## Testing Evidence

Validated scenarios:

| Test | Result |
|---|---|
| Valid lead email | Trigger executed |
| Invalid subject | Ignored |
| Duplicate email | Duplicate handling executed |

---

## Limitations

- Depends on Outlook connector availability.
- Requires Microsoft 365 permissions.
- Attachment content processing is not implemented.
- Emails without `[P2-003 LEAD]` are not processed.

---

## Status

| Requirement | Status |
|---|---|
| Outlook Trigger | Completed |
| Subject Filter | Completed |
| Autonomous Execution | Completed |
| Testing | Completed |
```


