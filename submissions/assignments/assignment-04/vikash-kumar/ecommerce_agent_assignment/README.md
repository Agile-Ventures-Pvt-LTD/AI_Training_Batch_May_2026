# Natural Language E-commerce Database Agent

The motive of this project is to build an AI agent that can answer business questions from an e
commerce SQLite database using natural language. The user should be able to ask plain-English 
questions, and the agent should use a database tool to retrieve accurate answers from the SQLite 
database

# Business Scenario

The business team frequently asks data-related questions, but they do not know SQL. They usually depend on developers or data analysts to extract information from the database.

The company wants to build a prototype of an AI-powered database assistant that allows business 
users to ask questions in plain English and receive accurate answers from the e-commerce database.
The prototype should use Python, LangChain, SQLite, an LLM with tool-calling capability, a custom 
database tool, and a simple natural language interface.

#  Expected User Experience
User: Which are the top 3 customers by total purchase amount?

Agent: The top 3 customers by total purchase amount are:
1. Rohan Mehta - Rs. 42,500
2. Priya Sharma - Rs. 38,900
3. Neha Gupta - Rs. 35,700

These customers have generated the highest total revenue based on completed orders.

# Security and Safety Requirement
- Allow Only SELECT Queries
-  Prevent Multiple Statements
- Limit Output Size
-  Handle Errors Gracefully

#  Version-Specific LangChain Requirements
 
I have used LangChain Version Less Than 1.0 which demonstrate demonstrates legacy LangChain agent development patterns. Participants may use older APIs such as initialize_agent, AgentExecutor, Tool, StructuredTool, or AgentType based on the compatible version selected.

#  Prompting Requirements

You are an AI assistant for an e-commerce business.
You can answer business questions using the ecommerce SQLite database.
The database has the following tables:- customers- products- orders- order_items
Use the database tool only when the user asks a question that requires data.

Important rules:
- Only generate SELECT queries.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE queries.
- Always explain results in simple business language.
- If the data is unavailable, clearly say that the answer cannot be determined from the database.
- Do not make up numbers.- If a query returns no records, explain that no matching data was found

# Future Improvements

We can use different robust tools which can help bot to retrieve the chunks for precisely.