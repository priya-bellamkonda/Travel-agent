import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dotenv import dotenv_values
for _k, _v in dotenv_values(os.path.join(os.path.dirname(__file__), "..", ".env")).items():
    os.environ[_k] = _v

from langchain_openai import ChatOpenAI
from state import TravelState
from skills.trip_planner_skill import get_activity_suggestions
from skills.security_skill import audit_log


def trip_planner_agent(state: TravelState) -> TravelState:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    city = state["city"]
    audit_log("TripPlannerAgent", "START", f"city={city}")
    suggestions = get_activity_suggestions(city, state["weather_report"], llm)
    audit_log("TripPlannerAgent", "DONE", f"suggestions_length={len(suggestions)}")
    return {**state, "activity_suggestions": suggestions}