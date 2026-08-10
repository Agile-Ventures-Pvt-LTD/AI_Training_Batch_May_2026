# Trigger Design

## Trigger

The agent starts automatically when a new email arrives in the Outlook mailbox.

The trigger used is:

**Office 365 Outlook – When a new email arrives (V3)**

The agent does not need a user chat to start.

---

## Trigger Filter

The agent processes only emails whose subject contains:

**[P2-003 LEAD]**

All other emails are ignored.

This prevents the agent from processing unrelated emails.

---

## Trigger Inputs

The trigger receives the following information from the email:

- Message ID
- Sender Name
- Sender Email
- Subject
- Email Body
- Received Date and Time
- Attachment Information (if available)

The email body is used to extract lead information.

---

## Processing Flow

1. A new email arrives.
2. The trigger checks the email subject.
3. If the subject contains **[P2-003 LEAD]**, the agent starts.
4. The agent checks for duplicate leads.
5. The agent extracts lead information.
6. The agent reads reference data from Excel.
7. The agent calculates the lead score.
8. The agent assigns the lead classification.
9. The agent updates the Excel Lead Register.
10. The agent creates a Word report if needed.
11. The agent sends the correct reply email.

---

## Test Evidence

The trigger was tested using sample project emails.

The following checks were completed:

- ✅ Trigger starts automatically.
- ✅ Only **[P2-003 LEAD]** emails are processed.
- ✅ Other emails are ignored.
- ✅ Lead information is extracted.
- ✅ Duplicate leads are detected.
- ✅ Excel records are added or updated.
- ✅ Word reports are created for Hot and Qualified leads.
- ✅ Reply emails are sent correctly.

---

## Limitations

- The agent processes only emails with **[P2-003 LEAD]** in the subject.
- Attachment content is not processed.
- The agent depends on Outlook, Excel, and Word connections.
- If a tool fails after one retry, the case is sent for human review.
- Only synthetic project data is supported.