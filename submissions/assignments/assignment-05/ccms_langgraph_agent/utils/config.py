try:
    import os
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Error: {e}")
    
def load_env():
    if not load_dotenv():
        print(f"Environment file not present. Configure a .env file and try again.")
    try:
        os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    except ValueError as e:
        print(f"GROQ_API_KEY not configured in environment. Error: {e}")