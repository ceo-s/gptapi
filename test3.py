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
