from fastapi import APIRouter, Request
from services.drive import GDriveEventsManager
from os import getenv

router = APIRouter()


@router.post("/events/")
async def event_handler(event: Request):
    # print("I am in event_handler router", f"{event.__dict__=}")
    drive_manager = GDriveEventsManager()
    drive_manager.HANDLER.handle_event(headers=event.headers)
    return "A"
