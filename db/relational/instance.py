from sqlalchemy.orm import declarative_base

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine

postgres_url = URL.create(
    drivername="postgresql+asyncpg",
    username="alex",
    password="280177",
    host="localhost",
    port=5432,
    database="gptapi"
)

BASE = declarative_base()
ENGINE = create_async_engine(postgres_url, echo=True)
