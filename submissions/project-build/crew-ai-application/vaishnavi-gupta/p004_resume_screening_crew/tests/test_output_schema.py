import os
import requests

from dotenv import load_dotenv

load_dotenv()

def test_weather_api():

    key = os.getenv("GROQ_API_KEY")

    url = (
        f"http://api.groq.com/v1/current.json"
        f"?key={key}&q=Delhi"
    )

    response = requests.get(url)

    assert response.status_code == 200

    print("✅  API Working")


if __name__ == "__main__":
    ai_resume_screening_and_interview_planning()



