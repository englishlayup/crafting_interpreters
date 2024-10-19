from typing import Final

from Token import Token


class RuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.token: Final[Token] = token
