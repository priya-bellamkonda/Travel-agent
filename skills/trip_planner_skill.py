
from langchain_core.messages import HumanMessage, SystemMessage


def get_activity_suggestions(city: str, weather_report: str, llm) -> str:
    """
    Returns 5 real must-visit places in `city` adapted to current weather.
    Uses the provided LangChain-compatible `llm` instance.
    """
    messages = [
        SystemMessage(content=(
            f"You are a travel expert for {city} ONLY. "
            f"Suggest 5 real, well-known places to visit in {city} suited to the current weather. "
            f"Start your response with this exact heading: 'Must-Visit Places in {city}:'\n"
            f"Then format as a numbered list, one line description each.\n"
            f"Example:\n"
            f"Must-Visit Places in {city}:\n"
            f"1. Place Name - Short description\n"
            f"Do NOT mention any other city."
        )),
        HumanMessage(content=(
            f"Weather in {city}:\n{weather_report}\n\n"
            f"List 5 places to visit in {city}."
        )),
    ]
    response = llm.invoke(messages)
    return response.content