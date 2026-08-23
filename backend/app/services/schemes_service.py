"""Government scheme assistant service using the project's RAG pipeline."""

import json
import logging

from google import genai
from google.genai import types
from google.genai import errors


from app.core.config import GEMINI_API_KEY
from app.rag import engine as rag_engine
from app.rag.config import RAG_ENABLED

logger = logging.getLogger("kisanai")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

_client = genai.Client(api_key=GEMINI_API_KEY)


_SYSTEM_PROMPT = """
You are KisanAI, an AI government scheme assistant for farmers in India.

Use ONLY the provided knowledge-base context.

Rules:
- Answer in the requested language.
- Keep the answer concise, clear and practical.
- Use simple language.
- Never invent scheme names, eligibility, benefits, documents,
  application procedures, amounts, deadlines or sources.
- If the context does not contain enough information, say so.
- Do not mention RAG, embeddings, vector databases or internal systems.

Return JSON with exactly this structure:

{
  "answer": "short answer",
  "schemes": [
    {
      "name": "scheme name",
      "summary": "short summary",
      "eligibility": ["item"],
      "documents": ["item"],
      "steps": ["item"],
      "source": "source name"
    }
  ]
}

If there are no relevant schemes:

{
  "answer": "No relevant government scheme information was found.",
  "schemes": []
}
"""


def _generate(prompt: str) -> str:
    try:
        response = _client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        return response.text.strip()

    except errors.ClientError as e:
        if e.code == 429:
            raise RuntimeError(
                "Gemini API quota exceeded. Please use another API key "
                "or wait until the quota resets."
            ) from e

        raise


def _clean_scheme(scheme: dict) -> dict:
    """Guarantee that the frontend always receives the expected structure."""

    return {
        "name": str(scheme.get("name") or "Unknown scheme"),
        "summary": str(scheme.get("summary") or ""),
        "eligibility": (
            scheme.get("eligibility")
            if isinstance(scheme.get("eligibility"), list)
            else []
        ),
        "documents": (
            scheme.get("documents")
            if isinstance(scheme.get("documents"), list)
            else []
        ),
        "steps": (
            scheme.get("steps")
            if isinstance(scheme.get("steps"), list)
            else []
        ),
        "source": str(scheme.get("source") or "Knowledge base"),
    }


def query(question: str, language: str) -> dict:
    """Return {answer, schemes} using the project's RAG knowledge base."""

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    language_name = {
        "en": "English",
        "hi": "Hindi",
    }.get(language, language)

    chunks = []

    if RAG_ENABLED:
        try:
            chunks = rag_engine.search(question)
        except Exception:
            logger.exception("RAG search failed")
            chunks = []

    context = rag_engine.format_context(chunks)

    prompt = f"""
{_SYSTEM_PROMPT}

Respond in {language_name}.

Knowledge-base context:
---
{context}
---

Farmer's question:
{question}

Return ONLY valid JSON.
"""

    raw_response = _generate(prompt)

    try:
        result = json.loads(raw_response)
    except json.JSONDecodeError:
        logger.error("Invalid JSON returned by Gemini: %s", raw_response)
        raise RuntimeError("Gemini returned an invalid scheme response.")

    answer = result.get("answer", "")

    if not isinstance(answer, str):
        answer = str(answer)

    raw_schemes = result.get("schemes", [])

    if not isinstance(raw_schemes, list):
        raw_schemes = []

    schemes = []

    for scheme in raw_schemes:
        if isinstance(scheme, dict):
            schemes.append(_clean_scheme(scheme))

    return {
        "answer": answer,
        "schemes": schemes,
    }