from functools import singledispatch
from typing import overload


@overload
def remove(name: str): ...
@overload
def remove(file_id: str): ...
@overload
def remove(description: str): ...


def remove(**kwargs):

    print(f"Sorting by {next(iter(kwargs.keys()))=}")


"""
А как работает делегирование при вызове new? Например есть классы:
class User(BaseUser): ...
class BaseUser: ...

Я в методе __new__ каждый раз прописываю super().__new__(cls)
Получается он так идёт по цепочке User -> BaseUser -> object и каждый раз 
super().__new__(cls) выдает класс следующего в списке mro класса.
Например
class User(BaseUser):
    def __new__(cls):
        _super = super().__new__(cls)
        print(_super) # <class '__main__.BaseUser'>
        return _super
Но я думал что метод __new__ должен в
"""
