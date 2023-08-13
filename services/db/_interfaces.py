from abc import ABC, abstractmethod
from datetime import datetime


class IUpdatable(ABC):

    @abstractmethod
    async def update(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback): ...


class ISettings(IUpdatable):
    history: list[dict[str, str]]
    prompt: str
    model_temperature: float
    history_size: int


class IUser(IUpdatable):
    id: int
    username: str
    first_name: str
    settings: ISettings


class IDocumentMetadata:
    file_id: str
    name: str
    description: str
    token_cost: int
    date_creation: datetime
    date_update: datetime


class IDocument(IUpdatable):
    metadata: dict
    embedding: list[float]


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
