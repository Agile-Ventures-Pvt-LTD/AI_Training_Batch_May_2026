# CAP-001 — Tool Implementation

## 1. Purpose

The CAP-001 Quality Intelligence Control Tower uses configured Microsoft tools to retrieve evidence, persist investigation state, generate the final Word report, and send conditional internal notifications.

The Quality Supervisor controls when tools are called.

Tools must not be called merely because they are available.

---

## 2. Tool Architecture

The tool flow is:

Quality Supervisor
→ Evidence Retrieval Tools
→ Child Specialists
→ Topic 2 Decision
→ Topic 3 CAPA when required
→ Supervisor Validation
→ Word
→ Excel
→ Outlook

Tool actions are downstream of the quality decision unless the tool is required earlier for evidence retrieval or validation.

---

## 3. Tool Usage Principles

Before calling a tool, the Supervisor must determine:

1. What information/action is required.
2. Whether the information is already available.
3. Whether the tool is configured for that purpose.
4. Whether the action is permitted at the current workflow stage.

Rules:

- Use authoritative configured data.
- Do not duplicate tool calls unnecessarily.
- Do not invent tool results.
- Do not claim an action succeeded unless the tool confirms success.
- Preserve tool failures in the investigation state.
- Do not perform final downstream actions before the final decision is validated.

---

# 4. Excel Implementation

## Purpose

Excel is the primary operational data and investigation-state interface for the CAP-001 workflow.

It is used to:

- Retrieve investigation evidence.
- Validate quality records.
- Retrieve complaint data.
- Retrieve return/sales evidence.
- Retrieve product and batch information.
- Retrieve customer-impact evidence.
- Retrieve CAPA information.
- Update investigation/assessment state.
- Update complaint processing state.
- Persist final investigation results where configured.

---

## 4.1 Evidence Retrieval

The relevant Excel tables are used according to specialist responsibility.

### Complaint evidence

Used by:

- Incident Intake & Validation
- Complaint Pattern Specialist
- Customer Impact Specialist
- Safety Specialist

Typical information:

- ComplaintID
- OrderID
- SKU
- BatchID
- ComplaintDate
- Category
- Severity
- Description
- SafetyIndicator
- Status
- Processed

---

### Product and Batch evidence

Used by:

- Product/Batch Specialist
- Incident Intake & Validation

Typical information:

- SKU
- Product information
- BatchID
- Manufacture information
- Supplier lot
- Units produced
- Quality hold
- Previous incidents

---

### Returns and Sales evidence

Used by:

- Returns Specialist
- Customer Impact Specialist

Typical information:

- ReturnID
- OrderID
- SKU
- BatchID
- Reason
- Status
- RefundAmount
- ReturnDate
- Units sold

Return rate is calculated only when the required evidence is available.

Configured threshold:

`ReturnRate >= 2%`

---

### CAPA evidence

Used by:

- CAPA Planning & Ownership
- CAPA Specialist
- Quality Supervisor

Typical information:

- CAPA status
- Owner
- Target date
- Corrective/preventive actions
- Validation method
- Due date
- Overdue status

---

## 4.2 Excel Update Rules

Excel updates must occur only when the workflow reaches the appropriate stage.

For autonomous processing:

