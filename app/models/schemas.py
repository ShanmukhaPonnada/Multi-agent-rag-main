from pydantic import BaseModel
from typing import List, Optional


class QueryRequest(BaseModel):
    query: str


class AnswerResponse(BaseModel):
    answer: str
    sources: List[str]
    grounded: bool
    route_used: str
    retry_count: int


class QueryLogOut(BaseModel):
    id: int
    query: str
    answer: str
    route_used: Optional[str]
    grounded: bool

    class Config:
        from_attributes = True
