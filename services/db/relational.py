from typing import overload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, bindparam, delete

from db import get_sessionmaker
from db.models import users as UM
from db.models import embeddings as EM
from db import interfaces as I


async def get_user(user_id: int) -> UM.User | None:
    async with get_sessionmaker().begin() as db_session:
        db_session: AsyncSession
        res = await db_session.execute(
            select(UM.User)
            .where(UM.User.id == user_id)
        )

        user = res.unique().scalar_one_or_none()

        db_session.expunge_all()
        return user


async def register_user(user: I.OUser) -> None:
    async with get_sessionmaker().begin() as db_session:
        db_session: AsyncSession

        new_user = UM.User(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
        )

        user_settings = UM.UserSettings(
            model_temperature=0.5,
            prompt="Ты - полезный чат-бот.",
            history=[],
            history_size=100,
        )

        collection = EM.Collection(
            documents=[],
        )

        new_user.settings = user_settings
        new_user.collection = collection
        await db_session.merge(new_user)


async def update_user(user: I.OUser) -> None:
    user_dict = user.model_dump()
    user_dict.pop("id")
    user_dict.pop("settings")
    values_to_change = dict(
        filter(lambda key_val: key_val[1] is not None, user_dict.items()))

    if not values_to_change:
        return

    async with get_sessionmaker().begin() as db_session:
        db_session: AsyncSession
        await db_session.execute(
            update(UM.User)
            .where(UM.User.id == user.id)
            .values(values_to_change)
        )


async def update_user_settings(user_id: int, settings: I.OSettings) -> None:

    settings_dict = settings.model_dump()
    values_to_change = dict(
        filter(lambda key_val: key_val[1] is not None, settings_dict.items()))
    if not values_to_change:
        return

    async with get_sessionmaker().begin() as db_session:
        db_session: AsyncSession
        await db_session.execute(
            update(UM.UserSettings)
            .where(UM.UserSettings.user_fk == user_id)
            .values(values_to_change)
        )
