from typing import Literal, overload, Type, NamedTuple, Optional
from enum import Enum
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from db import get_sessionmaker
from db.models import users as UM
from db.models import embeddings as EM
from db import interfaces as I
from .._interfaces import IOptimizer, IEmbedder, IDocument
# from ..llm.preprocessing import Embedder


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


# BUG: not sure, but this can lead to unexpected results cause, idk, maybe
# class DocumentUpdator:

#     def __init__(self, __document: EM.Document):
#         self.__document = __document

#     async def __aenter__(self) -> IDocument:
#         return self.__document

#     async def __aexit__(self, exc_type, exc_value, traceback):
#         self.__document.metadata_.date_update = datetime.datetime.now()


# class DocumentFactory:

#     def __init__(self):
#         self.__user_id: int
#         self.__embedder: IEmbedder
#         self._collection: EM.Collection
#         # TODO: buffer in separate class
#         self.__documents_buffer: list[BufferElement] = []

#     async def _ainit(self, __user_id, __embedder):
#         self._collection = await self.__get_collection(__user_id)
#         self.__embedder = __embedder

#     async def __get_collection(self, __user_id: int):
#         async with get_sessionmaker().begin() as db_session:
#             db_session: AsyncSession
#             res = await db_session.execute(
#                 select(EM.Collection)
#                 .where(EM.Collection.user_fk == __user_id)
#             )

#             collection = res.unique().scalar_one_or_none()

#             db_session.expunge_all()
#             return collection

#     def __buffer_append(self, document: I.Document, status: DocumentStatus):
#         self.__documents_buffer.append(BufferElement(document, status))

#     async def __create_document(self, file_id: str, text: str, metadata: I.DocumentMetadata):
#         embeddings = await self.__embedder.text_to_embeddings(text)
#         print(f"BEFORE APPEND {self.__documents_buffer}")
#         print("IM HERE")
#         print(f"{len(embeddings)=}")
#         for embedding in embeddings:
#             document = I.Document(
#                 file_id=file_id, text="A", embedding=embedding, metadata_=metadata)
#             self.__buffer_append(document, DocumentStatus.CREATE)
#         print(f"AFTER APPEND {self.__documents_buffer}")

#     # async def generate_document_from_metadata(self, file_id: str, text: str, metadata: I.DocumentMetadata) -> I.Document:
#     #     now = datetime.datetime.now()
#     #     metadata.date_creation = now
#     #     metadata.date_update = now
#     #     embedding = await self.__embedder.text_to_embedding(text)
#     #     document = I.Document(embedding=embedding, metadata_=metadata)
#     #     return document

#     async def _document_from_metadata(self, file_id: str, text: str, metadata: I.DocumentMetadata):
#         now = datetime.datetime.now()
#         metadata.date_creation = now
#         metadata.date_update = now
#         await self.__create_document(file_id, text, metadata=metadata)

#     async def _document_from_params(self, file_id: str, text: str, name: str,
#                                     description: str, token_cost: int):
#         now = datetime.datetime.now()
#         metadata = I.DocumentMetadata(
#             name=name,
#             description=description,
#             token_cost=token_cost,
#             date_creation=now,
#             date_update=now,
#         )
#         await self.__create_document(file_id, text, metadata=metadata)

#     def __find_document(self, file_id: str) -> EM.Document:
#         documents = list(filter(lambda x: x.file_id ==
#                                 file_id, self._collection.documents))
#         print(" IN __find_document", documents)

#         return documents[0]

#     def update_document(self, file_id: str) -> DocumentUpdator:
#         document = self.__find_document(file_id)
#         return DocumentUpdator(document)

#     async def delete_document(self, file_id: str):
#         document = self.__find_document(file_id)
#         self.__buffer_append(document, DocumentStatus.DELETE)

#     async def __pydantic_to_orm(self, __document: I.Document) -> EM.Document:
#         document = EM.Document()
#         document.file_id = __document.file_id
#         document.embedding = __document.embedding
#         document.text = __document.text
#         metadata = EM.DocumentMetadata()
#         document.metadata_ = metadata

