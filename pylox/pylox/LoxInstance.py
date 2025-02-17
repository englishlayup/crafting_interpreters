from __future__ import annotations
from typing import TYPE_CHECKING, Final
from RuntimeError import RuntimeError

from Token import Token


if TYPE_CHECKING:
    from LoxClass import LoxClass


class LoxInstance:
    def __init__(self, klass: LoxClass) -> None:
        self._klass = klass
        self._fields: Final[dict[str, object]] = {}

    def __str__(self) -> str:
        return self._klass.name + " instance"

    def get(self, name: Token) -> object:
        if name.lexeme in self._fields:
            return self._fields[name.lexeme]

        raise RuntimeError(name, f"Undefined property '{name.lexeme}'.")
