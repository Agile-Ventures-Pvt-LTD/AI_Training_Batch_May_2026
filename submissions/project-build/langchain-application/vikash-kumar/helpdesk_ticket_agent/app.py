import uuid

from agent import run_agent

from output_formatter import (format_agent_response,save_evaluation_output,save_sample_run)


def print_banner():
    print("AI Helpdesk Ticket Operations Agent")

def main():

    session_id = str(uuid.uuid4())

    show_plan = False
    show_reflection = False

    print_banner()

    while True:

        user_query = input("\nUser > ").strip()

        if not user_query:
            continue

        if user_query.lower() == "/exit":
            print("Exit")
            break

        if user_query.lower() == "/help":

            print("\nExample Queries:")
            print("- Show me all critical open tickets")
       
            print("- Prioritize my work queue")
            print("- Show comments for ticket TCK-08469")

            continue

        if user_query.lower() == "/show_plan":

            show_plan = not show_plan

            print(
                f"Planning Display: {'ON' if show_plan else 'OFF'}"
            )

            continue

        if user_query.lower() == "/show_reflection":

            show_reflection = not show_reflection

            print(
                f"Reflection Display: {'ON' if show_reflection else 'OFF'}"
            )

            continue

        try:

            response = run_agent(
                session_id=session_id,
                user_query=user_query
            )

            print("\nAssistant >")
            print(response["answer"])

            if show_plan:

                print("\nPLAN")
                print(response["plan"])

            if show_reflection:
                print("\nREFLECTION")
                print(response["reflection"])

            save_evaluation_output(
                session_id=session_id,
                query=user_query,
                response=response
            )

            formatted_output = format_agent_response(
                response["answer"],
                response["plan"],
                response["reflection"])

            save_sample_run(formatted_output)

        except Exception as error:
            print("\nError:")
            print(error)


if __name__ == "__main__":
    main()