#!/usr/bin/env python3
"""
Generate Embeddings for Document Chunks
Uses OpenAI text-embedding-3-small to create 1536-dimensional vectors
"""

import json
import os
from pathlib import Path
from openai import OpenAI
from typing import List
import time

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_embeddings_batch(texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    """
    Generate embeddings for a batch of texts
    OpenAI allows up to 2048 texts per batch
    """
    try:
        response = client.embeddings.create(
            input=texts,
            model=model
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        print(f"[ERROR] Failed to generate embeddings: {e}")
        raise

def main():
    """Generate embeddings for all chunks"""

    project_root = Path(__file__).parent.parent
    chunks_path = project_root / 'document_chunks.json'
    output_path = project_root / 'document_chunks_with_embeddings.json'

    print("Loading document chunks...")
    with open(chunks_path, 'r', encoding='utf-8') as f:
        chunks = json.load(f)

    print(f"Found {len(chunks)} chunks")

    # Check for existing embeddings
    if output_path.exists():
        print(f"\n[WARNING] Output file already exists: {output_path}")
        response = input("Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Aborted")
            return

    # Extract texts
    texts = [chunk['content'] for chunk in chunks]

    # Batch size (OpenAI allows up to 2048, but we'll use 100 for safety and progress tracking)
    batch_size = 100
    total_batches = (len(texts) + batch_size - 1) // batch_size

    print(f"\nGenerating embeddings...")
    print(f"  Model: text-embedding-3-small (1536 dimensions)")
    print(f"  Batches: {total_batches} x {batch_size} texts")
    print(f"  Estimated cost: ~$0.01 (${0.02 / 1_000_000 * len(' '.join(texts).split())} for ~{len(' '.join(texts).split())} words)")

    all_embeddings = []
    start_time = time.time()

    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        batch_num = (i // batch_size) + 1

        try:
            print(f"  Batch {batch_num}/{total_batches} ({len(batch_texts)} chunks)...", end=' ', flush=True)
            embeddings = generate_embeddings_batch(batch_texts)
            all_embeddings.extend(embeddings)
            print("[OK]")

        except Exception as e:
            print(f"[FAIL]")
            print(f"\n[ERROR] Failed at batch {batch_num}: {e}")
            print("Saving progress so far...")

            # Save partial results
            for j, chunk in enumerate(chunks[:len(all_embeddings)]):
                chunk['embedding'] = all_embeddings[j]

            partial_path = project_root / 'document_chunks_with_embeddings_partial.json'
            with open(partial_path, 'w', encoding='utf-8') as f:
                json.dump(chunks[:len(all_embeddings)], f, indent=2)

            print(f"Partial results saved to: {partial_path}")
            return

        # Rate limiting (optional, OpenAI has generous limits)
        time.sleep(0.1)

    elapsed = time.time() - start_time

    print(f"\n[OK] Generated {len(all_embeddings)} embeddings in {elapsed:.1f}s")

    # Add embeddings to chunks
    print("Adding embeddings to chunks...")
    for i, chunk in enumerate(chunks):
        chunk['embedding'] = all_embeddings[i]

    # Save with embeddings
    print(f"Saving to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2)

    # Statistics
    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"\n[OK] Complete!")
    print(f"  File size: {file_size_mb:.1f} MB")
    print(f"  Ready to load into Supabase")

if __name__ == "__main__":
    main()
