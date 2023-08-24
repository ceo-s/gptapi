from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import declared_attr
from sqlalchemy import String, BigInteger, ForeignKey, DateTime, LargeBinary
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from datetime import datetime

from db.instance import BASE
from ..mixins import mixins as M

OPENAI_EMBEDDING_SIZE = 1536


class Collection(M.AutoIncrement, M.ClassNamed, BASE):
    dir_id: Mapped[str] = mapped_column()

    drive_files: Mapped[list["DriveFile"]] = relationship(
        back_populates="collection",
        cascade="all, delete-orphan",
        uselist=True,
        lazy="selectin",
    )

    user_fk: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(
        back_populates="collection",
        cascade="all, delete",
        uselist=False,
        lazy="selectin",
    )


class DriveFile(BASE):
    __tablename__ = "drive_file"

    file_id: Mapped[str] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column()

    metadata_: Mapped["DocumentMetadata"] = relationship(
        back_populates="drive_file",
        cascade="all, delete",
        uselist=False,
        lazy="joined",
    )

    documents: Mapped[list["Document"]] = relationship(
        back_populates="drive_file",
        cascade="all, delete-orphan",
        uselist=True,
        lazy="selectin",
    )

    collection_fk: Mapped[int] = mapped_column(
        ForeignKey("collection.id")
    )
    collection: Mapped["Collection"] = relationship(
        back_populates="drive_files",
        lazy="joined",
    )


class Document(M.AutoIncrement, M.ClassNamed, BASE):

    text: Mapped[str] = mapped_column()
    embedding = mapped_column(Vector(OPENAI_EMBEDDING_SIZE))

    drive_file_fk: Mapped[int] = mapped_column(
        ForeignKey("drive_file.file_id", ondelete="CASCADE")
    )
    drive_file: Mapped["Document"] = relationship(
        back_populates="metadata_",
        cascade="all, delete",
        uselist=False,
        lazy="joined",
    )


class DocumentMetadata(M.AutoIncrement, BASE):
    __tablename__ = "document_metadata"

    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    token_cost: Mapped[int] = mapped_column(nullable=True)

    drive_file_fk: Mapped[str] = mapped_column(
        ForeignKey("drive_file.file_id", ondelete="CASCADE")
    )
    drive_file: Mapped[DriveFile] = relationship(
        back_populates="metadata_",
        cascade="all, delete",
        uselist=False,
        lazy="joined",
    )
