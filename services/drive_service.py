import io
from googleapiclient.http import MediaIoBaseDownload
import logging
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

# 10 MB limit
MAX_FILE_SIZE = 10 * 1024 * 1024  # bytes


def list_files_in_folder(service, folder_id):
    """
    Lists supported files in a specific Google Drive folder.
    Returns metadata including file size.
    """

    query = (
        f"'{folder_id}' in parents and "
        "(mimeType = 'application/pdf' or "
        "mimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or "
        "mimeType = 'text/plain') and trashed = false"
    )

    try:
        results = service.files().list(
            q=query,
            fields="files(id, name, mimeType, size)"
        ).execute()

        files = results.get("files", [])
        logger.info(f"Found {len(files)} supported files in folder {folder_id}.")
        return files
    except HttpError as e:
        logger.error(f"HTTP error listing files for folder {folder_id}: {e}")
        if e.resp.status in [403, 404]:
            raise ValueError("Permission denied or folder not found. Ensure the folder is public or shared with the service account.")
        raise ValueError(f"Failed to access Google Drive: {e._get_reason()}")


def get_folder_name(service, folder_id):
    """Gets the name of a Google Drive folder."""
    try:
        result = service.files().get(
            fileId=folder_id,
            fields="name"
        ).execute()

        return result.get("name", "Unknown Folder")
    except HttpError as e:
        logger.error(f"HTTP error getting folder name {folder_id}: {e}")
        if e.resp.status in [403, 404]:
            raise ValueError("Permission denied or folder not found. Ensure the folder is public or shared with the service account.")
        raise ValueError(f"Failed to retrieve folder details: {e._get_reason()}")


def download_file_to_memory(service, file_metadata):
    """
    Downloads a file into memory.
    Automatically skips files larger than 10MB.
    Returns BytesIO stream or None if skipped.
    """

    file_id = file_metadata["id"]
    file_name = file_metadata["name"]
    file_size = int(file_metadata.get("size", 0))

    # 🔹 Auto skip large files
    if file_size > MAX_FILE_SIZE:
        logger.warning(f"Skipping {file_name} (>{MAX_FILE_SIZE // (1024*1024)}MB)")
        return None

    try:
        request = service.files().get_media(fileId=file_id)

        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)

        done = False
        while not done:
            _, done = downloader.next_chunk()

        file_stream.seek(0)
        logger.info(f"Successfully downloaded: {file_name}")
        return file_stream

    except HttpError as e:
        logger.error(f"Error downloading {file_name}: {e}")
        return None