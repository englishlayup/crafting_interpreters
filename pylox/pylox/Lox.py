# /bin/env python3
import sys
import logging

from Token import Token


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
        from Scanner import Scanner
        scanner: Scanner = Scanner(source)
        tokens: list[Token] = scanner.scan_tokens()
        for token in tokens:
            print(token)

    @staticmethod
    def error(line: int, message: str):
        Lox._report(line, "", message)

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
