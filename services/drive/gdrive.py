from __future__ import print_function

import os.path
from enum import Enum

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/drive'
]

BASEDIR_ID = "1f7o4aD60tka0ehhv4WuSaeQ-2Uy-mAN0"


class GDrive:

    def __init__(self, root_dir_id: str = BASEDIR_ID) -> None:
        self.root_dir_id = root_dir_id
        self.creds = self.__init_creds()
        self.authorize()
        self.service = self.__init_service()

    def __del__(self):
        # self.service.channels().stop(body={"id": "1"})
        print("Deleting", self.__dict__)
        ...

    @staticmethod
    def __init_creds() -> Credentials:
        creds = None

        if os.path.exists('drive/token.json'):
            creds = Credentials.from_authorized_user_file(
                'drive/token.json', SCOPES)
        return creds

    def __init_service(self) -> Resource:
        service = build('drive', 'v3', credentials=self.creds)
        return service

    def authorize(self):
        creds = self.creds
        assert creds is self.creds
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'drive/credentials.json', SCOPES)
                creds = flow.run_local_server(port=8000)

            with open('drive/token.json', 'w') as token:
                token.write(creds.to_json())

    def get_basedir(self):
        try:
            basedir = self.service.files().get(fileId=self.root_dir_id).execute()
            print("BASEDIR", basedir)
            folders = self.service.files().list(
                q=f"'{self.root_dir_id}' in parents").execute()

            print(folders)

        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')

    def mkdir(self, name: str, parent_folder: str = None):
        if parent_folder is None:
            parent_folder = self.root_dir_id
        metadata = {'name': name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [parent_folder]}
        file = self.service.files().create(body=metadata, fields="id").execute()
        return file.get("id")

    def register_event_handler(self, url: str, file_id: str = None) -> None:
        if file_id is None:
            file_id = self.root_dir_id

        body = {'id': '2',
                'type': 'web_hook',
                'address': url}

        self.service.files().watch(fileId=file_id, body=body).execute()


def main():

    drive = GDrive(BASEDIR_ID)
    drive.get_basedir()
    # drive.register_event_handler()
    print(drive.mkdir("ja-ja"))


if __name__ == '__main__':
    main()
