from abc import ABC, abstractmethod
from typing import Any, Coroutine, overload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, bindparam, delete

from db import get_sessionmaker
from db.models import users as UM
from db import interfaces as I
from db.models.users import User

from ._relational import _Settings, _User
from ._interfaces import IUser, ISettings, IUpdatable


class Settings(_Settings, ISettings):

    @overload
    async def __init__(self, __user_id: int) -> None: ...
    @overload
    async def __init__(self, __settings: I.OSettings) -> None: ...
    @overload
    async def __init__(self, __settings: UM.UserSettings) -> None: ...

    async def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = I.Settings.model_validate(self._settings)
        self.__migrate_fields(settings)

    async def __migrate_fields(self, settings: I.Settings):
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
    # @overload
    # def __init__(self, __user_id: int) -> None: ...
    # @overload
    # def __init__(self, __user: I.OUser) -> None: ...

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     user = I.BaseUser.model_validate(self._user)
    #     self.__migrate_fields(user)
    #     self.settings = Settings(self._user.settings)

    async def ainit(self, *args, **kwargs):
        await super().ainit(*args, **kwargs)
        user = I.BaseUser.model_validate(self._user)

        await self.__migrate_fields(user)
        self.settings = Settings(self._user.settings)
        ...

    async def __migrate_fields(self, user: I.BaseUser):
        for attr, value in user:
            setattr(self, attr, value)

    async def get(self, user_id) -> User | None:
        return await super()._get(user_id)

    async def get_or_create(self, user: I.OUser) -> User:
        return await super()._get_or_create(user)

    async def update(self):
        return self

    async def __aenter__(self):
        ...

    async def __aexit__(self, exc_type, exc_value, traceback):
        for attr in vars(IUser)["__annotations__"].keys():
            setattr(self._user, attr, getattr(self, attr))
        self._update()


usr = User()


Settings()
