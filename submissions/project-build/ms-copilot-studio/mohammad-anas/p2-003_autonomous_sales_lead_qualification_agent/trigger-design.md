# Trigger Design

## Project Information

| Item | Details |
|------|---------|
| Project ID | P2-003 |
| Project Name | Autonomous Sales Lead Qualification Agent |
| Platform | Microsoft Copilot Studio |
| Participant | Mohammad Anas |

---

# Purpose

This document describes the trigger architecture used by the Autonomous Sales Lead Qualification Agent.

The solution uses an event-driven trigger that automatically starts the qualification workflow whenever a new sales enquiry is received in the monitored Outlook mailbox.

The trigger eliminates manual intervention and ensures timely processing of incoming opportunities.

---

# Trigger Type

| Property | Value |
|----------|-------|
| Trigger Model | Event-Driven |
| Platform | Microsoft Copilot Studio |
| Connector | Office 365 Outlook |
| Trigger Action | When a new email arrives (V3) |
| Execution Mode | Automatic |

---

# Trigger Workflow

```
New Outlook Email
        │
        ▼
When a New Email Arrives (V3)
        │
        ▼
Read Email Metadata
        │
        ▼
Validate Subject
        │
        ▼
Validate Email Scope
        │
 ┌──────┴─────────┐
 │                │
 ▼                ▼
Ignore        Continue Processing
                     │
                     ▼
           Execute Qualification Workflow
```

---

# Trigger Conditions

The workflow starts automatically when a new email is received.

The trigger captures the email and makes its properties available to the agent, including:

- Message ID
- Conversation ID
- Subject
- Sender
- Recipient
- Received Time
- Email Body
- Importance
- Attachments (if present)

These values are used throughout the qualification workflow.

---

# Subject Validation

The first validation step ensures that the email belongs to the lead qualification process.

Expected subject pattern:

```
[P2-003 LEAD]
```

Example:

```
[P2-003 LEAD] Contoso Ltd - CRM Solution Request
```

Emails that do not match the expected pattern are ignored and no further processing is performed.

---

# Scope Validation

After subject validation, the agent determines whether the email represents a genuine sales enquiry.

Examples of emails that continue through the workflow:

- Product enquiries
- Solution requests
- Pricing discussions
- Partnership opportunities
- Demo requests
- Enterprise implementation enquiries

Examples of emails that are excluded:

- Technical support requests
- Recruitment enquiries
- Vendor communications
- Internal emails
- Spam
- Marketing newsletters
- Academic requests
- Competitor research

Excluded emails are classified as **Not a Sales Lead** and the workflow ends.

---

# Trigger Data

The trigger provides the following information to downstream workflow steps.

| Data | Purpose |
|------|---------|
| Message ID | Duplicate detection |
| Subject | Scope validation |
| Sender Email | Customer identification |
| Sender Name | Contact information |
| Email Body | AI information extraction |
| Received Time | Processing audit |
| Conversation ID | Email threading |
| Attachments | Supporting business documents |

---

# Duplicate Protection

Before creating a new lead, the workflow checks existing records using trigger information.

Duplicate comparison includes:

- Message ID
- Sender Email
- Company Name
- Product Interest

If a duplicate is detected:

- Existing lead record is updated.
- Duplicate acknowledgement is prevented.
- Duplicate report generation is skipped.
- Processing status is recorded as **Duplicate**.

---

# Trigger Reliability

The trigger is designed to process each qualifying email independently.

Characteristics include:

- Automatic activation
- Event-driven execution
- Independent processing
- Stateless execution
- Retry support through Microsoft 365 connector capabilities

---

# Error Handling

If the trigger cannot retrieve the email successfully, processing stops and no downstream actions are executed.

If downstream connector actions fail after the trigger succeeds:

1. Processing status is recorded.
2. Completed actions are preserved.
3. Human review is requested when necessary.
4. Failed actions are not marked as successful.

---

# Security Considerations

The trigger does not expose:

- Authentication credentials
- Microsoft tenant information
- Connector secrets
- Internal configuration values

Processing occurs only after successful authentication through Microsoft 365.

---

# Design Decisions

The following design decisions were adopted:

| Decision | Reason |
|----------|--------|
| Event-driven execution | Eliminates manual initiation |
| Outlook trigger | Native integration with Microsoft 365 |
| Subject validation | Prevents accidental processing of unrelated emails |
| Early scope validation | Reduces unnecessary connector usage |
| Metadata preservation | Supports auditing and duplicate detection |
| Independent processing | Prevents one email from affecting another |

---

# Benefits

The trigger design provides:

- Fully autonomous execution
- Reduced manual effort
- Faster response time
- Consistent workflow initiation
- Reliable duplicate detection
- Improved operational efficiency
- Better auditability
- Scalable event processing

---

# Summary

The Autonomous Sales Lead Qualification Agent uses an event-driven Outlook trigger to automatically initiate lead processing whenever a qualifying sales enquiry is received.

By validating the email scope before invoking downstream business logic, the trigger ensures that only relevant opportunities enter the qualification workflow, improving efficiency, consistency, and governance while minimizing unnecessary processing.