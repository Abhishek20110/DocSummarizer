#here user serice account is used to access the google drive
import os
import json
from functools import lru_cache
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def _load_credentials():
    """
    Loads Google service account credentials.
    Priority:
    1. credentials.json file (local development)
    2. GOOGLE_CREDENTIALS environment variable (production)
    """

    # 1️⃣ Local development support
    if os.path.exists("credentials.json"):
        return service_account.Credentials.from_service_account_file(
            "credentials.json",
            scopes=SCOPES,
        )

    # 2️⃣ Production (Environment variable)
    creds_json = os.getenv("GOOGLE_CREDENTIALS")
    if not creds_json:
        raise RuntimeError(
            "GOOGLE_CREDENTIALS environment variable not set "
            "and credentials.json not found."
        )

    try:
        creds_dict = json.loads(creds_json)
    except json.JSONDecodeError:
        raise RuntimeError("GOOGLE_CREDENTIALS contains invalid JSON.")

    # Validate correct credential type
    if creds_dict.get("type") != "service_account":
        raise RuntimeError(
            "Invalid credentials type. Expected 'service_account' JSON."
        )

    return service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=SCOPES,
    )

@lru_cache()
def get_drive_service():
    """
    Returns a cached, authenticated Google Drive service client.
    Cached for efficiency in serverless environments.
    """
    try:
        credentials = _load_credentials()

        service = build(
            "drive",
            "v3",
            credentials=credentials,
            cache_discovery=False,  # Important for serverless
        )

        return service

    except HttpError as error:
        raise RuntimeError(f"Google Drive API error: {error}")

    except Exception as e:
        raise RuntimeError(f"Failed to initialize Drive service: {str(e)}")