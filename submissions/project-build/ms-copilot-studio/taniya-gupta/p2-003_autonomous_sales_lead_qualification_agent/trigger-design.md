# trigger-design.md — Trigger Design
## P2-003 Autonomous Sales Lead Qualification Agent

---

## Trigger Type

**Trigger:** Office 365 Outlook — When a new email arrives (V3)
**Channel:** Automated event trigger (non-interactive)
**Connector:** Office 365 Outlook (Microsoft 365 connector)

---

## Trigger Configuration

The following settings are configured in the trigger as shown in the Copilot Studio trigger panel:

| Parameter | Value |
|---|---|
| Trigger name | When a new email arrives (V3) |
| Folder | Inbox |
| Subject Filter | `[P2-003 LEAD]` |
| Include Attachments | No |
| Importance | Any |
| Advanced parameters shown | 4 of 9 |
| Connection | Shared Office 365 connection |

---

## Why Subject Filter `[P2-003 LEAD]`

The subject filter was chosen to:
- Protect all other inbox traffic from being processed by the agent
- Allow any sender to explicitly opt a message into qualification processing by using the prefix
- Match the PRD specification: *"When an email arrives with subject containing [P2-003 LEAD]"*

Only emails whose subject line contains this exact string trigger the agent. Emails without the prefix are completely ignored.

---

## Inputs Extracted from the Trigger

When the trigger fires, the full email payload is passed to the agent. Step 1 of the agent instruction pipeline extracts the following fields from the email body and headers:

| Field | Source | Required |
|---|---|---|
| Contact Name | Email body | Yes |
| Company Name | Email body | Yes |
| Job Title | Email body | No |
| Country | Email body | Yes |
| Product Interest | Email body | Yes |
| Budget (USD) | Email body | Yes |
| Purchase Timeline (days) | Email body | Yes |
| Decision Role | Email body | Yes |
| Business Need | Email body | No |
| Inquiry Type | Agent infers from content | Yes |
| Sender Email | Email From header | Yes — auto-used for reply |

---

## Trigger Behaviour

### Normal Flow
When an email matching the subject filter arrives in the monitored inbox, the trigger fires and passes the email content to the agent. The agent runs the full nine-step processing pipeline autonomously without any human interaction.

### Repeated Trigger (Idempotency)
If Outlook delivers the same email twice, the agent detects the duplicate at Step 3 using a LeadsRegisterTable lookup. The second trigger invocation produces no new Excel row, no new Word report, and no new external communication.

---

## Test Evidence

The trigger was verified through the following tests:

**1. Live Outlook trigger test**
Emails with subject `[P2-003 LEAD]` were sent from a test mailbox to the monitored inbox. The agent responded autonomously, producing the correct classification, Excel row, and outbound communications.

**2. Batch evaluation test**
The Copilot Studio Evaluate panel was used to run 23 email payloads in batch. All 23 triggered the correct pipeline execution path. The evaluation confirmed correct routing across all classification types.

**3. Duplicate trigger test (TC-019)**
The same email payload (Nora Schmidt, EuroBank) was submitted twice. On the second submission, the agent detected the existing record and correctly suppressed all duplicate actions — no new row, no new report, no new acknowledgement.

**4. Non-matching subject test**
Emails without `[P2-003 LEAD]` in the subject line were confirmed to produce no trigger activation.

**5. Non-sales inquiry test**
Emails containing the subject prefix but classified as Support, Academic, or Competitor in the body were correctly classified and stopped without creating qualification reports or sending external results.

---

## Limitations

| Limitation | Detail |
|---|---|
| Single mailbox | The trigger monitors one Outlook inbox only |
| No attachment parsing | Lead fields must be present in the email body; attachments are not read (Include Attachments = No) |
| Subject prefix required | Senders must include `[P2-003 LEAD]` in the subject line for the trigger to activate |
| Polling-based delivery | The trigger polls for new emails rather than using true push; short delays of up to 1–2 minutes may occur |
| No From filter | Any sender can activate the trigger if they include the correct subject prefix; this is mitigated by Step 2 inquiry classification |
