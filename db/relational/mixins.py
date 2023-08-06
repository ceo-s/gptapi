from sqlalchemy.orm import Mapped, mapped_column, declared_attr


class AutoIncrement:
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)


class ClassNamed:
    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
