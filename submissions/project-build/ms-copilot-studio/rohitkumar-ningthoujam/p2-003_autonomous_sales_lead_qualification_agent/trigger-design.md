# Trigger Design

## Purpose

The Autonomous Sales Lead Qualification Agent uses an Outlook event trigger to automatically start processing when a qualifying sales inquiry email is received. The trigger removes the need for manual chat interaction and enables autonomous execution of the lead qualification workflow.

---

# Trigger Configuration

**Platform:** Microsoft Copilot Studio

**Connector:** Office 365 Outlook

**Trigger:**
**When a new email arrives (V3)**

The trigger continuously monitors the configured Microsoft 365 mailbox for new incoming emails.

---

# Trigger Safety Filter

To prevent unrelated emails from being processed, the trigger only processes emails whose subject contains:

**[P2-003 LEAD]**

Emails that do not match this condition are ignored and no further processing is performed.

---

# Trigger Inputs

The trigger provides the following information to the agent:

| Input                  | Purpose                                                            |
| ---------------------- | ------------------------------------------------------------------ |
| Message ID             | Used for duplicate detection                                       |
| Sender Name            | Identifies the contact                                             |
| Sender Email           | Used for communication and duplicate checks                        |
| Subject                | Validates project scope                                            |
| Email Body             | Source for lead information extraction                             |
| Received Date and Time | Records lead receipt                                               |
| Attachment Metadata    | Indicates attachment presence (attachment parsing not implemented) |

---

# Trigger Processing Flow

1. A new email arrives in the monitored Outlook mailbox.
2. The subject is validated against **[P2-003 LEAD]**.
3. Matching emails are passed to the autonomous agent.
4. The agent extracts lead information.
5. Duplicate detection is performed.
6. Reference data is retrieved from Excel Online (Business).
7. Qualification scoring and classification are completed.
8. Operational actions are executed according to the classification.

---

# Test Evidence

The trigger was validated using synthetic project emails representing multiple business scenarios, including:

* Hot Lead
* Qualified Lead
* Nurture Lead
* Low Priority Lead
* Human Review Required
* Additional Information Required
* Duplicate Lead
* Non-Sales Request
* Academic Research Request
* Unknown Product
* Unmapped Territory

The trigger executed successfully for emails containing the required subject filter and ignored emails outside the defined scope.

---

# Trigger Limitations

* Processes only emails containing **[P2-003 LEAD]** in the subject.
* Requires a valid Microsoft 365 Outlook connection.
* Requires the agent to be published for autonomous execution.
* Attachment parsing was not implemented as part of the project scope.
* Trigger execution depends on Microsoft 365 connector availability and tenant permissions.

---

# Compliance with PRD

The trigger implementation satisfies the project requirements by:

* Using the Office 365 Outlook **When a new email arrives (V3)** trigger.
* Restricting execution to project emails through a subject filter.
* Passing the required email metadata to the agent.
* Supporting autonomous processing without manual chat interaction.
* Providing the necessary input for duplicate detection, qualification, and communication workflows.
