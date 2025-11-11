# Open Systems RAG System Guide

## Overview

Your Open Systems documentation is now fully searchable using semantic RAG (Retrieval-Augmented Generation). The system indexes 210 documents (500+ pages) with hybrid search combining semantic similarity and keyword matching.

## Quick Start

### For AI Agents

**Search documents** before answering questions about Open Systems:

```bash
python scripts/search_compact.py "your query here"
```

**Example**:
```bash
python scripts/search_compact.py "governance voting mechanism"
```

**Output** (compact, ~200 tokens):
```
1. Open Game System Spec (similarity: 0.59)
   Section: 5. Governance
   Governance - **Proposal Voting:** Game design decisions, balance adjustments...
   Source: DATA-DUMP\Recent\From Open Systems Project in ChatGpt\open_game_system_spec.md

2. Open Ventures User Flow (similarity: 0.53)
   Section: 3.3 Voting and Stake Token Rules
   **One Vote per Token**: Each token = 1 vote...
   Source: DATA-DUMP\Recent\From Open Systems Project in ChatGpt\open_ventures_user_flow.md
```

### For Humans

**Interactive search**:
```bash
python scripts/query_rag.py
```

This provides more detailed results with full previews.

## System Architecture

### Components

1. **Document Chunks**: 2,670 semantic chunks from 210 markdown files
2. **Embeddings**: 1536-dimensional vectors (OpenAI text-embedding-3-small)
3. **Database**: Supabase pgvector with hybrid search
4. **Search Functions**:
   - `hybrid_search()` - Semantic (70%) + keyword (30%)
   - `temporal_search()` - Prioritizes recent documents
   - `status_search()` - Filters by status (current/historical/deprecated)

### Priority System

- **Priority 1 (11%)**: Current specifications (Recent folder)
- **Priority 2 (5%)**: Active documentation
- **Priority 3-4 (81%)**: Historical/archived content
- **Priority 5 (3%)**: Deprecated specs

Results automatically boost Priority 1 content.

### Temporal Boosting

2,060 chunks (77%) have accurate dates from Google Drive. Recent documents are ranked higher in temporal search.

## Available Scripts

### Compact Search (Recommended for Agents)
```bash
python scripts/search_compact.py "query"
```
- Minimal output (~200 tokens)
- Top 3 results
- Similarity scores + source links

### Interactive Search (For Humans)
```bash
python scripts/query_rag.py
```
- Full previews (200 chars)
- Interactive mode
- Detailed metadata

### Simple Test
```bash
python scripts/test_rag_simple.py
```
- Runs 3 predefined test queries
- Good for system verification

## Maintenance Scripts

### Re-chunk Documents
```bash
python scripts/chunk_documents.py
```
Splits documents into semantic chunks (run after editing specs).

### Re-generate Embeddings
```bash
python scripts/generate_embeddings.py
```
Creates new embeddings (run after chunking). Cost: ~$0.01.

### Reload Database
```bash
python scripts/load_to_supabase.py
```
Uploads chunks to Supabase (run after generating embeddings).

## Statistics

- **Documents**: 210 markdown files
- **Chunks**: 2,670 semantic chunks
- **Words**: 319,924 total
- **Avg chunk size**: 119.8 words (~160 tokens)
- **Database size**: 118.4 MB (chunks with embeddings)
- **Supabase usage**: 17 MB (well within free tier)

## Cost

- **One-time setup**: ~$0.01 (OpenAI embeddings)
- **Per query**: ~$0.0001 (negligible)
- **Supabase**: Free tier (500 MB limit)

## When to Rebuild

Rebuild the index when:
- Specifications are updated/added
- Documents are reorganized
- Priority classifications change

**Full rebuild process** (~2 minutes):
```bash
python scripts/chunk_documents.py
python scripts/generate_embeddings.py
python scripts/load_to_supabase.py
```

## Configuration

### Supabase
- URL: `https://rkjpqqafreeewttyisog.supabase.co`
- Schema: [scripts/setup_supabase_schema.sql](scripts/setup_supabase_schema.sql)
- Tables: `document_chunks`, `document_metadata`, `chunk_flags`, `document_quality`, `query_logs`

### OpenAI
- Model: `text-embedding-3-small` (1536 dimensions)
- Cost: $0.02 per 1M tokens
- API key: Set via `OPENAI_API_KEY` environment variable

## Advanced Features (Phase 4)

Not yet implemented but schema supports:

- **Content Flagging**: Mark bad/outdated chunks
- **Quality Scoring**: Track helpful vs unhelpful results
- **Query Logging**: Analytics on search patterns
- **Self-Correction**: Auto-suppress low-quality content

See [RAG_IMPLEMENTATION_PLAN.md](RAG_IMPLEMENTATION_PLAN.md) for details.

## Troubleshooting

### "No results found"
- Lower similarity threshold in search script
- Check if query is too specific
- Try broader terms

### "Connection error"
- Verify Supabase credentials
- Check internet connection
- Ensure database has data

### "OpenAI API error"
- Verify `OPENAI_API_KEY` environment variable
- Check API quota/billing

## For More Information

- **Navigation Guide**: [DATA-DUMP/NAVIGATION_GUIDE.md](DATA-DUMP/NAVIGATION_GUIDE.md)
- **Implementation Plan**: [RAG_IMPLEMENTATION_PLAN.md](RAG_IMPLEMENTATION_PLAN.md)
- **Project Status**: [PROJECT_STATUS.md](PROJECT_STATUS.md)
