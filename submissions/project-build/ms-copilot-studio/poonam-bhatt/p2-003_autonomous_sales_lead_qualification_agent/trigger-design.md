# Trigger Design

# P2-003 Autonomous Sales Lead Qualification Agent

---

## 1. Trigger Specification

The agent uses a direct connector trigger to listen for external events rather than reacting to a manual chat session.

- **Trigger Name:** Office 365 Outlook: When a new email arrives (V3)
- **Connector Provider:** Microsoft 365 / Office 365 Outlook
- **Connection Type:** Direct Cloud Connector (asynchronous webhooks)

---

## 2. Safety Filters

To prevent the agent from reading, processing, or responding to unrelated corporate emails, a strict trigger-level safety filter is applied:

| Filter Field | Applied Value / Pattern | Behavior |
|---|---|---|
| **Subject Filter** | `[P2-003 LEAD]` | **Required Prefix/Substring.** The M365 event listener evaluates this condition at the mail-server boundary. |
| **Folder** | `Inbox` | Only monitors the root Inbox folder of the configured shared sales operations mailbox. |
| **Importance** | `Any` | Triggers for emails of any importance level. |

- **Non-Matching Messages:** If an email is received without `[P2-003 LEAD]` in its subject, the webhook does not fire. No billing tokens, API calls, or agent execution cycles are consumed.

---

## 3. Trigger Input Data Schema

When the trigger fires, the following data payload is extracted from the Outlook mail object and mapped directly into the Copilot Studio context variables:

| Variable Name | M365 Data Type | Description |
|---|---|---|
| `messageId` | String (GUID/Base64) | Unique internet message identifier. Used as the primary key for duplicate detection. |
| `fromAddress` | String (Email) | Sender's email address (e.g. `client@domain.example`). |
| `fromName` | String (Text) | Display name of the sender. |
| `subject` | String (Text) | Subject line of the email. |
| `body` | String (HTML/Text) | Raw unstructured content of the email body. |
| `receivedDateTime`| DateTime (ISO 8601) | Timestamp of email receipt. Used for recording `Received_Date`. |
| `hasAttachments` | Boolean | Flag indicating if attachments are present. |

---

## 4. Trigger Test Evidence

### Test Validation Cases:
1. **Valid Trigger Event (TC-001):** An email with the subject `[P2-003 LEAD] Enterprise multi-agent platform for Orbital Finance` was sent. The agent successfully triggered, executed the extraction workflow, scored the lead at 98, and wrote a record to Excel within 45 seconds of receipt.
2. **Suppression Event (Non-Scope Email):** An email with the subject `Project budget discussion` was sent to the inbox. The run history logs in Copilot Studio confirm that the agent did *not* trigger, and no activity was recorded.
3. **Idempotency/Trigger Flood (TC-017 / Duplicate Check):** Sending the same email twice (matching message ID or matching company/email/product combination) successfully triggers the agent, but the internal logic routes it to the duplicate handler. It updates the existing row with `Processing_Status = Duplicate` and suppresses further outbound alerts.

---

## 5. Known Trigger Limitations

- **Polling Frequency Latency:** Depending on Microsoft 365 tenant routing and Outlook sync, a polling latency of 30 to 120 seconds may occur between email receipt and agent initiation.
- **Attachment Exclusion:** Attachment parsing is disabled for this version. The agent reads the email body text only.
- **Email Size Limitations:** The maximum email size supported by the connector is 10 MB. Emails exceeding this limit will trigger a failure event in Copilot Studio.
- **HTML Character Encoding:** Heavy nesting of HTML elements in the email body can cause tokenization errors in generative extraction. The orchestrator is configured to sanitize HTML tags and extract text before executing the system prompt.
