# ⚡ Autonomous Trigger Design

> **P2-004 | NovaSphere BC/DR Readiness System**

---

# 🎯 Overview

The NovaSphere BC/DR Readiness System supports autonomous execution using **Microsoft Copilot Studio Triggers**.

Instead of requiring a user to manually start every assessment, the system continuously monitors incoming assessment requests and automatically initiates the BC/DR assessment workflow whenever a relevant change occurs.

This event-driven architecture minimizes manual effort while enabling near real-time assessment execution.

---

# 🚀 Trigger Objective

The trigger is responsible for automatically starting the Supervisor Agent whenever a new assessment request is detected.

The trigger performs three primary functions:

- Detect changes to assessment request files
- Activate the Supervisor Agent
- Initiate the complete BC/DR assessment workflow

---

# 🏗 Trigger Architecture

```text
                 Assessment Request
                      Excel File
                         │
                         ▼
               OneDrive Business
                         │
                         ▼
            When File Is Modified Trigger
                         │
                         ▼
          NovaSphere BCDR Supervisor
                         │
                         ▼
          Multi-Agent Assessment Workflow
                         │
      ┌──────────────────┼───────────────────┐
      ▼                  ▼                   ▼
 Business          Technical          Risk Assessment
 Analysis           Assessment
                         │
                         ▼
                  Microsoft Learn MCP
                         │
                         ▼
               Assessment Completion
                         │
      ┌──────────────────┼────────────────────┐
      ▼                  ▼                    ▼
 Assessment       Word Report         Email Notification
 Register
```

---

# 📂 Trigger Configuration

## Trigger Type

```
Autonomous Trigger
```

---

## Event

```
When a file is modified
```

---

## Storage Provider

```
OneDrive for Business
```

---

## Monitored Folder

```
/BCDR_Project
```

---

## Include Subfolders

```
Enabled
```

---

## Content Type Detection

```
Enabled
```

---

# 🔄 Workflow

Whenever the monitored folder detects a modification, the following sequence occurs.

```text
File Modified

        │

        ▼

Trigger Activated

        │

        ▼

Supervisor Agent Starts

        │

        ▼

Assessment Request Validation

        │

        ▼

Application Inventory Retrieval

        │

        ▼

Business Criticality Assessment

        │

        ▼

Recovery Requirement Validation

        │

        ▼

Technical Recovery Assessment

        │

        ▼

Microsoft Learn MCP

        │

        ▼

Risk Assessment

        │

        ▼

Remediation Planning

        │

        ▼

Report Generation

        │

        ▼

Assessment Register Update

        │

        ▼

Stakeholder Communication
```

---

# 🤖 Supervisor Responsibilities

Once activated, the Supervisor Agent:

✅ Validates the assessment request

✅ Retrieves the application inventory

✅ Coordinates all six specialist agents

✅ Collects technical evidence

✅ Validates Microsoft recommendations

✅ Calculates readiness

✅ Updates the assessment register

✅ Generates reports

✅ Prepares notifications

---

# 🎯 Why OneDrive Trigger?

Microsoft Copilot Studio currently provides native support for **OneDrive file events**.

Since the project stores assessment requests in an Excel workbook located in OneDrive, monitoring file modifications provides a simple event-driven mechanism to begin processing without requiring manual interaction.

This approach integrates naturally with the Microsoft 365 ecosystem used throughout the solution.

---

# ⚙ Trigger Scope

The trigger is intended to monitor assessment request updates.

Examples include:

- New assessment request added
- Existing request updated
- Assessment status modified
- Additional evidence uploaded

The Supervisor validates the modified content before continuing with the assessment.

---

# 🛡 Validation Before Execution

Before any specialist agent is invoked, the Supervisor verifies:

- Assessment Request exists
- Application ID is valid
- Application Inventory record exists
- Required business information is available
- Required recovery information is available

If validation fails, processing stops and the reason is returned.

---

# 🚨 Error Handling

The trigger itself does not perform business logic.

All validation occurs within the Supervisor Agent.

Possible outcomes include:

| Scenario | Behaviour |
|----------|-----------|
| Invalid Application ID | Assessment stops |
| Missing Inventory | Assessment stops |
| Missing Required Data | Supervisor requests additional information |
| MCP unavailable | Continue without Microsoft guidance |
| Connector failure | Return error and stop processing |

---

# 🔒 Security

The trigger inherits Microsoft 365 permissions.

Only authorized users with access to the monitored OneDrive location can initiate processing through file modifications.

No elevated permissions are granted by the trigger itself.

---

# 📈 Benefits

## ⚡ Automation

No manual initiation required.

---

## 🔄 Event Driven

Assessment starts immediately after relevant file updates.

---

## 🤖 Autonomous Processing

Supervisor coordinates the entire workflow automatically.

---

## 📊 Consistency

Every request follows the same assessment lifecycle.

---

## 📚 Integration

Works seamlessly with:

- OneDrive Business
- Excel Online
- Microsoft Learn MCP
- Word Online
- Outlook

---

# ⚠ Current Limitation

The current implementation monitors **file modifications** rather than **individual Excel row changes**.

As a result:

- Any update to the monitored workbook activates the trigger.
- The Supervisor validates the workbook contents before deciding whether a new assessment should begin.
- This prevents unnecessary processing but may result in additional trigger executions if unrelated changes are made.

In a production deployment, the trigger could be replaced with a more granular event source such as **Microsoft Dataverse**, where assessments can start only when a new assessment record is created or updated.

---

# 🚀 Future Enhancements

Possible improvements include:

- Microsoft Dataverse row triggers
- SharePoint List triggers
- Microsoft Forms submission trigger
- ServiceNow incident trigger
- Azure Event Grid integration
- Azure Service Bus integration

These enhancements would enable more precise event-driven execution while reducing unnecessary trigger activations.

---

# 📸 Evidence

Include screenshots demonstrating:

- Trigger configuration
- OneDrive connection
- Folder selection
- Trigger activation
- Supervisor execution after trigger

---

# ✅ Summary

The autonomous trigger transforms the NovaSphere BC/DR Readiness System from a manually initiated assistant into an event-driven assessment platform.

By integrating OneDrive Business with Microsoft Copilot Studio, the solution automatically detects relevant assessment updates and initiates a complete multi-agent BC/DR assessment workflow with minimal user intervention.