import json
import os
# Replace 'src.tools' with your actual file path if different
from src.tools import read_resume_tool, candidate_index_lookup_tool, read_job_description

def test_json_layout():
    # 1. Create a dummy file with real content
    mock_path = "candidate_001_rohan_mehta.md"
    with open(mock_path, "w", encoding="utf-8") as f:
        f.write("# Rohan Mehta\nRole: AI Engineer\nSkills: Python, CrewAI")
    
    # 2. Run your tool
    try:
        result = read_resume_tool(resume_path=mock_path)
    except AttributeError:
        result = read_resume_tool._run(resume_path=mock_path)
        
    # 3. Print it as a pretty JSON string
    print("\n=== CORRECTED TOOL OUTPUT LAYOUT ===")
    print(json.dumps(result, indent=4))
    print("====================================\n")
    
    # 4. Cleanup
    if os.path.exists(mock_path):
        os.remove(mock_path)

if __name__ == "__main__":
    test_json_layout()
