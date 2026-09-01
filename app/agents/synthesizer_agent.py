from app.models.llm_client import generate
from app.utils.prompts import SYNTHESIZER_PROMPT
from app.utils.logger import get_logger

logger = get_logger(__name__)


def synthesizer_agent(query: str, contexts: list[str]) -> str:
    if not contexts:
        logger.warning("No context available for synthesis")
        return "I don't have enough information in the available sources to answer that."

    context_text = "\n\n".join(contexts)
    prompt = SYNTHESIZER_PROMPT.format(context=context_text, query=query)
    answer = generate(prompt)
    logger.info("Synthesizer produced an answer")
    return answer
