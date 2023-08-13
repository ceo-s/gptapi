from pydantic import BaseModel, ConfigDict, Field
from functools import wraps
from typing import Optional


class Settings(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    history: list[dict[str, str]]
    prompt: str
    model_temperature: float
    history_size: int


class OSettings(BaseModel):
    history: Optional[list[dict[str, str]]] = None
    prompt: Optional[str] = None
    model_temperature: Optional[float] = None
    history_size: Optional[int] = None


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    first_name: str


class User(BaseUser):
    settings: Optional[OSettings] = None


class OUser(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    settings: Optional[OSettings] = None


class UserQuery(BaseModel):
    id: int
    query: str
