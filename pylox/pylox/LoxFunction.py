from __future__ import annotations
from typing import Final, Optional
from Interpreter import Interpreter
from LoxCallable import LoxCallable
from Stmt import Function
from Environment import Environment
from Return import Return


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function, closure: Environment) -> None:
        super().__init__()
        self._closure: Final[Environment] = closure
        self._declaration: Final[Function] = declaration

    def call(
        self, interpreter: Interpreter, arguments: list[object]
    ) -> Optional[object]:
        environment: Environment = Environment(self._closure)
        for idx, param in enumerate(self._declaration.params):
            environment.define(param.lexeme, arguments[idx])

        try:
            interpreter.execute_block(self._declaration.body, environment)
        except Return as return_value:
            return return_value.value

    def arity(self) -> int:
        return len(self._declaration.params)

    def __str__(self) -> str:
        return f"<fn {self._declaration.name.lexeme}>"
