from typing import overload, Any, Never, NamedTuple
from enum import Enum
from functools import singledispatchmethod
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, bindparam, delete
from abc import ABC, abstractstaticmethod, abstractclassmethod, abstractmethod

from db import get_sessionmaker
from db.models import users as UM
from db.models import embeddings as EM
from db import interfaces as I
from ._interfaces import ICollection, IDocument, IDocumentMetadata
from openai import Embedding

from dotenv import load_dotenv
import openai
import os

load_dotenv(".env")

openai.api_key = os.getenv("OPENAI_API_KEY")

texts = [
    "Hello my name is Gustavo, but you can call me Gus.",
    "-Say my Name! -Heisenberg... -You are god damn right."
]

embedding = openai.Embedding.create(
    input=texts, model="text-embedding-ada-002")

for i in range(len(texts)):
    print(len(embedding["data"][i]["embedding"]))


class Embedder:
    @staticmethod
    async def text_to_embedding(text: str):
        print("CREATING EMBEDDING")
        # embedding = await Embedding.acreate(
        #     input=[text], model="text-embedding-ada-002")
        # print("AFTER EMBEDDING")
        # return embedding["data"][0]["embedding"]
        return [6.] * 1536


class DocumentStatus(Enum):
    CREATE = 1
    UPDATE = 2
    DELETE = 3


class BufferElement(NamedTuple):
    document: I.Document
    status: DocumentStatus

    def __str__(self):
        return f"({self.document} to {self.status.name})"

    def __repr__(self):
        return str(self)


class DocumentFactory:
    __embedder = Embedder

    def __init__(self):
        self.__user_id: int
        self._collection: EM.Collection
        # TODO: buffer in separate class
        self.__documents_buffer: list[BufferElement] = []

    def __buffer_append(self, document: I.Document, status: DocumentStatus):
        self.__documents_buffer.append(BufferElement(document, status))

    async def __create_document(self, text: str, metadata: I.DocumentMetadata):
        embedding = await self.__embedder.text_to_embedding(text)
        document = I.Document(embedding=embedding, metadata_=metadata)
        self.__buffer_append(document, DocumentStatus.CREATE)

    async def _document_from_metadata(self, text: str, metadata: I.DocumentMetadata):
        now = datetime.datetime.now()
        metadata.date_creation = now
        metadata.date_update = now
        await self.__create_document(text, metadata=metadata)
        # self.__documents_buffer.append(document)

    async def _document_from_params(self, text: str, file_id: str, name: str,
                                    description: str, token_cost: int):
        now = datetime.datetime.now()
        metadata = I.DocumentMetadata(
            file_id=file_id,
            name=name,
            description=description,
            token_cost=token_cost,
            date_creation=now,
            date_update=now,
        )
        await self.__create_document(text, metadata=metadata)
        # self.__documents_buffer.append(document)

    async def update_document(self):
        ...

    async def delete_document(self):
        ...

    async def __pydantic_to_orm(self, document: I.Document) -> EM.Document:
        doc = EM.Document()
        doc.embedding = document.embedding
        metadata = EM.DocumentMetadata()
        doc.metadata_ = metadata

        for attr in self.__documents_buffer[0].document.metadata.__fields__:
            setattr(doc.metadata_, attr, getattr(document.metadata, attr))
        return doc

    async def commit(self):
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            print(
                f"AAA {self.__documents_buffer[0].document.metadata.model_dump_json()}")
            print(f"{self._collection.documents=}")
            if self._collection.documents:
                db_session.add_all(self._collection.documents)
            # TODO: aiter
            for buff_el in self.__documents_buffer:
                match buff_el.status:
                    case DocumentStatus.CREATE:
                        doc = await self.__pydantic_to_orm(buff_el.document)
                        doc.collection = self._collection
                        db_session.add(doc)
                    case DocumentStatus.UPDATE:
                        doc = await self.__pydantic_to_orm(buff_el.document)
                        doc.collection = self._collection
                        doc.metadata_.date_update = datetime.datetime.now()
                        db_session.add(doc)
                    case DocumentStatus.DELETE:
                        db_session.delete(buff_el.document)
            #             await self.__delete_document()

            # db_session.delete()
            #     # document = EM.Document()

            # await db_session.execute(
            #     update(UM.User)
            #     .where(UM.User.id. == user.id)
            #     .values(values_to_change)
            # )


