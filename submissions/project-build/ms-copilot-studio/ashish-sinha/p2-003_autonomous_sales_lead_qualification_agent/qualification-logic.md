# Qualification Logic

## Document Information

| Item | Details |
|------|---------|
| **Project Name** | NovaWorks Autonomous Sales Lead Qualification Agent |
| **Project ID** | P2-003 |
| **Platform** | Microsoft Copilot Studio |
| **Document Version** | 1.0 |
| **Prepared By** | Ashish Sinha |
| **Last Updated** | 31 July 2026 |

---

# 1. Purpose

This document describes the business logic used by the NovaWorks Autonomous Sales Lead Qualification Agent to evaluate incoming sales enquiries.

The logic defines how the agent:

- Detects duplicate leads
- Calculates qualification scores
- Applies business overrides
- Classifies leads
- Determines the next business action

The rules documented here are independent of the implementation technology and represent the business decision model used by the autonomous agent.

---

# 2. Qualification Workflow

```
Incoming Email
        │
        ▼
Extract Lead Information
        │
        ▼
Mandatory Field Validation
        │
        ▼
Duplicate Detection
        │
        ▼
Product Validation
        │
        ▼
Qualification Scoring
        │
        ▼
Business Overrides
        │
        ▼
Lead Classification
        │
        ▼
Determine Next Action
```

---

# 3. Mandatory Information Validation

Before qualification begins, the agent validates that sufficient information is available.

Mandatory information includes:

- Customer Name
- Company Name
- Email Address
- Product of Interest
- Business Requirement

If mandatory information is missing:

- No qualification score is calculated.
- The lead is marked as **Incomplete**.
- A request for additional information is sent to the customer.

---

# 4. Duplicate Detection Logic

Duplicate detection is performed before creating a new lead.

The agent compares the incoming enquiry with existing records in the Lead Register.

Matching criteria include:

1. Source Message ID (preferred)
2. Sender Email Address
3. Company Name
4. Product of Interest

---

## Duplicate Decision Matrix

| Condition | Action |
|-----------|--------|
| No matching lead | Create new lead |
| Existing lead found | Update existing record |
| Same email received multiple times | Ignore duplicate processing |
| Partial match requiring review | Escalate for human review |

---

# 5. Product Validation

The extracted product name is validated against the Product Catalog.

| Result | Action |
|---------|--------|
| Product found | Continue qualification |
| Product not found | Human review required |

The agent does not create new products automatically.

---

# 6. Qualification Scoring

Qualification scoring evaluates the quality of a lead using predefined business rules stored in the operational Excel workbook.

Typical evaluation factors include:

- Completeness of information
- Product availability
- Business requirement clarity
- Customer organization
- Territory availability

The scoring rules are maintained externally and retrieved dynamically during execution.

---

## Qualification Process

```
Lead Information
        │
        ▼
Read Qualification Rules
        │
        ▼
Evaluate Business Criteria
        │
        ▼
Calculate Score
```

---

# 7. Business Overrides

Certain business conditions take precedence over calculated scores.

Overrides ensure that predefined organizational policies are consistently applied.

Examples include:

| Override Condition | Result |
|--------------------|--------|
| Duplicate lead | Update existing record |
| Unknown product | Human review |
| Unknown territory | Human review |
| Missing mandatory information | Request additional information |
| Sales owner unavailable | Sales Operations review |

Overrides are evaluated before final classification.

---

# 8. Territory Assignment

The agent determines the responsible sales territory using the Territory Mapping table.

Input:

- Country
- Region (if available)

Possible outcomes:

- Territory identified
- Territory unavailable

If no territory can be identified, the lead is routed for manual review.

---

# 9. Sales Owner Assignment

After determining the territory, the agent assigns a sales owner using the Sales Owners table.

Assignment logic:

```
Territory
      │
      ▼
Sales Owner Lookup
      │
      ▼
Assigned Representative
```

If no owner is available, the lead is escalated to Sales Operations.

---

# 10. Lead Classification

After all validations and scoring have been completed, the lead is classified.

Example classifications include:

| Classification | Description |
|---------------|-------------|
| Qualified | Meets all qualification requirements |
| Needs Information | Mandatory information is missing |
| Duplicate | Existing lead identified |
| Human Review | Manual intervention required |

The classification determines the next workflow step.

---

# 11. Action Matrix

The Action Matrix defines the business action associated with each classification.

| Classification | Next Action |
|---------------|-------------|
| Qualified | Create lead, generate report, notify sales owner |
| Needs Information | Send customer information request |
| Duplicate | Update existing lead |
| Human Review | Notify Sales Operations |

The Action Matrix is maintained within the operational Excel workbook.

---

# 12. Decision Flow

```
New Email
      │
      ▼
Mandatory Fields Complete?
      │
 ┌────┴────┐
 │         │
No        Yes
 │         │
 ▼         ▼
Request   Duplicate?
Info       │
            ┌────┴────┐
            │         │
          Yes        No
            │         │
            ▼         ▼
       Update Lead   Validate Product
                        │
                        ▼
                 Product Valid?
                        │
                 ┌──────┴──────┐
                 │             │
                No            Yes
                 │             │
                 ▼             ▼
          Human Review    Score Lead
                               │
                               ▼
                        Assign Territory
                               │
                               ▼
                       Assign Sales Owner
                               │
                               ▼
                        Classify Lead
                               │
                               ▼
                        Execute Action
```

---

# 13. Error Handling

The qualification logic includes controlled handling for exceptional scenarios.

| Scenario | Action |
|----------|--------|
| Missing required information | Request additional information |
| Duplicate detected | Update existing lead |
| Invalid product | Human review |
| Unknown territory | Human review |
| Missing sales owner | Human review |
| Qualification rules unavailable | Stop processing and log error |

---

# 14. Design Principles

The qualification model follows these principles:

- Validate before processing.
- Prevent duplicate records.
- Apply business rules consistently.
- Separate business rules from implementation.
- Retrieve operational data dynamically.
- Escalate uncertain cases.
- Ensure repeatable decision making.

---

# 15. Assumptions

The qualification logic assumes:

- Operational data is available in the Excel workbook.
- Territory mappings are maintained.
- Product catalog is current.
- Sales owner assignments are accurate.
- Outlook emails contain sufficient information for evaluation.

---

# 16. Limitations

The current qualification logic does not:

- Predict lead conversion probability.
- Perform AI-based sentiment analysis.
- Automatically create new products.
- Assign owners outside configured mappings.
- Learn from historical qualification decisions.

These enhancements may be considered in future iterations.

---

# 17. Validation

The qualification logic was validated using representative business scenarios including:

- New qualified lead
- Duplicate lead
- Missing information
- Unknown product
- Unknown territory
- Sales owner unavailable

Each scenario produced the expected business outcome according to the configured rules.

---

# 18. Conclusion

The qualification logic provides a structured and auditable framework for evaluating incoming sales enquiries. By separating scoring rules, duplicate detection, business overrides, and classification from the implementation, the solution ensures consistent decision-making and simplifies future maintenance.

The use of externally maintained business rules within the operational workbook allows the organization to update qualification criteria without modifying the agent itself.