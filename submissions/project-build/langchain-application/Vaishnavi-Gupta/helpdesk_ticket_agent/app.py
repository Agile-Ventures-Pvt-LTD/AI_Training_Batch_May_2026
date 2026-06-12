from rich.console import Console
from rich.panel import Panel

from agent import (
    run_agent,
    health_check
)

from output_formatter import (
    format_agent_output,
    print_business_response
)

console = Console()



def show_banner():

    console.print(
        Panel.fit(
            """
AI Helpdesk Ticket Operations Agent

Features:
- Ticket Search
- Ticket Details
- SLA Analysis
- Ticket Prioritization
- Conversation Memory
- Archival Memory
- Ticket Updates
- Comment Management

Type 'help' for commands.
Type 'exit' to quit.
            """,
            title="Helpdesk Agent"
        )
    )



def show_help():

    console.print(
        Panel.fit(
            """
Examples:

Show me all open high-priority tickets

Which tickets are overdue?

Summarize ticket TCK-1003

Add a comment to TCK-1001 saying
billing team is reviewing the issue

Update TCK-1001 status to In Progress

Remember that I want to prioritize
enterprise customer issues first

Based on my preference,
which tickets should I handle first?

What did we discuss earlier
about billing tickets?

Summarize this conversation
and store it in memory

Commands:

help
health
exit
quit
            """,
            title="Help"
        )
    )



def run_health_check():

    result = health_check()

    console.print(
        Panel(
            str(result),
            title="Health Check"
        )
    )



def process_query(
    user_query: str
):

    result = run_agent(
        user_query
    )

    formatted = format_agent_output(
        result
    )

    print_business_response(
        formatted
    )



def main():

    show_banner()

    while True:

        try:

            user_query = input(
                "\nHelpdesk> "
            ).strip()

            if not user_query:
                continue

            command = user_query.lower()

            if command in (
                "exit",
                "quit"
            ):
                console.print(
                    "\nGoodbye.\n"
                )
                break

            if command == "help":
                show_help()
                continue

            if command == "health":
                run_health_check()
                continue

            process_query(
                user_query
            )

        except KeyboardInterrupt:

            console.print(
                "\nInterrupted.\n"
            )
            break

        except Exception as e:

            console.print(
                Panel(
                    str(e),
                    title="Application Error"
                )
            )



if __name__ == "__main__":
    main()