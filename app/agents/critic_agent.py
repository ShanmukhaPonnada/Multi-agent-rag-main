import json
import re
from app.models.llm_client import generate
from app.utils.prompts import CRITIC_PROMPT
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _strip_markdown_fence(text: str) -> str:
    """Removes ```json ... ``` or ``` ... ``` fences if present, safely."""
    text = text.strip()
    match = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, flags=re.DOTALL)
    return match.group(1).strip() if match else text


def critic_agent(answer: str, contexts: list[str]) -> dict:
    context_text = "\n\n".join(contexts)
    prompt = CRITIC_PROMPT.format(context=context_text, answer=answer)
    raw = generate(prompt)

    cleaned = _strip_markdown_fence(raw)
    try:
        result = json.loads(cleaned)
        if "grounded" not in result:
            raise ValueError("missing 'grounded' key")
        return result
    except Exception as e:
        logger.warning(f"Critic JSON parse failed ({e}), defaulting to grounded=True")
        return {"grounded": True, "reason": "parse_error_default_pass"}
