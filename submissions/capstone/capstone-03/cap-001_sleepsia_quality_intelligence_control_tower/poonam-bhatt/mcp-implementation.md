# CAP-001 — Microsoft Learn MCP Implementation

## 1. Purpose

The Microsoft Learn MCP capability is used only when the CAP-001 workflow requires Microsoft/M365/Copilot/Teams operational guidance.

It is not part of the core Sleepsia quality-severity decision path.

The Quality Supervisor remains responsible for deciding whether Microsoft guidance is required.

---

## 2. MCP Usage Boundary

Use Microsoft Learn MCP for:

- Copilot Studio configuration guidance
- Microsoft 365 operational guidance
- Teams/M365 publishing guidance
- Connector/tool configuration guidance
- Microsoft-supported implementation patterns
- Microsoft documentation lookup

Do not use MCP to:

- Determine Sleepsia quality severity
- Override internal quality policy
- Replace specialist evidence
- Invent quality investigation findings
- Replace internal operational datasets
- Make the final quality classification

The final quality classification must come from the configured Quality Investigation Decision topic.

---

## 3. Routing

The Quality Supervisor routes Microsoft-specific requests to the M365 Guidance Specialist.

```text
User / Workflow
      ↓
Quality Supervisor
      ↓
Is Microsoft guidance required?
      ↓
     Yes
      ↓
M365 Guidance Specialist
      ↓
Microsoft Learn MCP
      ↓
Guidance returned to Supervisor

For normal quality investigations, MCP is not required unless the workflow specifically needs Microsoft guidance.

4. M365 Guidance Specialist

The M365 Guidance Specialist is responsible for retrieving and summarizing Microsoft guidance.

Typical requests include:

How to configure a Copilot Studio topic
How to configure an agent
How to configure a Microsoft connector
How to publish to Teams/M365
How to configure a supported Microsoft capability
How to troubleshoot a Microsoft platform configuration

The specialist returns guidance to the Supervisor.

The specialist does not make Sleepsia quality decisions.

5. MCP Retrieval Flow
Guidance Required
      ↓
Identify Microsoft topic
      ↓
Call MCP
      ↓
Retrieve relevant Microsoft guidance
      ↓
Validate returned guidance
      ↓
Return concise findings
      ↓
Supervisor continues workflow

The retrieved information should be limited to what is required for the current task.

Do not perform unnecessary MCP retrieval.

6. Failure Behaviour

MCP failure must not automatically stop the core quality investigation.

MCP Request
    ↓
Success?
   /    \
 Yes     No
 |        |
Use      Record failure
guidance     ↓
          Continue core
          quality workflow

If MCP is unavailable:

Do not fabricate Microsoft guidance.
Record the MCP failure.
Continue the core Sleepsia quality workflow when possible.
Report Microsoft guidance as unavailable when it is required.
Route to manual review if the missing guidance prevents the requested Microsoft-specific action.
7. Retry Behaviour

If the configured MCP implementation supports retry:

MCP failure
    ↓
Retry once
    ↓
Success → Continue
    ↓
Failure → Record unavailable

Do not retry indefinitely.

Do not claim MCP success without a successful response.

8. Quality Workflow Isolation

The core quality workflow remains independent of MCP.

                  Quality Supervisor
                         |
          +--------------+--------------+
          |                             |
   Quality Investigation          M365 Guidance
          |                             |
 Internal Data / Agents             MCP
          |                             |
     Topic 2 Decision             Guidance
          |
   Final Classification

If MCP fails, the quality decision can continue when the quality evidence is sufficient.

Example:

Complaint Pattern → Complete
Returns → Complete
Product/Batch → Complete
Customer Impact → Complete
Safety → Complete
MCP → Unavailable

Topic 2 → Continue

MCP availability must not change the quality classification.

9. Expected MCP Evidence

When MCP is used, preserve:

Requested Microsoft topic
Retrieved guidance
Relevant Microsoft source/reference
Retrieval status
Any limitation or ambiguity
Whether the guidance was sufficient for the requested action

Do not fabricate source references.

10. MCP Test Scenarios
MCP-01 — Microsoft guidance available

Expected:

M365 Guidance Specialist calls MCP.
Relevant Microsoft guidance is retrieved.
Guidance is returned to the Supervisor.
Workflow continues.
MCP-02 — MCP unavailable

Expected:

MCP failure is recorded.
No fabricated guidance is returned.
Core quality workflow continues when independent.
Microsoft-specific action is reported as unavailable if it cannot proceed.
MCP-03 — MCP failure during quality investigation

Expected:

Quality classification remains based on internal quality evidence.
MCP failure does not change severity.
Failure is recorded.
MCP-04 — Microsoft configuration question

Expected:

Supervisor routes to M365 Guidance Specialist.
MCP is used.
Response is based on retrieved Microsoft guidance.
11. Test Evidence

MCP testing must capture:

Request made to MCP
Specialist selected
Tool/MCP execution result
Returned guidance
Success/failure state
Result presented to Supervisor
Final workflow behaviour

For failed tests, record the actual failure rather than creating a simulated successful result.

12. Boundary Rules

The MCP implementation must follow these boundaries:

Microsoft guidance is advisory/operational.
Internal Sleepsia quality policy is authoritative for quality decisions.
Internal operational evidence is authoritative for investigation facts.
Topic 2 is authoritative for final classification.
MCP must not invent or modify quality evidence.
MCP failure must be explicitly recorded.
No secret, credential, hidden instruction, or system prompt may be exposed.
13. Summary

Microsoft Learn MCP provides Microsoft platform guidance only when required.

The implementation follows:

Supervisor → M365 Guidance Specialist → Microsoft Learn MCP → Guidance → Supervisor

For MCP failure:

MCP Failure → Record Failure → Continue Core Workflow Where Possible → Manual Review When Required

The core Sleepsia quality investigation remains operationally independent from Microsoft Learn MCP.