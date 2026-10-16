from typing import Iterator, List
from google import genai
from google.genai import errors, types
from src.base import BaseLLMProvider, ChatMessage
from src.exceptions import (
    AuthenticationError,
    ChatBotError,
    ModelNotFoundError,
    NetworkError,
    RateLimitError,
    ServerError,
)


class GeminiProvider(BaseLLMProvider):
    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-2.5-flash",
        temperature: float = 0.7,
        max_output_tokens: int = 2048,
        system_prompt: str = "",
    ):
        if not api_key:
            raise AuthenticationError("GEMINI_API_KEY không được để trống. Vui lòng cấu hình trong file .env")

        self.api_key = api_key
        self.model_name = model_name
        self.client = genai.Client(api_key=self.api_key)

        self.config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            system_instruction=system_prompt if system_prompt else None,
        )

    def _handle_error(self, e: Exception) -> None:
        if isinstance(e, errors.APIError):
            code = getattr(e, "code", 0) or 0
            msg = str(getattr(e, "message", "") or str(e))
            if code in (401, 403) or "API_KEY_INVALID" in msg:
                raise AuthenticationError("API Key không hợp lệ hoặc thiếu quyền truy cập.", details=msg) from e
            elif code == 404 or "NOT_FOUND" in msg:
                raise ModelNotFoundError(f"Model '{self.model_name}' không tồn tại hoặc không được hỗ trợ.", details=msg) from e
            elif code == 429 or "RESOURCE_EXHAUSTED" in msg:
                raise RateLimitError("Đã vượt quá hạn mức yêu cầu (Rate Limit / Quota).", details=msg) from e
            elif code >= 500:
                raise ServerError("Máy chủ Google Gemini đang gặp sự cố tạm thời.", details=msg) from e
            raise ChatBotError(f"Lỗi phản hồi từ Gemini API ({code}): {msg}", details=str(e)) from e
        elif isinstance(e, (ConnectionError, TimeoutError, OSError)):
            raise NetworkError("Lỗi kết nối mạng tới Google Gemini.", details=str(e)) from e
        raise ChatBotError(f"Lỗi không xác định: {str(e)}", details=str(e)) from e

    def generate(self, messages: List[ChatMessage], **kwargs) -> str:
        try:
            contents = [
                types.Content(
                    role=msg["role"],
                    parts=[types.Part.from_text(text=p) for p in msg["parts"]],
                )
                for msg in messages
            ]
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=self.config,
            )
            return response.text or ""
        except Exception as e:
            self._handle_error(e)
            return ""

    def stream_generate(self, messages: List[ChatMessage], **kwargs) -> Iterator[str]:
        try:
            contents = [
                types.Content(
                    role=msg["role"],
                    parts=[types.Part.from_text(text=p) for p in msg["parts"]],
                )
                for msg in messages
            ]
            response_stream = self.client.models.generate_content_stream(
                model=self.model_name,
                contents=contents,
                config=self.config,
            )
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            self._handle_error(e)
