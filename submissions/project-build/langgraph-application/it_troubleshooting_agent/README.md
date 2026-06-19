# IT TROUBLESHOOTING AGENT

## Objective :

An enterprise IT support team receives frequent tickets for issues such as VPN 
failure, Outlook sync problems, password reset issues, slow laptops, network 
connectivity problems, and printer access problems.

In a real enterprise setup, support agents usually check:

1. Troubleshooting knowledge-base articles
2. User profile
3. Device health
4. Account status
5. Known incidents
6. Diagnostic results
7. Existing support ticket details

The goal of this project is to build an IT Troubleshooting Agent that uses 
LangGraph, Groq, RAG, and custom tools to perform structured diagnosis.
The assistant should not behave like a generic chatbot. It should classify the issue, 
retrieve relevant troubleshooting steps, call tools to inspect operational data, 
branch conditionally based on the issue type and missing information, and 
generate a safe resolution or escalation plan.


## Functionality :

1. Knowledge-Base Loading
2. Chunking and Indexing
3. SQLite Database Connection
4. Issue Classification
5. Troubleshooting Retrieval Tool
6. User Profile Tool
7. Device Status Tool
8. Known Incident Tool
9. Diagnostic Check Tool
10. Ticket Lookup Tool
11. Resolution Plan Generation
12. Safety Review
13. Clarification Handling
14. Ticket Summary Generation


## Tool Used :

1. classify_issue
2. retrieve_troubleshooting_steps
3. get_user_profile
4. get_device_status
5. check_known_incidents
6. run_diagnostic_check
7. get_ticket_details
8. generate_resolution_plan


## Folder Structure :

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
├── inspect_db.py
├── output_parser.py
├── requirements.txt
├── .env.example
├── README.md
├── test_graph.py
├── troubleshooting_graph.png
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



 ## Dataset Provided :

 Following is the structure of dataset provided to us.
 This include two major things :
 - knowlegde base containing all md files.
 - database containing it support data.

data/
├── knowledge_base/
│ ├── vpn_troubleshooting_guide.md
│ ├── email_outlook_troubleshooting_guide.md
│ ├── laptop_performance_guide.md
│ ├── password_reset_guide.md
│ ├── network_connectivity_guide.md
│ └── printer_troubleshooting_guide.md
│
└── database/
 └── it_support.db



# Prebuilt agents VS Custom agents :

We are given with the two choices :

Choice 1: LangGraph Pre-built ReAct Agent
Choice 2: Custom LangGraph Agent

I choose choice 1 :

Choice 1: LangGraph Pre-built ReAct Agent
This option is recommended for participants who want to focus on tools, RAG, and 
operational answer quality.
Expected architecture:
User Query
 |
 v
Pre-built ReAct Agent
 |
 +--> Issue Classification Tool
 +--> RAG Retrieval Tool
 +--> User Profile Tool
 +--> Device Status Tool
 +--> Known Incident Tool
 +--> Diagnostic Tool
 |
 v
Final Troubleshooting Response
The pre-built agent should be able to select from registered tools and produce a 
final answer based on tool outputs


This choice is much simpler as compared to custom langgraph agents.

Why we used it:

- It is very fast to set up.
- Handles tool calling automatically
- Good for testing retrieval + LLM responses quickly
- Reduces boilerplate code


## Execution : 

uv run app.py

## Graph

In the folder i also saved a graph image in png format to show the graphical representation of the project flow.

## Outputs

The output are saved in 2 formats -

1. First in md format where query with answer is saved.

2. Second in json format where the expected output as per the PRD.


## Tech Stack :

- langgraph
- langchain
- langchain-core
- langchain-community
- langchain-groq
- langchain-chroma
- chromadb
- sentence-transformers
- python-dotenv
- pydantic
- tabulate
- rich

These are added under requirements.txt file and are installed using the command :
uv add -r requirements.txt


## Conclusion :

In this project two data types are used at a time :
- database (it_support.db)
- sqllite (Vector_store)

I did all the implementation needed as per the PRD however i face few pointer errors in structuring the final output and then saving it to json file.

This project helps alot to get a hands on experience on tools and techniques including -
Langchain, Langgraph, Groq, Git, chromadb, hugging face, sentence transformer etc.

As per the guideline there is no use of AI for implementing this project.
It is done as per my understanding and knowledge.

For reference i used my previous project files etc .










