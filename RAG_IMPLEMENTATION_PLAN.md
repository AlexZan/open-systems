# RAG Implementation Plan for Open Systems

This document outlines the strategy for implementing Retrieval-Augmented Generation (RAG) for the Open Systems documentation corpus (500+ pages, 181 markdown files).

---

## Executive Summary

**Goal**: Enable AI agents to efficiently navigate, understand, and reason about Open Systems documentation with awareness of temporal evolution and document priority.

**Key Challenge**: Documents span 2018-2024 with evolving concepts, deprecated ideas, and multiple levels of detail. RAG must understand recency, priority, and conceptual relationships.

**Approach**: Multi-layered hybrid RAG with temporal awareness, metadata filtering, and hierarchical retrieval.

---

## Architecture Overview

```
Query → Router → Retrieval Strategy → Rerank → Context Assembly → LLM
         ↓
    [Metadata Filter]
    [Temporal Boost]
    [Priority Weighting]
```

### Core Components

1. **Document Processor** - Extracts metadata, chunks documents
2. **Vector Store** - Supabase pgvector (already in stack)
3. **Query Router** - Classifies query type and selects strategy
4. **Hybrid Retriever** - Combines semantic + keyword + graph
5. **Reranker** - Applies temporal/priority boosting
6. **Context Assembler** - Builds optimal context window

---

## Phase 1: Foundation - RECOMMENDED START

### 1.1 Document Metadata Extraction

Create `scripts/index_documents.py` that scans all markdown files and extracts:

```python
{
  "file_path": "DATA-DUMP/Recent/From Open Systems Project in ChatGpt/open_projects_spec_v_1.md",
  "title": "Open Projects Specification v1",
  "status": "current",           # current | historical | deprecated
  "priority": 1,                  # 1 (highest) - 5 (lowest)
  "date_created": "2023-11-15",   # Extract from git or file metadata
  "date_modified": "2024-01-05",
  "category": "specification",    # spec | theory | technical | use-case | thought | plan
  "folder": "Recent",             # Recent | Open Systems Shared | etc
  "subfolder": "From Open Systems Project in ChatGpt",
  "topics": ["projects", "goals", "milestones", "crowdfunding", "voting"],
  "related_files": [],            # Cross-references found in document
  "word_count": 8500,
  "heading_structure": ["Overview", "Core Concepts", ...],
  "has_acceptance_criteria": true,
  "mentioned_in_nav_guide": true
}
```

**Priority Assignment Rules:**
- Priority 1: `Recent/From Open Systems Project in ChatGpt/*.md`
- Priority 2: `Open Systems Shared/Introduction to Open Democracy and Open Systems.md`
- Priority 2: `Open Systems Shared/Publish/*.md`
- Priority 3: `Open Systems Shared/Technical/*.md`, `Theory/*.md`
- Priority 4: `Open Systems Shared/Thoughts/*.md`
- Priority 5: `Open Systems Shared/Depricated/*.md`

**Status Assignment Rules:**
- "current": Files in `Recent/`
- "deprecated": Files in `Depricated/`
- "historical": Everything else in `Open Systems Shared/`

### 1.2 Semantic Chunking Strategy

**Chunk by Markdown Sections:**
```python
# Each heading (##, ###) becomes a chunk boundary
# Preserve parent heading context in chunk metadata

Example chunk:
{
  "content": "## Voting Mechanics\n\nExperience is consumed when voting...",
  "file_path": "...",
  "heading_path": "Core Concepts > Voting Mechanics",  # Breadcrumb
  "chunk_index": 3,
  "heading_level": 2,
  "parent_headings": ["Core Concepts"],
  "chunk_tokens": 650,
  **metadata from file**
}
```

**Chunk Size:**
- Target: 500-800 tokens per chunk
- Max: 1200 tokens
- Include overlap: 100 tokens from previous/next chunk

**Special Handling:**
- Code blocks: Keep intact, don't split
- Lists: Keep complete lists together
- Tables: Keep entire table in one chunk

### 1.3 Vector Embeddings

**Embedding Model:**
- **Primary**: OpenAI `text-embedding-3-small` (1536 dimensions, cheaper)
- **Alternative**: `text-embedding-3-large` (3072 dimensions, better quality)
- **Open-source fallback**: `bge-large-en-v1.5`

