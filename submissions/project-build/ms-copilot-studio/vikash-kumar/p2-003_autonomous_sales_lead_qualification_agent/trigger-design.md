# 📥 Trigger Design

## 🚀 Project Information

| Property | Details |
|----------|---------|
| **Project ID** | P2-003 – Autonomous Sales Lead Qualification Agent |
| **Participant** | Vikash Kumar |
| **Platform** | Microsoft Copilot Studio |
| **Trigger Type** | Outlook – When a new email arrives (V3) |
| **Execution Mode** | Event-Driven Autonomous Processing |

---

# 🎯 Design Objective

The objective of the trigger is to enable the agent to begin processing automatically whenever a new sales enquiry is received.

Instead of requiring a user to manually invoke the agent, the Outlook trigger initiates the entire qualification workflow as soon as an eligible email reaches the configured mailbox.

This event-driven approach aligns with the project requirement of creating an autonomous sales lead qualification agent.

---

# 📨 Trigger Selection

The solution uses the Microsoft Outlook trigger:

**When a new email arrives (V3)**

This trigger continuously monitors the configured Outlook mailbox and automatically starts the agent whenever a matching email is received.

The trigger serves as the entry point for the complete lead qualification workflow.

---

# ⚙️ Trigger Configuration

The trigger was configured using the following settings.

| Setting | Configuration |
|----------|---------------|
| **Trigger Type** | When a new email arrives (V3) |
| **Mailbox** | Microsoft 365 Outlook |
| **Folder** | Inbox |
| **Include Attachments** | Yes |
| **Only With Attachments** | No |
| **From** | Not restricted |
| **Subject Filter** | `[P2-003 LEAD]` |

---

# 🎯 Subject Filter Strategy

To prevent accidental execution for unrelated emails, a subject filter was configured.

Only emails containing the following text are processed:

```text
[P2-003 LEAD]
```

Examples of valid subjects include:

- `[P2-003 LEAD] ERP Modernization`
- `[P2-003 LEAD] CRM Transformation`
- `[P2-003 LEAD] AI Automation Initiative`

Examples that will **not** trigger the agent:

- Meeting Request
- Support Ticket
- Job Application
- Vendor Proposal
- General Enquiry

This filtering mechanism significantly reduces unnecessary executions and ensures that only intended sales enquiries enter the workflow.

---

# 🔄 Trigger Workflow

After activation, the trigger automatically starts the AI orchestration process.

```text
New Outlook Email
        │
        ▼
Subject Validation
        │
        ▼
Generative AI Agent
        │
        ▼
Lead Qualification Workflow
```

No manual interaction is required after the trigger is activated.

---

# 🧠 Interaction with AI Orchestration

The trigger supplies the email context directly to the agent.

The incoming email becomes the primary input for AI reasoning.

The agent then determines:

- Whether the email is a valid sales lead.
- Which operational data is required.
- Which connector tools should be invoked.
- Whether the lead already exists.
- Whether the lead should be escalated.

The trigger itself performs no business logic; it simply initiates the autonomous processing sequence.

---

# 📋 Trigger Payload

The trigger provides the agent with the email context required for processing, including:

- Subject
- Email body
- Sender information
- Message ID
- Received timestamp
- Attachment information (when available)

These values are used during information extraction and operational processing.

---

# 🔒 Validation Rules

Before any operational actions are executed, the agent validates:

- The subject matches the configured filter.
- The email represents a genuine sales enquiry.
- The required business information is available.
- The request complies with the NovaWorks Lead Qualification Policy.

Emails that fail validation are ignored or classified as **Not a Sales Lead**, preventing unnecessary operational activity.

---

# ⚡ Event-Driven Processing

The implemented trigger enables a fully autonomous workflow.

Once activated, the agent proceeds through the following stages without manual intervention:

1. Receive Outlook email.
2. Validate trigger conditions.
3. Extract lead information.
4. Read operational reference tables.
5. Detect duplicate enquiries.
6. Calculate qualification.
7. Assign territory and sales owner.
8. Create or update the lead record.
9. Generate the qualification report.
10. Send the acknowledgement email.
11. Escalate when required.

---

# 🛡️ Reliability Considerations

The trigger configuration was designed to improve operational reliability by:

- Restricting execution using a subject filter.
- Monitoring only the Inbox folder.
- Accepting emails with or without attachments.
- Supporting a wide variety of genuine sales enquiries.
- Preventing execution for unrelated business emails.

These measures reduce false positives and improve the overall stability of the solution.

---

# 🧪 Validation

The trigger configuration was validated using multiple real Outlook email scenarios.

The following behaviors were successfully verified:

- ✔️ Trigger activated automatically for matching subjects.
- ✔️ Agent processed incoming email without manual interaction.
- ✔️ Lead information was extracted successfully.
- ✔️ Operational connector tools were invoked.
- ✔️ Lead records were created or updated.
- ✔️ Qualification reports were generated.
- ✔️ Acknowledgement emails were sent.

The trigger consistently initiated the complete autonomous qualification workflow.

---

# 🎉 Outcome

The Outlook trigger provides a reliable event-driven entry point for the NovaWorks Autonomous Sales Lead Qualification Agent.

By combining subject-based filtering with Generative AI Orchestration, the solution automatically transforms incoming sales enquiries into qualified operational records while minimizing manual effort and ensuring consistent processing.