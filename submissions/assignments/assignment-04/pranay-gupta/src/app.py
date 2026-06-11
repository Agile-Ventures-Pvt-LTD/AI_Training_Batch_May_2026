# src/app.py

from importlib.metadata import version


try:
    langchain_version = version("langchain")
    major_version = int(langchain_version.split(".")[0])

except Exception:
    langchain_version = "Unknown"
    major_version = 0


if major_version >= 1:

    from src.agents.modern_agent import run_agent

    AGENT_TYPE = "Modern Agent (LangChain >= 1.0)"

else:

    from src.agents.legacy_agent import run_legacy_agent

    run_agent = run_legacy_agent

    AGENT_TYPE = "Legacy Agent (LangChain < 1.0)"

def display_banner():

    print("\n" + "=" * 70)
    print("      E-Commerce AI Database Assistant")
    print("=" * 70)

    print(f"LangChain Version : {langchain_version}")
    print(f"Loaded Agent      : {AGENT_TYPE}")

    print("\nType 'exit' or 'quit' to close the application.")
    print("=" * 70)



def main():

    display_banner()

    while True:

        try:

            user_query = input(
                "\nAsk a business question: "
            ).strip()

            if not user_query:

                print(
                    "Please enter a valid question."
                )
                continue

            if user_query.lower() in [
                "exit",
                "quit"
            ]:

                print(
                    "\nApplication closed successfully."
                )
                break

            response = run_agent(user_query)

            print("\nAnswer:")
            print("-" * 70)
            print(response)

        except KeyboardInterrupt:

            print(
                "\n\nApplication interrupted by user."
            )
            break

        except Exception as error:

            print(
                f"\nUnexpected Error: {error}"
            )


if __name__ == "__main__":
    main()
