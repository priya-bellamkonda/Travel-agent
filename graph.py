import sys
import os

# Insert the project root so both agents/ and skills/ are always discoverable
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from langgraph.graph import StateGraph, END

from state import TravelState
from agents.weather_agent      import weather_agent
from agents.packing_agent      import packing_agent
from agents.trip_planner_agent import trip_planner_agent
from agents.restaurant_agent   import restaurant_agent
from agents.supervisor_agent   import supervisor_agent
from agents.security_agent     import security_agent


def build_graph():
    graph = StateGraph(TravelState)

    # Register all nodes
    graph.add_node("weather_agent",      weather_agent)
    graph.add_node("security_1",         security_agent)
    graph.add_node("packing_agent",      packing_agent)
    graph.add_node("security_2",         security_agent)
    graph.add_node("trip_planner_agent", trip_planner_agent)
    graph.add_node("security_3",         security_agent)
    graph.add_node("restaurant_agent",   restaurant_agent)
    graph.add_node("security_4",         security_agent)
    graph.add_node("supervisor_agent",   supervisor_agent)

    # Wire the edges
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