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
            "Assign   : name Token, value Expr[R]",
            "Binary   : left Expr[R], operator Token, right Expr[R]",
            "Call     : callee Expr[R], paren Token, arguments []Expr[R]",
            "Get      : object Expr[R], name Token",
            "Grouping : expression Expr[R]",
            "Literal  : value interface{}",
            "Logical  : left Expr[R], operator Token, right Expr[R]",
            "Set      : object Expr[R], name Token, value Expr[R]",
            "Super    : keyword Token, method Token",
            "Unary    : operator Token, right Expr[R]",
            "This     : keyword Token",
            "Variable : name Token",
        ],
    )

    define_ast(
        output_dir,
        "Stmt",
        [
            "Block      : statements []Stmt[R]",
            "Class      : name Token, superClass Variable[R], methods []Function[R]",
            "Expression : expression Expr[R]",
            "Function   : name Token, params []Token, body []Stmt[R]",
            "Iff        : condition Expr[R], thenBranch Stmt[R], elseBranch Stmt[R]",
            "Print      : expression Expr[R]",
            "Retern     : keyword Token, value Expr[R]",
            "Vaar       : name Token, initializer Expr[R]",
            "While      : condition Expr[R], body Stmt[R]",
        ],
    )


def define_ast(output_dir: str, base_name: str, types: list[str]):
    with open(f"{output_dir}/{base_name.lower()}.go", mode="w", encoding="utf-8") as f:
        f.write(f"""package main

type {base_name}[R any] interface {{
    accept(visitor {base_name}Visitor[R]) R
}}

""")

        define_visitor(f, base_name, types)
        for type in types:
            cls_name = type.split(":", maxsplit=1)[0].strip()
            fields = type.split(":", maxsplit=1)[1].strip()
            define_type(f, base_name, cls_name, fields)


def define_visitor(f: TextIO, base_name: str, types: list[str]):
    f.write(f"type {base_name}Visitor[R any] interface {{\n")
    for type in types:
        type_name = type.split(":", maxsplit=1)[0].strip()
        f.write(
            f"    visit{type_name}{base_name}({base_name.lower()} {type_name}[R]) R\n",
        )
    f.write("}\n\n")


def define_type(f: TextIO, base_name: str, cls_name: str, field_list: str):
    f.write(f"type {cls_name}[R any] struct {{\n")
    fields = field_list.split(",")
    for field in fields:
        field_name = field.split()[0].strip()
        field_type = field.split()[1].strip()
        f.write(f"  {field_name} {field_type}\n")
    f.write("}\n")
    f.write(f"""
func ({cls_name.lower()} {cls_name}[R]) accept(visitor {base_name}Visitor[R]) R {{
    return visitor.visit{cls_name}{base_name}({cls_name.lower()})
}}

""")


if __name__ == "__main__":
    generate_ast()
