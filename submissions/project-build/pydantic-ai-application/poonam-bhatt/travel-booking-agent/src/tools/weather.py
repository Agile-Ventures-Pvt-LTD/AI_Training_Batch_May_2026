def get_weather_forecast(destination: str, dates: str = None) -> str:
    """Fetch the weather forecast for a specific destination and travel dates.
    
    Args:
        destination (str): The city and country (e.g. 'Paris, France').
        dates (str, optional): The travel dates (e.g. '2026-08-15 to 2026-08-20').
    """
    dest_lower = destination.lower()
    if "paris" in dest_lower:
        return "Sunny and warm, high of 25°C, low of 16°C. Light breeze. Perfect for sightseeing."
    elif "tokyo" in dest_lower:
        return "Partly cloudy with mild humidity, high of 28°C, low of 21°C. 20% chance of showers."
    elif "new york" in dest_lower:
        return "Crisp and clear autumn weather, high of 18°C, low of 10°C."
    elif "miami" in dest_lower:
        return "Tropical and sunny, high of 31°C, low of 25°C. High humidity."
    elif "sydney" in dest_lower:
        return "Warm summer breeze, high of 26°C, low of 19°C."
    elif "london" in dest_lower:
        return "Mild and overcast, typical London drizzle expected, high of 19°C, low of 12°C."
    else:
        return f"Weather forecast for {destination} is currently sunny and clear, average temperature 22°C."





# Project: P005 Travel Booking Agent
# Author: Poonam Bhatt