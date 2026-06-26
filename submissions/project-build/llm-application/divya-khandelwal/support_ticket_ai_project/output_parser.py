import os
import json
def store_response_in_json(response, output_file_path):
    response_data = {
        "support_ticket_analysis": response
    }
    
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    with open(output_file_path, 'w') as json_file:
        json.dump(response_data, json_file, indent=4)
