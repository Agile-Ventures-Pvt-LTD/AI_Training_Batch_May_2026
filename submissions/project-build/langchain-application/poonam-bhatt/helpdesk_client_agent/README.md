#  AI Helpdesk Ticket Agent

An AI-powered helpdesk ticket management system built using **LangChain + Groq LLM + Python + SQLite**, capable of searching tickets, retrieving details, managing comments, and calculating SLA status using tool-based reasoning.

---

##  Features

-  Search tickets by status and priority  
-  Get full ticket details  
-  Fetch and add ticket comments  
-  SLA status calculation  
-  Ticket prioritization queue  
-  AI agent powered by LangChain + Groq LLM  
-  Full evaluation logging system (JSON-based)  
-  Tool usage tracking  
-  Structured output saved for every query  

---

##  Project Structure


helpdesk_ticket_agent/
│
├── app.py
├── agent.py
├── tools.py
├── db_utils.py
├── memory.py
├── prompts.py
├── requirements.txt
├── .env.example
├── README.md
├──config.py
├──output_parser.py
├──planner.py
│
├── data/
│ └── helpdesk_agent.db

├── evaluation/
│ └── evaluation_logger.py
│
└── outputs/
 └── sample_agent_run.txt


---


##  Tickets:--


search_tickets
get_ticket_details
get_ticket_comments
calculate_sla_status
prioritize_tickets
update_ticket_status
add_ticket_comment


## Memory:-

Save Conversation
Recall Conversation
Save Archival Memory
Recall Archival Memory

# Problem Faced:-

Since the db is too big hence resuts in rate limit hit with respect to Groq API Key .

this will result in my last minute testing phase, hence not able to complete the testing clearly .
Still json is saved and all is working when there is no limit hit .



