from pydantic import BaseModel
from functools import wraps
from typing import Optional


class Settings(BaseModel):
    history: list[dict[str, str]]
    prompt: str
    model_temperature: float
    history_size: int


class OSettings(BaseModel):
    history: Optional[list[dict[str, str]]] = None
    prompt: Optional[str] = None
    model_temperature: Optional[float] = None
    history_size: Optional[int] = None


class User(BaseModel):
    id: int
    username: str
    first_name: str
    settings: Optional[OSettings] = None


class OUser(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    settings: Optional[OSettings] = None


class UserQuery(BaseModel):
    id: int
    query: str
