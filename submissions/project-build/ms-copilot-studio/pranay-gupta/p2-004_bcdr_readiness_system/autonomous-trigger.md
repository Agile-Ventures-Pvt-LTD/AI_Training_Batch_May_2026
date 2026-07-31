# Autonomous Trigger

## Overview

The BCDR Readiness Assessment System uses an **Autonomous Trigger** to automatically initiate a BC/DR readiness assessment when a new assessment request is received.

The trigger removes the need for manual intervention and starts the assessment workflow by invoking the BCDR Supervisor Agent.

---

# Purpose

The Autonomous Trigger is responsible for:

* Detecting a new BC/DR assessment request.
* Starting the assessment workflow.
* Passing the assessment details to the Supervisor Agent.
* Initiating the multi-agent assessment process.

---

# Trigger Configuration

| Property      | Value                           |
| ------------- | ------------------------------- |
| Trigger Name  | BCDR Assessment Request Trigger |
| Trigger Type  | Autonomous Event Trigger        |
| Invoked Agent | BCDR Supervisor Agent           |

---

# Trigger Input

The trigger receives the assessment request containing:

* Assessment ID
* Application ID
* Assessment Type
* Priority
* Request Date
* Requested By

These values are passed to the BCDR Supervisor Agent to begin the assessment.

---

# Assessment Workflow

```text id="3r1j9q"
New Assessment Request
            │
            ▼
Autonomous Trigger
            │
            ▼
BCDR Supervisor Agent
            │
            ▼
Retrieve Assessment Data
            │
            ▼
Invoke Specialist Agents
            │
            ▼
Generate Final Assessment
```

---

# Trigger Responsibilities

After receiving an assessment request, the trigger:

1. Starts the BC/DR assessment process.
2. Passes the assessment information to the Supervisor Agent.
3. Allows the Supervisor Agent to coordinate all specialist agents.
4. Waits for the assessment workflow to complete.

The trigger does not perform any assessment or validation activities.

---

# Benefits

Using an Autonomous Trigger enables:

* Automatic assessment initiation.
* Consistent execution of the assessment workflow.
* Reduced manual effort.
* Standardized processing of assessment requests.

---

# Summary

The Autonomous Trigger serves as the entry point for the BC/DR Readiness Assessment System by automatically initiating the assessment workflow and transferring control to the BCDR Supervisor Agent for orchestration.
