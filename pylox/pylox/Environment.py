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

    def get_at(self, distance: int, name: str) -> object:
        return self.ancestor(distance)._values.get(name)

    def assign_at(self, distance: int, name: Token, value: object) -> None:
        self.ancestor(distance)._values[name.lexeme] = value

    def ancestor(self, distance: int) -> Environment:
        environment: Environment = self
        for _ in range(distance):
            if environment.enclosing:
                environment = environment.enclosing

        return environment

    def get(self, name: Token) -> object:
        if name.lexeme in self._values.keys():
            return self._values[name.lexeme]
        if self.enclosing:
            return self.enclosing.get(name)

        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: object):
        if name.lexeme in self._values.keys():
            self._values[name.lexeme] = value
            return
        if self.enclosing:
            self.enclosing.assign(name, value)
            return

        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")
