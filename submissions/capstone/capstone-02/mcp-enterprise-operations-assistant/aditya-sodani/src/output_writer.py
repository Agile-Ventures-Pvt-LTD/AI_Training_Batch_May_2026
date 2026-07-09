import json
import os

OUTPUT_FILE = "outputs/mandatory_query_results.json"

def save_query_result(
       user_query,
       servers_used,
       tools_used,
       evidence,
       operations_summary
):

   os.makedirs(
       "outputs",
       exist_ok=True
   )

   if os.path.exists(OUTPUT_FILE):
       with open(OUTPUT_FILE, "r") as f:
           try:
               results = json.load(f)
           except:
               results = []
   else:
       results = []

   output = {

       "user_query": user_query,

       "servers_used": list(set(servers_used)),

       "tools_used": list(set(tools_used)),

       "evidence": evidence,

       "operations_summary": operations_summary,

       "recommended_next_actions": [
           "Review available operational evidence.",
           "Investigate impacted service components.",
           "Coordinate with responsible support teams."
       ],

       "limitations": [
           "The dataset does not contain application logs.",
           "The dataset does not contain distributed traces."
       ]
   }

   results.append(output)

   with open(
       OUTPUT_FILE,
       "w"
   ) as f:

       json.dump(
           results,
           f,
           indent=4
       )