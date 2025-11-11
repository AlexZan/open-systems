# Agent-Ready Documentation System

## Overview

The Open Systems project is now fully **agent-human ready** with an intelligent semantic search system optimized for AI agent usage. This document explains how agents efficiently navigate 500+ pages of documentation with minimal context overhead.

## The Problem We Solved

**Challenge**: 210 documents (500+ pages) of Open Systems specifications are too large for agents to keep in context.

**Traditional Approach Issues**:
- Loading full documents: 1000+ tokens per document
- Naive search: Returns generic results for broad queries
- Context bloat: Search iterations consume main agent's context window

**Our Solution**: Semantic RAG with dedicated search agent and query optimization.

## System Architecture

### 1. Document Processing Pipeline

```
DOCX files (181)
  ↓ [Pandoc conversion]
Markdown files (210)
  ↓ [Semantic chunking]
2,670 chunks (~120 words each)
  ↓ [OpenAI embeddings]
1536-dimensional vectors
  ↓ [Load to Supabase]
Searchable vector database
```

### 2. Search Components

**Database**: Supabase pgvector
- 2,670 document chunks with embeddings
- 210 document metadata records
- HNSW vector index for fast similarity search
- Full-text search index for keyword matching

**Search Functions**:
- `hybrid_search()`: 70% semantic + 30% keyword
- `temporal_search()`: Prioritizes recent documents
- `status_search()`: Filters by status (current/historical/deprecated)

**Priority System**:
- Priority 1 (11%): Current specifications
- Priority 2 (5%): Active documentation
- Priority 3-4 (81%): Historical/archived content
- Priority 5 (3%): Deprecated specs

### 3. Doc-Search Agent

**Location**: [.claude/agents/doc-search.md](.claude/agents/doc-search.md)

**Purpose**: Specialized agent with isolated context window that optimizes RAG queries and iteratively refines them.

**Key Features**:
- **Own context window**: Search iterations don't bloat main conversation
- **Query optimization**: Converts broad questions into specific searches
- **Self-correcting**: Evaluates results and refines if needed
- **Efficient output**: Returns only top 3 results (~300 tokens)

## How Agents Use The System

### Invocation Pattern

```
Main Agent
  ↓ (detects need for Open Systems info)
Task tool → doc-search agent
  ↓ (in separate context)
  1. Receive question: "How is experience gained in Open Systems?"
  2. Optimize query: "earn experience points upvotes contributions"
  3. Run search (similarity: 0.65)
  4. Evaluate results
  5. Refine if needed (max 3 iterations)
  6. Return top 3 results
  ↓
Main Agent receives clean results (~300 tokens)
```

### Example Usage

**Agent needs information**:
```
Task(
  subagent_type="doc-search",
  prompt="How is voting experience gained?"
)
```

**Doc-search agent (in its own context)**:
- Optimizes: "voting experience gained" → "experience points upvotes contribution tokens"
- Searches vector database
- Evaluates: Top result 0.65 similarity ✓
- Returns: 3 results with sources

**Main agent receives**:
```
Found 3 relevant results:

1. Open Game System Spec (similarity: 0.65)
   Covers: Contributors earn experience points proportional to upvotes
   Source: DATA-DUMP/Recent/.../open_game_system_spec.md

2. Open Ventures User Flow (similarity: 0.54)
   Covers: Stake tokens grant voting power
   Source: DATA-DUMP/Recent/.../open_ventures_user_flow.md

3. Open Systems Projects Summary (similarity: 0.48)
   Covers: Non-transferable voting tokens
   Source: DATA-DUMP/Recent/.../open_systems_projects_summary.md
```

**Context cost**: ~300 tokens (vs 1000+ for manual search)

## Query Optimization Strategy

### How Vector Search Works

**User query** → **Embedding model** → **Vector** (1536 numbers)
- Semantic: "experience gained" matches "earn points" (different words, same concept)
- Cosine similarity: Measures how "close" vectors are in concept space

### Why Query Optimization Matters

**Broad query problem**:
```
"How is experience gained in Open Systems?"
↓ Embedding dominated by "open systems"
→ Returns: General Open Systems overview docs (similarity: 0.44)
```

**Optimized query**:
```
"earn experience points upvotes contributions"
↓ Embedding focused on specific mechanism
→ Returns: Technical docs about experience mechanics (similarity: 0.65)
```

### Optimization Patterns

**Remove filler words**:
- ❌ "how", "what", "in open systems"
- ✓ Focus on nouns and verbs

**Use specific terms**:
- ❌ "how things work"
- ✓ "mechanism", "process", "flow"

**Add related concepts**:
- ❌ "voting"
- ✓ "voting quorum threshold percentage"

**Use technical vocabulary**:
- ❌ "community takeover"
- ✓ "failover mechanism"

### Doc-Search Agent Learns These Patterns

The agent has domain knowledge about Open Systems concepts and automatically applies optimization patterns:

- Governance → voting, quorum, proposals, democracy
- Smart contracts → Project, Goal, Token, Proof, Voting contracts
- Funding → milestones, crowdfunding, stake tokens
- Experience → contribution rewards, voting power
- Failover → community takeover, inactive owners

## Context Efficiency

### Token Usage Breakdown

**Traditional approach** (without doc-search agent):
```
1. Agent searches: python scripts/search_compact.py "query" (~50 tokens)
2. Results returned: 3 × 200 tokens = 600 tokens
3. Agent refines: python scripts/search_compact.py "refined" (~50 tokens)
4. Results returned: 3 × 200 tokens = 600 tokens
Total: 1,300 tokens (for 2 iterations)
```

