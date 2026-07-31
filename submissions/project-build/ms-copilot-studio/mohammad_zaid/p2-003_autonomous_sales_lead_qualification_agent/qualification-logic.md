# Qualification Logic

# Project Information

| Property       | Value                                              |
| -------------- | -------------------------------------------------- |
| Project        | P2-003 – NovaWorks Sales Lead Qualification Agent |
| Platform       | Microsoft Copilot Studio                           |
| Component      | Qualification Logic                                |
| Execution Mode | Generative Orchestration                           |

---

# Purpose

The Qualification Logic defines the business decision framework used by the NovaWorks Sales Lead Qualification Agent to evaluate incoming sales enquiries.

The objective is to ensure that every lead is processed consistently, duplicate records are prevented, qualification decisions are standardized, and appropriate business actions are taken based on the available information.

The logic is executed after lead information has been extracted from the incoming email and operational reference data has been retrieved from the operational workbook.

---

# Qualification Workflow

The agent evaluates every incoming lead using the following sequence.

```
Incoming Email
        │
        ▼
Extract Lead Information
        │
        ▼
Validate Required Fields
        │
        ▼
Duplicate Detection
        │
        ▼
Retrieve Qualification Rules
        │
        ▼
Evaluate Business Criteria
        │
        ▼
Calculate Qualification Score
        │
        ▼
Determine Classification
        │
        ▼
Assign Sales Owner
        │
        ▼
Determine Next Action
```

---

# Lead Information Extraction

The agent attempts to extract all relevant business information from the incoming email and any attached documents.

Typical information includes:

- Contact Name
- Email Address
- Company Name
- Job Title
- Country
- Industry
- Company Size
- Product Interest
- Estimated Budget
- Purchase Timeline
- Decision Role
- Lead Source
- Inquiry Type
- Business Need

If information is unavailable, the field remains unpopulated and is treated according to the validation rules.

---

# Validation Logic

Before qualification begins, the agent validates the extracted information.

The validation process ensures:

- Mandatory business fields are identified.
- Missing information is detected.
- Invalid or unsupported values are not fabricated.
- Processing follows organizational policies.

If required information is incomplete, the agent may request additional information or escalate the lead for manual review depending on the business context.

---

# Duplicate Detection

Duplicate detection is performed before any operational record is created.

The objective is to prevent multiple records for the same sales opportunity.

The agent compares the incoming lead against the existing Lead Register using available business identifiers and operational reference data.

If an existing lead is identified:

- The existing operational record is updated.
- A new lead record is not created.

If no existing lead is found:

- The lead continues through the qualification process.
- A new operational record is created after qualification.

---

# Qualification Evaluation

The agent evaluates each lead using the operational qualification rules stored within the project dataset.

Typical evaluation criteria include:

- Product suitability
- Business need
- Estimated budget
- Purchase timeline
- Decision-maker involvement
- Territory availability
- Industry relevance
- Organizational fit

These criteria collectively determine the overall qualification outcome.

---

# Qualification Score

The qualification score represents the overall assessment of the lead.

The score is calculated using the qualification rules and reference data provided in the operational workbook.

The score is used to support downstream business decisions, including:

- Lead classification
- Priority determination
- Sales owner assignment
- Recommended next action

The exact scoring values are maintained within the project dataset and are not hardcoded into the agent instructions.

---

# Lead Classification

Based on the qualification evaluation, the agent assigns an appropriate lead classification.

The classification reflects the overall business potential of the opportunity and supports consistent downstream processing.

The classification influences:

- Recommended follow-up action
- Internal notification requirements
- Sales owner assignment
- Operational reporting

The classification logic follows the qualification rules defined in the operational workbook.

---

# Priority Determination

The agent determines the operational priority of the lead based on the qualification outcome and available business information.

Priority assists the organization in identifying which opportunities require more immediate attention.

The priority decision considers:

- Qualification outcome
- Business need
- Purchase timeline
- Estimated budget
- Organizational importance

---

# Sales Owner Assignment

Following qualification, the agent assigns the lead to an appropriate sales owner.

Assignment considers operational reference information such as:

- Territory
- Product responsibility
- Sales owner availability
- Capacity information

If an appropriate owner cannot be identified, the lead is escalated for manual review.

---

# Business Overrides

Certain situations require business overrides rather than standard automated processing.

Examples include:

- Missing mandatory information
- Conflicting operational data
- Unrecognized territory
- Unable to determine sales owner
- Insufficient qualification information

In these situations, the agent avoids unsupported assumptions and follows the configured escalation process.

---

# Decision Outcomes

After qualification, the agent determines the appropriate operational outcome.

Possible outcomes include:

- Create new lead record
- Update existing lead record
- Generate Lead Qualification Report
- Send customer acknowledgement
- Request additional information
- Notify internal sales owner
- Escalate for manual review

The selected outcome depends on the qualification result and operational rules.

---

# Design Principles

The qualification logic was designed according to the following principles:

- Consistent business decisions
- Policy-driven evaluation
- No fabricated information
- Duplicate prevention
- Operational transparency
- Human escalation when required
- Reusable business logic
- Separation of business rules from implementation

---

# Assumptions

The qualification logic assumes:

- Operational reference data is available.
- Qualification rules remain current.
- Outlook trigger executes successfully.
- Required Microsoft 365 connectors are authenticated.
- Incoming email contains sufficient information for evaluation.

---

# Limitations

The qualification outcome depends on the quality and completeness of the incoming information.

If required business information is unavailable or ambiguous, the agent may be unable to determine an appropriate qualification outcome without manual review.

Connector availability, operational workbook access, and Microsoft Copilot Studio runtime behaviour may also influence execution.

---

# Conclusion

The Qualification Logic provides a structured and policy-driven framework for evaluating inbound sales leads. By combining operational reference data, duplicate detection, validation, qualification rules, and business decision logic, the agent delivers consistent lead assessments while maintaining operational accuracy and supporting autonomous workflow execution within Microsoft Copilot Studio.

renshots
