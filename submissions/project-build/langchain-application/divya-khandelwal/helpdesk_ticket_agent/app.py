from agent import run_agent

from memory import save_conversation

from config import validate_config

import uuid
import json
import os
from datetime import datetime

OUTPUT_FILE = "outputs/conversation_history.json"

def save_output_json(result, user_query):

    os.makedirs(
        "outputs",
        exist_ok=True
    )


    if not os.path.exists(OUTPUT_FILE):

        with open(
            OUTPUT_FILE,
            "w"
        ) as f:

            json.dump(
                [],
                f
            )



    with open(
        OUTPUT_FILE,
        "r"
    ) as f:

        conversations = json.load(f)


    conversations.append(

        {
            "timestamp":
            datetime.now().isoformat(),

            "user_query":
            user_query,

            "plan":
            result["plan_summary"],

            "tools_used":
            result["tools_used"],

            "reflection":
            result["reflection_summary"],

            "final_answer":
            result["final_answer"]
        }

    )

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            conversations,
            f,
            indent=4
        )


def main():

    try:

        validate_config()

    except Exception as e:

        print(
            f"Configuration Error: {e}"
        )

        return



    session_id = str(
        uuid.uuid4()
    )


    print(
        "\nAI Helpdesk Ticket Operations Agent"
    )

    print(
        "Type 'exit' to stop\n"
    )



    while True:


        user_query = input(
            "User: "
        )


        if user_query.lower()=="exit":

            print(
                "Thank you!"
            )

            break



        try:


            result = run_agent(
                user_query
            )


            print("\nPLAN ")

            print(
                result["plan_summary"]
            )


            print("\nREFLECTION")

            print(
                result["reflection_summary"]
            )


            print("\nFINAL ANSWER")

            print(
                result["final_answer"]
            )

            save_output_json(
            result,
            user_query
            )

            

            save_conversation(

                session_id,

                user_query,

                result["final_answer"],

                result.get(
                    "tools_used"
                )

            )


        except Exception as e:


            print(
                "Agent Error:",
                str(e)
            )





if __name__=="__main__":

    main()