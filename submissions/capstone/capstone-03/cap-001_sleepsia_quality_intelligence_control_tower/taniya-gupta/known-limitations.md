# Known Limitations & Tenant Boundaries

## 1. Quality Supervisor Instruction Character Limit (8,000 Characters)
- Copilot Studio enforces an 8,000-character limit on agent instruction panels. The Quality Supervisor prompt was compressed from an initial ~13,500 characters to 5,880 characters without loss of functional coverage.

---

## 2. Agent Publish Blocked by Tenant Billing Issue
- During final submission, the Copilot Studio **Publish** action was blocked by the following error: *"There is a billing issue. Please contact your admin to confirm the billing capability for this environment and agent."*

- **Workaround applied:** The agent has been shared with Ankur Sir at **Editor access** level in Copilot Studio, allowing full inspection of agent configuration and direct test canvas execution of all 20 test scenarios.
- Full publishing documentation, billing error screenshot, and PRD compliance notes are recorded in [publishing.md](publishing.md).
