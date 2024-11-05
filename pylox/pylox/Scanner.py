from typing import Callable, Final
from Token import Token
from TokenTypes import TokenType


class Scanner:
    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source: str, error: Callable[[int, str], None]) -> None:
        self._source: Final[str] = source
        self._tokens: Final[list[Token]] = []
        self._start = 0
        self._current = 0
        self._line = 1
        self._error: Final[Callable[[int, str], None]] = error

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self._start = self._current
            self._scan_token()

        self._tokens.append(Token(TokenType.EOF, "", None, self._line))
        return self._tokens

    def _is_at_end(self) -> bool:
        return self._current >= len(self._source)

    def _scan_token(self) -> None:
        c: str = self._advance()
        match c:
            case "(":
                self._add_token(TokenType.LEFT_PAREN)
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
            case "{":
                self._add_token(TokenType.LEFT_BRACE)
            case "}":
                self._add_token(TokenType.RIGHT_BRACE)
            case ",":
                self._add_token(TokenType.COMMA)
            case ".":
                self._add_token(TokenType.DOT)
            case "-":
                self._add_token(TokenType.MINUS)
            case "+":
                self._add_token(TokenType.PLUS)
            case ";":
                self._add_token(TokenType.SEMICOLON)
            case "*":
                self._add_token(TokenType.STAR)
            case "!":
                self._add_token(
                    TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
                )
            case ">":
                self._add_token(
                    TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
                )
            case "<":
                self._add_token(
                    TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
                )
            case "=":
                self._add_token(
                    TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
                )
            case "/":
                if self._match("/"):
                    while self._peek() != "\n" and not self._is_at_end():
                        self._advance()
                else:
                    self._add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self._line += 1
            case '"':
                self._string()
            case _:
                if self._is_digit(c):
                    self._number()
                elif self._is_alpha(c):
                    self._identifier()
                else:
                    self._error(self._line, "Unexpected character.")

    def _add_token(self, type: TokenType, literal: object = None) -> None:
        lexeme = self._source[self._start : self._current]
        self._tokens.append(Token(type, lexeme, literal, self._line))

    def _advance(self) -> str:
        c: str = self._source[self._current]
        self._current += 1
        return c

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self._source[self._current]

    def _peek_next(self) -> str:
        if self._current + 1 >= len(self._source):
            return "\0"
        return self._source[self._current + 1]

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        if self._source[self._current] != expected:
            return False

        self._current += 1
        return True

    def _string(self) -> None:
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self._line += 1
            self._advance()

        if self._is_at_end():
            self._error(self._line, "Unterminated string.")
            return

        # The closing quote
        self._advance()

        # Trim the surrounding quotes
        value = self._source[self._start + 1 : self._current - 1]

        self._add_token(TokenType.STRING, value)

    def _is_digit(self, c: str) -> bool:
        return len(c) == 1 and c.isdigit()

    def _is_alpha(self, c: str) -> bool:
        return len(c) == 1 and (c.isalpha() or c == "_")

    def _is_alpha_numeric(self, c: str) -> bool:
        return self._is_alpha(c) or self._is_digit(c)

    def _number(self) -> None:
        while self._is_digit(self._peek()):
            self._advance()

        # Look for a fractional part
        if self._peek() == "." and self._is_digit(self._peek_next()):
            # Consume the '.'
            self._advance()
            while self._peek().isdigit():
                self._advance()

        value = float(self._source[self._start : self._current])

        self._add_token(TokenType.NUMBER, value)

    def _identifier(self):
        while self._is_alpha_numeric(self._peek()):
            self._advance()

        text = self._source[self._start : self._current]

        type = Scanner.keywords.get(text)

        if not type:
            type = TokenType.IDENTIFIER

        self._add_token(type)
