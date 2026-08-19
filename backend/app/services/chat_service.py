"""LLM / assistant service.

MOCK IMPLEMENTATION. Replace `get_reply()` internals with a real LLM call
(OpenAI/Anthropic/hosted model) once the AI/ML/RAG team is ready. Keep the
function signature the same so routes/chat.py doesn't need to change.
"""

_MOCK_REPLY = {
    "en": (
        "This is a placeholder answer. Once the LLM is connected, this will "
        "be a real AI-generated response to your farming question."
    ),
    "hi": (
        "यह एक अस्थायी उत्तर है। LLM जुड़ने के बाद, यह आपके कृषि प्रश्न का "
        "वास्तविक AI-जनित उत्तर होगा।"
    ),
}


def get_reply(message: str, language: str) -> dict:
    """Return {reply, sources} for a farmer's question.

    TODO(AI/RAG team): call the LLM here, e.g.
        response = llm_client.complete(prompt=build_prompt(message, language))
        return {"reply": response.text, "sources": response.sources}
    """
    return {
        "reply": _MOCK_REPLY.get(language, _MOCK_REPLY["en"]),
        "sources": ["MOCK — not a real source"],
    }
