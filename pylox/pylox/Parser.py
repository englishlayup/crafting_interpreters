from typing import Final
from Token import Token
from Expr import Binary, Expr
from TokenTypes import TokenType


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._tokens: Final[list[Token]] = tokens
        self._current: int = 0

    def _expression(self):
        return self._equality()

    def _equality(self) -> Expr:
        expr: Expr = self._comparision()

        while self._match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator: Token = self._previous()
            right: Expr = self._comparision()
            expr = Binary(expr, operator, right)

        return expr

    def _match(self, *types: TokenType) -> bool:
        for type in types:
            if self._check(type):
                self._advance()
                return True
        return False

    def _check(self, type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self._current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._tokens[self._current].type == TokenType.EOF

    def _peek(self) -> Token:
        return self._tokens[self._current]

    def _previous(self) -> Token:
        return self._tokens[self._current - 1]
