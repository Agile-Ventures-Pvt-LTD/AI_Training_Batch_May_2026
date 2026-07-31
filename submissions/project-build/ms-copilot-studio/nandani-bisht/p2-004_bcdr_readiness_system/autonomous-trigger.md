# Autonomous Trigger

## Overview

The Autonomous Trigger is responsible for initiating the BC/DR Readiness Assessment without requiring manual interaction with the Copilot agent.

The solution monitors a designated **OneDrive folder** for newly uploaded assessment request files. When a new file is detected, the trigger automatically invokes the BCDR Supervisor Agent, which begins the multi-agent assessment workflow.

This enables an event-driven assessment process that minimizes manual effort and supports repeatable, automated evaluations.

---

# Objective

The autonomous trigger enables:

- Automatic assessment initiation
- Elimination of manual Copilot interaction
- Event-driven processing
- Consistent execution of the assessment workflow
- Reduced operational effort

---

# Trigger Architecture

```
              User Uploads Assessment File
                          │
                          ▼
                 OneDrive Folder
                          │
                          ▼
           Power Automate Trigger
      (When a file is created)
                          │
                          ▼
              BCDR Supervisor Agent
                          │
                          ▼
         Multi-Agent Assessment Workflow
                          │
                          ▼
       Word │ Excel │ Outlook Outputs
```

---

# Trigger Configuration

The assessment process starts when a new assessment request is uploaded to the monitored OneDrive folder.

## Trigger Type

**When a file is created (OneDrive for Business)**

## Trigger Source

Microsoft OneDrive

## Trigger Condition

A new assessment request file is added to the configured folder.

---

# Assessment Workflow

The automated workflow executes the following sequence:

### Step 1

User uploads a new assessment request.

↓

### Step 2

Power Automate detects the new file.

↓

### Step 3

The flow invokes the BCDR Supervisor Agent.

↓

### Step 4

Supervisor validates the assessment request.

↓

### Step 5

Supervisor delegates work to specialist agents.

↓

### Step 6

Technical Recovery Specialist retrieves Microsoft documentation using MCP.

↓

### Step 7

Supervisor consolidates assessment findings.

↓

### Step 8

Reporting Specialist generates:

- Word Assessment Report
- Excel Assessment Register entry
- Outlook notification

---

# Trigger Inputs

The uploaded assessment request typically contains:

- Assessment ID
- Application Name
- Business Owner
- Business Unit
- Criticality
- Recovery Objectives
- Infrastructure Information
- Backup Configuration

---

# Autonomous Execution

Once the trigger activates:

- No manual intervention is required.
- The Supervisor coordinates all specialist agents.
- Specialist outputs are automatically consolidated.
- Final deliverables are generated.

---

# Integration with Supervisor Agent

The trigger invokes only one agent:

**BCDR Supervisor Agent**

The Supervisor is responsible for:

- Request validation
- Specialist selection
- Context passing
- Assessment consolidation
- Report generation

The trigger never communicates directly with specialist agents.

---

# Error Handling

The trigger includes basic error handling to ensure reliable execution.

## Missing File

If no assessment file is available:

- Workflow does not execute.

---

## Invalid Assessment

If required information is missing:

- Supervisor records validation issues.
- Assessment continues where possible.

---

## MCP Failure

If Microsoft Learn MCP cannot retrieve documentation:

- Technical Recovery Specialist records the failure.
- Supervisor completes the assessment without unsupported Microsoft evidence.

---

## Connector Failure

If Word, Excel, or Outlook connectors fail:

- Assessment findings are preserved.
- Connector failure is logged.
- Manual follow-up may be required.

---

# Benefits

The autonomous trigger provides several operational advantages:

- Fully automated assessment initiation
- Consistent execution
- Reduced manual effort
- Faster processing
- Scalable workflow
- Improved repeatability

---

# Limitations

Current limitations include:

- Depends on OneDrive availability.
- Assessment begins only after file upload.
- Connector failures may require manual intervention.
- Trigger reliability depends on Microsoft 365 services.

---

# Screenshots

The following screenshots are included in the repository:

- `autonomous-trigger.png`
- `supervisor-agent.png`
- `specialist-delegation.png`

These screenshots demonstrate:

- Trigger configuration
- Automatic Supervisor invocation
- Multi-agent orchestration

---

# Evaluation Mapping

| Evaluation Requirement | Status |
|------------------------|--------|
| Autonomous trigger implementation | ✔ |
| Supervisor invocation | ✔ |
| Automatic assessment workflow | ✔ |
| Multi-agent orchestration | ✔ |
| Error handling documented | ✔ |

---

# Conclusion

The autonomous trigger provides an event-driven mechanism for initiating BC/DR readiness assessments. By automatically invoking the BCDR Supervisor Agent when a new assessment request is uploaded, the solution eliminates manual execution steps and enables a scalable, repeatable, and autonomous assessment workflow integrated with Microsoft Copilot Studio and Microsoft 365 services.