from pydantic import BaseModel


class WeatherToday(BaseModel):
    tempC: float
    condition: str
    humidity: int
    windKmh: float
    rainChance: int


class ForecastDay(BaseModel):
    day: str
    tempC: float
    rain: int
    condition: str


class WeatherResponse(BaseModel):
    location: str
    today: WeatherToday
    forecast: list[ForecastDay]
    recommendation: str
    language: str
