# /bin/env python3
import sys
from typing import overload

from ast_printer import AstPrinter
from Expr import Expr
from Token import Token
from TokenTypes import TokenType


class Lox:
    _had_error = False

    @staticmethod
    def _run_file(path: str):
        with open(path, encoding="utf-8") as f:
            Lox._run(f.read())
        if Lox._had_error:
            sys.exit(65)

    @staticmethod
    def _run_prompt():
        while True:
            line = input(">")
            if not line:
                break
            Lox._run(line)
            Lox._had_error = False

    @staticmethod
    def _run(source: str):
        from Parser import Parser
        from Scanner import Scanner
        scanner: Scanner = Scanner(source)
        tokens: list[Token] = scanner.scan_tokens()
        parser: Parser = Parser(tokens)
        expression: Expr | None = parser.parse()

        if Lox._had_error:
            return

        if not expression:
            print(None)
            return

        print(AstPrinter().print(expression))

    @overload
    @staticmethod
    def error(line: int, message: str) -> None: ...

    @overload
    @staticmethod
    def error(token: Token, message: str) -> None: ...

    @staticmethod
    def error(arg: int | Token, message: str) -> None:
        if isinstance(arg, int):
            Lox._report(arg, "", message)
        else:
            if arg.type == TokenType.EOF:
                Lox._report(arg.line, " at end", message)
            else:
                Lox._report(arg.line, f" at '{arg.lexeme}'", message)

    @staticmethod
    def _report(line: int, where: str, message: str):
        print(f"[{line}] Error{where}: {message}")
        Lox._had_error = True

    @staticmethod
    def main() -> None:
        if len(sys.argv) > 2:
            logging.error("Usage: pylox [script]")
            sys.exit(64)
        elif len(sys.argv) == 2:
            Lox._run_file(sys.argv[0])
        else:
            Lox._run_prompt()


if __name__ == "__main__":
    Lox.main()
