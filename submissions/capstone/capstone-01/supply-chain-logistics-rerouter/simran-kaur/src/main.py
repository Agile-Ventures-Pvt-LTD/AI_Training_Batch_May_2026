
from src.graph import compiled_workflow

while True:
    try:
        incident_id = input("\nincident_id: ")
        manifest_txt = input("\nmanifest_txt: ")
        disrupted_port_id = input("\ndisrupted_port_id: ")

        if incident_id.lower() == "exit" or manifest_txt.lower()== "exit" or disrupted_port_id.lower == "exit":
            break


        response=compiled_workflow.invoke({"incident_id": incident_id,
                                  "manifest_txt": manifest_txt,
                                  "disrupted_port_id": disrupted_port_id})
        
    except Exception as e:
        print("ERROR:", e)