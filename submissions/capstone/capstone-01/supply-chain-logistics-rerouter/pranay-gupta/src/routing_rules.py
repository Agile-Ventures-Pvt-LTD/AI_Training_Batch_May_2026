from typing import Optional


def evaluate_route(metadata: dict,route: dict,warehouse_context: dict,) -> tuple:
    utilization = warehouse_context.get("current_utilization_pct", 0)
    status = warehouse_context.get("operational_status", "")
    risk = warehouse_context.get("risk_tier", "")
    added_delay = route.get("added_delay_hours", 0)
    max_tolerable = metadata.get("maximum_tolerable_delay_hours")

    if utilization > 85:
        decision = "ROUTE_CLARIFICATION"
        reason = "Warehouse utilization exceeds 85 percent"
    elif status != "ACTIVE":
        decision = "ROUTE_CLARIFICATION"
        reason = "Warehouse operational status is not ACTIVE"
    elif risk == "ELEVATED":
        decision = "ROUTE_CLARIFICATION"
        reason = "Warehouse risk tier is ELEVATED"
    elif added_delay > 120:
        decision = "CRITICAL_DELAY"
        reason = "Added route delay exceeds 120 hours"
    elif max_tolerable is not None and added_delay > max_tolerable:
        decision = "ROUTE_CLARIFICATION"
        reason = "Added delay exceeds maximum tolerable delay"
    else:
        decision = "OPTIMAL_PATH_FOUND"
        reason = "Warehouse and route conditions are acceptable"

    score = calculate_reroute_impact_score(
        utilization, status, risk, added_delay, max_tolerable
    )

    return decision, reason, score


def calculate_reroute_impact_score(utilization: int,status: str,risk: str,added_delay: int,max_tolerable: Optional[int],) -> int:
    score = 0

    if utilization > 85:
        score += 30
    if risk == "ELEVATED":
        score += 25
    if status != "ACTIVE":
        score += 30
    if max_tolerable is not None and added_delay > max_tolerable:
        score += 25
    if added_delay > 120:
        score += 50

    return min(score, 100)