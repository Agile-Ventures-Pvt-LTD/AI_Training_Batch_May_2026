import os
import json
from datetime import datetime

from langchain_core.messages import HumanMessage

from custom_react_agent import compiled_graph



# -----------------------------
# Output Configuration
# -----------------------------

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "outputs"
)


os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)



# -----------------------------
# Save Final Agent Response
# -----------------------------

def save_agent_json_output(
    user_question,
    answer,
    tools_used=None,
    records_found=0,
    limitations=None
):


    output = {

        "user_question": user_question,

        "implementation_choice":
        "custom_react_agent",

        "tools_used":
        tools_used or [],

        "records_found":
        records_found,

        "answer":
        answer,

        "sensitive_data_masked":
        True,

        "limitations":
        limitations or []

    }



    file_name = (
        "final_response_"
        +
        datetime.now().strftime("%Y%m%d_%H%M%S")
        +
        ".json"
    )



    file_path = os.path.join(
        OUTPUT_DIR,
        file_name
    )



    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:


        json.dump(
            output,
            file,
            indent=4,
            ensure_ascii=False
        )



    print(
        "\nJSON SAVED:"
    )

    print(
        file_path
    )





# -----------------------------
# Run Agent
# -----------------------------

def run_agent():


    print(
        "\n=============================="
    )

    print(
        " Credit Card Management Agent "
    )

    print(
        " Type exit to stop "
    )

    print(
        "==============================\n"
    )



    while True:


        user_input = input(
            "User: "
        )



        if user_input.lower() == "exit":


            print(
                "Agent stopped"
            )

            break




        result = compiled_graph.invoke(

            {

                "messages":

                [

                    HumanMessage(
                        content=user_input
                    )

                ],

                "plan":
                "",

                "reflection":
                "",

                "tools_used":
                []

            }

        )



        # -----------------------------
        # Final Response
        # -----------------------------

        final_message = result["messages"][-1]


        answer = final_message.content



        if not answer:

            answer = (
                "No response generated"
            )



        print(
            "\nAssistant:",
            answer
        )



        # -----------------------------
        # Get Tools Used
        # From State
        # -----------------------------

        tools_used = []


        for message in result["messages"]:

            if hasattr(message, "tool_calls"):

                for tool in message.tool_calls:

                    tools_used.append(
                        tool["name"]
                    )


        # -----------------------------
        # Save JSON
        # -----------------------------

        save_agent_json_output(

            user_question=user_input,

            answer=answer,

            tools_used=tools_used

        )



        print(
            "\n----------------------\n"
        )





if __name__ == "__main__":

    run_agent()