import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, bindparam, delete

from db import get_sessionmaker
from db.models.users import User, UserSettings
from db import interfaces as I


async def get_user(user_id: int) -> User | None:
    async with get_sessionmaker().begin() as db_session:
        db_session: AsyncSession
        res = await db_session.execute(
            select(User)
            .where(User.id == user_id)
        )

        user = res.scalar_one_or_none()

        db_session.expunge_all()
        return user


async def register_user(user: I.OUser) -> None:
    async with get_sessionmaker().begin() as db_session:
        db_session: AsyncSession

        user = User(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
        )

        user_settings = UserSettings(
            model_temperature=0.5,
            prompt="Ты - полезный чат-бот.",
            history=[],
            history_size=100,
        )

        user.settings = user_settings
        await db_session.merge(user)


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
            update(User)
            .where(User.id == user.id)
            .values(values_to_change)
        )


async def update_user_settings(user_id: int, settings: I.OSettings | None) -> None:

    if settings is None:
        return

    settings_dict = settings.model_dump()
    values_to_change = dict(
        filter(lambda key_val: key_val[1] is not None, settings_dict.items()))
    if not values_to_change:
        return

    async with get_sessionmaker().begin() as db_session:
        db_session: AsyncSession
        await db_session.execute(
            update(UserSettings)
            .where(UserSettings.user_fk == user_id)
            .values(values_to_change)
        )
