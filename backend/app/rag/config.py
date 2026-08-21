from pathlib import Path

RAG_DIR = Path(__file__).resolve().parents[2] / "data" / "rag"
KNOWLEDGE_FILE = RAG_DIR / "knowledge.json"
INDEX_FILE = RAG_DIR / "index.json"

TOP_K = 4
CHUNK_SIZE = 900
CHUNK_OVERLAP = 150
EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSION = 768
