from fastapi import Request

from .drive import GDriveEventsManager
from .db import UserCollection


async def db_drive_synchronization(event: Request):

    manager = GDriveEventsManager()
    changes_mapping = await manager.HANDLER.handle_event(headers=event.headers)

    for file_id, file in changes_mapping.items():
        if file["fileExtension"] == "txt":
            txt_file = file
            break

    print(txt_file)
