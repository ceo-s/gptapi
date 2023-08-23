from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Literal
from enum import Enum


class MimeTypes(Enum):

    TXT = "text/plain"


class File(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    mimeType: str
    trashed: bool
    fileExtension: Optional[str] = None
    parents: list[str]

    def __str__(self) -> str:
        return "FILE --> " + str([f"{field}={getattr(self, field)}" for field in self.__fields__])

    def __repr__(self) -> str:
        return str(self)