**Embedding Strategy:**
```python
# Embed enriched content with context
embedding_text = f"""
Title: {file_title}
Section: {heading_path}
Category: {category}
Status: {status}

{chunk_content}
"""
```

### 1.4 Vector Store Setup (Supabase)

**Schema:**
```sql
CREATE TABLE document_chunks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  file_path TEXT NOT NULL,
  file_title TEXT NOT NULL,
  chunk_index INTEGER NOT NULL,
  content TEXT NOT NULL,
  heading_path TEXT,
  heading_level INTEGER,

  -- Metadata
  status TEXT NOT NULL,  -- current | historical | deprecated
  priority INTEGER NOT NULL,
  category TEXT NOT NULL,
  folder TEXT NOT NULL,
  date_created DATE,
  date_modified DATE,
  topics TEXT[],

  -- Embedding
  embedding vector(1536),

  -- Search optimization
  tokens INTEGER,
  word_count INTEGER,

  created_at TIMESTAMP DEFAULT NOW(),

  UNIQUE(file_path, chunk_index)
);

-- Indexes
CREATE INDEX ON document_chunks USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX ON document_chunks (status, priority);
CREATE INDEX ON document_chunks (category);
CREATE INDEX ON document_chunks USING GIN (topics);
CREATE INDEX ON document_chunks (file_path);
```

**Hybrid Search Function:**
```sql
CREATE FUNCTION hybrid_search(
  query_embedding vector(1536),
  query_text TEXT,
  match_count INT DEFAULT 10,
  status_filter TEXT[] DEFAULT ARRAY['current', 'historical'],
  max_priority INT DEFAULT 3
)
RETURNS TABLE (
  file_path TEXT,
  content TEXT,
  heading_path TEXT,
  similarity FLOAT,
  priority INT,
  status TEXT,
  category TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    dc.file_path,
    dc.content,
    dc.heading_path,
    1 - (dc.embedding <=> query_embedding) AS similarity,
    dc.priority,
    dc.status,
    dc.category
  FROM document_chunks dc
  WHERE
    dc.status = ANY(status_filter)
    AND dc.priority <= max_priority
    AND (
      dc.embedding <=> query_embedding < 0.5  -- Semantic similarity
      OR dc.content ILIKE '%' || query_text || '%'  -- Keyword match
    )
  ORDER BY
    -- Boost by recency and priority
    (1 - (dc.embedding <=> query_embedding)) * (1 / dc.priority::FLOAT) DESC
  LIMIT match_count;
END;
$$;
```

---

## Phase 2: Query Intelligence

### 2.1 Query Classification

**Query Router:**
```python
class QueryRouter:
    PATTERNS = {
        "definition": ["what is", "define", "explain"],
        "how_to": ["how does", "how do", "how to", "process for"],
        "why": ["why", "rationale", "reason"],
        "example": ["example", "use case", "show me"],
        "technical": ["implementation", "code", "architecture", "contract"],
        "comparison": ["vs", "versus", "difference between", "compare"],
        "historical": ["evolution", "history", "how did", "originally"],
        "current": ["latest", "current", "now", "v1", "spec"]
    }

    def classify(self, query: str) -> dict:
        """
        Returns:
        {
            "query_type": "definition" | "how_to" | "why" | ...,
            "focus": "current" | "historical" | "comprehensive",
            "suggested_categories": ["spec", "theory"],
            "suggested_files": ["open_projects_spec_v_1.md"],
            "max_priority": 2
        }
        """
```

**Routing Rules:**

| Query Type | Priority Filter | Status Filter | Categories | Example |
|------------|----------------|---------------|------------|---------|
| definition | 1-2 | current | spec, theory | "What is experience?" |
| how_to | 1-2 | current | spec, technical | "How does voting work?" |
| why | 2-3 | current, historical | theory, thought | "Why experience-based?" |
| example | 2-3 | current, historical | use-case | "Show me project examples" |
| technical | 1-3 | current | spec, technical | "Smart contract architecture" |
| comparison | 2-4 | historical | theory, thought | "Open Systems vs DAOs" |
| historical | 3-5 | historical, deprecated | all | "How did voting evolve?" |
| current | 1-2 | current | spec | "Latest project spec" |

### 2.2 Multi-Strategy Retrieval

