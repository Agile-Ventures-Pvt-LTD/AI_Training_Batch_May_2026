# Tool Implementation

## 1. Excel Online (Business)

### Purpose

Excel Online (Business) is used for operational quality data and incident/CAPA state management.

### Workbook

**File:** `Sleepsia_CAP001_Quality_Capstone_Data.xlsx`

**Storage:** OneDrive for Business

### Tables

The workbook contains:

- `Product_Master`
- `Batch_Register`
- `Customer_Complaints`
- `Sales_Summary`
- `Returns`
- `Quality_Incidents`
- `CAPA_Register`
- `Owners`
- `Quality_Rules`
- `Test_Scenarios`

### Configuration

The Supervisor/specialist agents use Excel tools for:

- Complaint lookup
- Product/SKU validation
- Batch validation
- Return analysis
- Sales/return-rate calculation
- Previous incident lookup
- Owner lookup
- CAPA Register creation/update


## 2. Word Online (Business)

### Purpose

Word is used to generate the formal Quality Investigation / CAPA report after the Supervisor has completed the quality decision and CAPA planning.

### Report Content

The generated report contains:

- Incident ID
- SKU
- Batch ID
- Final classification
- Decision rationale
- Specialist findings
- Containment action
- Corrective action
- Preventive action
- Owner
- Target date
- Validation method

### Configuration

**Connector:** Word Online (Business)


## 3. Office 365 Outlook

### Purpose

Outlook is used to notify the assigned quality owner after Supervisor validation and CAPA ownership are completed.

### Notification Content

The notification contains:

- Incident ID
- Final classification
- Key findings
- CAPA requirement
- Owner
- Target date
- Required action

### Configuration

**Connector:** Office 365 Outlook

**Recipient:** Owner email retrieved from the `Owners` table.


## 4. Tool Boundaries

| Tool | Responsibility | Decision Authority |
|---|---|---|
| Excel | Read operational data and update incident/CAPA state | No |
| Word | Generate quality/CAPA report | No |
| Outlook | Send validated owner notification | No |
| Quality Supervisor | Final quality decision and authorization | Yes |

The Supervisor authorizes Word generation and Outlook notification. Excel provides operational evidence and state updates. The tools do not independently determine quality severity. 


## 5. Tool Test Evidence

| Test | Expected Result | Status |
|---|---|---|
| Excel table retrieval | Operational table data returned | [PASS] |
| Excel CAPA update | CAPA state successfully updated | [PASS] |
| Owner lookup | OwnerRole returns owner information | [PASS] |
| Word report generation | Required report sections generated | [PASS] |
| Word failure | No false success claim | [PASS] |
| Outlook notification | Owner notification sent | [PASS] |
| Outlook failure | Decision preserved and failure recorded | [PASS] |

