#!/usr/bin/env python3
"""
Google Drive Metadata Sync Script

Syncs metadata (creation/modification dates, revision history) from Google Drive
to local database for accurate temporal tracking in RAG system.

Usage:
    python scripts/sync_gdrive_metadata.py [--folder-id YOUR_FOLDER_ID]

If no folder ID provided, will search entire Drive (slower but thorough).
"""

import json
import pickle
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import argparse

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def load_credentials() -> Optional[Credentials]:
    """Load saved Google Drive credentials"""
    token_path = Path(__file__).parent.parent / '.gdrive_token.pickle'

    if not token_path.exists():
        print("[FAIL] No credentials found. Run setup_gdrive_auth.py first")
        return None

    with open(token_path, 'rb') as token:
        return pickle.load(token)

def get_gdrive_files(service, folder_id: Optional[str] = None) -> Dict[str, dict]:
    """
    Fetch all file metadata from Google Drive

    Args:
        service: Google Drive API service
        folder_id: Optional folder ID to limit search

    Returns:
        Dict mapping filename to metadata
    """
    print("Fetching files from Google Drive...")

    # Build query
    if folder_id:
        query = f"'{folder_id}' in parents"
        print(f"  Searching in folder ID: {folder_id}")
    else:
        query = "mimeType='application/vnd.google-apps.document' or mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document'"
        print("  Searching entire Drive (this may take a while)...")

    files_metadata = {}
    page_token = None
    file_count = 0

    while True:
        try:
            results = service.files().list(
                q=query,
                spaces='drive',
                fields='nextPageToken, files(id, name, createdTime, modifiedTime, version, parents, mimeType)',
                pageToken=page_token,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()

            files = results.get('files', [])

            for file in files:
                file_count += 1
                print(f"  [{file_count}] {file['name']}")

                # Get revision history (skip for Google Docs - they don't support revision API)
                revisions = []
                if file.get('mimeType') != 'application/vnd.google-apps.document':
                    try:
                        revisions_result = service.revisions().list(
                            fileId=file['id'],
                            fields='revisions(id, modifiedTime, lastModifyingUser)',
                            pageSize=100
                        ).execute()

                        revisions = revisions_result.get('revisions', [])
                    except Exception as e:
                        print(f"    [WARNING] Could not fetch revisions: {e}")
                        revisions = []

                # Store metadata
                files_metadata[file['name']] = {
                    'id': file['id'],
                    'name': file['name'],
                    'mime_type': file.get('mimeType'),
                    'created': file.get('createdTime'),
                    'modified': file.get('modifiedTime'),
                    'version': file.get('version'),
                    'revision_count': len(revisions),
                    'revisions': [
                        {
                            'id': rev['id'],
                            'modified': rev['modifiedTime'],
                            'user': rev.get('lastModifyingUser', {}).get('displayName', 'Unknown')
                        }
                        for rev in revisions
                    ]
                }

            page_token = results.get('nextPageToken')
            if not page_token:
                break

        except Exception as e:
            print(f"[FAIL] Error fetching files: {e}")
            break

    print(f"\n[OK] Found {len(files_metadata)} files")
    return files_metadata

def match_local_to_gdrive(local_path: Path, gdrive_files: Dict[str, dict]) -> Optional[dict]:
    """
    Match local file to Google Drive metadata

    Args:
        local_path: Path to local markdown file
        gdrive_files: Dict of Google Drive file metadata

    Returns:
        Matched metadata or None
    """
    local_stem = local_path.stem  # Filename without extension

    # Try exact match first (handles .md)
    for gdrive_name, metadata in gdrive_files.items():
        gdrive_stem = Path(gdrive_name).stem
        if gdrive_stem == local_stem:
            return metadata

    # Try fuzzy match (handle "My Doc.docx" → "My Doc.md")
    for gdrive_name, metadata in gdrive_files.items():
        gdrive_stem = Path(gdrive_name).stem
        # Normalize: remove special chars, lowercase, compare
        local_normalized = local_stem.lower().replace('_', ' ').replace('-', ' ')
        gdrive_normalized = gdrive_stem.lower().replace('_', ' ').replace('-', ' ')

        if local_normalized == gdrive_normalized:
            return metadata

    return None

def sync_metadata(folder_id: Optional[str] = None, output_json: bool = True):
    """
    Main sync function

    Args:
        folder_id: Optional Google Drive folder ID
        output_json: Whether to output JSON file with metadata
    """
    print("\n=== Google Drive Metadata Sync ===\n")

    # Load credentials
    creds = load_credentials()
    if not creds:
        return 1

    # Build Drive service
    service = build('drive', 'v3', credentials=creds)

    # Fetch Google Drive metadata
    gdrive_files = get_gdrive_files(service, folder_id)

    if not gdrive_files:
        print("[FAIL] No files found in Google Drive")
        return 1

    # Match local files to Google Drive
    print("\nMatching local files to Google Drive metadata...")
    project_root = Path(__file__).parent.parent
    data_dump = project_root / "DATA-DUMP"

    if not data_dump.exists():
        print(f"[FAIL] DATA-DUMP directory not found at: {data_dump}")
        return 1

    # Find all markdown files
    local_files = list(data_dump.rglob("*.md"))
    print(f"Found {len(local_files)} local markdown files")

    matched_metadata = {}
    matched_count = 0
    unmatched = []

    for local_path in local_files:
        rel_path = local_path.relative_to(project_root)
        gdrive_meta = match_local_to_gdrive(local_path, gdrive_files)

        if gdrive_meta:
            matched_count += 1
            print(f"[OK] {rel_path}")
            print(f"    GDrive: {gdrive_meta['name']}")
            print(f"    Created: {gdrive_meta['created']}")
            print(f"    Modified: {gdrive_meta['modified']}")
            print(f"    Revisions: {gdrive_meta['revision_count']}")

            matched_metadata[str(rel_path)] = {
                'file_path': str(rel_path),
                'gdrive_id': gdrive_meta['id'],
                'gdrive_name': gdrive_meta['name'],
                'mime_type': gdrive_meta['mime_type'],
                'date_created': gdrive_meta['created'],
                'date_modified': gdrive_meta['modified'],
                'revision_count': gdrive_meta['revision_count'],
                'revisions': gdrive_meta['revisions'],
                'synced_at': datetime.now().isoformat()
            }
        else:
            unmatched.append(str(rel_path))

    print(f"\n[OK] Matched {matched_count}/{len(local_files)} files")

    if unmatched:
        print(f"\n[WARNING] {len(unmatched)} files could not be matched:")
        for path in unmatched[:10]:  # Show first 10
            print(f"  - {path}")
        if len(unmatched) > 10:
            print(f"  ... and {len(unmatched) - 10} more")

    # Save to JSON
    if output_json:
        output_path = project_root / "gdrive_metadata.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(matched_metadata, f, indent=2, ensure_ascii=False)

        print(f"\n[OK] Metadata saved to: {output_path}")
        print(f"  Use this file during indexing to get accurate dates")

    return 0

def main():
    parser = argparse.ArgumentParser(description='Sync Google Drive metadata')
    parser.add_argument(
        '--folder-id',
        help='Google Drive folder ID to search (optional)',
        default=None
    )
    parser.add_argument(
        '--no-json',
        action='store_true',
        help='Don\'t output JSON file'
    )

    args = parser.parse_args()

    return sync_metadata(
        folder_id=args.folder_id,
        output_json=not args.no_json
    )

if __name__ == "__main__":
    import sys
    sys.exit(main())
