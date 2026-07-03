# Project 2: Travel Booking Agent

This project implements a natural language database querying assistant built with **Pydantic AI**, **Groq**, **weather** and **SQLite**. It enforces SQL injection/modification input guardrails and database schema leakage output audits, with automated evaluations running via **DeepEval** metrics.

---

## 🏗️ Project Flow Architecture

```
[User Query] ──> [Input Guardrails] (Filters drop/delete writes & structural queries)
                      │
                      ├─(Passes)
                      ▼
             [Pydantic AI Agent] (Dynamic Tool calling using injected connection context)
                      │
                      ├──> list_all_users
                      ├──> get_user_by_travels
                      └──> lookup_customer_orders
                      ├──> get_weather
                      
                               │
                               ▼
                         [SQLite Database/weather tool] (Returns raw rows)
                               │
                               ▼
                     [Output Guardrails] (Audits generated response for raw SQL leaks)
                               │
                               ▼
                            Final Answer
                               │
                     [DeepEval Pytest Suite] (Evaluates Answer Relevancy)
```

---



## 🏗️ Project Folder Structure 

```
travel-booking-agent
├───db                                         # Containing the provided database
    └───travel_data.db
├───src                                        # Core application source code
│   ├───tools                                  # Tool implementation (weather and database)
│   │   └───weather.py
        └───database.py
    ├───guardrails_config.py
    ├───agent.py                               # pydantic ai agent definition
│   
└───tests                                      # pytest and DeepEval suites
    └───conftest.py
    ├───test_Agent_metrics.py
├───requirements.txt                           # Hardened dependency definition
├───.env.example
├───README.md                                  # Setup Architecture and run-step

```


## 🛠️ Key Implementation Files

1. **`database.py`**: SQLite catalog client setup. Populates records, and handles SELECT queries safely.
2. **`weather.py`**: weather catalog setup.Created function get_weather_forecast and use it under tools in agent.py.
3. **`guardrails_config.py`**: Classifier models (`DatabaseInputGuardrailResult` and `DatabaseOutputGuardrailResult`) checking inputs for injection and outputs for raw schemas/queries leakage.
4. **`agent.py`**: Connects SQLite connection dependency  and weather using `RunContext`, maps tools, and implements output self-correction.
5. **`tests/test_db_evaluation.py`**: Automated evaluation suite. Builds a custom model `GroqDeepEvalModel` to run DeepEval metrics (`AnswerRelevancyMetric`) on Groq with custom thresholds.
6. **`tests/conftest.py`**:Tested the configuration of API and models. Ensure environment variables are populated for testing to avoid connection issues.

---

## 🚀 Running the Project (run-step)

### Prerequisites
- Python 3.10+
- Groq API Key

### Setup
1. Navigate to the project directory:
   ```bash
   cd "participant-poonam-bhatt/submissions/project-build/pydantic-ai-application/poonam-bhatt/travel-booking-agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your API key in the `.env` file:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

### Execution
Run the database agent pipeline:
```bash
python -m agent            # Run file from root
```

### Running DeepEval Evaluation Tests
Run the evaluation test suite to verify RAG metrics against a `0.8` threshold using `pytest`:
```bash
pytest tests/
```
Or run with DeepEval CLI (will print evaluation tables and logs):
```bash
deepeval test run tests/test_db_evaluation.py
```