**Strategy 1: Direct File Routing**
```python
# For queries matching known patterns, route directly to files
FILE_ROUTES = {
    "what is open systems": "Introduction to Open Democracy and Open Systems.md",
    "project spec": "open_projects_spec_v_1.md",
    "smart contracts": "open_systems_smart_contracts.md",
    "ai collaboration": "ai_collab_protocol.md",
    "spec to code": "spec_impl_system_v_1.md",
}
```

**Strategy 2: Hierarchical Retrieval**
```python
# Step 1: Search NAVIGATION_GUIDE.md to identify relevant folders
# Step 2: Filter search to those folders
# Step 3: Retrieve specific chunks

Example:
Query: "How does auditing work?"
→ Search nav guide: "auditing" → Points to Introduction doc + Thoughts/
→ Search filtered to those paths
→ Return relevant chunks
```

**Strategy 3: Cross-Reference Graph**
```python
# Build graph during indexing:
# "open_projects_spec_v_1.md" references:
#   - open_goals_and_tasks_system_v_1.md
#   - open_systems_smart_contracts.md
#   - Introduction to Open Democracy...

# On retrieval:
# 1. Find primary doc
# 2. Include referenced docs for context
# 3. Trace concept evolution through related files
```

**Strategy 4: Concept Evolution Tracking**
```python
# For historical queries, trace concept through time:
# "voting" →
#   Depricated/Early DeDem docs (2018)
#   → Thoughts/Thoughts on Voting.md (2020)
#   → Technical/Consensus and Voting Technical.md (2021)
#   → Recent/open_projects_spec_v_1.md (2023)
```

### 2.3 Temporal Boosting

**Recency Scoring:**
```python
def temporal_boost(similarity: float, priority: int, date_modified: date) -> float:
    """
    Boost scores based on recency and priority
    """
    # Base similarity: 0.0 - 1.0

    # Priority boost: 1-5 → 2.0x - 1.0x multiplier
    priority_multiplier = 2.0 - (priority - 1) * 0.25

    # Recency boost: More recent = higher
    days_old = (datetime.now().date() - date_modified).days
    if days_old < 180:  # Last 6 months
        recency_multiplier = 1.5
    elif days_old < 365:  # Last year
        recency_multiplier = 1.2
    elif days_old < 730:  # Last 2 years
        recency_multiplier = 1.0
    else:
        recency_multiplier = 0.8

    return similarity * priority_multiplier * recency_multiplier
```

---

## Phase 3: Advanced Features

### 3.1 Reranking with Cohere

After initial retrieval, rerank results considering:
- Query-document relevance
- Document authority (priority)
- Document recency
- Cross-reference importance

```python
from cohere import Client

def rerank_results(query: str, results: list, top_k: int = 5) -> list:
    """
    Use Cohere rerank to refine results
    """
    co = Client(api_key=COHERE_KEY)

    documents = [r['content'] for r in results]

    reranked = co.rerank(
        model="rerank-english-v3.0",
        query=query,
        documents=documents,
        top_n=top_k
    )

    # Combine rerank score with our temporal boosting
    return merge_scores(reranked, results)
```

### 3.2 Context Assembly

**Smart Context Building:**
```python
def build_context(query: str, retrieved_chunks: list, max_tokens: int = 8000) -> str:
    """
    Assemble optimal context for LLM
    """
    context = []

    # 1. Add navigation primer (if needed)
    if needs_navigation(query):
        context.append(load_nav_guide_summary())

    # 2. Add primary chunks (highest ranked)
    context.extend(retrieved_chunks[:5])

    # 3. Add cross-referenced content
    for chunk in retrieved_chunks[:3]:
        refs = get_cross_references(chunk['file_path'])
        context.extend(load_referenced_chunks(refs, limit=2))

    # 4. Add historical context (if historical query)
    if is_historical_query(query):
        context.extend(get_evolution_timeline(extract_concept(query)))

    # 5. Deduplicate and format
    context = deduplicate_chunks(context)

    # 6. Trim to token limit
    return format_context(context, max_tokens)
```

**Context Format:**
```markdown
# Retrieved Context for: [Query]

## Primary Sources (Most Relevant)

### [File 1 Title] (Priority: 1, Status: current, Updated: 2023-11-15)
**Section:** Core Concepts > Voting
[Content...]

### [File 2 Title] (Priority: 2, Status: current, Updated: 2023-10-20)
**Section:** Implementation > Smart Contracts
[Content...]

## Related Context

### [File 3 Title] (Priority: 3, Status: historical, Updated: 2021-05-10)
**Section:** Background > Voting Evolution
[Content...]

## Cross-References
- See also: open_systems_smart_contracts.md, Section 3.2
- Historical context: Thoughts/Thoughts on Voting.md
```

