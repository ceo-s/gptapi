import uvicorn
from fastapi import FastAPI
from os import getenv

from services.drive import GDrive
from static import register_staticfiles
from routes import register_routers

app = FastAPI()
register_staticfiles(app=app)
register_routers(app=app)

#drive = GDrive()
#drive.register_event_handler("https://babyfalcon.ru/drive/events/")

# drive.register_event_handler(
#     "https://7e9b-188-243-182-231.ngrok-free.app")

# if __name__ == '__main__':
#     uvicorn.run("app:main", host="0.0.0.0",
#                 port=8080, reload=True)
