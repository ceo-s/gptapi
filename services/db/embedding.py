import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, bindparam, delete
from abc import ABC, abstractstaticmethod, abstractclassmethod, abstractmethod

from db import get_sessionmaker
from db.models.users import User, UserSettings
from db.models.embeddings import Collection as Collection_
from db import interfaces as I


class CollectionAdapter:

    def __init__(self) -> None:
        self.__colection = I.Collection()

    async def create(self):
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            res = await db_session.execute(
                select(User)
                .where(User.id == user_id)
            )

            user = res.scalar_one_or_none()

            db_session.expunge_all()
            return user

    def update(self):
        ...

    def delete(self):
        ...

    @property
    def documents(self):
        return self.__colection.documents


class Collection:
    ...


class EmbeddingDB:

    def __init__(self) -> None:
        self.__collection = CollectionAdapter

    def get_collection(self, User) -> Collection:
        ...

# async def get_user(user_id: int) -> User | None:
#     async with get_sessionmaker().begin() as db_session:
#         db_session: AsyncSession
#         res = await db_session.execute(
#             select(User)
#             .where(User.id == user_id)
#         )

#         user = res.scalar_one_or_none()

#         db_session.expunge_all()
#         return user
