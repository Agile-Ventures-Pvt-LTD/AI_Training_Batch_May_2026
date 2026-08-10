# Tool Implementation

## Excel Online (Business)

**Storage:** Sleepsia_CAP001_Quality_Capstone_Data.xlsx, stored in OneDrive for Business, all sheets configured as named Tables.

**Read access, scoped per specialist:**
| Agent | Tables |
|---|---|
| Safety Specialist | Customer_Complaints |
| Complaint Pattern Specialist | Customer_Complaints |
| Returns Specialist | Returns, Sales_Summary |
| Product/Batch Specialist | Product_Master, Batch_Register, Quality_Incidents, CAPA_Register |
| Customer Impact Specialist | Customer_Complaints, Returns |
| CAPA Specialist | Owners (read), Quality_Incidents (read), CAPA_Register (read/write) |

**Write access, held by Quality Supervisor:**
- Update Quality_Incidents.Status, Notes, ReassessmentCount after final decision or reassessment cycle.
- Update Customer_Complaints.Processed = Yes, only after the Quality_Incidents update succeeds.

**Failure boundary:** If an Excel read fails, the affected specialist's assessment is stopped and the failure is recorded (retry once, then Insufficient Evidence). If the Excel update fails at the reporting stage, Customer_Complaints.Processed is not set to Yes, preventing silent loss of an unprocessed record.

## Word Online (Business)

**Template:** Product Quality Investigation Report (.docx), built with content-control placeholders for: Incident ID, SKU/Product Name, Batch ID, complaint summary, safety assessment, returns/return-rate assessment, product/batch findings, customer impact summary, final classification and rationale, CAPA actions, report generation status/date. Stored alongside the workbook in OneDrive.

**Action used:** Create a Microsoft Word File  by the Quality Supervisor after FinalClassification (and CAPA, where applicable) are available.

**Failure boundary:** On failure, ReportGeneration is set to Failed, the incident decision already recorded is preserved, and the pipeline does not proceed to the Excel/Outlook steps — no report is claimed to exist.

## Office 365 Outlook

**Action used:** First I use draft a message and than send a draft message tool, invoked by the Quality Supervisor only after  the Word report creation have succeeded.

**Recipient logic:** looked up from the Owners table based on final Status/FinalClassification (e.g. Critical Escalation and overdue CAPA route to Quality Lead and relevant escalation owner; standard Investigation/CAPA cases route to Quality Lead; fulfilment-only cases may route to CX Lead).

**Failure boundary:** On failure, Notification is set to Failed, the already-recorded incident decision is preserved, and no successful send is claimed.
