from rich.console import Console
from rich.panel import Panel

from agent import run_agent

console = Console()


def show_banner():

    console.print(
        Panel.fit(
            """
AI Helpdesk Ticket Operations Agent

Features:
- Ticket Search
- SLA Analysis
- Ticket Prioritization
- Ticket Updates
- Internal Comments
- Conversation Recall
- Archival Memory
- Conversation Summaries

Type 'exit' to quit
            """,
            title="Helpdesk Agent"
        )
    )


def main():

    show_banner()

    session_id = None

    while True:

        try:

            user_input = input(
                "\nHelpdesk User > "
            ).strip()

            if not user_input:
                continue

            if user_input.lower() in [
                "exit",
                "quit"
            ]:
                print("\nGoodbye.")
                break

            response = run_agent(
                user_input=user_input,
                session_id=session_id
            )

            session_id = response.get(
                "session_id"
            )

            print("\nAgent Response:\n")
            print(
                response.get(
                    "final_answer",
                    "No response."
                )
            )

        except KeyboardInterrupt:

            print("\nExiting...")
            break

        except Exception as e:

            print(
                f"\nError: {e}"
            )


if __name__ == "__main__":
    main()