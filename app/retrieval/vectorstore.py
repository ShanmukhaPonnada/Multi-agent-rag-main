from langchain_community.vectorstores import Chroma
from app.config import CHROMA_DB_PATH, RETRIEVER_TOP_K
from app.retrieval.embeddings import get_embedding_model

_vectorstore = None


def get_vectorstore():
    """Singleton loader for the persisted Chroma vector store."""
    global _vectorstore
    if _vectorstore is None:
        embeddings = get_embedding_model()
        _vectorstore = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embeddings,
        )
    return _vectorstore


def get_retriever(k: int = None):
    vectorstore = get_vectorstore()
    return vectorstore.as_retriever(search_kwargs={"k": k or RETRIEVER_TOP_K})


def build_vectorstore_from_documents(documents):
    """Used by scripts/ingest_documents.py to (re)build the store from scratch."""
    embeddings = get_embedding_model()
    vectorstore = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory=CHROMA_DB_PATH,
    )
    vectorstore.persist()
    return vectorstore
