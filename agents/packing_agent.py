import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dotenv import dotenv_values
for _k, _v in dotenv_values(os.path.join(os.path.dirname(__file__), "..", ".env")).items():
    os.environ[_k] = _v

from langchain_openai import ChatOpenAI
from state import TravelState
from skills.packing_skill import get_packing_advice
from skills.security_skill import audit_log


def packing_agent(state: TravelState) -> TravelState:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    city = state["city"]
    audit_log("PackingAgent", "START", f"city={city}")
    advice = get_packing_advice(city, state["weather_report"], llm)
    audit_log("PackingAgent", "DONE", f"advice_length={len(advice)}")
    return {**state, "packing_advice": advice}