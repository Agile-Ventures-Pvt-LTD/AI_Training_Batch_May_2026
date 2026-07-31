# Agent Instructions Design

## Purpose

The agent instructions help the agent process sales lead emails correctly and safely.
The instructions tell the agent what to do, when to use tools, and when to send a case for human review.
---

## Main Design

The instructions are divided into small sections so the agent can follow each step in order.

The main sections are:

- Role and objective
- Trigger scope
- Lead identification
- Lead information extraction
- Data normalization
- Duplicate detection
- Lead qualification
- Owner assignment
- Tool usage
- Word report creation
- Email communication
- Error handling
- Business rules

---

## Tool Design

The instructions tell the agent when to use each Microsoft 365 tool.

The agent uses tools to:

- Read Excel tables
- Add new lead records
- Update existing lead records
- Create Word reports
- Reply to emails

The agent does not guess data. It always uses the available tools.

---

## Decision Logic

The agent follows the same process for every email.

1. Check if the email is in scope.
2. Check if it is a sales lead.
3. Extract lead information.
4. Check for duplicate leads.
5. Read business rules from Excel.
6. Calculate the lead score.
7. Assign the correct classification.
8. Assign the sales owner.
9. Update Excel.
10. Create a Word report if needed.
11. Send the correct email reply.

---

## Human Review

The agent sends a case for human review when:

- Information is missing.
- Information is unclear.
- Product or territory cannot be matched.
- Tool errors continue after one retry.
- Business rules cannot be applied safely.

---

## Security

The instructions do not contain:

- Passwords
- API keys
- Secrets
- Access tokens
- Personal information

Only business rules and tool guidance are included.

---

## Result

The instruction design helps the agent:

- Follow the same process every time.
- Use Microsoft 365 tools correctly.
- Reduce manual work.
- Prevent duplicate records.
- Handle errors safely.
- Send difficult cases for human review.