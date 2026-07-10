# SUPPLY CHAIN LOGISTICS REROUTER

## What this is

- A LangGraph-based reroute advisory agent for supply-chain disruptions. Given a plain-English incident report (port closure, strike, weather event), it extracts the shipment details, checks a RAG-backed logistics policy knowledge base, evaluates candidate reroutes against live warehouse inventory data, and produces a JSON advisory report plus an LLM-written operations brief.

## Stack Of Choice

LangGraph (state machine / orchestration) · langchain-groq (LLM) · Groq
`llama-3.3-70b-versatile` · FAISS + langchain-huggingface
(`sentence-transformers/all-MiniLM-L6-v2`) for RAG retrieval · Pydantic
(structured extraction schema) · Python `json` for data access · pytest

## File Structure

supply-chain-logistics-rerouter/
├── data/
│   ├── logistics_knowledge_base.txt
│   ├── inventory_status.json
│   ├── route_options.json
│   └── sample_incidents.json
├── outputs/
├── src/
│   ├── main.py
│   ├── state.py
│   ├── schemas.py
│   ├── tools.py
│   ├── rag.py
│   ├── nodes.py
│   ├── graph.py
│   └── report_writer.py
├── tests/
├── .env.example
├── requirements.txt
└── pyproject.toml


## Setup and running it

- Install dependencies: `pip install -r requirements.txt` (into a venv)
- Copy `.env.example` to `.env` and set `GROQ_API_KEY`
- `python -m src.main` — lists the sample incidents, lets you pick one (or
  `all`), runs the full LangGraph pipeline, and writes a JSON advisory
  report per incident to `outputs/`.
- `pytest tests/` — runs the test suite.


## Limitations of How I Built This

- `data/logistics_knowledge_base.txt`, `inventory_status.json`,
  `route_options.json`, and `sample_incidents.json` are placeholder sample
  data I wrote to match the schemas the code expects, not the exact
  dataset from the capstone brief — real data should replace these.
- No retry logic — a failed or malformed Groq structured-output call in
  `parse_incident` isn't retried, it just propagates as an error.
- `generate_operations_brief` always writes a route-selection-style
  narrative, even when the incident was escalated with no route selected,
  so escalated reports can read a bit oddly.
- Route and warehouse IDs are matched by convention between
  `route_options.json` and `inventory_status.json` with no validation — a
  typo'd `warehouse_id` fails at runtime instead of at data-load time.
- No persistence or memory across incidents — each run is stateless, and
  `outputs/*.json` reports aren't deduplicated or versioned.
- Tests only cover node/tool logic directly — no test yet exercises the
  compiled LangGraph end-to-end.

## Where I used AI in This Project 

- I used AI for someof the help with creating some of the tests.
- I used AI to simplify `nodes.py` afterward — merging duplicate condition
  checks between the impact-scoring and routing-decision logic, and
  removing an unused `logs` field that was written to but never read
  anywhere.
- I used AI to draft this README 

## Where Some Of The Code Was Inspired From

- No external repo templates were used for this project — it was built
  directly from a detailed spec (file names, function signatures, and
  exact contents) that I wrote out myself, rather than adapted from a
  reference implementation.
- The LangGraph state-machine shape (parse → RAG lookup → load routes →
  select/check/analyze loop → finalize/escalate → report) follows the
  standard conditional-edge patterns documented in LangGraph's own docs,
  not a specific third-party example.
