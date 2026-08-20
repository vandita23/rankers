"""Weather service.

MOCK IMPLEMENTATION. Replace `get_weather()` internals with a real call to
a weather API (e.g. OpenWeatherMap, IMD) once WEATHER_API_KEY is set. Keep
the function signature the same so routes/weather.py doesn't need to change.
"""

_CONDITION = {"en": "Partly cloudy", "hi": "आंशिक रूप से बादल"}
_RECOMMENDATION = {
    "en": (
        "Rain is likely in the next few days. Delay any pesticide or urea "
        "application, and make sure field drainage channels are clear."
    ),
    "hi": (
        "अगले कुछ दिनों में बारिश संभव है। कीटनाशक या यूरिया डालने से बचें, "
        "और खेत की नालियां साफ रखें।"
    ),
}
_DAYS = {
    "en": ["Thu", "Fri", "Sat", "Sun", "Mon"],
    "hi": ["गुरु", "शुक्र", "शनि", "रवि", "सोम"],
}


def get_weather(location: str, crop: str | None, language: str) -> dict:
    """Return current + forecast weather plus an actionable recommendation.

    TODO(AI/ML team): call a real weather API here, e.g.
        raw = weather_client.forecast(location)
        return interpret_forecast(raw, crop, language)
    """
    days = _DAYS.get(language, _DAYS["en"])
    forecast = [
        {"day": days[0], "tempC": 30, "rain": 70, "condition": "rain"},
        {"day": days[1], "tempC": 29, "rain": 80, "condition": "rain"},
        {"day": days[2], "tempC": 32, "rain": 20, "condition": "cloud"},
        {"day": days[3], "tempC": 34, "rain": 5, "condition": "sun"},
        {"day": days[4], "tempC": 33, "rain": 10, "condition": "sun"},
    ]
    return {
        "location": location,
        "today": {
            "tempC": 31,
            "condition": _CONDITION.get(language, _CONDITION["en"]),
            "humidity": 68,
            "windKmh": 12,
            "rainChance": 40,
        },
        "forecast": forecast,
        "recommendation": _RECOMMENDATION.get(language, _RECOMMENDATION["en"]),
    }
