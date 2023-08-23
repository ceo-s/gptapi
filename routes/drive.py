from fastapi import APIRouter, Request
from services.drive import GDriveEventsManager
from services.drive_db import db_drive_synchronization
from os import getenv
from asyncio import CancelledError, create_task

router = APIRouter()


@router.post("/events/")
async def event_handler(event: Request):
    print("I am in event_handler router")
    task = create_task(db_drive_synchronization(event))
    print("SENDING A RESPONSE")
    return "A"
