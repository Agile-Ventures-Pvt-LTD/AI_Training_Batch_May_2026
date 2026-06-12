from uuid import uuid4
from datetime import datetime
from rich.console import Console

from agent import agent_build
from memory import saving_converstation


console = Console()

OUTPUT_FILE = "outputs/sample_agent_run.txt"


def save_agent_run(
    user_query: str,
    agent_response: str
):
    with open(OUTPUT_FILE,"a",encoding="utf-8") as f:

        f.write(f"Timestamp: {datetime.now()}\n")
        f.write("USER QUERY:\n")
        f.write(f"{user_query}\n\n")

        f.write("AGENT RESPONSE:\n")
        f.write(f"{agent_response}\n\n")


def main():

    agent = agent_build()

    session_id = str(uuid4())

    console.print(
        "\nAI Helpdesk Ticket Operations Agent\n",
        style="bold green"
    )

    while True:

        user_query = input("\nUser > ")

        if user_query.lower() in [
            "exit",
            "quit"
        ]:
            break

        try:

            response = agent.invoke(
                {
                    "input": user_query
                }
            )

            agent_response = response["output"]

            console.print(
                f"\n{agent_response}\n",
                style="cyan"
            )

            saving_converstation(
                session_id=session_id,
                user_message=user_query,
                agent_response=agent_response,
                tools_used=""
            )
            save_agent_run(
                user_query=user_query,
                agent_response=agent_response
            )

        except Exception as e:

            error_message = f"ERROR: {str(e)}"

            console.print(
                f"\n{error_message}\n",
                style="bold red"
            )

            save_agent_run(
                user_query=user_query,
                agent_response=error_message
            )


if __name__ == "__main__":
    main()