from typing import Final, Optional

from Expr import Binary, Expr, Grouping, Literal, Unary
from Lox import Lox
from Token import Token
from TokenTypes import TokenType


class Parser:
    class ParseError(RuntimeError): ...

    def __init__(self, tokens: list[Token]) -> None:
        self._tokens: Final[list[Token]] = tokens
        self._current: int = 0

    def parse(self) -> Optional[Expr]:
        try:
            return self._expression()
        except self.ParseError:
            return None

    def _expression(self):
        return self._equality()

    def _equality(self) -> Expr:
        # equality       → comparison ( ( "!=" | "==" ) comparison )* ;
        expr: Expr = self._comparision()

        while self._match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator: Token = self._previous()
            right: Expr = self._comparision()
            expr = Binary(expr, operator, right)

        return expr

    def _comparision(self) -> Expr:
        # comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
        expr: Expr = self._term()

        while self._match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator: Token = self._previous()
            right: Expr = self._term()
            expr = Binary(expr, operator, right)

        return expr

    def _term(self) -> Expr:
        # term           → factor ( ( "-" | "+" ) factor )* ;
        expr: Expr = self._factor()
        while self._match(
            TokenType.MINUS,
            TokenType.PLUS,
        ):
            operator: Token = self._previous()
            right: Expr = self._factor()
            expr = Binary(expr, operator, right)

        return expr

    def _factor(self) -> Expr:
        # factor         → unary ( ( "/" | "*" ) unary )* ;
        expr: Expr = self._unary()

        while self._match(
            TokenType.SLASH,
            TokenType.STAR,
        ):
            operator: Token = self._previous()
            right: Expr = self._unary()
            expr = Binary(expr, operator, right)

        return expr

    def _unary(self) -> Expr:
        # unary          → ( "!" | "-" ) unary
        #                  | primary ;
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator: Token = self._previous()
            right: Expr = self._unary()
            expr = Unary(operator, right)
            return expr
        else:
            return self._primary()

    def _primary(self) -> Expr:
        # primary        → NUMBER | STRING | "true" | "false" | "nil"
        #                  | "(" expression ")" ;
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.NIL):
            return Literal(None)

        if self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().literal)

        if self._match(TokenType.LEFT_PAREN):
            expr: Expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self._error(self._peek(), "Expect expression.")

    def _consume(self, type: TokenType, message: str):
        if self._check(type):
            return self._advance()

        raise self._error(self._peek(), message)

    def _error(self, token: Token, message: str) -> ParseError:
        Lox.error(token.line, message)
        return self.ParseError()

    def _synchronize(self) -> None:
        self._advance()

        while not self._is_at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return

            match self._peek().type:
                case (
                    TokenType.CLASS
                    | TokenType.FUN
                    | TokenType.VAR
                    | TokenType.FOR
                    | TokenType.IF
                    | TokenType.WHILE
                    | TokenType.PRINT
                    | TokenType.RETURN
                ):
                    return
                case _:
                    self._advance()

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
