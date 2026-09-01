# Autonomous Trigger Configuration (`autonomous-trigger.md`)

## Trigger Architecture

The BC/DR Readiness System operates completely autonomously without requiring manual interaction in the Copilot Studio chat widget.

```
[OneDrive File Modification Event]  ---> [Event Trigger] --> [BC/DR Supervisor Agent]
```

---

## Supported Autonomous Trigger Types

### Event-Driven Trigger: "When a file is modified" (OneDrive for Business)
- **Trigger Location**: OneDrive `/BCDR` folder
- **Monitored File**: `P2-004_BCDR_Lab_Data.xlsx` or `Assessment_Requests.txt`
- **Payload Extraction**: Extracts `ApplicationID` or application list automatically upon file update.

---

## Dynamic Filter Query Configuration
To ensure zero manual prompts during autonomous execution, the Excel `List rows present in a table` tool is configured with dynamic filter resolution:
- **Filter Query**: `ApplicationID eq '{ApplicationID}'`
- **Behavior**: Resolves `ApplicationID` from the incoming event payload without prompting the user.
