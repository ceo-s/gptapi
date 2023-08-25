from .llm.preprocessing import Embedder
from .db.embedding import DBDocuments


async def get_context(query: str):
    embedder = Embedder(512, 32, "OverlapOptimizer")
    query_embedding = await embedder.embed_query(query)
    documents_manager = DBDocuments()
    documents = await documents_manager.query_documents()
    print("\033[93m THIS ARE QUERIED DOCS \033[0m", documents)
