
import os
import requests


def fetch_weather(city: str) -> str:
    """
    Fetches current weather for the given city.
    Returns a formatted weather report string.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return f"[WeatherSkill] ERROR: OPENWEATHER_API_KEY not set in environment."

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        return f"[WeatherSkill] Network error: {e}"

    if response.status_code != 200:
        return (
            f"[WeatherSkill] Could not fetch weather for '{city}'. "
            f"HTTP {response.status_code}: {response.text}"
        )

    data = response.json()
    temp       = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    condition  = data["weather"][0]["description"]
    humidity   = data["main"]["humidity"]
    wind       = data["wind"]["speed"]

    report = (
        f"City: {city}\n"
        f"Condition: {condition}\n"
        f"Temperature: {temp}°C (feels like {feels_like}°C)\n"
        f"Humidity: {humidity}%\n"
        f"Wind Speed: {wind} m/s"
    )
    return report