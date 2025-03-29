package stmt

import (
	"github.com/englishlayup/crafting_interpreters/golox/internal/expr"
	"github.com/englishlayup/crafting_interpreters/golox/internal/token"
)

type Stmt[R any] interface {
	accept(visitor StmtVisitor[R]) R
}

type StmtVisitor[R any] interface {
	visitBlockStmt(stmt Block[R]) R
	visitClassStmt(stmt Class[R]) R
	visitExpressionStmt(stmt Expression[R]) R
	visitFunctionStmt(stmt Function[R]) R
	visitIfStmt(stmt If[R]) R
	visitPrintStmt(stmt Print[R]) R
	visitReturnStmt(stmt Return[R]) R
	visitVarStmt(stmt Var[R]) R
	visitWhileStmt(stmt While[R]) R
}

type Block[R any] struct {
	statements []Stmt[R]
}

func (b Block[R]) accept(visitor StmtVisitor[R]) R {
	return visitor.visitBlockStmt(b)
}

type Class[R any] struct {
	name       token.Token
	superClass expr.Variable[R]
	methods    []Function[R]
}

func (c Class[R]) accept(visitor StmtVisitor[R]) R {
	return visitor.visitClassStmt(c)
}

type Expression[R any] struct {
	expression expr.Expr[R]
}

func (e Expression[R]) accept(visitor StmtVisitor[R]) R {
	return visitor.visitExpressionStmt(e)
}

type Function[R any] struct {
	name   token.Token
	params []token.Token
	body   []Stmt[R]
}

func (f Function[R]) accept(visitor StmtVisitor[R]) R {
	return visitor.visitFunctionStmt(f)
}

type If[R any] struct {
	condition  expr.Expr[R]
	thenBranch Stmt[R]
	elseBranch Stmt[R]
}

func (i If[R]) accept(visitor StmtVisitor[R]) R {
	return visitor.visitIfStmt(i)
}

type Print[R any] struct {
	expression expr.Expr[R]
}

func (p Print[R]) accept(visitor StmtVisitor[R]) R {
	return visitor.visitPrintStmt(p)
}

type Return[R any] struct {
	keyword token.Token
	value   expr.Expr[R]
}

func (r Return[R]) accept(visitor StmtVisitor[R]) R {
	return visitor.visitReturnStmt(r)
}

type Var[R any] struct {
	name        token.Token
	initializer expr.Expr[R]
}

func (v Var[R]) accept(visitor StmtVisitor[R]) R {
	return visitor.visitVarStmt(v)
}

type While[R any] struct {
	condition expr.Expr[R]
	body      Stmt[R]
}

func (w While[R]) accept(visitor StmtVisitor[R]) R {
	return visitor.visitWhileStmt(w)
}
