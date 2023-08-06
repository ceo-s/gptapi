import os
from typing import Literal, TypedDict
from enum import Enum
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

DIRS = Literal[
    "bot_webapps",
    "someotherdir",
]

BOT_WEBAPPS_VIEWS = Literal[
    "history",
    "temperature",
]

SOMEOTHERDIR_VIEWS = Literal[
    "dir",
]

DIRS_MAPPING: dict[str, Literal] = {
    "bot_webapps": BOT_WEBAPPS_VIEWS,
    "someotherdir": SOMEOTHERDIR_VIEWS,
}


def get_page(dirname: DIRS, view: BOT_WEBAPPS_VIEWS, **params) -> HTMLResponse:
    path = os.path.join("views", dirname, view, "index.html")
    with open(path, "r") as file:
        html = file.read().format(**params)
    return HTMLResponse(content=html)
