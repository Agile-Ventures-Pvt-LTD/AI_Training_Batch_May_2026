# Lead Qualification Logic

## Overview

The Autonomous Sales Lead Agent evaluates each incoming sales enquiry using predefined business rules stored in Microsoft Excel. The objective is to consistently prioritize leads, eliminate duplicate processing, identify incomplete enquiries, and determine the appropriate follow-up actions.

The qualification process is fully automated and executed by Microsoft Copilot Studio.

---

# Qualification Workflow

Every enquiry follows the same logical sequence:

1. Receive the email from Outlook.
2. Extract lead information.
3. Validate mandatory fields.
4. Check for duplicate records.
5. Read qualification rules.
6. Calculate the qualification score.
7. Apply business override rules.
8. Determine lead classification.
9. Execute required business actions.
10. Update the Lead Register.
11. Generate reports and notifications.

---

# Mandatory Fields

The following information is required for a complete qualification:

| Field | Required |
|---------|----------|
| Contact Name | Yes |
| Company Name | Yes |
| Country | Yes |
| Product Interest | Yes |
| Budget | Yes |
| Purchase Timeline | Yes |
| Decision Role | Yes |

If one or more mandatory fields are missing:

- Qualification scoring is skipped.
- No classification is assigned.
- The customer receives a request for additional information.
- The enquiry remains pending until the missing details are received.

---

# Qualification Factors

The agent evaluates several business attributes when qualifying a lead.

## Budget

Higher available budgets generally indicate stronger purchasing capability.

Example considerations:

- Enterprise budget
- Mid-market budget
- Small project budget
- Budget not provided

---

## Purchase Timeline

The expected purchase timeframe indicates lead urgency.

Typical categories include:

- Immediate
- 30–60 days
- 60–120 days
- Long-term planning

Earlier purchase timelines generally receive higher priority.

---

## Decision Authority

The role of the contact influences qualification.

Typical decision roles include:

- Final Decision Maker
- Strong Influencer
- Evaluator
- End User
- Researcher
- Student

Contacts with purchasing authority receive higher priority than informational enquiries.

---

## Product Interest

The requested solution is validated against the Product Catalog to ensure it is supported.

Unsupported or unknown products require manual review.

---

## Country

The customer's country is used to determine:

- Territory assignment
- Responsible sales owner
- Regional routing

---

# Duplicate Detection

Before creating a new record, the agent searches the Lead Register.

Duplicate detection considers available identifiers such as:

- Customer Name
- Company Name
- Email Address (if available)

---

## Duplicate Found

When a duplicate is identified:

- No new lead record is created.
- The existing record is updated.
- Existing history is preserved.
- The latest enquiry is recorded.

---

## No Duplicate Found

When no existing lead is found:

- A new lead record is created.
- Qualification proceeds normally.

---

# Business Overrides

Certain business conditions override normal qualification behaviour.

Examples include:

### Existing Customer Follow-up

The enquiry updates the existing lead rather than creating a new one.

---

### Missing Mandatory Information

Qualification is suspended until required information is received.

---

### Non-commercial Requests

Examples include:

- Academic research
- Student enquiries
- Source code requests
- Competitive intelligence requests

These enquiries are excluded from sales qualification and handled according to business policy.

---

### Product Not Identified

If the requested product cannot be determined:

- Qualification may continue with reduced confidence, or
- The customer is asked to provide clarification.

---

# Lead Classification

After applying qualification rules, the lead is assigned a business classification.

## Hot Lead

Characteristics typically include:

- High budget
- Short purchase timeline
- Final decision maker
- Commercial intent
- Complete information

Business actions:

- Generate qualification report
- Notify Sales Operations
- Send acknowledgement
- Assign sales owner immediately

---

## Warm Lead

Characteristics typically include:

- Moderate budget
- Medium purchase timeline
- Influencer or evaluator
- Commercial opportunity

Business actions:

- Create lead record
- Generate report (if required)
- Send acknowledgement
- Schedule follow-up

---

## Cold Lead

Characteristics typically include:

- Low budget
- Long purchase timeline
- Limited purchasing authority
- Early-stage interest

Business actions:

- Create lead record
- Send acknowledgement
- Future nurturing

---

## Unqualified

Typical reasons include:

- Missing mandatory information
- Non-commercial request
- Student research
- Competitor intelligence request
- Unsupported enquiry

Business actions:

- Do not qualify
- Request additional information (if applicable)
- Record processing outcome

---

# Action Matrix

Each classification determines the next business actions.

| Classification | Lead Record | Report | Customer Email | Sales Notification |
|---------------|-------------|--------|----------------|-------------------|
| Hot | Create/Update | Yes | Yes | Yes |
| Warm | Create/Update | Optional | Yes | Based on rules |
| Cold | Create | No | Yes | No |
| Unqualified | No Qualification | No | Request Information / Response | No |

---

# Error Handling

If qualification cannot be completed:

- No fabricated values are generated.
- Processing stops safely.
- Existing data remains unchanged.
- The failure is recorded in the execution history.

---

# Governance Principles

The qualification process follows these principles:

- Consistent business rule application
- Deterministic decision making
- No manual scoring manipulation
- No disclosure of internal scoring logic
- Secure handling of customer information
- Full traceability of processing decisions

---

# Expected Outcome

The qualification logic ensures that every inbound enquiry is evaluated consistently, duplicate records are avoided, qualified opportunities are prioritized, and appropriate business actions are executed automatically while maintaining governance and data integrity.