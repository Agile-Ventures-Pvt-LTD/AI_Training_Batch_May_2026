# Credit Card Management System (CCMS) Agent

## Overview

This project is a Credit Card Management System (CCMS) Assistant built using LangGraph, LangChain, and Groq LLM. The goal of the project is to allow business users to retrieve customer, card, transaction, merchant, and spending information using natural language instead of writing SQL queries manually.



## Features

- Customer profile lookup
- Card information retrieval
- Customer search by card number
- Transaction history retrieval
- Merchant spending analysis
- Suspicious transaction detection
- Expiring card identification
- Customer activity summaries
- High-value transaction reporting
- Database schema inspection


## Implementation Approaches

### Choice 1: LangGraph Pre-built ReAct Agent

Implemented using:

- LangGraph ---> create_react_agent
- Groq LLM ---> llama-3.1-8b-instant
- Tool-based reasoning

The pre-built agent automatically handles:

- Tool selection
- Tool execution
- Observation handling
- Final response generation

### Choice 2: Custom LangGraph ReAct Agent

Implemented using:

- StateGraph
- ToolNode
- Conditional edges
- Custom agent state

Graph flow:

START -> Agent -> Tools -> Agent -> END

The custom implementation demonstrates how LangGraph manages tool execution and agent reasoning internally.


## Project Structure

```text
ccms_langgraph_agent/
│
├── app.py
├── prebuilt_agent.py
├── custom_react_agent.py
├── tools.py
├── db_utils.py
├── prompts.py
├── config.py
├──inspect_schema.py
├──output_formatter.py
├──prompts.py
├──README.md
├──.env.example
├──tools.py
├──requirements.txt
├──graph.png
│
├── data/
│   └── ccms.db
│
├── outputs/
│   ├── sample_prebuilt_agent_run.txt
│   └── sample_custom_agent_run.txt
│
└── tests/
    └── test_tools.py
```

## Security Measures

* Card numbers are masked except for the last four digits.
* CVV information is never exposed.
* Database results are treated as the source of truth.
* Responses are generated only from retrieved data.

Example:

```text
************1697
```

## Challenges Faced

### 1. Tool Selection Issues

Initially the model sometimes selected unrelated tools. This was improved by providing clearer tool descriptions and stricter system prompt instructions.

### 2. Graph Recursion Errors

While building the custom LangGraph implementation, recursion errors occurred because the graph was not reaching an END state correctly.

This was resolved by:

* Adding proper conditional routing
* Binding tools to the model
* Returning final responses after tool execution

### 3. SQL Query Errors

Some queries contained incorrect syntax and placeholder values. These were corrected after direct testing against the database.

### 4. Sensitive Data Exposure

Card numbers originally appeared in raw form. A masking utility was added to ensure only the last four digits are visible.

---

## How to Run

Install dependencies:

```bash
uv sync
```

Run the application:

```bash
uv run app.py
```

Example queries:

```text
Show profile of customer 1
Show card details for customer 1
Display last 5 transactions for customer 1
Which merchants have highest spending?
Are there suspicious transaction patterns?
Summarize customer 1 credit card activity
```

---

## Testing

Run tests:

```bash
uv run pytest -v
```

Tests cover:

* Schema inspection
* Customer retrieval
* Card lookup
* Transaction retrieval
* Merchant summaries
* Suspicious transaction detection

---

## Future Improvements

* Multi-customer comparisons
* Advanced fraud detection rules
* Conversation memory
* Dashboard integration
* API deployment
* Role-based access control

---

## Tech Stack

* Python
* LangChain
* LangGraph
* Groq API
* SQLite
* Pytest

---

## Conclusion

This project demonstrates how an LLM-powered agent can simplify access to credit card management data through natural language interactions while maintaining data security and structured tool usage.
