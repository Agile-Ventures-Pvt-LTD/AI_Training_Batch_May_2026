from src.tools.db_service import query_travel_data
from src.tools.weather_service import get_weather
from src.groq_service import groq_chat

def handle_user_request(user_input):
    intent_data = groq_chat(f"Classify and respond: {user_input}")
    if "weather" in intent_data.lower():
        city = user_input.split()[-1]
        return get_weather(city)
    elif "hotel" in intent_data.lower():
        return query_travel_data("SELECT * FROM hotels WHERE city=?", (city,))
    else:
        return "I can help with flights, hotels, and weather."

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        print("Agent:", handle_user_request(user_input=user_input))