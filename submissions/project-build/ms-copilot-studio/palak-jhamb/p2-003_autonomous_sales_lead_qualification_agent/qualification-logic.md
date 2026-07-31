# qualification-logic.md

# Qualification Logic

## Duplicate Detection

Before creating a new lead, the agent checks:

- Message ID
- Sender Email
- Company Name
- Product Interest

Duplicates update the existing record instead of creating a new one.

---

## Qualification Workflow

1. Extract information.
2. Normalize values.
3. Read Excel reference tables.
4. Validate products.
5. Validate territory.
6. Calculate qualification score.
7. Determine lead classification.
8. Assign Sales Owner.
9. Update Lead Register.
10. Generate report if required.

---

## Scoring Source

Qualification scores are retrieved from:

**Read Qualification Rules**

No scoring logic is hardcoded in the agent.

---

## Lead Classifications

- Hot
- Qualified
- Nurture
- Low Priority
- Additional Information Required
- Human Review Required
- Duplicate
- Not a Sales Lead

---

## Exception Rules

The Action Matrix determines whether:

- Report generation is required.
- Customer communication is required.
- Human Review is required.

---

## Owner Assignment

The agent determines:

Country

↓

Territory

↓

Assigned Sales Owner

using:

- Read Territory Owners
- Read Sales Owners

---

## Action Matrix

The Action Matrix controls:

- Qualification actions
- Report generation
- Customer emails
- Internal notifications
- Human Review