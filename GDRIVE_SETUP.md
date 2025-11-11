# Google Drive Metadata Sync Setup

This guide walks you through setting up Google Drive API access to sync accurate file creation/modification dates for your RAG system.

---

## Why This Matters

All your `.md` files were created today (2025-01-10) during DOCX conversion, so filesystem dates are useless. Google Drive has the **real** dates from when you originally created and edited the documents.

---

## Setup Steps

### 1. Install Dependencies

```bash
pip install -r requirements-gdrive.txt
```

### 2. Enable Google Drive API

1. Go to: https://console.cloud.google.com/
2. Create a new project (or select existing one)
   - Project name: "Open Systems RAG" (or whatever you want)
3. Enable the Google Drive API:
   - Search for "Google Drive API" in the API Library
   - Click "Enable"

### 3. Create OAuth Credentials

1. In Google Cloud Console, go to: **Credentials**
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. If prompted, configure OAuth consent screen:
   - User type: **External**
   - App name: "Open Systems RAG"
   - User support email: (your email)
   - Developer contact: (your email)
   - Add scope: `https://www.googleapis.com/auth/drive.readonly`
   - Add test users: (your Google account email)
4. Back to "Create OAuth client ID":
   - Application type: **Desktop app**
   - Name: "Open Systems Desktop Client"
5. Click **"Create"**
6. Download the JSON file
7. Rename it to `credentials.json`
8. Place it in project root: `d:\Dev\Open Systems\Open Systems\credentials.json`

**Important:** Add `credentials.json` to `.gitignore` (contains sensitive info!)

### 4. Authorize Access

Run the OAuth setup script:

```bash
python scripts/setup_gdrive_auth.py
```

This will:
1. Open a browser window
2. Ask you to sign in to Google
3. Request permission to read your Drive files (read-only)
4. Save authorization token to `.gdrive_token.pickle`

**Note:** The token is saved locally and reused for future runs.

### 5. Sync Metadata

Run the sync script:

```bash
# Sync entire Drive (searches all folders)
python scripts/sync_gdrive_metadata.py

# Or limit to specific folder (faster)
python scripts/sync_gdrive_metadata.py --folder-id YOUR_FOLDER_ID
```

To find your folder ID:
1. Open the folder in Google Drive
2. Look at the URL: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
3. Copy the ID after `/folders/`

### 6. Verify Results

The script will:
- Fetch all files from Google Drive
- Match them to local `.md` files by filename
- Output `gdrive_metadata.json` with accurate dates
- Show stats on matched/unmatched files

Check the output:
```bash
cat gdrive_metadata.json | head -50
```

You should see entries like:
```json
{
  "DATA-DUMP/Recent/From Open Systems Project in ChatGpt/open_projects_spec_v_1.md": {
    "gdrive_id": "1ABC...",
    "date_created": "2023-11-15T10:30:00.000Z",
    "date_modified": "2024-01-05T14:22:00.000Z",
    "revision_count": 6,
    "revisions": [...]
  }
}
```

---

## Using Synced Metadata

### In Phase 1 Indexing

When building `scripts/index_documents.py`, load the synced metadata:

```python
import json
from pathlib import Path

# Load Google Drive metadata
gdrive_metadata = {}
metadata_file = Path("gdrive_metadata.json")
if metadata_file.exists():
    with open(metadata_file) as f:
        gdrive_metadata = json.load(f)

def extract_metadata(file_path: Path) -> dict:
    # Try to get Google Drive dates
    rel_path = str(file_path.relative_to(project_root))

    if rel_path in gdrive_metadata:
        # Use accurate Google Drive dates
        gdrive = gdrive_metadata[rel_path]
        date_created = datetime.fromisoformat(gdrive['date_created'].replace('Z', '+00:00'))
        date_modified = datetime.fromisoformat(gdrive['date_modified'].replace('Z', '+00:00'))
        revision_count = gdrive['revision_count']
    else:
        # Fallback to filesystem (will be 2025-01-10)
        date_created = datetime.fromtimestamp(file_path.stat().st_ctime)
        date_modified = datetime.fromtimestamp(file_path.stat().st_mtime)
        revision_count = None

    return {
        'date_created': date_created,
        'date_modified': date_modified,
        'revision_count': revision_count,
        'has_gdrive_dates': rel_path in gdrive_metadata
    }
```

---

## Troubleshooting

### "credentials.json not found"
- Make sure you downloaded OAuth credentials from Google Cloud Console
- Rename the file to exactly `credentials.json`
- Place it in project root

### "No files found in Google Drive"
- Check if your Google account has access to the files
- Try running without `--folder-id` to search all Drive
- Verify the files are in Google Drive (not Google Docs format)

### "Could not match local files"
- Files might have been renamed after downloading from Drive
- Check if filenames match (case-insensitive, but must be similar)
- Some files might not have been in Google Drive originally

### "OAuth flow failed"
- Make sure you added your email as a test user in OAuth consent screen
- Try running with `--refresh` flag: `python scripts/setup_gdrive_auth.py --refresh`
- Check browser isn't blocking popup windows

---

## Re-syncing Later

To update metadata after changes in Google Drive:

```bash
# Re-fetch all metadata
python scripts/sync_gdrive_metadata.py

# This overwrites gdrive_metadata.json with latest dates
```

No need to re-run OAuth setup unless token expires (usually lasts ~7 days for test users).

---

## Security Notes

**Files to keep private (add to `.gitignore`):**
- `credentials.json` - OAuth client secrets
- `.gdrive_token.pickle` - Your authorization token
- `gdrive_metadata.json` - Optional (doesn't contain secrets, but has your file structure)

**API permissions:**
- Read-only access to Drive files
- Cannot modify, delete, or upload files
- Only fetches metadata (filenames, dates)

---

## Next Steps

After syncing metadata:
1. Verify `gdrive_metadata.json` looks correct
2. Proceed to Phase 1: Build indexing script
3. Use synced dates during indexing for accurate temporal ranking

---

*Estimated time: 30 minutes for first-time setup*
