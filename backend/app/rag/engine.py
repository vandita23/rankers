"""Gemini embeddings + PostgreSQL/pgvector retrieval for KisanAI."""

from __future__ import annotations

from google import genai
from google.genai import types

from app.core.config import DATABASE_URL, GEMINI_API_KEY
from app.core.db import query
from app.rag.config import (
    EMBEDDING_DIMENSION,
    EMBEDDING_MODEL,
    RAG_MIN_SIMILARITY,
    RAG_TOP_K,
)


if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

_client = genai.Client(api_key=GEMINI_API_KEY)


def _vector_literal(values: list[float]) -> str:
    return "[" + ",".join(str(float(v)) for v in values) + "]"


def embed_text(text: str, *, task_type: str = "RETRIEVAL_QUERY") -> list[float]:
    """Create a Gemini embedding with the same dimension as the DB column."""
    if not text.strip():
        raise ValueError("Cannot embed empty text.")

    response = _client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSION,
            task_type=task_type,
        ),
    )

    if not response.embeddings or not response.embeddings[0].values:
        raise RuntimeError("Gemini returned an empty embedding.")

    values = list(response.embeddings[0].values)
    if len(values) != EMBEDDING_DIMENSION:
        raise RuntimeError(
            f"Embedding dimension mismatch: expected {EMBEDDING_DIMENSION}, got {len(values)}."
        )
    return values


def search(question: str, top_k: int | None = None) -> list[dict]:
    """Retrieve the most semantically similar chunks from pgvector."""
    if not DATABASE_URL:
        return []

    embedding = embed_text(question, task_type="RETRIEVAL_QUERY")
    vector = _vector_literal(embedding)
    limit = max(1, min(top_k or RAG_TOP_K, 10))

    rows = query(
        """
        SELECT id, content, source, category, metadata,
               1 - (embedding <=> %s::vector) AS similarity
        FROM rag_documents
        WHERE 1 - (embedding <=> %s::vector) >= %s
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """,
        (vector, vector, RAG_MIN_SIMILARITY, vector, limit),
    )

    return [dict(row) for row in rows or []]


def format_context(chunks: list[dict]) -> str:
    """Turn retrieved chunks into a compact context block for Gemini."""
    if not chunks:
        return "No relevant knowledge-base documents were retrieved."

    parts = []
    for i, chunk in enumerate(chunks, start=1):
        source = chunk.get("source") or "Unknown source"
        category = chunk.get("category") or "general"
        similarity = float(chunk.get("similarity") or 0)
        parts.append(
            f"[Source {i}: {source} | category={category} | similarity={similarity:.2f}]\n"
            f"{chunk['content']}"
        )
    return "\n\n".join(parts)


def source_names(chunks: list[dict]) -> list[str]:
    """Return unique source names for the frontend."""
    seen: set[str] = set()
    sources: list[str] = []
    for chunk in chunks:
        source = str(chunk.get("source") or "Knowledge base")
        if source not in seen:
            seen.add(source)
            sources.append(source)
    return sources
