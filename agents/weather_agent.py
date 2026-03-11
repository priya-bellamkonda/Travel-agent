import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dotenv import dotenv_values
for _k, _v in dotenv_values(os.path.join(os.path.dirname(__file__), "..", ".env")).items():
    os.environ[_k] = _v

from state import TravelState
from skills.weather_skill import fetch_weather
from skills.security_skill import audit_log


def weather_agent(state: TravelState) -> TravelState:
    city = state["city"]
    audit_log("WeatherAgent", "START", f"city={city}")
    report = fetch_weather(city)
    audit_log("WeatherAgent", "DONE", f"report_length={len(report)}")
    return {**state, "weather_report": report}