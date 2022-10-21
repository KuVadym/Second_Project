from os import link
import pathlib
import dropbox
from dropbox import Dropbox
from dropbox.exceptions import AuthError
import io
import base64

from beanie import Document

class File(Document): # Now I don't know how it shoud work
    name = str
    link = str

# DROPBOX_ACCESS_TOKEN = ''


base64_DROPBOX_ACCESS_TOKEN = 'c2wuQlJsNDY3ZWQza19CU1ZxX0xCQk1YOVkzRHJ6V3NnLWpuWmRud2lLN2FVcFlMT0hKdl9nZ2oya05iaG1SUVA2cGY0dUFWNXdFSTNSdDYtcUdOM2Qtd29CWmo0R0RCYXZweWtyXzZOWE81SXRHZG5qSVRzM0pqeGRGYkdtbHFJejQwY3UyRy1iMTlBeGw='


base64_bytes = base64_DROPBOX_ACCESS_TOKEN.encode('ascii')
message_bytes = base64.b64decode(base64_bytes)
DROPBOX_ACCESS_TOKEN = message_bytes.decode('ascii')


CATEGORIES = ['archives', 'audio', 'documents', 'images', 'video']

FILE_TYPES = {'images': ('JPEG', 'PNG', 'JPG', 'SVG', 'BMP', 'TIF', 'TIFF', 'GIF', 'WEBP'),
              'archives': ('ZIP', 'GZ', 'TAR'),
              'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'PY'),
              'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
              'video':  ('AVI', 'MP4', 'MOV', 'MKV', 'MPG')
        }

def dropbox_connect(dropbox_token=DROPBOX_ACCESS_TOKEN):
    """Create a connection to Dropbox."""

    try:
        dbx = Dropbox(dropbox_token)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx


def order_files(dropbox_token=DROPBOX_ACCESS_TOKEN):
    links = dropbox_get_link(dropbox_token=dropbox_token)
    sort_files = {'images':{}, 'documents':{}}
    for key, value in links.items():
        ext = key.split(".")[-1]
        move_to =""
        for k, v in FILE_TYPES.items():
            if ext.upper() in FILE_TYPES.get(k):
                move_to = k
                break

        old_value = sort_files.get(move_to)
        old_value[key]=value
        sort_files[k]=old_value
    return sort_files


def dropbox_list_files(dropbox_token=DROPBOX_ACCESS_TOKEN):
    dbx = dropbox_connect(dropbox_token=dropbox_token)
    try:
        files = dbx.files_list_folder("").entries
        files_list = []
        for file in files:
            if isinstance(file, dropbox.files.FileMetadata):
                files_list.append(file)
        return files_list
    except Exception as e:
        print('Error getting list of files from Dropbox: ' + str(e))


def dropbox_upload_file(local_path, local_file, dropbox_file_path, dropbox_token=DROPBOX_ACCESS_TOKEN):
    try:
        dbx = dropbox_connect(dropbox_token=dropbox_token)

        local_file_path = pathlib.Path(local_path) / local_file

        with local_file_path.open("rb") as f:
            meta = dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))

            return meta
    except Exception as e:
        print('Error uploading file to Dropbox: ' + str(e))


def dropbox_upload_binary_file(binary_file, dropbox_file_path, dropbox_token=DROPBOX_ACCESS_TOKEN):
    try:
        dbx = dropbox_connect(dropbox_token=dropbox_token)
        meta = dbx.files_upload(binary_file.read(), f"/{dropbox_file_path}", mode=dropbox.files.WriteMode("overwrite"))

        return meta
    except Exception as e:
        print('Error uploading file to Dropbox: ' + str(e))

def dropbox_get_link(dropbox_token=DROPBOX_ACCESS_TOKEN):
    print(dropbox_token)
    links = []
    dbx = dropbox_connect(dropbox_token=dropbox_token)
    files = dropbox_list_files(dropbox_token=dropbox_token)
    for file in files:
        try:
            shared_link_metadata = dbx.sharing_create_shared_link_with_settings(file.path_display)
            shared_link = (shared_link_metadata.url).replace('?dl=0', '?dl=1')
            links.append(dict(name=file.path_display[1:], link=shared_link))
        except dropbox.exceptions.ApiError as exception:
            if exception.error.is_shared_link_already_exists():
                shared_link_metadata = dbx.sharing_get_shared_links(file.path_display)
                shared_link = (shared_link_metadata.links[0].url).replace('?dl=0', '?dl=1')
                links.append(dict(name=file.path_display[1:], link=shared_link))
    return links