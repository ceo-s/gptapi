from fastapi import APIRouter, Request
from pydantic import BaseModel
import requests
from services.drive.gdrive import GDrive
from os import getenv

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
    print(uri:=event.headers.get("x-goog-resource-uri"))
    creds = GDrive().creds
    headers = {
                'Authorization': f'Bearer {creds.token}',
                'Accept': 'application/json',
              }
    key = getenv("GDRIVE_API_KEY")
    params = {"key": key}
    resp = requests.get(uri, params=params, headers=headers)
    print(resp)
    print(resp.json())
    print("HERE WE GO, BODY", await event.body())
    return "A"
