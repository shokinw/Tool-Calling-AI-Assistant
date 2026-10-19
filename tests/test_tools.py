
import httpx

from app.tools import calculate_percentage, get_weather


# ---------- Calculator tests ----------


def test_weather_success(monkeypatch):
    responses = [
        httpx.Response(
            200,
            request=httpx.Request(
                "GET",
                "https://geocoding-api.open-meteo.com/v1/search"
            ),
            json={
                "results": [{
                    "name": "Bengaluru",
                    "latitude": 12.97,
                    "longitude": 77.59
                }]
            }
        ),
        httpx.Response(
            200,
            request=httpx.Request(
                "GET",
                "https://api.open-meteo.com/v1/forecast"
            ),
            json={
                "current": {
                    "temperature_2m": 25.0,
                    "relative_humidity_2m": 60
                }
            }
        )
    ]

    def fake_get(*args, **kwargs):
        return responses.pop(0)

    monkeypatch.setattr("app.tools.httpx.get", fake_get)

    result = get_weather("Bengaluru")

    assert result["city"] == "Bengaluru"
    assert result["temperature_c"] == 25.0
    assert result["humidity_percent"] == 60


def test_weather_city_not_found(monkeypatch):
    def fake_get(*args, **kwargs):
        return httpx.Response(
            200,
            request=httpx.Request(
                "GET",
                "https://geocoding-api.open-meteo.com/v1/search"
            ),
            json={"results": []}
        )

    monkeypatch.setattr("app.tools.httpx.get", fake_get)

    result = get_weather("UnknownCity123")

    assert "error" in result
    assert "City not found" in result["error"]



def test_weather_api_failure(monkeypatch):
    # Simulate a network connection failure.
    def fake_get(*args, **kwargs):
        raise httpx.ConnectError("Network unavailable")

    monkeypatch.setattr("app.tools.httpx.get", fake_get)

    result = get_weather("Bengaluru")

    assert "error" in result
    assert "Weather lookup failed" in result["error"]

def test_weather_http_error(monkeypatch):
    def fake_get(*args, **kwargs):
        return httpx.Response(
            503,
            request=httpx.Request(
                "GET",
                "https://geocoding-api.open-meteo.com/v1/search"
            )
        )

    monkeypatch.setattr("app.tools.httpx.get", fake_get)

    result = get_weather("Bengaluru")

    assert "error" in result
    assert "Weather lookup failed" in result["error"]
