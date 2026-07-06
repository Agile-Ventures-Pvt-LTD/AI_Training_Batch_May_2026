parce_incident_prompt = """
Extract the required fields from the manifest text and give the JSON response.
        
Manifest Text
{manifest_text}

Rules:
- Don't make any inforamtion on your own
- Give the response only in json forma

JSON Schema
{{
    "shipment_id" : ""
    "cargo_weight_tons" : ""
    "cargo_type" : ""
    "target_warehouse_id" : ""
    "has_perishables" : ""
    "maximum_tolerable_delay_hours" : ""   # If not define than mark it as None.
}}
"""

select_route_prompt = """
Select the ruote from the list of available routes

Available Routes
{available_routes}

JSON Schema
{{
    "route_id": "",
    "alternative_port": "",
    "warehouse_id": "",
    "added_delay_hours": 
}},
"""

incident_summary = """
Give the very short summary for this incident.

Manifest text
{manifest_text}
"""

final_operational_breif_prompt = """
The final summary for the logistic team

The brief should explain:
- What happened.
- Which route was selected or why the incident was escalated.
- The major rule or warehouse condition that affected the decision. 

Keep the brief concise

Manifest Text:
{manifest_text}

Extracted Metadata
{metadata}

Selected Route
{selected_route}

Warehouse Context
{warehouse_context}


"""