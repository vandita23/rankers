from datetime import datetime

import requests

from app.core.config import OPENWEATHER_API_KEY


CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def get_weather(
    location: str,
    crop: str | None = None,
    language: str = "en",
):
    if not OPENWEATHER_API_KEY:
        raise RuntimeError("OPENWEATHER_API_KEY is not configured.")

    params = {
        "q": location,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
    }

    try:
        current_response = requests.get(
            CURRENT_URL,
            params=params,
            timeout=20,
        )
        current_response.raise_for_status()
        current_data = current_response.json()

        forecast_response = requests.get(
            FORECAST_URL,
            params=params,
            timeout=20,
        )
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Weather service timed out. Please check your internet connection."
        )

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Weather service request failed: {exc}"
        )

    # -------------------------
    # Current weather
    # -------------------------

    current_temp = round(current_data["main"]["temp"])
    humidity = int(current_data["main"]["humidity"])
    wind_kmh = round(current_data["wind"]["speed"] * 3.6)

    current_condition = _normalize_condition(
        current_data["weather"][0]["main"]
    )

    # Get rain probability from the first forecast period.
    forecast_items = forecast_data.get("list", [])

    rain_chance = 0

    if forecast_items:
        rain_chance = round(
            forecast_items[0].get("pop", 0) * 100
        )

    # -------------------------
    # 5-day forecast
    # -------------------------

    forecast = _build_forecast(forecast_items)

    return {
        "location": current_data["name"],

        "today": {
            "tempC": current_temp,
            "condition": current_condition,
            "humidity": humidity,
            "windKmh": wind_kmh,
            "rainChance": rain_chance,
        },

        "forecast": forecast,

        "recommendation": _get_recommendation(
            condition=current_condition,
            temperature=current_temp,
            crop=crop,
            language=language,
        ),
    }


def _normalize_condition(condition: str) -> str:
    """
    Convert OpenWeather conditions into the values
    expected by the frontend.
    """

    condition = condition.lower()

    if "rain" in condition or "drizzle" in condition or "thunderstorm" in condition:
        return "rain"

    if "cloud" in condition:
        return "cloud"

    if "clear" in condition:
        return "sun"

    return "cloud"


def _build_forecast(items: list) -> list:
    """
    Convert OpenWeather's 3-hour forecast into
    five daily forecast entries.
    """

    days = {}

    for item in items:
        timestamp = item.get("dt")

        if not timestamp:
            continue

        date = datetime.fromtimestamp(timestamp).date()
        date_key = str(date)

        if date_key not in days:
            days[date_key] = []

        days[date_key].append(item)

    result = []

    for date_key, day_items in list(days.items())[:5]:
        # Pick the forecast closest to midday.
        selected = min(
            day_items,
            key=lambda x: abs(
                datetime.fromtimestamp(x["dt"]).hour - 12
            ),
        )

        temperatures = [
            item["main"]["temp"]
            for item in day_items
            if "main" in item and "temp" in item["main"]
        ]

        if temperatures:
            temperature = round(sum(temperatures) / len(temperatures))
        else:
            temperature = round(selected["main"]["temp"])

        rain_values = [
            item.get("pop", 0)
            for item in day_items
        ]

        rain_probability = round(
            max(rain_values) * 100
        ) if rain_values else 0

        date = datetime.fromtimestamp(
            selected["dt"]
        )

        result.append(
            {
                "day": date.strftime("%a"),
                "tempC": temperature,
                "rain": rain_probability,
                "condition": _normalize_condition(
                    selected["weather"][0]["main"]
                ),
            }
        )

    return result


def _get_recommendation(
    condition: str,
    temperature: int,
    crop: str | None,
    language: str,
) -> str:

    if language == "hi":

        if condition == "rain":
            return (
                "बारिश की संभावना है। खेत में जल निकासी की "
                "व्यवस्था रखें और अनावश्यक सिंचाई से बचें।"
            )

        if temperature >= 35:
            return (
                "गर्मी अधिक है। फसल की सिंचाई और मिट्टी की "
                "नमी पर ध्यान दें।"
            )

        if crop:
            return (
                f"मौसम {crop} की निगरानी के लिए अनुकूल है। "
                "फसल की नियमित देखभाल जारी रखें।"
            )

        return (
            "मौसम सामान्य है। फसल की नियमित निगरानी और "
            "सिंचाई जारी रखें।"
        )

    if condition == "rain":
        return (
            "Rain is expected. Make sure your field has "
            "proper drainage and avoid unnecessary irrigation."
        )

    if temperature >= 35:
        return (
            "Temperatures are high. Pay attention to "
            "irrigation and soil moisture."
        )

    if crop:
        return (
            f"Weather conditions are suitable for monitoring "
            f"your {crop} crop."
        )

    return (
        "Weather conditions are currently suitable. "
        "Continue regular crop monitoring."
    )