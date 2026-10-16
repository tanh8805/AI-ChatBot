from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Optional
from src.base import BaseLLMProvider, ChatMessage
from src.config import get_settings
from src.exceptions import ChatBotError
from src.llm_factory import get_llm


@dataclass
class Session:
    history: List[ChatMessage] = field(default_factory=list)
    system_prompt: Optional[str] = None


class ChatBot:
    def __init__(self, llm: Optional[BaseLLMProvider] = None, max_history: Optional[int] = None):
        self.settings = get_settings()
        self.llm = llm or get_llm()
        self.max_history = max_history or self.settings.max_history
        self._sessions: Dict[str, Session] = {}

    def get_session(self, session_id: str = "default") -> Session:
        if session_id not in self._sessions:
            self._sessions[session_id] = Session()
        return self._sessions[session_id]

    def get_history(self, session_id: str = "default") -> List[ChatMessage]:
        return self.get_session(session_id).history

    def set_persona(self, session_id: str, prompt: str) -> None:
        self.get_session(session_id).system_prompt = prompt.strip()

    def get_persona(self, session_id: str) -> str:
        session = self.get_session(session_id)
        if session.system_prompt is not None:
            return session.system_prompt
        return self.settings.system_prompt

    def _trim_history(self, session_id: str) -> None:
        session = self.get_session(session_id)
        if len(session.history) > self.max_history:
            session.history = session.history[-self.max_history:]

    def ask(self, user_input: str, session_id: str = "default") -> str:
        text = user_input.strip()
        if not text:
            return ""

        session = self.get_session(session_id)
        session.history.append({"role": "user", "parts": [text]})
        self._trim_history(session_id)

        reply = self.llm.generate(
            messages=session.history,
            system_prompt=self.get_persona(session_id),
        )
        session.history.append({"role": "model", "parts": [reply]})
        self._trim_history(session_id)
        return reply

    def ask_stream(self, user_input: str, session_id: str = "default") -> Iterator[str]:
        text = user_input.strip()
        if not text:
            return

        session = self.get_session(session_id)
        session.history.append({"role": "user", "parts": [text]})
        self._trim_history(session_id)

        full_reply: List[str] = []
        for chunk in self.llm.stream_generate(
            messages=session.history,
            system_prompt=self.get_persona(session_id),
        ):
            full_reply.append(chunk)
            yield chunk

        session.history.append({"role": "model", "parts": ["".join(full_reply)]})
        self._trim_history(session_id)

    def clear(self, session_id: str = "default") -> None:
        if session_id in self._sessions:
            self._sessions[session_id].history.clear()

    def list_sessions(self) -> List[str]:
        return list(self._sessions.keys())

    def delete_session(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
