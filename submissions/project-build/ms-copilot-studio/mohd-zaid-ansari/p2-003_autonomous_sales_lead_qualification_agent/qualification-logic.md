# Qualification Logic

## Scoring

The agent reads the scoring rules from **QualificationRulesTable**.

The score is based on:

- Product Fit
- Budget
- Purchase Timeline
- Decision Role
- Company Size
- Territory
- Lead Source
- Information Completeness

The agent always uses the latest rules from Excel.

The score is not hardcoded.

---

## Overrides

Some business rules are applied before the final result.

Examples:

- Startup/Micro companies with a very low budget are marked as **Low Priority**.
- Low confidence leads are marked as **Human Review Required**.
- Unknown products are marked as **Human Review Required**.
- Unknown territories are marked as **Human Review Required**.
- Conflicting information is marked as **Human Review Required**.

Override rules take priority over the score.

---

## Duplicate Detection

Before creating a new lead, the agent checks the **LeadsRegisterTable**.

First, it checks the **Source_Message_ID**.

If no exact match is found, it compares:

- Company Name
- Sender Email
- Product Interest

If a duplicate is found:

- The existing record is updated.
- No new record is created.
- No Word report is created.
- No acknowledgement email is sent.
- The lead is classified as **Duplicate**.

---

## Lead Classification

The agent assigns one of the following classifications:

| Classification | Description |
|---------------|-------------|
| Hot | High-quality lead with a high score. |
| Qualified | Good sales opportunity. |
| Nurture | Needs more follow-up before becoming a sales opportunity. |
| Low Priority | Low business value or low budget. |
| Additional Information Required | Important information is missing. |
| Human Review Required | The agent cannot make a safe decision. |
| Duplicate | The lead already exists. |
| Not a Sales Lead | The email is not a sales enquiry. |

Only one final classification is assigned to each email.

---

## Processing Order

The agent follows these steps:

1. Check if the email is in scope.
2. Check if it is a sales lead.
3. Check for duplicate leads.
4. Read scoring rules from Excel.
5. Calculate the score.
6. Apply override rules.
7. Assign the final classification.
8. Update the Excel Lead Register.
9. Create a Word report if required.
10. Send the correct email reply.