import os
from datetime import datetime

# Function to save the report
def save_report_tool(report_content, report_name="final_report"):
    """
    Saves the final report content to the outputs/ folder.
    
    Args:
        report_content (str): Content of the report to save.
        report_name (str): Optional base name for the report file.
        
    Returns:
        str: Path to the saved report file.
    """
    # Ensure outputs directory exists
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{report_name}_{timestamp}.txt"
    file_path = os.path.join(output_dir, filename)

    # Save the report content to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    return file_path



