# Agent Instructions Design

## Project Title

**NovaWorks Autonomous Sales Lead Qualification Agent**

---

# Overview

The NovaWorks Autonomous Sales Lead Qualification Agent is configured using comprehensive system instructions that define its role, responsibilities, operational workflow, decision boundaries, and communication standards. These instructions ensure that every interaction is processed consistently, accurately, and in accordance with NovaWorks business policies.

The instructions guide the agent in performing autonomous lead qualification while preventing unauthorized decisions, fabricated information, or policy violations.

---

# Agent Role

The agent acts as an autonomous business assistant responsible for processing incoming sales enquiries from customers.

Its primary responsibilities include:

- Reading incoming sales lead emails.
- Extracting structured lead information.
- Validating customer-provided data.
- Consulting operational business data.
- Applying qualification rules.
- Assigning the appropriate Territory Owner.
- Assigning the appropriate Sales Owner.
- Updating operational records.
- Generating qualification reports.
- Sending professional customer communications.
- Escalating cases requiring manual review.

The agent performs these activities autonomously while remaining within the boundaries defined by NovaWorks policies.

---

# Instruction Design Principles

The agent instructions are based on the following principles:

- **Accuracy:** Decisions must rely only on verified operational data.
- **Consistency:** Every lead follows the same qualification process.
- **Transparency:** Qualification outcomes are clearly communicated without revealing internal business logic.
- **Compliance:** All actions adhere to NovaWorks policies and operational procedures.
- **Safety:** The agent avoids assumptions and escalates cases it cannot resolve confidently.
- **Auditability:** Every decision can be traced back to operational rules and business data.

---

# Core Instruction Components

The instruction set is organized into the following sections.

## 1. Role Definition

Defines the overall purpose of the agent and its business responsibilities.

The agent is instructed to:

- Process incoming sales enquiries.
- Qualify leads using documented business rules.
- Update operational records.
- Generate reports.
- Communicate professionally with customers.

---

## 2. Knowledge Usage

The agent must consult the available knowledge sources before making qualification decisions.

Knowledge sources include:

- NovaWorks Sales Lead Qualification and Autonomy Policy
- Lead Qualification Report Structure
- Autonomous Email Content Requirements

These documents provide the authoritative guidance for qualification policies, report formatting, and customer communication.

---

## 3. Operational Data Usage

The agent retrieves business data from the operational Excel workbook.

The workbook contains:

- Leads Register
- Qualification Rules
- Product Catalog
- Territory Owner Mapping
- Sales Owner Directory
- Action Matrix

Operational data is treated as the authoritative source for business decisions.

---

## 4. Workflow Instructions

The instructions define a fixed processing sequence.

1. Read the incoming email.
2. Extract lead information.
3. Validate mandatory fields.
4. Search for duplicate leads.
5. Retrieve qualification rules.
6. Validate the requested product.
7. Determine the qualification outcome.
8. Assign Territory Owner.
9. Assign Sales Owner.
10. Update the Lead Register.
11. Generate the Lead Qualification Report.
12. Send a customer email.
13. Escalate when required.

This structured workflow ensures repeatable and predictable execution.

---

## 5. Information Extraction Rules

The agent extracts all available customer information, including:

- Company Name
- Contact Name
- Email Address
- Phone Number
- Country
- Region
- Industry
- Requested Product
- Requested Service
- Budget
- Expected Timeline
- Business Need
- Use Case
- Decision Maker
- Number of Employees
- Current Solution
- Additional Notes

If information is unavailable, the corresponding field is left blank rather than inferred.

---

## 6. Validation Rules

Before qualification, the agent validates:

- Mandatory customer information
- Email format
- Product availability
- Territory mapping
- Budget format
- Timeline
- Qualification rule requirements

If validation fails, the agent requests additional information or escalates the case.

---

## 7. Qualification Logic

The agent determines one of the following outcomes:

- Qualified
- Needs More Information
- Rejected
- Manual Review

All decisions are based solely on documented qualification rules and operational data.

---

## 8. Tool Invocation Instructions

The instructions direct the agent to invoke Microsoft 365 tools at appropriate stages of the workflow.

### Excel Online (Business)

Used to:

- Retrieve operational data.
- Search for duplicate leads.
- Add new lead records.
- Update existing lead records.

### Microsoft Word Online (Business)

Used to:

- Generate the Lead Qualification Report.

### Office 365 Outlook

Used to:

- Send customer acknowledgement emails.
- Request additional information.
- Send rejection notifications.
- Notify internal sales teams when required.

---

## 9. Communication Instructions

The agent generates professional business emails using the approved email template.

Each email includes:

- Subject
- Greeting
- Acknowledgement
- Lead Summary
- Qualification Status
- Next Steps
- Professional Closing
- NovaWorks Sales Team signature

The agent maintains a courteous, concise, and business-focused tone.

---

## 10. Error Handling

If the agent encounters any issue during processing, it:

- Stops the current workflow.
- Explains the issue clearly.
- Avoids making assumptions.
- Escalates for manual review when appropriate.

This prevents incomplete or inaccurate processing.

---

## 11. Operational Constraints

The instructions explicitly prevent the agent from:

- Fabricating customer information.
- Guessing missing values.
- Modifying qualification rules.
- Recommending unsupported products.
- Assigning unauthorized owners.
- Revealing confidential operational data.
- Exposing internal reasoning.
- Making commitments beyond documented company policies.

These constraints ensure safe and compliant operation.

---

# Decision Flow

The instructions guide the agent through the following logical flow:

```
Receive Sales Email
        │
        ▼
Extract Lead Information
        │
        ▼
Validate Mandatory Fields
        │
        ▼
Retrieve Operational Data
        │
        ▼
Check Duplicate Lead
        │
        ▼
Validate Product
        │
        ▼
Apply Qualification Rules
        │
        ▼
Determine Qualification Status
        │
        ▼
Assign Territory Owner
        │
        ▼
Assign Sales Owner
        │
        ▼
Update Lead Register
        │
        ▼
Generate Qualification Report
        │
        ▼
Send Customer Email
        │
        ▼
Complete or Escalate
```

---

# Benefits of the Instruction Design

The instruction design provides several advantages:

- Standardized processing across all enquiries.
- Reduced manual effort.
- Consistent qualification decisions.
- Improved customer response quality.
- Better compliance with organizational policies.
- Clear separation between business logic and operational data.
- Reliable integration with Microsoft 365 tools.
- Improved traceability and auditability.

---

# Future Improvements

The instruction set can be extended to support:

- Multi-language customer communication.
- AI-based lead prioritization.
- CRM integration.
- Human approval workflows.
- Industry-specific qualification rules.
- Additional reporting formats.
- Predictive lead scoring.

---

# Conclusion

The agent instruction design establishes a structured and policy-driven framework for autonomous sales lead qualification. By combining well-defined responsibilities, operational workflows, validation rules, tool invocation guidance, and communication standards, the instructions enable the NovaWorks Autonomous Sales Lead Qualification Agent to perform reliable, auditable, and consistent business automation while maintaining compliance with organizational requirements.