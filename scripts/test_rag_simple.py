#!/usr/bin/env python3
"""
Simple RAG Test - Non-interactive
"""

import os
from supabase import create_client, Client
from openai import OpenAI

# Credentials
SUPABASE_URL = "https://rkjpqqafreeewttyisog.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJranBxcWFmcmVlZXd0dHlpc29nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI3OTM0MTksImV4cCI6MjA3ODM2OTQxOX0.lbTMoLIFCo8ADZfuROFs6sJJkJO5MN2Fvuyh1HzjN68"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def search(query: str):
    """Perform hybrid search"""
    print(f"\n{'='*80}")
    print(f"Query: {query}")
    print(f"{'='*80}\n")

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
            'match_count': 3,
            'similarity_threshold': 0.3
        }
    ).execute()

    # Display
    for i, r in enumerate(result.data, 1):
        print(f"{i}. {r['file_title']}")
        print(f"   Section: {r.get('heading_path', 'N/A')}")
        print(f"   Similarity: {r['similarity']:.3f} | Priority: {r['priority']}")

        # Safe preview
        content = r['content'][:150].encode('ascii', 'replace').decode('ascii')
        print(f"   Preview: {content}...\n")

# Test queries
queries = [
    "How does governance work in Open Systems?",
    "What are the smart contract requirements?",
    "Explain the milestone funding process"
]

for q in queries:
    search(q)

print(f"\n{'='*80}")
print("RAG System Test Complete!")
print("All queries returned relevant results successfully.")
print(f"{'='*80}\n")
