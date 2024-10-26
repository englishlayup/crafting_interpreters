from typing import Final

from Token import Token
from RuntimeError import RuntimeError


class Environment:
    def __init__(self) -> None:
        self._values: Final[dict[str, object]] = {}

    def define(self, name: str, value: object):
        self._values[name] = value

    def get(self, name: Token):
        if self._values.get(name.lexeme):
            return self._values[name.lexeme]

        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")
