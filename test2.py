from db.interfaces import Document
from abc import ABC


class _User:

    def __init__(self, *args, **kwargs):
        self._arg = args[0]

    def _update(self):
        print("UPDATING")


class _UserUpdateContextManager:

    def __enter__(self):
        print("ENTERING")
        self._update()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        ...


class User(_UserUpdateContextManager, _User):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        return self


usr = User(1)

with usr.update() as upd:
    print(f"{upd=}")
    print("A")


# class IUser(ABC):
#     id: int = None
#     username: str
#     first_name: str


# for attr, value in vars(IUser)["__annotations__"].items():
#     print(f"{attr=} {value=}")
