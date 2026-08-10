# Tool Implementation

## 1. Purpose

This document defines the implementation and usage boundaries for the
tools required by the CAP-001 Sleepsia Product Quality & Customer
Experience Intelligence Control Tower.

The PRD requires three primary business tool groups:

-   Excel Online (Business)
-   Word Online (Business)
-   Office 365 Outlook

Microsoft Learn MCP is documented separately in `mcp-implementation.md`
and is attached only to the M365 Guidance Specialist.


The tool design follows one core principle:

> Tools perform controlled operational actions; the Quality Supervisor
> remains the only owner of the final internal quality classification
> and authorization of final report/notification actions.

## 2. Operational Workbook

The supplied workbook is the main operational data source.

Required tables include:

-   `Product_Master`
-   `Batch_Register`
-   `Customer_Complaints`
-   `Sales_Summary`
-   `Returns`
-   `Quality_Incidents`
-   `CAPA_Register`
-   `Owners`
-   `Quality_Rules`
-   `Test_Scenarios`

The PRD specifies the row counts and purpose of these tables and
requires the workbook to be stored in OneDrive for Business or
SharePoint so Excel Online (Business) can access it.


## 3. Tool-to-Agent Allocation

  -----------------------------------------------------------------------
  Tool              Main consumer     Purpose           Action type
  ----------------- ----------------- ----------------- -----------------
  Get Customer      Supervisor /      Retrieve          Read
  Complaint         Complaint Pattern complaint         
                    / Customer Impact evidence          

  Get Product       Supervisor /      Validate and      Read
  Master            Product-Batch     retrieve product  
                                      data              

  Get Batch Master  Supervisor /      Validate batch    Read
                    Product-Batch     and SKU mapping   

  Get Quality Rules Supervisor        Retrieve approved Read
                                      decision rules    

  Get Returns       Returns           Analyze returns   Read
                    Specialist                          

  Get Sales Summary Returns           Calculate         Read
                    Specialist        return-rate       
                                      denominator       

  Get Quality       Product-Batch /   Retrieve incident Read
  Incident          Supervisor        history/state     

  Get CAPA          CAPA / Supervisor Retrieve CAPA     Read
                                      status and due    
                                      dates             

  Get Location /    CAPA Specialist / Identify          Read
  Owner data        Supervisor        operational owner 
                                      information       

  Update Customer   Supervisor /      Update complaint  Update
  Complaint         trigger flow      processing state  

  Update Quality    Supervisor        Create/update     Update
  Incident                            incident state    

  Add CAPA Row      CAPA Specialist   Create a CAPA     Create
                                      record when       
                                      required          

  Update CAPA Row   CAPA Specialist / Update CAPA       Update
                    Supervisor        status/action     
                                      state             

  Create Word       Supervisor        Generate          Create
  Report                              investigation     
                                      report            

  Send Outlook      Supervisor        Send internal     Action
  Notification                        notification      
  -----------------------------------------------------------------------

The PRD requires Excel to read complaints, returns, products and rules
and to update incident/CAPA state. 

## 4. Read Tools

### 4.1 Get Customer Complaint

**Description:**

> Retrieves customer complaint records from `Customer_Complaints` using
> ComplaintID, OrderID, SKU, BatchID, or other supported identifiers.
> Returns only the operational complaint evidence required for
> validation and quality analysis.

**Use for:**

-   Incident intake.
-   Complaint clustering.
-   Category/failure-mode analysis.
-   Customer impact analysis.
-   Safety review.
-   Reassessment.

The Complaint Pattern Specialist uses `Customer_Complaints` to count
complaints by SKU, batch and category and identify repeated failure
modes. 

### 4.2 Get Product Master

**Description:**

> Retrieves authoritative product information from `Product_Master`,
> including supported SKU details and approved product references. Used
> to validate SKU existence and provide product evidence.

**Use for:**

-   SKU validation.
-   Product identification.
-   Product/batch analysis.
-   Approved product-link lookup.

The PRD defines `Product_Master` as the source for supported products
and public product links. 

### 4.3 Get Batch Master

**Description:**

> Retrieves batch information from `Batch_Register` and validates the
> relationship between BatchID and SKU, including supplier lot,
> manufacture information, quality hold and previous-incident evidence
> where available.

**Use for:**

-   Batch validation.
-   SKU/batch mapping.
-   Supplier-lot analysis.
-   Previous incident analysis.
-   Missing-batch detection.

The Product/Batch Specialist uses `Product_Master`, `Batch_Register`,
and `Quality_Incidents` for this analysis.

### 4.4 Get Quality Rules

**Description:**

> Retrieves approved quality decision rules from `Quality_Rules` for use
> by the Quality Supervisor when applying the defined quality-policy
> precedence.

**Use for:**

