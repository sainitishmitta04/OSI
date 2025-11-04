from fastmcp import FastMCP
import requests
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("ACCUWEATHER_API_KEY")

# 1️⃣ Create the MCP server
mcp = FastMCP(name="Weather Demo Server")

# 2️⃣ Define the weather tool
@mcp.tool
def get_simple_weather(city: str, language: str = "en-us") -> dict:
    """
    Returns a simple, human-readable weather summary for a given city using the AccuWeather API.
    Example output: "The temperature in London is 23°C and it’s sunny."
    """
    if not API_KEY:
        raise ValueError("AccuWeather API key not found in .env")

    # Step 1 — Get location key
    loc_url = "https://dataservice.accuweather.com/locations/v1/cities/search"
    params = {"apikey": API_KEY, "q": city}
    loc_response = requests.get(loc_url, params=params, timeout=5)

    if loc_response.status_code != 200:
        raise ValueError(f"Failed to fetch location key: {loc_response.text}")

    loc_data = loc_response.json()
    if not loc_data:
        raise ValueError(f"City '{city}' not found.")

    location_key = loc_data[0]["Key"]
    city_name = loc_data[0]["EnglishName"]
    country_name = loc_data[0]["Country"]["EnglishName"]

    # Step 2 — Get current conditions
    weather_url = f"https://dataservice.accuweather.com/currentconditions/v1/{location_key}"
    weather_params = {"apikey": API_KEY, "language": language, "details": "false"}
    weather_response = requests.get(weather_url, params=weather_params, timeout=5)

    if weather_response.status_code != 200:
        raise ValueError(f"Failed to fetch weather: {weather_response.text}")

    weather_data = weather_response.json()
    if not weather_data:
        raise ValueError("Weather data not available.")

    current = weather_data[0]
    temp_c = current.get("Temperature", {}).get("Metric", {}).get("Value")
    condition = current.get("WeatherText", "Unknown conditions")

    # Step 3 — Return summary
    summary = f"The temperature in {city_name}, {country_name} is {temp_c}°C and it's {condition.lower()}."

    return {
        "city": city_name,
        "country": country_name,
        "temperature_C": temp_c,
        "condition": condition,
        "summary": summary,
    }

# 3️⃣ Run the server
if __name__ == "__main__":
    print("Weather Demo Server is running...")
    mcp.run()
