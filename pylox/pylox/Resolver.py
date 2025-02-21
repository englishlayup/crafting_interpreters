from enum import Enum, auto
from typing import Callable, Final, override
from Expr import (
    Assign,
    Binary,
    Call,
    Expr,
    Get,
    Grouping,
    Literal,
    Logical,
    Set,
    This,
    Unary,
    Variable,
    Visitor as ExprVistor,
)
from Stmt import (
    Block,
    Class,
    Expression,
    Function,
    If,
    Print,
    Return,
    Stmt,
    Var,
    Visitor as StmtVisitor,
    While,
)
from Interpreter import Interpreter
from Token import Token


class _FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()
    INITIALIZER = auto()
    METHOD = auto()

class _ClassType(Enum):
    NONE = auto()
    CLASS = auto()

class Resolver(ExprVistor[None], StmtVisitor[None]):
    def __init__(
        self,
        interpreter: Interpreter,
        error: Callable[[Token, str], None],
    ) -> None:
        self._interpreter: Final[Interpreter] = interpreter
        self._scopes: Final[list[dict[str, bool]]] = []
        self._error: Callable[[Token, str], None] = error
        self._current_function: _FunctionType = _FunctionType.NONE
        self._current_class: _ClassType = _ClassType.NONE

    @override
    def visit_Block_Stmt(self, stmt: Block) -> None:
        self._begin_scope()
        self.resolve(stmt.statements)
        self._end_scope()

    @override
    def visit_Class_Stmt(self, stmt: Class) -> None:
        enclosing_class: _ClassType = self._current_class
        self._current_class = _ClassType.CLASS
        self._declare(stmt.name)
        self._define(stmt.name)

        self._begin_scope()
        self._scopes[-1]["this"] = True

        for method in stmt.methods:
            declaration = _FunctionType.METHOD
            if method.name.lexeme == "init":
                declaration = _FunctionType.INITIALIZER
            self._resolve_function(method, declaration)

        self._end_scope()
        self._current_class = enclosing_class

    @override
    def visit_Var_Stmt(self, stmt: Var) -> None:
        self._declare(stmt.name)
        if stmt.initializer:
            self._resolve(stmt.initializer)
        self._define(stmt.name)

    @override
    def visit_Variable_Expr(self, expr: Variable) -> None:
        if self._scopes and self._scopes[-1].get(expr.name.lexeme) is False:
            self._error(expr.name, "Can't read local variable in its own initializer.")

        self._resolve_local(expr, expr.name)

    @override
    def visit_Assign_Expr(self, expr: Assign) -> None:
        self._resolve(expr.value)
        self._resolve_local(expr, expr.name)

    @override
    def visit_Function_Stmt(self, stmt: Function) -> None:
        self._declare(stmt.name)
        self._define(stmt.name)
        self._resolve_function(stmt, _FunctionType.FUNCTION)

    @override
    def visit_Expression_Stmt(self, stmt: Expression) -> None:
        self._resolve(stmt.expression)

    @override
    def visit_If_Stmt(self, stmt: If) -> None:
        self._resolve(stmt.condition)
        self._resolve(stmt.thenBranch)
        if stmt.elseBranch:
            self._resolve(stmt.elseBranch)

    @override
    def visit_Print_Stmt(self, stmt: Print) -> None:
        self._resolve(stmt.expression)

    @override
    def visit_Return_Stmt(self, stmt: Return) -> None:
        if self._current_function == _FunctionType.NONE:
            self._error(stmt.keyword, "Can't return from top-level code.")
        if stmt.value:
            if self._current_function == _FunctionType.INITIALIZER:
                self._error(stmt.keyword, "Can't return a value from an initializer.")
            self._resolve(stmt.value)

    @override
    def visit_While_Stmt(self, stmt: While) -> None:
        self._resolve(stmt.condition)
        self._resolve(stmt.body)

    @override
    def visit_Binary_Expr(self, expr: Binary) -> None:
        self._resolve(expr.left)
        self._resolve(expr.right)

    @override
    def visit_Call_Expr(self, expr: Call) -> None:
        self._resolve(expr.callee)
        for argument in expr.arguments:
            self._resolve(argument)

    @override
    def visit_Get_Expr(self, expr: Get) -> None:
        self._resolve(expr.object)

    @override
    def visit_Set_Expr(self, expr: Set) -> None:
        self._resolve(expr.object)
        self._resolve(expr.value)

    @override
    def visit_This_Expr(self, expr: This) -> None:
        if self._current_class == _ClassType.NONE:
            self._error(expr.keyword, "Can't use 'this' outside of a class.")
            return
        self._resolve_local(expr, expr.keyword)

    @override
    def visit_Grouping_Expr(self, expr: Grouping) -> None:
        self._resolve(expr.expression)

    @override
    def visit_Literal_Expr(self, expr: Literal) -> None:
        _ = expr
        return

    @override
    def visit_Logical_Expr(self, expr: Logical) -> None:
        self._resolve(expr.left)
        self._resolve(expr.right)

    @override
    def visit_Unary_Expr(self, expr: Unary) -> None:
        self._resolve(expr.right)

    def resolve(self, statements: list[Stmt]):
        for statement in statements:
            self._resolve(statement)

    def _resolve(self, r: Stmt | Expr):
        r.accept(self)

    def _begin_scope(self):
        self._scopes.append({})

    def _end_scope(self):
        self._scopes.pop()

    def _declare(self, name: Token):
        if not self._scopes:
            return
        scope: dict[str, bool] = self._scopes[-1]
        if scope.get(name.lexeme):
            self._error(name, "Already a variable with this name in this scope.")
        scope[name.lexeme] = False

    def _define(self, name: Token):
        if not self._scopes:
            return
        self._scopes[-1][name.lexeme] = True

    def _resolve_local(self, expr: Expr, name: Token):
        for i in range(len(self._scopes) - 1, -1, -1):
            if self._scopes[i].get(name.lexeme) is not None:
                self._interpreter.resolve(expr, len(self._scopes) - 1 - i)
                return

    def _resolve_function(self, function: Function, function_type: _FunctionType):
        enclosing_function: _FunctionType = self._current_function
        self._current_function = function_type
        self._begin_scope()
        for param in function.params:
            self._declare(param)
            self._define(param)
        self.resolve(function.body)
        self._end_scope()
        self._current_function = enclosing_function
