from tabulate import tabulate

def format_ticket_table(tickets):

    if not tickets:
        return "No tickets found."

    return tabulate(tickets,headers="keys",tablefmt="grid")


def format_ticket_details(ticket):

    if not ticket:
        return "Ticket not found."

    rows = [
        ["Ticket ID", ticket.get("ticket_id")],
        ["Subject", ticket.get("subject")],
        ["Status", ticket.get("status")],
        ["Priority", ticket.get("priority")],
        ["Category", ticket.get("category")],
        ["Assigned Agent", ticket.get("assigned_agent")],
        ["Customer Tier", ticket.get("customer_tier")],
        ["Created At", ticket.get("created_at")],
        ["Due At", ticket.get("due_at")]
    ]

    return tabulate( rows, tablefmt="grid")


def format_comments(comments):

    if not comments:
        return "No comments found."

    return tabulate(comments,headers="keys",tablefmt="grid")


def format_summary(title, content):
    return (
        f"\n{title}\n"
        f"{'-' * len(title)}\n"
        f"{content}\n"
    )


def format_success(message):
    return f"SUCCESS: {message}"


def format_error(message):
    return f"ERROR: {message}"