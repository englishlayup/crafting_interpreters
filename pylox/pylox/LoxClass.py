from __future__ import annotations
from typing import Final, Optional, override

from LoxCallable import LoxCallable
from Interpreter import Interpreter
from LoxInstance import LoxInstance


class LoxClass(LoxCallable):
    def __init__(self, name: str) -> None:
        self.name: Final[str] = name

    def __str__(self) -> str:
        return self.name

    @override
    def call(self, interpreter: Interpreter, arguments: list[object]) -> Optional[object]:
        instance: LoxInstance = LoxInstance(self)
        return instance

    @override
    def arity(self) -> int:
        return 0
