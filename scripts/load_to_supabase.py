#!/usr/bin/env python3
"""
Load Document Chunks into Supabase
Uploads chunks with embeddings to Supabase pgvector database
"""

import json
from pathlib import Path
from supabase import create_client, Client
from typing import List, Dict
import time

# Supabase credentials
SUPABASE_URL = "https://rkjpqqafreeewttyisog.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJranBxcWFmcmVlZXd0dHlpc29nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI3OTM0MTksImV4cCI6MjA3ODM2OTQxOX0.lbTMoLIFCo8ADZfuROFs6sJJkJO5MN2Fvuyh1HzjN68"

def load_chunks_batch(supabase: Client, chunks: List[Dict], batch_size: int = 100):
    """
    Load chunks in batches to avoid rate limits
    """
    total_batches = (len(chunks) + batch_size - 1) // batch_size

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        batch_num = (i // batch_size) + 1

        try:
            print(f"  Batch {batch_num}/{total_batches} ({len(batch)} chunks)...", end=' ', flush=True)

            # Insert batch
            result = supabase.table('document_chunks').insert(batch).execute()

            print("[OK]")

        except Exception as e:
            print(f"[FAIL]")
            print(f"\n[ERROR] Failed at batch {batch_num}: {e}")

            # Try inserting one by one to identify problematic chunk
            print("Attempting individual inserts to identify issue...")
            for j, chunk in enumerate(batch):
                try:
                    supabase.table('document_chunks').insert(chunk).execute()
                except Exception as chunk_error:
                    print(f"[ERROR] Failed chunk {i+j}: {chunk['file_path']}:{chunk['chunk_index']}")
                    print(f"  Error: {chunk_error}")
                    raise

        # Rate limiting
        time.sleep(0.1)

def load_metadata(supabase: Client, metadata: List[Dict]):
    """
    Load document metadata
    """
    print(f"\nLoading document metadata ({len(metadata)} documents)...")

    try:
        result = supabase.table('document_metadata').insert(metadata).execute()
        print(f"[OK] Loaded {len(metadata)} document metadata records")
    except Exception as e:
        print(f"[FAIL] Error loading metadata: {e}")
        raise

def main():
    """Load all data into Supabase"""

    project_root = Path(__file__).parent.parent
    chunks_path = project_root / 'document_chunks_with_embeddings.json'
    index_path = project_root / 'document_index.json'

    print("Connecting to Supabase...")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("[OK] Connected")

    # Load chunks
    print(f"\nLoading chunks from: {chunks_path}")
    with open(chunks_path, 'r', encoding='utf-8') as f:
        chunks = json.load(f)

    print(f"Found {len(chunks)} chunks")

    # Load document metadata
    print(f"\nLoading document index from: {index_path}")
    with open(index_path, 'r', encoding='utf-8') as f:
        document_index = json.load(f)

    print(f"Found {len(document_index)} documents")

    # Prepare metadata for insertion
    metadata_records = []
    for doc in document_index:
        metadata_record = {
            'file_path': doc['file_path'],
            'title': doc['title'],
            'date_created': doc['date_created'],
            'date_modified': doc['date_modified'],
            'has_gdrive_dates': doc['has_gdrive_dates'],
            'priority': doc['priority'],
            'status': doc['status'],
            'word_count': doc['word_count'],
            'line_count': doc['line_count'],
            'chunk_count': len([c for c in chunks if c['file_path'] == doc['file_path']]),
            'heading_count': doc['heading_count'],
            'topics': doc.get('topics', []),
            'cross_references': doc.get('cross_references', []),
            'referenced_by': [],  # Will be computed later
            'reference_count': len(doc.get('cross_references', []))
        }
        metadata_records.append(metadata_record)

    # Check if data already exists
    try:
        existing = supabase.table('document_chunks').select('id', count='exact').limit(1).execute()
        if existing.count and existing.count > 0:
            print(f"\n[WARNING] Database already contains {existing.count} chunks")
            response = input("Clear existing data and reload? (y/n): ")
            if response.lower() == 'y':
                print("Clearing existing data...")
                supabase.table('document_chunks').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
                supabase.table('document_metadata').delete().neq('file_path', '__nonexistent__').execute()
                print("[OK] Cleared")
            else:
                print("Aborted")
                return
    except Exception as e:
        print(f"[INFO] No existing data found (this is fine for first load)")

    # Load metadata first
    load_metadata(supabase, metadata_records)

    # Load chunks
    print(f"\nLoading {len(chunks)} chunks into Supabase...")
    start_time = time.time()

    load_chunks_batch(supabase, chunks, batch_size=100)

    elapsed = time.time() - start_time

    print(f"\n[OK] Loaded {len(chunks)} chunks in {elapsed:.1f}s")

    # Verify
    print("\nVerifying data...")
    try:
        chunk_count = supabase.table('document_chunks').select('id', count='exact').limit(1).execute()
        metadata_count = supabase.table('document_metadata').select('file_path', count='exact').limit(1).execute()

        print(f"  Chunks in database: {chunk_count.count}")
        print(f"  Metadata in database: {metadata_count.count}")

        if chunk_count.count == len(chunks) and metadata_count.count == len(metadata_records):
            print("\n[OK] All data loaded successfully!")
            print("\nYour RAG system is ready!")
            print(f"  - {len(chunks)} searchable chunks")
            print(f"  - {len(metadata_records)} documents indexed")
            print(f"  - Hybrid search (semantic + keyword) enabled")
            print(f"  - Temporal boosting enabled for {sum(1 for c in chunks if c['has_gdrive_dates'])} chunks with accurate dates")
        else:
            print("\n[WARNING] Data counts don't match. Check for errors above.")

    except Exception as e:
        print(f"[ERROR] Verification failed: {e}")

if __name__ == "__main__":
    main()
