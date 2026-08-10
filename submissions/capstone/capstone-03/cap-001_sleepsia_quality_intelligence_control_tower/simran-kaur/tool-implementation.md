# Tool Implementation

## Excel / Data Tools

### Get Quality Incident
- Connector: Excel Online (Business)
- Action: Get a row
- Table: `Quality_Incidents`
- Key column: `IncidentID`
- Purpose: Retrieve the incident record.

### Check Existing Incidents
- Connector: Excel Online (Business)
- Action: List rows present in a table
- Table: `Quality_Incidents`
- Purpose: Duplicate/status checking.
- Key column: None.

### Update Quality Incident
- Connector: Excel Online (Business)
- Action: Update a row
- Table: `Quality_Incidents`
- Key column: `IncidentID`
- Purpose: Update approved incident fields/status.

### Check Existing CAPA Records
- Connector: Excel Online (Business)
- Action: List rows present in a table
- Table: `CAPA_Register`
- Purpose: Prevent duplicate CAPA creation.
- Key column: None.

## Word

### Generate Quality Incident Report
- Connector: Word Online (Business)
- Action: Create a Microsoft Word document with the given content
- Purpose: Generate the final quality incident report.
- File name pattern: `Quality_Incident_{IncidentID}.docx`

## Outlook

### Send Quality Notification
- Connector: Office 365 Outlook
- Action: Send an email (V2)
- Purpose: Send applicable quality escalation/notification emails.

## Evidence
Screenshots/tool configuration evidence:
`[Add screenshots after final configuration/testing.]`

## Important
Do not add tools against tables that do not exist in the project workbook. In particular, no `AuditLog` table is assumed.
