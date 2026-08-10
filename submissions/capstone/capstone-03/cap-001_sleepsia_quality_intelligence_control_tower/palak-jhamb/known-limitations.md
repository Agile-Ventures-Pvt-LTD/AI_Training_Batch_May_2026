# Known Limitations

## Project Limitations

The following limitations were identified during the implementation of the Sleepsia Product Quality & Customer Experience Intelligence Control Tower.

---

# Microsoft 365 Tenant Limitations

- Microsoft Teams publishing could not be completed because the Microsoft 365 tenant requires billing configuration before publishing to Teams.
- Public deployment could not be validated due to tenant restrictions.

---

# Connector Limitations

The project uses Microsoft 365 connectors available within the configured tenant.

Configured connectors include:

- Excel Online (Business)
- Word Online (Business)
- Office 365 Outlook

Connector execution depends on:

- Active Microsoft 365 license
- Valid authentication
- Connector permissions
- Accessible cloud storage locations

---

# Excel Tool Limitations

Excel tools operate only on configured workbooks.

Limitations include:

- Workbook must exist before execution.
- Table names must match configuration.
- Required columns must already exist.
- Missing or renamed tables will cause tool execution failures.

---

# Word Tool Limitations

Word document generation requires:

- A valid Word template.
- Accessible OneDrive or SharePoint storage.
- Proper template placeholders.

Incorrect templates may prevent successful document generation.

---

# Outlook Tool Limitations

Email notifications depend on:

- Valid recipient email addresses.
- Microsoft Outlook connectivity.
- Organization email policies.
- Connector authentication.

Delivery confirmation is handled by Microsoft Outlook.

---

# Knowledge Source Limitations

Knowledge responses depend on the configured Sleepsia documentation.

The supervisor does not generate unsupported product information and only responds using available knowledge sources.

---

# Child Agent Limitations

Specialist agents operate only within their assigned domains.

The supervisor is responsible for:

- Final classification
- CAPA approval
- Workflow orchestration
- Investigation closure

Child agents cannot override supervisor decisions.

---

# Topic Limitations

The implementation includes four deterministic topics:

1. Incident Intake & Validation
2. Quality Investigation Decision
3. CAPA Planning & Ownership
4. Evidence Update & Selective Reassessment

Topic execution depends on valid input data provided by the supervisor.

---

# Reassessment Limitation

Selective reassessment is bounded.

The workflow allows a maximum of two automated reassessment cycles.

If additional reassessments are required, the investigation is routed for Manual Review.

---

# Data Limitations

Testing was performed using synthetic project data.

No production customer data or live enterprise systems were used during implementation.

---

# Publishing Limitation

The solution could not be published to Microsoft Teams because billing was not enabled for the tenant.

All remaining functionality was successfully tested within Microsoft Copilot Studio.

---

# Future Improvements

Potential future enhancements include:

- Teams deployment after tenant billing activation.
- Integration with Dataverse or enterprise databases.
- Power BI dashboards for investigation analytics.
- Automated SLA monitoring.
- Expanded quality reporting.
- Additional specialist agents.
- Enhanced notification workflows.