"""
Build (or rebuild) the vector store from documents in data/raw/,
and register document metadata in Postgres.

By default this ingests data/raw/indian_medicines_sample.csv — a real,
cleaned sample of 2,000 Indian medicines (name, manufacturer, composition,
pack size, price) sourced from the public junioralive/Indian-Medicine-Dataset
on GitHub. Swap in your own CSV/PDF/txt files as needed.

Usage:
    python scripts/ingest_documents.py                       # ingest the default medicine CSV
    python scripts/ingest_documents.py --csv path/to/other.csv --text-cols col1 col2
    python scripts/ingest_documents.py --csv ""              # falls back to .txt/.pdf in data/raw
"""

import sys, os, argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.retrieval.loaders import (
    load_text_files, load_pdfs, load_csv_as_documents, chunk_documents,
)
from app.retrieval.vectorstore import build_vectorstore_from_documents
from app.db.database import SessionLocal
from app.db import crud


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", help="Path to a CSV file to ingest instead of data/raw text/pdf",
                         default="./data/raw/indian_medicines_sample.csv")
    parser.add_argument("--text-cols", nargs="+",
                         default=["name", "manufacturer_name", "short_composition1", "short_composition2"],
                         help="Columns to use as document text when --csv is given")
    parser.add_argument("--source-col", default="name",
                         help="Column to use as the citation/source label")
    args = parser.parse_args()

    if args.csv:
        print(f"Loading CSV: {args.csv}")
        raw_docs = load_csv_as_documents(args.csv, args.text_cols, args.source_col)
    else:
        print("Loading .txt and .pdf files from data/raw/")
        raw_docs = load_text_files("./data/raw") + load_pdfs("./data/raw")

    print(f"Loaded {len(raw_docs)} raw documents")

    chunks = chunk_documents(raw_docs)
    print(f"Split into {len(chunks)} chunks")

    build_vectorstore_from_documents(chunks)
    print("Vector store built and persisted.")

    # Register metadata in Postgres
    db = SessionLocal()
    try:
        seen = set()
        for doc in raw_docs:
            source = doc.metadata.get("source", "unknown")
            if source not in seen:
                crud.register_document(db, title=source, source=source)
                seen.add(source)
        print(f"Registered {len(seen)} document(s) in the database.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
