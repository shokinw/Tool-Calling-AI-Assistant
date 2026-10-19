
import httpx
from app.schemas import CalculatorInput


def calculate_percentage(amount: float, percentage: float) -> dict:
    data = CalculatorInput(
        amount=amount,
        percentage=percentage
    )

    return {
        "amount": data.amount,
        "percentage": data.percentage,
        "result": round(data.amount * data.percentage / 100, 2)
    }


def get_weather(city: str) -> dict:
    """Fetch current weather for a city using Open-Meteo."""

    try:
        geo_response = httpx.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1},
            timeout=10
        )
        geo_response.raise_for_status()
        places = geo_response.json().get("results", [])

        if not places:
            return {"error": f"City not found: {city}"}

        place = places[0]

        weather_response = httpx.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": "temperature_2m,relative_humidity_2m",
                "timezone": "auto"
            },
            timeout=10
        )
        weather_response.raise_for_status()

        current = weather_response.json()["current"]

        return {
            "city": place["name"],
            "temperature_c": current["temperature_2m"],
            "humidity_percent": current["relative_humidity_2m"]
        }

    except (httpx.HTTPError, KeyError, ValueError) as error:
        return {"error": f"Weather lookup failed: {error}"}
