from functools import lru_cache

from app.llm.deepseek_provider import DeepSeekLLMProvider
from app.llm.provider import LLMProvider


@lru_cache(maxsize=1)
def get_llm_provider() -> LLMProvider:
    return DeepSeekLLMProvider()
