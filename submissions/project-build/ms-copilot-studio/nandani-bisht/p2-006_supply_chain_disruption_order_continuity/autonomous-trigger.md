# autonomous-trigger.md

# Autonomous Trigger Design

## P2-006 – Supply Chain Disruption Order Continuity

---

# Overview

The Supply Chain Disruption Order Continuity solution is designed to execute autonomously whenever a new disruption request is detected.

Instead of requiring a user to manually start the workflow, an automated trigger periodically checks for new disruption requests and initiates the Supply Continuity Supervisor.

This enables continuous monitoring and rapid response to supply chain events.

---

# Objective

The autonomous trigger is responsible for:

- Monitoring incoming disruption requests
- Detecting pending disruptions
- Starting the Supervisor Agent
- Preventing duplicate processing
- Recording execution status
- Handling trigger failures safely

---

# Trigger Type

The solution uses a scheduled trigger based on Microsoft Copilot Studio automation.

### Trigger Characteristics

- Scheduled execution
- Automatic polling
- No user interaction required
- Enterprise workflow initiation

---

# Trigger Workflow

```text
Scheduled Trigger
        │
        ▼
Read Excel Table
        │
        ▼
Pending Disruption Found?
        │
   ┌────┴────┐
   │         │
 No         Yes
   │         │
   ▼         ▼
Exit     Invoke Supervisor
                 │
                 ▼
         Topic 1 – Validation
                 │
                 ▼
        Continue Workflow
```

---

# Polling Logic

At every scheduled interval, the trigger performs the following actions.

### Step 1

Connect to Excel Online.

---

### Step 2

Read the **Disruption Requests** table.

---

### Step 3

Search for records where:

```text
Status = Pending
```

---

### Step 4

If no pending disruptions exist:

```text
Exit safely
```

---

### Step 5

If a pending disruption exists:

```text
Invoke Supply Continuity Supervisor
```

---

# Trigger Conditions

The trigger starts the workflow only if all conditions are satisfied.

Required conditions:

- Status = Pending
- Valid Disruption ID
- Valid Supplier
- Valid SKU
- Not already being processed

If any validation fails, the workflow terminates without invoking the Supervisor Agent.

---

# Duplicate Prevention

Before starting a workflow, the trigger checks whether the disruption has already been processed.

Rules:

- Prevent duplicate execution
- Ignore completed disruptions
- Ignore requests already in progress

This ensures that the same disruption is never processed multiple times.

---

# Data Source

The trigger reads disruption requests from:

### Excel Online (Business)

Primary table:

```text
DisruptionRequests
```

Typical fields:

- Disruption ID
- Supplier ID
- SKU
- Purchase Order
- Status
- Recovery Date

---

# Supervisor Invocation

When a valid disruption is found, the trigger passes the following information to the Supervisor Agent.

Inputs:

- Disruption ID
- Supplier ID
- SKU
- Purchase Order
- Recovery Date
- Status

The Supervisor Agent then begins the orchestration workflow.

---

# Failure Handling

The trigger includes basic failure handling.

Possible failures:

### Excel unavailable

Action:

- Stop execution
- Log failure

---

### No pending disruptions

Action:

- Exit safely

---

### Invalid disruption data

Action:

- Do not invoke Supervisor
- Record validation failure

---

### Duplicate disruption

Action:

- Ignore duplicate
- Continue monitoring

---

# Trigger Frequency

Recommended execution interval:

| Environment | Suggested Frequency |
|-------------|---------------------|
| Development | Every 5–10 minutes |
| Testing | Every 2–5 minutes |
| Production | Every 15 minutes (or based on business needs) |

The schedule can be adjusted according to organizational requirements.

---

# Integration with Workflow

```text
Scheduled Trigger
        │
        ▼
Excel Online
        │
        ▼
Pending Request
        │
        ▼
Supply Continuity Supervisor
        │
        ▼
Topic 1
        │
        ▼
Recovery Planning
        │
        ▼
Topic 2
        │
        ▼
Topic 3
        │
        ▼
Reporting Specialist
```

---

# Benefits

The autonomous trigger provides:

- Continuous monitoring
- Faster disruption response
- Reduced manual effort
- Consistent workflow initiation
- Enterprise automation
- Improved operational efficiency

---

# Best Practices

Recommended implementation guidelines:

- Validate all records before execution.
- Prevent duplicate processing.
- Log trigger failures for troubleshooting.
- Use configurable polling intervals.
- Separate trigger logic from business logic.
- Keep the trigger lightweight and focused only on workflow initiation.

---

# Summary

The autonomous trigger serves as the entry point for the Supply Chain Disruption Order Continuity solution.

By continuously monitoring disruption requests and automatically invoking the Supervisor Agent, it enables an autonomous, event-driven workflow that reduces manual intervention and improves response times across the supply chain.

---

# Version

**Version:** 1.0

**Status:** Completed