# Autonomous Trigger

## Overview

The solution operates autonomously using a **Power Automate Recurrence Trigger** that periodically initiates the Supply Continuity Assessment workflow.

This eliminates the need for manual intervention and enables continuous monitoring of supply disruption requests.

---

# Trigger Type

**Power Automate – Recurrence Trigger**

The trigger executes at a predefined schedule and invokes the **Supply Continuity Supervisor**.

---

# Execution Flow

```
Recurring Trigger

        │

        ▼

Supply Continuity Supervisor

        │

        ▼

Retrieve Pending Disruption

        │

        ▼

Validate Disruption

        │

        ▼

Specialist Assessments

        │

        ▼

Recovery Planning

        │

        ▼

Reporting & Communication

        │

        ▼

Workflow Complete
```

---

# Trigger Responsibilities

The autonomous trigger is responsible for:

- Starting the workflow automatically
- Invoking the Supervisor Agent
- Eliminating manual execution
- Supporting continuous disruption monitoring

---

# Prompt Sent to the Supervisor

```
Start the Supply Continuity Assessment workflow.

Retrieve the oldest disruption request whose Status is "Pending" from the Disruption_Requests table.

Validate the disruption request and execute the complete assessment autonomously according to the Supervisor instructions.
```

---

# Benefits

- Fully autonomous execution
- Scheduled monitoring
- Reduced manual effort
- Consistent workflow execution
- Improved operational efficiency

---

# Future Enhancements

Future implementations may support additional trigger mechanisms such as:

- Event-based ERP notifications
- Microsoft Teams commands
- REST API requests
- Service Bus events
- Azure Event Grid
- Webhook integrations