"""Ingest local agricultural documents into Supabase pgvector.

Run from backend/:
    python -m app.rag.ingest --path ../ai/documents

Supported: .txt, .md, .pdf, .docx
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

from app.core.db import query
from app.rag.engine import embed_text


SUPPORTED = {".txt", ".md", ".pdf", ".docx"}
CHUNK_SIZE = 1800
CHUNK_OVERLAP = 250


def read_document(path: Path) -> str:
    suffix = path.suffix.lower()

    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8")

    if suffix == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if suffix == ".docx":
        from docx import Document

        document = Document(str(path))
        return "\n".join(p.text for p in document.paragraphs)

    raise ValueError(f"Unsupported file type: {suffix}")


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str) -> list[str]:
    if len(text) <= CHUNK_SIZE:
        return [text] if text else []

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        chunk = text[start:end]

        if end < len(text):
            split_at = max(chunk.rfind("\n\n"), chunk.rfind(". "))
            if split_at >= CHUNK_SIZE // 2:
                end = start + split_at + (2 if chunk[split_at:split_at + 2] == ". " else 0)
                chunk = text[start:end]

        chunk = chunk.strip()
        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break
        start = max(end - CHUNK_OVERLAP, start + 1)

    return chunks


def category_for(path: Path, root: Path) -> str:
    relative = path.relative_to(root)
    return relative.parts[0] if len(relative.parts) > 1 else "general"


def source_name(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").strip()


def chunk_id(path: Path, chunk: str) -> str:
    return hashlib.sha256(f"{path}:{chunk}".encode("utf-8")).hexdigest()


def ingest(root: Path) -> int:
    files = [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED]
    if not files:
        print(f"No supported documents found under {root.resolve()}")
        return 0

    total = 0
    for path in files:
        text = clean_text(read_document(path))
        chunks = chunk_text(text)
        category = category_for(path, root)
        source = source_name(path)

        print(f"\n{path} -> {len(chunks)} chunks")
        for index, chunk in enumerate(chunks, start=1):
            digest = chunk_id(path, chunk)
            embedding = embed_text(chunk, task_type="RETRIEVAL_DOCUMENT")
            vector = "[" + ",".join(str(float(v)) for v in embedding) + "]"

            query(
                """
                INSERT INTO rag_documents
                    (content, source, category, metadata, content_hash, embedding)
                VALUES
                    (%s, %s, %s, %s::jsonb, %s, %s::vector)
                ON CONFLICT (content_hash)
                DO UPDATE SET
                    content = EXCLUDED.content,
                    source = EXCLUDED.source,
                    category = EXCLUDED.category,
                    metadata = EXCLUDED.metadata,
                    embedding = EXCLUDED.embedding,
                    updated_at = now()
                """,
                (
                    chunk,
                    source,
                    category,
                    '{"file": "' + path.name.replace('"', '') + '", "chunk": ' + str(index) + '}',
                    digest,
                    vector,
                ),
                fetch_all=False,
            )
            total += 1
            print(f"  ingested chunk {index}/{len(chunks)}")

    print(f"\nDone. Ingested/updated {total} chunks.")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default="../ai/documents", help="Document directory")
    args = parser.parse_args()
    ingest(Path(args.path).resolve())


if __name__ == "__main__":
    main()
