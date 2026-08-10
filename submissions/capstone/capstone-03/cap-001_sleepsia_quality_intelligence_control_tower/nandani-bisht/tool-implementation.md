# Tool and Connector Integration

This document defines the configuration, schema mappings, boundaries, and failure behaviors for the three primary Office 365 connectors integrated into the **Sleepsia Quality Control Tower**.

---

## 1. Excel Online (Business) Connector

### Purpose
Used to query the operational dataset containing products, complaints, sales, and returns, and to record incident and CAPA statuses.

### Configurations
- **Connection Type:** Microsoft Entra ID (Service Principal or User Delegated Connection).
- **Location:** OneDrive for Business / SharePoint Document Library.
- **Workbook Path:** `/Sleepsia_CAP001_Quality_Capstone_Data.xlsx`

### Target Tables & Schema Mappings
1. **`Customer_Complaints` (Read/Write):**
   - *Fields Read:* `ComplaintID`, `OrderID`, `SKU`, `BatchID`, `ComplaintDate`, `Category`, `Severity`, `SafetyIndicator`.
   - *Fields Written:* `Processed = "Yes"` (Updated *only* after incident record creation is confirmed).
2. **`Quality_Incidents` (Write):**
   - *Fields Written:* `IncidentID`, `SKU`, `BatchID`, `DateCreated`, `Classification`, `Severity`, `State`, `ReportLink`, `NotificationStatus`.
3. **`CAPA_Register` (Write):**
   - *Fields Written:* `CAPAID`, `IncidentID`, `SKU`, `ContainmentAction`, `CorrectiveAction`, `OwnerRole`, `TargetDate`, `Status`.
4. **`Product_Master`, `Batch_Register`, `Returns`, `Sales_Summary` (Read-Only):**
   - Queried by specialists to extract reference data.

### Boundary Rules
- **No Overwriting Source Evidence:** Raw customer complaint records (e.g., texts, categories, and original safety flags) are strictly read-only.
- **Transactional Updates:** If writing to `Quality_Incidents` fails, the row in `Customer_Complaints` must *not* be updated to `Processed = Yes`. It must remain `Processed = No` for re-evaluation in the next run.

---

## 2. Word Online (Business) Connector

### Purpose
Automates the drafting of a formal `Product Quality Investigation Report` when an incident classification requires it (Investigation, High-Priority, or Critical).

### Configurations
- **Action Used:** "Populate a Microsoft Word template" -> "Create file" in OneDrive.
- **Template Path:** `/Templates/Sleepsia_Investigation_Report_Template.docx`

### Mapped Template Fields
- `{{IncidentID}}` - Auto-generated unique tracking string.
- `{{SKU}}` & `{{ProductName}}` - Validated item identifiers.
- `{{BatchID}}` & `{{SupplierLot}}` - Manufacture tracking info.
- `{{Severity}}` & `{{Classification}}` - Determined by Supervisor.
- `{{Findings}}` - Consolidated specialist outputs.
- `{{CAPA_Containment}}` & `{{CAPA_Corrective}}` - Drafted by CAPA Specialist.
- `{{TargetDate}}` & `{{OwnerRole}}` - Assigned action owners.

### Boundary & Failure Handling
- **Exception Catching:** The Word generation step is isolated. If the OneDrive file creation fails (e.g., due to account quota limits or filename conflicts):
  1. The system catches the error.
  2. The incident field `ReportLink` is populated with `"Failed - Check Logs"`.
  3. The system does *not* claim to the user or supervisor that the report was successfully generated.
  4. The workflow proceeds to the next notification block.

---

## 3. Office 365 Outlook Connector

### Purpose
Sends automated alerts to designated owners and supervisors following the final incident decision.

### Configurations
- **Action Used:** "Send an email (V2)"
- **Sender account:** `quality-control-tower@sleepsia.com`

### Email Template Schema
- **To:** Assigned `OwnerRole` email address retrieved from the `Owners` master table.
- **Subject:** `[CRITICAL ESCALATION] Quality Incident Alert - SKU {{SKU}} (Incident ID: {{IncidentID}})`
- **Body:**
  ```text
  Attention Quality Operations Team,
  
  A new quality incident has been registered and verified:
  - Incident ID: {{IncidentID}}
  - Affected SKU: {{SKU}} ({{ProductName}})
  - Batch ID / Lot: {{BatchID}}
  - Classification: {{Classification}}
  - Assessed Severity: {{Severity}}
  
  CAPA PLAN REQUIRED:
  - Containment Action: {{CAPA_Containment}}
  - Corrective Action: {{CAPA_Corrective}}
  - Assigned Owner: {{OwnerRole}}
  - Target Completion Date: {{TargetDate}}
  
  Please log in to the Control Tower dashboard to confirm receipt and begin execution.
  ```

### Boundary & Failure Handling
- **Non-blocking Status Logging:** If the email dispatch fails (e.g., due to an invalid email address or service outage):
  1. The system records the status `Notification = Failed` in the incident record.
  2. The incident decision is *not* rolled back.
  3. A manual alert flag is raised on the Supervisor's dashboard.
