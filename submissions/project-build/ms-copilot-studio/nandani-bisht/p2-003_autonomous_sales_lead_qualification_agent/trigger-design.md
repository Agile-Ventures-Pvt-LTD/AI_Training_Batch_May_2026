# Trigger Design

## Project Information

| Field | Details |
|-------|---------|
| Project ID | P2-003 |
| Project Name | Autonomous Sales Lead Qualification Agent |
| Platform | Microsoft Copilot Studio |
| Participant | Nandani Bisht |

---

# Trigger Overview

The Autonomous Sales Lead Qualification Agent is configured with an Outlook event trigger that automatically starts the workflow whenever a qualifying email is received.

The trigger eliminates manual intervention by continuously monitoring the configured Outlook mailbox and initiating the lead qualification process only for relevant sales inquiries.

---

# Trigger Configuration

| Property | Value |
|----------|-------|
| Trigger Type | Outlook – When a new email arrives (V3) |
| Event | New Email Received |
| Execution | Automatic |
| Processing Mode | Event Driven |
| Trigger Status | Enabled |

---

# Subject Filter

Only emails containing the following subject prefix are processed:

```
[P2-003 LEAD]
```

Examples of valid subjects:

- `[P2-003 LEAD] CRM Inquiry`
- `[P2-003 LEAD] ERP Implementation`
- `[P2-003 LEAD] Product Demo Request`

Emails that do not contain the required subject filter are ignored by the agent.

---

# Trigger Inputs

The trigger receives the following information from Outlook:

- Subject
- Sender Email Address
- Sender Name
- Email Body
- Message ID
- Date and Time Received
- Attachments (if present)

These inputs are used by the agent to extract lead information and perform downstream processing.

---

# Trigger Workflow

```
New Outlook Email
        │
        ▼
Subject Filter Validation
        │
        ▼
Matching Email
        │
        ▼
Generative Orchestration Starts
        │
        ▼
Lead Qualification Process
```

---

# Trigger Validation

The trigger was validated using multiple synthetic test emails provided as part of the project.

Validation confirmed:

- Automatic execution after email arrival.
- Correct application of the subject filter.
- Successful invocation of Generative Orchestration.
- End-to-end processing without manual intervention.

---

# Test Evidence

The following scenarios were successfully tested:

- Valid lead email
- Duplicate lead email
- Missing information
- Human review case
- Support request
- Competitor inquiry
- Unknown product
- Low-priority lead
- Qualified lead
- Hot lead

Activity History in Microsoft Copilot Studio confirmed successful execution for all supported scenarios.

---

# Error Handling

The trigger does not start processing if:

- The email subject does not match the required filter.
- The email cannot be accessed because of Outlook connector issues.
- Required Microsoft 365 connections are unavailable.

In such cases, no downstream actions are executed.

---

# Limitations

The trigger depends on:

- Microsoft Outlook availability.
- Active Microsoft 365 connector authentication.
- Network connectivity.
- Correct mailbox configuration.
- Subject line matching the required format.

Emails outside the configured scope are intentionally ignored to prevent unintended processing.

---

# Design Considerations

The trigger was designed to ensure:

- Event-driven execution.
- Minimal manual intervention.
- Controlled processing scope.
- Reliable automation.
- Reduced unnecessary executions.
- Improved operational efficiency.

---

# Summary

The Outlook event trigger provides the entry point for the Autonomous Sales Lead Qualification Agent. By combining automatic email detection with subject-based filtering, the solution ensures that only relevant sales inquiries initiate the qualification workflow, enabling efficient, reliable, and controlled automation.