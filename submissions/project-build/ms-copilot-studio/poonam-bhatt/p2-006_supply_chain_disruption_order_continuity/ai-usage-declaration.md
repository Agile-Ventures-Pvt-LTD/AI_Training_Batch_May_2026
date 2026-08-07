# AI Usage Declaration

## Project

P2-006 Supply Chain Disruption / Order Continuity

## Purpose of AI Usage

AI capabilities are used within the solution to support the assessment and orchestration of supply chain disruptions. The AI agents interpret structured disruption information, coordinate specialist assessments, apply predefined decision rules, consolidate assessment results, and produce a final response for authorized stakeholders.

The solution is designed so that AI supports the assessment and orchestration process while business rules, source data, approval requirements, and configured workflow controls remain the basis for operational decisions.

## AI Components Used

The solution uses a supervisor-agent and specialist-agent architecture.

### Supervisor Agent

The Supervisor Agent acts as the primary orchestrator for the disruption assessment workflow.

Its responsibilities include:

- Receiving or initiating a disruption assessment.
- Retrieving the relevant pending disruption record.
- Validating required disruption information.
- Updating the disruption status when validation succeeds.
- Calling the required specialist agents.
- Consolidating specialist assessment results.
- Determining the appropriate recovery strategy.
- Performing approval and reassessment checks.
- Coordinating the final response.
- Initiating the configured document and stakeholder-notification steps when the workflow reaches the applicable stage.

The Supervisor Agent does not independently invent missing source information.

### Specialist Agents

Specialist agents are used to evaluate specific aspects of a disruption.

The configured specialist assessments include:

- Inventory Impact Specialist
- Alternate Supplier Specialist
- Customer & Order Impact Specialist
- Commercial Impact Specialist

Each specialist is responsible for its defined assessment area and uses the authorized data sources and configured logic available to it.

## AI-Assisted Reasoning

AI is used to interpret and consolidate information returned by the configured tools and specialist agents.

Examples include:

- Interpreting disruption information.
- Identifying relationships between disruption, supplier, SKU, inventory, purchase-order, customer, and commercial information.
- Summarizing evidence returned by source systems.
- Identifying missing or conflicting evidence.
- Consolidating specialist outputs.
- Presenting the resulting assessment in a structured response.

AI reasoning does not replace the configured decision rules.

Where the solution contains explicit thresholds, status transitions, validation conditions, approval conditions, or recovery-strategy rules, those rules are implemented through the configured topics, conditions, variables, tools, and orchestration logic.

## Use of Source Data

The solution is designed to use authorized structured data sources rather than relying on unsupported assumptions.

Source data is used to support activities such as:

- Disruption intake validation.
- Inventory assessment.
- Supplier and alternate-supplier assessment.
- Customer and order impact assessment.
- Commercial impact assessment.
- Recovery strategy determination.
- Approval and reassessment decisions.

When required source information is unavailable or inconsistent, the assessment should identify the evidence limitation rather than fabricate a value.

For example, if a SKU cannot be found in the authorized inventory or master-data source, the solution should treat the resulting inventory assessment as insufficient evidence rather than assuming an inventory quantity.

## Business Rules and Deterministic Logic

The solution contains deterministic logic for important workflow decisions.

Examples include:

- Required disruption fields must be present.
- The disruption must be in the expected Pending state before initial assessment.
- Validated disruptions move to In Assessment.
- Existing inventory can result in an existing-stock recovery strategy when configured conditions are satisfied.
- An approved alternate supplier can result in an alternate-supplier recovery strategy.
- An unapproved alternate supplier requires manual review or qualification.
- No viable recovery route can result in management escalation.
- Approval is required when configured cost, expedite, supplier-qualification, or safety-stock conditions are met.
- Reassessment is limited according to the configured reassessment-cycle rule.

These controls are intended to prevent unrestricted AI decision-making for critical workflow transitions.

## Human Approval and Oversight

The solution recognizes that certain decisions require human involvement.

Where the configured approval conditions are met, the workflow can set the disruption to an approval-related status and identify the required approver.

The AI agent must not fabricate human approval.

The system should not represent an approval as completed merely because an AI agent has determined that approval is required.

Human oversight therefore remains part of the workflow for decisions requiring authorization.

## Document Generation

The final response/report document is generated using the configured Microsoft Word document capability when the workflow reaches the document-generation stage.

The AI may provide structured assessment content for the document, including:

- Disruption information.
- Validation outcome.
- Specialist assessment results.
- Recovery strategy.
- Risk and rationale.
- Approval information where applicable.
- Final assessment summary.

The document-generation process is controlled by the configured workflow and tool rather than by the AI simply claiming that a document was created.

## Stakeholder Notification

The solution includes a configured notification step for authorized stakeholder communication.

AI may generate or structure the notification content based on the completed assessment.

The actual notification is expected to be performed through the configured communication tool and connection.

The agent should not claim that an email or notification was successfully sent unless the configured tool execution confirms successful completion.

## Handling Missing or Conflicting Evidence

The solution is designed to identify insufficient evidence and data conflicts.

Examples include:

- Missing SKU records.
- Missing inventory records.
- Missing supplier information.
- Purchase orders that do not match the disruption SKU.
- Purchase orders associated with a different supplier.
- Missing customer or order information.
- Missing commercial information.
- Inconsistent dates or quantities.

When evidence is insufficient, the solution should report the limitation and avoid inventing unsupported values.

## AI Limitations

The solution has several limitations that are important to recognize.

AI-generated summaries can depend on the quality and completeness of the source information.

Tool failures can prevent an assessment step from completing.

For example, a connector failure may prevent a specialist from retrieving required Excel data. In such cases, the resulting workflow should not treat the unavailable data as confirmed evidence.

Similarly, document generation and stakeholder notification depend on the successful execution of their configured tools and valid connections.

## Validation and Testing

The solution is tested using defined disruption scenarios.

Testing focuses on:

- Correct retrieval of disruption records.
- Correct validation of required fields.
- Correct status transitions.
- Correct specialist-agent invocation.
- Correct application of recovery-strategy rules.
- Correct approval and reassessment behavior.
- Correct handling of insufficient evidence.
- Correct final response generation.
- Correct execution of configured document-generation and notification steps.

Test results are used to identify configuration, connector, orchestration, and data-quality issues.

## Responsible AI Considerations

The solution follows the following principles:

1. **Evidence-based assessment**  
   Decisions should be supported by available authorized data.

2. **No fabricated evidence**  
   Missing values should not be invented.

3. **Rule-based control**  
   Important workflow decisions are constrained by configured business rules.

4. **Human oversight**  
   Human approval remains required where configured.

5. **Traceability**  
   Assessment outputs should identify the relevant evidence, status, rationale, and blocking issues.

6. **Controlled automation**  
   Automation is used to coordinate the assessment workflow, while approval-sensitive actions remain subject to configured controls.

## Declaration

AI is used as an orchestration, reasoning, summarization, and decision-support capability within the P2-006 Supply Chain Disruption / Order Continuity solution.

The implementation combines AI agents with deterministic business rules, structured source data, configured tools, and human approval controls.

The AI is not intended to independently create unsupported facts, fabricate approvals, or bypass configured business controls.

The final assessment is dependent on the quality of the source data, successful execution of connected tools, and the workflow configuration implemented in the solution.
```