### 3.3 Feedback Loop

**Track retrieval quality:**
```python
# Log every query + retrieval + user feedback
{
  "query": "How does milestone voting work?",
  "query_type": "how_to",
  "retrieved_files": ["open_projects_spec_v_1.md", ...],
  "chunks_used": [3, 7, 12],
  "user_feedback": "helpful" | "not_helpful",
  "timestamp": "2024-01-10T10:30:00Z"
}

# Periodically analyze:
# - Which files are most useful for which query types?
# - Are priority weights accurate?
# - Should chunk sizes change?
```

---

## Phase 4: Content Quality & Feedback

### 4.1 Provenance Tracking

**Always include source citations in retrieved context:**

```python
def format_retrieval_result(chunks: list) -> str:
    """Format chunks with full provenance"""
    context = []

    for i, chunk in enumerate(chunks, 1):
        context.append(f"""
### Source {i}: {chunk['file_title']}
**Location:** {chunk['file_path']}
**Section:** {chunk['heading_path']}
**Status:** {chunk['status'].upper()} (Priority {chunk['priority']})
**Last Updated:** {chunk['date_modified']}
{f"**⚠️ Warning:** {chunk['status_warning']}" if chunk['status'] != 'current' else ""}

{chunk['content']}
        """)

    return "\n\n".join(context)
```

**Result:** Every piece of information can be traced back to its source document.

### 4.2 Content Flagging System

**Database Schema Addition:**

```sql
-- Add to document_chunks table
ALTER TABLE document_chunks ADD COLUMN flagged BOOLEAN DEFAULT FALSE;
ALTER TABLE document_chunks ADD COLUMN flag_reason TEXT;
ALTER TABLE document_chunks ADD COLUMN flag_date TIMESTAMP;
ALTER TABLE document_chunks ADD COLUMN quality_score FLOAT DEFAULT 1.0;

-- Track flagged chunks
CREATE TABLE chunk_flags (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  chunk_id UUID REFERENCES document_chunks(id),
  file_path TEXT NOT NULL,
  chunk_index INTEGER NOT NULL,
  reason TEXT NOT NULL,
  flagged_by TEXT,
  flagged_date TIMESTAMP DEFAULT NOW(),
  resolution TEXT,  -- "suppressed" | "fixed" | "reviewed"
  resolved_date TIMESTAMP
);

-- Document quality tracking
CREATE TABLE document_quality (
  file_path TEXT PRIMARY KEY,
  times_retrieved INTEGER DEFAULT 0,
  times_flagged INTEGER DEFAULT 0,
  helpful_count INTEGER DEFAULT 0,
  unhelpful_count INTEGER DEFAULT 0,
  quality_score FLOAT DEFAULT 1.0,
  suppressed BOOLEAN DEFAULT FALSE,
  last_updated TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX ON chunk_flags (file_path);
CREATE INDEX ON chunk_flags (resolution);
CREATE INDEX ON document_quality (quality_score);
```

**Flag Content Function:**

```python
def flag_chunk(
    file_path: str,
    chunk_id: str,
    reason: str,
    flagged_by: str = "user"
) -> None:
    """Flag a chunk as problematic"""

    # Mark chunk as flagged
    supabase.table('document_chunks').update({
        'flagged': True,
        'flag_reason': reason,
        'flag_date': datetime.now()
    }).eq('id', chunk_id).execute()

    # Record in flags table
    supabase.table('chunk_flags').insert({
        'chunk_id': chunk_id,
        'file_path': file_path,
        'reason': reason,
        'flagged_by': flagged_by
    }).execute()

    # Update document quality score
    update_document_quality(file_path)
```

**Update Quality Score:**

