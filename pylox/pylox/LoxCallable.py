from abc import ABC, abstractmethod
from typing import Optional

from Interpreter import Interpreter


class LoxCallable(ABC):
    @abstractmethod
    def arity(self) -> int: ...

    @abstractmethod
    def call(
        self, interpreter: Interpreter, arguments: list[object]
    ) -> Optional[object]: ...
