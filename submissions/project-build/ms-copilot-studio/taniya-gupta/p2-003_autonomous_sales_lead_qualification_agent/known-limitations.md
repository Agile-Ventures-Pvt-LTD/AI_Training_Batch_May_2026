# known-limitations.md — Known Limitations
## P2-003 Autonomous Sales Lead Qualification Agent

---

## Functional Limitations

### 1. Scoring is Generative
The scoring logic is implemented through generative AI instructions rather than hard-coded arithmetic. The agent applies the scoring rules from the knowledge source and instructions, but may occasionally produce minor differences in edge cases near band thresholds. All test cases produced correct classifications, but the exact numeric score may vary slightly between invocations on borderline leads.

**Mitigation:** The agent records the calculated score in the Excel row, allowing human review of any borderline case.

### 2. Email Body Parsing Depends on Email Format
The agent extracts fields by reading natural language email body text. If an incoming email is heavily formatted with HTML, embedded images, or non-standard layouts, the extraction may miss fields.

**Mitigation:** The sample email template in `Sample_Incoming_Lead_Emails.txt` provides a plain-text format that reliably produces complete field extraction.

### 3. No Attachment Processing
The agent does not read email attachments. All lead information must be present in the email body. If a sender includes lead details only in an attached PDF or spreadsheet, those fields will be missing.

**Mitigation:** The missing fields request email sent to the sender lists exactly which fields are needed in the reply body.

### 4. 90-Day Duplicate Window
The duplicate detection check searches LeadsRegisterTable for records within the last 90 days. A lead from the same company and contact submitted more than 90 days apart will be processed as a new lead rather than a duplicate.

### 5. Territory Table Scope
The territory mapping supports 11 countries. Leads from countries outside this list are correctly routed to Human Review Required. As NovaWorks expands into new territories, the TerritoryOwnersTable in the Excel workbook and the territory section of the agent instructions must both be updated.

### 6. Single Inbox Scope
The agent monitors one mailbox only.

---

## Connector Limitations

### 7. Excel Row Limit
The Excel Online connector reads up to 256 rows by default in Get Rows calls. If LeadsRegisterTable grows beyond 256 rows without pagination, the duplicate detection Get Rows call may not search the full history.

**Mitigation:** The duplicate check filter is scoped to the last 90 days, which limits the rows examined.

### 8. Word Document Stored in OneDrive Only
The Word Online Create document tool writes the qualification report to a OneDrive for Business path in root directory only not in specified folder path.

### 9. Synthetic Email Addresses in Tests
All test email addresses use `.example` non-routable domains. If the Outlook Send an email tool is invoked with these addresses during a live Outlook trigger test, Outlook will return an HTTP 400 recipient invalid error.

---
