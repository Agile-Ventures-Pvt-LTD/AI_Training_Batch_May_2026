# Trigger Design

## Document Information

| Item | Details |
|------|---------|
| **Project Name** | NovaWorks Autonomous Sales Lead Qualification Agent |
| **Project ID** | P2-003 |
| **Platform** | Microsoft Copilot Studio |
| **Trigger Type** | Microsoft Outlook – When a new email arrives (V3) |
| **Document Version** | 1.0 |
| **Prepared By** | Ashish Sinha |
| **Last Updated** | 31 July 2026 |

---

# 1. Purpose

This document describes the trigger configuration used by the **NovaWorks Autonomous Sales Lead Qualification Agent**.

The trigger is responsible for automatically initiating the lead qualification workflow whenever a qualifying sales enquiry email is received in the configured Outlook mailbox.

The objective is to eliminate manual intervention while ensuring that only relevant sales enquiries are processed by the autonomous agent.

---

# 2. Trigger Overview

The solution uses the **Microsoft Outlook** connector available in Microsoft Copilot Studio.

The trigger continuously monitors the configured mailbox for new incoming emails.

When a new qualifying email arrives, the agent automatically starts the lead qualification workflow.

No manual execution is required.

---

# 3. Trigger Configuration

| Property | Configuration |
|-----------|---------------|
| Trigger Name | New Sales Inquiry Email |
| Connector | Office 365 Outlook |
| Trigger Type | When a new email arrives (V3) |
| Execution Mode | Automatic |
| Event Source | Outlook Mailbox |
| Authentication | Microsoft Entra ID |
| Environment | Microsoft 365 |

---

# 4. Trigger Event

The trigger listens for the following event:

```
New Email Received
```

The event is generated whenever an email is delivered to the configured Outlook mailbox.

The trigger immediately passes the email metadata and content to the Copilot Studio agent for processing.

---

# 5. Trigger Inputs

The trigger provides the following information to the agent.

| Input | Description |
|--------|-------------|
| Message ID | Unique identifier for the email |
| Subject | Email subject |
| Sender Name | Customer name (if available) |
| Sender Email | Customer email address |
| Email Body | Complete email content |
| Received Date | Timestamp of receipt |
| Attachments | Email attachments (if present) |

These inputs become the initial context used by the autonomous agent.

---

# 6. Trigger Filters

To avoid processing unrelated emails, the trigger applies filtering criteria before executing the workflow.

Typical filtering includes:

- Inbox folder only
- New email events
- Sales enquiry subject pattern (if configured)
- Ignore draft messages
- Ignore sent items

Example subject filter:

```
[P2-003 LEAD]
```

If no subject filter is configured, all incoming emails are evaluated by the agent.

---

# 7. Trigger Execution Flow

```text
New Email Received
          │
          ▼
Trigger Activated
          │
          ▼
Read Email Metadata
          │
          ▼
Extract Email Body
          │
          ▼
Pass Data to Copilot Agent
          │
          ▼
Begin Lead Qualification Workflow
```

The trigger only initiates the workflow. Business decisions are performed by the agent after execution begins.

---

# 8. Trigger Processing Logic

Once activated, the trigger performs the following operations:

1. Detect a new email in the configured mailbox.
2. Retrieve email metadata.
3. Retrieve email body.
4. Retrieve attachment information (if available).
5. Pass all available data to the autonomous agent.
6. Start the qualification workflow.

No business validation occurs within the trigger itself.

---

# 9. Trigger Responsibilities

The trigger is responsible for:

- Monitoring the Outlook mailbox.
- Detecting new incoming emails.
- Retrieving email information.
- Starting the autonomous workflow.
- Passing email data to the agent.

The trigger does **not** perform:

- Qualification scoring.
- Duplicate detection.
- Product validation.
- Territory assignment.
- Report generation.
- Email notifications.

These activities are handled by the agent after the trigger has executed.

---

# 10. Trigger Validation

The trigger configuration was validated using multiple sample sales enquiry emails.

Validation confirmed:

| Validation Item | Status |
|-----------------|--------|
| Trigger detects new email | ✅ Passed |
| Email body retrieved | ✅ Passed |
| Sender information available | ✅ Passed |
| Subject captured correctly | ✅ Passed |
| Agent execution started | ✅ Passed |

---

# 11. Test Evidence

The trigger was tested using sample enquiry emails representing different business scenarios.

Test scenarios included:

- New customer enquiry.
- Existing customer enquiry.
- Duplicate lead.
- Missing information.
- Unknown product enquiry.

For each scenario, the trigger successfully initiated the autonomous workflow.

---

# 12. Error Handling

The trigger supports graceful handling of common issues.

| Scenario | Expected Behaviour |
|----------|--------------------|
| Empty email body | Workflow continues with available metadata |
| Missing sender name | Use sender email for identification |
| Missing attachments | Continue processing |
| Outlook service unavailable | Trigger waits until service becomes available |
| Authentication expired | Trigger execution fails until connection is reauthenticated |

Errors related to business processing are handled by the autonomous agent rather than the trigger.

---

# 13. Trigger Limitations

The trigger has the following operational limitations:

- Only monitors the configured Outlook mailbox.
- Depends on a valid Microsoft 365 connection.
- Requires active connector authentication.
- Cannot process emails received before activation.
- Processing speed depends on Microsoft 365 service availability.
- Does not classify or validate email content.

---

# 14. Security Considerations

The trigger follows Microsoft security best practices.

- Authentication is managed using Microsoft Entra ID.
- No credentials are stored within the trigger configuration.
- Access is limited to authorized Microsoft 365 users.
- Email content is processed within the Microsoft 365 environment.
- No external services are required to activate the workflow.

---

# 16. Conclusion

The Outlook trigger provides the event-driven entry point for the NovaWorks Autonomous Sales Lead Qualification Agent. By automatically monitoring incoming sales enquiry emails and initiating the qualification workflow, it enables timely, consistent, and unattended processing while keeping business logic separated from event detection.

The trigger design follows Microsoft 365 best practices, supports secure authentication through Microsoft Entra ID, and provides a reliable foundation for the autonomous lead qualification process.