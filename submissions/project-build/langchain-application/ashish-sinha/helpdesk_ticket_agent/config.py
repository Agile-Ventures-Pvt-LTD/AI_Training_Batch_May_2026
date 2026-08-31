import os
from dotenv import load_dotenv

load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

GROQ_Model = os.getenv('GROQ_MODEL','llama-3.3-70b-versatile')

DB_Path = os.getenv("DB_Path","data/helpdesk_agent.db")

Reference_Time = "2026-06-12 10:00:00"

Valid_Status = [ "Open","In Progress","Pending","Resolved","Closed","Escalated"]

High_Priority_Values = ["High","Urgent"]

Enterprise_Tier = "Enterprise"

Max_Recall_Results = 10

Max_Summary_Messages = 20

Archival_Memory_Importtance_Threshold = 3