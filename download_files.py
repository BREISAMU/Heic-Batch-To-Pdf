import io
import os
from pathlib import Path
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from search_and_verify import verify, folder
from params import FOLDER_OF_INTERST
import shutil

def get_download_path():
    home = str(Path.home())
    downloads_folder = ''

    # Detect the operating system and set the Downloads folder path accordingly
    if os.name == 'nt':  # Windows
        downloads_folder = os.path.join(home, 'Downloads')
    else:  # macOS or Linux
        downloads_folder = os.path.join(home, 'Downloads')

    return os.path.join(downloads_folder)

def download_file(real_file_id):
    creds = verify()
    try:
        # create drive api client
        service = build("drive", "v3", credentials=creds)
        file_id = real_file_id
        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}.")
    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    return file.getvalue()

def get_images():
    fois = folder(FOLDER_OF_INTERST)
    for i in range(len(fois)):
        fh = download_file(real_file_id=fois[i])
        # Write the downloaded content to a file on your local filesystem
        with open('./heics/garbage' + str(i)  + '.heic', 'wb') as f:
            f.write(fh)
    