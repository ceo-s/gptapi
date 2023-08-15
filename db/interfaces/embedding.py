from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from .user import User


class DocumentMetadata(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None
    description: Optional[str] = None
    token_cost: Optional[int] = None
    date_creation: Optional[datetime] = None
    date_update: Optional[datetime] = None


class Document(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    file_id: Optional[str] = None
    embedding: Optional[list[float]] = None
    metadata: Optional[DocumentMetadata] = Field(
        default=None, alias="metadata_")

    def __str__(self) -> str:
        return f"Document <{self.metadata.name}>"

    def __repr__(self) -> str:
        return f"Document <{self.metadata.name}>"


class Collection(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user: Optional[User] = None
    documents: Optional[list[Document]] = None
