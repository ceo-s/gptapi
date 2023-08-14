from abc import ABC, abstractmethod
from typing import Any, Coroutine, overload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, bindparam, delete

from db import get_sessionmaker
from db.models import users as UM
from db import interfaces as I
from db.models.users import User

from ._relational import _Settings, _User
from ._relational import _Settings2, _User2
from ._interfaces import IUser, ISettings, IUpdatable


class Settings(_Settings, ISettings):

    def __init__(self, __settings: I.OSettings) -> None:
        super().__init__(__settings)
        settings = I.Settings.model_validate(self._settings)
        self.__migrate_fields(settings)

    def __migrate_fields(self, settings: I.Settings):
        for attr, value in settings:
            setattr(self, attr, value)

    async def update(self):
        return self

    async def __aenter__(self):
        ...

    async def __aexit__(self, exc_type, exc_value, traceback):
        for attr in vars(IUser)["__annotations__"].keys():
            setattr(self._settings, attr, getattr(self, attr))
        self._update()


class User(_User, IUser):

    def __init__(self):
        super().__init__()

    @overload
    async def ainit(self, __user_id: int): ...
    @overload
    async def ainit(self, __user: I.User): ...

    async def ainit(self, *args, **kwargs):
        await super().ainit(*args, **kwargs)
        print(f"{self._user=}")
        print(f"{vars(self._user)=}")
        user = I.BaseUser.model_validate(self._user)

        await self.__migrate_fields(user)
        self.settings = Settings(self._user.settings)
        ...

    async def __migrate_fields(self, user: I.BaseUser):
        for attr, value in user:
            setattr(self, attr, value)

    async def get(self, user_id) -> User | None:
        return await super()._get(user_id)

    async def get_or_create(self, user: I.User) -> User:
        return await super()._get_or_create(user)

    async def update(self):
        return self

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        for attr in vars(IUser)["__annotations__"].keys():
            setattr(self._user, attr, getattr(self, attr))
        self._update()


class Settings2(_Settings2, ISettings):

    def __init__(self, __settings: UM.UserSettings) -> None:
        super().__init__(__settings)

    async def update(self):
        return self

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        for attr in vars(IUser)["__annotations__"].keys():
            setattr(self._user, attr, getattr(self, attr))
        self._update()


class User2(_User2, IUser):

    # def __new__(cls, *args, **kwargs):
    #     print("THIS IS USER2 cls in new", cls)
    #     print("FIRST NEW")
    #     _user2 = super().__new__(cls)
    #     print("_USER@ INSTANCE", _user2)
    #     return _user2

    @classmethod
    async def from_pydantic(cls, __user: I.User):
        self = cls()
        await super().from_pydantic(self, __user)
        self.__migrate_info(self._user)
        print("VARS SELF", vars(self))

        return self

    @classmethod
    async def from_id(cls, __user_id: int):
        self = cls()
        await super().from_id(self, __user_id)
        self.__migrate_info(self._user)
        print("VARS SELF", vars(self))
        self.settings = Settings2(self._user.settings)

        return self

    def __migrate_info(self, user: UM.User):
        print(I.BaseUser.__fields__)
        for attr in I.BaseUser.__fields__:
            setattr(self, attr, getattr(user, attr))

    def __migrate_settings(self):
        ...

    async def update(self):
        return self

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        for attr in vars(IUser)["__annotations__"].keys():
            setattr(self._user, attr, getattr(self, attr))
        self._update()
