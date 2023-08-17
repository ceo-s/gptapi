import os
import openai
from dotenv import load_dotenv
from typing import Literal, Type
from .._interfaces import IOptimizer, IEmbedder
from math import ceil


BASE_PROMPT_TEMPLATE = """
Дополнительные сведения по вопросу (если они есть) находятся ниже, в тэге "справочный материал":
    <справочный материал>
        {}
    </справочный материал>
"""


load_dotenv(".env")

openai.api_key = os.getenv("OPENAI_API_KEY")


OPTIMIZERS = Literal[
    "OverlapOptimizer",
]


class OverlapOptimizer:

    def __init__(self, __n: int, text_len: int, overlap: int):
        self.__n = __n
        self.text_len = text_len
        self.overlap = overlap
        self.n_chunks: int
        self.optimized_overlap = overlap
        self.len_ = self.calculate_len()
        self.n_chunks = self.clalculate_n_chuncks()

    def calculate_len(self) -> int:
        """
        Calculates len of the text without first __n characters
        """
        return self.text_len - self.__n

    def clalculate_n_chuncks(self) -> int:
        """
        Calculates n of solid chuncks with len() == __n
        """
        __n_ = self.__n - self.overlap  # Actual new chars appearence in all chunks except first
        n_overlapped_chunks = self.len_ // __n_  # Number of overlapped solid chunks
        print(f"{self.len_=} {__n_=} {n_overlapped_chunks=}")
        # Add that one chunk we subtracted in calculate_len
        return n_overlapped_chunks + 1

    def get_last_chunk_length(self) -> int:
        # Actual new chars appearence in all chunks except first
        __n_ = self.__n - self.overlap
        # Actual new chars appearence in last chunk
        last_new_char_len = self.len_ % __n_
        # Adding overlap to get the actual length
        return last_new_char_len + self.overlap

    def increase_overlap(self, last_chunk_length: int):
        missed_chars_len = self.__n - last_chunk_length
        overlap_raise = missed_chars_len // self.n_chunks
        return self.overlap + overlap_raise

    def decrease_overlap(self, last_chunk_length: int):
        # Eeh... Ima not sure about this
        return self.overlap - ceil((last_chunk_length - self.overlap) / (self.n_chunks-1))

    def optimize_overlap(self) -> int:
        last_chunk_length = self.get_last_chunk_length()
        print(last_chunk_length)
        if last_chunk_length >= self.__n / 2:
            overlap = self.increase_overlap(last_chunk_length)
            self.n_chunks += 1
        else:
            overlap = self.decrease_overlap(last_chunk_length)

        self.optimized_overlap = overlap

    def optimize(self):
        if self.len_ < 0:
            return self.optimized_overlap, 1
        elif self.len_ < self.__n:
            print(self.len_)
            return self.__n - self.len_, 2
        else:
            self.optimize_overlap()
        return self.optimized_overlap, self.n_chunks


OPTIMIZERS_MAPPING = {
    "OverlapOptimizer": OverlapOptimizer,
}


class TextPreprocessor:

    def __init__(self, text: str):
        self.text = text

    def split_by_n_chars(self, __n: int, overlap: int, optimizer_class: Type[OverlapOptimizer] = None) -> list[str]:
        text_len = len(self.text)
        optimizer = optimizer_class(__n, text_len, overlap)

        if optimizer is not None:
            overlap, n_chunks = optimizer.optimize()

        chunks = []
        for i in range(0, len(self.text), __n-overlap):
            chunk = self.text[i: i+__n]
            chunks.append(chunk)

        return chunks[:n_chunks]


class Embedder(IEmbedder):

    def __init__(self, chunk_size: int, overlap: int, optimizer: OPTIMIZERS):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self._optimizer = OPTIMIZERS_MAPPING[optimizer]

    async def text_to_embeddings(self, text: str) -> list[list[float]]:
        print("CREATING EMBEDDING")
        preprocessor = TextPreprocessor(text)
        texts = preprocessor.split_by_n_chars(
            self.chunk_size, self.overlap, self._optimizer)

        print(f"{len(texts)=}")
        print(f"{len(texts[-1])=}")
        # embedding = await openai.Embedding.acreate(
        #     input=[text], model="text-embedding-ada-002")
        # print("AFTER EMBEDDING")
        # return embedding["data"][0]["embedding"]
        return [[6.] * 1536] * len(texts)


def generate_prompt(prompt: str, context: str) -> str:
    return prompt + BASE_PROMPT_TEMPLATE.format(context)


def history_add_message(role: Literal["user", "assistant"], message: str, history: list[dict[str, str]], max_history_size: int, name: str = None) -> None:

    new_message = {
        "role": role,
        "content": message,
    }
    if name:
        new_message["name"] = name

    history.append(new_message)

    if len(history) > max_history_size:
        history.pop(0)
