

from langchain_core.messages import HumanMessage, SystemMessage


def get_restaurant_suggestions(city: str, llm) -> str:
    """
    Returns 5 recommended restaurants in `city`.
    Uses the provided LangChain-compatible `llm` instance.
    """
    messages = [
        SystemMessage(content=(
            f"You are a local food expert for {city} ONLY. "
            f"Suggest 5 real, well-known restaurants in {city}. "
            f"Start your response with this exact heading: 'Best Restaurants in {city}:'\n"
            f"Format as a numbered list:\n"
            f"1. Restaurant Name - Cuisine type, one line about why it's great\n"
            f"Do NOT mention any other city."
        )),
        HumanMessage(content=(
            f"What are the 5 best restaurants to visit in {city}?"
        )),
    ]
    response = llm.invoke(messages)
    return response.content