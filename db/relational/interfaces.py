from pydantic import BaseModel
from functools import wraps
from typing import Optional


# def optional(cls) -> callable:

#     @wraps(cls, updated=())
#     class OptionalCopy(cls):
#         ...

#     for field in OptionalCopy.__fields__.values():
#         field.required = False

#     return OptionalCopy


class Settings(BaseModel):
    history: list[dict[str, str]]
    prompt: str
    model_temperature: float
    history_size: int


class OSettings(BaseModel):
    history: Optional[list[dict[str, str]]]
    prompt: Optional[str]
    model_temperature: Optional[float]
    history_size: Optional[int]


class User(BaseModel):
    id: int
    username: str
    first_name: str
    settings: Optional[OSettings]


class OUser(BaseModel):
    id: Optional[int]
    username: Optional[str]
    first_name: Optional[str]
    settings: Optional[OSettings]


class UserQuery(BaseModel):
    id: int
    query: str
