from fastapi import APIRouter, Request
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
async def event_handler(event: Request):
    #print("HERE WE GO", event.__dict__)
    print("HERE WE GO", event.headers)
    print("HERE WE GO, BODY", await event.body())
    return "A"
