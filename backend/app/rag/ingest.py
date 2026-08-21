"""Build the local RAG embedding index.

Run from the backend directory:
    python -m app.rag.ingest
"""

from app.rag.engine import _build_index


if __name__ == "__main__":
    index = _build_index()
    print(f"RAG index created with {len(index['documents'])} chunks.")
