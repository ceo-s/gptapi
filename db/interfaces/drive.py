from pydantic import BaseModel, Field
from typing import Optional
from io import BytesIO


class File(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    mime_type: str = Field(alias="mimeType")
    trashed: bool
    file_extension: Optional[str] = Field(default=None, alias="fileExtension")
    parents: list[str]

    content: Optional[BytesIO] = None

    def __str__(self) -> str:
        return "FILE --> " + str([f"{field}={getattr(self, field)}" for field in self.__fields__])

    def __repr__(self) -> str:
        return str(self)
