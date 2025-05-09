from typing import Callable, Final, Optional

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
    Super,
    This,
    Unary,
    Variable,
)
from Token import Token
from TokenTypes import TokenType
from Stmt import Block, Class, Expression, Function, If, Return, Stmt, Print, Var, While


class Parser:
    class ParseError(RuntimeError): ...

    def __init__(
        self,
        tokens: list[Token],
        parse_error: Callable[[Token, str], None],
    ) -> None:
        self._tokens: Final[list[Token]] = tokens
        self._current: int = 0
        self._parse_error: Final[Callable[[Token, str], None]] = parse_error

    def parse(self) -> list[Stmt]:
        statements: list[Stmt] = []

        while not self._is_at_end():
            statements.append(self._declaration())  # type: ignore[reportArgumentType]

        return statements

    def _expression(self):
        return self._assignment()

    def _assignment(self) -> Expr:
        expr: Expr = self._or()

        if self._match(TokenType.EQUAL):
            equals: Token = self._previous()
            value: Expr = self._assignment()

            if isinstance(expr, Variable):
                return Assign(expr.name, value)
            elif isinstance(expr, Get):
                return Set(expr.object, expr.name, value)

            self._error(equals, "Invalid assignment target.")

        return expr

    def _or(self) -> Expr:
        expr: Expr = self._and()

        while self._match(TokenType.OR):
            operator = self._previous()
            right = self._and()
            expr = Logical(expr, operator, right)

        return expr

    def _and(self) -> Expr:
        expr: Expr = self._equality()

        while self._match(TokenType.AND):
            operator = self._previous()
            right = self._equality()
            expr = Logical(expr, operator, right)

        return expr

    def _declaration(self):
        try:
            if self._match(TokenType.CLASS):
                return self._class_declaration()
            if self._match(TokenType.FUN):
                return self._function("function")
            if self._match(TokenType.VAR):
                return self._var_declaration()
            return self._statement()
        except self.ParseError:
            self._synchronize()
            return None

    def _class_declaration(self) -> Class:
        name = self._consume(TokenType.IDENTIFIER, "Expect class name.")
        super_class: Optional[Variable] = None
        if self._match(TokenType.LESS):
            self._consume(TokenType.IDENTIFIER, "Expect superclass name.")
            super_class = Variable(self._previous())
        self._consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")
        methods: list[Function] = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            methods.append(self._function("method"))

        self._consume(TokenType.RIGHT_BRACE, "Expect '}' after class body.")
        return Class(name, super_class, methods)

    def _function(self, kind: str) -> Function:
        name: Token = self._consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        self._consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")

        arguments: list[Token] = []
        if not self._check(TokenType.RIGHT_PAREN):
            arguments.append(
                self._consume(TokenType.IDENTIFIER, "Expect parameter name.")
            )
            while self._match(TokenType.COMMA):
                if len(arguments) >= 255:
                    self._error(self._peek(), "Can't have more than 255 parameters.")
                arguments.append(
                    self._consume(TokenType.IDENTIFIER, "Expect parameter name.")
                )

        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        self._consume(TokenType.LEFT_BRACE, f"Expect '{{' before {kind} body.")
        body: list[Stmt] = self._block()
        return Function(name, arguments, body)

    def _statement(self) -> Stmt:
        if self._match(TokenType.FOR):
            return self._for_statement()
        if self._match(TokenType.RETURN):
            return self._return_statement()
        if self._match(TokenType.WHILE):
            return self._while_statement()
        if self._match(TokenType.IF):
            return self._if_statement()
        if self._match(TokenType.PRINT):
            return self._print_statement()
        if self._match(TokenType.LEFT_BRACE):
            return Block(self._block())

        return self._expression_statement()

    def _for_statement(self) -> Stmt:
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        initializer: Optional[Stmt]
        if self._match(TokenType.SEMICOLON):
            initializer = None
        elif self._match(TokenType.VAR):
            initializer = self._var_declaration()
        else:
            initializer = self._expression_statement()

        condition: Optional[Expr] = None
        if not self._check(TokenType.SEMICOLON):
            condition = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment: Optional[Expr] = None
        if not self._check(TokenType.RIGHT_PAREN):
            increment = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body: Stmt = self._statement()

        if increment:
            body = Block([body, Expression(increment)])

        if not condition:
            condition = Literal(True)

        body = While(condition, body)

        if initializer:
            body = Block([initializer, body])

        return body

    def _if_statement(self) -> Stmt:
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch: Stmt = self._statement()
        else_branch: Stmt = None  # type: ignore[reportAssignmentType]
        if self._match(TokenType.ELSE):
            else_branch = self._statement()

        return If(condition, then_branch, else_branch)

    def _print_statement(self):
        value: Expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def _return_statement(self) -> Stmt:
        keyword: Token = self._previous()
        value: Expr = None  # type: ignore[reportAssignmentType]
        if not self._check(TokenType.SEMICOLON):
            value = self._expression()

        self._consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return Return(keyword, value)

    def _var_declaration(self):
        name: Token = self._consume(TokenType.IDENTIFIER, "Expect variable name.")

        intializer: Expr = None  # type: ignore[reportAssignmentType]
        if self._match(TokenType.EQUAL):
            intializer = self._expression()

        self._consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, intializer)

    def _while_statement(self):
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self._statement()

        return While(condition, body)

    def _expression_statement(self):
        value: Expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(value)

    def _block(self):
        statements: list[Stmt] = []

        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            statements.append(self._declaration())  # type: ignore[reportArgumentType]

        self._consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def _equality(self) -> Expr:
        # equality       → comparison ( ( "!=" | "==" ) comparison )* ;
        expr: Expr = self._comparision()

        while self._match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator: Token = self._previous()
            right: Expr = self._comparision()
            expr = Binary(expr, operator, right)

        return expr

    def _comparision(self) -> Expr:
        # comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
        expr: Expr = self._term()

        while self._match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator: Token = self._previous()
            right: Expr = self._term()
            expr = Binary(expr, operator, right)

        return expr

    def _term(self) -> Expr:
        # term           → factor ( ( "-" | "+" ) factor )* ;
        expr: Expr = self._factor()
        while self._match(
            TokenType.MINUS,
            TokenType.PLUS,
        ):
            operator: Token = self._previous()
            right: Expr = self._factor()
            expr = Binary(expr, operator, right)

        return expr

    def _factor(self) -> Expr:
        # factor         → unary ( ( "/" | "*" ) unary )* ;
        expr: Expr = self._unary()

        while self._match(
            TokenType.SLASH,
            TokenType.STAR,
        ):
            operator: Token = self._previous()
            right: Expr = self._unary()
            expr = Binary(expr, operator, right)

        return expr

    def _unary(self) -> Expr:
        # unary          → ( "!" | "-" ) unary
        #                  | primary ;
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator: Token = self._previous()
            right: Expr = self._unary()
            return Unary(operator, right)

        return self._call()

    def _call(self) -> Expr:
        expr: Expr = self._primary()

        while True:
            if self._match(TokenType.LEFT_PAREN):
                expr = self._finish_call(expr)
            elif self._match(TokenType.DOT):
                name = self._consume(
                    TokenType.IDENTIFIER, "Expect property name after '.'."
                )
                expr = Get(expr, name)
            else:
                break

        return expr

    def _finish_call(self, expr: Expr) -> Expr:
        arguments: list[Expr] = []

        if not self._check(TokenType.RIGHT_PAREN):
            arguments.append(self._expression())

            while self._match(TokenType.COMMA):
                if len(arguments) >= 255:
                    self._error(self._peek(), "Can't have more than 255 arguments.")
                arguments.append(self._expression())

        paren: Token = self._consume(
            TokenType.RIGHT_PAREN, "Expect ')' after arguments."
        )

        return Call(expr, paren, arguments)

    def _primary(self) -> Expr:
        # primary        → NUMBER | STRING | "true" | "false" | "nil"
        #                  | "(" expression ")" ;
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.NIL):
            return Literal(None)
        if self._match(TokenType.IDENTIFIER):
            return Variable(self._previous())
        if self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().literal)
        if self._match(TokenType.THIS):
            return This(self._previous())

        if self._match(TokenType.LEFT_PAREN):
            expr: Expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        if self._match(TokenType.SUPER):
            keyword = self._previous()
            self._consume(TokenType.DOT, "Expect '.' after 'super'.")
            method = self._consume(TokenType.IDENTIFIER, "Expect superclass method name.")
            return Super(keyword, method)

        raise self._error(self._peek(), "Expect expression.")

    def _consume(self, type: TokenType, message: str):
        if self._check(type):
            return self._advance()

        raise self._error(self._peek(), message)

    def _error(
        self,
        token: Token,
        message: str,
    ) -> ParseError:
        self._parse_error(token, message)
        return self.ParseError()

    def _synchronize(self) -> None:
        self._advance()

        while not self._is_at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return

            match self._peek().type:
                case (
                    TokenType.CLASS
                    | TokenType.FUN
                    | TokenType.VAR
                    | TokenType.FOR
                    | TokenType.IF
                    | TokenType.WHILE
                    | TokenType.PRINT
                    | TokenType.RETURN
                ):
                    return
                case _:
                    self._advance()

    def _match(self, *types: TokenType) -> bool:
        for type in types:
            if self._check(type):
                self._advance()
                return True
        return False

    def _check(self, type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self._current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._tokens[self._current].type == TokenType.EOF

    def _peek(self) -> Token:
        return self._tokens[self._current]

    def _previous(self) -> Token:
        return self._tokens[self._current - 1]
