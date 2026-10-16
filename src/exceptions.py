class ChatBotError(Exception):
    def __init__(self, message: str, details: str = ""):
        super().__init__(message)
        self.message = message
        self.details = details


class AuthenticationError(ChatBotError):
    pass


class RateLimitError(ChatBotError):
    pass


class ModelNotFoundError(ChatBotError):
    pass


class ContentFilterError(ChatBotError):
    pass


class NetworkError(ChatBotError):
    pass


class ServerError(ChatBotError):
    pass
