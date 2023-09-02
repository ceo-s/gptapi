from .llm.preprocessing import Embedder
from .db.embedding import DBDocuments
from log import logger


async def get_context(user_id: int, query: str):
    embedder = Embedder(512, 32, "OverlapOptimizer")
    query_embedding = await embedder.embed_query(query)
    documents_manager = DBDocuments()
    documents = await documents_manager.query_documents(user_id, query_embedding)
    logger.debug(f"THESE ARE QURIED DOCS {documents}")
    return documents
