# 🚀 Publishing
## Platform
The solution is implemented in Microsoft Copilot Studio.
Publishing makes the configured agent available through supported channels.
Publishing should happen only after testing.

## Build Process
Create the Supervisor.
Create or connect specialist agents.
Create the four mandatory topics.
Configure Excel tools.
Configure Word tools.
Configure Outlook tools.
Configure required variables.
Configure conditions.
Configure topic routing.
Test each component.
Test the complete workflow.
Review errors.
Retest corrected flows.
Publish the agent.

## Topic Validation
Topic 1 should be tested with valid data.
Topic 1 should be tested with incomplete data.
Topic 2 should be tested with specialist findings.
Topic 3 should be tested with CAPA-required outcomes.
Topic 4 should be tested with new evidence.
Fallback paths should be tested.
Tool failures should be considered.

## Agent Validation
The Supervisor should be able to identify the relevant topic.
Child agents should be connected.
Child agents should have clear responsibilities.
Child agents should return evidence.
Child agents should not make unsupported final decisions.

## Tool Validation
Excel retrieval should work.
Excel updates should work.
Word generation should work.
Outlook communication should work.
Permissions should be verified.
Connector authentication should be verified.

## Publishing Checklist
Save the solution.
Check topic configuration.
Check agent connections.
Check tool connections.
Run topic tests.
Run end-to-end tests.
Review errors.
Confirm expected outputs.
Publish.

## Post-Publishing
Run a smoke test.
Verify the published agent responds correctly.
Verify tool access.
Verify specialist routing.
Verify fallback behavior.
Verify final operational outputs.
Record any environment-specific issues.

## Deployment Principle
Publishing should not be treated as the end of validation.
The published environment should be tested independently.