**With doc-search agent**:
```
1. Invoke agent: Task tool (~100 tokens)
2. Agent optimizes and searches (in own context, doesn't count)
3. Agent returns results: ~300 tokens
Total: 400 tokens (70% savings)
```

**Efficiency gain**: ~70% reduction in context usage

### Scalability

**Per agent session**:
- Average queries: 3-5
- Token cost: 400 × 5 = 2,000 tokens
- vs. Traditional: 1,300 × 5 = 6,500 tokens
- **Savings: 4,500 tokens per session**

**90% agent usage** (target):
- Most queries optimized automatically
- Main agent context stays clean
- Human users can also benefit (10% usage)

## Direct Script Usage (Alternative)

For situations where the doc-search agent isn't available or for human users:

### Compact Search
```bash
python scripts/search_compact.py "governance voting mechanism"
```

Output (~200 tokens):
```
1. Document Title (similarity: 0.XX)
   Section: Heading path
   Summary: First meaningful sentence...
   Source: file/path.md
```

### Full Search (Humans)
```bash
python scripts/query_rag.py
```

Interactive mode with detailed previews.

## Maintenance

### When to Rebuild Index

Rebuild when:
- Specifications are updated/added
- Documents are reorganized
- Priority classifications change

### Rebuild Process (~2 minutes)

```bash
# 1. Re-chunk documents (splits into semantic chunks)
python scripts/chunk_documents.py

# 2. Generate embeddings (OpenAI API, ~$0.01)
python scripts/generate_embeddings.py

# 3. Load to Supabase (uploads to database)
python scripts/load_to_supabase.py
```

### Costs

**One-time setup**: ~$0.01 (OpenAI embeddings)
**Per query**: ~$0.0001 (negligible)
**Supabase**: Free tier (17 MB / 500 MB limit)

**Total ongoing cost**: Essentially free

## Architecture Benefits

### For AI Agents

✅ **Minimal context**: ~300 tokens per search (vs 1000+)
✅ **High accuracy**: Query optimization improves relevance
✅ **Self-correcting**: Iterates until good results found
✅ **Fast**: Sub-second search across 500+ pages
✅ **Sourced**: Every result has file path for follow-up

### For Humans

✅ **Semantic search**: Finds concepts, not just keywords
✅ **Priority boosting**: Current specs ranked higher
✅ **Temporal awareness**: Recent docs prioritized
✅ **Quality tracking**: Future phase supports flagging bad content

### For the Project

✅ **Scalable**: Works with 10x more documents
✅ **Maintainable**: Simple rebuild process
✅ **Version controlled**: Agent config in `.claude/agents/`
✅ **Team sharable**: Commit agent to git

## System Statistics

**Documents**: 210 markdown files
**Chunks**: 2,670 semantic chunks
**Words**: 319,924 total
**Avg chunk**: 119.8 words (~160 tokens)
**Database**: 118.4 MB (chunks with embeddings)
**Supabase usage**: 17 MB (3.4% of free tier)
**Embedding dimensions**: 1536 (OpenAI text-embedding-3-small)

**Search performance**:
- Query time: <500ms
- Similarity threshold: 0.3 (adjustable)
- Top results: 3 (configurable)
- Context footprint: ~300 tokens

## Files and Locations

### Core Components

**Doc-Search Agent**:
- [.claude/agents/doc-search.md](.claude/agents/doc-search.md)

**Search Scripts**:
- [scripts/search_compact.py](scripts/search_compact.py) - Minimal output
- [scripts/query_rag.py](scripts/query_rag.py) - Interactive search
- [scripts/test_rag_simple.py](scripts/test_rag_simple.py) - System verification

**Processing Pipeline**:
- [scripts/chunk_documents.py](scripts/chunk_documents.py) - Document chunking
- [scripts/generate_embeddings.py](scripts/generate_embeddings.py) - Embedding generation
- [scripts/load_to_supabase.py](scripts/load_to_supabase.py) - Database loading

**Database Schema**:
- [scripts/setup_supabase_schema.sql](scripts/setup_supabase_schema.sql)

### Documentation

- [RAG_SYSTEM_GUIDE.md](RAG_SYSTEM_GUIDE.md) - Complete usage guide
- [RAG_IMPLEMENTATION_PLAN.md](RAG_IMPLEMENTATION_PLAN.md) - Implementation roadmap
- [CLAUDE.md](CLAUDE.md) - Project instructions for agents
- [DATA-DUMP/NAVIGATION_GUIDE.md](DATA-DUMP/NAVIGATION_GUIDE.md) - Folder structure guide

### Generated Data

- `document_index.json` - Metadata for all documents
- `document_chunks.json` - Chunks without embeddings
- `document_chunks_with_embeddings.json` - Chunks with vectors (118 MB)
- `gdrive_metadata.json` - Accurate file dates from Google Drive

## Future Enhancements (Phase 4)

The system is designed for self-improvement:

**Content Quality Tracking**:
- Flag bad/outdated chunks
- Track helpful vs unhelpful results
- Auto-suppress low-quality content

**Query Analytics**:
- Log search patterns
- Identify documentation gaps
- Optimize based on usage

**Advanced Search**:
- Multi-query fusion
- Re-ranking models
- Contextual boosting

See [RAG_IMPLEMENTATION_PLAN.md](RAG_IMPLEMENTATION_PLAN.md) for details.

## Success Metrics

**Goal**: Make Open Systems documentation accessible to agents with minimal context overhead

**Results**:
✅ 70% reduction in context usage per search
✅ 0.6+ similarity scores on specific queries (vs 0.4 before)
✅ Sub-second search across 500+ pages
✅ Isolated context for search iterations
✅ Self-correcting query optimization

**The Open Systems project is now fully agent-human ready.**
