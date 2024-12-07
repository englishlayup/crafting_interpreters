from __future__ import annotations
from typing import Optional
from Interpreter import Interpreter
from LoxCallable import LoxCallable
from Stmt import Function
from Environment import Environment


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function) -> None:
        super().__init__()
        self._declaration: Function = declaration

    def call(
        self, interpreter: Interpreter, arguments: list[object]
    ) -> Optional[object]:
        environment: Environment = Environment(interpreter.globals)
        for idx, param in enumerate(self._declaration.params):
            environment.define(param.lexeme, arguments[idx])

        interpreter.execute_block(self._declaration.body, environment)

    def arity(self) -> int:
        return len(self._declaration.params)

    def __str__(self) -> str:
        return f"<fn {self._declaration.name.lexeme}>"
