from typing import Literal, overload, Type, NamedTuple, Optional, Sequence
from enum import Enum
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from db import get_sessionmaker
from db.models import users as UM
from db.models import embeddings as EM
from db import interfaces as I
from log import logger


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


class DBDriveFiles:

    async def create_files(self, files: Sequence[I.File]):
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            logger.debug(
                f"Creating files from Drive: \n{[file.id for file in files]}")

            for file in files:

                db_file = EM.DriveFile(
                    file_id=file.id,
                    content=file.content,
                    collection_fk=file.parents[0]
                )

                metadata = EM.DocumentMetadata(
                    name=file.name,
                    description=file.description,
                )

                db_file.metadata_ = metadata

                await db_session.merge(db_file)

            await db_session.commit()

    async def get_file(self, file_id: str) -> EM.DriveFile:
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            res = await db_session.execute(
                select(EM.DriveFile)
                .where(EM.DriveFile.file_id == file_id)
            )
            file = res.scalar_one_or_none()

            db_session.expunge_all()
            return file

    async def update_files(self, files: Sequence[tuple[I.File, EM.DriveFile]]) -> None:
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            for new_file, old_file in files:
                old_file.content = new_file.content
                old_file.metadata_.name = new_file.name
                old_file.metadata_.description = new_file.description

                await db_session.merge(old_file)

            await db_session.commit()

    async def delete_files(self, files: list[I.File]) -> None:
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            file_ids = [file.id for file in files]

            await db_session.execute(
                delete(EM.DriveFile)
                .where(EM.DriveFile.file_id.in_(file_ids))
            )

    async def list_files(self, file_ids: Sequence[str]) -> list[EM.DriveFile]:
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            res = await db_session.execute(
                select(EM.DriveFile)
                .where(EM.DriveFile.file_id.in_(file_ids))
            )
            files = res.scalars().all()

            db_session.expunge_all()
            return files


class DBDocuments:

    async def create_documents(self, drive_file_id: str, texts: list[str], embedding_dicts: list[dict]):
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            for i in range(len(texts)):

                db_file = EM.Document(
                    text=texts[i],
                    embedding=embedding_dicts[i]["embedding"],
                    drive_file_fk=drive_file_id
                )
                db_session.add(db_file)

            await db_session.commit()

    async def delete_documents(self, drive_files: Sequence[I.File]) -> None:
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            file_ids = [file.id for file in drive_files]

            await db_session.execute(
                delete(EM.Document)
                .where(EM.Document.drive_file_fk.in_(file_ids))
            )

    async def query_documents(self, user_id: int, query_embedding: list[float], n_documents: int = 3):
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession

            dir_id = await db_session.scalar(select(EM.Collection.dir_id).where(EM.Collection.user_fk == user_id))
            file_ids = (await db_session.scalars(select(EM.DriveFile.file_id).where(EM.DriveFile.collection_fk == dir_id))).all()

            res = await db_session.scalars(
                select(EM.Document.text).where(EM.Document.drive_file_fk.in_(file_ids)).order_by(
                    EM.Document.embedding.l2_distance(query_embedding)).limit(n_documents)
            )

            documents = res.all()
            db_session.expunge_all()
            return documents


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
        self.files = DBDriveFiles(dir_id)
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

    @staticmethod
    async def get_id(user_id: int):
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            res = await db_session.scalar(
                select(EM.Collection.dir_id)
                .where(EM.Collection.user_fk == user_id)
            )
            return res
