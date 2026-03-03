import io
from googleapiclient.http import MediaIoBaseDownload
import os

def list_files_in_folder(service, folder_id):
    """Lists files in a specific Google Drive folder."""
    query = f"'{folder_id}' in parents and (mimeType = 'application/pdf' or mimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or mimeType = 'text/plain') and trashed = false"
    results = service.files().list(
        q=query, fields="files(id, name, mimeType)").execute()
    return results.get('files', [])

def get_folder_name(service, folder_id):
    """Gets the name of a Google Drive folder."""
    result = service.files().get(fileId=folder_id, fields="name").execute()
    return result.get('name', 'Unknown Folder')

def download_file(service, file_id, file_name, dest_folder='temp'):
    """Downloads a file from Google Drive."""
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
        
    request = service.files().get_media(fileId=file_id)
    file_path = os.path.join(dest_folder, file_name)
    
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        
    with open(file_path, 'wb') as f:
        f.write(fh.getvalue())
        
    return file_path
