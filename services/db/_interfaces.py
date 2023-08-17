from abc import ABC, abstractmethod
from datetime import datetime


class IUpdatable(ABC):

    @abstractmethod
    async def update(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback): ...


class ICollection(IUpdatable):

    @abstractmethod
    async def __get__(self) -> list[IDocument]: ...

    @abstractmethod
    async def __getitem__(self, __key: int) -> IDocument: ...

    @abstractmethod
    async def __delitem__(self, __key: int): ...

    @abstractmethod
    async def push(self): ...

    @abstractmethod
    async def pop(self): ...


# class ITextPreprocessor(ABC):

#     @abstractmethod
#     def split_into_junks(self): ...
