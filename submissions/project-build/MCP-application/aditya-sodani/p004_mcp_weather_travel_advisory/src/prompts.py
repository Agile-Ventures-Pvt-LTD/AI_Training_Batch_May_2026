def travel_readiness_prompt(data):
    return (
        f"Travel advisory for {data['destination']}:\n"
        f"Weather risk is {data['weather_risk']}.\n"
        f"Travel is "
        + (
            "comfortable."
            if data["weather_risk"] == "LOW"
            else "manageable with precautions."
            if data["weather_risk"] == "MEDIUM"
            else "risky due to weather conditions."
        )
    )


def weather_risk_summary_prompt(data):
    factors = ", ".join(data.get("risk_factors", []))

    return (
        f"The overall weather risk for {data['destination']} is {data['weather_risk']}.\n"
        f"Reason: {factors if factors else 'No major risk factors.'}"
    )


def packing_recommendation_prompt(data):
    items = ["Water bottle"]

    if data["weather_risk"] != "LOW":
        items.append("Umbrella")

    if data["weather_risk"] == "HIGH":
        items.append("Avoid heavy outdoor gear")

    items.append("Light comfortable clothes")

    return items

# def travel_readiness_prompt(data):
#     return f"{data['destination']} travel is {data['weather_risk']}"


# def weather_risk_summary_prompt(data):
#     return f"Risk: {data['weather_risk']}"


# def packing_recommendation_prompt(data):
#     return ["Water bottle", "Umbrella"]