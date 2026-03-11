import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dotenv import dotenv_values
for _k, _v in dotenv_values(os.path.join(os.path.dirname(__file__), "..", ".env")).items():
    os.environ[_k] = _v

from langchain_openai import ChatOpenAI
from state import TravelState
from skills.restaurant_skill import get_restaurant_suggestions
from skills.security_skill import audit_log


def restaurant_agent(state: TravelState) -> TravelState:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    city = state["city"]
    audit_log("RestaurantAgent", "START", f"city={city}")
    suggestions = get_restaurant_suggestions(city, llm)
    audit_log("RestaurantAgent", "DONE", f"suggestions_length={len(suggestions)}")
    return {**state, "restaurant_suggestions": suggestions}