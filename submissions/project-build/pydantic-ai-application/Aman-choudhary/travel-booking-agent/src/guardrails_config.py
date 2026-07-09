import re

def validate_input(user_input):
    if not re.match("^[A-Za-z ]+$", user_input):
        raise ValueError("Invalid input. Please enter a valid city name.")
    return user_input.strip()

def sanitize_output(text):
    return text.replace("<", "&lt;").replace(">", "&gt;")