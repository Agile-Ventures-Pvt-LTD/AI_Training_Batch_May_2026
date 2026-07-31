# 🚀 NovaWorks Autonomous Sales Lead Qualification Agent

> **Project ID:** P2-003  
> **Platform:** Microsoft Copilot Studio  
> **Automation:** Outlook Event Trigger + Microsoft 365 Connectors  
> **Storage:** OneDrive for Business  
> **Author:** Ashish Sinha

---

# 📖 Project Overview

The **NovaWorks Autonomous Sales Lead Qualification Agent** is an enterprise-grade AI solution built using **Microsoft Copilot Studio**.

The agent automatically processes incoming sales inquiry emails, extracts lead information, validates business data, qualifies opportunities, assigns ownership, updates operational records, generates qualification reports, and communicates with customers and internal sales teams without manual intervention.

The solution combines AI-powered reasoning with Microsoft 365 services to automate the complete lead qualification lifecycle.

---

# 🎯 Business Problem

Organizations receive hundreds of sales inquiry emails every day.

Manual processing results in:

- Slow response times
- Duplicate lead creation
- Inconsistent qualification
- Human errors
- Delayed sales assignments
- Poor customer experience
- Lack of standardized reporting

NovaWorks required an autonomous AI agent capable of handling these activities while maintaining business consistency.

---

# 💡 Solution

The solution uses **Microsoft Copilot Studio Autonomous Agent** with Microsoft 365 integrations.

The agent automatically:

- Monitors Outlook inbox
- Detects new sales inquiries
- Extracts lead information
- Performs duplicate detection
- Validates products
- Determines sales territory
- Assigns sales owners
- Calculates qualification score
- Determines lead classification
- Updates Excel operational database
- Generates Word qualification reports
- Sends customer acknowledgement emails
- Notifies sales representatives
- Escalates uncertain leads for human review

---

# 🏗 Solution Architecture

```
                    Outlook Email
                          │
                          ▼
            Outlook Event Trigger (V3)
                          │
                          ▼
      Microsoft Copilot Studio Autonomous Agent
                          │
        ┌─────────────────┼──────────────────┐
        │                 │                  │
        ▼                 ▼                  ▼
 Excel Online      Word Online        Office 365 Outlook
 (Business)         (Business)            (Business)
        │                 │                  │
        ▼                 ▼                  ▼
 Lead Register     Qualification       Customer Emails
 Qualification     Reports             Owner Notification
 Territory                              Human Review
 Product Catalog
 Sales Owners
 Action Matrix
```

---

# ⚙ Technology Stack

| Component | Technology |
|------------|------------|
| AI Platform | Microsoft Copilot Studio |
| LLM | GPT-5.5 Chat |
| Automation | Microsoft Power Automate Trigger |
| Email | Office 365 Outlook |
| Database | Excel Online (Business) |
| Document Generation | Word Online (Business) |
| Storage | OneDrive for Business |
| Reports | Microsoft Word |
| Authentication | Microsoft Entra ID |

---

# 📁 Project Structure

```
P2-003_Autonomous_Sales_Lead_Qualification/

│
├── README.md
├── AGENT_INSTRUCTIONS.md
├── ARCHITECTURE.md
├── TOOLS.md
├── WORKFLOW.md
├── BUSINESS_RULES.md
├── TRIGGERS.md
├── TESTING.md
├── DEPLOYMENT.md
├── TROUBLESHOOTING.md
├── CHANGELOG.md
│
├── Data/
│     └── P2-003_Sales_Lead_Operational_Data.xlsx
│
├── Templates/
│     └──Lead_Qualification_Report_Required_Structure.docx
│
├── Reports/
│
├── Documentation/
│     ├── NovaWorks Policy.docx
│     ├── Autonomous_Email_Content_Requirements.txt
│     └── Dataset_Manifest.md
│
└── TestData/
      ├── Sample_Incoming_Lead_Emails.txt
      └── Test_Cases.xlsx
```

---

# 📂 Folder Purpose

## Data

Stores the operational Excel workbook used by the autonomous agent.

Contains:

- Lead Register
- Qualification Rules
- Product Catalog
- Territory Mapping
- Sales Owners
- Action Matrix

---

## Templates

Contains Microsoft Word templates used during report generation.

The agent uses the official report template to create standardized qualification reports.

---

## Reports

Stores generated Lead Qualification Reports.

Example:

