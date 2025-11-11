#!/usr/bin/env python3
"""
Chunk Documents for RAG
Splits markdown documents into semantic chunks suitable for embedding
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime

def split_by_headings(content: str, file_path: Path) -> List[Tuple[str, str, str]]:
    """
    Split document by headings, keeping context hierarchy
    Returns: [(chunk_text, heading_path, chunk_type)]
    """
    chunks = []

    # Split by markdown headings
    lines = content.split('\n')
    current_chunk = []
    heading_stack = []  # Track heading hierarchy
    current_heading_path = ""

    for line in lines:
        # Check if line is a heading
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)

        if heading_match:
            # Save previous chunk if exists
            if current_chunk:
                chunk_text = '\n'.join(current_chunk).strip()
                if chunk_text:
                    chunks.append((chunk_text, current_heading_path, 'section'))
                current_chunk = []

            # Update heading stack
            level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()

            # Pop headings of same or lower level
            while heading_stack and heading_stack[-1][0] >= level:
                heading_stack.pop()

            # Add current heading
            heading_stack.append((level, heading_text))
            current_heading_path = ' > '.join([h[1] for h in heading_stack])

            # Add heading to current chunk
            current_chunk.append(line)
        else:
            current_chunk.append(line)

    # Save final chunk
    if current_chunk:
        chunk_text = '\n'.join(current_chunk).strip()
        if chunk_text:
            chunks.append((chunk_text, current_heading_path, 'section'))

    return chunks

def split_large_chunks(chunks: List[Tuple[str, str, str]], max_tokens: int = 500) -> List[Tuple[str, str, str]]:
    """
    Split chunks that are too large (rough estimate: 1 token ≈ 4 chars)
    """
    max_chars = max_tokens * 4
    result = []

    for chunk_text, heading_path, chunk_type in chunks:
        if len(chunk_text) <= max_chars:
            result.append((chunk_text, heading_path, chunk_type))
        else:
            # Split by paragraphs
            paragraphs = chunk_text.split('\n\n')
            current_subchunk = []
            current_length = 0

            for para in paragraphs:
                para_length = len(para)

                if current_length + para_length > max_chars and current_subchunk:
                    # Save current subchunk
                    subchunk_text = '\n\n'.join(current_subchunk)
                    result.append((subchunk_text, heading_path, 'subsection'))
                    current_subchunk = []
                    current_length = 0

                current_subchunk.append(para)
                current_length += para_length

            # Save final subchunk
            if current_subchunk:
                subchunk_text = '\n\n'.join(current_subchunk)
                result.append((subchunk_text, heading_path, 'subsection'))

    return result

def chunk_document(file_path: Path, metadata: Dict, project_root: Path) -> List[Dict]:
    """
    Chunk a single document and return chunk metadata
    """
    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip empty files
    if not content.strip():
        return []

    # Split by headings
    chunks = split_by_headings(content, file_path)

    # Split large chunks
    chunks = split_large_chunks(chunks, max_tokens=500)

    # Create chunk objects
    chunk_objects = []
    rel_path = str(file_path.relative_to(project_root))

    for idx, (chunk_text, heading_path, chunk_type) in enumerate(chunks):
        chunk_obj = {
            'file_path': rel_path,
            'file_title': metadata['title'],
            'chunk_index': idx,
            'chunk_type': chunk_type,
            'content': chunk_text,
            'heading_path': heading_path if heading_path else None,
            'priority': metadata['priority'],
            'status': metadata['status'],
            'date_created': metadata['date_created'],
            'date_modified': metadata['date_modified'],
            'has_gdrive_dates': metadata['has_gdrive_dates'],
            'word_count': len(chunk_text.split()),
            'char_count': len(chunk_text),
            'file_references': metadata.get('cross_references', []),
            'referenced_by': [],  # Will be computed later
            'flagged': False,
            'flag_reason': None,
            'flag_date': None,
            'quality_score': 1.0,
            'indexed_at': datetime.now().isoformat()
        }
        chunk_objects.append(chunk_obj)

    return chunk_objects

def main():
    """Chunk all documents"""

    project_root = Path(__file__).parent.parent
    index_path = project_root / 'document_index.json'
    output_path = project_root / 'document_chunks.json'

    print("Loading document index...")
    with open(index_path, 'r', encoding='utf-8') as f:
        document_index = json.load(f)

    print(f"Found {len(document_index)} documents")

    all_chunks = []
    total_chunks = 0

    print("\nChunking documents...")
    for doc in document_index:
        file_path = project_root / doc['file_path']

        if not file_path.exists():
            print(f"[WARNING] File not found: {file_path}")
            continue

        try:
            chunks = chunk_document(file_path, doc, project_root)
            all_chunks.extend(chunks)
            total_chunks += len(chunks)

            # Progress indicator
            if len(all_chunks) % 100 == 0:
                print(f"  Processed {len(all_chunks)} chunks from {document_index.index(doc)+1}/{len(document_index)} documents...")

        except Exception as e:
            print(f"[ERROR] Failed to chunk {file_path}: {e}")

    print(f"\n[OK] Chunked {len(document_index)} documents into {total_chunks} chunks")

    # Save chunks
    print(f"Saving chunks to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    # Statistics
    total_words = sum(chunk['word_count'] for chunk in all_chunks)
    total_chars = sum(chunk['char_count'] for chunk in all_chunks)
    avg_chunk_size = total_words / len(all_chunks) if all_chunks else 0

    print(f"\nStatistics:")
    print(f"  Total chunks: {total_chunks}")
    print(f"  Total words: {total_words:,}")
    print(f"  Total characters: {total_chars:,}")
    print(f"  Average chunk size: {avg_chunk_size:.1f} words")
    print(f"  Estimated tokens: ~{total_words * 1.3:.0f} (1 token ~= 0.75 words)")

    # Priority breakdown
    priority_counts = {}
    for chunk in all_chunks:
        p = chunk['priority']
        priority_counts[p] = priority_counts.get(p, 0) + 1

    print(f"\nChunks by priority:")
    for priority in sorted(priority_counts.keys()):
        count = priority_counts[priority]
        pct = (count / total_chunks) * 100
        print(f"  Priority {priority}: {count} chunks ({pct:.1f}%)")

    print(f"\n[OK] Chunks saved to: {output_path}")

if __name__ == "__main__":
    main()