```python
def update_document_quality(file_path: str) -> None:
    """Recalculate document quality based on flags and feedback"""

    # Get stats
    stats = supabase.table('document_chunks')\
        .select('flagged, chunk_id')\
        .eq('file_path', file_path)\
        .execute()

    total_chunks = len(stats.data)
    flagged_chunks = sum(1 for c in stats.data if c['flagged'])

    # Get feedback stats
    feedback = supabase.table('query_logs')\
        .select('user_feedback')\
        .contains('retrieved_files', [file_path])\
        .execute()

    helpful = sum(1 for f in feedback.data if f['user_feedback'] == 'helpful')
    unhelpful = sum(1 for f in feedback.data if f['user_feedback'] == 'not_helpful')

    # Calculate quality score (0.0 - 1.0)
    if total_chunks > 0:
        flag_penalty = flagged_chunks / total_chunks
        feedback_score = helpful / (helpful + unhelpful) if (helpful + unhelpful) > 0 else 0.5
        quality_score = (1.0 - flag_penalty) * feedback_score
    else:
        quality_score = 0.5

    # Update database
    supabase.table('document_quality').upsert({
        'file_path': file_path,
        'times_flagged': flagged_chunks,
        'helpful_count': helpful,
        'unhelpful_count': unhelpful,
        'quality_score': quality_score,
        'suppressed': quality_score < 0.3,  # Auto-suppress very low quality
        'last_updated': datetime.now()
    }).execute()
```

### 4.3 Retrieval Filtering

**Filter flagged content during search:**

```python
def hybrid_search_with_quality_filter(
    query_embedding: list,
    query_text: str,
    match_count: int = 10,
    include_flagged: bool = False,  # Default: exclude flagged
    min_quality_score: float = 0.5   # Default: exclude low quality
) -> list:
    """Search with quality filtering"""

    # Base search
    results = supabase.rpc('hybrid_search', {
        'query_embedding': query_embedding,
        'query_text': query_text,
        'match_count': match_count * 2  # Get more, will filter
    }).execute()

    # Apply quality filters
    filtered = []
    for result in results.data:
        # Skip flagged chunks
        if not include_flagged and result['flagged']:
            continue

        # Check document quality
        doc_quality = get_document_quality(result['file_path'])
        if doc_quality['suppressed'] and not include_flagged:
            continue
        if doc_quality['quality_score'] < min_quality_score:
            continue

        # Apply quality boost to ranking
        result['boosted_score'] = result['similarity'] * doc_quality['quality_score']
        filtered.append(result)

    # Re-sort by boosted score and return top k
    filtered.sort(key=lambda x: x['boosted_score'], reverse=True)
    return filtered[:match_count]
```

### 4.4 Feedback Collection

**Query Logging:**

```python
# Log every query and retrieval
CREATE TABLE query_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  query_text TEXT NOT NULL,
  query_type TEXT,  -- From query router
  retrieved_files TEXT[],
  retrieved_chunks UUID[],
  user_feedback TEXT,  -- "helpful" | "not_helpful" | "bad_info"
  feedback_note TEXT,
  timestamp TIMESTAMP DEFAULT NOW()
);

def log_query(
    query: str,
    query_type: str,
    retrieved_chunks: list,
    user_feedback: str = None,
    feedback_note: str = None
) -> None:
    """Log query for analysis"""

    supabase.table('query_logs').insert({
        'query_text': query,
        'query_type': query_type,
        'retrieved_files': [c['file_path'] for c in retrieved_chunks],
        'retrieved_chunks': [c['id'] for c in retrieved_chunks],
        'user_feedback': user_feedback,
        'feedback_note': feedback_note
    }).execute()
```

### 4.5 CLI Tools

**Flag Content Script (`scripts/flag_content.py`):**

