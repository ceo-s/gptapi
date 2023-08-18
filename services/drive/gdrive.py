from __future__ import print_function

import requests
from os import path, getenv
from pprint import pp
from typing import Literal

# from google.auth.transport._aiohttp_requests import Request
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
# If modifying these scopes, delete the file token.json.


class GDrive:

    SCOPES = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.activity',
    ]

    __CREDS = path.join("services", "drive", "credentials.json")
    __TOKEN = path.join("services", "drive", "token.json")

    def __init__(self) -> None:
        self.creds = self.__init_creds()
        self.__authorize()
        self.service = self.__init_service()

    def __del__(self):
        print("Deleting", self.__dict__)
        ...

    @classmethod
    def __init_creds(cls) -> Credentials:
        creds = None

        if path.exists(cls.__TOKEN):
            creds = Credentials.from_authorized_user_file(
                cls.__TOKEN, cls.SCOPES)
        return creds

    def __init_service(self) -> Resource:
        service = build('drive', 'v3', credentials=self.creds)
        return service

    def __authorize(self):
        creds = self.creds
        assert creds is self.creds
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.__CREDS, self.SCOPES)
                creds = flow.run_local_server(port=8080)

            with open(self.__TOKEN, 'w') as token:
                token.write(creds.to_json())

    def share_dir(self, dir_id: str, permissions: Literal["owner", "organizer", "fileOrganizer", "writer", "commenter", "reader"]):
        permission = {
            'type': 'anyone',
            'role': permissions,
        }
        try:
            self.service.permissions().create(
                fileId=dir_id, body=permission, fields='id').execute()
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')

    def listdir(self, dir_id: str):
        try:
            # basedir = self.service.files().get(fileId=self.BASEDIR_ID).execute()
            # print("BASEDIR", basedir)
            folders = self.service.files().list(
                q=f"'{dir_id}' in parents").execute()

            print(folders)

        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')

    def mkdir(self, name: str, parent_folder: str = None):
        metadata = {'name': name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'type': 'anyone',
                    'role': 'writer',
                    }
        if parent_folder is not None:
            metadata["parents"] = [parent_folder]

        try:
            file = self.service.files().create(body=metadata, fields="id",
                                               supportsAllDrives=True).execute()

        except HttpError as error:
            print(f'An error occurred: {error}')
        print(f"{file=}")
        return file.get("id")

    def __get_dir_id(self, dirname: str):
        try:
            folder = self.service.files().list(
                q=f"'{self.BASEDIR_ID}' in parents and name = '{dirname}'").execute()
            print("THIS IS FOLDER", folder)
        except HttpError as error:
            print(f'An error occurred: {error}')

        file = folder.get("files")[0]

        return file.get("id")

    # def listdir(self, dirname: str):
    #     dir_id = self.__get_dir_id(dirname)
    #     try:
    #         files = self.service.files().list(
    #             q=f"'{dir_id}' in parents").execute()

    #     except HttpError as error:
    #         print(f'An error occurred: {error}')

    #     print(files)
    #     return files.get("files")

#    def register_event_handler(self, url: str) -> None:
#        headers = {
#                'Authorization': f'Bearer {self.creds.token}',
#                'Accept': 'application/json',
#                  }
#        body = {
#                'id': '5',
#                'type': 'web_hook',
#                'address': f'{url}',
#               }
#        
#        key = getenv("GDRIVE_API_KEY")
#        params = {"key": key}
#        print("KEY", key)
#        response = requests.post('https://www.googleapis.com/drive/v3/files/root/watch', params=params, headers=headers, json=body)
#        print(self.creds.__dict__)
#        print(self.creds.token)
#        print(response)
#        print(response.status_code)
#        print(response.json())
#        resp_headers = response.headers
#        dct_key = "resourceUri"
#        print("URI", resp_headers.get(dct_key))





    def register_event_handler(self, url: str) -> None:

        token = self.service.changes().getStartPageToken().execute()
        body = {'id': '6',
                'type': 'web_hook',
                'address': url,
                }
        #print("THIS IS YOUR FUCKING TOKEN BITCH", token)
        key = getenv("GDRIVE_API_KEY")
        print("KEY", key)

        #self.service.files().watch(fileId='root', key=key, body=body).execute()
        self.service.changes().watch(body=body, pageToken=token["startPageToken"]).execute()

    # def check_updates(self):
    #     try:
    #         service = build('driveactivity', 'v2', credentials=self.creds)
    #         results = service.activity().query(body={
    #             'pageSize': 10
    #         }).execute()
    #         print("LEN ACTIVITIES")
    #         print(len(results["activities"]))
    #         print("LAST UPDATE")
    #         pp(results["activities"][0])

    #     except HttpError as error:
    #         print(f'An error occurred: {error}')


def main():

    drive = GDrive()
    drive.get_basedir()
    # drive.register_event_handler()
    print(drive.mkdir("ja-ja"))


if __name__ == '__main__':
    main()
