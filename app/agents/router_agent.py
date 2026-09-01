from app.models.llm_client import generate
from app.utils.prompts import ROUTER_PROMPT
from app.utils.logger import get_logger

logger = get_logger(__name__)

VALID_ROUTES = {"internal_docs", "web_search", "both"}


def router_agent(query: str) -> str:
    prompt = ROUTER_PROMPT.format(query=query)
    route = generate(prompt).strip().lower()

    if route not in VALID_ROUTES:
        logger.warning(f"Router returned unexpected route '{route}', defaulting to 'both'")
        route = "both"

    logger.info(f"Routed query to: {route}")
    return route
