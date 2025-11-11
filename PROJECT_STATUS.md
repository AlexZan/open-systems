# Open Systems RAG Project - Current Status

**Last Updated:** 2025-01-10
**Status:** Phase 1 (Foundation) - In Progress

---

## What We've Accomplished

### ✅ Completed Tasks

1. **Document Conversion** (DONE)
   - Converted 181 DOCX files to Markdown using Pandoc
   - Original DOCX files deleted (backed up on Google Drive)
   - All documents now in agent-friendly format

2. **Navigation Guide** (DONE)
   - Created [DATA-DUMP/NAVIGATION_GUIDE.md](DATA-DUMP/NAVIGATION_GUIDE.md)
   - Comprehensive guide for AI agents to navigate 500+ pages
   - Priority classification system (1-5)
   - Quick reference mappings

3. **Google Drive Metadata Sync** (DONE)
   - Set up OAuth authentication for Google Drive API
   - Created [scripts/setup_gdrive_auth.py](scripts/setup_gdrive_auth.py)
   - Created [scripts/sync_gdrive_metadata.py](scripts/sync_gdrive_metadata.py)
   - **Result:** [gdrive_metadata.json](gdrive_metadata.json) with accurate dates for 162 files
   - Critical: Filesystem dates are all 2025-01-10 (conversion date)
   - Google Drive has real creation/modification dates (2022-2024)

4. **Document Indexing** (DONE)
   - Created [scripts/index_documents.py](scripts/index_documents.py)
   - Indexed 210 markdown documents
   - Extracted metadata: headings, topics, cross-references, word counts
   - **Result:** [document_index.json](document_index.json)
   - Statistics:
     - Priority 1 (current): 25 docs
     - Priority 2 (intro/published): 4 docs
     - Priority 3 (technical/theory): 93 docs
     - Priority 4 (thoughts): 82 docs
     - Priority 5 (deprecated): 6 docs
   - Most referenced: "Open Systems Smart Contracts" (3 refs)

5. **Supabase Schema** (READY)
   - Created [scripts/setup_supabase_schema.sql](scripts/setup_supabase_schema.sql)
   - Created [SUPABASE_SETUP.md](SUPABASE_SETUP.md) with instructions
   - Schema includes:
     - 5 tables (document_chunks, document_metadata, chunk_flags, document_quality, query_logs)
     - pgvector indexes for similarity search
     - Full-text search indexes
     - 3 search functions (hybrid, temporal, status-based)
   - **Action Required:** User needs to run SQL in Supabase dashboard

---

## 📋 Next Steps (In Order)

### Immediate: Supabase Setup

**User must do this before we can continue:**

