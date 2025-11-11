#!/usr/bin/env python3
"""
Convert DOCX files to Markdown using Pandoc, one at a time, and delete originals.
Usage: python convert_docx.py
"""

import os
import subprocess
import sys
from pathlib import Path

def convert_docx_to_md(docx_path):
    """Convert a single DOCX file to Markdown using Pandoc."""
    try:
        # Create MD file path
        md_path = docx_path.with_suffix('.md')

        # Run Pandoc conversion
        result = subprocess.run(
            ['pandoc', str(docx_path), '-f', 'docx', '-t', 'markdown', '-o', str(md_path)],
            capture_output=True,
            text=True,
            check=True
        )

        # Delete original DOCX
        os.remove(docx_path)

        return True, f"[OK] Converted: {docx_path.name} -> {md_path.name}"

    except subprocess.CalledProcessError as e:
        return False, f"[FAIL] Pandoc error: {docx_path.name} - {e.stderr}"
    except Exception as e:
        return False, f"[FAIL] Error: {docx_path.name} - {str(e)}"

def find_all_docx(root_dir):
    """Find all DOCX files recursively."""
    root = Path(root_dir)
    return sorted(root.rglob("*.docx"))

def main():
    root_dir = Path(__file__).parent

    # Find all DOCX files
    docx_files = find_all_docx(root_dir)

    if not docx_files:
        print("No DOCX files found.")
        return

    print(f"Found {len(docx_files)} DOCX files.\n")
    print("Converting files one by one (will delete originals after conversion)...\n")

    successful = 0
    failed = 0
    failed_files = []

    for i, docx_path in enumerate(docx_files, 1):
        rel_path = docx_path.relative_to(root_dir)
        print(f"[{i}/{len(docx_files)}] {rel_path}")

        success, message = convert_docx_to_md(docx_path)
        print(f"  {message}")

        if success:
            successful += 1
        else:
            failed += 1
            failed_files.append(str(rel_path))

        print()

    print(f"\n{'='*60}")
    print(f"Conversion complete!")
    print(f"{'='*60}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    if failed_files:
        print(f"\nFailed files:")
        for f in failed_files:
            print(f"  - {f}")

if __name__ == "__main__":
    main()
