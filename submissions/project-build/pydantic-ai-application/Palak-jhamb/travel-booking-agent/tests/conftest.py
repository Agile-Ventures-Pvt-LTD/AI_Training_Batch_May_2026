from src.tools.database import get_details
from src.tools.weather import get_weather
from src.guardrails_config import profinity_guard, toxic_guard



def test_get_details():
    result=get_details(user_name="Alice Smith")
    assert result['found']==True
    assert result['user']["user_name"]=="Alice Smith"

def test_get_weather():
    result=get_weather(location="Sonipat")
    assert result['fetch']==True

def test_profinity():
    result=profinity_guard("hello")
    assert result["found"]==True

def test_toxicity():
    result=toxic_guard("hello")
    assert result["found"]==True


    



