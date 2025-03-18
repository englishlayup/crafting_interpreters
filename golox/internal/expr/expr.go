package expr

import "github.com/englishlayup/crafting_interpreters/golox/internal/token"

type Token = token.Token

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
	name  Token
	value Expr[R]
}

func (assign Assign[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitAssignExpr(assign)
}

type Binary[R any] struct {
	left     Expr[R]
	operator Token
	right    Expr[R]
}

func (binary Binary[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitBinaryExpr(binary)
}

type Call[R any] struct {
	callee    Expr[R]
	paren     Token
	arguments []Expr[R]
}

func (call Call[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitCallExpr(call)
}

type Get[R any] struct {
	object Expr[R]
	name   Token
}

func (get Get[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitGetExpr(get)
}

type Grouping[R any] struct {
	expression Expr[R]
}

func (grouping Grouping[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitGroupingExpr(grouping)
}

type Literal[R any] struct {
	value interface{}
}

func (literal Literal[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitLiteralExpr(literal)
}

type Logical[R any] struct {
	left     Expr[R]
	operator Token
	right    Expr[R]
}

func (logical Logical[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitLogicalExpr(logical)
}

type Set[R any] struct {
	object Expr[R]
	name   Token
	value  Expr[R]
}

func (set Set[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitSetExpr(set)
}

type Super[R any] struct {
	keyword Token
	method  Token
}

func (super Super[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitSuperExpr(super)
}

type Unary[R any] struct {
	operator Token
	right    Expr[R]
}

func (unary Unary[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitUnaryExpr(unary)
}

type This[R any] struct {
	keyword Token
}

func (this This[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitThisExpr(this)
}

type Variable[R any] struct {
	name Token
}

func (variable Variable[R]) accept(visitor ExprVisitor[R]) R {
	return visitor.visitVariableExpr(variable)
}