```
Reports/

LEAD-00001.docx

LEAD-00002.docx
```

---

## Documentation

Contains project documentation including:

- Business policies
- Email content requirements
- Dataset descriptions

Used as implementation reference.

---

## TestData

Contains sample emails and execution logs used for testing the solution.

---

# 🤖 Agent Capabilities

The agent can automatically:

✅ Read Outlook emails

✅ Extract customer information

✅ Normalize business data

✅ Detect duplicate leads

✅ Validate products

✅ Calculate qualification score

✅ Assign sales territory

✅ Assign sales owner

✅ Generate Word report

✅ Update Excel database

✅ Send acknowledgement email

✅ Notify sales owner

✅ Escalate uncertain cases

---

# 📊 Operational Excel Tables

The operational workbook contains:

| Table | Purpose |
|---------|----------|
| LeadsRegisterTable | Stores all processed leads |
| QualificationRulesTable | Qualification scoring |
| ProductCatalogTable | Product validation |
| TerritoryOwnersTable | Country mapping |
| SalesOwnersTable | Owner assignment |
| ActionMatrixTable | Business decision rules |

---

# 🔧 Configured Tools

## Excel Online (Business)

- Read_Lead_Register
- Create_Lead_Record
- Update_Lead_Record
- Read_Qualification_Rules
- Read_Product_Catalog
- Read_Territory_Owners
- Read_Sales_Owners
- Read_Action_Matrix

---

## Word Online (Business)

Generate_Qualification_Report

---

## Office 365 Outlook

- Send_Acknowledgement_Email
- Send_Missing_Information_Email
- Notify_Sales_Owner
- Notify_Sales_Ops

---

# ⚡ Trigger

The solution starts automatically whenever Outlook receives an email matching:

```
[P2-003 LEAD]
```

No manual intervention is required.

---

# 🔄 Processing Workflow

```
Receive Email

↓

Extract Information

↓

Duplicate Detection

↓

Product Validation

↓

Qualification Rules

↓

Territory Mapping

↓

Owner Assignment

↓

Calculate Score

↓

Determine Classification

↓

Create/Update Lead

↓

Generate Word Report

↓

Send Outlook Emails
```

---

# 📄 Report Generation

The agent:

1. Reads the official Word template

2. Replaces placeholders

3. Generates a Lead Qualification Report

4. Saves the report into the Reports folder

5. Updates the Lead Register with the report path

---

# 📧 Automated Emails

The agent automatically sends:

### Customer

- Acknowledgement
- Missing Information Request

### Internal

- Sales Owner Notification
- Sales Operations Review

---

# 🔒 Security

The solution uses:

- Microsoft Entra ID Authentication
- OneDrive for Business
- Office 365 Connectors
- Microsoft Copilot Studio Permissions

No external APIs are required.

---

# 🧪 Testing

The project includes:

- Sample Lead Emails
- Test Cases
- Expected Results
- Execution Logs

Testing scenarios include:

- Qualified Lead
- Duplicate Lead
- Missing Information
- Unknown Product
- Unknown Territory
- Human Review
- High Priority Lead

---

# 🚀 Deployment

Deployment steps:

1. Import project assets

2. Create OneDrive folder structure

3. Upload operational workbook

4. Upload Word template

5. Configure Outlook trigger

6. Configure connectors

7. Publish Agent

8. Execute test cases

---

# 📈 Future Enhancements

Possible future improvements:

- CRM Integration (Dynamics 365 / Salesforce)
- SharePoint document storage
- Teams notifications
- Power BI dashboards
- Azure AI Document Intelligence
- Multi-language lead processing
- Sentiment analysis
- Lead prioritization using AI
- Dataverse migration
- Approval workflows

---

# 📚 Documentation

| File | Description |
|------|-------------|
| AGENT_INSTRUCTIONS.md | Complete AI instructions |
| ARCHITECTURE.md | Solution architecture |
| WORKFLOW.md | Business workflow |
| TOOLS.md | Connector documentation |
| BUSINESS_RULES.md | Qualification logic |
| TRIGGERS.md | Outlook trigger configuration |
| TESTING.md | Test execution guide |
| DEPLOYMENT.md | Deployment instructions |
| TROUBLESHOOTING.md | Common issues |
| CHANGELOG.md | Version history |

---

# 👨‍💻 Author

Ashish Sinha

Microsoft Copilot Studio Autonomous Agent Project

Project ID: P2-003
