from sqlalchemy.orm import Session

from app.agents.router_agent import router_agent
from app.agents.retriever_agent import retriever_agent_internal
from app.agents.web_search_agent import retriever_agent_web
from app.agents.synthesizer_agent import synthesizer_agent
from app.agents.critic_agent import critic_agent
from app.config import MAX_CRITIC_RETRIES
from app.db import crud
from app.utils.logger import get_logger

logger = get_logger(__name__)


def run_pipeline(query: str, db: Session = None) -> dict:
    # 1. Route
    route = router_agent(query)

    # 2. Retrieve
    contexts: list[str] = []
    if route in ("internal_docs", "both"):
        contexts.extend(retriever_agent_internal(query))
    if route in ("web_search", "both"):
        contexts.extend(retriever_agent_web(query))

    # 3. Synthesize
    answer = synthesizer_agent(query, contexts)

    # 4. Verify + retry loop
    grounded = True
    retry_count = 0
    for attempt in range(MAX_CRITIC_RETRIES):
        check = critic_agent(answer, contexts)
        grounded = check.get("grounded", True)
        if grounded:
            break
        logger.info(f"Answer not grounded (reason: {check.get('reason')}), retrying...")
        answer = synthesizer_agent(query, contexts)
        retry_count += 1

    result = {
        "answer": answer,
        "sources": contexts,
        "grounded": grounded,
        "route_used": route,
        "retry_count": retry_count,
    }

    # 5. Log to DB if a session was provided
    if db is not None:
        try:
            crud.log_query(
                db,
                query=query,
                answer=answer,
                route_used=route,
                grounded=grounded,
                retry_count=retry_count,
                sources=contexts,
            )
        except Exception as e:
            logger.error(f"Failed to log query to DB: {e}")

    return result
