# known-limitations.md

# Known Limitations

## Outlook Connector

- Requires valid Microsoft 365 authentication.
- Cannot process emails without mailbox access.
- Subject filter must match the configured trigger.

---

## Excel Online

- Dependent on workbook availability.
- Table structure must remain unchanged.
- Connector failures stop operational validation.

---

## Microsoft Word

- Report generation depends on connector availability.
- Large documents may increase processing time.

---

## Copilot Studio

- Autonomous decisions depend on available tools and knowledge.
- Business rules should remain in external reference tables.
- Connector failures require retry or manual intervention.

---

## Tenant Constraints

- Agent is available only within the configured Microsoft tenant.
- Requires appropriate Microsoft 365 licenses and permissions.
- External access depends on tenant sharing policies.

---

## Autonomous Orchestration

- Tool execution order is determined by the orchestration engine.
- Long-running connector operations may affect execution time.
- Unexpected connector failures can interrupt autonomous processing.

---

## Assumptions

The solution assumes:

- Operational Excel tables contain valid data.
- Outlook, Excel, and Word connectors are configured correctly.
- Knowledge sources are available.
- Users have the required permissions.
- All test data is synthetic and intended for evaluation only.