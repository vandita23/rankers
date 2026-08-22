-- Run this AFTER your existing schema.sql in Supabase SQL Editor.
-- KisanAI RAG storage using PostgreSQL + pgvector.

create extension if not exists vector;

create table if not exists rag_documents (
    id bigserial primary key,
    content text not null,
    source text not null,
    category text not null default 'general',
    metadata jsonb not null default '{}'::jsonb,
    content_hash text not null unique,
    embedding vector(768) not null,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index if not exists rag_documents_category_idx
    on rag_documents(category);

create index if not exists rag_documents_embedding_idx
    on rag_documents using hnsw (embedding vector_cosine_ops);

create or replace function match_rag_documents(
    query_embedding vector(768),
    match_count integer default 5,
    min_similarity double precision default 0.25
)
returns table (
    id bigint,
    content text,
    source text,
    category text,
    metadata jsonb,
    similarity double precision
)
language sql
stable
as $$
    select
        d.id,
        d.content,
        d.source,
        d.category,
        d.metadata,
        1 - (d.embedding <=> query_embedding) as similarity
    from rag_documents d
    where 1 - (d.embedding <=> query_embedding) >= min_similarity
    order by d.embedding <=> query_embedding
    limit match_count;
$$;
