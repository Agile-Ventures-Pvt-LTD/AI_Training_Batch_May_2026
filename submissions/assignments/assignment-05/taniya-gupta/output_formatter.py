from tabulate import tabulate
import pandas as pd

def format_as_table(df, limit = 20):
    """Formats a DataFrame with a strict row limit to save tokens."""
    count = len(df)
    if count > limit:
        df = df.head(limit)
        msg = tabulate(df, headers='keys', tablefmt='psql', showindex=False)
        return f"{msg}\n\n[Showing 20/{count} records.]"
    return tabulate(df, headers='keys', tablefmt='psql', showindex=False)

def print_agent_output(question, choice_label, tools_used, records_found, final_answer, data_masked):
    """Prints the formatted output."""
    print(f"QUESTION: {question}")
    print(f"CHOICE: {choice_label}")
    print(f"TOOLS USED: {', '.join(set(tools_used)) if tools_used else 'None'}")
    print(f"RECORDS FOUND: {records_found}")
    print(f"FINAL ANSWER:{final_answer}")

    print(f"SENSITIVE DATA MASKED: {data_masked}")

