from abc import ABC, abstractmethod
from datetime import datetime


class IOptimizer(ABC):

    @abstractmethod
    def optimize(self, chunks: list[str]): ...


class IEmbedder(ABC):

    @abstractmethod
    async def text_to_embeddings(self) -> list[list[float]]: ...


class ISettings(ABC):
    history: list[dict[str, str]]
    prompt: str
    model_temperature: float
    history_size: int


class IUser(ABC):
    id: int
    username: str
    first_name: str
    settings: ISettings


class IDocumentMetadata(ABC):
    name: str
    description: str
    token_cost: int
    date_creation: datetime
    date_update: datetime


class IDocument(ABC):
    file_id: str
    metadata_: IDocumentMetadata
    embedding: list[float]
