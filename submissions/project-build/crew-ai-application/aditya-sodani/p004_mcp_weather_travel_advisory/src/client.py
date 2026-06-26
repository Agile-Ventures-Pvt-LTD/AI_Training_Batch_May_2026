import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from src.tools import (
    validate_city_input_tool,
    get_weather_forecast_tool,
    normalize_weather_data_tool,
    calculate_weather_risk_tool,
    save_travel_advisory_tool
)

from src.prompts import (
    travel_readiness_prompt,
    weather_risk_summary_prompt,
    packing_recommendation_prompt
)

from src.report_writer import build_report

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")


def extract_with_llm(query: str):
    prompt = f"""
    Extract the following from the user query:
    1. City name
    2. Intent (one of: travel, packing, risk)

    Query: "{query}"

    Return JSON only:
    {{
        "city": "...",
        "intent": "travel | packing | risk"
    }}
    """

    response = llm.invoke(prompt).content

    try:
        import json
        return json.loads(response)
    except:
        return {"city": "Jaipur", "intent": "general"}


def generate_user_response(query, report):
    prompt = f"""
    User question: {query}

    Weather Risk: {report["weather_risk"]}
    Advisory: {report["travel_readiness_advisory"]}
    Packing: {report["packing_suggestions"]}

    Generate a clear and helpful answer for the user.
    Keep it short and practical.
    """

    return llm.invoke(prompt).content


def run(query: str):

    parsed = extract_with_llm(query)
    city = parsed.get("city", "Jaipur")
    intent = parsed.get("intent", "general")

    print(f"City: {city}")
    print(f"Intent: {intent}")

    step1 = validate_city_input_tool({"city_name": city})
    if not step1.get("success"):
        print(step1["message"])
        return

    step2 = get_weather_forecast_tool({
        "normalized_city_name": step1["normalized_city_name"]
    })

    step3 = normalize_weather_data_tool({
        "raw_weather_data": step2["raw_weather_data"]
    })

    step4 = calculate_weather_risk_tool({
        "normalized_weather_data": step3
    })


    report = build_report(step3, step4)


    travel_text = travel_readiness_prompt({
    "destination": step3["destination"],
    "weather_risk": step4["weather_risk"],
    "forecast_summary": "3-day weather outlook",
    "recommended_actions": step4.get("recommended_actions", [])
})

    risk_text = weather_risk_summary_prompt({
    "destination": step3["destination"],
    "weather_risk": step4["weather_risk"],
    "risk_factors": step4.get("risk_factors", [])
})

    packing_list = packing_recommendation_prompt({
    "destination": step3["destination"],
    "weather_risk": step4["weather_risk"],
    "risk_factors": step4.get("risk_factors", [])
})

    report["packing_suggestions"] = packing_list
    report["travel_readiness_advisory"] = travel_text
    report["weather_risk_explanation"] = risk_text

    save_travel_advisory_tool({"report": report})

    answer = generate_user_response(query, report)

    print("\nANSWER:\n")
    print(answer)

    print("\nJSON file saved at outputs/travel_advisory_report.json")


if __name__ == "__main__":
    while True:
        query = input("\nAsk your travel question (or exit): ")

        if query.lower() in ["exit", "quit", "q"]:
            print("Exiting...")
            break

        run(query)
