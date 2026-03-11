import sys
import os
from dotenv import dotenv_values

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

_env_path = os.path.join(ROOT, ".env")
for _k, _v in dotenv_values(_env_path).items():
    os.environ[_k] = _v

from langgraph.graph import StateGraph, END
from state import TravelState
from skills.security_skill import validate_city, audit_log
from agents.weather_agent      import weather_agent
from agents.packing_agent      import packing_agent
from agents.trip_planner_agent import trip_planner_agent
from agents.restaurant_agent   import restaurant_agent
from agents.supervisor_agent   import supervisor_agent
from agents.security_agent     import security_agent


def build_graph():
    graph = StateGraph(TravelState)
    graph.add_node("weather_agent",      weather_agent)
    graph.add_node("security_1",         security_agent)
    graph.add_node("packing_agent",      packing_agent)
    graph.add_node("security_2",         security_agent)
    graph.add_node("trip_planner_agent", trip_planner_agent)
    graph.add_node("security_3",         security_agent)
    graph.add_node("restaurant_agent",   restaurant_agent)
    graph.add_node("security_4",         security_agent)
    graph.add_node("supervisor_agent",   supervisor_agent)
    graph.set_entry_point("weather_agent")
    graph.add_edge("weather_agent",      "security_1")
    graph.add_edge("security_1",         "packing_agent")
    graph.add_edge("packing_agent",      "security_2")
    graph.add_edge("security_2",         "trip_planner_agent")
    graph.add_edge("trip_planner_agent", "security_3")
    graph.add_edge("security_3",         "restaurant_agent")
    graph.add_edge("restaurant_agent",   "security_4")
    graph.add_edge("security_4",         "supervisor_agent")
    graph.add_edge("supervisor_agent",   END)
    return graph.compile()


def ask_for_city() -> str:
    print("  WEATHER-AWARE TRAVEL PLANNER")
    print("Get live weather, packing tips, places to visit,")
    print("restaurant picks, and a full trip summary.\n")
    while True:
        raw = input("Enter the city you want to travel to: ").strip()
        valid, result = validate_city(raw)
        if valid:
            return result
        print(f"  WARNING: {result}  Please try again.\n")


def plan_trip(city: str) -> None:
    print(f"  PLANNING YOUR TRIP TO: {city.upper()}")

    audit_log("main", "TRIP_START", f"city={city}")
    app = build_graph()
    result = app.invoke({
        "city": city,
        "weather_report": "",
        "packing_advice": "",
        "activity_suggestions": "",
        "restaurant_suggestions": "",
        "final_summary": "",
        "_signature": "",
    })

    d = "-" * 60
    print(f"\n{d}\n  WEATHER IN {city.upper()}\n{d}")
    print(result["weather_report"])
    print(f"\n{d}\n  PACKING ADVICE FOR {city.upper()}\n{d}")
    print(result["packing_advice"])
    print(f"\n{d}\n  TOP 5 PLACES TO VISIT IN {city.upper()}\n{d}")
    print(result["activity_suggestions"])
    print(f"\n{d}\n  BEST RESTAURANTS IN {city.upper()}\n{d}")
    print(result["restaurant_suggestions"])
    print(f"\n{d}\n  FINAL SUMMARY FOR {city.upper()}\n{d}")
    print(result["final_summary"])
    audit_log("main", "TRIP_END", f"city={city}")


if __name__ == "__main__":
    destination = ask_for_city()
    plan_trip(destination)