#         for attr in self.__documents_buffer[0].document.metadata.__fields__:
#             setattr(document.metadata_, attr,
#                     getattr(__document.metadata, attr))
#         return document

#     async def commit(self):
#         async with get_sessionmaker().begin() as db_session:
#             db_session: AsyncSession

#             print(f"{self._collection.documents=}")
#             if self._collection.documents:
#                 db_session.add_all(self._collection.documents)
#             # TODO: aiter
#             for buff_el in self.__documents_buffer:
#                 match buff_el.status:
#                     case DocumentStatus.CREATE:
#                         doc = await self.__pydantic_to_orm(buff_el.document)
#                         doc.collection = self._collection
#                         db_session.add(doc)
#                     case DocumentStatus.UPDATE:  # this will never be called actualy
#                         doc = await self.__pydantic_to_orm(buff_el.document)
#                         doc.collection = self._collection
#                         doc.metadata_.date_update = datetime.datetime.now()
#                         db_session.add(doc)
#                     case DocumentStatus.DELETE:
#                         print("IN DELETE", buff_el.document)
#                         await db_session.delete(buff_el.document)


# class UserCollection(DocumentFactory):

#     @classmethod
#     async def from_user(cls, __user_id: int, embedder: IEmbedder):
#         self = cls()
#         self.__user_id = __user_id
#         await super()._ainit(self, __user_id, embedder)
#         return self

#     @overload
#     async def add_document(self, __file_id: str, __text: str, *,
#                            metadata: I.DocumentMetadata): ...

#     @overload
#     async def add_document(self, __file_id: str, __text: str, *, file_id: str, name: str,
#                            description: str, token_cost: int): ...

#     async def add_document(self, *args, **kwargs):
#         metadata = kwargs.get("metadata")
#         if metadata:
#             await super()._document_from_metadata(args[0], args[1], metadata)
#         else:
#             await super()._document_from_params(args[0], args[1], **kwargs)

class DBDriveFiles:

    def __init__(self, collection_dir_id):
        self.collection_dir_id = collection_dir_id

    async def create_file(self, file_id: str, file_name: str, content: bytes, description: Optional[str] = None):
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession

            file = EM.DriveFile(
                file_id=file_id,
                content=content,
            )

            metadata = EM.DocumentMetadata(
                name=file_name,
                description=description,
            )

            file.metadata_ = metadata

            await db_session.add(file)

    async def get_file(self, file_id: str) -> EM.DriveFile:
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            res = await db_session.execute(
                select(EM.DriveFile)
                .where(EM.DriveFile.collection_fk == self.collection_dir_id)
            )
            file = res.scalar_one_or_none()

            db_session.expunge_all()
            return file

    async def delete_file(self, file_id: str) -> None:
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            await db_session.execute(
                delete(EM.DriveFile)
                .where(EM.DriveFile.file_id == file_id)
            )

    async def list_drive_files(self):
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            res = await db_session.execute(
                select(EM.DriveFile)
                .where(EM.DriveFile.collection_fk == self.collection_dir_id)
            )
            files = res.all()

            db_session.expunge_all()
            return files


class DBDocuments:
    ...


class UserCollection:

    @classmethod
    async def from_user_id(cls, user_id: int):
        collection = await cls.__get_collection("user_fk", user_id)

        self = super().__new__(cls)
        self.__collection = collection
        self.files = DBDriveFiles(collection.dir_id)
        return self

    @classmethod
    async def from_dir_id(cls, dir_id: str):
        collection = await cls.__get_collection("dir_id", dir_id)

        self = super().__new__(cls)
        self.__collection = collection
        return self

    @staticmethod
    async def __get_collection(attr: str, val: str | int):
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            res = await db_session.execute(
                select(EM.Collection)
                .where(getattr(EM.Collection, attr) == val)
            )
            collection = res.unique().scalar_one_or_none()

            db_session.expunge_all()
            return collection

    def __init__(self):
        self.__collection: EM.Collection
        self.files: DBDriveFiles

    def get_document(self):
        ...

    def list_documents(self):
        ...

    def list_drive_files(self):
        ...
