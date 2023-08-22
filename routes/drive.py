from fastapi import APIRouter, Request
from services.drive import GDriveEventsManager
from os import getenv
from asyncio import CancelledError

router = APIRouter()


@router.post("/events/")
async def event_handler(event: Request):
    # print("I am in event_handler router", f"{event.__dict__=}")
    drive_manager = GDriveEventsManager()
    try:
        await drive_manager.HANDLER.handle_event(headers=event.headers)

    except CancelledError:
        print("Debounce did its stuff right here nigga")

    return "A"
