
# Multi-Agent RAG System

A Retrieval-Augmented Generation system built with multiple collaborating agents:

**Router → Retriever(s) → Synthesizer → Critic**

Backed by a PostgreSQL database for logging, document metadata, and evaluation history.

## Architecture

```text
User Query
    |
    v
Router Agent -----> decides which source(s) to use
    |
    +--> Retriever Agent (Vector DB / Chroma)
    +--> Web Search Agent
    |
    v
Synthesizer Agent -> drafts answer from retrieved context
    |
    v
Critic Agent -------> checks grounding and triggers retry if needed
    |
    v
Final Answer (+ citations, logged to DB)

## Dataset

`data/raw/indian_medicines_sample.csv` — a real, cleaned sample of **2,000
Indian medicines** (name, manufacturer, composition, pack size, price),
sourced from the public
[junioralive/Indian-Medicine-Dataset](https://github.com/junioralive/Indian-Medicine-Dataset)
on GitHub (253,973 medicines total; this sample was filtered to non-discontinued
items with a valid composition, then randomly sampled for a fast, demo-friendly
ingestion time). Swap in your own CSV/PDF/txt files in `data/raw/` as needed —
see `scripts/ingest_documents.py --help`.

## Frontend (Streamlit)

A simple chat UI is included (`streamlit_app.py`) — pure Python, no
JavaScript required. It talks to the FastAPI backend over HTTP, same as any
real frontend would.

**Run the backend first** (in one terminal):
```bash
uvicorn app.main:app --reload
```

**Then, in a separate terminal**, run the frontend:
```bash
streamlit run streamlit_app.py
```

This opens a browser tab at `http://localhost:8501` with a chat interface —
type a question, see the answer with a grounded/not-grounded badge, which
route was used, and the retrieved sources in an expandable panel. The
sidebar shows backend connection status and recent query history pulled
from Postgres.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # fill in your keys + DB URL
python scripts/init_db.py       # create DB tables
python scripts/ingest_documents.py   # build vector store from data/raw
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

## Project Structure

See [`docs/folder_structure.txt`](docs/folder_structure.txt) for the full annotated
layout. Quick summary:

```
app/
  agents/        Router, Retriever, Synthesizer, Critic, Web-Search agents
  orchestrator/  Ties the agents together into the full pipeline
  retrieval/     Document loading, chunking, embeddings, vector store
  models/        Gemini client + Pydantic request/response schemas
  db/            SQLAlchemy models + CRUD for logging queries/eval results
  utils/         Prompts + logging
scripts/         init_db.py, ingest_documents.py, evaluate_rag.py
tests/           pytest suite (needs a real GEMINI_API_KEY to run)
data/raw/        Source documents (ships with a real 2,000-row medicine dataset)
```

## Environment Variables (`.env`)

```
GEMINI_API_KEY=your_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/ragdb
CHROMA_DB_PATH=./data/chroma_db
HF_HUB_OFFLINE=1
TRANSFORMERS_OFFLINE=1
```

## Running Tests

```bash
pytest tests/
```

## Evaluation

```bash
python scripts/evaluate_rag.py
```


## License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for details.
