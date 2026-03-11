
from typing import TypedDict


class TravelState(TypedDict, total=False):
    city: str
    weather_report: str
    packing_advice: str
    activity_suggestions: str
    restaurant_suggestions: str
    final_summary: str
    _signature: str          