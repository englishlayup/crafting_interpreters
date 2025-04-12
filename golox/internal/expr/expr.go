package expr

import "github.com/englishlayup/crafting_interpreters/golox/internal/token"

type Expr[R any] interface {
	Accept(visitor ExprVisitor[R]) R
}

type ExprVisitor[R any] interface {
	VisitAssignExpr(expr Assign[R]) R
	VisitBinaryExpr(expr Binary[R]) R
	VisitCallExpr(expr Call[R]) R
	VisitGetExpr(expr Get[R]) R
	VisitGroupingExpr(expr Grouping[R]) R
	VisitLiteralExpr(expr Literal[R]) R
	VisitLogicalExpr(expr Logical[R]) R
	VisitSetExpr(expr Set[R]) R
	VisitSuperExpr(expr Super[R]) R
	VisitUnaryExpr(expr Unary[R]) R
	VisitThisExpr(expr This[R]) R
	VisitVariableExpr(expr Variable[R]) R
}

type Assign[R any] struct {
	Name  token.Token
	Value Expr[R]
}

func (a Assign[R]) Accept(visitor ExprVisitor[R]) R {
	return visitor.VisitAssignExpr(a)
}

type Binary[R any] struct {
	Left     Expr[R]
	Operator token.Token
	Right    Expr[R]
}

func (b Binary[R]) Accept(visitor ExprVisitor[R]) R {
	return visitor.VisitBinaryExpr(b)
}

type Call[R any] struct {
	Callee    Expr[R]
	Paren     token.Token
	Arguments []Expr[R]
}

func (c Call[R]) Accept(visitor ExprVisitor[R]) R {
	return visitor.VisitCallExpr(c)
}

type Get[R any] struct {
	Object Expr[R]
	Name   token.Token
}

func (g Get[R]) Accept(visitor ExprVisitor[R]) R {
	return visitor.VisitGetExpr(g)
}

type Grouping[R any] struct {
	Expression Expr[R]
}

func (g Grouping[R]) Accept(visitor ExprVisitor[R]) R {
	return visitor.VisitGroupingExpr(g)
}

type Literal[R any] struct {
	Value any
}

func (l Literal[R]) Accept(visitor ExprVisitor[R]) R {
	return visitor.VisitLiteralExpr(l)
}

type Logical[R any] struct {
	Left     Expr[R]
	Operator token.Token
	Right    Expr[R]
}

func (l Logical[R]) Accept(visitor ExprVisitor[R]) R {
	return visitor.VisitLogicalExpr(l)
}

type Set[R any] struct {
	Object Expr[R]
	Name   token.Token
	Value  Expr[R]
}

func (s Set[R]) Accept(visitor ExprVisitor[R]) R {
	return visitor.VisitSetExpr(s)
}

type Super[R any] struct {
	Keyword token.Token
	Method  token.Token
}

func (s Super[R]) Accept(visitor ExprVisitor[R]) R {
	return visitor.VisitSuperExpr(s)
}

type Unary[R any] struct {
	Operator token.Token
	Right    Expr[R]
}

func (u Unary[R]) Accept(visitor ExprVisitor[R]) R {
	return visitor.VisitUnaryExpr(u)
}

type This[R any] struct {
	Keyword token.Token
}

func (t This[R]) Accept(visitor ExprVisitor[R]) R {
	return visitor.VisitThisExpr(t)
}

type Variable[R any] struct {
	Name token.Token
}

func (v Variable[R]) Accept(visitor ExprVisitor[R]) R {
	return visitor.VisitVariableExpr(v)
}
