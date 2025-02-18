from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Final, Optional, Type, override
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
    Visitor as ExprVisitor,
)
from Token import Token
from TokenTypes import TokenType
from RuntimeError import RuntimeError
from Stmt import (
    Block,
    Class,
    Expression,
    Function,
    If,
    Print,
    Return as StmtReturn,
    Stmt,
    Var,
    Visitor as StmtVisitor,
    While,
)
from Environment import Environment
from Return import Return

if TYPE_CHECKING:
    from LoxCallable import LoxCallable
    from LoxFunction import LoxFunction
    from LoxClass import LoxClass
    from LoxInstance import LoxInstance
import time


class Interpreter(ExprVisitor[object], StmtVisitor[None]):
    def __init__(
        self,
        callable_interface: Type[LoxCallable],
        function_class: Type[LoxFunction],
        klass_class: Type[LoxClass],
        instance_class: Type[LoxInstance],
    ) -> None:
        super().__init__()
        self.globals: Final[Environment] = Environment()
        self._environment: Environment = self.globals
        self._locals: Final[dict[Expr, int]] = {}
        self._callable_interface: Type[LoxCallable] = callable_interface
        self._function_class: Type[LoxFunction] = function_class
        self._klass_class: Type[LoxClass] = klass_class
        self._instance_class: Type[LoxInstance] = instance_class

        class _NativeFnClock(self._callable_interface):
            @override
            def arity(self) -> int:
                return 0

            @override
            def call(self, interpreter: Interpreter, arguments: list[object]) -> float:
                _ = interpreter
                _ = arguments
                return time.time()

            def __str__(self) -> str:
                return "<native fn>"

        self.globals.define("clock", _NativeFnClock())

    def interpret(
        self,
        statements: list[Stmt],
        runtime_error: Callable[[RuntimeError], None],
    ):
        try:
            for statement in statements:
                self._execute(statement)
        except RuntimeError as e:
            runtime_error(e)

    def _execute(self, statement: Stmt):
        statement.accept(self)

    def resolve(self, expr: Expr, depth: int):
        self._locals[expr] = depth

    def execute_block(self, statements: list[Stmt], environment: Environment):
        previous: Environment = self._environment
        try:
            self._environment = environment

            for statement in statements:
                self._execute(statement)
        finally:
            self._environment = previous

    @override
    def visit_Block_Stmt(self, stmt: Block) -> None:
        self.execute_block(stmt.statements, Environment(self._environment))

    @override
    def visit_Class_Stmt(self, stmt: Class) -> None:
        self._environment.define(stmt.name.lexeme, None)
        methods: dict[str, LoxFunction] = {}
        for method in stmt.methods:
            function = self._function_class(method, self._environment)
            methods[method.name.lexeme] = function
        klass = self._klass_class(stmt.name.lexeme, methods)
        self._environment.assign(stmt.name, klass)

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
                if isinstance(left, str) and isinstance(right, str):
                    return self._stringify(left) + self._stringify(right)
                raise RuntimeError(
                    expr.operator,
                    "Operands must be two numbers or two strings.",
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

    @override
    def visit_Call_Expr(self, expr: Call) -> object:
        callee: object = self._evaluate(expr.callee)

        arguments: list[object] = []
        for argument in expr.arguments:
            arguments.append(self._evaluate(argument))

        if not isinstance(callee, self._callable_interface):
            raise RuntimeError(expr.paren, "Can only call functions and classes.")

        function: LoxCallable = callee

        if len(arguments) != function.arity():
            raise RuntimeError(
                expr.paren,
                f"Expected {function.arity()} arguments but got {len(arguments)}.",
            )

        return function.call(self, arguments)

    def _is_equal(self, a: object, b: object):
        if type(a) is not type(b):
            return False
        return a == b

    @override
    def visit_Get_Expr(self, expr: Get) -> object:
        obj: object = self._evaluate(expr.object)
        if isinstance(obj, self._instance_class):
            return obj.get(expr.name)

        raise RuntimeError(expr.name, "Only instances have properties.")

    @override
    def visit_Grouping_Expr(self, expr: Grouping) -> object:
        return self._evaluate(expr.expression)

    @override
    def visit_Literal_Expr(self, expr: Literal) -> object:
        return expr.value

    @override
    def visit_Logical_Expr(self, expr: Logical) -> object:
        left: object = self._evaluate(expr.left)

        if expr.operator.type == TokenType.OR:
            if self._is_truthy(left):
                return left
        else:
            if not self._is_truthy(left):
                return left

        return self._evaluate(expr.right)

    @override
    def visit_Set_Expr(self, expr: Set) -> object:
        obj: object = self._evaluate(expr.object)

        if not isinstance(obj, self._instance_class):
            raise RuntimeError(expr.name, "Only instances have fields.")

        value: object = self._evaluate(expr.value)
        obj.set(expr.name, value)
        return value

    @override
    def visit_This_Expr(self, expr: This) -> object:
        return self._look_up_variable(expr.keyword, expr)

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
        return self._look_up_variable(expr.name, expr)

    def _look_up_variable(self, name: Token, expr: Expr) -> object:
        distance: Optional[int] = self._locals.get(expr)
        if distance is not None:
            return self._environment.get_at(distance, name.lexeme)
        else:
            return self.globals.get(name)

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
            return obj
        return True

    def _evaluate(self, expr: Expr):
        return expr.accept(self)

    @override
    def visit_Expression_Stmt(self, stmt: Expression) -> None:
        self._evaluate(stmt.expression)

    @override
    def visit_Function_Stmt(self, stmt: Function) -> None:
        function = self._function_class(stmt, self._environment)
        self._environment.define(stmt.name.lexeme, function)

    @override
    def visit_If_Stmt(self, stmt: If) -> None:
        if self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.thenBranch)
        elif stmt.elseBranch:
            self._execute(stmt.elseBranch)
        return None

    @override
    def visit_Print_Stmt(self, stmt: Print) -> None:
        value: object = self._evaluate(stmt.expression)
        print(self._stringify(value))

    @override
    def visit_Return_Stmt(self, stmt: StmtReturn) -> None:
        value: object = None
        if stmt.value:
            value = self._evaluate(stmt.value)

        raise Return(value)

    @override
    def visit_Var_Stmt(self, stmt: Var) -> None:
        value: object = None
        if stmt.initializer:
            value = self._evaluate(stmt.initializer)

        self._environment.define(stmt.name.lexeme, value)

    @override
    def visit_While_Stmt(self, stmt: While) -> None:
        while self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.body)

    @override
    def visit_Assign_Expr(self, expr: Assign) -> object:
        value: object = self._evaluate(expr.value)
        distance: Optional[int] = self._locals.get(expr)
        if distance is not None:
            self._environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)
        return value
