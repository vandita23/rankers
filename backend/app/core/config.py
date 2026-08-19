import os

from dotenv import load_dotenv

load_dotenv()


def _get_env(name: str, default: str = "") -> str:
    """Read an environment variable and remove surrounding whitespace."""
    return os.getenv(name, default).strip()


def _get_origins() -> list[str]:
    """Parse comma-separated frontend origins from CORS_ORIGINS."""
    value = _get_env("CORS_ORIGINS", "http://localhost:5173")

    return [
        origin.strip().rstrip("/")
        for origin in value.split(",")
        if origin.strip()
    ]


DATABASE_URL = _get_env("DATABASE_URL")
CORS_ORIGINS = _get_origins()

# These are optional until the corresponding AI/external services are added.
OPENAI_API_KEY = _get_env("OPENAI_API_KEY")
WEATHER_API_KEY = _get_env("WEATHER_API_KEY")
DISEASE_MODEL_PATH = _get_env("DISEASE_MODEL_PATH")