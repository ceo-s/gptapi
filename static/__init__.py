from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def register_staticfiles(app: FastAPI):
    app.mount("/static", StaticFiles(directory="static"), name="static")