```python
#!/usr/bin/env python3
"""
Interactive tool to flag problematic content
Usage: python scripts/flag_content.py
"""

import sys
from supabase import create_client

def flag_content_interactive():
    """Interactive flagging workflow"""

    print("\n=== Content Flagging Tool ===\n")

    # Recent queries for context
    recent = get_recent_queries(limit=5)
    print("Recent queries:")
    for i, q in enumerate(recent, 1):
        print(f"{i}. {q['query_text']}")
        print(f"   Sources: {', '.join(q['retrieved_files'][:3])}")

    print("\n")

    # Get file to flag
    file_path = input("File path with bad info: ").strip()
    if not file_path:
        print("Cancelled.")
        return

    # Get specific content or flag entire file
    print("\nOptions:")
    print("1. Flag specific content (chunk)")
    print("2. Downgrade entire file priority")
    print("3. Mark entire file as deprecated")
    choice = input("Choice (1-3): ").strip()

    reason = input("Reason: ").strip()

    if choice == "1":
        # Show chunks from file
        chunks = get_file_chunks(file_path)
        print(f"\nFound {len(chunks)} chunks. Search for content:")
        search = input("Search term: ").strip()
        matching = [c for c in chunks if search.lower() in c['content'].lower()]

        for i, c in enumerate(matching[:5], 1):
            print(f"\n{i}. {c['heading_path']}")
            print(f"   {c['content'][:200]}...")

        chunk_num = int(input("\nWhich chunk? (1-5): ")) - 1
        chunk_id = matching[chunk_num]['id']

        flag_chunk(file_path, chunk_id, reason)
        print(f"✓ Chunk flagged and suppressed from search")

    elif choice == "2":
        downgrade_file_priority(file_path, reason)
        print(f"✓ File priority downgraded")

    elif choice == "3":
        mark_file_deprecated(file_path, reason)
        superseded_by = input("Superseded by which file? (optional): ").strip()
        if superseded_by:
            add_superseded_link(file_path, superseded_by)
        print(f"✓ File marked deprecated")

if __name__ == "__main__":
    flag_content_interactive()
```

**Quality Dashboard (`scripts/quality_report.py`):**

```python
#!/usr/bin/env python3
"""
Generate document quality report
Usage: python scripts/quality_report.py
"""

def generate_quality_report():
    """Show document quality metrics"""

    print("\n=== Document Quality Report ===\n")

    # Low quality documents
    low_quality = supabase.table('document_quality')\
        .select('*')\
        .lt('quality_score', 0.6)\
        .order('quality_score', desc=False)\
        .execute()

    if low_quality.data:
        print("⚠️  Low Quality Documents (Score < 0.6):\n")
        for doc in low_quality.data:
            print(f"  {doc['file_path']}")
            print(f"    Quality Score: {doc['quality_score']:.2f}")
            print(f"    Flagged Chunks: {doc['times_flagged']}")
            print(f"    Retrieved: {doc['times_retrieved']} times")
            print(f"    Feedback: {doc['helpful_count']} helpful, {doc['unhelpful_count']} unhelpful")
            print(f"    Status: {'SUPPRESSED' if doc['suppressed'] else 'Active'}")
            print()

    # High quality documents
    high_quality = supabase.table('document_quality')\
        .select('*')\
        .gt('quality_score', 0.9)\
        .gt('times_retrieved', 10)\
        .order('quality_score', desc=True)\
        .limit(10)\
        .execute()

    print("✓ High Quality Documents (Score > 0.9, Used >10 times):\n")
    for doc in high_quality.data:
        print(f"  {doc['file_path']}")
        print(f"    Quality Score: {doc['quality_score']:.2f}")
        print(f"    Retrieved: {doc['times_retrieved']} times")
        print()

    # Flagged chunks summary
    flags = supabase.table('chunk_flags')\
        .select('*')\
        .is_('resolution', None)\
        .execute()

    print(f"🚩 Unresolved Flags: {len(flags.data)}\n")

    # Group by file
    from collections import defaultdict
    by_file = defaultdict(list)
    for flag in flags.data:
        by_file[flag['file_path']].append(flag)

    for file_path, file_flags in sorted(by_file.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {file_path} ({len(file_flags)} flags)")
        for flag in file_flags[:3]:
            print(f"    - {flag['reason']}")
        if len(file_flags) > 3:
            print(f"    ... and {len(file_flags) - 3} more")
        print()

if __name__ == "__main__":
    generate_quality_report()
```

### 4.6 Self-Correcting Workflow

**Normal Operation:**
1. User asks question
2. RAG retrieves relevant chunks (filters out flagged content)
3. Response includes source citations
4. User provides feedback (optional)

**When Bad Info Detected:**
1. User notices incorrect/outdated info in response
2. Checks citation to identify source file/chunk
3. Runs `python scripts/flag_content.py`
4. Flags the problematic chunk with reason
5. Chunk immediately suppressed from future searches
6. Document quality score updated

**Periodic Review:**
1. Run `python scripts/quality_report.py`
2. Review low quality files (score < 0.6)
3. Decide: fix, deprecate, or remove
4. Update metadata and links
5. Re-index if needed

---

## Phase 5: Optimization

### 5.1 Caching Layer

