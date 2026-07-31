# 📈 Qualification Logic

## 🚀 Project Information

| Property | Details |
|----------|---------|
| **Project ID** | P2-003 – Autonomous Sales Lead Qualification Agent |
| **Participant** | Vikash Kumar |
| **Platform** | Microsoft Copilot Studio |
| **Decision Engine** | Generative AI Orchestration |
| **Reference Data Source** | Excel Online (Business) |

---

# 🎯 Purpose

The qualification logic determines whether an incoming email represents a genuine sales opportunity and identifies the appropriate business action.

Rather than relying solely on natural language understanding, the agent combines AI reasoning with operational reference data stored in Microsoft Excel. This ensures that business decisions are consistent, traceable, and aligned with organizational policies.

---

# 🔄 Qualification Workflow

Every incoming email follows the same qualification lifecycle.

```text
Receive Email
      │
      ▼
Validate Trigger
      │
      ▼
Determine Sales Intent
      │
      ▼
Extract Lead Information
      │
      ▼
Normalize Data
      │
      ▼
Read Operational Reference Tables
      │
      ▼
Duplicate Detection
      │
      ▼
Qualification Assessment
      │
      ▼
Assign Territory
      │
      ▼
Assign Sales Owner
      │
      ▼
Determine Business Action
      │
      ▼
Create / Update Lead
      │
      ▼
Generate Report
      │
      ▼
Send Email
```

---

# 📥 Step 1 – Sales Lead Validation

The first decision is whether the incoming email is a genuine sales enquiry.

The agent considers:

- Commercial buying intent
- Interest in NovaWorks products or services
- Business requirements
- Opportunity details
- Contact information

The following requests are **not** treated as sales leads:

- Technical support
- Job applications
- Internship requests
- Vendor proposals
- Academic research
- Competitor enquiries
- Spam
- General information requests

If the email is not identified as a sales lead, no operational records are created.

---

# 📑 Step 2 – Information Extraction

The agent extracts all available business information from the email.

### Contact

- Contact Name
- Email Address
- Job Title
- Decision Role

### Organization

- Company Name
- Country
- Territory
- Industry
- Company Size

### Opportunity

- Product Interest
- Business Need
- Estimated Budget
- Purchase Timeline
- Lead Source

Missing information is retained as **Unknown** rather than inferred.

---

# 🔄 Step 3 – Data Normalization

To ensure consistency across operational records, extracted values are normalized.

Examples include:

| Input | Normalized Value |
|--------|------------------|
| USA | United States |
| U.S. | United States |
| UK | United Kingdom |
| AI ERP | ERP |
| Enterprise Resource Planning | ERP |

The normalization process reduces duplicate records caused by inconsistent terminology.

---

# 📊 Step 4 – Operational Data Retrieval

Before making any business decision, the agent retrieves operational reference data from the Excel workbook.

The following reference tables are used:

| Table | Purpose |
|--------|---------|
| LeadsRegisterTable | Existing leads |
| QualificationRulesTable | Qualification criteria |
| TerritoryOwnersTable | Territory mapping |
| ProductCatalogTable | Product validation |
| SalesOwnersTable | Sales owner assignment |
| ActionMatrixTable | Operational actions |

These tables provide the operational context required for qualification.

---

# 🔍 Step 5 – Duplicate Detection

Duplicate detection is performed before creating any new lead.

The comparison order is:

1. Source Message ID
2. Sender Email
3. Company Name
4. Product Interest

### Duplicate Found

If a duplicate exists:

- Existing lead record is updated.
- No additional lead is created.
- No duplicate report is generated.
- No duplicate acknowledgement email is sent.

### No Duplicate Found

If no existing record is found:

- Continue with qualification.
- Create a new operational lead record.

---

# 📈 Step 6 – Lead Qualification

The agent evaluates the opportunity using the Qualification Rules reference table.

The assessment considers:

- Business need
- Product fit
- Budget availability
- Purchase timeline
- Completeness of information
- Confidence level

The agent combines AI reasoning with operational rules to determine the final qualification outcome.

---

# 🏷️ Step 7 – Lead Classification

Every processed enquiry is assigned one of the following classifications:

| Classification | Description |
|---------------|-------------|
| 🔥 Hot | Strong opportunity requiring immediate follow-up |
| ✅ Qualified | Meets qualification requirements |
| 🌱 Nurture | Requires future engagement |
| 🟡 Low Priority | Valid lead with limited opportunity |
| 📋 Additional Information Required | Missing essential business information |
| 👨‍💼 Human Review Required | AI confidence insufficient |
| 🔁 Duplicate | Existing lead already present |
| ❌ Not a Sales Lead | Does not represent a sales opportunity |

The assigned classification determines subsequent business actions.

---

# 🌍 Step 8 – Territory Assignment

The Territory Owners reference table is used to determine the correct sales region.

Typical mapping includes:

- North America
- Europe
- Asia-Pacific
- Middle East & Africa
- Latin America

This ensures leads are routed to the correct regional sales organization.

---

# 👤 Step 9 – Sales Owner Assignment

Once the territory is identified, the Sales Owners reference table is consulted to assign the responsible sales representative.

The assignment is based on predefined operational mappings rather than AI assumptions.

---

# ⚙️ Step 10 – Operational Action

The Action Matrix reference table determines the next business action.

Examples include:

- Create new lead
- Update existing lead
- Generate qualification report
- Send acknowledgement
- Escalate to human review

The agent follows the action defined by the operational rules.

---

# 👨‍💼 Human Review Logic

Autonomous processing stops and human review is requested when:

- Product cannot be validated.
- Territory cannot be determined.
- Qualification confidence is low.
- Required operational data is unavailable.
- Conflicting information exists.
- Connector execution fails twice.

This prevents unreliable autonomous decisions.

---

# 📄 Report Generation Logic

A Microsoft Word qualification report is generated for valid operational scenarios.

Reports are **not** generated for:

- Duplicate enquiries
- Non-sales enquiries

The report contains:

- Lead summary
- Qualification outcome
- Assigned sales owner
- Recommended next actions

---

# 📧 Customer Communication Logic

Acknowledgement emails are sent only after successful processing.

The response includes:

- Confirmation of receipt
- Next steps
- Appropriate sales contact

The agent never discloses:

- Internal qualification scores
- Confidence values
- Operational rules
- Business reasoning

---

# ⚠️ Exception Handling

The qualification process includes controlled exception handling.

If a connector fails:

1. Retry once.
2. If the retry fails:
   - Stop processing.
   - Record the failure.
   - Escalate for human review.
   - Do not report successful completion.

---

# 🧪 Validation

The qualification logic was validated using multiple scenarios including:

- ✔️ Valid sales lead
- ✔️ Duplicate enquiry
- ✔️ Missing budget
- ✔️ Missing purchase timeline
- ✔️ Unknown product
- ✔️ Unknown territory
- ✔️ Non-sales enquiry
- ✔️ Human review scenario

The results confirmed that the agent consistently followed the defined qualification logic and operational rules.

---

# 🎉 Outcome

The qualification logic combines AI reasoning with operational business rules to produce consistent, explainable, and policy-compliant decisions.

By separating operational reference data from the prompt and using Microsoft 365 connector tools, the solution delivers a maintainable and scalable autonomous lead qualification process.