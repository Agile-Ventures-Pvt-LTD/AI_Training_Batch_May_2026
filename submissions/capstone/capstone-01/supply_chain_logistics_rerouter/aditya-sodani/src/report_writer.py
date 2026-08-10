import json
import os

def save_report(incident_id,report):

   os.makedirs("outputs",exist_ok=True)

   path = (
       f"outputs/"
       f"{incident_id}_reroute_advisory_report.json"
   )

   with open(path,"w") as f:

       json.dump(report,f,indent=4)

   return path