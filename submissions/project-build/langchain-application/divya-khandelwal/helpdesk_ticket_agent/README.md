# AI Helpdesk Ticket Operations Agent

## Summary

An AI-powered helpdesk assistant built using LangChain, LangGraph, Groq LLM, and SQLite.

The agent helps support teams manage tickets by searching tickets, checking SLA status, prioritizing issues, updating ticket status, adding comments, and maintaining conversation memory.

---

## Project Flow

User Query  
&nbsp;&nbsp;↓  
LangGraph AI Agent  
&nbsp;&nbsp;↓  
Understand User Intent  
&nbsp;&nbsp;↓  
Select Required Tool  
&nbsp;&nbsp;↓  
Execute Tool with SQLite Database  
&nbsp;&nbsp;↓  
Process Tool Result  
&nbsp;&nbsp;↓  
Reflection Check  
&nbsp;&nbsp;↓  
Generate Final Response  
&nbsp;&nbsp;↓  
Save Conversation Output in JSON

---

## Technologies Used

- Python
- LangChain
- LangGraph
- Groq LLM
- SQLite
- Pydantic
- dotenv

---

## Features

- Ticket search and details retrieval
- SLA status checking
- Ticket prioritization
- Ticket status updates
- Internal comments
- Conversation memory
- JSON output logging