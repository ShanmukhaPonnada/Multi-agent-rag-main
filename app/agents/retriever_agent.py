from app.retrieval.vectorstore import get_retriever
from app.utils.logger import get_logger

logger = get_logger(__name__)


def retriever_agent_internal(query: str) -> list[str]:
    retriever = get_retriever()
    docs = retriever.get_relevant_documents(query)
    logger.info(f"Internal retriever returned {len(docs)} chunks")
    return [d.page_content for d in docs]
