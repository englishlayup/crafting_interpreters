from __future__ import annotations
from typing import Final, Optional, override

from LoxCallable import LoxCallable
from Interpreter import Interpreter
from LoxInstance import LoxInstance
from LoxFunction import LoxFunction
from RuntimeError import RuntimeError


class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: dict[str, LoxFunction]) -> None:
        self.name: Final[str] = name
        self._methods: Final[dict[str, LoxFunction]] = methods

    def __str__(self) -> str:
        return self.name

    def find_method(self, name: str) -> Optional[LoxFunction]:
        if name in self._methods:
            return self._methods[name]

        return None

    @override
    def call(
        self, interpreter: Interpreter, arguments: list[object]
    ) -> Optional[object]:
        instance: LoxInstance = LoxInstance(self)
        return instance

    @override
    def arity(self) -> int:
        return 0
