-- Supabase pgvector Schema for Open Systems RAG
-- Run this in Supabase SQL Editor

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Document chunks table (stores vectorized content)
CREATE TABLE IF NOT EXISTS document_chunks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- File metadata
  file_path TEXT NOT NULL,
  file_title TEXT NOT NULL,

  -- Chunk metadata
  chunk_index INTEGER NOT NULL,
  chunk_type TEXT NOT NULL, -- 'heading', 'paragraph', 'list', etc.

  -- Content
  content TEXT NOT NULL,
  heading_path TEXT, -- e.g., "Introduction > System Overview > Goals"

  -- Embedding
  embedding vector(1536), -- OpenAI text-embedding-3-small dimension

  -- Classification
  priority INTEGER NOT NULL, -- 1-5 (1 = highest)
  status TEXT NOT NULL, -- 'current', 'historical', 'deprecated', 'unknown'

  -- Dates (from Google Drive where available)
  date_created TIMESTAMP WITH TIME ZONE,
  date_modified TIMESTAMP WITH TIME ZONE,
  has_gdrive_dates BOOLEAN DEFAULT FALSE,

  -- Statistics
  word_count INTEGER,
  char_count INTEGER,

  -- Cross-references
  file_references TEXT[], -- Array of referenced file paths
  referenced_by TEXT[], -- Array of files that reference this document

  -- Quality tracking (for Phase 4)
  flagged BOOLEAN DEFAULT FALSE,
  flag_reason TEXT,
  flag_date TIMESTAMP WITH TIME ZONE,
  quality_score FLOAT DEFAULT 1.0,

  -- Metadata
  indexed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  -- Composite unique constraint
  UNIQUE(file_path, chunk_index)
);

-- Indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_chunks_file_path ON document_chunks(file_path);
CREATE INDEX IF NOT EXISTS idx_chunks_priority ON document_chunks(priority);
CREATE INDEX IF NOT EXISTS idx_chunks_status ON document_chunks(status);
CREATE INDEX IF NOT EXISTS idx_chunks_date_modified ON document_chunks(date_modified DESC);
CREATE INDEX IF NOT EXISTS idx_chunks_quality ON document_chunks(quality_score DESC);
CREATE INDEX IF NOT EXISTS idx_chunks_flagged ON document_chunks(flagged) WHERE flagged = TRUE;

-- Vector similarity index (HNSW for fast approximate search)
CREATE INDEX IF NOT EXISTS idx_chunks_embedding ON document_chunks
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);

-- Full-text search index (for hybrid search)
ALTER TABLE document_chunks ADD COLUMN IF NOT EXISTS content_tsv tsvector
  GENERATED ALWAYS AS (to_tsvector('english', content)) STORED;

CREATE INDEX IF NOT EXISTS idx_chunks_content_tsv ON document_chunks USING gin(content_tsv);

