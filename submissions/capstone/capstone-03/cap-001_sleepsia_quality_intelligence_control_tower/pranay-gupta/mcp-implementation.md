# Microsoft Learn MCP Implementation

## 1. Scope
Microsoft Learn MCP is implemented only for the **M365 Guidance Specialist**.

It exists to provide current Microsoft product and implementation guidance, not Sleepsia product-quality evidence.

## 2. Configuration

| Setting | Configuration |
|---|---|
| Server Name | Microsoft Learn MCP Server |
| Server URL | https://learn.microsoft.com/api/mcp |
| Authentication | None |
| Agent | M365 Guidance Specialist |

## 3. Appropriate Use
Use MCP for questions such as:
- Copilot Studio configuration.
- Microsoft Teams configuration.
- Microsoft 365 behavior.
- Connector/tool guidance.
- Other current Microsoft implementation guidance supported by Microsoft Learn.

## 4. Prohibited Use
MCP must not be used to:
- Determine Sleepsia complaint severity.
- Override the Sleepsia Quality Policy.
- Decide CAPA requirements.
- Determine safety classification.
- Replace operational evidence.
- Invent unavailable Microsoft guidance.

## 5. Failure Handling
If MCP is unavailable, the M365 Guidance Specialist should return:

`Microsoft guidance unavailable - manual review`

The core quality workflow must continue independently.

## 6. Architectural Boundary
```text
M365 Guidance Specialist
          ↓
Microsoft Learn MCP
          ↓
Microsoft operational guidance
```

This path remains separate from the quality-decision evidence path.

## 7. Validation
Connection and failure behavior will be formally tested during the final testing phase.
