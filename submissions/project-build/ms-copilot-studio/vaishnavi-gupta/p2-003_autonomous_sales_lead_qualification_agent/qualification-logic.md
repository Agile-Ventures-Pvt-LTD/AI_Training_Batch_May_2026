# Qualification Logic

## Project Title

**NovaWorks Autonomous Sales Lead Qualification Agent**

---

# Overview

The NovaWorks Autonomous Sales Lead Qualification Agent follows a structured, rule-based qualification process to ensure every sales enquiry is evaluated consistently, accurately, and in accordance with NovaWorks business policies.

The qualification logic combines customer-provided information, organizational policies, and operational data stored in the connected Excel workbook. Every decision is fully traceable and based only on approved business rules.

---

# Qualification Objectives

The qualification logic is designed to:

- Standardize lead evaluation.
- Eliminate inconsistent qualification decisions.
- Prevent duplicate lead creation.
- Ensure product validation.
- Assign the correct Territory Owner and Sales Owner.
- Generate auditable qualification outcomes.
- Escalate cases requiring manual review.

---

# Inputs

The qualification process uses two categories of inputs.

## 1. Customer Information

Extracted from the incoming email:

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

---

## 2. Operational Data

Retrieved from the connected Excel workbook.

Tables used:

- Leads Register
- Qualification Rules
- Product Catalog
- Territory Owner Mapping
- Sales Owner Directory
- Action Matrix

These tables act as the authoritative source for all business decisions.

---

# Qualification Workflow

The agent evaluates each lead using the following sequence.

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
Check Duplicate Lead
       │
       ▼
Validate Product
       │
       ▼
Retrieve Qualification Rules
       │
       ▼
Evaluate Budget
       │
       ▼
Evaluate Timeline
       │
       ▼
Determine Territory
       │
       ▼
Assign Territory Owner
       │
       ▼
Assign Sales Owner
       │
       ▼
Determine Qualification Status
       │
       ▼
Determine Next Action
       │
       ▼
Update Lead Register
       │
       ▼
Generate Report
       │
       ▼
Send Customer Email
```

---

# Validation Logic

Before qualification, the following validations are performed.

## Required Fields

The agent verifies that mandatory information is available.

Typical mandatory fields include:

- Company Name
- Contact Name
- Email Address
- Country
- Requested Product

If mandatory information is missing:

- Qualification is paused.
- Customer is asked to provide the missing information.
- No qualification decision is made.

---

## Email Validation

The email address must:

- Follow a valid email format.
- Be available for customer communication.

Invalid email addresses prevent further processing.

---

## Product Validation

The requested product is validated against the Product Catalog.

If the product exists:

- Continue processing.

If the product does not exist:

- Follow the Action Matrix.
- Reject or escalate according to company policy.
- Do not recommend unsupported products.

---

## Territory Validation

The customer's Country and Region are matched against the Territory Owner Mapping table.

If no matching territory exists:

- Escalate for manual review.

---

## Budget Validation

Budget values are compared against the Qualification Rules.

The agent verifies:

- Budget format
- Minimum qualification threshold (if applicable)

The agent never estimates or modifies budget values.

---

## Timeline Validation

The expected implementation timeline is evaluated according to operational qualification rules.

If the timeline does not satisfy business requirements, the appropriate action is determined using the Action Matrix.

---

# Duplicate Detection

Before creating a new lead:

The agent searches the Leads Register.

If an existing lead is found:

- Update the existing record.
- Preserve historical information where appropriate.
- Do not create duplicate entries.

If no existing lead is found:

- Create a new Lead Register entry.

---

# Owner Assignment Logic

## Territory Owner

Assigned using:

- Country
- Region
- Territory Mapping

Only valid operational mappings are used.

---

## Sales Owner

Assigned using:

- Territory
- Product responsibility
- Sales Owner Directory

The agent never assigns an owner that is not defined in the operational data.

---

# Qualification Outcomes

The agent produces one of the following outcomes.

## Qualified

Conditions:

- Mandatory information available.
- Product supported.
- Validation successful.
- Qualification Rules satisfied.
- Territory mapping exists.
- Sales Owner assigned.

Next Action:

- Assign to Sales.
- Generate report.
- Send acknowledgement email.

---

## Needs More Information

Conditions:

- Required customer information is missing.
- Validation cannot be completed.

Next Action:

- Request additional information.
- Suspend qualification until a customer response is received.

---

## Rejected

Conditions:

- Product unsupported.
- Qualification Rules not satisfied.
- Action Matrix specifies rejection.

Next Action:

- Send professional rejection email.
- Record decision in Lead Register.

---

## Manual Review

Conditions:

- Operational lookup failure.
- Territory cannot be determined.
- Sales Owner unavailable.
- Business conflict detected.
- Unexpected validation failure.

Next Action:

- Escalate to an authorized user.
- Do not continue automated processing.

---

# Action Matrix Integration

The Action Matrix determines the next business step after qualification.

Supported actions include:

- Assign to Sales
- Request Additional Information
- Reject Lead
- Escalate
- Manual Review

The agent never generates actions outside those defined in the Action Matrix.

---

# Decision Principles

The qualification logic follows these principles:

- Operational data is authoritative.
- Company policies override assumptions.
- Missing information is never inferred.
- Validation always precedes qualification.
- Qualification decisions are deterministic and repeatable.
- Every outcome must be auditable.

---

# Error Handling

If any required lookup or validation fails:

- Stop the qualification process.
- Do not update operational records.
- Do not generate reports.
- Do not send misleading communications.
- Escalate the case when required.

---

# Compliance Rules

The agent must never:

- Fabricate customer information.
- Modify qualification rules.
- Recommend unsupported products.
- Assign unauthorized sales representatives.
- Expose internal operational tables.
- Reveal internal reasoning or business logic.
- Make commitments beyond documented company policies.

---

# Success Criteria

The qualification process is considered successful when:

- Customer information is extracted accurately.
- All mandatory validations are completed.
- Operational data is successfully retrieved.
- Qualification rules are correctly applied.
- Territory and Sales Owners are assigned.
- Lead Register is updated.
- Lead Qualification Report is generated.
- Customer communication is sent.
- All actions comply with NovaWorks policies.

---

# Conclusion

The qualification logic provides a consistent, transparent, and policy-driven framework for evaluating sales enquiries. By combining structured customer information with operational business data, the NovaWorks Autonomous Sales Lead Qualification Agent ensures reliable lead qualification, accurate owner assignment, standardized reporting, and professional customer communication while maintaining full compliance with organizational standards.