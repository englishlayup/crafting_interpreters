import io
from typing import override
from Expr import Binary, Expr, Grouping, Literal, Unary, Visitor
from Token import Token
from TokenTypes import TokenType


class AstPrinter(Visitor[str]):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    @override
    def visit_Binary_Expr(self, expr: Binary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    @override
    def visit_Grouping_Expr(self, expr: Grouping) -> str:
        return self._parenthesize("group", expr.expression)

    @override
    def visit_Literal_Expr(self, expr: Literal) -> str:
        if not expr.value:
            return "nil"
        return str(expr.value)

    @override
    def visit_Unary_Expr(self, expr: Unary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.right)

    def _parenthesize(self, name: str, *expr: Expr) -> str:
        with io.StringIO() as buffer:
            buffer.write("(")
            buffer.write(name)
            for e in expr:
                buffer.write(" ")
                buffer.write(e.accept(self))
            buffer.write(")")
            s = buffer.getvalue()
        return s


def main():
    expression = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123),
        ),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67)),
    )

    print(AstPrinter().print(expression))


if __name__ == "__main__":
    main()
