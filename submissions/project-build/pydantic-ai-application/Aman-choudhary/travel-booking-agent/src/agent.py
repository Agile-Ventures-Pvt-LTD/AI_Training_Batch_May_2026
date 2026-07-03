import os
import sys  
from db import search_flights, search_hotels
from guardrails import validate_input, sanitize_output
from tools.weather_service import get_weather
def travel_agent():
    print("Welcome to the Travel Booking Assistant!")
    destination = validate_input(input("Enter your destination: "))
    weather_info = get_weather(destination)
    print(f"Weather in {destination}: {weather_info}")
    flights = search_flights(destination)
    hotels = search_hotels(destination)
    print(sanitize_output(f"Flights: {flights}"))
    print(sanitize_output(f"Hotels: {hotels}"))
if __name__ == "__main__":
    travel_agent()