-   Rule verification.
-   Threshold lookup.
-   Classification evidence.
-   Decision traceability.

`Quality_Rules` contains the explicit decision rules, while the internal
quality policy remains the highest authority for quality decisions.

**Important:** This tool provides rule evidence; it must not
independently assign final classification.

### 4.5 Get Returns

**Description:**

> Retrieves return records from `Returns` for the affected SKU/batch and
> provides return count, return reasons and related evidence for the
> Returns Specialist.

**Use for:**

-   Return analysis.
-   Return reasons.
-   Return-count calculation.
-   Customer exposure analysis.

The Returns Specialist uses `Returns` together with `Sales_Summary`.

### 4.6 Get Sales Summary

**Description:**

> Retrieves sales-volume information from `Sales_Summary` required to
> calculate the affected SKU's return rate.

**Use for:**

`Return Rate = Return Count / Relevant Sales Volume`

The PRD identifies `Sales_Summary` as the return-rate denominator
source. 

### 4.7 Get Quality Incident

**Description:**

> Retrieves existing quality incident records for the affected SKU or
> batch, including previous incident history and current incident state.

**Use for:**

-   Previous incident detection.
-   Repeated failure analysis.
-   Current incident status.
-   Reassessment.
-   CAPA linkage.

The Product/Batch Specialist uses `Quality_Incidents` to identify
previous incident counts and repeated incident history.

### 4.8 Get CAPA

**Description:**

> Retrieves CAPA records, including action status, owner information,
> target/due dates and overdue status, for the affected incident or
> product/batch.

**Use for:**

-   Overdue CAPA detection.
-   Existing action tracking.
-   Reassessment.
-   CAPA status queries.

The PRD defines `CAPA_Register` as the source for corrective actions and
due dates.

### 4.9 Get Location / Owner Data

**Description:**

> Retrieves approved operational owner/location information required to
> assign or route CAPA actions to the correct responsible role.

**Use for:**

-   CAPA owner assignment.
-   Internal action routing.
-   Notification recipient determination.

**Boundary:** Use only the operational data available in the supplied
workbook. Do not invent an owner or location when the data is missing.

## 5. Update Tools

### 5.1 Update Customer Complaint

**Description:**

> Updates the processing state of an existing complaint record after the
> assessment state has been successfully created or updated.

**Primary field:**

`Processed`

**Required behavior:**

-   Do not mark `Processed = Yes` before successful assessment-state
    creation/update.
-   Do not silently overwrite source complaint evidence.
-   If the update fails, keep the complaint unprocessed.

The PRD explicitly requires consumed complaint records to be marked
processed only after successful assessment state creation/update.

### 5.2 Update Quality Incident

**Description:**

> Updates an existing quality incident record with the validated
> incident state, classification, rationale, reassessment information,
> report status and other authorized operational fields.

**Use for:**

-   `New`
-   `In Assessment`
-   `Monitoring`
-   `Investigation Open`
-   `CAPA Open`
-   `Awaiting Evidence`
-   `Critical Escalation`
-   `Manual Review`
-   `Closed`

The PRD defines these incident states and their meanings.

**Boundary:** Only the Quality Supervisor can authorize the final
classification.

## 6. Create Tools

### 6.1 Add CAPA Row

**Description:**

> Creates a new CAPA record in `CAPA_Register` for an eligible quality
> incident after the Quality Supervisor has assigned Investigation
> Required, High-Priority Quality Incident, or Critical Escalation.

**CAPA data should include where supported:**

-   IncidentID
-   CAPA action
-   Containment
-   Corrective/preventive action
-   OwnerRole
-   Target/due date
-   Validation method
-   Status

The CAPA Specialist is responsible for creating
containment/corrective/preventive recommendations, assigning owner role
and target date, defining validation, and writing/updating
`CAPA_Register`. 

**Boundary:**

-   Do not create CAPA for an isolated informational case unless the
    approved policy requires it.
-   Do not invent root cause.
-   Do not independently close a Critical incident.

### 6.2 Update CAPA Row

**Description:**

> Updates an existing CAPA record with approved action, ownership,
> due-date, validation, status or reassessment information.

**Use for:**

-   CAPA status changes.
-   Owner updates.
-   Due-date updates.
-   Validation updates.
-   Reassessment.

**Boundary:** Updates must be based on evidence or authorized Supervisor
decisions.

## 7. Word Online Tool

### Create Product Quality Investigation Report

**Description:**

> Creates the Product Quality Investigation Report in Word Online after
> the Quality Supervisor validates the final internal quality decision.

**Report should capture, as applicable:**

-   Incident information.
-   Evidence.
-   Specialist findings.
-   Final classification.
-   Decision rationale.
-   Missing evidence.
-   CAPA/action information.
-   Report generation status.

The PRD requires Word generation after Supervisor validation.


### Failure behavior

