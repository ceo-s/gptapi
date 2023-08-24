import uvicorn
from fastapi import FastAPI
from os import getenv
from contextlib import asynccontextmanager

from services.drive import GDriveEventsManager
from static import register_staticfiles
from routes import register_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("this is lifespan start")
    drive_manager = GDriveEventsManager()
    await drive_manager.POLLER.start_polling()

    yield
    drive_manager.POLLER.delete_channel()
    print("this is lifespan end")


app = FastAPI(lifespan=lifespan)
register_staticfiles(app=app)
register_routers(app=app)

# if __name__ == '__main__':
#     uvicorn.run("app:main", host="0.0.0.0",
#                 port=8080, reload=True)
