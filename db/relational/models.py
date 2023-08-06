from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import declared_attr
from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from .instance import BASE
from . import mixins as M


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

    def __repr__(self) -> str:
        return f"User №{self.id}. Name: {self.username}"


class UserSettings(M.AutoIncrement, BASE):
    __tablename__ = "user_settings"

    model_temperature: Mapped[float] = mapped_column()
    prompt: Mapped[str] = mapped_column()
    history = mapped_column(JSONB)

    user_fk: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(
        back_populates="settings",
        cascade="all, delete", uselist=False,
        lazy="joined",
    )

    def __repr__(self) -> str:
        return f"{self.user.first_name} settings."
