from fastapi import APIRouter, Request
from services.drive import GDriveEventsManager
from os import getenv
from asyncio import CancelledError, create_task

router = APIRouter()


@router.post("/events/")
async def event_handler(event: Request):
    # print("I am in event_handler router", f"{event.__dict__=}")
    drive_manager = GDriveEventsManager()
    task = create_task(drive_manager.HANDLER.handle_event(headers=event.headers))

    print("SENDING A RESPONSE")
    return "A"
