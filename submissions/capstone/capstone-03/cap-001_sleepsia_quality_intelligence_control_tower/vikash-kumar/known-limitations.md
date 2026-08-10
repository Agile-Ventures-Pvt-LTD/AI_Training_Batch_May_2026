# ⚠️ Known Limitations
## Data Quality
The system depends on operational data quality.
Incomplete complaint records can reduce investigation quality.
Incorrect identifiers can prevent successful retrieval.
Missing batch information can limit product analysis.
Missing dates can limit pattern analysis.
Missing descriptions can limit similarity analysis.
Missing safety indicators can limit safety analysis.

## Connector Limitations
Excel access depends on connector configuration.
Word access depends on connector configuration.
Outlook access depends on connector configuration.
Authentication can affect tool execution.
Permissions can affect tool execution.
Tenant policies can affect available capabilities.
Licensing can affect available features.

## Agent Limitations
Specialists depend on the evidence returned to them.
Specialists may not produce reliable findings when source information is incomplete.
The Supervisor depends on specialist outputs.
Incorrect specialist routing can affect results.
Prompt and configuration changes can affect agent behavior.

## AI Limitations
AI can interpret evidence incorrectly.
AI-generated summaries should be validated.
AI should not be treated as a substitute for source records.
AI should not fabricate missing information.
AI should explicitly identify uncertainty.

## Topic Limitations
Topic 1 depends on successful complaint retrieval.
Topic 2 depends on specialist availability.
Topic 3 depends on CAPA information and tool availability.
Topic 4 depends on correctly identifying affected evidence areas.
Incorrect reassessment mapping can lead to unnecessary or incomplete reassessment.

## Operational Limitations
Excel updates depend on valid identifiers.
Word generation depends on available document actions.
Outlook communication depends on valid recipients and permissions.
Tool failures can interrupt the workflow.
Operational failures should be surfaced clearly.

## Knowledge Limitations
The system is limited by configured knowledge sources.
Outdated documentation can affect responses.
Incomplete documentation can create uncertainty.
Conflicting sources require configured precedence.
Unsupported information should not be invented.

## Safety Limitations
Safety analysis is evidence based.
The Safety Specialist does not provide medical advice.
Safety findings should be reviewed through the Supervisor.
The system should escalate appropriately when configured evidence indicates a concern.

## Fallback
When evidence is insufficient, the preferred behavior is controlled fallback.
The workflow should return Insufficient Evidence.
The workflow should stop or request additional evidence.
The system should not create unsupported conclusions.

## Environment Limitations
Copilot Studio behavior can vary by tenant.
Connector behavior can vary by environment.
Permissions can vary by user.
Published behavior can differ from development behavior.
Post-publishing smoke tests are therefore recommended.