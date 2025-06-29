from langchain.tools import tool
from pydantic import BaseModel, Field
import requests

class OpenMeteoInput(BaseModel):
    lati: float = Field(..., description="Latitude of the location")
    longi: float = Field(..., description="Longitude of the location")

@tool(args_schema=OpenMeteoInput)
def current_weather(lati: float, longi: float) -> str:
    """Fetch current temperature using Open-Meteo API for given coordinates."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lati,
        "longitude": longi,
        "current_weather": "true",
        "hourly": "temperature_2m",
        "forecast_days": 1
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return f"❌ Failed to fetch weather data: {response.status_code}"

    data = response.json()
    temperature = data.get("current_weather", {}).get("temperature")

    if temperature is not None:
        return f"🌡️ Current temperature at ({lati}, {longi}) is {temperature}°C"
    else:
        return "⚠️ Weather data not available for this location."
