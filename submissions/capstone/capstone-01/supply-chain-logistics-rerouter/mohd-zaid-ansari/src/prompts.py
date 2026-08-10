system_prompt="""You are a operational expert you are required to generate a final report on basis of the incidents metadata, extracted metadata, retrived contex, selected route and give the final report in the structured format.
"""

human_message="""
"Incident_extracted_metadata:{extracted_metadata}",
"Retrive routing rule:{routing_rag_context}",
"Select route:{selected_route}",
"warehouse context:{warehouse_db_context}",
"reroute impact score:{reroute_impact_score}",
"routing decision:{routing_decision}"
"""
