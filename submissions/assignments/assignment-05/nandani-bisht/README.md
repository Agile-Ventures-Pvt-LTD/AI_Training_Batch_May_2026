# CCMS Agent

A LangGraph agent for the Credit Card Management System database. Ask questions in plain English — the agent picks the right tool, queries SQLite, and returns a clean answer with sensitive fields masked.

Both assignment implementations are included:

- **main.py** (no args) — pre-built ReAct agent using `create_react_agent` (Choice 1)
- **main.py custom** — custom `StateGraph` with agent, tools, and reflection nodes (Choice 2)

---

# Participant Name
Nandani Bisht

## Setup

Python 3.10 or higher is required.

```bash
pip install -r requirements.txt
```

Copy the env template and add your Groq key:

```bash
cp .env.example .env
```

Get a free key at https://console.groq.com

---

## Database

Drop `ccms.db` into the `data/` folder:

```
Assignment05/
  data/
    ccms.db
```

The path defaults to `data/ccms.db` and can be overridden with `DB_PATH` in `.env`.

---

## Running

Pre-built ReAct agent:

```bash
python app.py
```

Custom StateGraph agent:
```bash
python app.py custom
```

Both run an interactive loop. Type `exit` or `quit` to stop.

---

## Agent Architecture

**Choice 1 — pre-built:** `create_react_agent` from `langgraph.prebuilt` wraps the LLM and 13 tools in a standard ReAct loop. The LLM decides which tool to call, gets the result, and repeats until it has a final answer.

**Choice 2 — custom graph:**

```
START
  |
  v
agent_node  <-----------+
  |                     |
  +-- tool calls? ---> tools_node
  |
  +-- final answer?
        |
        v
  reflection_node
        |
        v
       END
```

`AgentState` is a TypedDict that carries four fields through the graph:

| Field | Type | Purpose |
|-------|------|---------|
| `messages` | list | Full conversation history |
| `plan` | str | High-level plan the agent builds |
| `reflection` | str | Post-answer self-review |
| `tools_used` | list | Names of every tool called |

`route_after_agent` inspects the last message: if it contains tool calls, route to `tools_node`; otherwise route to `reflection_node` and finish.

---

## Tools

13 tools total (8 minimum required by the assignment):

| Tool | What it does |
|------|-------------|
| `inspect_database_schema` | Lists all tables and columns. Good first call. |
| `get_customer_profile` | Lookup by ID, name, email, or phone. Email and phone are masked. |
| `get_card_details` | Card info for a customer. Card number shown as last 4 digits. |
| `search_transactions` | Up to 10 filters: customer, card, merchant, category, amount range, date range, type, limit. |
| `get_customer_transactions` | Recent transactions for one customer, newest first. |
| `get_statement_summary` | Total debit spend, 5% minimum due, due date, risk level. |
| `get_rewards_summary` | 1 point per 100 units on debit transactions. |
| `get_merchant_spend_summary` | Total spend grouped by merchant name or merchant category. |
| `get_notification_summary` | Tells the agent that the notification table is not in this DB version. |
| `detect_suspicious_transactions` | Three SQL rules: high-value amount, same-card velocity, terminal location spread. |
| `get_cards_expiring_soon` | Cards expiring within N days. Card numbers masked. |
| `get_top_customers_by_due` | Customers ranked by total debit spend, highest first. |
| `get_transaction_type_summary` | Debit/Credit split by Local/International with counts and totals. |

---

## Sample Questions

```
Show me the database schema.
What is the profile of customer 1?
Show me the card details for customer 2.
What are the last 10 transactions for customer 3?
Which customers have the highest amount due?
Show statement summary for customer 1.
Which merchant category has the highest total spend?
How many reward points does customer 5 have?
Are there any suspicious transactions?
Which cards expire in the next 60 days?
```

---

## Data Masking

| Field | Rule | Example output |
|-------|------|----------------|
| Card number | Last 4 digits only | `**** **** **** 1697` |
| Email | First char + domain | `d****@gmail.com` |
| Phone | First 2 + last 2 digits | `90****17` |

Full card numbers, CVV codes, passwords, and security answers are never returned by any query.

---

## Tests

Run directly:
```bash
python tests/test_tools.py
```

Or with pytest:
```bash
pytest tests/test_tools.py -v
```

26 test cases across all 13 tools, run against the live database.

---

## Known Limitations

- The `notification`, `rewards`, and `statement` tables are absent from this version of `ccms.db`. Rewards and dues are computed from the `transaction` table instead.
- Customer IDs in the database are plain integers. Both `1` and `CUST-1` work as input.
- Fraud thresholds (75,000 and 50,000) exceed the maximum transaction in this dataset (320.15), so the high-value rules return no matches. The terminal location rule may still flag records depending on coordinate spread.

---

## Future Work

- Real `rewards` table with per-category point multipliers.
- Real `statement` table with billing cycle tracking.
- Card activation and block tools.
- REST API wrapper around the agent.
- ML-based anomaly scoring to replace the fixed-threshold fraud rules.
