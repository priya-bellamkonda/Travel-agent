
from langchain_core.messages import HumanMessage, SystemMessage


def get_packing_advice(city: str, weather_report: str, llm) -> str:
    """
    Returns packing advice for `city` given its `weather_report`.
    Uses the provided LangChain-compatible `llm` instance.
    """
    messages = [
        SystemMessage(content=(
            f"You are a packing expert for {city} ONLY. "
            f"Give packing advice ONLY for {city} based on the weather below. "
            f"Be practical: list clothing, accessories, and essentials. "
            f"Do NOT mention any other city."
        )),
        HumanMessage(content=(
            f"Weather in {city}:\n{weather_report}\n\n"
            f"What should I pack for my trip to {city}?"
        )),
    ]
    response = llm.invoke(messages)
    return response.content