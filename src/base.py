from abc import ABC, abstractmethod
from typing import Iterator, List, Literal, Optional, TypedDict


class ChatMessage(TypedDict):
    role: Literal["user", "model"]
    parts: List[str]


class BaseLLMProvider(ABC):
    @abstractmethod
    def generate(
        self,
        messages: List[ChatMessage],
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        pass

    @abstractmethod
    def stream_generate(
        self,
        messages: List[ChatMessage],
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> Iterator[str]:
        pass
