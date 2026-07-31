# Agent Instructions Design

## Purpose

This document describes the instruction design implemented in the Autonomous Sales Lead Qualification Agent. The instructions guide the agent through an end-to-end autonomous workflow for processing inbound sales leads while ensuring consistent decision-making, deterministic execution, and compliance with business policies.

No confidential information, credentials, tenant-specific configuration, or secrets are included in this document.

---

# Instruction Design Objectives

The agent instructions were designed with the following objectives:

- Perform autonomous lead qualification without human intervention for standard scenarios.
- Ensure deterministic execution through clearly defined processing phases.
- Prevent hallucinations by using reference data and configured business rules.
- Execute Microsoft 365 tools only when required.
- Maintain consistent communication and reporting.
- Escalate uncertain cases for human review.

---

# Autonomous Workflow

The instruction set follows an eleven-phase processing model.

1. Trigger Validation
2. Lead Information Extraction
3. Data Normalization
4. Duplicate Detection
5. Qualification and Scoring
6. Lead Classification
7. Sales Owner Assignment
8. Excel Lead Register Update
9. Word Qualification Report Generation
10. Outlook Communications
11. Completion and Status Recording

> **Screenshot – Instructions and Knowledge Base**

![Instruction and KB](<Screenshot 2026-07-31 164452.png>)

---

# Instruction Categories

## Input Processing

The agent extracts structured lead information from incoming Outlook emails and validates the presence of mandatory business fields before continuing with qualification.

---

## Knowledge-Based Decision Making

The agent references configured operational datasets and business policies to ensure that all qualification decisions are based on approved organizational rules rather than model assumptions.

---

## Qualification Logic

The instructions guide the agent to:

- Normalize extracted information.
- Detect duplicate submissions.
- Apply qualification rules.
- Calculate qualification score.
- Determine decision confidence.
- Classify the lead.
- Assign the appropriate owner.

---

## Tool Orchestration

The instructions specify when each Microsoft connector should be invoked.

| Tool | Purpose |
|------|---------|
| Excel Online | Store and retrieve operational data |
| Microsoft Word Business | Generate qualification reports |
| Office 365 Outlook | Trigger processing and send communications |

Tool execution occurs only after the required decision logic has been completed.

---

## Communication Strategy

The instructions determine whether external acknowledgements, requests for additional information, or internal notifications should be generated based on the final lead classification and configured business rules.

Email content is generated using the approved communication requirements document.

---

## Error Handling

The instructions include safeguards for:

- Missing mandatory information
- Duplicate submissions
- Unsupported products
- Unsupported territories
- Low decision confidence
- Connector failures
- Retry handling for transient errors

Cases that cannot be resolved autonomously are routed for human review.

---

## Completion Logic

The workflow concludes only after all required operations have completed successfully.

The completion stage records:

- Processing status
- Actions performed
- Exceptions encountered
- Tool execution status
- Final classification
- Assigned owner

---

# Design Principles

The instruction design follows the following principles:

- Deterministic execution
- Rule-driven qualification
- Tool-first processing
- Policy compliance
- No unsupported assumptions
- Minimal autonomous risk
- Human escalation for uncertain scenarios