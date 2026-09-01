from app.utils.logger import get_logger

logger = get_logger(__name__)


def retriever_agent_web(query: str) -> list[str]:
    """
    Web search fallback. Uses DuckDuckGo by default (no API key needed).
    Swap in Tavily / SerpAPI / Bing here for production use.
    """
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
        search = DuckDuckGoSearchRun()
        result = search.run(query)
        logger.info("Web search agent returned a result")
        return [result]
    except Exception as e:
        logger.error(f"Web search failed: {e}")
        return []
