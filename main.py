import uvicorn
from fastapi import FastAPI
from os import getenv
from contextlib import asynccontextmanager

from services.drive import GDriveEventsManager
from static import register_staticfiles
from routes import register_routers


@asynccontextmanager
async def lifespan():
    drive_manager = GDriveEventsManager()
    await drive_manager.POLLER.start_polling()
    print("this is lifespan start")
    print("this is pointer of poller in lifespan", id(drive_manager.POLLER))
    yield
    drive_manager.POLLER.delete_channel()
    print("this is lifespan end")


app = FastAPI(lifespan=lifespan)
register_staticfiles(app=app)
register_routers(app=app)

# drive.register_event_handler("https://babyfalcon.ru/drive/events/")

# drive.register_event_handler(
#     "https://7e9b-188-243-182-231.ngrok-free.app")

# if __name__ == '__main__':
#     uvicorn.run("app:main", host="0.0.0.0",
#                 port=8080, reload=True)
