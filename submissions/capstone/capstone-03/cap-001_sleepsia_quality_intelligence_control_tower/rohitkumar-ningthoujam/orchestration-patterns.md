# Orchestration Patterns

## 1. Sequential

The Quality Supervisor validates the complaint/incident before starting specialist analysis.

Flow:
1. Receive investigation request.
2. Validate record.
3. Run specialist assessment.
4. Consolidate findings.
5. Determine final decision.
6. Create CAPA/report/notification when required.

## 2. Parallel Fan-Out / Fan-In

After validation, the Supervisor coordinates independent specialist agents.

Specialists include:
- Complaint Pattern Specialist
- Safety Specialist
- Product/Batch Specialist
- Customer Impact Specialist
- Returns Specialist

Their findings are collected and consolidated before the final decision.

## 3. Hierarchical Decision

The Quality Supervisor resolves conflicting specialist findings using quality precedence.

Priority is given to:
1. Safety concerns
2. Critical/high-priority quality conditions
3. Customer impact
4. Product/batch risk
5. Complaint and return evidence
6. CAPA requirements

## 4. Conditional Routing

The Supervisor routes cases according to validation and investigation results.

Examples:
- Invalid record → stop processing.
- Insufficient evidence → request/retain evidence gap.
- Safety concern → safety escalation.
- CAPA-required classification → CAPA Planning & Ownership.
- Final outcome → generate report and/or notification.

## 5. CAPA Planning

For Investigation Required, High-Priority Quality Incident, or Critical Escalation cases:

1. Create containment action.
2. Define corrective/preventive action.
3. Assign OwnerRole from Owners table.
4. Set target date.
5. Define validation method.
6. Write CAPA_Register.
7. Return CAPA summary.

## 6. Selective Reassessment

When new evidence or changed specialist findings affect the investigation, the Supervisor reassesses the affected analysis instead of unnecessarily restarting the entire workflow.

## 7. Retry / Fallback

If a specialist result or required operation fails, the Supervisor retries when appropriate. If the required evidence remains unavailable, the workflow uses the configured fallback path and does not fabricate results.

## 8. Reporting and Notification

After the final decision:

- Generate Quality Investigation Report using the Word tool.
- Send Quality Investigation Notification using the Outlook tool when required.

## 9. Tool Boundaries

- Quality Supervisor: orchestration and decision coordination.
- Specialist agents: domain-specific investigation.
- Excel tools: structured quality data retrieval/update.
- Word tool: investigation report generation.
- Outlook tool: investigation notification.
- MCP tool: Microsoft 365 guidance/retrieval.
