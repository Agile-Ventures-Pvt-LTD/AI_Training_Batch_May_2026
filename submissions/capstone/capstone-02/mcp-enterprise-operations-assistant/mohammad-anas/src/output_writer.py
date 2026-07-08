import json
from pathlib import Path



def write_discovery_results(discovery_data:dict):
    file_path = Path("outputs/tool_discovery.json")
    if not file_path:
        raise FileNotFoundError
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(discovery_data,file,indent=2)
        
def write_mandatory_queries(result:list):
    file_path = Path("outputs/mandatory_query_results.json")
    if not file_path:
        raise FileNotFoundError
    with open(file_path,"w",encoding="utf-8") as file:
        return json.dump(result,file,indent=2)
    
def write_sample_runs(results:list):
    file_path = Path("outputs/sample_run_outputs.md")
    md_content = "# Sample Run Outputs\n"
    for item in results:
        md_content += f"## {item['query_id']} Query\n\n"
        md_content += f"**User Query:**\n{item['user_query']}\n\n"
        md_content += f"**Servers Used:**\n{', '.join(item['servers_used'])}\n\n"
        md_content += f"**Tools Used:**\n{', '.join(item['tools_used'])}\n\n"
        md_content += f"**Final Answer:**\n{item['final_answer']}\n\n"
        md_content += "---\n\n"
    
    with open(file_path,"w",encoding="utf-8") as file:
        file.write(md_content)