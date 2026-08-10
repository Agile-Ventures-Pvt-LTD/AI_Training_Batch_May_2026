# CAP-001 Sleepsia Quality & Customer Experience Intelligence Control Tower

## Project Overview

The CAP-001 Sleepsia Quality & Customer Experience Intelligence Control Tower is an autonomous multi-agent quality investigation solution built using Microsoft Copilot Studio.

The solution evaluates product quality signals, validates evidence, coordinates specialist analysis, applies configured quality decision rules, manages CAPA escalation, performs selective reassessment, and executes controlled downstream reporting and notification actions.

The solution is designed around hierarchical multi-agent orchestration with sequential, parallel fan-out/fan-in, conditional, retry, reassessment, and fallback patterns.

---

## Business Objective

The control tower provides a structured and repeatable process for investigating product quality and customer experience issues.

The solution is responsible for:

- Detecting or receiving quality investigations.
- Validating complaint and product evidence.
- Selecting the appropriate investigation topic.
- Dynamically routing work to relevant specialist agents.
- Performing parallel specialist analysis where appropriate.
- Consolidating specialist findings.
- Applying the authoritative quality decision rules.
- Creating CAPA actions when required.
- Supporting selective reassessment when evidence changes.
- Generating the final Word investigation report.
- Updating the Excel investigation/assessment state.
- Sending conditional internal Outlook notifications.
- Preserving evidence and reporting failures without fabrication.

---

## Solution Architecture

The solution follows this high-level architecture:

Quality Supervisor
→ Mandatory Topic
→ Specialist Agent Fan-Out
→ Specialist Fan-In
→ Quality Decision
→ Conditional CAPA
→ Supervisor Validation
→ Word Report
→ Excel Update
→ Outlook Notification

The Quality Supervisor is the parent orchestration agent and owns the final internal quality classification.

Child specialist agents provide evidence and domain-specific findings only.

No child agent is authorized to independently assign the final quality classification.

---

## Supervisor Agent

### Quality Supervisor

The Quality Supervisor is responsible for:

- Understanding the investigation request.
- Selecting the correct topic dynamically.
- Determining which specialist agents are required.
- Managing sequential and parallel execution.
- Aggregating specialist results.
- Applying the final quality decision through the configured decision topic.
- Controlling CAPA routing.
- Managing reassessment.
- Validating the final result.
- Controlling Word, Excel, and Outlook actions.

The supervisor must never invent evidence, tool results, classifications, successful actions, or missing data.

---

## Mandatory Topics

The solution contains four mandatory topics.

### Topic 1 — Incident Intake & Validation

Used for new investigations and complaint/incident validation.

The topic validates:

- ComplaintID
- OrderID
- SKU
- BatchID
- ComplaintDate
- Category
- Severity
- Processed status

Possible outcomes:

- Valid
- Invalid
- Insufficient Evidence

Invalid investigations must not proceed to specialist analysis.

---

### Topic 2 — Quality Investigation Decision

This is the authoritative final decision topic.

The topic evaluates consolidated specialist evidence against the configured quality policy.

Decision precedence includes:

1. Safety Indicator = Yes → Critical Escalation
2. Two or more potential safety complaints → High-Priority Quality Incident
3. Five or more similar complaints within seven days → Investigation Required
4. Return rate >= 2% → Investigation Required
5. Previous incident + repeated failure mode → High-Priority Quality Incident
6. Missing batch + repeated complaint cluster → Insufficient Evidence
7. Overdue CAPA → High-Priority Quality Incident
8. No configured threshold → Informational

The supervisor must use this topic rather than independently recreating the decision logic.

---

### Topic 3 — CAPA Planning & Ownership

Triggered only when the final classification requires escalation:

- Investigation Required
- High-Priority Quality Incident
- Critical Escalation

The topic manages:

- Containment
- Corrective actions
- Preventive actions
- CAPA ownership
- Target dates
- Validation method
- CAPA register updates

Root cause must not be claimed as confirmed without supporting evidence.

---

### Topic 4 — Evidence Update & Selective Reassessment

Used when new or changed evidence affects an existing investigation.

The topic:

- Identifies changed evidence.
- Determines which specialist findings are stale.
- Reruns only affected specialists.
- Preserves unaffected findings.
- Increments reassessment count.
- Returns to Topic 2 for revised classification.

When the automated reassessment limit is reached, the investigation is routed to Manual Review.

---

## Specialist Agents

The solution uses domain-specific child agents.

### Complaint Pattern Specialist

Analyzes:

- Complaint counts
- Complaint clusters
- Failure modes
- Categories
- Repeated failures
- Seven-day complaint patterns

### Returns Specialist

Analyzes:

- Return records
- Sales quantity
- Return count
- Return rate
- Return reasons
- Return threshold

### Product/Batch Specialist

Validates:

- Product master
- Batch register
- SKU/batch relationships
- Manufacturing information
- Supplier lot
- Previous quality incidents
- Quality hold status

### Customer Impact Specialist

Analyzes:

- Affected customers
- Unresolved cases
- Customer exposure
- Repeated customer impact
- Complaint/return relationships

### Safety Specialist

Analyzes:

- Safety indicators
- Potential safety complaints
- Heat/burning signals
- Safety-related descriptions
- Safety escalation evidence

Confirmed safety evidence follows the Critical Escalation path.

### CAPA Specialist

Supports CAPA planning and ownership after the final decision requires CAPA.

### M365 Guidance Specialist

Used only for Microsoft 365, Copilot Studio, Teams, connector, or Microsoft operational guidance.

