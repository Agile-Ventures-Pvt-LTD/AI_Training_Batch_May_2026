import json
from graph import graph


def pre_compute():
    INCIDENT_PATH = "./data/sample_incidents.json"

    try: 
        with open(INCIDENT_PATH, "r") as f:
            data = json.load(f)

    except Exception as e:
        print(f"Error loading the smaple incidents file : {e}")

    ids = []
    for i in range(0, len(data)):
        ids.append(data[i]["incident_id"])

    return ids


while True:
    print("Available Incidents:")
    ids = pre_compute()

    for idx, i in enumerate(ids):
        print(str(idx + 1) + ".", i)
    
    select_incedent = input("Select Incident: ")
    if select_incedent is ["q", "quit"]:
        break
    

    incident_id = ids[int(select_incedent) - 1]

    response = graph.invoke({"incident_id" : incident_id})

    print(response)
        