package stmt

import "github.com/englishlayup/crafting_interpreters/golox/internal/token"

import "github.com/englishlayup/crafting_interpreters/golox/internal/expr"

type Token = token.Token

type Stmt[R any] interface {
	accept(visitor StmtVisitor[R]) R
}

type StmtVisitor[R any] interface {
	visitBlockStmt(stmt Block[R]) R
	visitClassStmt(stmt Class[R]) R
	visitExpressionStmt(stmt Expression[R]) R
	visitFunctionStmt(stmt Function[R]) R
	visitIffStmt(stmt Iff[R]) R
	visitPrintStmt(stmt Print[R]) R
	visitReternStmt(stmt Retern[R]) R
	visitVaarStmt(stmt Vaar[R]) R
	visitWhileStmt(stmt While[R]) R
}

type Block[R any] struct {
	statements []Stmt[R]
}

func (block Block[R]) accept(visitor StmtVisitor[R]) R {
	return visitor.visitBlockStmt(block)
}

type Class[R any] struct {
	name       Token
	superClass expr.Variable[R]
	methods    []Function[R]
}

func (class Class[R]) accept(visitor StmtVisitor[R]) R {
	return visitor.visitClassStmt(class)
}

type Expression[R any] struct {
	expression expr.Expr[R]
}

func (expression Expression[R]) accept(visitor StmtVisitor[R]) R {
	return visitor.visitExpressionStmt(expression)
}

type Function[R any] struct {
	name   Token
	params []Token
	body   []Stmt[R]
}

func (function Function[R]) accept(visitor StmtVisitor[R]) R {
	return visitor.visitFunctionStmt(function)
}

type Iff[R any] struct {
	condition  expr.Expr[R]
	thenBranch Stmt[R]
	elseBranch Stmt[R]
}

func (iff Iff[R]) accept(visitor StmtVisitor[R]) R {
	return visitor.visitIffStmt(iff)
}

type Print[R any] struct {
	expression expr.Expr[R]
}

func (print Print[R]) accept(visitor StmtVisitor[R]) R {
	return visitor.visitPrintStmt(print)
}

type Retern[R any] struct {
	keyword Token
	value   expr.Expr[R]
}

func (retern Retern[R]) accept(visitor StmtVisitor[R]) R {
	return visitor.visitReternStmt(retern)
}

type Vaar[R any] struct {
	name        Token
	initializer expr.Expr[R]
}

func (vaar Vaar[R]) accept(visitor StmtVisitor[R]) R {
	return visitor.visitVaarStmt(vaar)
}

type While[R any] struct {
	condition expr.Expr[R]
	body      Stmt[R]
}

func (while While[R]) accept(visitor StmtVisitor[R]) R {
	return visitor.visitWhileStmt(while)
}
