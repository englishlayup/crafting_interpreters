import logging
import os
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
            "Assign   : name token.Token, value Expr[R]",
            "Binary   : left Expr[R], operator token.Token, right Expr[R]",
            "Call     : callee Expr[R], paren token.Token, arguments []Expr[R]",
            "Get      : object Expr[R], name token.Token",
            "Grouping : expression Expr[R]",
            "Literal  : value interface{}",
            "Logical  : left Expr[R], operator token.Token, right Expr[R]",
            "Set      : object Expr[R], name token.Token, value Expr[R]",
            "Super    : keyword token.Token, method token.Token",
            "Unary    : operator token.Token, right Expr[R]",
            "This     : keyword token.Token",
            "Variable : name token.Token",
        ],
    )

    define_ast(
        output_dir,
        "Stmt",
        [
            "Block      : statements []Stmt[R]",
            "Class      : name token.Token, superClass expr.Variable[R], methods []Function[R]",
            "Expression : expression expr.Expr[R]",
            "Function   : name token.Token, params []token.Token, body []Stmt[R]",
            "If        : condition expr.Expr[R], thenBranch Stmt[R], elseBranch Stmt[R]",
            "Print      : expression expr.Expr[R]",
            "Return     : keyword token.Token, value expr.Expr[R]",
            "Var       : name token.Token, initializer expr.Expr[R]",
            "While      : condition expr.Expr[R], body Stmt[R]",
        ],
    )


def define_ast(output_dir: str, base_name: str, types: list[str]):
    package_path = f"{output_dir}/internal/{base_name.lower()}"
    os.makedirs(package_path, exist_ok=True)
    import_str = ""
    if base_name == "Expr":
        import_str = 'import "github.com/englishlayup/crafting_interpreters/golox/internal/token"'
    if base_name == "Stmt":
        import_str = """import (
	"github.com/englishlayup/crafting_interpreters/golox/internal/expr"
	"github.com/englishlayup/crafting_interpreters/golox/internal/token"
)"""

    with open(
        f"{package_path}/{base_name.lower()}.go",
        mode="w",
        encoding="utf-8",
    ) as f:
        f.write(f"""package {base_name.lower()}

{import_str}

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
func ({cls_name.lower()[0]} {cls_name}[R]) accept(visitor {base_name}Visitor[R]) R {{
    return visitor.visit{cls_name}{base_name}({cls_name.lower()[0]})
}}

""")


if __name__ == "__main__":
    generate_ast()
