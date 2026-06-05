import json
import os
from datetime import datetime




import json
import os
from datetime import datetime

def save_json(data, folder="outputs"):
    """
    Saves final ticket output as JSON file
    """

    # create folder if not exists
    os.makedirs(folder, exist_ok=True)

    # unique filename using timestamp
    filename = f"{folder}/ticket_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return filename