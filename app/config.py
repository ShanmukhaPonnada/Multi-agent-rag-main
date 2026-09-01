import os
from dotenv import load_dotenv

load_dotenv()

# --- LLM ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# --- Database ---
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://raguser:ragpassword@localhost:5432/ragdb"
)

# --- Vector store ---
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# --- RAG tuning ---
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
RETRIEVER_TOP_K = int(os.getenv("RETRIEVER_TOP_K", 4))
MAX_CRITIC_RETRIES = int(os.getenv("MAX_CRITIC_RETRIES", 2))
