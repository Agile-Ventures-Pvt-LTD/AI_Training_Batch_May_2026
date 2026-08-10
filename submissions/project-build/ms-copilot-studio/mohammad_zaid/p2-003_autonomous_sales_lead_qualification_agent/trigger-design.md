
# Trigger Design

# Project Information

| Property     | Value                                              |
| ------------ | -------------------------------------------------- |
| Project      | P2-003 – NovaWorks Sales Lead Qualification Agent |
| Platform     | Microsoft Copilot Studio                           |
| Trigger Type | Event Trigger                                      |
| Connector    | Office 365 Outlook                                 |
| Event        | When a new email arrives (V3)                      |

---

# Purpose

The Outlook event trigger serves as the entry point for the autonomous workflow. Its purpose is to automatically initiate the Sales Lead Qualification process whenever a new qualifying email is received in the configured Outlook mailbox.

The trigger removes the need for manual intervention by allowing the agent to continuously monitor incoming lead enquiries and begin processing immediately after the trigger conditions are satisfied.

---

# Trigger Configuration

The trigger is configured using the **Office 365 Outlook** connector.

| Configuration Item  | Value                            |
| ------------------- | -------------------------------- |
| Connector           | Office 365 Outlook               |
| Event               | When a new email arrives (V3)    |
| Mailbox             | Configured Microsoft 365 mailbox |
| Folder              | Inbox                            |
| Trigger Mode        | Automatic                        |
| Include Attachments | Enabled                          |
| Authentication      | Microsoft 365 Connection         |

---

# Trigger Conditions

The trigger executes only when a new email satisfies the configured conditions.

Current configuration includes:

- Monitoring the Inbox folder.
- Processing newly received emails.
- Including email attachments for downstream processing.
- Running automatically without user interaction.

Where configured for testing, the trigger may use a subject filter (for example, project-specific test prefixes) to ensure that only intended test emails activate the workflow.

---

# Trigger Inputs

The trigger makes the following information available to the agent.

## Email Metadata

- Message ID
- Subject
- Sender Name
- Sender Email Address
- Date and Time Received

## Email Content

- Email Body
- HTML Body (where available)

## Attachments

- Attachment Name
- Attachment Content
- Attachment Metadata

These inputs provide the information required for downstream extraction and qualification.

---

# Trigger Workflow

The following sequence describes the trigger execution process.

```
New Email Arrives
        │
        ▼
Outlook Event Trigger
        │
        ▼
Collect Email Metadata
        │
        ▼
Collect Email Body
        │
        ▼
Collect Attachments
        │
        ▼
Pass Context to Generative Orchestration
        │
        ▼
Begin Lead Qualification Workflow
```

---

# Integration with Generative Orchestration

The trigger does not directly invoke individual tools.

Instead, once activated, it passes the email context to the Copilot Studio Generative Orchestration engine.

Based on the configured instructions and available tools, the orchestration engine determines:

- Which tool should be called.
- The order of execution.
- The required tool inputs.
- Subsequent business decisions.

This design reduces manual workflow configuration while allowing the agent to adapt its execution path according to the content of each incoming email.

---

# Expected Processing Sequence

After trigger activation, the expected workflow is:

1. Read operational reference data.
2. Extract lead information.
3. Validate mandatory information.
4. Detect duplicate leads.
5. Apply qualification rules.
6. Assign the appropriate sales owner.
7. Generate the Lead Qualification Report.
8. Create or update the operational workbook.
9. Send the appropriate communication.

---

# Test Evidence

The trigger was validated using the synthetic lead emails supplied with the project dataset.

Testing verified:

- Trigger activation upon receipt of qualifying emails.
- Successful handoff to Generative Orchestration.
- Invocation of configured tools.
- Operational record creation/update.
- Report generation.
- Communication workflow execution.

Detailed execution results are documented separately in **test-report.md**.

---

# Error Handling

The trigger relies on Microsoft Copilot Studio and the Office 365 Outlook connector.

If the trigger cannot execute successfully, processing may fail due to:

- Expired connector authentication.
- Mailbox permission issues.
- Microsoft 365 service availability.
- Missing or inaccessible downstream resources.

Operational errors are surfaced through the Copilot Studio Activity history for troubleshooting.

---

# Design Considerations

The trigger design follows these principles:

- Event-driven execution.
- Automatic processing.
- Minimal manual intervention.
- Secure Microsoft 365 authentication.
- Separation of trigger logic from business logic.
- Compatibility with Generative Orchestration.

---

# Known Limitations

The trigger is subject to platform and tenant limitations, including:

- Dependency on Microsoft 365 Outlook availability.
- Connector authentication requirements.
- Organization-specific mailbox permissions.
- Possible execution delays caused by Microsoft cloud services.
- Runtime behavior controlled by the Copilot Studio orchestration engine.

These limitations do not alter the business logic but may affect execution timing or availability.

---

# Conclusion

The Outlook event trigger provides an automated, event-driven entry point for the NovaWorks Sales Lead Qualification Agent.

By integrating directly with Microsoft 365 Outlook and Generative Orchestration, the trigger enables autonomous processing of incoming sales enquiries while maintaining a clear separation between event detection, business logic, and tool execution.
