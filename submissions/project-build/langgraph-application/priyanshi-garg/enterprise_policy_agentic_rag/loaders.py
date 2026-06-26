import os

folder_path = r"C:\Users\Priyanshi Garg\Desktop\enterprise_policy_agentic_rag\data\policies"   # <-- your folder

markdown_files = []
for filename in os.listdir(folder_path):
    if filename.endswith(".md"):
        with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
            markdown_files.append((filename, f.read()))

print("Loaded files:", len(markdown_files))

