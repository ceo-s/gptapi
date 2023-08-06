import uvicorn
from fastapi import FastAPI

from drive import GDrive
from static import register_staticfiles
from routes import register_routers

app = FastAPI()
register_staticfiles(app=app)
register_routers(app=app)

# drive = GDrive("1f7o4aD60tka0ehhv4WuSaeQ-2Uy-mAN0")
# drive.get_basedir()

# drive.register_event_handler(
#     "https://7e9b-188-243-182-231.ngrok-free.app")

# if __name__ == '__main__':
#     uvicorn.run("app:main", host="127.0.0.1",
#                 port=8080, reload=True, workers=3)