**Cache common queries:**
```python
# Redis cache for frequent queries
CACHE = {
    "what is open systems": {
        "context": [...],
        "files": [...],
        "ttl": 86400  # 24 hours
    }
}
```

### 4.2 Incremental Updates

**Don't reindex everything on document updates:**
```python
# Watch for file changes
# Only re-embed changed chunks
# Update metadata without re-embedding if only metadata changed
```

### 4.3 Query Expansion

**Expand queries with synonyms/related terms:**
```python
CONCEPT_MAP = {
    "experience": ["voting power", "influence", "reputation"],
    "bounty": ["reward", "incentive", "prize"],
    "project": ["initiative", "venture", "crowdfund"],
    "goal": ["milestone", "objective", "target"]
}

def expand_query(query: str) -> str:
    # Add related terms to improve recall
    pass
```

---

## Implementation Roadmap

### Phase 1: Foundation
- [x] Convert DOCX to MD (DONE)
- [x] Create NAVIGATION_GUIDE (DONE)
- [ ] Build `scripts/index_documents.py`
  - Extract metadata from all markdown files
  - Generate topics from content
  - Detect cross-references
  - Export to JSON
- [ ] Set up Supabase pgvector schema
- [ ] Create chunking script
- [ ] Generate embeddings for all chunks
- [ ] Load into Supabase

**Deliverable:** Searchable vector database with metadata

### Phase 2: Query Intelligence
- [ ] Build query router
- [ ] Implement routing rules
- [ ] Create hybrid search function
- [ ] Add temporal boosting
- [ ] Test with sample queries

**Deliverable:** Smart retrieval system

### Phase 3: Advanced Features
- [ ] Integrate Cohere reranking
- [ ] Build context assembler
- [ ] Implement cross-reference graph
- [ ] Add concept evolution tracking

**Deliverable:** Advanced RAG system

### Phase 4: Content Quality & Feedback
- [ ] Implement provenance tracking in responses
- [ ] Add content flagging database schema
- [ ] Build flag_chunk and quality scoring functions
- [ ] Create retrieval filtering with quality checks
- [ ] Implement query logging
- [ ] Build CLI tools (flag_content.py, quality_report.py)
- [ ] Test self-correcting workflow

**Deliverable:** Self-correcting, traceable RAG system

### Phase 5: Optimization
- [ ] Add Redis caching
- [ ] Implement incremental updates
- [ ] Add query expansion
- [ ] Performance tuning
- [ ] Documentation

**Deliverable:** Production-ready, maintainable system

---

## Technology Stack

### Required Services
- **Vector DB**: Supabase (pgvector) - Already in stack ✅
- **Embeddings**: OpenAI API (text-embedding-3-small)
- **Reranking** (optional): Cohere API
- **Cache** (optional): Redis

### Python Dependencies
```txt
openai>=1.0.0
supabase>=2.0.0
tiktoken>=0.5.0
cohere>=4.0.0  # Optional
redis>=5.0.0  # Optional
pydantic>=2.0.0
python-dotenv>=1.0.0
```

### Cost Estimates (Monthly)

**Indexing (One-time):**
- 181 files × ~5,000 tokens avg = ~900,000 tokens
- Chunks: ~2,000 chunks × 600 tokens avg = 1.2M tokens
- Embeddings: 1.2M tokens × $0.02/1M = $0.024

**Query (Ongoing):**
- 1,000 queries/month × 10 chunks × 600 tokens = 6M tokens
- Embeddings: 6M × $0.02/1M = $0.12/month
- Reranking (optional): 1,000 queries × $0.002 = $2/month

**Total: ~$2-3/month for moderate usage**

---

## Evaluation Metrics

### Retrieval Quality
- **Precision@5**: Are top 5 results relevant?
- **Recall@10**: Are all relevant docs in top 10?
- **MRR (Mean Reciprocal Rank)**: How quickly do we find the right doc?

### Temporal Accuracy
- **Current vs Historical**: Are current docs prioritized for current queries?
- **Evolution Tracking**: Can we trace concept evolution?

### User Satisfaction
- **Helpful Rate**: % of queries marked helpful
- **File Coverage**: Are all important files being retrieved?
- **Query Resolution**: Did user find their answer?

---

## Testing Strategy

### Test Queries (Must Handle Well)

**Definition Queries:**
- "What is Open Systems?"
- "Define experience in Open Systems"
- "What are bounties?"

