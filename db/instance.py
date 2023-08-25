from sqlalchemy.orm import declarative_base
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
from os import getenv

load_dotenv(".env.db")

postgres_url = URL.create(
    drivername="postgresql+asyncpg",
    username=getenv("USERNAME"),
    password=getenv("PASSWORD"),
    host=getenv("HOST"),
    port=5432,
    database=getenv("DATABASE"),
)

BASE = declarative_base()
ENGINE = create_async_engine(postgres_url, echo=True)
