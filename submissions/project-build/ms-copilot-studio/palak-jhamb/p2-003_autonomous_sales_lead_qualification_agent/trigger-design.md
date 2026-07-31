# trigger-design.md

# Trigger Design

## Trigger

The agent uses the **Get emails (V3)** Outlook connector to monitor incoming emails.

---

## Trigger Condition

Only process emails whose subject contains:

`[P2-003 LEAD]`

All other emails are ignored.

---

## Email Filters

The trigger validates:

- Subject


Only valid sales enquiry emails continue for processing.

---

## Information Extraction

The agent extracts:

- Message ID
- Subject
- Sender Name
- Sender Email
- Contact Name
- Company Name
- Country
- Product Interest
- Budget
- Purchase Timeline
- Business Need
- Decision Role

Missing values are recorded as **Unknown**.

---

## Validation

Before qualification, the agent:

- Normalizes extracted values.
- Validates products using the Product Catalog.
- Validates territories using Territory Owners.
- Detects duplicate opportunities.

---

## Human Review Trigger

The lead is routed for manual review when:

- Product cannot be identified.
- Territory cannot be mapped.
- Qualification confidence is low.
- Information conflicts exist.
- Tool execution fails.

---

## Test Evidence

| Test | Status |
|------|--------|
| Outlook Trigger |  Passed |
| Subject Filter |  Passed |
| Information Extraction |  Passed |
| Duplicate Detection |  Passed |
| Invalid Email Ignored |  Passed |