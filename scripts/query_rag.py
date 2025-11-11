#!/usr/bin/env python3
"""
Query RAG System
Test the hybrid search functionality
"""

import os
from supabase import create_client, Client
from openai import OpenAI
from typing import List, Dict

# Credentials
SUPABASE_URL = "https://rkjpqqafreeewttyisog.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJranBxcWFmcmVlZXd0dHlpc29nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI3OTM0MTksImV4cCI6MjA3ODM2OTQxOX0.lbTMoLIFCo8ADZfuROFs6sJJkJO5MN2Fvuyh1HzjN68"

# Initialize clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_query_embedding(query: str) -> List[float]:
    """Generate embedding for search query"""
    response = openai_client.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def hybrid_search(query: str, match_count: int = 5, similarity_threshold: float = 0.5) -> List[Dict]:
    """
    Perform hybrid search (semantic + keyword)
    """
    print(f"\nSearching for: '{query}'")
    print(f"Generating query embedding...")

    # Generate embedding
    query_embedding = generate_query_embedding(query)

    print(f"Searching database (top {match_count} results)...")

    # Call hybrid_search function
    result = supabase.rpc(
        'hybrid_search',
        {
            'query_embedding': query_embedding,
            'query_text': query,
            'match_count': match_count,
            'similarity_threshold': similarity_threshold
        }
    ).execute()

    return result.data

def temporal_search(query: str, match_count: int = 5) -> List[Dict]:
    """
    Perform temporal search (prioritizes recent documents)
    """
    print(f"\nTemporal search for: '{query}'")
    print(f"Generating query embedding...")

    # Generate embedding
    query_embedding = generate_query_embedding(query)

    print(f"Searching with temporal boosting...")

    # Call temporal_search function
    result = supabase.rpc(
        'temporal_search',
        {
            'query_embedding': query_embedding,
            'query_text': query,
            'match_count': match_count,
            'recency_weight': 0.3
        }
    ).execute()

    return result.data

def display_results(results: List[Dict], search_type: str = "Hybrid"):
    """Display search results"""

    if not results:
        print("\n[WARNING] No results found")
        return

    print(f"\n=== {search_type} Search Results ===\n")

    for i, result in enumerate(results, 1):
        print(f"{i}. [{result['file_title']}]")
        print(f"   File: {result['file_path']}")
        print(f"   Section: {result.get('heading_path', 'N/A')}")
        print(f"   Priority: {result['priority']} | Status: {result['status']}")

        if 'similarity' in result:
            print(f"   Similarity: {result['similarity']:.3f}", end='')
        if 'rank' in result:
            print(f" | Rank: {result['rank']:.3f}", end='')
        if 'temporal_score' in result:
            print(f" | Temporal Score: {result['temporal_score']:.3f}", end='')

        print(f"\n   Modified: {result.get('date_modified', 'Unknown')}")

        # Show content preview
        content = result['content']
        preview = content[:200] + "..." if len(content) > 200 else content
        # Handle Unicode for Windows console
        safe_preview = preview.encode('ascii', 'replace').decode('ascii')
        print(f"\n   {safe_preview}\n")

def main():
    """Run test queries"""

    print("=" * 80)
    print("Open Systems RAG - Query Test")
    print("=" * 80)

    # Test queries
    test_queries = [
        "How does governance work in Open Systems?",
        "What are the smart contract requirements?",
        "Explain the milestone funding process",
        "What is the voting mechanism?"
    ]

    print("\nRunning test queries...")

    for query in test_queries:
        try:
            # Hybrid search
            results = hybrid_search(query, match_count=3, similarity_threshold=0.3)
            display_results(results, search_type="Hybrid")

            print("\n" + "-" * 80 + "\n")

        except Exception as e:
            print(f"[ERROR] Query failed: {e}")
            import traceback
            traceback.print_exc()

    # Interactive mode
    print("\n" + "=" * 80)
    print("Interactive Mode (type 'exit' to quit)")
    print("=" * 80)

    while True:
        query = input("\nEnter your query: ").strip()

        if query.lower() in ['exit', 'quit', 'q']:
            print("Goodbye!")
            break

        if not query:
            continue

        try:
            results = hybrid_search(query, match_count=5, similarity_threshold=0.3)
            display_results(results, search_type="Hybrid")

        except Exception as e:
            print(f"[ERROR] Query failed: {e}")

if __name__ == "__main__":
    main()
