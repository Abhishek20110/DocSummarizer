import io
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

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

    results = service.files().list(
        q=query,
        fields="files(id, name, mimeType, size)"
    ).execute()

    return results.get("files", [])


def get_folder_name(service, folder_id):
    """Gets the name of a Google Drive folder."""
    result = service.files().get(
        fileId=folder_id,
        fields="name"
    ).execute()

    return result.get("name", "Unknown Folder")


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
        print(f"Skipping {file_name} (>{MAX_FILE_SIZE // (1024*1024)}MB)")
        return None

    try:
        request = service.files().get_media(fileId=file_id)

        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)

        done = False
        while not done:
            _, done = downloader.next_chunk()

        file_stream.seek(0)
        return file_stream

    except HttpError as e:
        print(f"Error downloading {file_name}: {e}")
        return None