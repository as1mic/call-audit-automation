from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload

from config import CREDENTIALS_PATH, TOKEN_PATH

SCOPES = ["https://www.googleapis.com/auth/drive"]

def get_drive_service():
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    service = build("drive", "v3", credentials=creds)

    return service


def list_files_in_folder(service, folder_id):
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()

    return results.get("files", [])


def is_audio_file(file_info):
    mime_type = file_info.get("mimeType", "")
    return mime_type.startswith("audio/")


def filter_audio_files(files):
    return [file for file in files if is_audio_file(file)]


def get_existing_file_names(service, folder_id):
    files = list_files_in_folder(service, folder_id)
    return set(file["name"] for file in files)


def copy_file_to_folder(service, file_id, target_folder_id, file_name):
    copied_file = {"name": file_name, "parents": [target_folder_id]}
    return service.files().copy(fileId=file_id, body=copied_file).execute()


def download_file(service, file_id, destination_path):
    request = service.files().get_media(fileId=file_id)
    with open(destination_path, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download progress: {int(status.progress() * 100)}%")
