from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import declared_attr
from sqlalchemy import String, BigInteger, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from datetime import datetime

from db.instance import BASE
from ..mixins import mixins as M

OPENAI_EMBEDDING_SIZE = 1536


class Collection(M.AutoIncrement, M.ClassNamed, BASE):
    documents: Mapped[list["Document"]] = relationship(
        back_populates="collection",
        cascade="all, delete-orphan",
        uselist=True,
        lazy="joined",
    )

    user_fk: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(
        back_populates="collection",
        cascade="all, delete",
        uselist=False,
        lazy="joined",
    )


class Document(M.AutoIncrement, M.ClassNamed, BASE):
    metadata_: Mapped["DocumentMetadata"] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="joined",
    )
    embedding = mapped_column(Vector(OPENAI_EMBEDDING_SIZE))

    collection_fk: Mapped[int] = mapped_column(
        ForeignKey("collection.id", ondelete="CASCADE")
    )
    collection: Mapped["Collection"] = relationship(
        back_populates="documents",
        cascade="all, delete",
        lazy="joined",
    )


class DocumentMetadata(M.AutoIncrement, BASE):
    __tablename__ = "document_metadata"

    file_id: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    token_cost: Mapped[int] = mapped_column()
    date_creation: Mapped[datetime] = mapped_column(DateTime())
    date_update: Mapped[datetime] = mapped_column(DateTime())

    document_fk: Mapped[int] = mapped_column(
        ForeignKey("document.id", ondelete="CASCADE")
    )
    document: Mapped["Document"] = relationship(
        back_populates="metadata_",
        cascade="all, delete",
        uselist=False,
        lazy="joined",
    )
