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
            "Assign   : name: Token, value: Expr",
            "Binary   : left: Expr, operator: Token, right: Expr",
            "Grouping : expression: Expr",
            "Literal  : value: object",
            "Unary    : operator: Token, right: Expr",
            "Variable : name: Token",
        ],
    )

    define_ast(
        output_dir,
        "Stmt",
        [
            "Block      : statements: list[Stmt] ",
            "Expression : expression: Expr",
            "Print      : expression: Expr",
            "Var        : name: Token, initializer: Expr",
        ],
    )


def define_ast(output_dir: str, base_name: str, types: list[str]):
    with open(f"{output_dir}/{base_name}.py", mode="w", encoding="utf-8") as f:
        f.write(
            f"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Final, override

from Token import Token


class {base_name}(ABC):
    @abstractmethod
    def accept[R](self, visitor: Visitor[R]) -> R: ...


"""
        )

        define_visitor(f, base_name, types)
        for type in types:
            cls_name = type.split(":", maxsplit=1)[0].strip()
            fields = type.split(":", maxsplit=1)[1].strip()
            define_type(f, base_name, cls_name, fields)


def define_visitor(f: TextIO, base_name: str, types: list[str]):
    f.write("class Visitor[R]:\n")
    for type in types:
        type_name = type.split(":", maxsplit=1)[0].strip()

        f.writelines(
            [
                "    @abstractmethod\n",
                f"    def visit_{type_name}_{base_name}(self, {base_name.lower()}: {type_name}) -> R: ...\n",
                "\n",
            ]
        )


def define_type(f: TextIO, base_name: str, cls_name: str, field_list: str):
    f.write(f"class {cls_name}({base_name}):\n")
    f.write(f"    def __init__(self, {field_list}):\n")
    f.write("        super().__init__()\n")
    fields = field_list.split(",")
    for field in fields:
        field_name = field.split(":")[0].strip()
        field_type = field.split(":")[1].strip()
        f.write(f"        self.{field_name}: Final[{field_type}] = {field_name}\n")
    f.write("\n")
    f.writelines(
        [
            "    @override\n",
            "    def accept[R](self, visitor: Visitor[R]) -> R:\n",
            f"        return visitor.visit_{cls_name}_{base_name}(self)\n",
        ]
    )
    f.write("\n")


if __name__ == "__main__":
    generate_ast()
