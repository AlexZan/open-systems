#!/usr/bin/env python3
"""
Google Drive OAuth Setup Script

This script sets up authentication for accessing Google Drive metadata.
Run this once to authorize access and save credentials.

Prerequisites:
1. Go to https://console.cloud.google.com/
2. Create a new project (or select existing)
3. Enable Google Drive API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials.json and place in project root

Usage:
    python scripts/setup_gdrive_auth.py
"""

import os
import pickle
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes required (read-only access to Drive files)
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_credentials(force_refresh: bool = False):
    """
    Get or refresh Google Drive credentials.

    Args:
        force_refresh: Force new OAuth flow even if token exists

    Returns:
        Credentials object
    """
    project_root = Path(__file__).parent.parent
    token_path = project_root / '.gdrive_token.pickle'
    credentials_path = project_root / 'credentials.json'

    # Check if credentials.json exists
    if not credentials_path.exists():
        print("\n[FAIL] ERROR: credentials.json not found!")
        print("\nTo set up Google Drive API access:")
        print("1. Go to: https://console.cloud.google.com/")
        print("2. Create a new project or select existing")
        print("3. Enable 'Google Drive API'")
        print("4. Go to 'Credentials' → 'Create Credentials' → 'OAuth client ID'")
        print("5. Choose 'Desktop app' as application type")
        print("6. Download the credentials JSON file")
        print(f"7. Save it as: {credentials_path}")
        print("\nThen run this script again.")
        return None

    creds = None

    # Load existing token if available
    if token_path.exists() and not force_refresh:
        print("Loading existing credentials...")
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired credentials...")
            try:
                creds.refresh(Request())
                print("[OK] Credentials refreshed successfully")
            except Exception as e:
                print(f"[FAIL] Failed to refresh credentials: {e}")
                print("Starting new OAuth flow...")
                creds = None

        if not creds:
            print("\nStarting OAuth flow...")
            print("A browser window will open for you to authorize access.")
            print("Choose the Google account that has access to your Drive files.")

            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_path),
                    SCOPES
                )
                creds = flow.run_local_server(port=0)
                print("[OK] Authorization successful!")
            except Exception as e:
                print(f"[FAIL] OAuth flow failed: {e}")
                return None

        # Save credentials for next time
        print(f"Saving credentials to: {token_path}")
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

        print("[OK] Credentials saved")
    else:
        print("[OK] Using valid existing credentials")

    return creds

def test_credentials(creds):
    """Test if credentials work by fetching user info"""
    from googleapiclient.discovery import build

    try:
        service = build('drive', 'v3', credentials=creds)
        about = service.about().get(fields='user').execute()
        user = about.get('user', {})

        print(f"\n[OK] Successfully authenticated as:")
        print(f"  Name: {user.get('displayName', 'Unknown')}")
        print(f"  Email: {user.get('emailAddress', 'Unknown')}")

        return True
    except Exception as e:
        print(f"\n[FAIL] Failed to test credentials: {e}")
        return False

def main():
    print("\n=== Google Drive OAuth Setup ===\n")

    # Get or refresh credentials
    creds = get_credentials()

    if not creds:
        print("\n[FAIL] Failed to obtain credentials")
        return 1

    # Test credentials
    if test_credentials(creds):
        print("\n[OK] Setup complete! You can now run:")
        print("   python scripts/sync_gdrive_metadata.py")
        return 0
    else:
        print("\n[FAIL] Credentials don't work. Try running with --refresh flag")
        return 1

if __name__ == "__main__":
    import sys

    # Check for --refresh flag
    force_refresh = '--refresh' in sys.argv

    if force_refresh:
        print("Force refresh requested - will start new OAuth flow\n")

    sys.exit(main())
