#!/usr/bin/env python3
"""
Setup Supabase Schema
Runs the complete pgvector schema setup via Supabase Python client
"""

from supabase import create_client, Client
from pathlib import Path

# Supabase credentials
SUPABASE_URL = "https://rkjpqqafreeewttyisog.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJranBxcWFmcmVlZXd0dHlpc29nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI3OTM0MTksImV4cCI6MjA3ODM2OTQxOX0.lbTMoLIFCo8ADZfuROFs6sJJkJO5MN2Fvuyh1HzjN68"

def setup_schema():
    """Run the complete schema setup"""

    print("Connecting to Supabase...")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Read SQL schema
    sql_path = Path(__file__).parent / 'setup_supabase_schema.sql'
    print(f"Reading schema from: {sql_path}")

    with open(sql_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    print("\nExecuting schema setup...")
    print("This will create:")
    print("  - pgvector extension")
    print("  - 5 tables (document_chunks, document_metadata, chunk_flags, document_quality, query_logs)")
    print("  - Indexes (vector HNSW, full-text search, etc.)")
    print("  - 3 search functions (hybrid_search, temporal_search, status_search)")

    try:
        # Execute the SQL via RPC
        # Note: Supabase Python client doesn't have direct SQL execution
        # We need to use the REST API directly
        import httpx

        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

        # Supabase doesn't expose SQL execution through anon key for security
        # We need to use the SQL Editor in the dashboard
        print("\n[ERROR] Cannot execute SQL directly with anon key.")
        print("\nYou need to run the schema in Supabase SQL Editor:")
        print("1. Go to: https://supabase.com/dashboard/project/rkjpqqafreeewttyisog/sql/new")
        print("2. Copy the contents of: scripts/setup_supabase_schema.sql")
        print("3. Paste into the SQL Editor")
        print("4. Click 'Run' (or press Ctrl+Enter)")
        print("\nAlternatively, I can create a simpler setup using service_role key if you have it.")

        return False

    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        return False

if __name__ == "__main__":
    success = setup_schema()
    if success:
        print("\n[OK] Schema setup complete!")
    else:
        print("\n[FAIL] Schema setup requires manual SQL execution in Supabase dashboard")