**How-To Queries:**
- "How does milestone voting work?"
- "How do projects get funded?"
- "How is experience earned?"

**Technical Queries:**
- "Smart contract architecture"
- "Blockchain implementation details"
- "API endpoints for projects"

**Comparison Queries:**
- "Open Systems vs DAOs"
- "Bounties vs Projects vs Goals"

**Historical Queries:**
- "How has voting evolved?"
- "Why was DeDem renamed to Open Systems?"
- "Original thinking on experience"

**Complex Queries:**
- "Show me the complete workflow from project creation to funding release"
- "What are all the ways to earn experience?"

### Success Criteria
- 90%+ of definition queries return Introduction doc
- 85%+ of how-to queries return current specs
- 80%+ of technical queries return Technical/ docs
- 75%+ of historical queries include Thoughts/ or Depricated/

---

## Next Steps

**Immediate (This Week):**
1. Set up Supabase pgvector schema
2. Create document indexing script
3. Generate metadata for all files
4. Create first embeddings batch

**Short-term (Next 2 Weeks):**
1. Build query router
2. Implement hybrid search
3. Test with sample queries
4. Iterate on retrieval quality

**Medium-term (Month 2):**
1. Add reranking
2. Implement cross-reference graph
3. Build context assembler
4. Launch beta for internal use

---

## Appendix A: Sample Queries & Expected Results

### Query: "What is Open Systems?"
**Expected Files:**
1. Introduction to Open Democracy and Open Systems.md (Priority 2)
2. open_systems_conclusions.md (Priority 1)
3. Theory/Open Systems.md (Priority 3)

### Query: "How do milestones work in projects?"
**Expected Files:**
1. open_projects_spec_v_1.md (Priority 1)
2. open_goals_and_tasks_system_v_1.md (Priority 1)
3. Use Cases/Project examples (Priority 3)

### Query: "Why is voting experience-based instead of token-based?"
**Expected Files:**
1. Introduction to Open Democracy... (Priority 2) - "Equal Opportunity to Power"
2. Theory/The need for open systems... (Priority 3)
3. Thoughts/Thoughts on Token Voting.md (Priority 4)

### Query: "Smart contract architecture for failover"
**Expected Files:**
1. open_systems_smart_contracts.md (Priority 1)
2. Technical/Open Systems Technical.md (Priority 3)

---

## Appendix B: Metadata Extraction Script Skeleton

```python
import os
import re
from pathlib import Path
from datetime import datetime
import git  # GitPython for commit dates

def extract_metadata(file_path: Path) -> dict:
    """Extract metadata from a markdown file"""

    # Read content
    content = file_path.read_text(encoding='utf-8')

    # Extract title (first # heading or filename)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else file_path.stem

    # Determine status and priority based on path
    path_str = str(file_path)
    if 'Recent/' in path_str:
        status = 'current'
        priority = 1
    elif 'Depricated/' in path_str:
        status = 'deprecated'
        priority = 5
    else:
        status = 'historical'
        priority = 3 if 'Publish/' in path_str else 4

    # Extract topics from headings and content
    headings = re.findall(r'^#{2,}\s+(.+)$', content, re.MULTILINE)
    topics = extract_topics(content, headings)

    # Get dates from git
    repo = git.Repo(search_parent_directories=True)
    commits = list(repo.iter_commits(paths=file_path, max_count=1))
    date_created = commits[-1].committed_datetime if commits else None
    date_modified = commits[0].committed_datetime if commits else None

    # Extract cross-references
    related_files = re.findall(r'\[.*?\]\((.*?\.md)\)', content)

    return {
        'file_path': str(file_path.relative_to(Path.cwd())),
        'title': title,
        'status': status,
        'priority': priority,
        'category': determine_category(path_str, title, content),
        'folder': file_path.parts[-3] if len(file_path.parts) > 2 else '',
        'subfolder': file_path.parts[-2] if len(file_path.parts) > 1 else '',
        'topics': topics,
        'related_files': related_files,
        'word_count': len(content.split()),
        'heading_structure': headings,
        'has_acceptance_criteria': 'AC-' in content,
        'date_created': date_created,
        'date_modified': date_modified or datetime.now()
    }
```

---

*This RAG implementation plan is designed specifically for the Open Systems documentation corpus. Update as the system evolves.*
