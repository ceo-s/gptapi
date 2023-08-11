from fastapi.responses import HTMLResponse
from typing import Literal
from os import path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def register_staticfiles(app: FastAPI):
    app.mount("/static", StaticFiles(directory="static"), name="static")


DIRS = Literal[
    "bot_webapps",
]

BOT_WEBAPPS_VIEWS = Literal[
    "history",
    "history_menu",
    "change_history_limit",
    "temperature",
]


# TODO: is it blocking? aiofiles??

def get_page(dirname: DIRS, view: BOT_WEBAPPS_VIEWS, user_id: int, **params) -> HTMLResponse:
    dir_path = path.join("static", dirname, view)

    with open(path.join(dir_path, "index.html"), "r") as page:
        body = page.read().format(
            user_id=user_id,
            **params)

    with open(path.join("static", dirname, "template.html"), "r") as template:
        html = template.read().format(
            js=path.join(dir_path, "index.js"),
            css=path.join(dir_path, "styles.css"),
            user_id=user_id,
            body=body
        )

    return HTMLResponse(content=html)
