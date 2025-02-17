# /bin/env python3
import sys
from typing import overload

from Token import Token
from TokenTypes import TokenType
from RuntimeError import RuntimeError
from Interpreter import Interpreter
from Parser import Parser
from Scanner import Scanner
from Stmt import Stmt
from LoxCallable import LoxCallable
from LoxFunction import LoxFunction
from Resolver import Resolver
from LoxClass import LoxClass


class Lox:
    _interpreter: Interpreter = Interpreter(LoxCallable, LoxFunction, LoxClass)
    _had_error = False
    _had_runtime_error = False

    @staticmethod
    def _run_file(path: str):
        with open(path, encoding="utf-8") as f:
            Lox._run(f.read())
        if Lox._had_error:
            sys.exit(65)
        if Lox._had_runtime_error:
            sys.exit(70)

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
        scanner: Scanner = Scanner(source, Lox.error)
        tokens: list[Token] = scanner.scan_tokens()
        parser: Parser = Parser(tokens, Lox.error)
        statements: list[Stmt] = parser.parse()

        if Lox._had_error:
            return

        resolver: Resolver = Resolver(Lox._interpreter, Lox.error)
        resolver.resolve(statements)

        if Lox._had_error:
            return

        Lox._interpreter.interpret(statements, Lox.runtime_error)

    @overload
    @staticmethod
    def error(line: int, message: str) -> None: ...

    @overload
    @staticmethod
    def error(token: Token, message: str) -> None: ...

    @staticmethod
    def error(arg: int | Token, message: str) -> None:  # type: ignore[reportInconsistentOverload]
        if isinstance(arg, int):
            Lox._report(arg, "", message)
        else:
            if arg.type == TokenType.EOF:
                Lox._report(arg.line, " at end", message)
            else:
                Lox._report(arg.line, f" at '{arg.lexeme}'", message)

    @staticmethod
    def runtime_error(error: RuntimeError):
        print(f"{error}\n[line {error.token.line}]", file=sys.stderr)
        Lox._had_runtime_error = True

    @staticmethod
    def _report(line: int, where: str, message: str):
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        Lox._had_error = True

    @staticmethod
    def main() -> None:
        if len(sys.argv) > 2:
            print("Usage: pylox [script]", file=sys.stderr)
            sys.exit(64)
        elif len(sys.argv) == 2:
            Lox._run_file(sys.argv[1])
        else:
            Lox._run_prompt()


if __name__ == "__main__":
    Lox.main()
