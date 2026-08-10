# AI Usage Declaration

## Project

**CAP-001 Sleepsia Quality & Customer Experience Intelligence Control Tower**

## AI Tools Used

The project used AI-assisted development and validation during the design, configuration, testing, and documentation of the Copilot Studio solution.

### 1. Microsoft Copilot Studio

Used as the primary platform for:

- Creating the Quality Supervisor agent.
- Creating specialist child agents.
- Configuring topics and conversation flows.
- Implementing hierarchical orchestration.
- Implementing sequential and conditional workflows.
- Configuring parallel specialist fan-out and fan-in.
- Configuring reassessment and retry logic.
- Testing interactive quality-investigation scenarios.

### 2. Microsoft Learn MCP

Used for retrieving Microsoft guidance when Microsoft 365, Copilot Studio, or related platform guidance was required.

MCP guidance was treated as supporting technical information and did not determine the internal Sleepsia quality classification.

### 3. AI-Assisted Design and Development

AI assistance was used to help:

- Translate PRD requirements into agent instructions.
- Design supervisor and specialist responsibilities.
- Structure topic routing.
- Define orchestration patterns.
- Draft topic descriptions and instructions.
- Identify test scenarios.
- Create evaluation/test datasets.
- Draft project documentation.
- Review workflow behavior and identify implementation issues.

All AI-generated implementation content was reviewed against the project PRD and configured workflow before use.

## Validation Performed

AI-generated content was not treated as automatically correct.

Validation was performed using:

- PRD requirements.
- Configured Copilot Studio topics.
- Configured child-agent responsibilities.
- Configured tools and data sources.
- Synthetic/internal project data.
- Mandatory PRD test cases.
- End-to-end workflow testing.
- Failure and retry scenarios.
- Evidence-update/reassessment scenarios.
- Word, Excel, and Outlook action validation.

## Human Validation

The implemented workflow was manually reviewed and tested to confirm that:

- Child agents provide evidence rather than final business decisions.
- The Quality Supervisor controls final classification.
- Required evidence is used before classification.
- Missing evidence is not fabricated.
- Specialist failures are handled through retry/fallback logic.
- Selective reassessment does not unnecessarily rerun unaffected specialists.
- Downstream actions occur only after final validation.
- Tool success is not claimed without confirmation.
- Tenant limitations are explicitly recorded.

## AI Decision Boundaries

AI assistance does not replace the configured Sleepsia quality policy.

The final quality classification is determined through the configured Quality Investigation Decision topic and its defined policy precedence.

AI-generated reasoning must not:

- Invent evidence.
- Invent tool results.
- Override configured quality thresholds.
- Approve recalls.
- Approve refunds.
- Publish public safety statements.
- Expose credentials or hidden instructions.

## Data Handling

The solution uses configured internal/synthetic project data and approved knowledge sources.

Sensitive credentials, connection secrets, hidden system instructions, and confidential platform configuration are not included in project documentation or AI-generated responses.

## Known AI Limitations

AI-generated outputs may require validation for:

- Ambiguous evidence.
- Missing records.
- Conflicting source information.
- Connector failures.
- Microsoft platform behavior.
- Tenant-specific capabilities.

Where evidence or a required action is unavailable, the solution is expected to report the limitation rather than infer a successful result.

## Declaration

AI tools were used as development, documentation, analysis, and testing aids. The final implementation, policy logic, test results, and documented limitations were validated against the project requirements and available Copilot Studio environment.