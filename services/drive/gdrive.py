from __future__ import print_function

from os import path, getenv
from typing import Any, Literal, Self
from uuid import uuid4
from enum import Enum
import asyncio
from datetime import timedelta, datetime
from functools import wraps
from db import interfaces as I

# from google.auth.transport._aiohttp_requests import Request
from google.auth.transport.requests import Request, AuthorizedSession
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


class GDriveEventsPoller:

    __SELF: "GDriveEventsPoller" = None
    __DRIVE = GDrive

    def __new__(cls) -> Self:
        if cls.__SELF is not None:
            return cls.__SELF
        return super().__new__(cls)

    def __init__(self) -> None:
        self.hanler_address = "https://babyfalcon.ru/drive/events/"
        self.start_page_token = self.__init_start_page_token()
        self.__channel = {}

    async def start_polling(self):

        # while True:
        self.register_event_handler()
#            await sleep(timedelta(weeks=1).total_seconds())

    def delete_channel(self):
        print("deleting channel", self.__channel)
        self.__DRIVE()._service.channels().stop(body=self.__channel).execute()

    def __init_start_page_token(self):
        token = self.__DRIVE()._service.changes().getStartPageToken().execute()
        return token["startPageToken"]

    def register_event_handler(self) -> None:
        drive = self.__DRIVE()
        body = {
            'id': str(uuid4()),
            'type': 'web_hook',
            'expiration': self.get_expiration_time(),
            'address': self.hanler_address,
        }

        self.__channel = drive._service.changes().watch(
            pageToken=self.start_page_token, body=body).execute()

#    def get_expiration_time(self):
#        ttl = duration_pb2.Duration()
#        ttl.seconds = int(timedelta(weeks=1).total_seconds())
#        return ttl

    def get_expiration_time(self):
        datetime_expiration = datetime.now() + timedelta(weeks=1)
        return int(datetime.timestamp(datetime_expiration)*1000)


class GDriveEventProcesser:

    def _map_changes(self, changes: list[dict]) -> dict[str, I.File]:
        changes_mapping = {}

        for change in changes:
            fileId = change["fileId"]
            file = I.File.model_validate(change["file"])

            changes_mapping[fileId] = file

        return changes_mapping

    def _get_trashed(self, mapping: dict):
        return tuple(filter(lambda items: items[1]["trashed"] == True, mapping.items()))

    def _set_parents_folders(self):

        ...


class GDriveEventsHandler(GDriveEventProcesser):

    __SELF: "GDriveEventsHandler" = None
    __DRIVE = GDrive

    class Headers(Enum):
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

    def __new__(cls) -> Self:
        print("I am in new method and this is __SELF=", cls.__SELF)
        if cls.__SELF is None:
            cls.__SELF = super().__new__(cls)
            cls.__SELF.__task: asyncio.Task | None = None
            cls.__SELF.__resource_uris = set()
        return cls.__SELF

    # def __init__(self) -> None:
        # print(f"\033[93mI am in init of so called singelton{id(self)}\033[0m")

    def __process_event(self):
        print("\033[93mstart to proceed\033[0m")
        drive = self.__DRIVE()
        session = AuthorizedSession(drive._creds)
        changes: list[dict] = []

        fields = f'nextPageToken,newStartPageToken,changes(fileId,kind,removed,file(name,mimeType,parents,id,description,trashed,webContentLink,fileExtension))'

        for uri in self.__resource_uris:
            # print(f"{uri}&fields={fields}")
            resp = session.get(f"{uri}&fields={fields}")
            # print(f"{resp.json()=}")
            changes += resp.json()["changes"]

        # print(f"{changes=}")
        mapping = self._map_changes(changes)
        trashed_files = self._get_trashed(mapping)
        return mapping

    # def __process_event(self, headers: dict):

    #     if headers[self.Headers.Resource_State.value] == self.ResourceStates.SYNC.value:
    #         return
    #     drive = self.__DRIVE()
    #     session = AuthorizedSession(drive._creds)
    #     resp = session.get(headers[self.Headers.Resource_URI.value])
    #     print(headers)
    #     print(resp.json())
    #     print(len(resp.json()["changes"]))
    #     last = resp.json()["changes"][-1]
    #     print("Last change -->", last)
    #     fields = 'kind,id,name,mimeType,description,trashed,parents'
    #     fields = '*'
    #     resp2 = session.get(
    #         f"https://www.googleapis.com/drive/v3/files/{last['file']['id']}?fields={fields}")

    #     print(resp2.json())
    # 'https://www.googleapis.com/drive/v3/changes?alt=json&pageToken=232'
    # 'https://www.googleapis.com/drive/v3/changes?alt=json&pageToken=232'

    async def __handle_event(self):
        print("in __handle_event")
        await asyncio.sleep(7)
        return self.__process_event()

    async def handle_event(self, headers: dict):

        if headers[self.Headers.Resource_State.value] == self.ResourceStates.SYNC.value:
            return

        if self.__task is not None:
            print("\033[93mCanceling task\033[0m")
            self.__task.cancel()

        self.__task = asyncio.create_task(self.__handle_event())
        self.__resource_uris.add(headers[self.Headers.Resource_URI.value])
        print("Awaiting task")
        return await self.__task


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
