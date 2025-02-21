from __future__ import annotations
from typing import Final, Optional
from Interpreter import Interpreter
from LoxCallable import LoxCallable
from Stmt import Function
from Environment import Environment
from Return import Return
from LoxInstance import LoxInstance


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function, closure: Environment, is_initializer: bool) -> None:
        super().__init__()
        self._closure: Final[Environment] = closure
        self._declaration: Final[Function] = declaration
        self._is_initializer: Final[bool] = is_initializer

    def bind(self, instance: LoxInstance):
        environment = Environment(self._closure)
        environment.define("this", instance)
        return LoxFunction(self._declaration, environment, self._is_initializer)

    def call(
        self, interpreter: Interpreter, arguments: list[object]
    ) -> Optional[object]:
        environment: Environment = Environment(self._closure)
        for idx, param in enumerate(self._declaration.params):
            environment.define(param.lexeme, arguments[idx])

        try:
            interpreter.execute_block(self._declaration.body, environment)
        except Return as return_value:
            if self._is_initializer:
                return self._closure.get_at(0, "this")
            return return_value.value

        if self._is_initializer:
            return self._closure.get_at(0, "this")

    def arity(self) -> int:
        return len(self._declaration.params)

    def __str__(self) -> str:
        return f"<fn {self._declaration.name.lexeme}>"
