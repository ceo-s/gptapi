from typing import overload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, bindparam, delete

from db import get_sessionmaker
from db.models import users as UM
from db.models import embeddings as EM
from db import interfaces as I
from .._interfaces import IUser


class UserUpdator:

    def __init__(self, __user: UM.User):
        self.__user = __user

    async def __aenter__(self) -> UM.User:
        return self.__user

    async def __aexit__(self, exc_type, exc_value, traceback):
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            await db_session.merge(self.__user)


class DBUser(IUser):
    __user_id: int
    __user: UM.User

    def __bool__(self):
        return bool(self.__user)

    def __getattr__(self, attr):
        return getattr(self.__user, attr)

    def __str__(self):
        return f"User<id={self.__user_id} & first_name={self.__user.first_name}>"

    @classmethod
    async def from_id(cls, __user_id: int):
        self = cls()
        self.__user_id = __user_id
        self.__user = await self.__get()
        return self

    def dict(self):
        res = self.__user.__dict__

        res["settings"] = res["settings"].__dict__
        res.pop("collection")
        res.pop("_sa_instance_state")
        res["settings"].pop("_sa_instance_state")

        return res

    async def __get(self) -> UM.User | None:
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            res = await db_session.execute(
                select(UM.User)
                .where(UM.User.id == self.__user_id)
            )

            user = res.unique().scalar_one_or_none()

            db_session.expunge_all()
            return user

    async def create(self, username: str, first_name: str, drive_dir_id: str) -> None:
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession

            new_user = UM.User(
                id=self.__user_id,
                username=username,
                first_name=first_name,
            )

            user_settings = UM.UserSettings(
                model_temperature=0.5,
                prompt="Ты - полезный чат-бот.",
                history=[],
                history_size=100,
            )

            collection = EM.Collection(
                dir_id=drive_dir_id,
                drive_files=[],
            )

            new_user.settings = user_settings
            new_user.collection = collection
            await db_session.merge(new_user)

    def update(self):
        return UserUpdator(self.__user)

    async def update_settings(self, settings: I.OSettings) -> None:

        settings_dict = settings.model_dump()
        values_to_change = dict(
            filter(lambda key_val: key_val[1] is not None, settings_dict.items()))
        if not values_to_change:
            return

        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            await db_session.execute(
                update(UM.UserSettings)
                .where(UM.UserSettings.user_fk == self.__user_id)
                .values(values_to_change)
            )
