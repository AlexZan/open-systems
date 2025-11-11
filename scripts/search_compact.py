#!/usr/bin/env python3
"""
Compact RAG Search - Minimal context footprint for agents
Usage: python search_compact.py "your query here"
"""

import sys
import os
from supabase import create_client, Client
from openai import OpenAI

# Credentials
SUPABASE_URL = "https://rkjpqqafreeewttyisog.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJranBxcWFmcmVlZXd0dHlpc29nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI3OTM0MTksImV4cCI6MjA3ODM2OTQxOX0.lbTMoLIFCo8ADZfuROFs6sJJkJO5MN2Fvuyh1HzjN68"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def search(query: str, top_k: int = 3):
    """Compact search with minimal output"""

    # Generate embedding
    response = openai_client.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    )
    embedding = response.data[0].embedding

    # Search
    result = supabase.rpc(
        'hybrid_search',
        {
            'query_embedding': embedding,
            'query_text': query,
            'match_count': top_k,
            'similarity_threshold': 0.3
        }
    ).execute()

    if not result.data:
        print("No results found")
        return

    # Compact output format
    for i, r in enumerate(result.data, 1):
        # Title and similarity
        print(f"{i}. {r['file_title']} (similarity: {r['similarity']:.2f})")

        # Section if available
        if r.get('heading_path'):
            heading = r['heading_path'].encode('ascii', 'replace').decode('ascii')
            print(f"   Section: {heading}")

        # One-line summary (first meaningful sentence or 150 chars)
        content = r['content'].replace('\n', ' ').replace('#', '').strip()
        # Get first sentence up to 150 chars, skip very short ones
        sentences = content.split('.')
        summary = None
        for sent in sentences:
            sent = sent.strip()
            if len(sent) > 20:  # Skip headings/short fragments
                summary = sent[:150]
                break
        if not summary:
            summary = content[:150]
        summary = summary.encode('ascii', 'replace').decode('ascii')
        print(f"   {summary}...")

        # Source with line reference (for easy file opening)
        file_path = r['file_path']
        print(f"   Source: {file_path}")
        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search_compact.py \"your query\"")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    search(query, top_k=3)
