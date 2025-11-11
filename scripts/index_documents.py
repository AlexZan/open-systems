#!/usr/bin/env python3
"""
Document Indexing Script for RAG System

Scans all markdown files in DATA-DUMP and extracts:
- File metadata (title, path, dates from Google Drive)
- Document structure (headings, hierarchy)
- Topics and keywords
- Cross-references
- Priority classification based on folder location

Outputs: document_index.json for loading into vector database
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

# Priority mapping based on folder location
PRIORITY_MAP = {
    'Recent/From Open Systems Project in ChatGpt': 1,  # Current specs
    'Recent': 1,
    'Published': 2,
    'Introduction': 2,
    'Technical': 3,
    'Theory': 3,
    'Applications': 3,
    'Plan': 3,
    'Rules': 3,
    'Thoughts': 4,
    'Depricated': 5,
    'Open Systems Shared': 3,  # Historical but comprehensive
}

# Status classification
STATUS_MAP = {
    'Recent/From Open Systems Project in ChatGpt': 'current',
    'Recent': 'current',
    'Published': 'current',
    'Introduction': 'current',
    'Depricated': 'deprecated',
    'Open Systems Shared': 'historical',
}


def load_gdrive_metadata() -> Dict:
    """Load Google Drive metadata with accurate dates"""
    project_root = Path(__file__).parent.parent
    metadata_file = project_root / 'gdrive_metadata.json'

    if metadata_file.exists():
        with open(metadata_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    print("[WARNING] gdrive_metadata.json not found - dates will be inaccurate")
    return {}


def classify_priority(file_path: Path, project_root: Path) -> Tuple[int, str]:
    """
    Classify document priority based on folder location

    Returns:
        (priority: int, status: str)
    """
    rel_path = str(file_path.relative_to(project_root))

    # Check each priority mapping
    for folder_pattern, priority in PRIORITY_MAP.items():
        if folder_pattern in rel_path:
            status = STATUS_MAP.get(folder_pattern, 'historical')
            return priority, status

    # Default: unknown location
    return 4, 'unknown'


def extract_headings(content: str) -> List[Dict]:
    """
    Extract markdown headings and build hierarchy

    Returns list of:
    {
        'level': int,
        'text': str,
        'line_number': int,
        'hierarchy': str  # e.g., "Introduction > System Overview > Goals"
    }
    """
    headings = []
    hierarchy_stack = []

    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()

            # Update hierarchy stack
            # Pop headings of same or lower level
            while hierarchy_stack and hierarchy_stack[-1]['level'] >= level:
                hierarchy_stack.pop()

            # Add current heading
            hierarchy_stack.append({'level': level, 'text': text})

            # Build hierarchy path
            hierarchy_path = ' > '.join([h['text'] for h in hierarchy_stack])

            headings.append({
                'level': level,
                'text': text,
                'line_number': i,
                'hierarchy': hierarchy_path
            })

    return headings


def extract_cross_references(content: str, file_path: Path) -> List[str]:
    """
    Extract cross-references to other documents

    Looks for:
    - Markdown links: [text](other_file.md)
    - Direct mentions: "see open_projects_spec_v_1.md"
    - Relative references: "as described in the Projects spec"
    """
    references = []

    # Extract markdown links to .md files
    md_links = re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)', content)
    for link_text, link_path in md_links:
        references.append(link_path)

    # Extract direct .md mentions
    direct_mentions = re.findall(r'\b(\w+\.md)\b', content)
    references.extend(direct_mentions)

    # Deduplicate
    return list(set(references))


def extract_topics(content: str, headings: List[Dict]) -> List[str]:
    """
    Extract main topics from document

    Uses:
    - Top-level headings (h1, h2)
    - Title patterns
    - Key terminology
    """
    topics = []

    # Extract from headings
    for heading in headings:
        if heading['level'] <= 2:
            topics.append(heading['text'])

    # Extract from content (look for bolded key terms)
    bold_terms = re.findall(r'\*\*([^*]+)\*\*', content)
    topics.extend(bold_terms[:10])  # Limit to first 10

    # Deduplicate and clean
    topics = list(set(topics))
    topics = [t.strip() for t in topics if len(t.strip()) > 3]

    return topics[:20]  # Max 20 topics per document


def extract_metadata(file_path: Path, project_root: Path, gdrive_metadata: Dict) -> Dict:
    """
    Extract complete metadata for a single markdown file
    """
    rel_path = str(file_path.relative_to(project_root))

    # Read file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[FAIL] Could not read {rel_path}: {e}")
        return None

    # Extract title (first h1 or filename)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = file_path.stem.replace('_', ' ').title()

    # Get dates from Google Drive or filesystem fallback
    if rel_path in gdrive_metadata:
        gdrive_data = gdrive_metadata[rel_path]
        date_created = gdrive_data['date_created']
        date_modified = gdrive_data['date_modified']
        has_gdrive_dates = True
    else:
        # Fallback to filesystem (will be 2025-01-10 for converted files)
        stat = file_path.stat()
        date_created = datetime.fromtimestamp(stat.st_ctime).isoformat() + 'Z'
        date_modified = datetime.fromtimestamp(stat.st_mtime).isoformat() + 'Z'
        has_gdrive_dates = False

    # Classify priority and status
    priority, status = classify_priority(file_path, project_root)

    # Extract structure
    headings = extract_headings(content)
    topics = extract_topics(content, headings)
    cross_refs = extract_cross_references(content, file_path)

    # Calculate stats
    word_count = len(content.split())
    line_count = len(content.split('\n'))

    return {
        'file_path': rel_path,
        'title': title,
        'date_created': date_created,
        'date_modified': date_modified,
        'has_gdrive_dates': has_gdrive_dates,
        'priority': priority,
        'status': status,
        'word_count': word_count,
        'line_count': line_count,
        'heading_count': len(headings),
        'headings': headings,
        'topics': topics,
        'cross_references': cross_refs,
        'indexed_at': datetime.now().isoformat()
    }


def build_cross_reference_graph(documents: List[Dict]) -> Dict[str, List[str]]:
    """
    Build bidirectional cross-reference graph

    Returns:
    {
        'file_path': ['referenced_by_1', 'referenced_by_2', ...]
    }
    """
    graph = defaultdict(list)

    # Map of filename to full path
    filename_to_path = {}
    for doc in documents:
        filename = Path(doc['file_path']).name
        filename_to_path[filename] = doc['file_path']

    # Build graph
    for doc in documents:
        source_path = doc['file_path']

        for ref in doc['cross_references']:
            # Try to resolve reference
            ref_filename = Path(ref).name
            if ref_filename in filename_to_path:
                target_path = filename_to_path[ref_filename]
                graph[target_path].append(source_path)

    return dict(graph)


def main():
    print("\n=== Document Indexing for RAG System ===\n")

    project_root = Path(__file__).parent.parent
    data_dump = project_root / "DATA-DUMP"

    if not data_dump.exists():
        print(f"[FAIL] DATA-DUMP not found at: {data_dump}")
        return 1

    # Load Google Drive metadata
    print("Loading Google Drive metadata...")
    gdrive_metadata = load_gdrive_metadata()
    print(f"  {len(gdrive_metadata)} files with Google Drive dates")

    # Find all markdown files
    print("\nScanning for markdown files...")
    md_files = list(data_dump.rglob("*.md"))
    print(f"  Found {len(md_files)} markdown files")

    # Extract metadata from each file
    print("\nExtracting metadata...")
    documents = []
    for i, md_file in enumerate(md_files, 1):
        if i % 20 == 0:
            print(f"  Processed {i}/{len(md_files)} files...")

        metadata = extract_metadata(md_file, project_root, gdrive_metadata)
        if metadata:
            documents.append(metadata)

    print(f"\n[OK] Extracted metadata from {len(documents)} documents")

    # Build cross-reference graph
    print("\nBuilding cross-reference graph...")
    ref_graph = build_cross_reference_graph(documents)
    print(f"  {len(ref_graph)} documents have incoming references")

    # Add referenced_by to each document
    for doc in documents:
        doc['referenced_by'] = ref_graph.get(doc['file_path'], [])
        doc['reference_count'] = len(doc['referenced_by'])

    # Generate statistics
    print("\n=== Statistics ===")
    print(f"Total documents: {len(documents)}")
    print(f"\nBy priority:")
    priority_counts = defaultdict(int)
    for doc in documents:
        priority_counts[doc['priority']] += 1
    for priority in sorted(priority_counts.keys()):
        print(f"  Priority {priority}: {priority_counts[priority]} documents")

    print(f"\nBy status:")
    status_counts = defaultdict(int)
    for doc in documents:
        status_counts[doc['status']] += 1
    for status, count in status_counts.items():
        print(f"  {status}: {count} documents")

    print(f"\nDates:")
    with_gdrive = sum(1 for doc in documents if doc['has_gdrive_dates'])
    without_gdrive = len(documents) - with_gdrive
    print(f"  With Google Drive dates: {with_gdrive}")
    print(f"  Without (using filesystem): {without_gdrive}")

    # Most referenced documents
    print(f"\nMost referenced documents:")
    top_referenced = sorted(documents, key=lambda d: d['reference_count'], reverse=True)[:5]
    for doc in top_referenced:
        if doc['reference_count'] > 0:
            # Encode title to ASCII, replacing non-ASCII chars
            safe_title = doc['title'].encode('ascii', 'replace').decode('ascii')
            print(f"  {safe_title}: {doc['reference_count']} references")

    # Save to JSON
    output_path = project_root / "document_index.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Index saved to: {output_path}")
    print(f"\nNext step: Create chunking script to split documents for vectorization")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
