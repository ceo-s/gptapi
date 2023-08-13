from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from .user import User


class DocumentMetadata(BaseModel):
    name: Optional[str] = None
    token_cost: Optional[int] = None


class Document(BaseModel):
    embedding: Optional[list[float]] = None
    metadata_: Optional[DocumentMetadata] = None
    date_creation: Optional[datetime] = None
    date_update: Optional[datetime] = None


class Collection(BaseModel):
    user: Optional[User] = None
    documents: Optional[list[Document]] = None
