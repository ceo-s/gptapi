import os
from dotenv import load_dotenv
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

load_dotenv(".env")

openai_embeddings = OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-ada-002"
)


client = PersistentClient("embeddings")
# col1 = client.create_collection("col111", embedding_function=openai_embeddings)
# col2 = client.create_collection("col112", embedding_function=openai_embeddings)
# col3 = client.create_collection("col113", embedding_function=openai_embeddings)
# cols = [
#     col1,
#     col2,
#     col3,
# ]

# for i, col in enumerate(cols):
#     with open(f"docs/tex{i+1}.txt", "r") as doc:
#         col.add(
#             documents=[doc.read()],
#             metadatas=[{"source": f"tex{i+1}.txt"}],
#             ids=[f"id{i+1}"],
#         )
