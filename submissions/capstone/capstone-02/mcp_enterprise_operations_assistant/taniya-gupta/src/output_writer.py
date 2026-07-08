import json
from pathlib import Path

# service-health
# ├── list_services
# ├── get_service_health
# └── get_active_incidents
# support-ticket
# ├── search_tickets
# ├── get_ticket_details
# └── get_high_priority_tickets
# change-management
# ├── list_recent_changes
# ├── get_change_details
# └── get_changes_for_service

def parse_execution_history(history):
    "Parsing langchain history to extract the details like servers and tools used and so on"
    servers_used=set()
    tools_used=[]
    evidence={
        "services":[],
        "incidents" : [],
        "tickets": [],
        "changes": []
    }

    tool_server_map={
        "list_services": "service-health",
        "get_service_health":"service-health",
        "get_active_incidents": "service-health",
        "search_tickets":"support-ticket",
        "get_ticket_details":"support-ticket",
        "get_high_priority_tickets":"support-ticket",
        "list_recent_changes":"change-management",
        "get_change_details":"change-management",
        "get_changes_for_service":"change-management",
        "get_changes_for_services":"change-management"
    }

    seen_services=set()
    seen_incidents=set()
    seen_tickets=set()
    seen_changes=set()

    for msg in history:
        msg_type=type(msg).__name__
        if msg_type=="ToolMessage":
            tool_name=getattr(msg, "name")
            if tool_name in tool_server_map:
                servers_used.add(tool_server_map[tool_name])
                tools_used.append(tool_name)

                content_str=getattr(msg, "content")
                content=json.loads(content_str)

                if tool_name in ["get_service_health", "list_services"]:
                    services=[]
                    if "service" in content:
                        services.append(content["service"])
                    elif "services" in content:
                        val = content["services"]
                        if isinstance(val, list):
                            services.extend(val)
                        else:
                            services.append(val)
                    for s in services:
                        sname= s.get("service_name")
                        if sname not in seen_services:
                            seen_services.add(sname)
                            evidence["services"].append({
                                "service_name": sname,
                                "status": s.get("status"),
                                "error_rate_percent": s.get("error_rate_percent"),
                                "average_latency_ms": s.get("average_latency_ms")
                            })
                elif tool_name == "get_active_incidents":
                    incidents=content.get("incidents")
                    for i in incidents:
                        i_id=i.get("incident_id")
                        if i_id and i_id not in seen_incidents:
                            seen_incidents.add(i_id)
                            evidence["incidents"].append({
                                "incident_id": i_id,
                                "severity": i.get("severity"),
                                "status": i.get("status")
                            })
                elif tool_name in ["get_ticket_details", "search_tickets", "get_high_priority_tickets"]:
                    tickets=[]
                    if "ticket" in content:
                        tickets.append(content["ticket"])
                    elif "tickets" in content:
                        val = content["tickets"]
                        if isinstance(val, list):
                            tickets.extend(val)
                        else:
                            tickets.append(val)
                    for t in tickets:
                        tid=t.get("ticket_id")
                        if tid not in seen_tickets:
                            seen_tickets.add(tid)
                            evidence["tickets"].append({
                                "ticket_id": tid,
                                "service_name": t.get("service_name"),
                                "priority": t.get("priority"),
                                "status": t.get("status"),
                                "subject": t.get("subject")
                            })
                elif tool_name in ["list_recent_changes", "get_change_details", "get_changes_for_service", "get_changes_for_services"]:
                    changes=[]
                    if "change" in content:
                        changes.append(content["change"])
                    elif "changes" in content:
                        val = content["changes"]
                        if isinstance(val, list):
                            changes.extend(val)
                        else:
                            changes.append(val)
                    for c in changes:
                        cid=c.get("change_id")
                        if cid not in seen_changes:
                            seen_changes.add(cid)
                            evidence["changes"].append({
                                "change_id": cid,
                                "risk": c.get("risk"),
                                "implemented_at": c.get("implemented_at")
                            })

    return list(servers_used), tools_used, evidence

def save_query_result(results):
    "save structured results in output dir"
    out_dir= Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True, parents=True)
    output_file=out_dir / "mandatory_query_results.json"

    with open(output_file, "w") as f:
        json.dump(results,f,indent=2)
    print("saved query results")

def save_output_samples(results):
    "save outputs"
    out_dir= Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(exist_ok=True, parents=True)
    output_file=out_dir / "sample_run_outputs.md"

    lines=[]
    for res in results:
        qid= res.get("query_id")
        query= res.get("user_query")
        servers=res.get("servers_used")
        tools=res.get("tools_used")
        final_answer=res.get("final_answer")
        lines.append(f"{qid}")
        lines.append("User query:")
        lines.append(f"{query}")
        lines.append("Servers used:")
        for s in servers:
            lines.append(f"{s}")
            lines.append("")
        lines.append("Tools used:")
        for t in tools:
            lines.append(f"{t}")
            lines.append("")
        lines.append("Final answer:")
        lines.append(f"{final_answer}")


    with open(output_file,"w") as f:
        f.write("\n".join(lines))
    print("batch run outputs are saved")