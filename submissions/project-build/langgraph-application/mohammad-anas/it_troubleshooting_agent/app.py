from utils import save_output
from rich.console import Console

from prebuilt_agent import run_agent

console = Console()


def main():

    console.print(
        "IT Troubleshooting Agent"
    )

    while True:

        query = input(
            "\nEnter Issue (or type exit): "
        )

        if query.lower() == "exit":
            break

        try:
            result = run_agent(query)
            
            save_path = save_output(
                query=query,
                response=str(result)
            )
            console.print(result)
            console.print(
            f"\nSaved to: {save_path}"
            )
        except Exception as error:

            console.print(
                f"\nError: {error}"
            )


if __name__ == "__main__":
    main()