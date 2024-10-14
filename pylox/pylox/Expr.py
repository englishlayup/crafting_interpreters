from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Final, override

from Token import Token


class Expr(ABC):
    @abstractmethod
    def accept[R](self, visitor: Visitor[R]) -> R: ...


class Visitor[R]:
    @abstractmethod
    def visit_Binary_Expr(self, expr: Binary) -> R: ...

    @abstractmethod
    def visit_Grouping_Expr(self, expr: Grouping) -> R: ...

    @abstractmethod
    def visit_Literal_Expr(self, expr: Literal) -> R: ...

    @abstractmethod
    def visit_Unary_Expr(self, expr: Unary) -> R: ...


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        super().__init__()
        self.left: Final[Expr] = left
        self.operator: Final[Token] = operator
        self.right: Final[Expr] = right

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_Binary_Expr(self)


class Grouping(Expr):
    def __init__(self, expression: Expr):
        super().__init__()
        self.expression: Final[Expr] = expression

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_Grouping_Expr(self)


class Literal(Expr):
    def __init__(self, value: object):
        super().__init__()
        self.value: Final[object] = value

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_Literal_Expr(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        super().__init__()
        self.operator: Final[Token] = operator
        self.right: Final[Expr] = right

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_Unary_Expr(self)
