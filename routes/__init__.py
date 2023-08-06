from fastapi import FastAPI
from .base import router as BaseRouter
from .bot import router as BotRouter
from .drive import router as DriveRouter


def register_routers(app: FastAPI):
    app.include_router(BaseRouter)
    app.include_router(BotRouter, prefix="/bot")
    app.include_router(DriveRouter, prefix="/drive")
