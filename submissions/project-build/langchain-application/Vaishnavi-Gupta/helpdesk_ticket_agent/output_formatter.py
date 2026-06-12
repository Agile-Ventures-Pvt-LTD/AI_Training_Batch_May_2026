from typing import Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.json import JSON


console = Console()


def build_response(
    user_request: str,
    plan_summary: str,
    tools_used: list,
    reflection_summary: str,
    final_answer: str,
    memory_used: bool = False,
    write_action_performed: bool = False
):
    """
    Standard response structure.
    """

    return {
        "user_request": user_request,
        "plan_summary": plan_summary,
        "tools_used": tools_used,
        "reflection_summary": reflection_summary,
        "final_answer": final_answer,
        "memory_used": memory_used,
        "write_action_performed": write_action_performed
    }



def print_json_response(
    response: Dict[str, Any]
):
    """
    Pretty JSON output.
    """

    console.print(
        JSON.from_data(response)
    )



def print_business_response(
    response: Dict[str, Any]
):
    """
    Cleaner operational display.
    """

    console.print(
        Panel(
            response["plan_summary"],
            title="Plan Summary"
        )
    )

    console.print(
        Panel(
            ", ".join(
                response["tools_used"]
            ),
            title="Tools Used"
        )
    )

    console.print(
        Panel(
            response["reflection_summary"],
            title="Reflection"
        )
    )

    console.print(
        Panel(
            response["final_answer"],
            title="Final Answer"
        )
    )



def format_error(
    error_message: str
):
    """
    Standard error response.
    """

    return {
        "user_request": "",
        "plan_summary": "",
        "tools_used": [],
        "reflection_summary": "",
        "final_answer": "",
        "memory_used": False,
        "write_action_performed": False,
        "error": error_message
    }



def is_write_operation(
    tools_used: list
):
    """
    Detect DB modifications.
    """

    write_tools = {
        "update_ticket_status",
        "add_ticket_comment",
        "save_user_preference",
        "summarize_conversation"
    }

    return any(
        tool in write_tools
        for tool in tools_used
    )



def format_agent_output(
    agent_result: Dict[str, Any]
):
    """
    Convert raw agent result
    into standard format.
    """

    if "error" in agent_result:

        return format_error(
            agent_result["error"]
        )

    return build_response(
        user_request=agent_result.get(
            "user_request",
            ""
        ),

        plan_summary=agent_result.get(
            "plan_summary",
            ""
        ),

        tools_used=agent_result.get(
            "tools_used",
            []
        ),

        reflection_summary=agent_result.get(
            "reflection_summary",
            ""
        ),

        final_answer=agent_result.get(
            "final_answer",
            ""
        ),

        memory_used=True,

        write_action_performed=is_write_operation(
            agent_result.get(
                "tools_used",
                []
            )
        )
    )