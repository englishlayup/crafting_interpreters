from TokenTypes import TokenType
from typing import Final


class Token:
    def __init__(
        self,
        type: TokenType,
        lexeme: str,
        literal: object,
        line: int,
    ) -> None:
        self.type: Final[TokenType] = type
        self.lexeme: Final[str] = lexeme
        self.literal: Final[object] = literal
        self.line: Final[int] = line

    def __str__(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal}"
