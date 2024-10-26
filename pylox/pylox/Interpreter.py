from typing import override
from Expr import (
    Assign,
    Binary,
    Expr,
    Grouping,
    Literal,
    Unary,
    Variable,
    Visitor as ExprVisitor,
)
from Token import Token
from TokenTypes import TokenType
from RuntimeError import RuntimeError
from Stmt import Expression, Print, Stmt, Var, Visitor as StmtVisitor
from Environment import Environment


class Interpreter(ExprVisitor[object], StmtVisitor[None]):
    def __init__(self) -> None:
        super().__init__()
        self._environment: Environment = Environment()

    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self._execute(statement)
        except RuntimeError as e:
            from Lox import Lox

            Lox.runtime_error(e)

    def _execute(self, statement: Stmt):
        statement.accept(self)

    def _stringify(self, obj: object):
        if obj is None:
            return "nil"

        if obj is True:
            return "true"

        if obj is False:
            return "false"

        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text

        return str(obj)

    @override
    def visit_Binary_Expr(self, expr: Binary) -> object:
        left: object = self._evaluate(expr.left)
        right: object = self._evaluate(expr.right)

        match expr.operator.type:
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return left + right
                if isinstance(left, str) or isinstance(right, str):
                    return self._stringify(left) + self._stringify(right)
                raise RuntimeError(
                    expr.operator,
                    "Both operands must be two numbers or at least one operand has to be a string.",
                )
            case TokenType.MINUS:
                self._check_number_operands(expr.operator, left, right)
                return float(left) - float(right)  # type: ignore[ReportArgumentType]
            case TokenType.STAR:
                self._check_number_operands(expr.operator, left, right)
                return float(left) * float(right)  # type: ignore[ReportArgumentType]
            case TokenType.SLASH:
                self._check_number_operands(expr.operator, left, right)
                if right == 0:
                    raise RuntimeError(
                        expr.operator,
                        "Right operand cannot be 0.",
                    )
                return float(left) / float(right)  # type: ignore[ReportArgumentType]
            case TokenType.LESS:
                self._check_number_operands(expr.operator, left, right)
                return float(left) < float(right)  # type: ignore[ReportArgumentType]
            case TokenType.LESS_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)  # type: ignore[ReportArgumentType]
            case TokenType.GREATER:
                self._check_number_operands(expr.operator, left, right)
                return float(left) > float(right)  # type: ignore[ReportArgumentType]
            case TokenType.GREATER_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)  # type: ignore[ReportArgumentType]
            case TokenType.EQUAL_EQUAL:
                return self._is_equal(left, right)
            case TokenType.BANG_EQUAL:
                return not self._is_equal(left, right)
            case _:
                pass

        # Unreachable
        return None

    def _is_equal(self, a: object, b: object):
        return a == b

    @override
    def visit_Grouping_Expr(self, expr: Grouping) -> object:
        return self._evaluate(expr.expression)

    @override
    def visit_Literal_Expr(self, expr: Literal) -> object:
        return expr.value

    @override
    def visit_Unary_Expr(self, expr: Unary) -> object:
        right: object = self._evaluate(expr.right)

        match expr.operator.type:
            case TokenType.BANG:
                return not self._is_truthy(right)
            case TokenType.MINUS:
                self._check_number_operand(expr.operator, right)
                return -float(right)  # type: ignore[ReportArgumentType]
            case _:
                pass

        # Unreachable
        return None

    @override
    def visit_Variable_Expr(self, expr: Variable) -> object:
        return self._environment.get(expr.name)

    def _check_number_operand(self, operator: Token, operand: object) -> None:
        if isinstance(operand, float):
            return
        raise RuntimeError(operator, "Operand must be a number.")

    def _check_number_operands(
        self,
        operator: Token,
        left: object,
        right: object,
    ) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeError(operator, "Operands must be numbers.")

    def _is_truthy(self, obj: object) -> bool:
        if obj is None:
            return False
        if isinstance(obj, bool):
            return bool(obj)
        return True

    def _evaluate(self, expr: Expr):
        return expr.accept(self)

    @override
    def visit_Expression_Stmt(self, stmt: Expression) -> None:
        self._evaluate(stmt.expression)

    @override
    def visit_Print_Stmt(self, stmt: Print) -> None:
        value: object = self._evaluate(stmt.expression)
        print(self._stringify(value))

    @override
    def visit_Var_Stmt(self, stmt: Var) -> None:
        value: object = None
        if stmt.initializer:
            value = self._evaluate(stmt.initializer)

        self._environment.define(stmt.name.lexeme, value)

    @override
    def visit_Assign_Expr(self, expr: Assign) -> object:
        value: object = self._evaluate(expr.value)
        self._environment.assign(expr.name, value)
        return value
