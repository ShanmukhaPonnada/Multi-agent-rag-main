"""
Document loading + chunking. Add new loaders here as you add data sources
(CSV, PDF, DB table, API, etc.) and call them from scripts/ingest_documents.py.
"""

import pandas as pd
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

from app.config import CHUNK_SIZE, CHUNK_OVERLAP


def load_text_files(folder_path: str = "./data/raw"):
    loader = DirectoryLoader(folder_path, glob="**/*.txt")
    return loader.load()


def load_pdfs(folder_path: str = "./data/raw"):
    import glob
    docs = []
    for pdf_path in glob.glob(f"{folder_path}/**/*.pdf", recursive=True):
        docs.extend(PyPDFLoader(pdf_path).load())
    return docs


def load_csv_as_documents(csv_path: str, text_columns: list[str],
                           source_column: str = None) -> list[Document]:
    """
    Turns rows of a CSV (e.g. a medicine dataset) into LangChain Documents.
    text_columns: which columns to concatenate into the document body.
    source_column: which column to use as the citation/source label.
    """
    df = pd.read_csv(csv_path)
    documents = []
    for _, row in df.iterrows():
        # Skip missing/NaN values so they don't render as the literal string "nan"
        content = "\n".join(
            f"{col}: {row[col]}" for col in text_columns
            if col in row and pd.notna(row[col]) and str(row[col]).strip()
        )
        source_label = str(row[source_column]) if source_column and source_column in row else csv_path
        documents.append(Document(page_content=content, metadata={"source": source_label}))
    return documents


def chunk_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)
