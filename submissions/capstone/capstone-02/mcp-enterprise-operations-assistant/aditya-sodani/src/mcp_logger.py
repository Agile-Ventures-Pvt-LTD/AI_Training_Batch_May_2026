import json
import os

LOG_FILE = "outputs/current_tool_execution.json"

def reset_log():

    os.makedirs("outputs",exist_ok=True)

    with open(LOG_FILE, "w") as f:
        json.dump(
            {
                "servers_used": [],
                "tools_used": [],
                "evidence": {
                    "services": [],
                    "incidents": [],
                    "tickets": [],
                    "changes": []
                }
            },
            f,
            indent=4
        )

def log_tool(
        server_name,
        tool_name,
        result
):

    if not os.path.exists(LOG_FILE):
        reset_log()

    try:
       with open(LOG_FILE) as f:
          data=json.load(f)
    except json.JSONDecodeError:
       reset_log()
       with open(LOG_FILE) as f:
          data=json.load(f)


    data["servers_used"].append(server_name)
    data["tools_used"].append(tool_name)

    if "service" in result:
        data["evidence"]["services"].append(
            result["service"]
        )

    if "services" in result:
        data["evidence"]["services"].extend(
            result["services"]
        )

    if "incidents" in result:
        data["evidence"]["incidents"].extend(
            result["incidents"]
        )

    if "ticket" in result:
        data["evidence"]["tickets"].append(
            result["ticket"]
        )

    if "tickets" in result:
        data["evidence"]["tickets"].extend(
            result["tickets"]
        )

    if "change" in result:
        data["evidence"]["changes"].append(
            result["change"]
        )

    if "changes" in result:
        data["evidence"]["changes"].extend(
            result["changes"]
        )

    # remove duplicates
    data["servers_used"] = list(
        set(data["servers_used"])
    )

    data["tools_used"] = list(
        set(data["tools_used"])
    )

    with open(LOG_FILE,"w") as f:

        json.dump(data,f,indent=4)


def get_log():
   if not os.path.exists(LOG_FILE):
       reset_log()

   try:
       with open(LOG_FILE, "r") as f:
           return json.load(f)

   except json.JSONDecodeError:

       reset_log()

       with open(LOG_FILE, "r") as f:
           return json.load(f)
 