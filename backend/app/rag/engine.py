import json
import math
import threading
from pathlib import Path

from google import genai
from google.genai import types

from app.core.config import GEMINI_API_KEY
from app.rag.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_DIMENSION,
    EMBEDDING_MODEL,
    INDEX_FILE,
    KNOWLEDGE_FILE,
    TOP_K,
)

_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
_lock = threading.Lock()
_index = None


def _require_client():
    if _client is None:
        raise RuntimeError("GEMINI_API_KEY is not configured.")


def _chunk_text(text: str) -> list[str]:
    text = " ".join(text.split()).strip()
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        chunk = text[start:end]

        if end < len(text):
            split_at = max(chunk.rfind(". "), chunk.rfind("। "), chunk.rfind(" "))
            if split_at > CHUNK_SIZE // 2:
                end = start + split_at + 1
                chunk = text[start:end]

        chunks.append(chunk.strip())
        if end >= len(text):
            break

        start = max(end - CHUNK_OVERLAP, start + 1)

    return chunks


def _embed_documents(texts: list[str], titles: list[str]) -> list[list[float]]:
    _require_client()
    result = _client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=EMBEDDING_DIMENSION,
        ),
    )
    return [list(item.values) for item in result.embeddings]


def _embed_query(text: str) -> list[float]:
    _require_client()
    result = _client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=EMBEDDING_DIMENSION,
        ),
    )
    return list(result.embeddings[0].values)


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if not na or not nb:
        return 0.0
    return dot / (na * nb)


def _build_index() -> dict:
    if not KNOWLEDGE_FILE.exists():
        raise RuntimeError(f"RAG knowledge file not found: {KNOWLEDGE_FILE}")

    records = json.loads(KNOWLEDGE_FILE.read_text(encoding="utf-8"))
    chunks = []

    for record in records:
        for i, chunk in enumerate(_chunk_text(record["content"])):
            chunks.append(
                {
                    "id": f'{record["id"]}-{i + 1}',
                    "title": record["title"],
                    "source": record["source"],
                    "content": chunk,
                }
            )

    embeddings = _embed_documents(
        [item["content"] for item in chunks],
        [item["title"] for item in chunks],
    )

    index = {
        "model": EMBEDDING_MODEL,
        "dimension": EMBEDDING_DIMENSION,
        "documents": [
            {**chunk, "embedding": embedding}
            for chunk, embedding in zip(chunks, embeddings)
        ],
    }

    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_text(
        json.dumps(index, ensure_ascii=False),
        encoding="utf-8",
    )
    return index


def _load_index() -> dict:
    global _index

    with _lock:
        if _index is not None:
            return _index

        if INDEX_FILE.exists():
            try:
                data = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
                if (
                    data.get("model") == EMBEDDING_MODEL
                    and data.get("dimension") == EMBEDDING_DIMENSION
                    and data.get("documents")
                ):
                    _index = data
                    return _index
            except (json.JSONDecodeError, OSError):
                pass

        _index = _build_index()
        return _index


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    index = _load_index()
    query_embedding = _embed_query(query)

    scored = []
    for item in index["documents"]:
        score = _cosine(query_embedding, item["embedding"])
        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [
        {
            "id": item["id"],
            "title": item["title"],
            "source": item["source"],
            "content": item["content"],
            "score": round(score, 4),
        }
        for score, item in scored[:top_k]
    ]


def format_context(documents: list[dict]) -> str:
    if not documents:
        return "No relevant documents were retrieved."

    blocks = []
    for i, doc in enumerate(documents, start=1):
        blocks.append(
            f"[Source {i}: {doc['title']} | {doc['source']}]\n"
            f"{doc['content']}"
        )
    return "\n\n".join(blocks)
