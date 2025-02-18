from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Final, override

from Token import Token


class Expr(ABC):
    @abstractmethod
    def accept[R](self, visitor: Visitor[R]) -> R: ...


class Visitor[R]:
    @abstractmethod
    def visit_Assign_Expr(self, expr: Assign) -> R: ...

    @abstractmethod
    def visit_Binary_Expr(self, expr: Binary) -> R: ...

    @abstractmethod
    def visit_Call_Expr(self, expr: Call) -> R: ...

    @abstractmethod
    def visit_Get_Expr(self, expr: Get) -> R: ...

    @abstractmethod
    def visit_Grouping_Expr(self, expr: Grouping) -> R: ...

    @abstractmethod
    def visit_Literal_Expr(self, expr: Literal) -> R: ...

    @abstractmethod
    def visit_Logical_Expr(self, expr: Logical) -> R: ...

    @abstractmethod
    def visit_Set_Expr(self, expr: Set) -> R: ...

    @abstractmethod
    def visit_Unary_Expr(self, expr: Unary) -> R: ...

    @abstractmethod
    def visit_This_Expr(self, expr: This) -> R: ...

    @abstractmethod
    def visit_Variable_Expr(self, expr: Variable) -> R: ...


class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        super().__init__()
        self.name: Final[Token] = name
        self.value: Final[Expr] = value

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_Assign_Expr(self)


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        super().__init__()
        self.left: Final[Expr] = left
        self.operator: Final[Token] = operator
        self.right: Final[Expr] = right

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_Binary_Expr(self)


class Call(Expr):
    def __init__(self, callee: Expr, paren: Token, arguments: list[Expr]):
        super().__init__()
        self.callee: Final[Expr] = callee
        self.paren: Final[Token] = paren
        self.arguments: Final[list[Expr]] = arguments

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_Call_Expr(self)


class Get(Expr):
    def __init__(self, object: Expr, name: Token):
        super().__init__()
        self.object: Final[Expr] = object
        self.name: Final[Token] = name

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_Get_Expr(self)


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


class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        super().__init__()
        self.left: Final[Expr] = left
        self.operator: Final[Token] = operator
        self.right: Final[Expr] = right

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_Logical_Expr(self)


class Set(Expr):
    def __init__(self, object: Expr, name: Token, value: Expr):
        super().__init__()
        self.object: Final[Expr] = object
        self.name: Final[Token] = name
        self.value: Final[Expr] = value

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_Set_Expr(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        super().__init__()
        self.operator: Final[Token] = operator
        self.right: Final[Expr] = right

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_Unary_Expr(self)


class This(Expr):
    def __init__(self, keyword: Token):
        super().__init__()
        self.keyword: Final[Token] = keyword

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_This_Expr(self)


class Variable(Expr):
    def __init__(self, name: Token):
        super().__init__()
        self.name: Final[Token] = name

    @override
    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_Variable_Expr(self)
