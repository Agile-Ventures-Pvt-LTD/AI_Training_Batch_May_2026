# Output_formatter.py

import os

def save_output(file_name, u_qery, answer):
    
    folder = "outputs"

    if not os.path.exists(folder):
        os.mkdir(folder)

    path = os.path.join(folder, file_name)

    with open(path, "a", encoding="utf-8") as file:
        
        file.write("\n" + "=" * 60 + "\n")
        
        file.write(f"User's Question: \n{u_qery}\n\n")
        
        file.write(f"Answer: \n{answer}\n")