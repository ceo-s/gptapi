from typing import overload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, bindparam, delete

from db import get_sessionmaker
from db.models import users as UM
from db import interfaces as I

from functools import singledispatchmethod


# class _Settings:

#     def __init__(self, __settings: UM.UserSettings):
#         self._settings = __settings

#     async def _update(self):
#         async with get_sessionmaker().begin() as db_session:
#             db_session: AsyncSession
#             await db_session.merge(self._settings)


# class _User:

#     def __init__(self) -> None:
#         ...

#     async def ainit(self, *args, **kwargs):
#         self.__init__()
#         self._user: UM.User
#         self.is_new = False
#         await self.__init_argument(args[0])

#     @singledispatchmethod
#     async def __init_argument(self):
#         ...

#     @__init_argument.register
#     async def _(self, __user_id: int):
#         self._user = await self._get(__user_id)

#     @__init_argument.register
#     async def _(self, __user: I.User):
#         self._user = await self._get_or_create(__user)

#     async def _create(self, user: I.User) -> UM.User:
#         async with get_sessionmaker().begin() as db_session:
#             db_session: AsyncSession

#             user = UM.User(
#                 id=user.id,
#                 username=user.username,
#                 first_name=user.first_name,
#             )

#             user_settings = UM.UserSettings(
#                 model_temperature=0.5,
#                 prompt="Ты - полезный чат-бот.",
#                 history=[],
#                 history_size=100,
#             )

#             user.settings = user_settings
#             await db_session.merge(user)

#             await db_session.refresh(user)
#             await db_session.expunge_all()
#             return user

#     async def _get(self, user_id) -> UM.User | None:
#         async with get_sessionmaker().begin() as db_session:
#             db_session: AsyncSession
#             res = await db_session.execute(
#                 select(UM.User)
#                 .where(UM.User.id == user_id)
#             )

#             user = res.scalar_one_or_none()

#             db_session.expunge_all()
#             return user

#     async def _get_or_create(self, user: I.User) -> UM.User:
#         user = self._get(user.id)
#         if user is None:
#             user = self._create(user)
#             self.is_new = True

#         return user

#     async def _update(self):

#         async with get_sessionmaker().begin() as db_session:
#             db_session: AsyncSession
#             await db_session.merge(self._user)

#     async def _delete(self):
#         async with get_sessionmaker().begin() as db_session:
#             db_session: AsyncSession
#             await db_session.delete(self._user)


class _Settings:

    def __init__(self, __settings: UM.UserSettings) -> None:
        self._settings = __settings
        self.__migrate_fields()

    def __migrate_fields(self):
        print(self._settings)
        for attr in I.Settings.__fields__:
            setattr(self, attr, getattr(self._settings, attr))


class _User:

    def __init__(self) -> None:
        self._user: UM.User
        self.is_new: bool = False
        print("IMA IN INIT")

    # def __new__(cls):
    #     print("THIS IS _USER2 cls in new", cls)
    #     print("I am calling new")
    #     _super = super().__new__(cls)
    #     print(_super)
    #     return _super

    @classmethod
    async def from_pydantic(cls, __parent_cls, __user: I.User):
        self = __parent_cls
        self._user = await self._get_or_create(__user)
        print(self.is_new)

    @classmethod
    async def from_id(cls, __parent_cls, __user_id: int):
        self = __parent_cls
        self._user = await self._get(__user_id)

    async def _create(self, __user: I.User) -> UM.User:
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession

            user = UM.User(
                id=__user.id,
                username=__user.username,
                first_name=__user.first_name,
            )

            user_settings = UM.UserSettings(
                model_temperature=0.5,
                prompt="Ты - полезный чат-бот.",
                history=[],
                history_size=100,
            )

            user.settings = user_settings
            await db_session.merge(user)
            return user

    async def _get(self, __user_id) -> UM.User | None:
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            res = await db_session.execute(
                select(UM.User)
                .where(UM.User.id == __user_id)
            )

            # user = res.scalar_one_or_none()
            user = res.unique().scalar_one_or_none()
            # next(user)
            # print(f"IMA IN SESSION GET {user.settings=}")
            # print(f"IMA IN SESSION GET {user=}")

            # db_session.expunge_all()
            return user

    async def _get_or_create(self, __user: I.User) -> UM.User:
        user = await self._get(__user.id)
        if user is None:

            user = await self._create(__user)
            self.is_new = True
            # print(f"IMA REALLY CREATING {user.settings}")
        # print(f"IMA GET OR CREATE {user.settings}")
        return user

    async def _update(self):
        async with get_sessionmaker().begin() as db_session:
            db_session: AsyncSession
            await db_session.merge(self._user)

# async def get_user(user_id: int) -> UM.User | None:
#     async with get_sessionmaker().begin() as db_session:
#         db_session: AsyncSession
#         res = await db_session.execute(
#             select(UM.User)
#             .where(UM.User.id == user_id)
#         )

#         user = res.scalar_one_or_none()

#         db_session.expunge_all()
#         return user


# async def register_user(user: I.OUser) -> None:
#     async with get_sessionmaker().begin() as db_session:
#         db_session: AsyncSession

#         user = UM.User(
#             id=user.id,
#             username=user.username,
#             first_name=user.first_name,
#         )

#         user_settings = UM.UserSettings(
#             model_temperature=0.5,
#             prompt="Ты - полезный чат-бот.",
#             history=[],
#             history_size=100,
#         )

#         user.settings = user_settings
#         await db_session.merge(user)


# async def update_user(user: I.OUser) -> None:
#     user_dict = user.model_dump()
#     user_dict.pop("id")
#     user_dict.pop("settings")
#     values_to_change = dict(
#         filter(lambda key_val: key_val[1] is not None, user_dict.items()))

#     if not values_to_change:
#         return

#     async with get_sessionmaker().begin() as db_session:
#         db_session: AsyncSession
#         await db_session.execute(
#             update(UM.User)
#             .where(UM.User.id == user.id)
#             .values(values_to_change)
#         )


# async def update_user_settings(user_id: int, settings: I.OSettings | None) -> None:

#     if settings is None:
#         return

#     settings_dict = settings.model_dump()
#     values_to_change = dict(
#         filter(lambda key_val: key_val[1] is not None, settings_dict.items()))
#     if not values_to_change:
#         return

#     async with get_sessionmaker().begin() as db_session:
#         db_session: AsyncSession
#         await db_session.execute(
#             update(UM.UserSettings)
#             .where(UM.UserSettings.user_fk == user_id)
#             .values(values_to_change)
#         )
