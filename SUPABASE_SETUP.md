# Supabase Setup for RAG System

This guide walks you through setting up Supabase with pgvector for the RAG system.

---

## Prerequisites

- Supabase account (free tier works fine)
- Project already in your proposed tech stack

---

## Setup Steps

### 1. Create/Access Supabase Project

If you don't have a Supabase project yet:

1. Go to: https://supabase.com/dashboard
2. Click "New Project"
3. Project name: "Open Systems RAG" (or use existing project)
4. Database password: (save this securely)
5. Region: Choose closest to you
6. Click "Create new project"

Wait ~2 minutes for provisioning.

### 2. Enable pgvector Extension

1. In Supabase dashboard, go to **Database** → **Extensions**
2. Search for `vector`
3. Enable the `vector` extension
4. This enables pgvector for similarity search

### 3. Run Schema Setup

1. In Supabase dashboard, go to **SQL Editor**
2. Click **"New query"**
3. Copy entire contents of `scripts/setup_supabase_schema.sql`
4. Paste into SQL editor
5. Click **"Run"**

This creates:
- `document_chunks` table (stores vectorized content)
- `document_metadata` table (file-level stats)
- `chunk_flags` table (quality tracking)
- `document_quality` table (quality scores)
- `query_logs` table (analytics)
- Indexes for fast queries
- Search functions (`hybrid_search`, `temporal_search`, `status_search`)

### 4. Verify Schema

Run this query in SQL Editor:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN (
    'document_chunks',
    'document_metadata',
    'chunk_flags',
    'document_quality',
    'query_logs'
  );
```

You should see all 5 tables listed.

### 5. Get API Credentials

1. In Supabase dashboard, go to **Settings** → **API**
2. Copy these values:

   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon/public key**: `eyJhbGc...` (long JWT token)

3. Create `.env` file in project root:

```bash
# Supabase credentials
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here

# OpenAI (for embeddings)
OPENAI_API_KEY=your-openai-key-here
```

4. Add `.env` to `.gitignore`:

```bash
echo ".env" >> .gitignore
```

### 6. Install Python Dependencies

```bash
pip install supabase openai python-dotenv
```

Or add to requirements.txt:

```
supabase>=2.0.0
openai>=1.0.0
python-dotenv>=1.0.0
```

### 7. Test Connection

Create `scripts/test_supabase.py`:

```python
#!/usr/bin/env python3
"""Test Supabase connection"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("[FAIL] Missing SUPABASE_URL or SUPABASE_KEY in .env")
    exit(1)

supabase = create_client(url, key)

# Test query
result = supabase.table('document_chunks').select("count", count='exact').execute()
print(f"[OK] Connected to Supabase")
print(f"  document_chunks count: {result.count}")

print("\nTables:")
tables = ['document_chunks', 'document_metadata', 'chunk_flags', 'document_quality', 'query_logs']
for table in tables:
    result = supabase.table(table).select("count", count='exact').execute()
    print(f"  {table}: {result.count} rows")
```

Run:
```bash
python scripts/test_supabase.py
```

Expected output:
```
[OK] Connected to Supabase
  document_chunks count: 0

Tables:
  document_chunks: 0 rows
  document_metadata: 0 rows
  chunk_flags: 0 rows
  document_quality: 0 rows
  query_logs: 0 rows
```

---

## Database Schema Overview

### Tables

1. **document_chunks**
   - Stores individual chunks of documents with embeddings
   - ~1000 chunks per large document (varies by chunk size)
   - Primary table for vector search

2. **document_metadata**
   - One row per file
   - Aggregated stats, topics, cross-references
   - Used for filtering and analytics

3. **chunk_flags** (Phase 4)
   - Tracks problematic content
   - Links to chunks that need attention

4. **document_quality** (Phase 4)
   - Quality scores per document
   - Auto-suppression for low-quality content

5. **query_logs** (Phase 4)
   - Tracks all queries and retrievals
   - User feedback collection
   - Analytics data

### Search Functions

1. **hybrid_search(embedding, text, count)**
   - Combines semantic similarity + keyword matching
   - Priority boosting (Priority 1 ranked higher)
   - Filters out flagged content

2. **temporal_search(embedding, text, count, recency_weight)**
   - Same as hybrid_search + recency boost
   - Newer documents ranked higher
   - Only for files with Google Drive dates

3. **status_search(embedding, status, count)**
   - Filter by status: 'current', 'historical', 'deprecated'
   - Use for "current specs only" queries

---

## Next Steps

After Supabase is set up:

1. **Create chunking script** to split documents
2. **Generate embeddings** with OpenAI
3. **Load data** into Supabase
4. **Test queries** to verify retrieval works

---

## Cost Estimates (Supabase Free Tier)

- **Database**: 500 MB included (plenty for this use case)
- **Bandwidth**: 5 GB/month included
- **Storage**: 1 GB included

**Estimated usage:**
- 210 documents × ~10 chunks each = ~2,100 chunks
- Each chunk: ~500 tokens × 4 bytes = ~2 KB
- Embeddings: 1536 floats × 4 bytes = ~6 KB per chunk
- Total: ~2,100 chunks × 8 KB = **~17 MB**

Free tier is more than sufficient.

---

## Troubleshooting

### "Extension vector not found"
- Go to Database → Extensions
- Search "vector"
- Enable it
- Re-run schema SQL

### "Permission denied"
- Ensure you're running SQL as project owner
- Check API key is anon/public key (not service_role)

### "Table already exists"
- Schema was already created
- Use `DROP TABLE` if you want to start fresh
- Or skip to step 5 (Get API Credentials)

---

*Estimated setup time: 10-15 minutes*
