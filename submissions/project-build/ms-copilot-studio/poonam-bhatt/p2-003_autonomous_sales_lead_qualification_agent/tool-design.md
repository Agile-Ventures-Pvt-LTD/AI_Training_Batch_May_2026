# Tool Design Document

# P2-003 Autonomous Sales Lead Qualification Agent

---

## 1. Tool Design Overview

The agent is configured with 12 specific connector tools in Microsoft Copilot Studio. These tools represent direct integrations with Microsoft Excel Online (Business), Office 365 Outlook, OneDrive/SharePoint, and Word Online (Business). The tools are enabled and orchestrated by the agent's generative reasoning engine.

---

## 2. Detailed Tool Specifications

### 2.1 Excel Online (Business) Connector Tools
These tools connect to the operational workbook `P2-003_Sales_Lead_Operational_Data.xlsx` hosted on OneDrive for Business or SharePoint.

#### 1. Tool Name: `Add Lead`
- **Connector Type:** Excel Online (Business)
- **Status:** Enabled (On)
- **When it should be used:** Used when a new qualified, hot, nurture, low-priority, or review lead needs to be recorded as a new row in the `LeadsRegisterTable`.
- **Required Inputs:**
  - `File Path` (String)
  - `Table Name`: `LeadsRegisterTable` (String)
  - `Row Data`: JSON object containing lead fields (e.g. `Lead_ID`, `Received_Date`, `Company_Name`, `Country`, `Score`, `Classification`, `Assigned_Owner`, etc.).
- **Expected Outputs:**
  - `Row Reference ID` (String)
  - `Response Status` (Boolean)
- **Conditions under which it must not be used:** Must not be used for leads identified as duplicates (those route to `Update Lead` instead).
- **Action Boundary:** Internal database write operation.

#### 2. Tool Name: `Get Sales Owners`
- **Connector Type:** Excel Online (Business)
- **Status:** Enabled (On)
- **When it should be used:** Used to read the sales owner directory from the `SalesOwnersTable` to check representative names, emails, active/inactive statuses, and current capacities.
- **Required Inputs:**
  - `File Path` (String)
  - `Table Name`: `SalesOwnersTable` (String)
- **Expected Outputs:**
  - Array of sales owner records (Owner Name, Territory, Role, Email, Status, Capacity).
- **Conditions under which it must not be used:** None.
- **Action Boundary:** Internal read operation.

#### 3. Tool Name: `Get Qualification Rules`
- **Connector Type:** Excel Online (Business)
- **Status:** Enabled (On)
- **When it should be used:** Used to fetch the scoring rules and point thresholds from the `QualificationRulesTable` to dynamically calculate scores.
- **Required Inputs:**
  - `File Path` (String)
  - `Table Name`: `QualificationRulesTable` (String)
- **Expected Outputs:**
  - List of scoring criteria across 8 dimensions (Product Fit, Budget, Timeline, Decision Role, Company Size, Territory, Source, Completeness).
- **Conditions under which it must not be used:** None.
- **Action Boundary:** Internal read operation.

#### 4. Tool Name: `Get Product Catalog`
- **Connector Type:** Excel Online (Business)
- **Status:** Enabled (On)
- **When it should be used:** Used to retrieve canonical product names, categories, and minimum budget requirements from the `ProductCatalogTable`.
- **Required Inputs:**
  - `File Path` (String)
  - `Table Name`: `ProductCatalogTable` (String)
- **Expected Outputs:**
  - Product catalogue records (Product ID, Product Name, Category, Minimum Budget, Product Fit).
- **Conditions under which it must not be used:** None.
- **Action Boundary:** Internal read operation.

#### 5. Tool Name: `Get Action Matrix`
- **Connector Type:** Excel Online (Business)
- **Status:** Enabled (On)
- **When it should be used:** Used to look up the required actions (report generation, external emails, internal notifications) associated with each lead classification from the `ActionMatrixTable`.
- **Required Inputs:**
  - `File Path` (String)
  - `Table Name`: `ActionMatrixTable` (String)
- **Expected Outputs:**
  - Classification criteria and required action text (Hot, Qualified, Nurture, Low Priority, Review, Duplicate, Not a Sales Lead).
- **Conditions under which it must not be used:** None.
- **Action Boundary:** Internal read operation.

#### 6. Tool Name: `Get Territory Mapping`
- **Connector Type:** Excel Online (Business)
- **Status:** Enabled (On)
- **When it should be used:** Used to look up country-to-territory mappings and resolve default sales owners from the `TerritoryOwnersTable`.
- **Required Inputs:**
  - `File Path` (String)
  - `Table Name`: `TerritoryOwnersTable` (String)
- **Expected Outputs:**
  - Territory mapping rules (Country, Territory, Default Owner, Time Zone, Status).
- **Conditions under which it must not be used:** None.
- **Action Boundary:** Internal read operation.

