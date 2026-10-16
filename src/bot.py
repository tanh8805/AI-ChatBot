from typing import Iterator, List, Optional
from src.base import BaseLLMProvider, ChatMessage
from src.config import get_settings
from src.exceptions import ChatBotError
from src.llm_factory import get_llm


class ChatBot:
    def __init__(self, llm: Optional[BaseLLMProvider] = None, max_history: Optional[int] = None):
        self.settings = get_settings()
        self.llm = llm or get_llm()
        self.max_history = max_history or self.settings.max_history
        self.history: List[ChatMessage] = []

    def _trim_history(self) -> None:
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def ask(self, user_input: str) -> str:
        text = user_input.strip()
        if not text:
            return ""

        self.history.append({"role": "user", "parts": [text]})
        self._trim_history()

        reply = self.llm.generate(self.history)
        self.history.append({"role": "model", "parts": [reply]})
        self._trim_history()
        return reply

    def ask_stream(self, user_input: str) -> Iterator[str]:
        text = user_input.strip()
        if not text:
            return

        self.history.append({"role": "user", "parts": [text]})
        self._trim_history()

        full_reply: List[str] = []
        for chunk in self.llm.stream_generate(self.history):
            full_reply.append(chunk)
            yield chunk

        self.history.append({"role": "model", "parts": ["".join(full_reply)]})
        self._trim_history()

    def clear(self) -> None:
        self.history.clear()

