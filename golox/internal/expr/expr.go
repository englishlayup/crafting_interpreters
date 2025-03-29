package expr

import "github.com/englishlayup/crafting_interpreters/golox/internal/token"

type Expr[R any] interface {
	accept(visitor ExprVisitor[R]) R
}

type ExprVisitor[R any] interface {
	visitAssignExpr(expr Assign[R]) R
	visitBinaryExpr(expr Binary[R]) R
	visitCallExpr(expr Call[R]) R
	visitGetExpr(expr Get[R]) R
	visitGroupingExpr(expr Grouping[R]) R
	visitLiteralExpr(expr Literal[R]) R
	visitLogicalExpr(expr Logical[R]) R
	visitSetExpr(expr Set[R]) R
	visitSuperExpr(expr Super[R]) R
	visitUnaryExpr(expr Unary[R]) R
	visitThisExpr(expr This[R]) R
	visitVariableExpr(expr Variable[R]) R
}

type Assign[R any] struct {
	name  token.Token
	value Expr[R]
}

func (a Assign[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitAssignExpr(a)
}

type Binary[R any] struct {
	left     Expr[R]
	operator token.Token
	right    Expr[R]
}

func (b Binary[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitBinaryExpr(b)
}

type Call[R any] struct {
	callee    Expr[R]
	paren     token.Token
	arguments []Expr[R]
}

func (c Call[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitCallExpr(c)
}

type Get[R any] struct {
	object Expr[R]
	name   token.Token
}

func (g Get[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitGetExpr(g)
}

type Grouping[R any] struct {
	expression Expr[R]
}

func (g Grouping[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitGroupingExpr(g)
}

type Literal[R any] struct {
	value interface{}
}

func (l Literal[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitLiteralExpr(l)
}

type Logical[R any] struct {
	left     Expr[R]
	operator token.Token
	right    Expr[R]
}

func (l Logical[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitLogicalExpr(l)
}

type Set[R any] struct {
	object Expr[R]
	name   token.Token
	value  Expr[R]
}

func (s Set[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitSetExpr(s)
}

type Super[R any] struct {
	keyword token.Token
	method  token.Token
}

func (s Super[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitSuperExpr(s)
}

type Unary[R any] struct {
	operator token.Token
	right    Expr[R]
}

func (u Unary[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitUnaryExpr(u)
}

type This[R any] struct {
	keyword token.Token
}

func (t This[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitThisExpr(t)
}

type Variable[R any] struct {
	name token.Token
}

func (v Variable[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitVariableExpr(v)
}
