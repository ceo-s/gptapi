from ..mixins import mixins as M
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import declared_attr
from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from openai import Embedding

from db.instance import BASE


class User(M.ClassNamed, BASE):

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(36))
    first_name: Mapped[str] = mapped_column(String(32))

    settings: Mapped["UserSettings"] = relationship(
        back_populates="user",
        cascade="all, delete",
        uselist=False,
        lazy="joined",
    )

    collection: Mapped["Collection"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="joined",
    )

    def __repr__(self) -> str:
        return f"User №{self.id}. Name: {self.username}"


class UserSettings(M.AutoIncrement, BASE):
    __tablename__ = "user_settings"

    model_temperature: Mapped[float] = mapped_column()
    prompt: Mapped[str] = mapped_column()
    history = mapped_column(JSONB)
    history_size: Mapped[int] = mapped_column()

    user_fk: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(
        back_populates="settings",
        cascade="all, delete",
        uselist=False,
        lazy="joined",
    )

    def __repr__(self) -> str:
        return f"Some user settings."
