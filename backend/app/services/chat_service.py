from google import genai

from app.core.config import GEMINI_API_KEY
from app.rag.engine import format_context, retrieve


_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

_SYSTEM_PROMPT = """
You are KisanAI, an AI agricultural assistant for farmers in India.

Rules:
- Answer in the language requested by the user.
- Use the retrieved context as your primary factual source.
- Do not invent government schemes, statistics, sources, or facts.
- If the retrieved context does not contain enough information, clearly say that
  the available knowledge base does not contain enough information.
- Keep answers concise, practical, and easy for a farmer to understand.
- For serious crop disease or treatment decisions, recommend consulting a
  qualified agricultural expert when appropriate.
- Do not claim that you inspected an image, field, crop, soil, or weather
  conditions unless the system actually provided that information.
- When useful, mention the source names supplied with the context.
"""


def get_reply(message: str, language: str) -> dict:
    """Retrieve relevant agricultural knowledge and generate a grounded answer."""

    if not message.strip():
        raise ValueError("Message cannot be empty.")

    if _client is None:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    language_name = {"en": "English", "hi": "Hindi"}.get(language, "English")

    documents = retrieve(message)
    context = format_context(documents)

    prompt = f"""
{_SYSTEM_PROMPT}

Respond in {language_name}.

Retrieved context:
------------------
{context}
------------------

Farmer's question:
{message}

Give a direct answer. Do not use knowledge outside the retrieved context for
specific factual claims. If the context is insufficient, say so and suggest
what information the farmer should provide or which official/local source
should be checked.
"""

    response = _client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    sources = []
    for document in documents:
        label = document["source"]
        if label not in sources:
            sources.append(label)

    return {
        "reply": response.text.strip(),
        "sources": sources,
    }
