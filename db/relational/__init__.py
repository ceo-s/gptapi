from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from .models import BASE
from .instance import ENGINE


def get_sessionmaker() -> sessionmaker:
    return sessionmaker(ENGINE, class_=AsyncSession)