#### 7. Tool Name: `Get Lead Register`
- **Connector Type:** Excel Online (Business)
- **Status:** Enabled (On)
- **When it should be used:** Used at the beginning of the evaluation phase to fetch existing records from `LeadsRegisterTable` for duplicate detection logic.
- **Required Inputs:**
  - `File Path` (String)
  - `Table Name`: `LeadsRegisterTable` (String)
- **Expected Outputs:**
  - Array of previous leads (Lead ID, Message ID, Email, Company, Product).
- **Conditions under which it must not be used:** None.
- **Action Boundary:** Internal read operation.

#### 8. Tool Name: `Update Lead`
- **Connector Type:** Excel Online (Business)
- **Status:** Enabled (On)
- **When it should be used:** Used when a duplicate lead is detected, or when a lead status changes. Updates details (e.g. `Last_Updated`, `Last_Action`, `Processing_Status`) on an existing row using the `Lead_ID` key.
- **Required Inputs:**
  - `File Path` (String)
  - `Table Name`: `LeadsRegisterTable` (String)
  - `Key Column`: `Lead_ID`
  - `Key Value`: Matched Lead ID (e.g., `LD-2026-0001`)
  - `Updated Fields`: JSON object representing changed cells.
- **Expected Outputs:**
  - `Response Status` (Boolean)
- **Conditions under which it must not be used:** Must not be used for creating new leads.
- **Action Boundary:** Internal database write operation.

---

### 2.2 Office 365 Outlook Connector Tool

#### 9. Tool Name: `Send an email (V2)`
- **Connector Type:** Office 365 Outlook
- **Status:** Enabled (On)
- **When it should be used:** Used for all outbound email communications:
  - Sending external acknowledgements to clients for new Hot/Qualified leads.
  - Sending missing information requests to prospects.
  - Alerting assigned territory owners (Internal Hot/Qualified Lead Alerts).
  - Alerting the Sales Operations team for leads classified as `Human Review Required`.
- **Required Inputs:**
  - `To`: Recipient email address (String)
  - `Subject`: Standardized subject line (String)
  - `Body`: Structured email body content (HTML or Plain Text)
- **Expected Outputs:**
  - `Response Status` (Boolean)
- **Conditions under which it must not be used:**
  - Must not be used to communicate a qualification decision externally when a lead is classified as `Human Review Required` (due to competitor risk, unmapped territory, unknown product, or low confidence).
  - Must not contain pricing, discounts, SLAs, or contract promises.
- **Action Boundary:** Can cross security boundaries to send emails externally to customers, as well as internally to team members.

---

### 2.3 File and Word Online (Business) Connector Tools

#### 10. Tool Name: `Create file`
- **Connector Type:** OneDrive / SharePoint
- **Status:** Enabled (On)
- **When it should be used:** Used to write and save the generated Word document lead briefs (`LD-YYYY-NNNN_Lead_Qualification_Report.docx`) in the target SharePoint or OneDrive document library folder `/LeadBriefs/`.
- **Required Inputs:**
  - `Folder Path`: Target OneDrive or SharePoint directory (e.g. `/LeadBriefs/`)
  - `File Name`: Name of the file, which must contain the unique Lead ID.
  - `File Content`: Binary document stream generated by the reporting engine.
- **Expected Outputs:**
  - `File Path` / `Web URL` (String)
- **Conditions under which it must not be used:** Must not be called for leads classified as `Nurture`, `Low Priority`, `Additional Info Required`, `Duplicate`, or `Not a Sales Lead`.
- **Action Boundary:** Internal file generation and storage write.

#### 11. Tool Name: `Generate Lead Qualification Report`
- **Connector Type:** Word Online (Business)
- **Status:** Enabled (On)
- **When it should be used:** Used to compile the structured Word brief for `Hot` and `Qualified` leads. This tool structures the extracted metadata, scoring breakdown, risk assessments, and next steps into the document layout before writing it to OneDrive.
- **Required Inputs:**
  - `Lead Metadata`: JSON object with Lead ID, Contact, Company, Product, Score, Classification, Owner, and Risk Flags.
- **Expected Outputs:**
  - Document file stream.
- **Conditions under which it must not be used:**
  - Must not be called if the lead is not classified as `Hot` or `Qualified`.
  - Must not be called if a duplicate lead is processed.
- **Action Boundary:** Internal file compilation.

#### 12. Tool Name: `Populate a Microsoft Word template`
- **Connector Type:** Word Online (Business)
- **Status:** **Disabled (Off)**
- **Why it is disabled:** This tool was part of an alternative report generation architecture. It has been replaced by the custom tool `Generate Lead Qualification Report` to provide better control over dynamic table grids (such as the scoring breakdown matrix) which standard content controls cannot handle. It is kept inactive in the configuration for compliance reference.
