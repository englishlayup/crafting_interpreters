package stmt

import (
	"github.com/englishlayup/crafting_interpreters/golox/internal/expr"
	"github.com/englishlayup/crafting_interpreters/golox/internal/token"
)

type Stmt[R any] interface {
	Accept(visitor StmtVisitor[R]) R
}

type StmtVisitor[R any] interface {
	VisitBlockStmt(stmt Block[R]) R
	VisitClassStmt(stmt Class[R]) R
	VisitExpressionStmt(stmt Expression[R]) R
	VisitFunctionStmt(stmt Function[R]) R
	VisitIfStmt(stmt If[R]) R
	VisitPrintStmt(stmt Print[R]) R
	VisitReturnStmt(stmt Return[R]) R
	VisitVarStmt(stmt Var[R]) R
	VisitWhileStmt(stmt While[R]) R
}

type Block[R any] struct {
	Statements []Stmt[R]
}

func (b Block[R]) Accept(visitor StmtVisitor[R]) R {
	return visitor.VisitBlockStmt(b)
}

type Class[R any] struct {
	Name       token.Token
	Superclass expr.Variable[R]
	Methods    []Function[R]
}

func (c Class[R]) Accept(visitor StmtVisitor[R]) R {
	return visitor.VisitClassStmt(c)
}

type Expression[R any] struct {
	Expression expr.Expr[R]
}

func (e Expression[R]) Accept(visitor StmtVisitor[R]) R {
	return visitor.VisitExpressionStmt(e)
}

type Function[R any] struct {
	Name   token.Token
	Params []token.Token
	Body   []Stmt[R]
}

func (f Function[R]) Accept(visitor StmtVisitor[R]) R {
	return visitor.VisitFunctionStmt(f)
}

type If[R any] struct {
	Condition  expr.Expr[R]
	Thenbranch Stmt[R]
	Elsebranch Stmt[R]
}

func (i If[R]) Accept(visitor StmtVisitor[R]) R {
	return visitor.VisitIfStmt(i)
}

type Print[R any] struct {
	Expression expr.Expr[R]
}

func (p Print[R]) Accept(visitor StmtVisitor[R]) R {
	return visitor.VisitPrintStmt(p)
}

type Return[R any] struct {
	Keyword token.Token
	Value   expr.Expr[R]
}

func (r Return[R]) Accept(visitor StmtVisitor[R]) R {
	return visitor.VisitReturnStmt(r)
}

type Var[R any] struct {
	Name        token.Token
	Initializer expr.Expr[R]
}

func (v Var[R]) Accept(visitor StmtVisitor[R]) R {
	return visitor.VisitVarStmt(v)
}

type While[R any] struct {
	Condition expr.Expr[R]
	Body      Stmt[R]
}

func (w While[R]) Accept(visitor StmtVisitor[R]) R {
	return visitor.VisitWhileStmt(w)
}
