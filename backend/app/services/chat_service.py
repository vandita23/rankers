from google import genai

from app.core.config import GEMINI_API_KEY


_client = genai.Client(api_key=GEMINI_API_KEY)

_SYSTEM_PROMPT = """
You are KisanAI, an AI agricultural assistant for farmers in India.

Your job is to provide practical, clear and easy-to-understand
agricultural guidance.

Rules:
- Answer in the language requested by the user.
- Keep answers concise and practical.
- Prefer simple language that a farmer can understand.
- Do not invent government schemes, statistics, sources, or facts.
- Do not present uncertain information as certain.
- For serious crop disease or treatment decisions, recommend consulting
  a qualified agricultural expert when appropriate.
- Do not claim that you inspected an image, field, crop, soil, or weather
  conditions unless the system actually provided that information.
"""


def get_reply(message: str, language: str) -> dict:
    """Generate an agricultural response using Gemini."""

    if not message.strip():
        raise ValueError("Message cannot be empty.")

    language_name = {
        "en": "English",
        "hi": "Hindi",
    }.get(language, language)

    prompt = f"""
{_SYSTEM_PROMPT}

Respond in {language_name}.

Farmer's question:
{message}
"""

    response = _client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return {
        "reply": response.text.strip(),
        "sources": [],
    }