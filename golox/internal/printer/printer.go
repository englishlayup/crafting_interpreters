package printer

import (
	"fmt"
	"strings"

	"github.com/englishlayup/crafting_interpreters/golox/internal/expr"
)

type Printer struct{}

// VisitAssignExpr implements expr.ExprVisitor.
func (p Printer) VisitAssignExpr(expr expr.Assign[string]) string {
	return "unimplemented"
}

// VisitBinaryExpr implements expr.ExprVisitor.
func (p Printer) VisitBinaryExpr(expr expr.Binary[string]) string {
	return p.parenthesize(expr.Operator.Lexeme, expr.Left, expr.Right)
}

// VisitCallExpr implements expr.ExprVisitor.
func (p Printer) VisitCallExpr(expr expr.Call[string]) string {
	return "unimplemented"
}

// VisitGetExpr implements expr.ExprVisitor.
func (p Printer) VisitGetExpr(expr expr.Get[string]) string {
	return "unimplemented"
}

// VisitGroupingExpr implements expr.ExprVisitor.
func (p Printer) VisitGroupingExpr(expr expr.Grouping[string]) string {
	return p.parenthesize("group", expr.Expression)
}

// VisitLiteralExpr implements expr.ExprVisitor.
func (p Printer) VisitLiteralExpr(expr expr.Literal[string]) string {
    if expr.Value == nil {
        return "nil"
    }
	return fmt.Sprintf("%v", expr.Value)
}

// VisitLogicalExpr implements expr.ExprVisitor.
func (p Printer) VisitLogicalExpr(expr expr.Logical[string]) string {
	return "unimplemented"
}

// VisitSetExpr implements expr.ExprVisitor.
func (p Printer) VisitSetExpr(expr expr.Set[string]) string {
	return "unimplemented"
}

// VisitSuperExpr implements expr.ExprVisitor.
func (p Printer) VisitSuperExpr(expr expr.Super[string]) string {
	return "unimplemented"
}

// VisitThisExpr implements expr.ExprVisitor.
func (p Printer) VisitThisExpr(expr expr.This[string]) string {
	return expr.Keyword.Lexeme
}

// VisitUnaryExpr implements expr.ExprVisitor.
func (p Printer) VisitUnaryExpr(expr expr.Unary[string]) string {
	return p.parenthesize(expr.Operator.Lexeme, expr.Right)
}

// VisitVariableExpr implements expr.ExprVisitor.
func (p Printer) VisitVariableExpr(expr expr.Variable[string]) string {
	return expr.Name.Lexeme
}

func (p Printer) Print(expression expr.Expr[string]) string {
	return expression.Accept(p)
}

func (p Printer) parenthesize(name string, exprs ...expr.Expr[string]) string {
    var builder strings.Builder
    builder.WriteString("(")
    builder.WriteString(name)
    for _, expr := range exprs{
        builder.WriteString(" ")
        builder.WriteString(expr.Accept(p))
    }
    builder.WriteString(")")
    return builder.String()
}
