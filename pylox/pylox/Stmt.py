from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Final, override

from Token import Token
from Expr import Expr


class Stmt(ABC):
    @abstractmethod
    def accept[R](self, visitor: Visitor[R]) -> R: ...


class Visitor[R]:
    @abstractmethod
    def visit_Block_Stmt(self, stmt: Block) -> R: ...

    @abstractmethod
    def visit_Expression_Stmt(self, stmt: Expression) -> R: ...

    @abstractmethod
    def visit_Print_Stmt(self, stmt: Print) -> R: ...

    @abstractmethod
    def visit_Var_Stmt(self, stmt: Var) -> R: ...


class Block(Stmt):
    def __init__(self, statements: list[Stmt]):
        super().__init__()
        self.statements: Final[list[Stmt]] = statements

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_Block_Stmt(self)


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


class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr):
        super().__init__()
        self.name: Final[Token] = name
        self.initializer: Final[Expr] = initializer

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_Var_Stmt(self)
