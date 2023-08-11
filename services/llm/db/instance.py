import os
from dotenv import load_dotenv
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

load_dotenv(".env")

openai_embeddings = OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-ada-002"
)


client = PersistentClient("db/embeddings")


def get_context(user_id: int, query: str) -> str:
    collection = client.get_or_create_collection(
        f"{user_id}", embedding_function=openai_embeddings)
    embeddings = openai_embeddings([query])
    context = collection.query(query_embeddings=embeddings, n_results=3)

    collection.add(
        ids=["10"],
        metadatas=[{"sourse": "balls"}],
        documents=[
            "IQ baby palace это детский сад и детский развивающий центр в городе Гатчина. Сюда можно отправить детей, чтобы они стали гениями."
        ]
    )

    print("collection_name ", collection.name)
    print("context", context["documents"])

    return "\n".join(context["documents"][0])


def get_collection_size(user_id: int) -> bool:
    collection = client.get_collection(
        str(user_id), embedding_function=openai_embeddings)

    print("collection", collection.count())
    return collection.count()
