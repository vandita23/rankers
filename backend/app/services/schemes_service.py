"""Government scheme assistant service using the project's RAG pipeline."""

import json

from google import genai

from app.core.config import GEMINI_API_KEY
from app.rag import engine as rag_engine
from app.rag.config import RAG_ENABLED


if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

_client = genai.Client(api_key=GEMINI_API_KEY)


_SYSTEM_PROMPT = """
You are KisanAI, an AI government scheme assistant for farmers in India.

Your job is to answer questions about Indian government agricultural schemes
using ONLY the provided knowledge-base context.

Rules:
- Answer in the language requested by the user.
- Keep the answer concise, clear and practical.
- Use simple language that a farmer can understand.
- Do not invent scheme names, eligibility requirements, benefits,
  documents, application procedures, amounts, deadlines or sources.
- If the knowledge-base context does not contain enough information,
  say that the available knowledge base does not contain enough information.
- Do not mention embeddings, vector databases, RAG, prompts or internal
  system details.

You MUST return valid JSON in exactly this structure:

{
  "answer": "short answer to the farmer",
  "schemes": [
    {
      "name": "scheme name",
      "summary": "short summary",
      "eligibility": ["item 1", "item 2"],
      "documents": ["item 1", "item 2"],
      "steps": ["step 1", "step 2"],
      "source": "source/document name"
    }
  ]
}

If there are no relevant schemes in the context, return:

{
  "answer": "No relevant government scheme information was found.",
  "schemes": []
}
"""


def _generate(prompt: str) -> str:
    response = _client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text.strip()


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
            chunks = []

    context = rag_engine.format_context(chunks)

    prompt = f"""
{_SYSTEM_PROMPT}

Respond in {language_name}.

Knowledge-base context retrieved for this question:

---
{context}
---

Farmer's question:

{question}

Return ONLY valid JSON.
"""

    raw_response = _generate(prompt)

    # Remove markdown code fences if Gemini happens to return them.
    cleaned = raw_response.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "", 1)
        cleaned = cleaned.replace("```", "", 1)
        cleaned = cleaned.strip()

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError:
        raise RuntimeError("Gemini returned an invalid scheme response.")

    return {
        "answer": result.get("answer", ""),
        "schemes": result.get("schemes", []),
    }