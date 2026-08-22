from google import genai

from app.core.config import GEMINI_API_KEY
from app.rag import engine as rag_engine
from app.rag.config import RAG_ENABLED


if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

_client = genai.Client(api_key=GEMINI_API_KEY)

_SYSTEM_PROMPT = """
You are KisanAI, an AI agricultural assistant for farmers in India.

Your job is to provide practical, clear and easy-to-understand agricultural guidance.

Rules:
- Answer in the language requested by the user.
- Keep answers concise and practical.
- Prefer simple language that a farmer can understand.
- When knowledge-base context is provided, use it as the primary source for factual claims.
- Do not invent government schemes, statistics, sources, facts, or treatment instructions.
- If the supplied knowledge-base context does not contain enough information, clearly say that
  the available knowledge base does not contain enough information instead of making up details.
- Do not claim that you inspected an image, field, crop, soil, or weather conditions unless
  the system actually provided that information.
- For serious crop disease or treatment decisions, recommend consulting a qualified agricultural
  expert when appropriate.
"""


def _generate(prompt: str) -> str:
    response = _client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )
    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")
    return response.text.strip()


def get_reply(message: str, language: str) -> dict:
    """Generate a grounded agricultural response using RAG when enabled."""
    if not message.strip():
        raise ValueError("Message cannot be empty.")

    language_name = {"en": "English", "hi": "Hindi"}.get(language, language)
    chunks = []

    if RAG_ENABLED:
        try:
            chunks = rag_engine.search(message)
        except Exception:
            # Keep the chatbot usable if pgvector has not been configured yet.
            chunks = []

    context = rag_engine.format_context(chunks)
    sources = rag_engine.source_names(chunks)

    prompt = f"""
{_SYSTEM_PROMPT}

Respond in {language_name}.

Knowledge-base context retrieved for this question:
---
{context}
---

Farmer's question:
{message}

Answer the farmer directly. Do not mention embeddings, vector databases, RAG, prompts,
or internal system details. If the context is insufficient, say so briefly and avoid guessing.
"""

    return {
        "reply": _generate(prompt),
        "sources": sources,
    }
