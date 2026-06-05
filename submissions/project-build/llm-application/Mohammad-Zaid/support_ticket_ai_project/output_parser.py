# Joutput SON parsing
import json

def parse_json_response(json_string:str, file_name:str):
    try:
        with open(f"./outputs/{file_name}", "w") as f:
            json.dump(json_string, f, indent=4)
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}")
    
parse_json_response(ticket_summary_dict, "sample_ticket_summary.json")