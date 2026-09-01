"""
CRUD helper functions — keeps raw SQLAlchemy queries out of the agents/orchestrator.
"""

from sqlalchemy.orm import Session
from app.db import models


def log_query(db: Session, query: str, answer: str, route_used: str,
               grounded: bool, retry_count: int, sources: list[str]) -> models.QueryLog:
    entry = models.QueryLog(
        query=query,
        answer=answer,
        route_used=route_used,
        grounded=grounded,
        retry_count=retry_count,
    )
    db.add(entry)
    db.flush()  # get entry.id before commit

    for src in sources:
        db.add(models.QuerySource(query_log_id=entry.id, content_snippet=src[:2000]))

    db.commit()
    db.refresh(entry)
    return entry


def get_recent_queries(db: Session, limit: int = 20):
    return (
        db.query(models.QueryLog)
        .order_by(models.QueryLog.created_at.desc())
        .limit(limit)
        .all()
    )


def register_document(db: Session, title: str, source: str, category: str = None):
    doc = models.Document(title=title, source=source, category=category)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def save_eval_result(db: Session, question: str, expected: str, actual: str,
                      grounded: bool, passed: bool):
    result = models.EvalResult(
        question=question,
        expected_answer=expected,
        actual_answer=actual,
        grounded=grounded,
        passed=passed,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