1. Go to https://supabase.com/dashboard
2. Create/select project for "Open Systems RAG"
3. Go to **SQL Editor**
4. Copy contents of [scripts/setup_supabase_schema.sql](scripts/setup_supabase_schema.sql)
5. Paste and run in SQL Editor
6. Go to **Settings** → **API**
7. Copy Project URL and anon/public key
8. Create `.env` file in project root:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key
   OPENAI_API_KEY=your-openai-key
   ```
9. Run: `pip install supabase openai python-dotenv`

Full instructions in [SUPABASE_SETUP.md](SUPABASE_SETUP.md).

### Phase 1 Remaining Tasks

Once Supabase is set up:

1. **Create Chunking Script** (scripts/chunk_documents.py)
   - Load document_index.json
   - Split each document into semantic chunks
   - Strategy:
     - Chunk by heading hierarchy (preserve context)
     - Target ~500 tokens per chunk
     - Max 1000 tokens (OpenAI limit: 8191)
     - Overlap: 50 tokens between chunks
   - Output: chunks.json with ~2,100 chunks

2. **Generate Embeddings** (scripts/generate_embeddings.py)
   - Use OpenAI text-embedding-3-small (1536 dimensions)
   - Process chunks in batches of 100
   - Add embeddings to chunks.json
   - Estimated cost: ~$0.05 (2,100 chunks × ~500 tokens)

3. **Load into Supabase** (scripts/load_to_supabase.py)
   - Upload chunks to document_chunks table
   - Upload file metadata to document_metadata table
   - Verify vector indexes are working
   - Test search functions

4. **Test Retrieval** (scripts/test_rag.py)
   - Sample queries: "what is open systems?", "how do projects work?"
   - Verify results are relevant
   - Check temporal boosting (recent docs ranked higher)
   - Validate priority system

---

## 📂 Key Files Created

### Documentation
- [DATA-DUMP/NAVIGATION_GUIDE.md](DATA-DUMP/NAVIGATION_GUIDE.md) - AI agent navigation guide
- [RAG_IMPLEMENTATION_PLAN.md](RAG_IMPLEMENTATION_PLAN.md) - 5-phase implementation plan
- [GDRIVE_SETUP.md](GDRIVE_SETUP.md) - Google Drive OAuth setup guide
- [SUPABASE_SETUP.md](SUPABASE_SETUP.md) - Supabase database setup guide
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - This file (current status)

### Scripts (Python)
- [scripts/convert_docx.py](scripts/convert_docx.py) - DOCX to MD converter (completed)
- [scripts/setup_gdrive_auth.py](scripts/setup_gdrive_auth.py) - Google Drive OAuth
- [scripts/sync_gdrive_metadata.py](scripts/sync_gdrive_metadata.py) - Fetch accurate dates
- [scripts/index_documents.py](scripts/index_documents.py) - Extract document metadata
- [scripts/setup_supabase_schema.sql](scripts/setup_supabase_schema.sql) - Database schema

### Data Files
- [gdrive_metadata.json](gdrive_metadata.json) - 162 files with accurate dates from Google Drive
- [document_index.json](document_index.json) - 210 documents with metadata, topics, cross-refs
- `.gdrive_token.pickle` - Google Drive OAuth token (do not commit)
- `credentials.json` - Google Drive API credentials (do not commit)

### Configuration
- [requirements-gdrive.txt](requirements-gdrive.txt) - Google Drive API dependencies
- `.env` - Supabase/OpenAI credentials (TO BE CREATED by user)

---

## 🗂️ Project Statistics

### Documents
- **Total markdown files:** 210
- **With Google Drive dates:** 162 (77%)
- **Without (filesystem dates):** 48 (23%)
- **Total word count:** ~500,000 words (estimated)
- **Average file size:** ~2,400 words

### Priority Distribution
| Priority | Count | Description |
|----------|-------|-------------|
| 1 | 25 | Current specifications (2023-2024) |
| 2 | 4 | Introduction, Published docs |
| 3 | 93 | Technical, Theory, Applications |
| 4 | 82 | Thoughts, exploratory |
| 5 | 6 | Deprecated |

### Status Distribution
| Status | Count | Description |
|--------|-------|-------------|
| current | 29 | Active specifications |
| historical | 164 | Older but valid |
| deprecated | 6 | Superseded |
| unknown | 11 | Unclassified |

### Cross-References
- **Total documents with incoming refs:** 17
- **Most referenced:** Open Systems Smart Contracts (3), Spec→Implementation System (3)

---

## 🎯 Project Goals

### Primary Objective
Make the Open Systems project **agent-human ready** by:
1. Converting all documentation to agent-friendly format (Markdown) ✅
2. Building a RAG system for efficient knowledge retrieval 🔄
3. Enabling AI agents to answer questions about the project
4. Supporting agents in implementation tasks

### RAG System Features

**Phase 1 (Current):** Foundation
- Vector database with semantic search
- Temporal ranking (recent docs ranked higher)
- Priority-based filtering
- Full-text + semantic hybrid search

**Phase 2 (Future):** Query Intelligence
- Query routing (definition vs implementation queries)
- Smart retrieval strategies
- Context-aware responses

**Phase 3 (Future):** Advanced Features
- Reranking with Cohere
- Cross-reference graph navigation
- Concept evolution tracking

**Phase 4 (Future):** Quality & Feedback
- Content flagging system
- Quality scoring
- Self-correcting based on user feedback

**Phase 5 (Future):** Optimization
- Caching layer
- Incremental updates
- Performance tuning

---

## 💾 Database Schema (Supabase)

### Tables

1. **document_chunks**
   - Stores vectorized chunks of documents
   - ~2,100 rows expected (210 docs × ~10 chunks each)
   - Columns: id, file_path, file_title, chunk_index, content, embedding (vector), priority, status, dates, word_count, references, quality_score, etc.

2. **document_metadata**
   - One row per file (210 rows)
   - Aggregated stats: word count, topics, cross-references
   - Used for filtering and analytics

3. **chunk_flags** (Phase 4)
   - Tracks problematic content
   - User can flag bad/outdated chunks

4. **document_quality** (Phase 4)
   - Quality scores per document (0.0-1.0)
   - Auto-suppression for score < 0.3

5. **query_logs** (Phase 4)
   - Tracks queries and retrievals
   - User feedback collection

### Search Functions

1. **hybrid_search(embedding, text, count)**
   - Semantic similarity (70%) + keyword matching (30%)
   - Priority boosting
   - Filters flagged content

2. **temporal_search(embedding, text, count, recency_weight)**
   - Hybrid search + recency boost
   - Recent docs ranked higher
   - Uses Google Drive dates

3. **status_search(embedding, status, count)**
   - Filter by status ('current', 'historical', 'deprecated')

---

## 🔧 Technical Details

### Chunking Strategy
- **Method:** Semantic chunking by heading hierarchy
- **Target size:** 500 tokens (~375 words)
- **Max size:** 1000 tokens (OpenAI limit: 8191)
- **Overlap:** 50 tokens between chunks
- **Preserve:** Heading context in each chunk

### Embedding Model
- **Model:** OpenAI text-embedding-3-small
- **Dimensions:** 1536
- **Cost:** $0.02 per 1M tokens
- **Expected cost:** ~$0.05 for entire corpus

### Vector Search
- **Index type:** HNSW (Hierarchical Navigable Small World)
- **Distance metric:** Cosine similarity
- **Parameters:** m=16, ef_construction=64
- **Expected query time:** <50ms for 2,100 chunks

---

## 🚨 Important Notes

### Do Not Commit
Add to `.gitignore`:
```
.env
credentials.json
.gdrive_token.pickle
gdrive_metadata.json
document_index.json
```

### Google Drive Dates Are Critical
- All MD files created 2025-01-10 (conversion date)
- Filesystem dates are useless for temporal ranking
- **Must use Google Drive dates** for accurate recency
- 162/210 files (77%) have accurate dates

### Priority System
Based on folder location:
- `Recent/From Open Systems Project in ChatGpt/` → Priority 1
- `Recent/` → Priority 1
- `Published/` → Priority 2
- `Technical/`, `Theory/`, `Applications/` → Priority 3
- `Thoughts/` → Priority 4
- `Depricated/` → Priority 5

### Token Estimates
All estimates use **tokens**, not time:
- Phase 1: ~30K tokens
- Phase 2: ~40K tokens
- Phase 3: ~50K tokens
- Phase 4: ~40K tokens
- Phase 5: ~30K tokens
- **Total:** ~190K tokens

---

## 📞 Contact & Resources

### Documentation References
- [RAG_IMPLEMENTATION_PLAN.md](RAG_IMPLEMENTATION_PLAN.md) - Full 5-phase plan
- [SUPABASE_SETUP.md](SUPABASE_SETUP.md) - Database setup instructions
- [GDRIVE_SETUP.md](GDRIVE_SETUP.md) - Google Drive OAuth guide
- [DATA-DUMP/NAVIGATION_GUIDE.md](DATA-DUMP/NAVIGATION_GUIDE.md) - Content navigation

### External Links
- Supabase Dashboard: https://supabase.com/dashboard
- Google Cloud Console: https://console.cloud.google.com/
- OpenAI API: https://platform.openai.com/api-keys

---

## 🎬 Quick Start for Next Session

**If Supabase is already set up:**
1. Verify `.env` file exists with SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY
2. Continue with: "Create the chunking script"

**If Supabase is NOT set up:**
1. Follow [SUPABASE_SETUP.md](SUPABASE_SETUP.md)
2. Create `.env` file
3. Test connection: `python scripts/test_supabase.py`
4. Then continue with chunking script

**Current Phase:** Phase 1 (Foundation) - 60% complete
**Next Step:** Create chunking script to split documents into embeddable chunks

---

*This is a living document. Update as project progresses.*
