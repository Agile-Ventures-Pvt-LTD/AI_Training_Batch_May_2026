# Trigger Design

## Overview

The Autonomous Sales Lead Qualification Agent is initiated through an Office 365 Outlook trigger. The trigger continuously monitors a designated mailbox for new incoming emails that match the configured subject filter. Only emails intended for sales lead processing are passed to the agent for autonomous execution.

---

# Trigger Type

| Property | Value |
|----------|-------|
| Connector | Office 365 Outlook |
| Trigger | When a new email arrives (V3) |
| Trigger Mode | Event-based |
| Folder | Inbox |
| Execution | Automatic |

---

# Trigger Purpose

The trigger acts as the entry point for the autonomous workflow.

Its responsibilities include:

- Detecting newly received emails.
- Filtering valid lead enquiries.
- Preventing unrelated emails from initiating processing.
- Passing the email content to the agent for analysis.

---

# Subject Filter

The trigger processes only emails whose subject contains the predefined project identifier.

**Configured Subject Filter**

```
[P2-003 LEAD]
```

### Example Accepted Subjects

```
[P2-003 LEAD] Enterprise multi-agent platform for Orbital Finance

[P2-003 LEAD] Lead automation for Acme Logistics

[P2-003 LEAD] AI Governance Accelerator
```

### Example Rejected Subjects

```
Meeting Invitation

Holiday Request

Invoice Payment

Technical Support Ticket

Product Feedback
```

---

# Trigger Inputs

When activated, the trigger provides the following email metadata to the agent.

| Input | Description |
|--------|-------------|
| Subject | Email subject |
| Body | Email content |
| Sender Name | Customer name |
| Sender Email | Customer email address |
| Received Time | Timestamp |
| Message ID | Unique email identifier |
| Conversation ID | Email thread identifier |
| Attachments | Attachment metadata (if present) |

---

# Data Extraction

The agent extracts business information from the email body, including:

- Customer Name
- Company Name
- Job Title
- Country
- Product Interest
- Budget
- Purchase Timeline
- Decision Role
- Business Requirement

These values are passed to downstream qualification tools.

---

# Trigger Validation

Before processing begins, the agent validates:

- Email successfully received.
- Subject matches the required filter.
- Email body is not empty.
- Required customer details can be extracted.
- Outlook connection is available.

If validation fails, processing is stopped.

---

# Trigger Behaviour

### Valid Lead Email

If the subject matches the configured filter:

- Trigger executes.
- Agent starts.
- Qualification workflow begins.

---

### Invalid Subject

If the subject does not match:

- Agent does not start.
- Email remains in the mailbox.
- No tools are executed.

---

### Empty Email

If the email body contains insufficient information:

- Agent starts.
- Mandatory field validation fails.
- Customer receives a request for additional information.
- Qualification scoring is skipped.

---

# Error Handling

If Outlook is unavailable or the trigger cannot retrieve the email:

- Workflow terminates safely.
- No lead record is created.
- No qualification report is generated.
- No customer communication is sent.

The failure is recorded in the execution logs.

---

# Security Considerations

The trigger only reads emails from the configured Outlook mailbox.

It does not:

- Delete emails.
- Modify email content.
- Forward emails automatically.
- Access mailboxes outside the configured connection.

Authentication is managed through Microsoft 365.

---

# Testing Approach

The trigger is validated using representative business enquiries sent to the monitored Outlook mailbox.

Each test email:

- Uses the required subject format.
- Contains realistic lead information.
- Verifies successful trigger activation.
- Confirms downstream tool execution.

Testing includes:

- Valid enquiries
- Duplicate enquiries
- Missing information
- Existing customer follow-ups
- Invalid subject lines

---

# Test Evidence

The following evidence should be collected during testing:

- Outlook email received.
- Trigger activation in Copilot Studio.
- Successful workflow execution.
- Tool execution history.
- Generated qualification report.
- Lead register update.
- Customer acknowledgement email.
- Internal notification email.

---

# Current Status

| Component | Status |
|----------|--------|
| Outlook Trigger Configured | Completed |
| Subject Filter Applied | Completed |
| Inbox Monitoring Enabled | Completed |
| Microsoft Connection Valid | Configured |
| Trigger Testing | Pending |
| Production Validation | Pending |

---

# Known Limitations

- The trigger only monitors the configured Outlook mailbox.
- Processing depends on Microsoft 365 connector availability.
- Emails without the required subject filter are ignored.
- Attachments are not used during qualification unless future enhancements are implemented.
- Processing begins only after the email is successfully delivered to the monitored Inbox.

---

# Summary

The Outlook trigger provides a reliable event-driven entry point for the Autonomous Sales Lead Qualification Agent. By filtering incoming emails based on a predefined subject pattern, the trigger ensures that only relevant sales enquiries initiate the qualification workflow, reducing unnecessary processing while maintaining consistent and secure automation.