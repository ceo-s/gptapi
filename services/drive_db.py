from fastapi import Request

from .drive import GDriveEventsManager, GDrive
from .db import UserCollection


async def db_drive_synchronization(event: Request):

    manager = GDriveEventsManager()
    changes_mapping = await manager.HANDLER.handle_event(headers=event.headers)
    if changes_mapping is None:
        return

    for file_id, file in changes_mapping.items():
       # if file.fileExtension == "txt":
       #     txt_file = file
       #     break
       print(file)
    
    # drive = GDrive()
    # content = drive.get_file_content(txt_file.id, txt_file.mimeType)
    
    # print(txt_file)
    # print(content)
