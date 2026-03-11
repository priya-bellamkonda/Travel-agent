import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dotenv import dotenv_values
for _k, _v in dotenv_values(os.path.join(os.path.dirname(__file__), "..", ".env")).items():
    os.environ[_k] = _v

from langchain_openai import ChatOpenAI
from state import TravelState
from skills.supervisor_skill import build_final_summary
from skills.security_skill import audit_log


def supervisor_agent(state: TravelState) -> TravelState:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    city = state["city"]
    audit_log("SupervisorAgent", "START", f"city={city}")
    summary = build_final_summary(
        city=city,
        weather_report=state["weather_report"],
        packing_advice=state["packing_advice"],
        activity_suggestions=state["activity_suggestions"],
        restaurant_suggestions=state["restaurant_suggestions"],
        llm=llm,
    )
    audit_log("SupervisorAgent", "DONE", f"summary_length={len(summary)}")
    return {**state, "final_summary": summary}