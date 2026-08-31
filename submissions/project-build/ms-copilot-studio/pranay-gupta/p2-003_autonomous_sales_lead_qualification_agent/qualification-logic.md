# Qualification Logic

## Project Information

| Field                | Details              |
| -------------------- | -------------------- |
| **Project ID**       | P2-003           |
| **Participant Name** | Pranay Gupta |
| **Agent Name**       | Pranay NovaWorks Sales Lead Agent       |

---

# Overview

The agent evaluates each incoming email to determine whether it is a valid sales opportunity. It follows the NovaWorks Sales Lead Qualification and Autonomy Policy and uses the operational Excel workbook to ensure consistent and accurate decision-making.

---

# Qualification Workflow

```text
Receive Lead Email
        │
        ▼
Validate Sales Inquiry
        │
        ▼
Extract Lead Information
        │
        ▼
Normalize Data
        │
        ▼
Check Duplicate
        │
        ▼
Calculate Qualification Score
        │
        ▼
Apply Business Rules
        │
        ▼
Assign Classification
        │
        ▼
Assign Sales Owner
        │
        ▼
Update Records & Complete Processing
```

---

# Information Used for Qualification

The agent evaluates the following information extracted from the email:

* Contact Name
* Company Name
* Country
* Product Interest
* Business Need
* Budget
* Purchase Timeline
* Decision Role
* Company Size
* Lead Source

---

# Qualification Factors

The qualification score is calculated using the operational rules based on:

| Factor            | Purpose                                                            |
| ----------------- | ------------------------------------------------------------------ |
| Product Fit       | Measures how well the requested product matches the business need. |
| Budget            | Evaluates budget availability against product requirements.        |
| Purchase Timeline | Gives higher priority to near-term opportunities.                  |
| Decision Role     | Considers the authority of the contact.                            |
| Company Size      | Evaluates potential business value.                                |
| Territory         | Verifies supported sales regions.                                  |
| Lead Source       | Considers the origin of the inquiry.                               |
| Completeness      | Rewards complete and usable information.                           |

---

# Lead Classifications

Based on the calculated score and business rules, the agent assigns one of the following classifications:

* Hot
* Qualified
* Nurture
* Low Priority
* Additional Information Required
* Human Review Required
* Duplicate
* Not a Sales Lead

---

# Duplicate Handling

Before creating a new lead, the agent:

* Checks the Message ID.
* Compares Company Name.
* Compares Contact Email.
* Compares Product Interest.

If a duplicate is found:

* Update the existing record.
* Do not create a new Lead ID.
* Do not generate another report.
* Do not send another acknowledgement.

---

# Sales Owner Assignment

After qualification, the agent:

* Identifies the lead territory.
* Maps the territory to the assigned sales owner.
* Routes unsupported territories to Human Review.

---

# Exception Handling

The agent routes the lead for Human Review when:

* Product is unknown.
* Territory cannot be mapped.
* Information is conflicting.
* Confidence is low.
* Competitor-related content is detected.
* Required tools fail during processing.

---

# Processing Outcome

After completing qualification, the agent:

* Creates or updates the lead record.
* Generates a Word report for eligible leads.
* Sends the appropriate Outlook communication.
* Records the processing status and assigned owner.

---

# Conclusion

The qualification logic combines structured business rules, operational reference data, and automated decision-making to ensure consistent lead evaluation while routing uncertain or exceptional cases for manual review.
