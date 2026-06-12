import json
import re
from config import OUTPUT_DIR

def clean_text(text):

    if text is None:
        return ""

    text = str(text)

    text = text.replace("\\n", " ")
    text = text.replace("\\t", " ")

    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("\r", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()

def format_ticket(ticket):

    if not ticket:
        return "Ticket not found."

    lines = [
        "=" * 60,
        "TICKET DETAILS",
        "=" * 60,
        f"Ticket ID      : {ticket.get('ticket_id', 'N/A')}",
        f"Customer       : {ticket.get('customer_name', 'N/A')}",
        f"Company        : {ticket.get('company_name', 'N/A')}",
        f"Customer Tier  : {ticket.get('customer_tier', 'N/A')}",
        f"Priority       : {ticket.get('priority', 'N/A')}",
        f"Status         : {ticket.get('status', 'N/A')}",
        f"Assigned To    : {ticket.get('assigned_to', 'N/A')}",
        f"Category       : {ticket.get('category', 'N/A')}",
        f"Subject        : {ticket.get('subject', 'N/A')}",
        "",
        "Description:",
        clean_text(ticket.get("description", "")),
    ]

    return "\n".join(lines)


def format_ticket_list(tickets):

    if not tickets:
        return "No tickets found."

    lines = ["TICKET RESULTS"]

    for ticket in tickets:

        lines.append(
            f"[{ticket.get('ticket_id', 'N/A')}] "
            f"{ticket.get('priority', 'N/A')} | "
            f"{ticket.get('status', 'N/A')} | "
            f"{ticket.get('customer_name', 'N/A')} | "
            f"{ticket.get('subject', 'N/A')}"
        )

    return "\n".join(lines)


def format_comments(comments):

    if not comments:
        return "No comments found."

    lines = ["TICKET COMMENTS",]

    for comment in comments:

        lines.extend([
            "",
            f"[{comment.get('created_at', 'N/A')}] "
            f"{comment.get('author', 'Unknown')}",
            f"Type: {comment.get('comment_type', 'N/A')}",
            f"Comment: {clean_text(comment.get('comment', ''))}"
        ])

    return "\n".join(lines)


def format_sla_result(sla_result):

    if not sla_result:
        return "No SLA information available."

    lines = [
        "SLA STATUS",
      ]

    for key, value in sla_result.items():
        lines.append(f"{key}: {value}")

    return "\n".join(lines)


def format_agent_response(answer, plan, reflection):

    answer = clean_text(answer)
    plan = clean_text(plan)
    reflection = clean_text(reflection)

    sections = [
               "EXECUTION PLAN",
  
        plan,
        "",
        "AGENT RESPONSE",
        answer,
        "",
        "REFLECTION",
        reflection,
    ]

    return "\n".join(sections)


def save_evaluation_output(session_id, query, response):

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    file_path = OUTPUT_DIR / "evaluation_outputs.json"

    record = {
        "session_id": clean_text(session_id),
        "query": clean_text(query),
        "answer": clean_text(response.get("answer", "")),
        "plan": clean_text(response.get("plan", "")),
        "reflection": clean_text(response.get("reflection", ""))
    }

    if file_path.exists():

        try:
            with open(file_path,"r",encoding="utf-8") as file:

                data = json.load(file)

                if not isinstance(data, list):
                    data = []

        except Exception:
            data = []

    else:
        data = []

    data.append(record)

    with open(file_path,"w",encoding="utf-8") as file:

        json.dump(data,file,indent=4,ensure_ascii=False)


def save_sample_run(content):

    OUTPUT_DIR.mkdir(parents=True,exist_ok=True)

    file_path = OUTPUT_DIR / "sample_agent_run.txt"

    with open(file_path,"w",encoding="utf-8") as file:

        file.write(clean_text(content))


def save_raw_response(filename, data):

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    file_path = OUTPUT_DIR / filename

    with open(file_path,"w",encoding="utf-8") as file:

        json.dump(data,file,indent=4,ensure_ascii=False,default=str)