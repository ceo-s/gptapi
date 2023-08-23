from fastapi import Request

from .drive import GDriveEventsManager
from .db import UserDrive


async def db_drive_synchronization(self, event: Request):

    manager = GDriveEventsManager()
    changes = await manager.HANDLER.handle_event(headers=event.headers)

    drive = UserDrive()
