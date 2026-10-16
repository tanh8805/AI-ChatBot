from typing import Optional
from src.base import BaseLLMProvider
from src.config import Config, get_settings
from src.gemini import GeminiProvider


class LLMFactory:
    @staticmethod
    def create_provider(config: Optional[Config] = None) -> BaseLLMProvider:
        cfg = config or get_settings()
        provider = cfg.provider.strip().lower()

        if provider == "gemini":
            return GeminiProvider(
                api_key=cfg.gemini_api_key,
                model_name=cfg.model_name,
                temperature=cfg.temperature,
                max_output_tokens=cfg.max_output_tokens,
                system_prompt=cfg.system_prompt,
            )

        raise ValueError(f"Provider '{cfg.provider}' hiện chưa được hỗ trợ.")


def get_llm(config: Optional[Config] = None) -> BaseLLMProvider:
    return LLMFactory.create_provider(config)