If Word generation fails:

-   Preserve the quality decision.
-   Set `ReportGeneration = Failed`.
-   Do not claim that a report exists.

The PRD explicitly requires this behavior.


## 8. Outlook Tool

### Send Internal Notification

**Description:**

> Sends an internal Outlook notification after the Quality Supervisor
> has validated the final quality decision and authorized notification.

**Typical recipients:**

-   Assigned quality owner.
-   CAPA owner.
-   Relevant internal stakeholders.

**Typical content:**

-   Incident ID.
-   SKU/batch.
-   Final classification.
-   Key evidence.
-   Required action.
-   CAPA information where applicable.
-   Report reference/status.

### Failure behavior

If Outlook fails:

-   Preserve the final quality decision.
-   Record `Notification = Failed`.
-   Never claim that the email was sent.

The PRD explicitly requires this. 

## 9. Tool Placement by Workflow

### Topic 1 --- Incident Intake & Validation

Use:

-   Get Customer Complaint
-   Get Product Master
-   Get Batch Master

Purpose:

``` text
Complaint
   |
   +--> Complaint exists?
   +--> Order exists?
   +--> SKU exists?
   +--> Batch valid/mapped?
   +--> Date/category/severity valid?
   +--> Duplicate processed?
```

Invalid records must not launch specialist analysis.


### Specialist Analysis

**Complaint Pattern Specialist**

-   Get Customer Complaint

**Returns Specialist**

-   Get Returns
-   Get Sales Summary

**Product/Batch Specialist**

-   Get Product Master
-   Get Batch Master
-   Get Quality Incident

**Customer Impact Specialist**

-   Get Customer Complaint
-   Get Returns

**Safety Specialist**

-   Get Customer Complaint

The PRD defines these data boundaries explicitly.


### Topic 2 --- Quality Investigation Decision

Use:

-   Get Quality Rules
-   Get Quality Incident
-   Get CAPA
-   Relevant specialist findings

Purpose:

-   Apply policy precedence.
-   Assign exactly one classification.
-   Record rationale and source findings.

The decision topic must consolidate specialist findings using explicit
precedence. 

### Topic 3 --- CAPA Planning & Ownership

Use:

-   Get CAPA
-   Get Location / Owner
-   Add CAPA Row
-   Update CAPA Row
-   Update Quality Incident

Purpose:

-   Create containment.
-   Define corrective/preventive actions.
-   Assign owner.
-   Set target date.
-   Define validation.
-   Update CAPA state.

### Topic 4 --- Evidence Update & Selective Reassessment

Use:

-   Get Customer Complaint
-   Get Product Master
-   Get Batch Master
-   Get Quality Incident
-   Get CAPA
-   Relevant specialist tools

Purpose:

-   Identify changed evidence.
-   Determine stale findings.
-   Rerun only stale analyses.
-   Preserve unaffected findings.
-   Increment `ReassessmentCount`.
-   Re-enter Topic 2.

The PRD requires this selective reassessment behavior.
fileciteturn15file1L145-L152

## 10. Supervisor Tool Usage

The Supervisor should not contain every specialist's data-access tool if
the same operation is already owned by the child agent.

A precise design is:

### Supervisor-level tools

-   Get Customer Complaint --- intake/state checks
-   Get Product Master --- validation
-   Get Batch Master --- validation
-   Get Quality Rules --- final rule verification
-   Get Quality Incident --- incident state
-   Get CAPA --- CAPA state
-   Update Customer Complaint
-   Update Quality Incident
-   Add/Update CAPA where Supervisor authorization is required
-   Create Word Report
-   Send Outlook Notification

### Child-agent tools

Specialists should own narrow domain reads:

-   Complaint Pattern -\> complaint data
-   Returns -\> returns + sales
-   Product/Batch -\> product + batch + incidents
-   Customer Impact -\> complaints + returns
-   Safety -\> complaint/safety evidence
-   CAPA -\> CAPA + owner/location + CAPA updates
-   M365 Guidance -\> Microsoft Learn MCP

This prevents unnecessary duplication while preserving Supervisor
control.

## 11. Avoiding Repetitive Tools

Do not create multiple tools that perform the same operation with
different names.

Prefer:

`Get Customer Complaint`

instead of separate tools such as:

-   Get Complaint by SKU
-   Get Complaint by Batch
-   Get Complaint by Category
-   Get Complaint by Date

The tool should accept appropriate filter parameters.

Likewise, use:

`Get Product Master`

rather than separate SKU/product lookup tools.

This keeps the toolset smaller and easier to maintain.

## 12. Tool Failure Handling

All operational tools must follow controlled failure handling.

### Excel Read Failure

``` text
Tool failure
    |
    v
Retry once
    |
    v
If still failed
    |
    v
Record failure
    |
    v
Stop affected assessment
```