-- Document metadata table (aggregated stats per file)
CREATE TABLE IF NOT EXISTS document_metadata (
  file_path TEXT PRIMARY KEY,
  title TEXT NOT NULL,

  -- Dates
  date_created TIMESTAMP WITH TIME ZONE,
  date_modified TIMESTAMP WITH TIME ZONE,
  has_gdrive_dates BOOLEAN DEFAULT FALSE,

  -- Classification
  priority INTEGER NOT NULL,
  status TEXT NOT NULL,

  -- Statistics
  word_count INTEGER,
  line_count INTEGER,
  chunk_count INTEGER,
  heading_count INTEGER,

  -- Topics
  topics TEXT[],

  -- Cross-references
  cross_references TEXT[],
  referenced_by TEXT[],
  reference_count INTEGER DEFAULT 0,

  -- Metadata
  indexed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_metadata_priority ON document_metadata(priority);
CREATE INDEX IF NOT EXISTS idx_metadata_status ON document_metadata(status);
CREATE INDEX IF NOT EXISTS idx_metadata_date_modified ON document_metadata(date_modified DESC);
CREATE INDEX IF NOT EXISTS idx_metadata_reference_count ON document_metadata(reference_count DESC);

-- Chunk flags table (for Phase 4 - content quality tracking)
CREATE TABLE IF NOT EXISTS chunk_flags (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  chunk_id UUID REFERENCES document_chunks(id) ON DELETE CASCADE,
  file_path TEXT NOT NULL,
  chunk_index INTEGER NOT NULL,
  reason TEXT NOT NULL,
  flagged_by TEXT,
  flagged_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  resolution TEXT, -- 'suppressed' | 'fixed' | 'reviewed'
  resolved_date TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_flags_file_path ON chunk_flags(file_path);
CREATE INDEX IF NOT EXISTS idx_flags_resolution ON chunk_flags(resolution);
CREATE INDEX IF NOT EXISTS idx_flags_chunk_id ON chunk_flags(chunk_id);

-- Document quality table (for Phase 4)
CREATE TABLE IF NOT EXISTS document_quality (
  file_path TEXT PRIMARY KEY,
  times_retrieved INTEGER DEFAULT 0,
  times_flagged INTEGER DEFAULT 0,
  helpful_count INTEGER DEFAULT 0,
  unhelpful_count INTEGER DEFAULT 0,
  quality_score FLOAT DEFAULT 1.0,
  suppressed BOOLEAN DEFAULT FALSE,
  last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_quality_score ON document_quality(quality_score DESC);
CREATE INDEX IF NOT EXISTS idx_quality_suppressed ON document_quality(suppressed) WHERE suppressed = TRUE;

-- Query logs table (for Phase 4 - analytics and feedback)
CREATE TABLE IF NOT EXISTS query_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  query_text TEXT NOT NULL,
  query_type TEXT, -- From query router: 'definition', 'implementation', etc.
  retrieved_files TEXT[],
  retrieved_chunks UUID[],
  user_feedback TEXT, -- 'helpful' | 'not_helpful' | 'bad_info'
  feedback_note TEXT,
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON query_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_logs_query_type ON query_logs(query_type);

-- Hybrid search function (semantic + keyword)
CREATE OR REPLACE FUNCTION hybrid_search(
  query_embedding vector(1536),
  query_text TEXT,
  match_count INT DEFAULT 10,
  similarity_threshold FLOAT DEFAULT 0.5
)
RETURNS TABLE (
  id UUID,
  file_path TEXT,
  file_title TEXT,
  chunk_index INTEGER,
  content TEXT,
  heading_path TEXT,
  priority INTEGER,
  status TEXT,
  date_modified TIMESTAMP WITH TIME ZONE,
  similarity FLOAT,
  rank FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    dc.id,
    dc.file_path,
    dc.file_title,
    dc.chunk_index,
    dc.content,
    dc.heading_path,
    dc.priority,
    dc.status,
    dc.date_modified,
    (1 - (dc.embedding <=> query_embedding)) AS similarity,
    -- Combined rank: semantic similarity + keyword relevance + priority boost
    (
      (1 - (dc.embedding <=> query_embedding)) * 0.7 +
      ts_rank(dc.content_tsv, plainto_tsquery('english', query_text)) * 0.3
    ) * (1.0 / dc.priority::FLOAT) AS rank
  FROM document_chunks dc
  WHERE
    dc.flagged = FALSE -- Exclude flagged content
    AND (1 - (dc.embedding <=> query_embedding)) > similarity_threshold
  ORDER BY rank DESC
  LIMIT match_count;
END;
$$;

-- Temporal boosted search (prioritizes recent documents)
CREATE OR REPLACE FUNCTION temporal_search(
  query_embedding vector(1536),
  query_text TEXT,
  match_count INT DEFAULT 10,
  recency_weight FLOAT DEFAULT 0.3
)
RETURNS TABLE (
  id UUID,
  file_path TEXT,
  file_title TEXT,
  chunk_index INTEGER,
  content TEXT,
  heading_path TEXT,
  priority INTEGER,
  status TEXT,
  date_modified TIMESTAMP WITH TIME ZONE,
  similarity FLOAT,
  temporal_score FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    dc.id,
    dc.file_path,
    dc.file_title,
    dc.chunk_index,
    dc.content,
    dc.heading_path,
    dc.priority,
    dc.status,
    dc.date_modified,
    (1 - (dc.embedding <=> query_embedding)) AS similarity,
    -- Temporal boost: newer docs ranked higher
    (
      (1 - (dc.embedding <=> query_embedding)) * (1 - recency_weight) +
      (EXTRACT(EPOCH FROM (NOW() - dc.date_modified)) / 31536000)::FLOAT * recency_weight
    ) * (1.0 / dc.priority::FLOAT) AS temporal_score
  FROM document_chunks dc
  WHERE
    dc.flagged = FALSE
    AND dc.has_gdrive_dates = TRUE -- Only use temporal boost if we have accurate dates
  ORDER BY temporal_score DESC
  LIMIT match_count;
END;
$$;

-- Status-filtered search (e.g., only current documents)
CREATE OR REPLACE FUNCTION status_search(
  query_embedding vector(1536),
  target_status TEXT,
  match_count INT DEFAULT 10
)
RETURNS TABLE (
  id UUID,
  file_path TEXT,
  file_title TEXT,
  content TEXT,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    dc.id,
    dc.file_path,
    dc.file_title,
    dc.content,
    (1 - (dc.embedding <=> query_embedding)) AS similarity
  FROM document_chunks dc
  WHERE
    dc.status = target_status
    AND dc.flagged = FALSE
  ORDER BY similarity DESC
  LIMIT match_count;
END;
$$;

-- Grant permissions (adjust for your Supabase role)
-- GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
-- GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO authenticated;

-- Summary
SELECT
  'Schema setup complete!' AS message,
  count(*) FILTER (WHERE table_name = 'document_chunks') AS chunks_table,
  count(*) FILTER (WHERE table_name = 'document_metadata') AS metadata_table,
  count(*) FILTER (WHERE table_name = 'chunk_flags') AS flags_table,
  count(*) FILTER (WHERE table_name = 'document_quality') AS quality_table,
  count(*) FILTER (WHERE table_name = 'query_logs') AS logs_table
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('document_chunks', 'document_metadata', 'chunk_flags', 'document_quality', 'query_logs');