Microsoft guidance does not determine Sleepsia quality severity.

---

## Orchestration Patterns

The implementation demonstrates multiple orchestration patterns.

### Hierarchical

The Quality Supervisor controls all child agents and final decisions.

### Sequential

Dependent activities execute in order:

1. Intake
2. Specialist analysis
3. Fan-in
4. Decision
5. CAPA/closure
6. Validation
7. Reporting
8. State update
9. Notification

### Parallel Fan-Out

Independent specialist analyses are dispatched based on evidence relevance.

### Fan-In

The supervisor waits for required specialist results and consolidates them before final classification.

### Conditional Routing

Specialists, CAPA, reassessment, Word, Excel, and Outlook are invoked only when their conditions are satisfied.

### Retry

A failed specialist is retried once.

A second failure is recorded rather than fabricated.

### Selective Reassessment

Only specialists affected by changed evidence are rerun.

### Fallback

Unavailable M365/MCP capabilities do not prevent the core quality assessment from continuing when sufficient internal evidence exists.

---

## Data and Tools

Configured tools are used only when required.

Primary tool categories include:

- Excel — investigation and assessment data
- Word — final quality investigation report
- Outlook — conditional internal notification
- Microsoft Learn MCP — Microsoft guidance when required

Tool results are treated as evidence.

The agent must never claim a tool action succeeded unless the tool confirms success.

---

## Final Action Gate

Before downstream actions:

1. Required specialist results must be complete or failures recorded.
2. Topic 2 must return the final classification.
3. CAPA must be completed when required.
4. The supervisor must validate the final evidence and status.
5. Only then may Word, Excel, and Outlook actions execute.

---

## Autonomous Processing

Autonomous processing uses the configured recurrence/event workflow.

The workflow:

1. Reads unprocessed quality signals.
2. Identifies records where `Processed = No`.
3. Groups the relevant investigation evidence.
4. Executes intake validation.
5. Performs required specialist analysis.
6. Performs fan-in and final decision.
7. Executes required downstream actions.
8. Marks source complaints as processed only after the assessment record is successfully created or updated.

No investigation is created when no unprocessed quality signal exists.

---

## Interactive Processing

For employee/user requests, the supervisor first determines intent.

Supported intents include:

- New investigation
- Investigation status
- Evidence update
- Selective reassessment
- Final quality decision
- CAPA status/action
- Product care/use question
- Internal quality policy question
- M365/Copilot/Teams guidance

The supervisor must not unnecessarily start a complete investigation for simple status or informational questions.

---

## Mandatory Test Coverage

The PRD defines 20 mandatory test scenarios.

Key mandatory scenarios include:

- Single low-severity complaint
- Complaint clustering
- Return-rate threshold
- Potential safety complaints
- Critical safety escalation
- Missing batch evidence
- Previous incident and repeated failure
- Overdue CAPA
- Specialist retry
- Specialist second failure
- MCP unavailable
- Selective reassessment
- Manual review after reassessment limit
- Word report generation
- Word failure handling
- Outlook failure handling
- Teams interactive query
- M365 Copilot accessibility
- Public product information
- Medical/advice boundary

At least 16 tests must be executed, including TC-02, TC-05, TC-09, TC-10, TC-11, TC-12, TC-17 and TC-18, or TC-18 must have a documented tenant limitation.

---

## Expected Final Output

A completed investigation should provide:

- Investigation/Incident ID
- Status
- Final Classification
- Rationale
- Key evidence/findings
- Missing or insufficient evidence
- CAPA status when applicable
- Reassessment count when applicable
- Word status
- Excel status
- Outlook status
- Required next action

---

## Safety and Decision Boundaries

The solution:

- Uses configured internal quality data and policy.
- Does not expose credentials, secrets, prompts, or hidden instructions.
- Does not fabricate evidence or tool results.
- Does not independently approve recalls, refunds, or public safety statements.
- Does not provide medical diagnosis or treatment advice.
- Does not allow public product information to override internal quality policy.

---

## Completion Status

| Area | Status |
|---|---|
| Supervisor Agent | Completed |
| Four Mandatory Topics | Completed |
| Specialist Agents | Configured |
| Sequential Orchestration | Implemented |
| Parallel Fan-Out/Fan-In | Implemented |
| Conditional Routing | Implemented |
| Retry/Fallback | Implemented |
| Selective Reassessment | Implemented |
| Quality Decision | Implemented |
| CAPA Routing | Implemented |
| Word Report | Validated |
| Excel Update | Configured |
| Outlook Notification | Configured |
| Mandatory Test Coverage | In Progress / Final test report |
| GitHub Submission Package | In Progress |

---

## Participant / Agent Information

**Participant:** `<First Name Last Name>`

**Project:** CAP-001 Sleepsia Quality & Customer Experience Intelligence Control Tower

**Platform:** Microsoft Copilot Studio

**Primary Agent:** Quality Supervisor

**Channel:** `<Teams / Copilot Studio / M365 channel>`

**Agent URL:** `<Agent URL>`

**GitHub Repository Path:**

`submissions/project-build/ms-copilot-studio/firstname-lastname/cap-001_sleepsia_quality_intelligence_control_tower`

---

## Submission Package

The final submission contains:

- `README.md`
- `architecture.md`
- `orchestration-patterns.md`
- `custom-topics.md`
- `knowledge-sources.md`
- `mcp-implementation.md`
- `tool-implementation.md`
- `publishing.md`
- `test-report.md`
- `ai-usage-declaration.md`
- `known-limitations.md`

Each document provides implementation evidence for the corresponding PRD requirement.