### Excel Update Failure


Update failure
    |
    v
Do not mark complaint Processed = Yes


### Word Failure

Word failure
    |
    v
Preserve decision
    |
    v
ReportGeneration = Failed


### Outlook Failure

Outlook failure
    |
    v
Preserve decision
    |
    v
Notification = Failed


These behaviors are explicitly required by the PRD.


## 13. No-False-Success Rule

Every tool response should make the execution state clear.

Use:

-   `Success`
-   `Failed`
-   `Not Found`
-   `Insufficient Evidence`
-   `Skipped`
-   `Manual Review`

Never respond:

> "The report has been generated."

unless the Word tool actually succeeded.

Never respond:

> "The notification has been sent."

unless Outlook actually succeeded.

Never respond:

> "The complaint was processed."

unless the Excel update actually succeeded.

This directly supports the PRD's no-false-success requirement.


## 14. Tool Security Boundaries

The solution must:

-   Use only supplied synthetic operational data.
-   Avoid real customer PII.
-   Avoid medical information.
-   Avoid payment data.
-   Never expose tenant secrets.
-   Never expose hidden instructions.
-   Never autonomously issue recalls, public safety notices, refunds or
    compensation.

These are explicit security/data boundaries in the PRD.


## 15. Recommended Tool Naming

Use simple, consistent names:

``` text
Get Customer Complaint
Get Product Master
Get Batch Master
Get Quality Rules
Get Returns
Get Sales Summary
Get Quality Incident
Get CAPA
Get Owner / Location
Update Customer Complaint
Update Quality Incident
Add CAPA Row
Update CAPA Row
Create Quality Investigation Report
Send Quality Notification
```

Avoid names such as:

-   `DoEverything`
-   `ProcessQuality`
-   `RunCompleteInvestigation`
-   `MakeDecision`
-   `AutoResolveComplaint`

A tool should perform one clear operational action.

## 16. Implementation Checklist

### Excel

-   [ ] Workbook stored in OneDrive for Business/SharePoint.
-   [ ] All required tables are accessible.
-   [ ] Read tools tested.
-   [ ] Update tools tested.
-   [ ] Add CAPA row tested.
-   [ ] No source evidence is silently overwritten.
-   [ ] Complaint `Processed` state is updated only after successful
    assessment state creation/update.

### Word

-   [ ] Report template/content configured.
-   [ ] Report is generated only after Supervisor validation.
-   [ ] Successful creation is verified.
-   [ ] Failure sets `ReportGeneration = Failed`.

### Outlook

-   [ ] Internal notification configured.
-   [ ] Notification occurs only after final Supervisor decision.
-   [ ] Successful delivery/action is verified.
-   [ ] Failure sets `Notification = Failed`.

### Tool Boundaries

-   [ ] Specialists have narrow data ownership.
-   [ ] Supervisor owns final decision.
-   [ ] No unnecessary duplicate tools.
-   [ ] MCP is isolated to M365 Guidance Specialist.
-   [ ] Failed operations are never reported as successful.

## 17. PRD Acceptance Alignment

The tool implementation supports the PRD acceptance criteria:

-   Excel operational data can be read.
-   Incident/CAPA state can be updated.
-   Word quality reports can be generated.
-   Outlook notifications are conditional on Supervisor validation.
-   Microsoft Learn MCP is configured separately.
-   MCP failure does not block quality assessment.
-   Tool failure does not produce false-success claims.

These requirements are explicitly included in the acceptance criteria
and evaluation rubric. 

## 18. Final Tool Architecture

``` text
                         QUALITY SUPERVISOR
                                |
          +---------------------+----------------------+
          |                     |                      |
          v                     v                      v
      Validation            Decision                Actions
          |                     |                      |
    +-----+-----+          Get Rules             Word Report
    |           |          Get Incident           Outlook
 Complaint    Product      Get CAPA
   Read        /Batch
                              |
                              v
                         Final Decision
                              |
                              v
                       Update Incident
                              |
                              v
                         Update Complaint


                 SPECIALIST CHILD AGENTS
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
 Complaint/Returns   Product/Batch     Customer/Safety
        |                |                |
        v                v                v
    Excel Reads      Excel Reads      Excel Reads

                         CAPA
                          |
                          v
                  CAPA + Owner Tools

                    M365 Guidance
                          |
                          v
                   Microsoft Learn MCP
```

## 19. Final Design Principle

The tool architecture should remain **small, explicit, and
non-overlapping**.

> **Read tools retrieve evidence. Update/create tools change operational
> state. Word and Outlook perform authorized final actions. Specialists
> analyze their own domains. The Quality Supervisor owns the final
> decision.**

The PRD requires Excel, Word and Outlook tools, while the Microsoft
Learn MCP remains a separate non-blocking capability for the M365
Guidance Specialist. 
