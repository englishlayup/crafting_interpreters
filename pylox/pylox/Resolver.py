from typing import Final, override
from Expr import Assign, Expr, Variable, Visitor as ExprVistor
from Stmt import Block, Function, Stmt, Var, Visitor as StmtVisitor
from Interpreter import Interpreter
from Token import Token
from Lox import Lox


class Resolver(ExprVistor[None], StmtVisitor[None]):
    def __init__(self, interpreter: Interpreter) -> None:
        self._interpreter: Final[Interpreter] = interpreter
        self._scopes: Final[list[dict[str, bool]]] = []

    @override
    def visit_Block_Stmt(self, stmt: Block) -> None:
        self._begin_scope()
        self.resolve(stmt.statements)
        self._end_scope()

    @override
    def visit_Var_Stmt(self, stmt: Var) -> None:
        self._declare(stmt.name)
        if stmt.initializer:
            self._resolve(stmt.initializer)
        self._define(stmt.name)

    @override
    def visit_Variable_Expr(self, expr: Variable) -> None:
        if not self._scopes and not self._scopes[0][expr.name.lexeme]:
            Lox.error(expr.name, "Can't read local variable in its own initializer.")

        self._resolve_local(expr, expr.name)

    @override
    def visit_Assign_Expr(self, expr: Assign) -> None:
        self._resolve(expr.value)
        self._resolve_local(expr, expr.name)

    @override
    def visit_Function_Stmt(self, stmt: Function) -> None:
        self._declare(stmt.name)
        self._define(stmt.name)

        self._resolve_function(stmt)

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
        scope = self._scopes[-1]
        scope[name.lexeme] = False

    def _define(self, name: Token):
        if not self._scopes:
            return
        self._scopes[-1][name.lexeme] = True

    def _resolve_local(self, expr: Expr, name: Token):
        for i in range(len(self._scopes) - 1, -1, -1):
            if self._scopes[i].get(name.lexeme):
                self._interpreter.resolve(expr, len(self.scopes) - 1 - i)

    def _resolve_function(self, function: Function):
        self._begin_scope()
        for param in function.params:
            self._declare(param)
            self._define(param)
        self.resolve(function.body)
        self._end_scope()
