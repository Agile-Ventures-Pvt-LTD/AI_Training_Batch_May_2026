# Trigger Design

## P2-003 Autonomous Sales Lead Qualification Agent

## Purpose

This document describes the trigger design for the **NovaWorks Autonomous Sales Lead Qualification Agent** implemented in **Microsoft Copilot Studio**.

The trigger enables fully autonomous execution by starting the agent automatically whenever a qualifying Outlook email is received. The design follows the P2-003 PRD requirements for event-driven processing, safety filtering, deterministic input handling, and autonomous monitoring.

---

# Trigger objective

The trigger initiates the complete lead qualification workflow without requiring any manual chat interaction.

The trigger must:

* monitor the designated Outlook mailbox
* filter only project lead emails
* pass email metadata to the agent
* initiate autonomous processing
* prevent unrelated inbox messages from being processed

---

# Trigger type

| Configuration     | Value                         |
| ----------------- | ----------------------------- |
| Trigger Platform  | Microsoft Copilot Studio      |
| Trigger Connector | Office 365 Outlook            |
| Trigger Action    | When a new email arrives (V3) |
| Execution Mode    | Autonomous                    |
| Trigger Status    | Enabled                       |

---

# Trigger configuration

## Mailbox

The trigger monitors the dedicated Microsoft 365 mailbox used for synthetic sales lead processing.

| Setting            | Configuration                    |
| ------------------ | -------------------------------- |
| Mailbox            | Configured Microsoft 365 mailbox |
| Folder             | Inbox                            |
| Include Subfolders | No                               |
| Trigger Frequency  | Event-driven                     |

---

# Subject safety filter

To prevent unintended processing, the trigger processes only emails whose subject contains:

```text
[P2-003 LEAD]
```

Examples of valid subjects:

```text
[P2-003 LEAD] Enterprise CRM Request
[P2-003 LEAD] Manufacturing Analytics Inquiry
[P2-003 LEAD] Retail Platform Evaluation
```

Examples of ignored subjects:

```text
Support Ticket
Interview Request
Invoice Query
Meeting Invitation
General Inquiry
```

This filter ensures that only project-specific synthetic lead emails activate the autonomous workflow.

---

# Trigger input mapping

The trigger passes the following data to the agent.

| Trigger Field       | Agent Variable      | Required |
| ------------------- | ------------------- | -------- |
| Message ID          | Source_Message_ID   | Yes      |
| From Email          | Sender_Email        | Yes      |
| From Name           | Sender_Name         | Yes      |
| Subject             | Email_Subject       | Yes      |
| Body                | Email_Body          | Yes      |
| Received Time       | Received_Date       | Yes      |
| Has Attachments     | Has_Attachments     | Optional |
| Attachment Metadata | Attachment_Metadata | Optional |

The **Message ID** is used for exact duplicate detection.

---

# Trigger execution flow

```text
New Outlook Email
        |
        v
Subject Filter
        |
        +------ No Match
        |         |
        |         v
        |     Ignore Email
        |
        +------ Match
                  |
                  v
        Extract Trigger Data
                  |
                  v
        Start Copilot Agent
                  |
                  v
        Autonomous Processing
```

---

# Trigger validation logic

Before processing begins, the trigger validates:

1. subject contains `[P2-003 LEAD]`
2. sender email exists
3. message ID exists
4. email body is available
5. trigger execution is unique

If validation fails, the email is ignored and no autonomous processing occurs.

---

# Idempotency design

The trigger must avoid duplicate execution.

The agent performs duplicate detection using:

* Source_Message_ID
* sender email
* company name
* product interest

If the same email is delivered multiple times:

* no duplicate Excel row is created
* no duplicate Word report is created
* no duplicate acknowledgement is sent

This satisfies the PRD idempotency requirement.

---

# Trigger security boundary

The trigger is restricted to authenticated Microsoft 365 resources.

The trigger does not:

* process external mailboxes
* access unauthorized folders
* bypass connector authentication
* process emails outside the configured scope

---

# Autonomous processing boundary

After the trigger fires, the agent executes the complete workflow.

The trigger is responsible only for initiating execution.

The trigger does not:

* calculate scores
* assign owners
* create Word reports
* update Excel
* send Outlook communications

Those actions are performed by the agent through connector tools.

---

# Failure handling

## Trigger delivery failure

If Outlook does not deliver the trigger event:

* no autonomous run occurs
* no Excel changes occur
* no Word report is generated
* no communication is sent

## Trigger validation failure

If the subject filter does not match:

* processing is skipped
* no lead record is created

## Duplicate trigger delivery

If the same message is delivered multiple times:

* duplicate detection prevents duplicate records
* duplicate reports are not created
* duplicate emails are not sent

---

# Retry behavior

The trigger itself is event-driven.

Retry behavior applies to downstream tool execution.

If a connector action fails:

1. perform one controlled retry
2. record the failure
3. notify Sales Operations when required
4. stop dependent actions

The trigger does not repeatedly reprocess the same message after successful duplicate detection.

---

# Monitoring configuration

Trigger execution is monitored through **Copilot Studio Activity / Run History**.

The following information is reviewed:

* trigger execution time
* message ID
* autonomous run status
* tool execution sequence
* success or failure state
* retry events
* duplicate detection result

Monitoring confirms that the trigger is operating autonomously and processing only qualifying emails.

---

# Test evidence

The trigger was validated using synthetic Outlook emails.

## Test scenarios

| Test               | Expected Result                       |
| ------------------ | ------------------------------------- |
| Valid lead email   | Trigger executes                      |
| Invalid subject    | Trigger ignored                       |
| Duplicate email    | Existing record updated               |
| Human review case  | Trigger executes and escalates        |
| Unknown product    | Trigger executes and routes to review |
| Unmapped territory | Trigger executes and routes to review |
| Repeated delivery  | No duplicate outputs                  |

---

# Validation results

| Validation Item                 | Result |
| ------------------------------- | ------ |
| Trigger activated automatically | Passed |
| Subject filter enforced         | Passed |
| Trigger inputs mapped correctly | Passed |
| Message ID captured             | Passed |
| Autonomous execution started    | Passed |
| Duplicate prevention confirmed  | Passed |
| Monitoring visibility confirmed | Passed |

---

# Configuration evidence

The following screenshots should be included in the submission.

* Trigger overview
* Outlook connector configuration
* Folder configuration
* Subject filter configuration
* Trigger input mapping
* Successful trigger execution
* Run history
* Duplicate prevention evidence

---

# Design rationale

The trigger design intentionally uses a **strict subject filter** combined with **event-driven execution**.

This approach provides:

* deterministic activation
* reduced accidental processing
* simplified testing
* improved auditability
* controlled autonomy
* PRD compliance

The trigger acts as the entry point for the autonomous qualification pipeline while keeping business logic inside the Copilot Studio agent and connector tools.

---

# PRD compliance

| PRD Requirement               | Status   |
| ----------------------------- | -------- |
| Outlook event trigger         | Complete |
| When a new email arrives (V3) | Complete |
| Subject filtering             | Complete |
| Trigger input mapping         | Complete |
| Autonomous execution          | Complete |
| Duplicate-safe processing     | Complete |
| Monitoring support            | Complete |
| Microsoft 365 implementation  | Complete |

---

# Final status

The Outlook trigger has been designed and configured to provide **safe, autonomous, event-driven lead qualification initiation** in Microsoft Copilot Studio.

The implementation satisfies the P2-003 PRD requirements for trigger scope, filtering, input handling, idempotency, monitoring, and autonomous workflow initiation.
