import openai
from pydantic_ai import Agent, WebSearchTool
from guardrails_config import output_safety_guardrail, safe_input_guardrail
from tools.weather import fetch_weather, geocode_city
import logging
from agent import (
    output_guardrail,
    OutputGuardrailTripwireTriggered,
    Agent,
    Runner,
    TResponseInputItem,
    FunctionTool,
    RunContextWrapper,
    function_tool,
    WebSearchTool,
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    set_tracing_export_api_key
)

logger = logging.getLogger(__name__)
agent = Agent(
    name="TravelAdvisor",
    instructions="""
    You are a detailed, friendly, and helpful travel planning assistant. Clearly follow these steps when assisting users:

    1. **Weather Forecast**:  
       Fetch the weather forecast for the destination city for the next 24 hours. Provide a concise yet detailed summary, including temperature ranges and general conditions (e.g., sunny, rainy, cloudy).

    2. **Places of Interest**:  
       Recommend attractions based on weather conditions:
       - **Rainy or unfavorable weather**: Suggest indoor places such as museums, galleries, historical sites, or shopping centers.
       - **Sunny or pleasant weather**: Suggest outdoor attractions like parks, landmarks, scenic spots, or walking tours.
       - **Mixed conditions**: Suggest a balanced mix of both indoor and outdoor attractions.

    3. **Fetch Updated Information (WebSearchTool)**:  
       Use the WebSearchTool to gather the latest information about local events, festivals, recent news, transportation disruptions, or travel advisories relevant to the user's destination. Clearly label this information as "Latest Updates" in your response.
       Only search for safe-for-work, factual, and travel-related information. Avoid querying controversial or sensitive topics.

    4. **Detailed Recommendations**:  
       Provide brief descriptions, highlights, or practical tips for each attraction you recommend, when available.

    5. **Additional Travel Advice**:  
       Include practical advice based on the weather and other information gathered—such as recommended clothing, footwear, or essential items to pack.
    **Format the entire response in Markdown**, using headings, bullet points, and bold text where appropriate to make it easy to read.
    **Answer only if you can determine the destination city**. If the user's request is off-topic or inappropriate, provide a polite response indicating the need for a valid destination city.
    Always be structured, verbose, and friendly. Aim to create a useful, practical, and enjoyable itinerary.
    """,
    tools=[
        fetch_weather,
        geocode_city,
        WebSearchTool()
    ],
    input_guardrails=[safe_input_guardrail],
    output_guardrails=[output_safety_guardrail]
)

if __name__ == "__main__":
    openai.api_key = OPENAI_API_KEY
    city = input("Enter your destination city: ").strip()
    if not city:
        print("City name cannot be empty.")
        exit(1)

    logger.info(f"Running TravelAdvisor for city: {city}")

    prompt = (
        f"I'm planning a trip within the next 24 hours to {city}. "
        "Provide a detailed weather forecast for the next 24 hours, suggest suitable places of interest "
        "based on the weather conditions, include the latest updates from the web about local events, "
        "travel advisories, or relevant news. Also, provide practical advice for traveling there."
    )
    

    try:
        result = Runner.run_sync(agent, prompt)
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Please give me the destination city that you want to travel to within the next 24 hours.")
    except OutputGuardrailTripwireTriggered:
        print("Please try rephrasing your request.")
    except Exception as e:
        logger.exception("Unexpected error during TravelAdvisor execution")
        print("An unexpected error occurred. Please try again later.")