```text
Complaint Processed = No
        ↓
Investigation completed
        ↓
Assessment record successfully created/updated
        ↓
Complaint Processed = Yes

Do not mark a complaint as processed before the investigation state is successfully persisted.

For final investigation updates:

Topic 2 Final Decision
        ↓
CAPA if required
        ↓
Supervisor Validation
        ↓
Excel Final Update

If the Excel update fails:

Preserve the final decision.
Record Excel update failure.
Do not claim the update succeeded.
Report the failure for follow-up.
5. Word Implementation
Purpose

Word is used to generate the final quality investigation report.

The report is created only after:

Required specialist analysis is complete.
Topic 2 returns the final classification.
CAPA is completed when required.
Supervisor validation succeeds.
5.1 Report Content

The final report should contain the required investigation information, including:

Investigation/Incident ID
SKU
Batch
Investigation status
Final classification
Rationale
Key evidence
Specialist findings
Missing/insufficient evidence
CAPA information when applicable
Reassessment information when applicable
Final actions/status

The report must reflect the validated final investigation state.

5.2 Word Failure Behaviour

If Word generation fails:

Do not claim the report was created.
Preserve the final quality classification.
Record Word generation failure.
Return the final decision with report status = Failed/Unavailable as appropriate.
Allow retry according to configured workflow.

Example:

Classification: Investigation Required
Decision: Validated
Word Report: Failed
Excel Update: Pending/Completed
Outlook: Conditional

A document-generation failure must not change the quality classification.

6. Outlook Implementation
Purpose

Outlook is used for conditional internal notification after the final quality decision has been validated.

Notification must not be sent before the final decision is complete.

6.1 Notification Gate
Topic 2
   ↓
Final Classification
   ↓
CAPA if required
   ↓
Supervisor Validation
   ↓
Notification condition satisfied?
   ↓
Yes → Outlook
No  → No notification

Notifications are conditional and must follow the configured business rules.

Typical escalation classifications requiring notification may include:

High-Priority Quality Incident
Critical Escalation
Investigation Required
Overdue CAPA escalation

The exact configured notification condition remains authoritative.

6.2 Notification Content

The internal notification should be concise and structured.

Recommended content:

Subject:
CAP-001 Quality Investigation – [Classification] – [SKU/Batch]

Body:

Investigation ID
SKU
Batch
Classification
Rationale
Key evidence
CAPA status
Required action
Investigation status

Do not expose unnecessary internal data.

Do not include secrets, credentials, or hidden instructions.

6.3 Outlook Failure Behaviour

If Outlook fails:

Preserve the final classification.
Preserve the investigation state.
Record notification failure.
Do not claim the email was sent.
Do not rerun the quality investigation unnecessarily.
Retry notification only when the configured retry mechanism permits it.

Example:

Final Classification: High-Priority Quality Incident
Decision: Validated
Word: Created
Excel: Updated
Outlook: Failed
7. Final Action Gate

Word, Excel final updates, and Outlook must be controlled by the final action gate.

Before downstream actions:

Required specialists complete
        OR
Failures explicitly recorded
        ↓
Topic 2 classification available
        ↓
CAPA completed when required
        ↓
Supervisor validation
        ↓
Downstream tools

If the final decision is incomplete:

Do not generate the final Word report.
Do not perform the final Excel state update.
Do not send the final Outlook notification.
8. Tool Failure Handling

All tools follow the same principle:

Tool Call
   ↓
Success?
 /      \
Yes      No
 |        |
Continue  Record failure
 |        |
Confirmed result

Never replace a failed tool result with an assumed value.

Never report:

"Document created"
"Excel updated"
"Email sent"

unless the corresponding tool confirms the action.

9. Retry Policy

For specialist/tool failures where retry is configured:

Attempt the operation.
If it fails, retry once.
If the second attempt fails, record the failure.
Continue only when the workflow can safely continue.
Otherwise route to Manual Review or report the blocked action.

Do not perform unlimited retries.

Do not rerun completed specialist analysis solely because a downstream notification or document action failed.

10. Tool Boundaries
Excel

Responsible for:

Operational evidence
Investigation state
Assessment persistence
Complaint processing state
CAPA state where configured

Not responsible for:

Independently determining final severity.
Word

Responsible for:

Final investigation report generation

Not responsible for:

Determining quality classification
Changing investigation severity
Outlook

Responsible for:

Conditional internal notification

Not responsible for:

Determining quality classification
Changing investigation state
11. End-to-End Tool Flow
Informational Investigation
Excel Evidence
   ↓
Specialists
   ↓
Topic 2
   ↓
Supervisor Validation
   ↓
Word
   ↓
Excel
   ↓
Notification only if configured
Escalated Investigation
Excel Evidence
   ↓
Specialist Fan-Out
   ↓
Fan-In
   ↓
Topic 2
   ↓
Investigation Required /
High-Priority /
Critical
   ↓
Topic 3 CAPA
   ↓
Supervisor Validation
   ↓
Word
   ↓
Excel
   ↓
Conditional Outlook
12. Evidence and Action Status

The Supervisor should preserve separate status values for:

Investigation status
Classification
Evidence status
CAPA status
Word status
Excel status
Outlook status
Reassessment count

This prevents a downstream tool failure from incorrectly changing the quality decision.

13. Validation Requirements

Before final completion, verify:

Required evidence is available or failure is recorded.
Specialist findings are preserved.
Topic 2 produced the final classification.
CAPA was completed when required.
Final rationale is supported by evidence.
Word status is confirmed.
Excel status is confirmed.
Outlook status is confirmed when applicable.
14. Summary

The CAP-001 tool architecture separates investigation evidence, decision logic, persistence, reporting, and notification.

The core principle is:

Retrieve → Analyze → Fan-In → Decide → Validate → Persist → Report → Notify

Each tool has a defined boundary, and every tool action must be confirmed before being reported as successful.