from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from .instance import ENGINE, BASE


def get_sessionmaker() -> sessionmaker:
    return sessionmaker(ENGINE, class_=AsyncSession)
