import asyncio
from fastapi import APIRouter, Request
from services.drive_db import db_drive_synchronization
from log import logger

router = APIRouter()


@router.post("/events/")
async def event_handler(event: Request):
    logger.debug(
        f"Handling event from channel {event.headers.get('x-goog-channel-id')}")
    asyncio.create_task(db_drive_synchronization(event))
    return {"succsess": True}
