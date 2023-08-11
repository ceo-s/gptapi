from fastapi import FastAPI
from importlib import import_module

ROUTES = [
    ("base", ""),
    ("gpt", "/gpt"),
    ("db_routes", "/db"),
    ("drive", "/drive"),
    ("pages", "/pages"),
]


def register_routers(app: FastAPI) -> None:
    for module_conf in ROUTES:
        module = import_module("." + module_conf[0], "routes")
        app.include_router(module.router, prefix=module_conf[1])
