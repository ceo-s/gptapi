from __future__ import print_function

from os import path, getenv
from typing import Literal, Self
from uuid import uuid4
from enum import Enum
from asyncio import sleep

# from google.auth.transport._aiohttp_requests import Request
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
# If modifying these scopes, delete the file token.json.


class GDriveAuth:
    SCOPES = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.activity',
    ]

    __CREDS = path.join("services", "drive", "credentials.json")
    __TOKEN = path.join("services", "drive", "token.json")

    def __init__(self) -> None:
        self._creds = self.__init_creds()
        self.__authorize()
        self._service = self.__init_service()

    @classmethod
    def __init_creds(cls) -> Credentials:
        creds = None

        if path.exists(cls.__TOKEN):
            creds = Credentials.from_authorized_user_file(
                cls.__TOKEN, cls.SCOPES)
        return creds

    def __init_service(self) -> Resource:
        service = build('drive', 'v3', credentials=self._creds)
        return service

    def __authorize(self):
        creds = self._creds
        assert creds is self._creds
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.__CREDS, self.SCOPES)
                creds = flow.run_local_server(port=8080)

            with open(self.__TOKEN, 'w') as token:
                token.write(creds.to_json())


class GDrive(GDriveAuth):

    def share_dir(self, dir_id: str, permissions: Literal["owner", "organizer", "fileOrganizer", "writer", "commenter", "reader"]):
        permission = {
            'type': 'anyone',
            'role': permissions,
        }
        try:
            self._service.permissions().create(
                fileId=dir_id, body=permission, fields='id').execute()
        except HttpError as error:
            print(f'An error occurred: {error}')

    def listdir(self, dir_id: str):
        try:
            files = self._service.files().list(
                q=f"'{dir_id}' in parents").execute()

            print(files)

        except HttpError as error:
            print(f'An error occurred: {error}')

        return files

    def mkdir(self, name: str, parent_folder: str = None):
        metadata = {'name': name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'type': 'anyone',
                    'role': 'writer',
                    }
        if parent_folder is not None:
            metadata["parents"] = [parent_folder]

        try:
            file = self._service.files().create(body=metadata, fields="id",
                                                supportsAllDrives=True).execute()

        except HttpError as error:
            print(f'An error occurred: {error}')

        return file.get("id")

    def __get_dir_id(self, dirname: str):
        try:
            folder = self._service.files().list(
                q=f"'{self.BASEDIR_ID}' in parents and name = '{dirname}'").execute()
            print("THIS IS FOLDER", folder)
        except HttpError as error:
            print(f'An error occurred: {error}')

        file = folder.get("files")[0]

        return file.get("id")

    def register_event_handler(self, url: str) -> None:

        body = {
            'id': '5',
            'type': 'web_hook',
            'address': url,
            'expiration': 604_800_000
        }

        self._service.files().watch(
            fileId='1BEq3UQKUC8LueT5xIxZLBKdGKq9aMQJe', body=body).execute()


class GDriveEventsPoller:
    __SELF = None
    __DRIVE = GDrive

    def __new__(cls) -> Self:
        if cls.__SELF is not None:
            return cls.__SELF
        return cls()

    def __init__(self) -> None:
        self.hanler_address = "https://babyfalcon.ru/drive/events/"
        self.start_page_token = self.__init_start_page_token()
        self.__channel = {}

    async def start_polling(self):

        while True:
            self.register_event_handler()
            await sleep(self.__channel["expiration"])

    def delete_channel(self):
        self.__DRIVE()._service.channels().stop(body=self.__channel)

    def __init_start_page_token(self):
        token = self.__DRIVE()._service.changes().getStartPageToken().execute()
        return token["startPageToken"]

    def register_event_handler(self) -> None:
        drive = self.__DRIVE()
        body = {
            'id': uuid4(),
            'type': 'web_hook',
            'expiration': 604_800_000,
            'pageToken': self.start_page_token,
            'address': self.hanler_address,
        }

        self.__channel = drive._service.changes().watch(body=body).execute()


class GDriveEventsHandler:

    __DRIVE = GDrive

    class GoogleEventHeaders(Enum):
        Channel_ID = "X-Goog-Channel-ID"
        Channel_Token = "X-Goog-Channel-Token"
        Channel_Expiration = "X-Goog-Channel-Expiration"
        Resource_ID = "X-Goog-Resource-ID"
        Resource_URI = "X-Goog-Resource-URI"
        Resource_State = "X-Goog-Resource-State"
        Changed = "X-Goog-Changed"
        Message_Number = "X-Goog-Message-Number"

    class ResourceStates(Enum):
        SYNC = "sync"
        ADD = "add"
        REMOVE = "remove"
        UPDATE = "update"
        TRASH = "trash"
        UNTRASH = "untrash"
        CHANGE = "change"

    class UpdateType(Enum):
        CONTENT = "content"
        PROPERTIES = "properties"
        PARENTS = "parents"
        CHILDREN = "children"
        PERMISSIONS = "permissions"

    def handle_event(self, headers: dict):
        print(headers)


class GDriveEventsManager:

    def __init__(self) -> None:
        self.POLLER = GDriveEventsPoller()
        self.HANDLER = GDriveEventsHandler()


def main():

    drive = GDrive()
    drive.get_basedir()
    # drive.register_event_handler()
    print(drive.mkdir("ja-ja"))


if __name__ == '__main__':
    main()
