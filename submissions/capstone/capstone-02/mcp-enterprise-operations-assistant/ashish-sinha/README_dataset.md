# Capstone Project Build 2 - Enterprise Operations Dataset

This package contains all local data required by the MCP-Based Enterprise Operations Assistant capstone.

## Files

- `data/service_health.json` - service health records and operational incidents.
- `data/tickets.db` - SQLite support-ticket database.
- `data/changes.json` - recent change-management records.
- `data/sample_queries.json` - eight mandatory queries for end-to-end validation.
- `scripts/create_ticket_db.py` - recreates `data/tickets.db`.

No external operational API is required.

## Source-of-truth mapping

| MCP server | Data source |
|---|---|
| Service Health MCP Server | `data/service_health.json` |
| Support Ticket MCP Server | `data/tickets.db` |
| Change Management MCP Server | `data/changes.json` |

## Recreate the ticket database

```bash
uv run python scripts/create_ticket_db.py
```

Participants should use the data as supplied. Do not hard-code the expected answers to the mandatory queries. The MCP tools must read the JSON/SQLite sources at runtime.
