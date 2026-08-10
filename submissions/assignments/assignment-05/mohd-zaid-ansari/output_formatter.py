import os

def save_output(file_name, question, answer):
    folder = "outputs"

    if not os.path.exists(folder):
        os.mkdir(folder)

    path = os.path.join(folder, file_name)

    with open(path, "a", encoding="utf-8") as file:
        file.write("\n" + "-" * 50 + "\n")
        file.write(f"Question: {question}\n\n")
        file.write(f"Answer:\n{answer}\n")