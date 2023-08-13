from typing import overload, Any, Never
from functools import singledispatchmethod
import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, bindparam, delete
from abc import ABC, abstractstaticmethod, abstractclassmethod, abstractmethod

from db import get_sessionmaker
from db.models import users as UM
from db.models import embeddings as EM
from db import interfaces as I
from ._embedding import _Collection
from ._interfaces import ICollection, IDocument, IDocumentMetadata


class Collection(_Collection, ICollection):

    def __init__(self) -> None:
        self.__colection = I.Collection()

    def push(self): ...

    def pop(self): ...


Collection().create()
