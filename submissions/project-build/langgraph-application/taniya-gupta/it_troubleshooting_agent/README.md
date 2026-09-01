# Project 003 - IT Troubleshooting agent

## Name
Taniya gupta

## About project
This project showcases a prebuilt langgraph agent that is implemented by using knowledge base and data base as the data for the agent. The project is implementation of Langgraph and RAG topics.

## Getting Started

### 1. Installation
install the dependencies from requirements.txt:
```bash
pip install -r requirements.txt
```

### 2. Configuration
Copy the `.env.example` file to `.env` and add your Groq API Key

### 3. Run the app
```bash
python app.py
```

---

## File Structure
```
it_troubleshooting_agent/
│
├── app.py
├── config.py
├── loaders.py
├── retrievers.py
├── db_utils.py
├── tools.py
├── graph.py
├── prebuilt_agent.py
├── prompts.py
├── output_parser.py
├── requirements.txt
├── .env.example
├── README.md
│
├── data/
│ ├── knowledge_base/
│ └── database/
│
├── vector_store/
│
└── outputs/
 ├── sample_run_outputs.md
 └── evaluation_results.json
```
### Implementation Choice: Pre built Langgraph agent

Why I chose prebuilt langgraph agent over custom agent - Custom agent was very long to implement with the given number of tools and well as slow with the number of nodes that were present in the langgraph workflow, so the faster and better suited application for this project was Pre built langgraph agent.

Sequential, parallelization and conditional patterns have been implemented in the project.

## Known Limitations and Future Improvements
**Streamlit integration**: Integrating streamlit UI interface for seamless interaction instead of CLI
**LLM fallback**: LLM fallback to be implemented for large number of queries

## Challenges Faced
- SQL query: The sql query confusion, LIKE was used for getting full name of user instead of getting it directly, since fullname consists of firstname and lastname
- Langchain version - Changing state_modifier variable to message_modifier to support the used langchain version
- Confusion of llm - since the known_incidents table has 'region' column while the user has 'location' column which confused the llm, so i mapped them accordingly in the prompt for clarity
- LLM fallback - Implemented llm fallback while testing the queries