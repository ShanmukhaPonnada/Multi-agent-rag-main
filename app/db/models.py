"""
ORM models for storing queries, retrieved sources, and evaluation results.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Document(Base):
    """Metadata about ingested source documents (the actual chunks live in Chroma)."""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    source = Column(String(500), nullable=True)       # file path / URL
    category = Column(String(100), nullable=True)      # e.g. "medicine", "docs"
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())


class QueryLog(Base):
    """Every user query and the final answer produced by the pipeline."""
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    route_used = Column(String(50), nullable=True)     # internal_docs / web_search / both
    grounded = Column(Boolean, default=True)
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sources = relationship("QuerySource", back_populates="query_log", cascade="all, delete-orphan")


class QuerySource(Base):
    """Which context chunks/sources were used to answer a given query."""
    __tablename__ = "query_sources"

    id = Column(Integer, primary_key=True, index=True)
    query_log_id = Column(Integer, ForeignKey("query_logs.id"), nullable=False)
    content_snippet = Column(Text, nullable=False)
    source_name = Column(String(255), nullable=True)

    query_log = relationship("QueryLog", back_populates="sources")


class EvalResult(Base):
    """Results from running scripts/evaluate_rag.py against a labeled eval set."""
    __tablename__ = "eval_results"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    expected_answer = Column(Text, nullable=True)
    actual_answer = Column(Text, nullable=False)
    grounded = Column(Boolean, default=True)
    passed = Column(Boolean, default=False)
    run_at = Column(DateTime(timezone=True), server_default=func.now())
