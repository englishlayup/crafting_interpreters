import logging
import sys
from typing import TextIO


def generate_ast():
    if len(sys.argv) != 2:
        logging.error("Usage: generate_ast <output directory>")
        sys.exit(64)

    output_dir = sys.argv[1]
    define_ast(
        output_dir,
        "Expr",
        [
            "Assign   : name Token, value Expr",
            "Binary   : left Expr, operator Token, right Expr",
            "Call     : callee Expr, paren Token, arguments []Expr",
            "Get      : object Expr, name Token",
            "Grouping : expression Expr",
            "Literal  : value object",
            "Logical  : left Expr, operator Token, right Expr",
            "Set      : object Expr, name Token, value Expr",
            "Super    : keyword Token, method Token",
            "Unary    : operator Token, right Expr",
            "This     : keyword Token",
            "Variable : name Token",
        ],
    )

    define_ast(
        output_dir,
        "Stmt",
        [
            "Block      : statements []Stmt",
            "Class      : name: Token, superClass: Variable, methods: []Function",
            "Expression : expression Expr",
            "Function   : name Token, params []Token, body []Stmt",
            "If         : condition Expr, thenBranch Stmt, elseBranch Stmt",
            "Print      : expression Expr",
            "Return     : keyword Token, value Expr",
            "Var        : name Token, initializer Expr",
            "While      : condition Expr, body Stmt",
        ],
    )


def define_ast(output_dir: str, base_name: str, types: list[str]):
    with open(f"{output_dir}/{base_name}.go", mode="w", encoding="utf-8") as f:
        f.write(
            f"""import (
    Token
)

type {base_name} interface:
    accept[R any](visitor {base_name}Visitor[R]) -> R: ...
"""
        )

        define_visitor(f, base_name, types)
        for type in types:
            cls_name = type.split(":", maxsplit=1)[0].strip()
            fields = type.split(":", maxsplit=1)[1].strip()
            define_type(f, base_name, cls_name, fields)


def define_visitor(f: TextIO, base_name: str, types: list[str]):
    f.write(f"type {base_name}Visitor interface{{\n")
    for type in types:
        type_name = type.split(":", maxsplit=1)[0].strip()
        f.write(
                f"    visit{type_name}{base_name}(self, {base_name.lower()} {type_name}) R\n",
        )


def define_type(f: TextIO, base_name: str, cls_name: str, field_list: str):
    f.write(f"type {cls_name} struct{{\n")
    fields = field_list.split(",")
    for field in fields:
        field_name = field.split(":")[0].strip()
        field_type = field.split(":")[1].strip()
        f.write(f"  {field_name} {field_type}")
    f.write(f"""
func ({cls_name.lower()} {cls_name}) accept[T any](visitor {base_name}Visitor) T{{
    return visit.visit{cls_name}{base_name}({cls_name.lower()})
}}
""")


if __name__ == "__main__":
    generate_ast()
