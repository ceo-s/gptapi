from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class GDriveEvent(BaseModel):
    kind: str
    id: str
    resourceId: str
    resourceUri: str
    token: str
    expiration: str


@router.post("/events/")
async def event_handler(event: GDriveEvent):
    print("HERE WE GO", event)
    return "A"
