from tabulate import tabulate


def format_output(records):

    if not records:
        return "No records found."

    return tabulate(
        records,
        headers="keys",
        tablefmt="grid"
    )