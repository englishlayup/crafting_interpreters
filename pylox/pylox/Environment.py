from __future__ import annotations
from typing import Final, Optional

from Token import Token
from RuntimeError import RuntimeError


class Environment:
    def __init__(self, enclosing: Optional[Environment] = None) -> None:
        self.enclosing: Final[Optional[Environment]] = enclosing
        self._values: Final[dict[str, object]] = {}

    def define(self, name: str, value: object):
        self._values[name] = value

    def get(self, name: Token) -> object:
        if self._values.get(name.lexeme):
            return self._values[name.lexeme]
        if self.enclosing:
            return self.enclosing.get(name)

        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: object):
        if self._values.get(name.lexeme):
            self._values[name.lexeme] = value
            return
        if self.enclosing:
            self.enclosing.assign(name, value)
            return

        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")
