
from langchain_core.messages import HumanMessage, SystemMessage


def build_final_summary(
    city: str,
    weather_report: str,
    packing_advice: str,
    activity_suggestions: str,
    restaurant_suggestions: str,
    llm,
) -> str:
    """
    Combines weather, packing, places, and restaurant info into a single
    polished travel summary for `city`.
    Uses the provided LangChain-compatible `llm` instance.
    """
    messages = [
        SystemMessage(content=(
            f"You are a travel assistant summarising a trip to {city} ONLY. "
            f"Combine all the information below into a clear, friendly, well-structured summary. "
            f"Use headings for each section. Do NOT mention any other city."
        )),
        HumanMessage(content=(
            f"City: {city}\n\n"
            f"--- WEATHER ---\n{weather_report}\n\n"
            f"--- PACKING ---\n{packing_advice}\n\n"
            f"--- PLACES TO VISIT ---\n{activity_suggestions}\n\n"
            f"--- RESTAURANTS ---\n{restaurant_suggestions}"
        )),
    ]
    response = llm.invoke(messages)
    return response.content