class UserCollection(DocumentFactory):

    @classmethod
    async def from_user(cls, __user_id: int):
        self = cls()
        self.__user_id = __user_id
        self._collection = await self.__get_collection(__user_id)
        # self.collection = CollectionAdapter()

        return self

    @overload
    async def add_document(
        self, __text: str, metadata: I.DocumentMetadata): ...

    @overload
    async def add_document(self, __text: str, file_id: str, name: str,
                           description: str, token_cost: int): ...

    async def add_document(self, *args, **kwargs):
        metadata = kwargs.get("metadata")
        if metadata:
            await super()._document_from_metadata(args[0], metadata)
        else:
            await super()._document_from_params(text=args[0], **kwargs)

    async def __get_collection(self, __user_id: int):
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            res = await db_session.execute(
                select(EM.Collection)
                .where(EM.Collection.user_fk == __user_id)
            )

            collection = res.unique().scalar_one_or_none()

            db_session.expunge_all()
            return collection


class _Embedder:
    async def __init__(self, text: str):
        result = await openai.Embedding.acreate(
            input=[text],
            model="text-embedding-ada-002"
        )

        self.embedding = result["data"][i]["embedding"]
        self.token_cost = result["usage"]["total_tokens"]


class _Document:

    def __init__(self, document: I.Document):
        self._document = document

    @classmethod
    async def _create(cls, text: str) -> "_Document":
        emb = _Embedder(text)
        time_now = datetime.datetime.now()
        metadata = I.DocumentMetadata(
            token_cost=emb.token_cost,
            date_creation=time_now,
            date_update=time_now,
        )

        document = I.Document(
            embedding=emb.embedding,
            metadata=metadata,
        )

        return cls.__init__(cls, document)

    async def _add_metadata(self, file_id: str, name: str, description: str | None):
        self._document.metadata.file_id = file_id
        self._document.metadata.name = name
        self._document.metadata.description = description


class _Collection:
    async def __init__(self, __collection: EM.Collection):
        self._id = __collection.id
        self.__collection_docs = __collection.documents
        self.__new_docs = []
        self.__del_docs = []
        self.__update_docs = []

    async def __get__(self) -> list[IDocument]:
        return self.__collection_docs

    async def __getitem__(self, __key: int) -> IDocument:
        return self.__collection_docs[__key]

    async def __delitem__(self, __key: str):
        self.__del_docs.append(self.__collection_docs[__key])
        del self.__collection_docs[__key]

    async def create_document(self, text: str, file_id: str, name: str, description: str) -> _Document:
        document = await _Document._create(text)
        document._add_metadata(
            file_id=file_id,
            name=name,
            description=description,
        )
        return document

    async def push(self, document: _Document):
        self.__collection_docs.append(document._document)
        self.__new_docs.append(document)

    async def pop(self, __index: int = None) -> None:
        if __index is None:
            __index = -1

        del self[__index]

    async def _remove(self, **kwargs: dict[str, str]):
        attr, value = next(iter(kwargs.values))
        for i, document in enumerate(self.__collection_docs):
            if getattr(document.metadata_, attr) == value:
                del self[i]
                break


# col = _Collection()

# class _Collection:
#     @overload
#     def __init__(self, __user: UM.User) -> None: ...
#     @overload
#     def __init__(self, __user_id: int) -> None: ...

#     def __init__(self, *args, **kwargs) -> None:
#         ...

#     @singledispatchmethod
#     async def _create(self, user: UM.User):
#         ...

#     @_create.register
#     async def _(self, user_id: int):
#         async with get_sessionmaker().begin() as db_session:
#             db_session: AsyncSession

#             collection = EM.Collection(
#                 user_fk=user_id
#             )
#             await db_session.merge(collection)
#             await db_session.refresh(collection)
#             await db_session.expunge_all()
#             return collection

#     @_create.register
#     async def _(self, user: UM.User):
#         async with get_sessionmaker().begin() as db_session:
#             db_session: AsyncSession

#             collection = EM.Collection(
#                 user=user
#             )
#             # TODO : DRY ?
#             await db_session.merge(collection)
#             await db_session.refresh(collection)
#             await db_session.expunge_all()
#             return collection

#     @singledispatchmethod
#     async def _get():
#         ...

#     @_get.register
#     async def _(user_id: int):
#         ...

#     @_get.register
#     async def _(user: UM.User):
#         ...

#     async def add_documents():
#         ...

#     async def get_documents():
#         ...


# class _Embedder:
#     ...


# class _Document:

#     async def create():
#         ...
