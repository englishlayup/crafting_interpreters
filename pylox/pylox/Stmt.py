from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Final, override

from Expr import Expr


class Stmt(ABC):
    @abstractmethod
    def accept[R](self, visitor: Visitor[R]) -> R: ...


class Visitor[R]:
    @abstractmethod
    def visit_Expression_Stmt(self, stmt: Expression) -> R: ...

    @abstractmethod
    def visit_Print_Stmt(self, stmt: Print) -> R: ...


class Expression(Stmt):
    def __init__(self, expression: Expr):
        super().__init__()
        self.expression: Final[Expr] = expression

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_Expression_Stmt(self)


class Print(Stmt):
    def __init__(self, expression: Expr):
        super().__init__()
        self.expression: Final[Expr] = expression

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_Print_Stmt(self)
