from app.core.config import _get_env

EMBEDDING_MODEL = _get_env("RAG_EMBEDDING_MODEL", "gemini-embedding-001")
EMBEDDING_DIMENSION = int(_get_env("RAG_EMBEDDING_DIMENSION", "768"))
RAG_TOP_K = int(_get_env("RAG_TOP_K", "5"))
RAG_MIN_SIMILARITY = float(_get_env("RAG_MIN_SIMILARITY", "0.25"))
RAG_ENABLED = _get_env("RAG_ENABLED", "true").lower() in {"1", "true", "yes", "on"}
