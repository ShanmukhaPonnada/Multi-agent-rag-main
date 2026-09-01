from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.models.schemas import QueryRequest, AnswerResponse, QueryLogOut
from app.orchestrator.pipeline import run_pipeline
from app.db.database import get_db
from app.db import crud

app = FastAPI(title="Multi-Agent RAG API", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
def ask(request: QueryRequest, db: Session = Depends(get_db)):
    result = run_pipeline(request.query, db=db)
    return result


@app.get("/history", response_model=list[QueryLogOut])
def history(limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_recent_queries(db, limit=limit)
