# Trigger Design

## Project Information

| Field                | Details              |
| -------------------- | -------------------- |
| **Project ID**       | P2-003           |
| **Participant Name** | Pranay Gupta|
| **Agent Name**       | Pranay NovaWorks Sales Lead Agent       |

---

# Overview

The agent uses an **Office 365 Outlook event trigger** to automatically start the lead qualification process whenever a new sales inquiry email is received.

This event-driven approach eliminates manual monitoring of the mailbox and ensures timely processing of incoming leads.

---

# Trigger Configuration

| Setting        | Value                         |
| -------------- | ----------------------------- |
| Trigger        | When a new email arrives (V3) |
| Service        | Office 365 Outlook            |
| Folder         | Inbox                         |
| Subject Filter | [P2-003 LEAD]               |
| Execution      | Automatic                     |

---

# Trigger Logic

The trigger follows this simple workflow:

```text
New Email Received
        │
        ▼
Check Subject Filter
        │
        ├── No → Ignore Email
        │
        └── Yes
               │
               ▼
Start Agent Processing
```

---

# Trigger Data

The trigger passes the following information to the agent:

* Message ID
* Sender Name
* Sender Email
* Email Subject
* Email Body
* Received Date & Time

These fields are used for lead validation, duplicate detection, and business information extraction.

---

# Validation Rules

Before processing begins, the agent verifies that:

* The email matches the required subject filter.
* The email represents a potential sales inquiry.
* The required trigger data is available.

Emails that do not meet these conditions are ignored.

---

# Benefits

* Automatic lead processing
* Reduced manual effort
* Faster response time
* Consistent event-driven execution
* Supports scalable lead management

---

# Future Enhancements

Potential improvements include:

* Monitoring multiple mailboxes
* Processing email attachments
* Supporting additional trigger conditions
* Priority-based email routing

---

# Conclusion

The Outlook event trigger provides a reliable entry point for the autonomous lead qualification process. It ensures that only relevant project emails initiate the workflow, improving efficiency while preventing unnecessary processing.
